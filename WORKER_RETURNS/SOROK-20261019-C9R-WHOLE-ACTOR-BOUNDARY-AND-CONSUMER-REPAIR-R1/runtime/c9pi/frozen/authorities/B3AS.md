# B3AS-I2 independent schema/readset repair court

**Verdict: ACCEPT_SCOPED — the exact local-authored repair `16f15a125ba54cdf17f5d41be2d851bbcd2240d7` closes both unchanged B3A-I2 schema REDs, and no frozen, atomicity, B3, F2, E3, X3, inherited or sourcefree expectation was weakened to do so.** The acceptance is scoped to the tested logical schema/readset contract, the sourcefree test-only grade and the preserved owner-permission boundaries. It is an engineering acceptance of a bounded SQLite custody candidate, not semantic adoption, not CAN008/CAN011 law, not M2 integration and not production adoption. No new repair commission is created; findings return to Sorok HQ for adjudication.

## Custody and independence

Repository: private `maidiu/rawlsing`. Assigned branch: `agent/reviewer-sorok-20261018-b3a-schema-readset-repair-independent-i2-r1`. Exact sealed startup `e18c41b5faa6cbb0ab393561833d850e1dd1e383`, direct parent `528e8cde0cff9e28f3c55d5d54a66e820d7401fa` (the complete previous B3A-I2 REVISE return). The seal changes exactly one path, this commission file; its remote head was verified before work (`git ls-remote` matched the local SHA).

This reviewer is a fresh independent source-free I2 reviewer: not the B3A/B3AS author, not the first B3A-I2 reviewer, not HQ and not a semantic issuer. One accountable OpenCode agent with MiMo-V2.6-Pro performed the complete commission in a new sparse worktree over the existing shared Git object store. No Codex, no model/provider switch, no delegation, no helper agents, no package installation, no external model call, no real actor/source run. Actual cash/quota remain UNKNOWN. Independence is documentary reviewer separation, not a provider/account attestation.

Pinned Sorok `00_READ_ME_FIRST`, `00D`, `00B/00C` and the accepted B2/ADP019 and CAN008/CAN011 jurisdiction boundaries were read from the commission base; no HQ role follows from those reads.

### Phase 0 — custody-only publication of the exact local repair

The reported local repair `16f15a125ba54cdf17f5d41be2d851bbcd2240d7` was probed directly in the shared object store, not inferred from any message:

- author `Maidiu` (identity exactly as recorded in the commit object), author date 2026-10-18, single parent `8bd4d6b01fd402e7e6a8d07903f2c3cada837f55` (the exact original B3A candidate reviewed by the first court). Ancestry confirmed with `merge-base --is-ancestor`.
- 305 changed paths, **all** inside the authorized repair-author subtree `WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-R1/`. Zero paths outside it. No secret-shaped filenames; a content scan for private-key, token and credential patterns returned nothing.
- The repair's `candidate/` reproduces the original candidate byte-for-byte except one file: `candidate/integration.py`. Its Git blob is `d3a324bb93c17fdaf12670dd153aeb138d9c426a` and its SHA-256 is `6b0187c5dfa0a48928f78fb0c3979de6c35e49aa770c9d10f644f57eaed6a679`, exactly the identity the author's `00_RETURN.md` claims.
- All frozen courts carried in the repair (`frozen_review/test_reviewer_hostiles.py`, `test_seeded_refusals.py`, `reviewer_worker.py`, `test_atomic.py`, `test_projected_atomic.py`, `frozen_x3/*`) are byte-identical to the first review's frozen inputs. No frozen expectation was edited.

Custody-only publication was then performed as an ordinary non-force push of the exact unchanged commit and its ancestry to the previously absent branch `agent/rabochii-sorok-20261018-b3a-schema-readset-repair-r1`. `git ls-remote` and a fresh fetch both report remote SHA `16f15a125ba54cdf17f5d41be2d851bbcd2240d7`. No cherry-pick, amend, rebase or identity rewrite. The uploaded author commit is source-custody evidence only; it is not independent acceptance.

## Source and import verification

Runtime sources were independently materialized from pinned Git commits through the candidate's exact transport, verifying every blob SHA-1 against the object store: **199 staged entries, 0 mismatches**, with identical manifests for the pre-repair and repaired candidates. Only `integration.py` differs between the two runtimes. Eleven actually imported Python modules were hash-verified against those pinned identities (`evidence/actual_imports.json`); the imported `integration.py` is exactly the repaired SHA-256 above. Pre-repair contrast executions used the original blob `604e09986d87f404daa9857b25758ec2e1fe491d` in its own isolated runtime. No prior runner state, author database or author execution log was reused as proof.

## The two unchanged B3A-I2 REDs, reproduced and re-tested

The two frozen falsifiers were executed **unmodified** (file SHA-256 `30baf690d09ac079d370f7730c06114481848403efd52629f279ec2aceb9246f`, matching the first court's preregistration) against the pre-repair candidate first:

1. `test_schema_only_race_is_rejected` — **RED reproduced.** A second connection's `CREATE INDEX` between scratch validation and public publication was accepted: expected `REFUSED`, observed `ELIGIBLE_NONCAUSAL`. The claimed full publication readset did not cover `sqlite_master` definitions.
2. `test_schema_change_on_refusal_sets_no_mutation_false` — **RED reproduced.** After an external index plus a domain refusal, `no_mutation=True` was reported although the logical schema had changed.

Against the repaired candidate both are **PASS** (`evidence/junit/repair_two_reds.xml`). The full frozen 20-case I2 hostile court moves from **18 PASS / 2 RED** to **20 PASS / 0 RED**; the pre-repair run is retained separately (`orig_hostiles.xml`). The clean/seeded bad-origin/future-event refusal controls pass on both B3A versions; on original B3 their four historical REDs are preserved unchanged (`origb3_seeded.xml`).

## Actual independent execution

| Court | PASS | RED |
|---|---:|---:|
| Two frozen I2 schema falsifiers, before repair | 0 | 2 |
| Same two falsifiers, after repair | 2 | 0 |
| Frozen 20-case I2 hostile court, before repair | 18 | 2 |
| Same court, after repair | 20 | 0 |
| Clean/seeded refusal controls (4), after repair | 4 | 0 |
| B3, unchanged | 71 | 0 |
| B3A atomicity, unchanged | 63 | 0 |
| F2 through candidate | 42 | 0 |
| F2 blinded IDs/expectations | 42 | 0 |
| E3 on corrected B2 | 26 | 0 |
| Frozen X3 (28) | 24 | 4 |
| Author's extended court (frozen 20 + 13 author controls) | 33 | 0 |
| **This reviewer's independent hostile controls** | **19** | **0** |
| Same independent controls on pre-repair candidate | 13 | 6 |
| Original B3 seeded controls (historical) | 0 | 4 |

Zero errors, zero skips. Blinded F2 retains 20 eligible / 22 refusal-or-deferral with expectations removed and IDs replaced before the engine. The author's 33-case court is supplementary evidence from the author's own run, recounted here only after this reviewer reran it; it is not independent acceptance.

### Independent hostile controls (preregistered before first execution)

Eight independently authored families, 19 cases, frozen in `preregistration_independent.json` and `test_independent_hostiles.py` before any control executed. Four reviewer-side fixture-mechanics amendments made during first execution are logged in `freeze_hashes.json`; none touches the candidate, a frozen court or a substantive requirement. First-run outputs are preserved under `evidence/independent_run1/`.

- **HC1** an index created by an independent OS process between scratch validation and public `BEGIN IMMEDIATE` (clean and seeded): post-repair `REFUSED` with `PUBLICATION_READSET_CHANGED`, `no_mutation=False`, external index preserved, rows unchanged, no candidate rows. Pre-repair: **RED** (accepted).
- **HC2** trigger, view, table and `user_version` metadata mutations inside the documented schema contract: all four refuse post-repair with truthful `no_mutation=False` and preserved objects. Pre-repair: trigger/view/user_version **RED**; a new table was already caught by the old table-name key comparison.
- **HC3** external trigger immediately before a late domain refusal: `REFUSED`, `no_mutation=False` (pre-repair **RED**, reported `True`), rows unchanged, trigger preserved.
- **HC4** concurrent independent B2 fact **and** index in the late window (clean and seeded): refused, `no_mutation=False`, every pre-existing row preserved as a subset, the independent fact survives, no `b3_source`/`b3_transition` candidate rows. No deletion or rollback of foreign state.
- **HC5** real SIGKILL at the scratch boundary, at the public publication boundary and after successful return (clean and seeded, 6 cases): exit verified as `-9`, cold inspectors run in distinct PIDs, cold schema **and** rows unchanged at precommit boundaries with `PRAGMA integrity_check = ok`; the after-return stratum keeps committed rows replayable. Process-death evidence only.
- **HC6** a refused proposal followed by correct retry (clean and seeded): refusal leaves the database byte-equal at the logical level; the retry publishes exactly one source row for its own event; no duplicate transition rows; a repeat call adds no source/transition ghosts.
- **HC7** `no_mutation` semantics matrix across seven strata (below).
- **HC8** external DDL attempted with `timeout=0` inside the public `BEGIN IMMEDIATE` window: the DDL cannot commit (writer lock), publication completes, final schema contains no foreign object. This documents a lock boundary, not cryptographic protection.

### `no_mutation` semantics as measured

| Stratum | Observed | Accurate? |
|---|---|---|
| refusal, no external change | `True` | yes: proposal-only rollback |
| refusal after external schema change | `False` | yes (this was the pre-repair RED) |
| refusal after external row change | `False` | yes |
| fresh success | `False` | yes: rows were published |
| identical repeat call | `True` | yes: no state change |
| repeat after a committed target | `False`, sole delta one appended `b3_response` | yes: the response record is computed over current middle and legitimately differs; `exact_replay` asserts source identity, not a write-free call |
| valid-empty target (missing permission) | `False`, transition `VALID_EMPTY` | yes: the objective event is still admitted |
| denied target (permission not registered) | transition `DENIED`, `owner_effect_committed=False`, no `independent_owner_receipt` | yes |

One structural boundary worth recording: scene projections are bound to event identity, so a **second** event that reuses the same utterance/exposure evidence is refused `SOURCE_PREIMAGE_IDENTITY_COLLISION`. Independent second-event probes therefore run on isolated databases. This is preimage identity protection, not a new defect.

### Cold replay and SQL receipts

Both developmental loops (`positive`, `permission_absent`) were executed and then reconstructed in fresh Python processes against fresh SQLite files: exact `snapshot_hash` match, exact per-episode receipt list match, full `sqlite_master` definition and complete table-row match between live and cold copies, `PRAGMA integrity_check = ok` on all four files. A double replay into an already-populated file (this reviewer's own first verification mistake) is preserved in the transcript as a clock-guard observation: re-running an earlier episode is refused `B3_TIME_REVERSED` with no state change.

### Inherited courts, executed fresh

249 inherited checks pass (B1 39, P1 74, historical D1 22, corrected D1 17, F1 reference 97), plus B2 integration/accounting 81, R1 45, repair regression 5, E2 strict 2 and M2 41. Historical negatives reproduce at their exact identities: full E2 42/2, X2 16/1, M1-on-M2 18/19, strict I2-on-M2 13/10, M3 source-preimage 3 RED, and native F1 **17 RED** with unchanged IDs F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21. None was edited, skipped or xfailed.

## Exact old-versus-new RED accounting

| Identity | Before repair | After repair |
|---|---|---|
| `test_schema_only_race_is_rejected` | RED | **PASS** |
| `test_schema_change_on_refusal_sets_no_mutation_false` | RED | **PASS** |
| Frozen 20-case court | 18/2 | 20/0 |
| Independent controls HC1/HC2/HC3 (6 cases) | RED | **PASS** |
| X3 duplicate physical-check IDs | RED | RED (preserved) |
| X3 pre-loss threshold | RED | RED (preserved) |
| X3 standalone helper readset | RED | RED (preserved) |
| X3 obsolete delayed-detection race | RED | RED (preserved) |
| Original B3 seeded refusal controls | 4 RED | 4 RED (preserved) |
| Native F1 | 17 RED | 17 RED (preserved) |
| M3 source-preimage | 3 RED | 3 RED (preserved) |
| E2/X2 legacy assertions | 2+1 RED | 2+1 RED (preserved) |
| M1/I2-on-M2 interface grain | 19+10 RED | 19+10 RED (preserved) |

No legacy scientifically unsupported expectation was marked PASS; no target/practice rule was changed to turn anything green.

## Why the repair works (independent reading of the diff)

The pre-repair `snapshot()` returned table names and rows only. `Integration.run` now captures one consistent logical readset — `sqlite_master` definitions for tables/indexes/triggers/views plus `schema_version`/`user_version`/`application_id` and all rows — via `_database_snapshot()`, and rechecks it under `BEGIN IMMEDIATE` (`PUBLICATION_READSET_CHANGED`). Schema identity and cross-file `user_version`/`application_id` are compared separately (`PUBLICATION_SCHEMA_CHANGED`), while `schema_version` is compared against the scratch copy's own post-backup baseline because SQLite backup legitimately advances the destination's schema cookie; this is a correct fix and the rollback-acceptance control in the author's development history caught the earlier cross-file mistake. Refusal receipts now compute `no_mutation` over the full logical snapshot. Table identifiers are quoted. Row publication remains strictly additive, and independent rows are preserved rather than deleted. No policy drift, trigger execution or schema mutation was introduced by the patch.

## What is not established

Everything in `02_REQUIREMENTS_AND_LIMITATIONS.md` is preserved and in force. In particular: no human habit-acquisition law, no enacted third check at t9, no selected durable belief/affect, no independent other-actor development, no ADP016/017 grant, no native ADP019 issuer authority, no CAN008/CAN011 law admission, no M2 repair incorporation (frozen M2 `5c2fbe14ccfa5027becfabc682206a1e61aaf986` retains its three M3 preimage REDs and durable interpretation stays quarantined), no R3/R4 or ONECALL, no production feasibility, no power-loss/fsync durability claim, no immunity to arbitrary privileged SQL or DBA corruption, no whole-database physical-layout or connection-local-setting coverage (the readset is logical state; staging remains O(database size) with writer contention). External raw SQL here is a privileged schema-writer adversary, distinct from an unauthenticated B2 request; the finding was a missing promised schema/readset boundary, and nothing here shows unauthenticated request data can alter schema. A durable observed candidate is not evidence of practice formation or human psychology. No authorization is manufactured from review tests.

## Disposition

**ACCEPT_SCOPED** at the tested grain, returned to Sorok HQ for adjudication. No automatic follow-on commission is created. If REDs had remained they would have been returned literally rather than repaired here; none remained in the commissioned scope.

All review changes are confined to this return subtree on the assigned reviewer branch. The custody push of the unchanged author commit to `agent/rabochii-sorok-20261018-b3a-schema-readset-repair-r1` was the sole additional repository write. Candidate and reviewer SHAs accompany the handoff.

CLOSURE_ONLY. Terminal: `SOROK_B3AS_I2_SCHEMA_READSET_REPAIR_COURT_R1__RETURN_TO_HQ`.
