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
## LiTS representation-blocker investigation

- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/08_LITS_REPRESENTATION_DIAGNOSTIC.py`
  - candidate-neutral local diagnostic for exact q301_2/q301_7 decoder representation classes and current typed physical-key matches; does not mint semantic authority.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/09_LITS_REPRESENTATION_BLOCKER_HOLDING.md`
  - documents the old canonicalized-key vs current typed-key transition and holds LiTS oracle production pending representation-authority closure.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/02_STATIC_AUDIT.json`
  - records the local pre-candidate blocker and exact historical/current owner identities.
- `WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/00_RETURN.md`
  - records the lawful pre-candidate entry and representation blocker.

A speculative `exact_cell()` production repair was explored in intermediate commits and then fully reverted. Final production/test/qualification-script blobs are restored to their previously qualified content; no unqualified numeric coercion remains in the tree.

## LiTS representation-authority closure and qualification

- `rawlsing_next/fiabc_lits_i_representation_authority.py`
  - binds only the exact LiTS-I source, q301_2/q301_7 identities, seven
    decoder-observed float64 tokens, exact banked Decimal tokens, exact system
    missing, historical owner blob, and accepted projection/release/replay;
  - states explicit no-generic-coercion, no-other-source/variable, no-label,
    no-missingness-inference, no-semantic-remap, and no-candidate limits.
- `rawlsing_next/fiabc_final_oracle_freeze_producers.py`
  - loads the exact accepted historical physical-key owner by commit/blob;
  - applies only the bounded representation bridge;
  - fails closed unless the accepted C11 release and replay identities are
    reproduced exactly;
  - freezes the representation authority into LiTS court/provenance material.
- `rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py`
  - adds focused hostile/source-free coverage, including the complete banked
    projection conversion.
- `WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`
  - pins the new production/test blobs and includes them in the complete court.
- `10_LITS_REPRESENTATION_AUTHORITY_CLOSURE.md`
- `11_LITS_REPRESENTATION_AUTHORITY_OBJECT.json`
- `12_LITS_REPRESENTATION_SOURCE_FREE_QUALIFICATION_GREEN.md`

Exact qualified code head: `d1833f9ebe363258575c6bd95737eb8f1b0f4154`.
Result: `172 passed, 28 subtests passed`, exact green terminal emitted.

No source-backed oracle, T3, Candidate A/B/C, or measured P2X ran during this
repair or qualification.

## Post-qualification launch-guard rebind

- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/02_PRE_CANDIDATE_LOCAL_PREFLIGHT.sh`
- `WORKER_RETURNS/FIABC-FINAL-LAUNCH-FANIN-R1/03_MEASURED_SIX_CELL_RUN.sh`
  - now require qualified code head `d1833f9ebe363258575c6bd95737eb8f1b0f4154`;
  - now require qualification closure head `2d93017626a2815d84fd13123ac872047614c353`;
  - preserve the dedicated execution branch and exact post-green path allowlist.
- `13_LITS_REPRESENTATION_EXECUTION_GUARD_REBIND.md`
  - records the lawful fast-forward condition and unchanged stop boundary.
