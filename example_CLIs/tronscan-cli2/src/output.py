"""Output formatting utilities: XLSX via pandas."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.config import Config

logger = logging.getLogger("tronscan")


def _flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """Recursively flatten a nested dict/list into dot-notation keys."""
    result: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            result.update(_flatten(v, key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            key = f"{prefix}.{i}" if prefix else str(i)
            result.update(_flatten(item, key))
    else:
        result[prefix] = obj
    return result


def _to_dataframe(data: Any) -> pd.DataFrame:
    """Convert API response data to a DataFrame."""
    if isinstance(data, list):
        rows = [_flatten(item) if isinstance(item, dict) else {"value": item} for item in data]
        return pd.DataFrame(rows)
    if isinstance(data, dict):
        # Try to find the list payload (data, results, items…)
        for key in ("data", "results", "items", "records"):
            if isinstance(data.get(key), list):
                return _to_dataframe(data[key])
        # Single object — one-row frame
        return pd.DataFrame([_flatten(data)])
    return pd.DataFrame([{"value": data}])


def _timestamped_path(base_dir: str, stem: str, suffix: str) -> Path:
    """Build an output file path with timestamp appended to stem."""
    ts = datetime.now().strftime(Config.TIMESTAMP_FORMAT)
    out_dir = Path(base_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{stem}_{ts}{suffix}"


def save_xlsx(
    data: Any,
    stem: str = "results",
    output_dir: Optional[str] = None,
    output_file: Optional[str] = None,
) -> Path:
    """Save API response data to an XLSX file.

    Args:
        data: API response (dict or list).
        stem: Base filename (without extension/timestamp).
        output_dir: Directory for timestamped output. Ignored if output_file given.
        output_file: Explicit file path (no timestamp added).

    Returns:
        Path to the written file.
    """
    df = _to_dataframe(data)

    # Format numeric floats with 0 decimal places where appropriate
    for col in df.select_dtypes(include="float").columns:
        if (df[col] % 1 == 0).all():
            df[col] = df[col].astype("Int64")

    if output_file:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        dir_ = output_dir or Config.OUTPUT_DIR
        path = _timestamped_path(dir_, stem, ".xlsx")

    df.to_excel(path, index=False, engine="openpyxl")
    logger.info("Saved %d rows → %s", len(df), path)
    return path


def print_json(data: Any) -> None:
    """Pretty-print data to stdout as JSON."""
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
