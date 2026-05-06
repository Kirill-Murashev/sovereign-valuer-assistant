# Data Layer (Current Draft)

The Data Layer is represented by the `data_hub/` directory structure:

- `data_hub/connectors/`
- `data_hub/services/`
- `data_hub/tools/`

Current status: planned, not implemented yet (only structural placeholders exist).

First candidate tool:
- `get_risk_free_rate(date, maturity_years)`

Future Data Layer tools should return metadata-rich responses (value, unit, date, source, freshness, limitations) and should not let the LLM invent structured market data.
