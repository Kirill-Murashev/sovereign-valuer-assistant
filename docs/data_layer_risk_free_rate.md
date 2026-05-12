# Data Layer design: risk-free rate (`get_risk_free_rate`)

This document defines the **design** for the first planned Data Layer tool. It is **documentation only**: nothing here is implemented as production code yet.

Related overview: [data_layer.md](data_layer.md).

---

## 1. Purpose

A **risk-free rate** (or government-benchmark yield used as a risk-free proxy) is **structured numeric market data**, not narrative knowledge.

It belongs in the **Data Layer**, not in RAG and not as LLM free text, because:

- valuation models need **reproducible inputs** (same request → same sourced value under the same dataset version);
- every value must carry **source identity** and **as-of timestamp** so reports can cite provenance;
- **LLMs must not invent** yields, curves, or “typical” rates when a tool is the correct source of truth.

RAG may hold methodology text; the Data Layer holds **facts** with metadata. If the tool cannot return data, the system must surface an **explicit error**, not a guessed number.

---

## 2. Tool contract (planned)

```text
get_risk_free_rate(date: str, maturity_years: int) -> dict
```

### Inputs

| Argument | Type | Meaning |
|----------|------|--------|
| `date` | `str` | **ISO 8601** calendar date: `YYYY-MM-DD` (as-of date for the observation). |
| `maturity_years` | `int` | Integer maturity in **whole years** (e.g. `1`, `2`, `5`, `10`). |

Validation rules (design):

- `date` must parse as a valid calendar date.
- `maturity_years` must be a **supported** maturity for the active dataset (exact allowed set is defined with the fixture or provider schema).

### Output shape

The function returns a **dictionary** (JSON-serializable). Example shape:

```json
{
  "value": 14.2,
  "unit": "% per annum",
  "date": "2026-05-06",
  "maturity_years": 10,
  "source": "local_fixture:ofz_sample_v1",
  "updated_at": "2026-05-06T12:00:00Z",
  "method": "linear interpolation between adjacent tenors in local CSV (design)",
  "is_stale": false,
  "notes": "Sample data for development; not a live market feed."
}
```

**Typing note:** During implementation, `value` should preferably be a **float** (or `Decimal` if the project later standardizes on it). The design allows a string placeholder in examples only for human readability; production shape should be consistent and documented in code.

Required keys (minimum contract):

- `value` — numeric yield (interpret with `unit`).
- `unit` — e.g. `% per annum`.
- `date` — as-of date echoed or normalized to ISO `YYYY-MM-DD`.
- `maturity_years` — echoed maturity.
- `source` — stable identifier for the dataset or provider (e.g. `local_fixture:...` or future `provider:...`).
- `updated_at` — when this record was last updated in the local store or ingested (ISO 8601 timestamp).
- `method` — short human-readable description (interpolation rule, primary tenor, etc.).
- `is_stale` — boolean under the staleness policy (see section 5).
- `notes` — limitations, fixture disclaimer, or interpolation caveats.

---

## 3. Candidate source (conceptual)

**Preferred conceptual source:** sovereign / government bond yield curve data (e.g. **OFZ** curve in the Russian market context), or another **deterministic, inspectable** source chosen by the maintainer.

Design constraints:

- The source must be **inspectable** (file, documented API response, or versioned local table).
- **v0.4 first implementation** should **not** depend on a specific external commercial API unless explicitly approved later.
- **Initial implementation** may use:
  - a **local CSV** fixture under `data_hub/`; or
  - a **small hand-maintained** sample dataset checked into the repo only if it is **synthetic or clearly licensed** for redistribution.

**Live API integration** can be added later behind a small adapter interface, without changing the public contract of `get_risk_free_rate` beyond richer `source` / `method` strings.

---

## 4. Offline / mock-first implementation

**v0.4 should start without network I/O:**

- ship **local deterministic** sample data under `data_hub/` (path to be chosen during implementation);
- **unit tests** must use fixtures only — **no live HTTP**, no reliance on external availability;
- a later **provider adapter** may replace or extend the local loader while preserving the same response envelope and error behaviour.

This keeps CI reproducible and avoids silent “best effort” scraping.

---

## 5. Staleness policy

Every successful response must include **`updated_at`** and **`is_stale`**.

**Initial policy (simple, documented):**

- Define a maximum acceptable age `T_max` (e.g. number of calendar days) for the sample dataset, **or** compare `updated_at` to “today” in tests with a frozen clock.
- If the observation is older than the policy allows, set `is_stale: true` and keep the numeric `value` **only if** the design explicitly allows returning stale values with a flag; otherwise prefer an **error** (project decision at implementation time — either behaviour must be **tested**, not silent).

**Rule:** stale data must **never** be silently treated as current. Callers (CLI, skills, future orchestration) must surface staleness to the user or downstream prompts.

---

## 6. Error policy

Errors must be **explicit** and **testable** (e.g. dedicated exception types or structured error dicts — final choice at implementation time).

| Condition | Expected behaviour |
|-----------|---------------------|
| Invalid `date` format or non-existent calendar date | Reject with clear validation error. |
| Unsupported `maturity_years` | Reject with “unsupported maturity” (include allowed set in message or docs). |
| No row for requested `date` in local data | “missing data for date” error — **no** invented interpolation from unrelated dates unless explicitly specified and tested. |
| Malformed local CSV / schema drift | Parse error with file path and line hint where practical. |
| Provider unavailable (future network path) | Distinct “provider unavailable” error — **no** silent fallback to another provider. |

The LLM must **not** substitute a guessed rate when any of the above occurs.

---

## 7. Relationship to valuation workflow

`get_risk_free_rate` provides **input data** for models and checks, not a valuation conclusion.

Typical uses:

- **Discount rate build-up** (risk-free component).
- **CAPM / cost of equity** (risk-free leg).
- **Income approach** assumptions and sensitivity tables.
- **Report review**: compare stated risk-free assumption in a report fragment against sourced tool output (future skill integration).

The tool returns **facts + metadata**; professional judgement remains with the valuer.

---

## 8. Relationship to LLM and RAG

- **LLM** may **request** tool output or **cite** it when included in a prompt with explicit provenance.
- **RAG** may retrieve **methodology** (how to choose a rate, standards text).
- **Data Layer** supplies **numeric** results and **source/time** metadata.
- If the Data Layer returns **no data** or an **error**, the LLM must **not** invent a substitute yield.

---

## 9. Planned repository structure (future)

No files are created by this design document alone. A minimal future layout could be:

```text
data_hub/
└── risk_free_rate/
    ├── README.md              # dataset provenance and limitations
    └── sample_curve.csv       # local deterministic fixture (synthetic or approved)

app/
├── data_layer.py              # or app/data_tools.py — thin public API

tests/
└── test_data_layer.py         # fixture-based tests, no network
```

Naming is indicative; the maintainer may adjust to match existing `data_hub/` conventions.

---

## 10. v0.4 minimal implementation checklist (future)

When implementation begins, a minimal vertical slice should include:

1. **Local sample dataset** (CSV or equivalent) under `data_hub/risk_free_rate/` (or agreed path).
2. **Parser / loader** with strict schema validation.
3. **`get_risk_free_rate(date, maturity_years)`** returning the contract dict (or raising structured errors).
4. **Unit tests** covering: happy path, invalid date, unsupported maturity, missing date, malformed file, staleness flag behaviour.
5. **Callable interface** — internal Python API first; optional **CLI** flag later if desired (not required for v0.4 core).
6. **No live network** dependency in default tests and default runtime path.

---

## 11. Non-goals (explicit)

The first tool must **not** attempt to become:

- a full **macroeconomic database**;
- a **yield curve modeling engine** (beyond simple documented interpolation if ever added);
- an automatic **web scraper**;
- an uncontrolled stream of **API calls** without user configuration and tests;
- a source of **LLM-generated** interest rates;
- a **production-grade** financial data service or vendor substitute.

Those may be separate projects or much later milestones with their own governance.

---

## Roadmap note

This document **prepares v0.4**; it does **not** implement `get_risk_free_rate`. Implementation remains a future coding milestone after maintainer approval of data sourcing and error semantics.
