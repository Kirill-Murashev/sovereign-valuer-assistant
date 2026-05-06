# Contributing

Thank you for contributing to Sovereign Valuer Assistant.

This project is early-stage and evolves in small, controlled increments.

## Before You Start

- Read `AGENTS.md` first.
- Read `PROJECT_CONTEXT.md` and `README.md` for current scope and constraints.
- Keep changes small, focused, and easy to review.

## Required Safety Rules

Do not commit:
- secrets or credentials;
- confidential valuation reports;
- private or personal data.

Do not implement:
- uncontrolled memory writes;
- hidden autonomous self-modifying behavior.

## Development and Tests

Run tests locally before opening a PR:

```bash
python -m pytest -q
```

## Proposing Larger Architectural Changes

For larger changes, open an issue or PR proposal first with:

1. the problem being solved;
2. files/modules expected to change;
3. dependencies (if any);
4. risks and trade-offs;
5. test plan;
6. migration/rollback considerations if relevant.

Major architectural or methodological changes require explicit maintainer approval before implementation.

