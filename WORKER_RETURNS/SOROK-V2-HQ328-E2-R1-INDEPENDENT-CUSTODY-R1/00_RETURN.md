# HQ328 E2 independent event-custody review

**Verdict: `REVIEW_REVISE`.** R1 repairs X2's original collision at the B2 ingress boundary. The independent court nevertheless finds a specific failure of the commission's additional **legacy fail-closed under both insertion orders** gate: after B2 mapping, a conflicting direct B1 occurrence is not detected on subsequent B2 reentry. This does not show a second conflicting payload admitted through R1's wrapper, nor require R1 to prevent all privileged B1/SQL writes. It does prevent an unconditional acceptance of the requested bidirectional legacy-state check.

Sealed reviewer startup and observed initial remote: `a85f2964dbaae907eefea3355d2ea41c913eafea`. Assigned branch: `agent/reviewer-sorok-v2-hq328-e2-r1-independent-event-custody-r1`. Exact repair: `358fd1086eac0a4aa7791ca14abc25c45b935ddd`. Exact original B2: `950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883`. Original X2: `931aec3497c60114444806c375d1bb51ec7c0e7d`. One accountable reviewer; no subagents or candidate repairs. This conversation previously checked R1 completion and replayed author tests; it did not implement R1. E2's new source, materialization, assertions and evidence are separate from R1's author return. That prior exposure is disclosed rather than claiming a blind review.

## Blocking finding: mapped legacy collision is not fail-closed

The exact repair `bridge.py:217–237` follows an existing identity mapping, validates only its referenced occurrence and ingress, and may return `ALREADY_ADMITTED` before scanning the occurrence ledger. The legacy scan at `238–241` is an `elif`: it runs only when the identity mapping is absent.

Independent minimal sequence:

1. Admit B2 witness `event1`; either deny the target grant or let its response commit.
2. Call unchanged `B1.Store.admit_fixture(B1.episode(label='E2_CONFLICTING_LEGACY_OCCURRENCE'))` on that same database. This is deliberately outside B2 ingress.
3. Reenter B2 with the original exact, registered witness and readset.

There are now two `occurrence` rows with `event_id=event1` and different objective content hashes:

| Objective payload | Content hash |
|---|---|
| `OBSERVED_INTERACTION_AFTER_MATERIAL_LOSS` | `84dd4d03ed380d9436c9342ead143d79c11f998046f09af5f28b5b32544edc80` |
| `E2_CONFLICTING_LEGACY_OCCURRENCE` | `6462b0270dc9bc0096a85c16a9a8c38d3675e1036d3c35c91256c858cc84ea5d` |

With the original checkpoint current, B2 returns an admitted-event/ingress object and invokes B1; the response rolls back because the target grant is denied. After checkpoint advancement, B2 returns `ALREADY_ADMITTED` and the admitted-event/ingress object without B1 invocation. Neither reports ambiguous event identity. SQL tables remain unchanged during reentry, so **this is failure to detect pre-existing conflicting ledger state, not another wrapper-created row**.

By contrast, inserting the direct B1 event **before** any B2 mapping returns `DENIED / EVENT_IDENTITY_UNBOUND_LEGACY`, `event_admission=NOT_PERFORMED`, with no mutation. The two insertion orders are therefore asymmetric.

`test_legacy_after_mapping_must_fail_closed_at_b2_reentry[False/True]` preserves two actual assertion failures and exit 1. `evidence/repaired/sql/strict_legacy_after_{False,True}.json` contains receipts and full before/after SQL rows; `e2.log` and `e2.xml` contain the failures. The two green `test_direct_b1_after_wrapper_limit_is_measured` cases are explicitly observational boundary characterization, not assertions that the unsafe condition is acceptable. The strict pair was added after the initial 42 observational cases; that initial run remains under `evidence/development/`.

**Smallest requested revision:** under the existing B2 writer lock, reconcile all occurrences bearing the requested ID even when a mapping exists; refuse conflicting/unbound extra content before returning a successful replay or invoking B1. Preserve all previously committed objective facts; do not delete, rewrite or retrospectively authorize them. This can be a B2-only prestate check without editing B1. A later independent review must rerun these exact strict tests plus existing courts. Preventing arbitrary direct B1 writes remains a separate ownership/access-control problem.

## What independently passed

| Court | Original B2 | Exact R1 repair |
|---|---:|---:|
| B1 inherited | 39 pass | 39 pass |
| P1 inherited | 74 pass | 74 pass |
| Original D1, historical defective absence guard | 22 pass | 22 pass |
| Corrected D1 | 17 pass | 17 pass |
| Frozen F1 reference | 97 pass | 97 pass |
| B2 connected | 45 pass | 45 pass |
| F1 applicability accounting | 36 pass | 36 pass |
| Original frozen X2 | 17 pass, defect demonstrated | 16 pass, 1 changed defect-demonstration failure |
| Unchanged R1 author court | not applicable | 45 pass |
| New independent E2 court | not applicable | **42 pass, 2 RED** |
| Untouched native F1 runner | **17 RED, exit 1** | **same 17 RED, exit 1** |

All 249 inherited +81 B2 checks remain green at their original grades. F1 accounting remains **19 boundary negative/deferral passes and 17 N/A**, not native positive acceptance. Native RED IDs: `F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21`. Supplemental native JUnit preserves all 17 failures; actual runner JSON/exit records remain primary. D1 supplemental JUnit derives from actual unchanged Node PASS lines.

The unchanged X2 failure is exactly `test_same_event_id_accepts_distinct_objective_payload_hashes`. Its original assertion expects an admitted second object; R1 now returns `NOT_PERFORMED`. No X2 test was edited, xfailed, skipped, or reclassified. That changed result is **positive evidence of the original repair**, separate from E2's two new legacy-state REDs.

`probe_e2.py` independently reproduces two original rows at one ID, then one repaired row and `EVENT_IDENTITY_CONFLICT` before second admission. Full reproducible inputs, SQL cursor trace, checkpoint, occurrence, ingress, identity and joint-receipt rows are in `evidence/{original,repaired}/collision.json`. Response rollback retains the one valid occurrence and leaves no mediator/checkpoint/joint-receipt changes. All witness-content mutations, full packet/context/policy readsets, registration removal/substitution, legitimate distinct IDs, exact replay before/after checkpoint advancement, and missing/partial mapped rows behave as the new court specifies.

E2 independently opens **six simultaneous fresh OS processes per terrain** for same content, three competing payloads at one ID, six legitimate IDs, and simultaneous successful replay. The first three leave the initial checkpoint intact as grants are denied; the successful terrain commits exactly one response/mediator/joint receipt. Actual process IDs, receipts, traced SQL and all table rows are in `evidence/repaired/sql/processes_*.json`. R1's separately rerun four-process tests also pass.

`BEGIN IMMEDIATE` occurs before identity and checkpoint checks. E2 holds a competing SQLite writer lock, changes the checkpoint, observes the child's blocked lock request, commits, and verifies the child refuses the now-stale witness without admission. Admission insert traces show occurrence → ingress → identity → one COMMIT under that lock. Separate response transactions preserve occurrence on response rollback. E2 pauses and sends **SIGKILL at three uncommitted boundaries**: after occurrence, after ingress, and after identity insertion before COMMIT. Other connections see no partial rows; reopening yields exact prestate; `PRAGMA integrity_check=ok`; a fresh lawful retry commits. This is process-death rollback evidence, **not power-loss durability**.

The exact real two-event positive and journal-only control still produce `joint_check:caretaker` versus `inspect_alone:caretaker`. Both trace bundles are byte-identical between original and repaired courts, and the original cold runner reproduces exact receipts and final hashes. E2 additionally replays an old event from a fresh process after two persisted responses; it changes no table and returns `ALREADY_ADMITTED`.

## Source custody and reproducibility

`run_e2.py` independently retrieves Git blobs and binary archive bytes, computes SHA-1 with the Git blob header/NUL and separate SHA-256, stages original B2 and exact R1 bridge, and independently materializes all **69 inherited files/archive members**. It verifies archive paths and compares the frozen X2 copy with its original Git bytes. No network code, package installation, model API, original survey, or production actor is used. Both original and repaired courts execute in separate staging directories using the existing shared Git object store. Actual bridge/B1/P1 module `__file__` paths and byte hashes are recorded relative to those roots. D1 executes its exact verified corrected JS in Node; F1 runs the exact archive members.

The R1 author delta from its seal changes only the commissioned B2 `bridge.py` and its return folder. B1/P1/D1/F1, historical tests, frozen sources and owner law are unchanged. E2 changes only this return folder on the assigned reviewer branch. Independent per-phase manifests, frozen/author test identities, actual commands/exits, source-runtime records and updated passport are provided. Evidence copies remove hostnames and local paths only; tests, test status, receipts, SQL values and source bytes are preserved. `git diff --check` reports four trailing-whitespace lines in the preserved pytest traceback log/XML; those raw traceback spaces are retained, not source-code changes.

From this return directory:

```sh
python3 run_e2.py
python3 audit_e2.py
```

The orchestrator expects raw X2 exit 1 on the repaired source and E2 exit 1 for the exact two new strict legacy failures; it verifies their names. This is evidence orchestration, not a green pytest claim. `audit_e2.py` validates test totals, failure identities, imported source hashes, actual loaded module hashes, collision row counts, transaction order, process counts, SIGKILL recovery and preserved REDs. `verification_receipt.json` records `REVIEW_REVISE`.

## Authority and disposition

This verdict is confined to synthetic B2 event custody. Direct B1/SQL bypass remains outside that wrapper, and no general producer security is established. The exact-return binding assumes a trusted test-fixture registrar and trusted ledger writers; unkeyed hashes and issuer strings do not authenticate an external producer. The requested legacy reentry integrity gate is still unmet, so **`SOURCEFREE_EVENT_CUSTODY_ACCEPT_SCOPED` is withheld** despite the verified pure-wrapper collision repair.

CAN008 immediate response remains separate from CAN011 durable target authority; the latter is independently validated only by the test owner here. ADP019 retains production occurrence/admission, ADP020 retains lawful causal RNG, and P1 selection remains noncausal test policy. No label such as `recognized_plan` is scientifically adopted, and the 17 native F1 gaps remain. No source-owner law, actor permission, psychological rule, registry, CURRENT, PREMAIN or production code is changed. HQ owns disposition and subsequent repair dispatch.

The governing-read identities, including the missing-at-seal 00C fallback, are in `governing_sources.json`. Exact final return SHA is verified directly against the assigned remote after push and reported in the final reply, rather than inserted into its own commit preimage.
