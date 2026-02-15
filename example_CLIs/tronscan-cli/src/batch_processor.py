"""Batch request processing from CSV files."""

import csv
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from .client import TronscanClient

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process batch requests from CSV files."""

    def __init__(self, client: TronscanClient, output_dir: str = "output"):
        """Initialize batch processor."""
        self.client = client
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    async def process_csv(
        self,
        csv_file: str,
        format: str = "json",
        include_timestamp: bool = True,
        output_file: Optional[str] = None,
    ) -> str:
        """Process batch requests from CSV file."""
        csv_path = Path(csv_file)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        logger.info(f"Processing batch file: {csv_file}")

        # Read CSV
        requests = []
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                requests.append(row)

        logger.info(f"Read {len(requests)} requests from CSV")

        # Execute requests
        results = await self._execute_requests(requests)

        # Save results
        output_path = self._get_output_path(format, include_timestamp, output_file)
        self._save_results(results, output_path, format)

        logger.info(f"Results saved to {output_path}")
        return str(output_path)

    async def _execute_requests(
        self, requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute batch requests concurrently."""
        results = []

        for idx, request in enumerate(requests, 1):
            method = request.get("method", "GET").upper()
            endpoint = request.get("endpoint", "")

            if not endpoint:
                logger.warning(f"Request {idx}: Missing endpoint, skipping")
                continue

            # Extract parameters (all fields except method and endpoint)
            params = {
                k: v for k, v in request.items()
                if k not in ["method", "endpoint"] and v
            }

            try:
                logger.debug(f"Executing request {idx}: {method} {endpoint}")

                response = await self.client.get(endpoint, params)

                results.append({
                    "request_id": idx,
                    "endpoint": endpoint,
                    "method": method,
                    "status": "success",
                    "response": response,
                    "timestamp": datetime.now().isoformat(),
                })

            except Exception as e:
                logger.error(f"Request {idx} failed: {e}")

                results.append({
                    "request_id": idx,
                    "endpoint": endpoint,
                    "method": method,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })

        return results

    def _get_output_path(
        self,
        format: str,
        include_timestamp: bool,
        custom_name: Optional[str] = None,
    ) -> Path:
        """Generate output file path."""
        if custom_name:
            return self.output_dir / custom_name

        base_name = "results"
        if include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{base_name}_{timestamp}"

        ext = "json" if format == "json" else "xlsx"
        return self.output_dir / f"{base_name}.{ext}"

    def _save_results(
        self,
        results: List[Dict[str, Any]],
        output_path: Path,
        format: str = "json",
    ):
        """Save results in specified format."""
        if format == "json":
            self._save_json(results, output_path)
        elif format == "xlsx":
            self._save_xlsx(results, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _save_json(self, results: List[Dict[str, Any]], output_path: Path):
        """Save results as JSON."""
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Saved {len(results)} results as JSON")

    def _save_xlsx(self, results: List[Dict[str, Any]], output_path: Path):
        """Save results as XLSX, flattening nested structures."""
        flattened = []

        for result in results:
            row = {
                "request_id": result.get("request_id"),
                "endpoint": result.get("endpoint"),
                "method": result.get("method"),
                "status": result.get("status"),
                "timestamp": result.get("timestamp"),
            }

            # Flatten response or error
            if result.get("status") == "success":
                response = result.get("response", {})
                if isinstance(response, dict):
                    # Add first-level response fields
                    for key, value in response.items():
                        if isinstance(value, (str, int, float, bool)):
                            row[f"response_{key}"] = value
            else:
                row["error"] = result.get("error")

            flattened.append(row)

        # Create DataFrame and export
        df = pd.DataFrame(flattened)

        # Format floats with 0 decimal places
        float_cols = df.select_dtypes(include=["float64"]).columns
        if len(float_cols) > 0:
            df[float_cols] = df[float_cols].astype("int64")

        df.to_excel(output_path, index=False, engine="openpyxl")
        logger.info(f"Saved {len(results)} results as XLSX")
