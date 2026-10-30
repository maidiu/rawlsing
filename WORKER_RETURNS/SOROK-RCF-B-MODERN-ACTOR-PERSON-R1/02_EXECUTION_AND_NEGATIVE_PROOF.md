# RCF-B — execution and negative proof

Observed FINDING: the BP4R episode-origin/C9-writer-version candidate is executable on the BP2P4J base and passes 9/9 under the same receiving test consumer. Causal INTERPRETATION: the C12 fork location and immutable episode origin, and the C9 supported-writer schema, are separable and can be checked before a shared consumer. Proposed HQ ACTION: owner-review this subset while keeping C9 R3B actor durability, G17/M04R and F1CR out of the integrated selection. Accountable OWNER: BP4/C12, C9 R3B, F1C/R31J and original component owners.

## Environment

PRE-MAIN readback `750548ddbb9b4392a16ce93097b856f349e16182`; worktree isolated at that head. Device `oldMac`; OpenCode 1.18.34; `opencode-go/deepseek-v4.1-flash`, local session variant `max`; Python 3.11.3; pytest 9.1.1; SQLite 3.40.1. No native source, no original survey, no production DB.

## Actual S2 probe — BP4R on BP2P4J base

Setup: detached BP2P4J worktree at `5b3e6577400ea1d88971ae6b48e41a118b8059ae`; overlay BP4R candidate `candidate/bp2p4/c12_guard.py` blob `e0d9d904…` and `candidate/c9_actor_r3.py` blob `b9000cdb…`; test blob `3057e06f…`; C9 dependency directory set via `BP4R_C9_DIR`.

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 BP2P4J_ORIGIN_RUNTIME=off \
BP4R_C9_DIR=<c9-dir> python3 -m pytest tests/test_bp4r_candidate.py -q
```

Actual: **9 passed, 0 failed, 0 errors, 0 skipped**, exit 0. JUnit SHA-256 `69310122569c0feae971294065d4ed52ed36d6d2d6e3958f48447dc11af2d747`.

Executed witnesses:

1. `test_legitimate_episode_bearing_fork_passes` — real `JoinedProduct.say`, guarded fork `root`→`alt`, `verify_store` `ok/content/fork` true; SQL location `alt`, sealed body origin `root`; cold reopen preserved; fork root prefix `BP4_C12_FORK_ROOT@2`.
2. `test_forged_branch_transplant_fails_at_same_read` — transplanted child-local episode refused at the same read (`branch_id_origin_mismatch`).
3. `test_actual_c9_consumer_rejects_unsupported_writer_at_2` — actual C9 `c12_fork_guard` returns `FORK_HELD`/`C12_WRITER_SCHEMA_UNSUPPORTED` for `BP4_C12_STORE@2`.
4. `test_c9_writer_schema_gate_source_severance_red_then_restored` — severing the schema gate reproduces old `@2 → FORK_READY`; restoring returns `FORK_HELD`.
5. `test_supported_writer_still_reaches_ready_and_mirror_handshake` — `@1` remains `FORK_READY`/`READY`.
6. `test_cold_reopen_and_forced_schema_mismatch_fail_closed` — cold reopen and forced schema mismatch fail closed.
7. `test_mixed_writer_domain_is_refused` — mixed writer/mirror domain refused.
8. `test_residual_global_writer_clock_is_still_accepted_red` — **preserved RED**: perception clock 11 followed by episode clock 10 remains accepted by the writer.
9. `test_residual_anchor_actor_clock_coverage_remains_unbound_red` — **preserved RED**: changing root actors and `created_clock` leaves anchor payload unchanged; external anchor absent.

Before-repair evidence is the BP4I3/BP4R attributed record: legitimate episode fork returned `content_ok=false`, `fork_ok=true`, `episode:0:branch_id_column_body_mismatch`; C9 `@2` returned `FORK_READY` and two `@2` strings returned `READY`. The BP4R return records exact pre-repair probe JSON `evidence/08_PROBE_ORIGINAL_EPISODE_FORK.json` and `evidence/10_PROBE_ORIGINAL_C9_WRITER_VERSION.json`; not re-executed here.

## Other component courts (attributed, not rerun)

- G17I2 `95f15026…`: original 11/3 RED, patched 14/14 reviewer and 13/13 author; C9 durability HOLD. Source cut `8b9a39da…`.
- M04R `8f200fd6…`: 51/51 and 587/587, nine CAN3 RED retained; post-return owner/reviewer pending. Candidate `d9efd3f5…`.
- F1CR `03be5c2…`: 13/13 sourcefree outcomes and three live-history mutations attributed; **the patched executable `bf7e625e…` is not present at any tree path and the author blob `104f5bd7…` is only a loose blob**, so the executable was NOT_RUN by RCF-B. JOIN targetless REFUSE 1/1 is attributed and read-only.
- C9 R3B `fac064c9…`: 15/15 test-only SQL court and C9/C12 14/1 conflict attributed; `tests/test_c9_r3.py:476` old-count RED remains. RCF-B did not stage the full S36/C12 closure.
- BP4I3 `0aaf119f…`: fork/version defects and C9 external anchor HOLD preserved.
- OC5E `67a4f156…`: 49 novel + 10 previous failures, owner issuance held.
- Native F1 17 RED/X3 historical, 9 CAN3 RED and OC5 49 remain separate; no test was weakened.

## RUN / NOT_RUN

RUN: BP4R 9/9 on BP2P4J base; exact episode fork/cold/forged-transplant, C9 `@2` refusal, schema-gate severance/restore, writer clock and anchor residual RED.

NOT_RUN: C9 R3B full S36/C12 15-case staging; F1CR executable (absent); G17I2/M04R suites in this worktree (attributed from prior returns); native source/world/Rule A/T/E2/C9/C12 anchor; A0–A5 human; PRE-MAIN/PR mutation.

## First actual consumer

The tested consumer is `bp2p4.c12_guard.verify_store`/`GuardedC12Store.fork` over the BP2P4J `JoinedProduct` C12 SQLite, with the C9 `c12_fork_guard` at the same boundary. It is a sourcefree test consumer, not a native C9/C12 reader or person.

DONE: actual 9/9 cross-component probe with positive, cold, forgery and severance evidence; preserved residual REDs; exact hashes. REMAINING: owner C12 origin/anchor decision, C9 version split, F1CR code commit/adapter, G17/M04R integration decisions. CRITICAL BLOCKERS: no native C9/C12 anchor or whole-person consumer. LARGEST PRODUCTIVE MOVE: owner reviews the BP4R C12/C9 boundary and commits the missing F1CR executable before any C9R adapter. FLIGHT: local sourcefree Git/Python/SQLite only. DELTA: the episode fork and C9 writer-version edge is green under the same consumer while old-count, clock, anchor and person HOLDs remain explicit.
