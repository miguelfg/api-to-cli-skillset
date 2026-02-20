"""
Output formatting and export helpers.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def _as_frame(payload: Any) -> pd.DataFrame:
    """Convert arbitrary API payload into a DataFrame."""
    if isinstance(payload, list):
        return pd.json_normalize(payload)
    if isinstance(payload, dict):
        return pd.json_normalize([payload])
    return pd.DataFrame([{"value": payload}])


def save_output(payload: Any, output_format: str, output_dir: str, stem: str = "results") -> Path:
    """Save output in json/csv/xlsx format."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if output_format == "json":
        path = out_dir / f"{stem}_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
        return path

    frame = _as_frame(payload)
    if output_format == "csv":
        path = out_dir / f"{stem}_{ts}.csv"
        frame.to_csv(path, index=False)
        return path

    if output_format == "xlsx":
        path = out_dir / f"{stem}_{ts}.xlsx"
        frame.to_excel(path, index=False, engine="openpyxl")
        return path

    raise ValueError(f"Unsupported output format: {output_format}")
