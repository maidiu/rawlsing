# A09 — Exact LMQ-013 Deployment Blocker

## Blocker token

`LMQ013_BLOCKED__NO_LIVE_POSTGRES_RUNTIME__PR27_G8_POST_REPAIR_DEPLOYMENT_AND_FRESH_EXECUTION_REQUIRED`

## Why execution stopped

A genuinely fresh A09 court requires a process with:
- the PR #27 G8 runtime tree at exact head `75aac98e0280289a717e2b49f8d2066ab1c926db` or a later exact recorded PR #27 head;
- Python runtime modules used by the smoke (`pandas`, `pyarrow`, `psycopg2`, `yaml`);
- a reachable live respondent PostgreSQL `DATABASE_URL`;
- post-PG8 UID/QSM and facet-ready views deployed into that database;
- all six V550→V552J compiler entrypoints and runtime authority directories.

This connected worker has GitHub repository access, but not a live respondent PostgreSQL execution process. The A09 starting commit also has no associated workflow run that supplies such a runtime.

## Last recorded deployment state

PR #27 says G8 is open for post-repair live DB deployment + 35-scope preflight + 9-scope full-J canary + broader `CLOSED_35` smoke.

PR #60 fixed the positional view migration defect and explicitly states that it performed no live production DB mutation.

Therefore the deployment step must be executed, not presumed.

## Minimum safe action

Safest single idempotent deployment action after checking out the current PR #27 head:

```bash
export DATABASE_URL='postgresql://...'
python data/ddm_build_copy/apply_postgres_facet_ready_substrate.py
```

Then execute the A09 preflight and fresh courts described in `RESULT.md`.

A narrower `--views-only` rerun is lawful only if an operator first verifies that the SWID respondent identity/QSM state and required tables were already successfully deployed; A09 cannot verify that state from GitHub alone.
