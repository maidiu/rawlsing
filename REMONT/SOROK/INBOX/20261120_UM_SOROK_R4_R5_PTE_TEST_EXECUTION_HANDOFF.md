# REMONT/SOROK intake — UM-SOROK R4/R5 builder execution and defect handoff

**2026-11-20 (America/New_York) · Provisional external-builder intake · DO NOT ASSIGN CANONICAL SR-P/T/E IDs WITHOUT REMONT CUSTODIAN RECONCILIATION**

## Authority, scope, frozen provenance

- **Receiving baseline:** REMONTATHON PR #1171 R8 at `d03e8a681ad5cf27c6b9ee63f70e8bc80ec88764`, observed live before handoff. Existing P001–P069, T0 confirmed, E6 holds and R8's **171 normal + 171 optimized local author-executed passes** are **not altered** by this intake. No native or protected receiving.
- **Source being handed over:** UM-SOROK [R4 PR #1172](https://github.com/maidiu/rawlsing/pull/1172), whose GitHub Actions workflow was committed at `e675ed0005bffce0aa21d5df641e40170ad36858`; and [R5 PR #1175](https://github.com/maidiu/rawlsing/pull/1175), source cut `782b7f377bcac4873bbf4a6dccbc567d99c368b5` (recheck its HEAD on receipt). **R5 currently inherits R7 `5bdaaeb8a6e4fd99d76402a9c85bd1fd0f0e4400`, not R8**. Its R4/R5 psychological changes have not been tested together on a cold, exact-HEAD runtime.
- **Ownership:** SOROK organism builder logged these findings but is **not** the separate REMONT engineer, independent reviewer or native owner. REMONT controls triage, identity allocation, red/green reproduction, repair and changes to existing P/T/E status. This handoff is a proposed ledger intake on an **isolated branch**, not a silent mutation of the active #1171 repair branch. No PROGRAMMA or paired CURRENT_PROGRESS was altered.

## Queue T — source-identified harness problem, not a claimed red/green test

**R5-T-INBOX-01 — Original R4 `unittest` fixture incompatible with method injection.**

- **First source fault:** During migration of the 11 R4 tests to `unittest.TestCase`, `test_runtime_private_pre_event_metabolism_is_not_public_expression(tmp_path)` retained pytest's `tmp_path` fixture parameter. Native `unittest` invokes the bound method without that fixture. This is a code-inspected test-harness defect, **not** a separately logged executed failure.
- **Builder source correction:** `739da5a149c8c55f9069bdc610f26f987fcdb54e`; method takes `self`, creates a Python `tempfile` directory and registers cleanup. Later present in #1175 source. **No post-repair unittest execution receipt**.
- **REMONT test obligation:** Execute the exact offending test on the original before-fix commit to obtain an honest red witness where possible; execute corrected test and complete R4/R5 court at a frozen later commit. Record runner, SHA, commands, output and independent review before any closure.
- **Status:** `STATIC_SOURCE_FAULT_IDENTIFIED__BUILDER_SOURCE_CORRECTED__RED_GREEN_UNVERIFIED`. Do not increment confirmed T or label repaired/tested until custodian verifies.

## Queue E — unavailable execution, stale integration and receiving

**R5-E-INBOX-01 — GitHub Actions jobs produced no Python test receipt.**

- At R4 workflow SHA `e675ed0005bffce0aa21d5df641e40170ad36858`, GitHub Actions run IDs **44675087533** (push) and **44675093891** (PR) were observed failed with zero reported job steps and unavailable job logs. That is **not** a Python traceback, a red unit test or evidence the test commands ran.
- **Requirement:** Establish a real exact-source runner using REMONT's proven *cold archive / checkout, source identity and full normal + optimized test* practice. Where Actions refuses to start, capture the precise GitHub workflow/job configuration or runner dispatch explanation rather than forging Python results. Runner can be local/independently controlled; CI is not mandatory.
- **Status:** `EXECUTION_EVIDENCE_HOLD`; no author/tested success at R4/R5.

**R5-E-INBOX-02 — Parent has moved; merged R5+R8 not executed.**

- The R5 branch was based on the legitimate R7 head, but #1171 later reached R8 at `d03e8a... `; R8 fixes SR-P064–069 in background history, typed sensory input and project admission. R5 is therefore not a verified carrier of those fixes.
- **Requirement:** Have the **authorized integrator** build a fresh R8-derived candidate, reconcile the overlapping `constitution.py`/`development.py` changes and report exact merge hunks. Run R8 + R4 + R5 tests in one cold directory. Do **not** overwrite the active R8 REMONT repair branch or silently declare the R5 branch fully up-to-date.
- **Status:** `INTEGRATION_CURRENTNESS_HOLD` until exact source and regression receipt; no owner/protected rights.

**R5-E-INBOX-03 — Independent psychological validation and receiving missing.**

- The new relational-motif algorithm is sourcefree; no independent G5, CAN/ADP psychological issuance, PYAT source-conditioned whole-person validation, protected receiving or scientific accreditation. This overlaps the existing E ledger, **not a request for a newly minted E closure/status change**.

## Queue P — test obligations and possible functional defects, NOT yet reproduced production failures

**R5-P-INBOX-01 — Coupled historical-motif recruitment and inhibition requires adversarial receiving.**

- R5 introduces `RECRUIT_FORM` into the `constitution.compose` fixed-point loop. It may indirectly recruit already acquired third forms through a configuration containing an inhibited form, but must not restore the inhibited form's direct action, bypass body/scope/actor-access rules, self-bootstrap a project, or produce an endless activation/veto cycle.
- **Candidate negative tests authored, not run:** `tests/test_relational_recruitment_r5.py` contains **6 native unittest cases** for indirect recruitment; no motific edge; location mismatch; body limit; missing ritual cue; and unearned `inferred_hidden_trauma` target. **11 R4 `unittest` cases** remain in `tests/test_relational_metabolism_r4.py`. Test discovery counts must be reported as discovered, not inferred from the filenames.
- **Further REMONT falsifiers needed:** multi-motif cyclic recruitment/suppression with bounded termination; deep three-hop contextual scope and typed source access; changed historical relation followed by a *later* different encounter and measurable difference in actual actor-owned options; preservation of independent Other consent/physical nonfeasibility; no private analytical `historical_psychodynamic_context` leaking to public expression or actor self-account; invalid model proposal after a valid mutation must rollback atomically; persistent SQLite cold reopen and hash/owner verification.
- **Status:** `CAPABILITY_AND_CORRECTNESS_RISK__NO_FIRST_FAULT_REPRODUCED`; not automatically a confirmed SR-P defect. Only REMONT may assign a native ID and repair.

## Required exact-source execution matrix

1. **Freeze branch/commit and archive source.** Record `git rev-parse HEAD`, source SHA-256 manifest, base lineage, Python version and external dependencies; no tests on moving refs.
2. **Establish first negative and positive witnesses.** Run the tests as they exist at the frozen source; any observed failure must be classified by first owner (P vs T vs E), with raw output preserved before any repair.
3. **Run full research tests** in `SEAM/ORACLE/UM_SOROK_ORGANISM_R3/`:
   - `python -m unittest discover -s tests -v`
   - `python -O -m unittest discover -s tests -q`
   - `python -m unittest tests.test_relational_metabolism_r4 tests.test_relational_recruitment_r5 -v` where import resolution permits; otherwise use `unittest discover` and named `-p` files.
   - `python -m um_sorok_organism demo --db /tmp/sorok_r5_remont.sqlite3`; close and reopen the SQLite ledger, verify event chain and actor/world consistency.
4. **Inherited historical R8 benchmark:** 171 normal+optimized passes on R8 only. R4 author wrote 11 test methods and R5 6 additional methods. If a complete R8-integrated candidate discovers all distinct tests, **188 is an arithmetic expectation, not an observed execution count or guaranteed passing denominator**.
5. **Record proof:** exact green and red logs, source identities, cold-extraction runner, `python -O` behavior, no private disclosure, no result attribution to another commit, and explicit REMONT review/receiving grade.

## Disposition and routing

**`BUILDER_TO_REMONT_INBOX__EVIDENCE_UNEXECUTED__OWNERSHIP_UNTRANSFERRED_UNTIL_REMONT_ACK`.** Do not promote counts (R8 P69, T0, E6) merely because intake items are appended. No repairs to the organism are being assigned back to the original builder in this document. The construction priority remains broad integrated SOROK progress, with *separate* REMONT defect triage and negative-proof custody.
