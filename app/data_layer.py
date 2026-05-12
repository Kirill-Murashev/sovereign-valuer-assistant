"""Structured valuation data helpers (Data Layer)."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

_EXPECTED_HEADER = (
    "date",
    "maturity_years",
    "value",
    "unit",
    "updated_at",
    "source",
    "notes",
)

_METHOD_LOOKUP = "direct lookup in local synthetic fixture CSV"

# Resolved relative to this module so lookups work regardless of process cwd.
_RISK_FREE_RATE_FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data_hub"
    / "risk_free_rate"
    / "sample_curve.csv"
)


def _validate_iso_date(date: str) -> str:
    if not isinstance(date, str):
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
    date = date.strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.") from exc
    return date


def _validate_maturity_years(maturity_years: int) -> int:
    if type(maturity_years) is not int or isinstance(maturity_years, bool):
        raise ValueError("maturity_years must be a positive integer.")
    if maturity_years < 1:
        raise ValueError("maturity_years must be a positive integer.")
    return maturity_years


def _parse_fixture_row(
    row: dict[str, str],
    line_number: int,
) -> tuple[str, int, dict[str, Any]]:
    try:
        row_date = row["date"].strip()
        datetime.strptime(row_date, "%Y-%m-%d")
    except (KeyError, ValueError) as exc:
        raise ValueError(
            f"Malformed risk-free rate fixture row: line {line_number}"
        ) from exc

    raw_my = row.get("maturity_years", "").strip()
    try:
        maturity = int(raw_my)
    except ValueError as exc:
        raise ValueError(
            f"Malformed risk-free rate fixture row: line {line_number}"
        ) from exc
    if maturity < 1:
        raise ValueError(
            f"Malformed risk-free rate fixture row: line {line_number}"
        )

    value_raw = row.get("value", "").strip()
    try:
        value = float(value_raw)
    except ValueError as exc:
        raise ValueError(
            f"Malformed risk-free rate fixture row: line {line_number}"
        ) from exc

    unit = row.get("unit", "").strip()
    updated_at = row.get("updated_at", "").strip()
    source = row.get("source", "").strip()
    notes = row.get("notes", "").strip()
    if not unit or not updated_at or not source:
        raise ValueError(
            f"Malformed risk-free rate fixture row: line {line_number}"
        )

    payload = {
        "value": value,
        "unit": unit,
        "date": row_date,
        "maturity_years": maturity,
        "source": source,
        "updated_at": updated_at,
        "method": _METHOD_LOOKUP,
        "is_stale": False,
        "notes": notes,
    }
    return row_date, maturity, payload


def _load_risk_free_rate_index(path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Risk-free rate fixture not found: {path}")

    index: dict[tuple[str, int], dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Malformed risk-free rate fixture row: empty header")
        normalized = tuple(
            (name or "").strip() for name in reader.fieldnames
        )
        if normalized != _EXPECTED_HEADER:
            raise ValueError(
                "Malformed risk-free rate fixture row: "
                f"unexpected header {normalized!r}"
            )

        for line_number, row in enumerate(reader, start=2):
            if not any((v or "").strip() for v in row.values()):
                continue
            key_date, maturity, payload = _parse_fixture_row(row, line_number)
            key = (key_date, maturity)
            if key in index:
                raise ValueError(
                    f"Malformed risk-free rate fixture row: duplicate key {key!r}"
                )
            index[key] = payload
    return index


def get_risk_free_rate(date: str, maturity_years: int) -> dict[str, Any]:
    """Return risk-free rate metadata for an exact date and maturity from the local fixture.

    Reads only ``data_hub/risk_free_rate/sample_curve.csv`` (synthetic sample data).
    No interpolation, network, or LLM calls.
    """
    normalized_date = _validate_iso_date(date)
    maturity = _validate_maturity_years(maturity_years)

    index = _load_risk_free_rate_index(_RISK_FREE_RATE_FIXTURE_PATH)
    dates_present = {key[0] for key in index}
    if normalized_date not in dates_present:
        raise ValueError(f"No risk-free rate data for date: {normalized_date}")

    key = (normalized_date, maturity)
    if key not in index:
        raise ValueError(
            "No risk-free rate data for maturity_years: "
            f"{maturity} on date: {normalized_date}"
        )
    return dict(index[key])
