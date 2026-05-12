# Risk-free rate fixture (synthetic)

This directory holds **synthetic** sample data for the Data Layer
`get_risk_free_rate` helper.

**Disclaimer**

- The CSV data is **synthetic** (fabricated, not observed market quotes).
- It is intended **only for automated tests and local development**, not production.
- It is **not** a live market data feed and does not reflect real yields or curves.
- **Do not use this fixture as the basis for real valuation conclusions** or
  client-facing reports; substitute data with proper provenance and licensing first.

## Files

- `sample_curve.csv` — small CSV keyed by calendar date and whole-year maturity.
  Rows are fabricated for deterministic tests and local experimentation only.

## Schema

CSV columns:

`date`, `maturity_years`, `value`, `unit`, `updated_at`, `source`, `notes`

## Provenance

- **Source identifier:** `local_fixture:risk_free_rate_sample_v1` (in-file `source` column).
- **License:** synthetic data generated for this repository; safe to redistribute with the project.
