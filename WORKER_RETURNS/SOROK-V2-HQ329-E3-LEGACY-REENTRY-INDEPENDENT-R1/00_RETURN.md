# HQ329 E3 independent post-repair legacy event-custody court

**Verdict: `SOURCEFREE_BFIRST_EVENT_CUSTODY_ACCEPT_SCOPED`** for exact repair `8f7966d6d0bbb1ea2e57359de9defbcf552268bd`. The two original E2 strict failures reproduce on original R1 and both pass on this repair. Fresh hostile SQL, concurrent-writer, crash/recovery and cold-process execution qualifies the bounded synthetic SQLite B2 ingress mechanism. This is independent engineering acceptance at the commissioned grain, not HQ adoption, psychological science, production ADP019 authentication, CAN011 owner permission, or native F1 completion.

The assigned reviewer branch began at the exact remote-verified sealed startup `ccc84471c27b6dbe3ff1040dcaf78a3070746e99`. The preexisting app checkout initially pointed at unrelated `25830fe7462bb9e29bc4087e6ae14f3f84cec377`; it was clean. I fetched only the commissioned reviewer ref and created the assigned local branch at the sealed SHA. One accountable reviewer performed this commission; no candidate authorship, helper agents, provider switch, package installs, external model calls, or candidate edits. Exact prior 00C was read at `3c685eb4734856b61f2d601e082eb325e3f6f1d1` because it is absent at this seal; governing identities are in `governing_sources.json`. The selected local route follows the commission's LOCAL_DOMINANT dispensation. Actual billing, quota and runtime model selection remain unverified; the requested GPT-6 Medium setting is not inferred from test results.

## Exact executable results

| Court | Original R1 `358fd108…` | Repair `8f7966d6…` |
|---|---:|---:|
| E2 strict legacy fail-closed gate, unchanged | **2 FAIL**, exit 1 | **2 PASS**, exit 0 |
| B1 inherited | 39 PASS | 39 PASS |
| P1 inherited | 74 PASS | 74 PASS |
| Historical D1 original guard | 22 PASS, known historical defect | same |
| Corrected D1 guard | 17 PASS | 17 PASS |
| Frozen F1 reference | 97 PASS | 97 PASS |
| B2 integration | 45 PASS | 45 PASS |
| B2 F1 applicability accounting | 36 PASS | 36 PASS |
| Frozen R1 repair court | not repeated on old R1 | 45 PASS |
| Frozen full E2 | strict pair above | **42 PASS / 2 FAIL**, exit 1 |
| Frozen X2 | not required on old R1 | **16 PASS / 1 FAIL**, exit 1 |
| Frozen user-directed repair controls | not applicable | 5 PASS |
| New independent E3 controls | not applicable | **26 PASS** |
| Raw native F1 | **17 RED**, exit 1 | **same 17 RED**, exit 1 |

All 249 inherited +81 B2 checks pass in both materializations. The 36 F1 accounting checks still mean 19 boundary negative/deferral passes and 17 N/A, with zero native positive qualification. Native RED IDs remain **F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21**. Raw native JSON and original exit receipts are primary; `native_f1_derived.xml` is explicitly supplementary.

The full E2 failures are precisely `test_direct_b1_after_wrapper_limit_is_measured[False]` and `[True]`: these historical observational assertions require the now-repaired bypass behavior. X2 fails precisely `test_same_event_id_accepts_distinct_objective_payload_hashes`, which expects the original collision to be admitted. These three assertion failures are preserved literally, without edits, xfail, skip or expectation replacement. They are not remaining repair defects. Frozen E2 strict checks prove the opposite required behavior and both pass.

## Why the repair qualifies

The bridge now scans all occurrence bodies under its existing `BEGIN IMMEDIATE` writer lock before successful mapped replay. An exact mapping must resolve to exactly one occurrence at its recorded content hash; additional same-ID content returns `DENIED / EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE`, `event_admission=NOT_PERFORMED`, with no B1 response invocation. Legacy state before mapping returns `EVENT_IDENTITY_UNBOUND_LEGACY`. Objective history is preserved on refusal. The candidate commit changes only B2 `bridge.py` and the author's new evidence subtree: seven added/two removed bridge lines. B1/P1/D1/F1 and frozen tests remain original bytes.

The new E3 court independently tests same-ID pollution before/after mapping under both permission denial and committed response; exact duplicate B1 content; duplicated unrelated content; exact-content legacy state without mapping; forged issuer/world/checkpoint/participant; changed packet/context/policy readsets; schema-valid policy identity changes; and stale checkpoint. All database tables are snapshotted, including committed responses and owner effects. Refusal never deletes or mutates those snapshots.

For each response condition, two independent cold B2 writers wait behind a privileged B1 writer's real SQLite transaction. Each reports its PID and traced `BEGIN IMMEDIATE` request; neither passes the held lock. After the B1 conflict commits, both refuse at reentry and leave the exact committed tables untouched. A separate rollback control proves an uncommitted B1 conflict does not poison reentry. Cold mapped replay after pollution also refuses without rewriting an already committed response. The B1 bypass succeeds in creating conflicting history: this is a measured limitation, not access-control immunity.

The untouched full E2 court additionally executes six simultaneous processes for each of four terrains (same content, conflicting content, distinct IDs, successful replay), three SIGKILL boundaries (occurrence, ingress, identity), held-lock stale-checkpoint checks and replay after later persisted events. R1's 45 tests include their original concurrent writers and crash controls. Process IDs, full SQL traces, inputs, receipts and before/after rows are under `evidence/fixed/{sql,r1_sql,repair_sql,e3_sql}/`. SIGKILL recovery establishes process-death transaction rollback, not power-loss durability.

Both original real two-event positive and journal-only controls are byte-identical between old R1 and repair. They preserve `joint_check:caretaker` versus `inspect_alone:caretaker`; cold reconstruction reproduces exact receipts and final state hashes.

## Performance and trust limits

`EXPLAIN QUERY PLAN SELECT hash,body FROM occurrence` reports `SCAN occurrence`. E3 measured three end-to-end replay attempts at each of 0, 100 and 1,000 unrelated rows; observed medians were about 72.4, 75.9 and 75.9 ms on this host. These small samples include Node guard/process overhead and do not establish production throughput or scan-only timing. Every entry still decodes every occurrence body while holding the write lock: O(total rows), with writer contention and denial-of-service exposure as the ledger grows. No global index migration was authorized or performed.

Acceptance assumes the bounded closed registrar, trusted fixture issuer/allowlist and well-formed B1 ledger records. Arbitrary privileged SQL can alter/delete/corrupt tables or forge a coherent replacement; the scan is not a signature or a security boundary against that writer. It detects the tested later conflicting B1 event on subsequent B2 entry. No general malformed-JSON storage recovery, scalable multi-actor event service, external producer authentication or production signer is certified.

ADP019 keeps real occurrence/admission jurisdiction. CAN008 immediate response remains separate from CAN011 durable target authority. Authored recognition labels and probabilities remain sourcefree hypotheses. No original survey, live actor/model, owner registry, CURRENT or PREMAIN is changed. F1's native gaps remain open.

## Source identities and reproduction

| Material | Git blob SHA-1 | Content SHA-256 |
|---|---|---|
| Old R1 bridge | `7245046bc448fee0b00b85c849c50c8db656f129` | `681cb99e8808025b8f5698fac670183e91f7788c7390baaa7b9841e840587769` |
| Exact repaired bridge | `ca27e715fca33da49b2d566cfe4bef521d5eb502` | `9c112a7984b0581e965394983acf0e38064847083b78096e2d8215b48932250f` |

`evidence/{old,fixed}/source_manifest.json` records complete Git/content hashes, including 69 inherited files/archive members. `loaded_modules.json` records actual imported bridge/B1/P1 paths and hashes. `frozen_manifest.json` verifies exact E2/R1/repair-control bytes; X2 is separately compared with its original `931aec3497c60114444806c375d1bb51ec7c0e7d` object. `audit_review.py` independently checks Git preimages, module hashes, all result counts, changed-status test names, lock evidence, native REDs and candidate/return write terrain. Frozen E2's pinned materialization helper is reused as transport; its output bytes and execution are independently audited rather than trusting the repair author's evidence.

From this return directory:

```sh
python3 run_review.py
python3 finalize_evidence.py
python3 audit_review.py
```

Requires the existing authorized Git object store and observed Python 3.11.3, pytest 9.1.1, SQLite 3.40.1, Node 18.14.2 and Git 2.39.1. No network/package installation is part of the runner. Logs/JUnit retain actual failures; only local paths and hostnames are sanitized in portable evidence. The final independent expansion to 26 checks was run as a targeted pytest command recorded in `commands.json`; earlier inherited suites were not needlessly rerun after that test-only addition.

Development disclosure: the first independent run was 21 PASS /2 harness failures. One overstrict assertion expected DENIED for a policy-schema refusal whose lawful result was DEFERRED; the other parsed an additional B1 response lock trace as JSON. Only E3's new controls were corrected; their initial log/JUnit remains under `evidence/development/`. Portable XML placeholder escaping was corrected in the evidence packaging, without altering source or test outcomes. Historical author setup notes in copied execution receipts remain author provenance, not new E3 incidents.

Direct remote verification confirmed `codex/b2-legacy-reentry-repair` still points to the exact reviewed `8f7966d6d0bbb1ea2e57359de9defbcf552268bd`; the startup remote receipt is in `evidence/remote_at_review.txt`. The final reviewer commit is verified directly after push and reported outside its own preimage. All E3 changes are confined to this new return directory. HQ owns intake and subsequent adoption; this return grants no production authority.

`git diff --cached --check` reports trailing spaces in preserved pytest failure tracebacks (development and old strict log/XML). They are retained as raw evidence; source files have no whitespace findings.
