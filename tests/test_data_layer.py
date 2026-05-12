import textwrap

import pytest

from app import data_layer
from app.data_layer import get_risk_free_rate


def test_get_risk_free_rate_success():
    result = get_risk_free_rate("2026-05-06", 10)
    assert result["value"] == 15.0
    assert result["unit"] == "% per annum"
    assert result["date"] == "2026-05-06"
    assert result["maturity_years"] == 10


def test_get_risk_free_rate_metadata_fields():
    result = get_risk_free_rate("2026-05-06", 1)
    required = {
        "value",
        "unit",
        "date",
        "maturity_years",
        "source",
        "updated_at",
        "method",
        "is_stale",
        "notes",
    }
    assert set(result.keys()) == required
    assert result["method"] == "direct lookup in local synthetic fixture CSV"
    assert result["is_stale"] is False
    assert result["updated_at"] == "2026-05-06T12:00:00Z"


def test_get_risk_free_rate_source_is_local_fixture():
    result = get_risk_free_rate("2026-05-06", 5)
    assert result["source"].startswith("local_fixture:")


def test_get_risk_free_rate_notes_synthetic_disclaimer():
    result = get_risk_free_rate("2026-05-06", 3)
    notes_lower = result["notes"].lower()
    assert "synthetic" in notes_lower
    assert "not a live market feed" in notes_lower


def test_invalid_date_format():
    with pytest.raises(ValueError, match="Invalid date format"):
        get_risk_free_rate("06-05-2026", 1)


def test_invalid_calendar_date():
    with pytest.raises(ValueError, match="Invalid date format"):
        get_risk_free_rate("2026-02-30", 1)


def test_unsupported_date():
    with pytest.raises(ValueError, match="No risk-free rate data for date: 2020-01-01"):
        get_risk_free_rate("2020-01-01", 1)


def test_unsupported_maturity():
    with pytest.raises(
        ValueError,
        match=r"No risk-free rate data for maturity_years: 2 on date: 2026-05-06",
    ):
        get_risk_free_rate("2026-05-06", 2)


@pytest.mark.parametrize("bad_maturity", [0, -1])
def test_non_positive_maturity(bad_maturity):
    with pytest.raises(ValueError, match="maturity_years must be a positive integer"):
        get_risk_free_rate("2026-05-06", bad_maturity)


def test_malformed_fixture_row(monkeypatch, tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        textwrap.dedent(
            """\
            date,maturity_years,value,unit,updated_at,source,notes
            2026-05-06,not-an-int,12.0,% per annum,2026-05-06T12:00:00Z,local_fixture:x,x
            """
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(data_layer, "_RISK_FREE_RATE_FIXTURE_PATH", bad_csv)
    with pytest.raises(ValueError, match="Malformed risk-free rate fixture row"):
        get_risk_free_rate("2026-05-06", 1)
