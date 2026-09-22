# Changed Files — FIABC Canonical Terminal Readiness R1

Exact base: `3206bad6419e02c3aa12fff38e288e4faf13d82d`

## Bounded repair paths

- `rawlsing_next/pre553_independent_parity_oracle.py`
  - added the authoritative named constants `LITS_CANDIDATE_COUNT = 50` and `LITS_QUERY_ROLE_COUNT = 77`;
  - replaced only semantically identical LiTS 50/77 literal checks with those names.
- `rawlsing_next/fiabc_final_oracle_freeze_producers.py`
  - imports `LITS_CANDIDATE_COUNT` and `LITS_QUERY_ROLE_COUNT` from the authoritative oracle owner;
  - no competing values were introduced.
- `WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`
  - prefers `python3`, falls back to `python`, verifies Python major version 3, then uses one selected executable;
  - pins the exact repaired oracle/producer blobs before allowing those two paths through the existing reconciliation drift filter;
  - preserves the pre-existing source-free import/compile/pytest/static-assertion sequence.
- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/02_PRE_CANDIDATE_LOCAL_PREFLIGHT.sh`
  - adds the same fail-closed Python 3 interpreter selection;
  - preserves the pre-existing source SHA, oracle-freeze, succession, and `--preflight` command order.
- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/03_MEASURED_SIX_CELL_RUN.sh`
  - adds the same fail-closed Python 3 interpreter selection;
  - preserves the single measured-driver `--run` invocation and frozen manifest reference.

## Return-packet paths

- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/00_RETURN.md`
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/01_CHANGED_FILES.md`
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/02_STATIC_AUDIT.json`
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/03_LOCAL_QUALIFICATION_COMMAND.md`

No empirical semantics, workload constitution, candidate design, oracle law, telemetry metric, architecture-selection law, source identity, candidate ordering, or frozen six-cell order was changed.
## Follow-up qualification-test repair after user local run

- `tests/test_fiabc_terminal_completeness.py`
  - updated one hostile-test expectation from the superseded per-slot absence code to the stricter current exact-metric-set drift code; production completeness law unchanged.
- `rawlsing_next/tests/test_fiabc_final_preflight_fanin.py`
  - replaced brittle literal-in-source checking with a semantic assertion that `WVS_DISCOVERY_AUTHORITY` equals the exact successor authority, scoped to the active `_wvs_docs` validation block.
- `tests/test_ee_p2x_darwin_court_driver.py`
  - isolated legacy driver-mechanics fixtures from the independently tested T3/T4 integration seam by stubbing only live-stage accounting admission inside the unit fixture.
- `WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`
  - pins the exact repaired preflight-test Git blob and admits only that exact path through the existing reconciliation test-drift filter.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/04_LOCAL_QUALIFICATION_FAILURE_FOLLOWUP.md`
  - records the user-reported 154-pass/9-fail qualification result, static diagnosis, bounded follow-up repair, and rerun requirement.

No production FIABC, WVS, P2, PRE553, candidate, oracle, telemetry, workload, or architecture-selection implementation was modified by this follow-up.
## Final static-assertion repair after second local qualification

- `WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`
  - corrected the final WVS successor replay assertion to use the authoritative exported symbol `WVS7_LOCK2_REPLAY_IDENTITY`.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/05_LOCAL_QUALIFICATION_FINAL_ASSERTION_FOLLOWUP.md`
  - records the user-reported fully green pytest court, the final assertion typo, and the bounded repair.

No production module or semantic identity changed in this follow-up.
## Green local qualification closure

- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/06_LOCAL_SOURCE_FREE_QUALIFICATION_GREEN.md`
  - records the user-reported green source-free qualification at head `6e2b817c80fc8745354e4a54103ba97a04c4437d`, including the exact green terminal and stop boundary.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/02_STATIC_AUDIT.json`
  - records final user-local qualification PASS and clears the source-free rerun requirement.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/00_RETURN.md`
  - records final closure of the source-free canonical qualification court.

No pre-candidate freeze, oracle generation/standardization, Candidate A/B/C, or measured P2X was performed by this closure update.
