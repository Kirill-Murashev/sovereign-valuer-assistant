# Data layer (current draft)

The Data Layer will provide **structured valuation data** with **metadata-rich
responses** (value, unit, date, source, freshness, limitations). The LLM must not
invent market figures when a data tool is the appropriate source.

## Repository layout (planned)

The Data Layer is represented by the `data_hub/` directory structure:

- `data_hub/connectors/`
- `data_hub/services/`
- `data_hub/tools/`

## Current status

**Planned, not implemented.** Only structural placeholders exist; there are no connectors or tools wired into the CLI yet.

## First candidate tool

- `get_risk_free_rate(date, maturity_years)` — illustrative first integration point for risk-free or benchmark yields with full provenance in the response.

## Response expectations

Future Data Layer tools should return structured fields such as value, unit,
as-of date, source identifier, `updated_at`, staleness flags, and documented
limitations—consistent with the project’s “no silent substitution of outdated or
guessed data” rule.
