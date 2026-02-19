"""Batch processor for TXT (JSON Lines) input files.

Each line in the input file is a JSON object specifying the command to run:

    {"command": "accounts-list", "limit": 20, "sort": "-balance"}
    {"command": "accounts-get", "address": "TAddr..."}
    {"command": "blocks-list", "limit": 10}
    {"command": "blocks-stats"}
    {"command": "contracts-list", "search": "USDT", "limit": 20}
    {"command": "contracts-get", "contract": "TAddr..."}
    {"command": "contracts-events", "contract_address": "TAddr...", "term": "Transfer", "limit": 50}

Supported command values:
    accounts-list, accounts-get, accounts-tokens,
    blocks-list, blocks-stats,
    contracts-list, contracts-get, contracts-events
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from src.client import TronscanClient
from src.config import Config
from src.output import _to_dataframe

logger = logging.getLogger("tronscan")


def _run_command(client: TronscanClient, entry: Dict[str, Any]) -> Any:
    """Dispatch a single JSON Lines entry to the appropriate API call."""
    command = entry.get("command", "").strip()

    if command == "accounts-list":
        return client.get("/api/account/list", params={
            "start": entry.get("start", 0),
            "limit": entry.get("limit", 10),
            "sort": entry.get("sort"),
        })

    if command == "accounts-get":
        return client.get("/api/accountv2", params={"address": entry["address"]})

    if command == "accounts-tokens":
        return client.get("/api/account/tokens", params={
            "address": entry["address"],
            "start": entry.get("start", 0),
            "limit": entry.get("limit", 10),
            "hidden": entry.get("hidden", False),
            "sortBy": entry.get("sort_by"),
        })

    if command == "blocks-list":
        return client.get("/api/block", params={
            "start": entry.get("start", 0),
            "limit": entry.get("limit", 10),
            "producer": entry.get("producer"),
            "sort": entry.get("sort", "-number"),
            "start_timestamp": entry.get("start_timestamp"),
        })

    if command == "blocks-stats":
        return client.get("/api/block/statistic")

    if command == "contracts-list":
        return client.get("/api/contracts", params={
            "search": entry.get("search"),
            "start": entry.get("start", 0),
            "limit": entry.get("limit", 10),
            "sort": entry.get("sort"),
            "open-source-only": entry.get("open_source_only") or None,
        })

    if command == "contracts-get":
        return client.get("/api/contract", params={"contract": entry["contract"]})

    if command == "contracts-events":
        return client.post("/api/contracts/smart-contract-triggers-batch", json={
            "contractAddress": entry.get("contract_address"),
            "hashList": entry.get("hashes", []),
            "term": entry.get("term"),
            "limit": entry.get("limit", 20),
        })

    raise ValueError(f"Unknown command: {command!r}")


def process_batch(
    input_file: str,
    output_dir: str,
    client: TronscanClient,
    dry_run: bool = False,
) -> Path:
    """Process a TXT (JSON Lines) batch file and save results to XLSX.

    Args:
        input_file: Path to the .txt file (one JSON object per line).
        output_dir: Directory for XLSX output.
        client: Configured TronscanClient instance.
        dry_run: If True, parse and validate only — do not call API.

    Returns:
        Path to the generated XLSX file.
    """
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Batch input file not found: {input_file}")

    entries: List[Dict[str, Any]] = []
    with open(input_path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as exc:
                logger.warning("Line %d: invalid JSON — %s", lineno, exc)

    logger.info("Batch: %d entries loaded from %s", len(entries), input_path.name)

    results: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    for idx, entry in enumerate(entries, start=1):
        command = entry.get("command", "<missing>")
        if dry_run:
            logger.info("[%d/%d] DRY RUN  %s", idx, len(entries), entry)
            continue
        try:
            data = _run_command(client, entry)
            row_df = _to_dataframe(data)
            row_df.insert(0, "_command", command)
            row_df.insert(1, "_entry_index", idx)
            results.append(row_df)
            logger.info("[%d/%d] OK  %s", idx, len(entries), command)
        except Exception as exc:  # noqa: BLE001
            logger.error("[%d/%d] FAIL  %s — %s", idx, len(entries), command, exc)
            errors.append({"entry_index": idx, "command": command, "error": str(exc)})

    if dry_run:
        logger.info("DRY RUN complete — %d entries would be processed", len(entries))
        return Path(output_dir) / "dry_run_preview.txt"

    # --- Build output XLSX with multiple sheets ---
    ts = datetime.now().strftime(Config.TIMESTAMP_FORMAT)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"batch_results_{ts}.xlsx"

    results_df = pd.concat(results, ignore_index=True) if results else pd.DataFrame()
    errors_df = pd.DataFrame(errors)
    summary_df = pd.DataFrame([{
        "total": len(entries),
        "success": len(results),
        "errors": len(errors),
        "timestamp": ts,
        "input_file": str(input_path),
    }])

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        if not results_df.empty:
            results_df.to_excel(writer, sheet_name="Results", index=False)
        if not errors_df.empty:
            errors_df.to_excel(writer, sheet_name="Errors", index=False)

    logger.info(
        "Batch complete: %d ok, %d errors → %s",
        len(results),
        len(errors),
        out_path,
    )
    return out_path
