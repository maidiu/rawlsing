# HQ285 S06G — native atomic integrity repair candidate

Status: **IMPLEMENTED_AND_LOCALLY_TESTED; NOT_ADOPTED; INDEPENDENT_REVIEW_REQUIRED**. External authenticated issuance/custody remains **HOLD**.

Sealed startup: `85a8b99e9ddb7518ba37ced2a065a72a9d17b587`. Native source parent: `6187d0a25f98370a3d78371fcdf1752a3b1ec80f`. Independent baseline: S06FR `1b5b6072f855a74864c82d0f1b3923327bfb8b99`, 111 passed / 3 failed, including 12 passing tests that demonstrated defects. Canonical `7f29aec36d24f16da52d84f17c00f08db3a55434` is unchanged.

## Implemented corrections

1. B5 event payloads are recursively detached and immutable: mappings become read-only proxies, sequences become tuples, and exports canonicalize into detached JSON-safe containers. Public `events` and `release_history` retain stable references after attempted nested mutation. M2 closure metadata receives the same recursive immutability so immutable repository records can safely be shared.
2. Checkpoint restoration retains ordinal, predecessor and projected-state checks, then re-executes native operations from the exact staged subjects and event arguments. It compares complete generated events, receipts, selection indexes and all state to the supplied checkpoint. Registration/publication fields are derived from subjects; selection authority, attestation, predecessor and determinant snapshot are regenerated; invalidation closure, rebuild eligibility/link, GC proofs and receipt release/event identity are regenerated. Inconsistent rehashed payloads and receipts are refused. The caller's checkpoint containers are detached before parsing.
3. All 17 B5 mutators hold one reentrant owner lock across validation, event allocation, append and projection/receipt updates. An outer transaction snapshots owner containers and restores them on any raised `BaseException`. Nested native operations use the same transaction. Public state/history/checkpoint readers hold that lock. Competing selectors with the same stale predecessor now produce exactly one winner and one conflict.
4. All five M2 writers similarly serialize validation and collision insertion, with rollback of all five stores on exceptions. Readers hold the same repository lock. The check/compare/write collision sequence cannot interleave through native writers.
5. Saved `_append_events`, `_commit_selection_transition_receipts` and M2 `_insert` refuse outside an active owner transaction. Append also checks event type and subject/product/scope; selection transition commits check typed receipt/event/key/release linkage; M2 insert checks owned store, record type and exact index identity. Native in-body preflight also requires the transaction, so calling a decorator's saved `__wrapped__` body cannot accidentally bypass serialization. This hardening is not a Python principal boundary.

N04's M2 release-ref → release_subject_ref → producer-subject route is unchanged. No new issuer, permission, revocation or semantic authority was added.

## Actual courts

Final unfiltered run: **187 passed, 14 failed, exit 1; no skips or errors**. Every test identity/result and exact command is in `01_EXECUTION_MANIFEST.json`, with original output/JUnit in `repro/final_full.log` and `repro/final_full.xml`.

| Final suite | Passed | Failed |
|---|---:|---:|
| S06F native | 18 | 0 |
| Accepted B5 | 39 | 0 |
| Accepted M2, unchanged | 26 | 2 |
| New S06G repair court | 42 | 0 |
| Exact S06FR reviewer overlay, unchanged | 17 | 12 |
| Adjacent source-free integration courts | 45 | 0 |

The 12 S06FR failures are its unmodified `OBSERVED` defect-presence assertions: all 12 defect reproductions cease to satisfy their old assertions. In particular, the original independent immutability acceptance test now **passes**. These failures are not relabeled green. The old in-lock race probe's barrier now times out because the second writer cannot enter its predecessor check concurrently; the new S06G race court instead synchronizes before the public call and requires one success/one conflict across 12 trials. No frozen reviewer test was edited. Its exact Git bytes were copied into an own-return overlay, checked by SHA256 and made read-only (0444) for execution. Git preserves bytes, not read-only permission; repro instructions restore the runtime permission.

The two original M2 fixture failures remain visible: their foreign representation/binding setup is refused with `RELEASE_UNAVAILABLE` before the later oracle. Write terrain excludes those accepted test files, so they remain unchanged. New `test_reconciled_m2_17_early_refusal_and_lawful_downstream_mismatch` and `test_reconciled_m2_18_early_refusal_and_lawful_failover_mismatch` both pass: first assert strict early refusal, then lawfully register the exact foreign subject/closures/release/representation and retain the original `PUBLICATION_BINDING_MISMATCH` oracle. Same-release failover success is also retained. This reconciles the behaviors without weakening native checks or silently changing inherited fixtures.

A separately labeled acceptance selection excludes exactly those two incompatible inherited setups and the 12 obsolete defect-presence assertions; it executes all other tests, including both new reconciliation cases and the unchanged immutability expectation: **187 passed, 14 deselected, exit 0**. This selection is not a claim that the unfiltered court is green. Exact expression and deselection list are recorded. Intermediate runs are labeled separately; final evidence controls.

The 42 new cases include rollback after append for each of 14 event-mutating B5 methods; post-write failure for staging, protocol staging and selection keys; post-insert failure for all five M2 writers; concurrent exact preimage collision; reader blocking during interrupted publication; nested immutability; rehashed publication and every receipt-family inconsistency; invalidation receipt omission; lawful no-op history; and the two M2 reconciliations. Adjacent integration courts preserve synthetic world composition and exact current/as-of behavior, including an actual fresh-process checkpoint reconstruction.

## Remaining limitations and adoption gate

This is in-memory exception atomicity and serialization. It does not provide durable commit storage, OS-kill recovery after an unsaved transaction, multiprocess coordination, fork/pickle portability of locks, or distributed custody. A complete exported checkpoint can be restored in a fresh process; no claim is made for unfinished or unsaved history.

Python callers with arbitrary same-process code can set private attributes, open private transaction contexts, replace callables or mutate dictionaries directly. Saved-helper refusal prevents ordinary out-of-transaction invocation; it does not authenticate a caller. Hostile issuers require separate principals/processes and an independently anchored history root, epoch and revocation stream. Coherent alternative histories remain locally replayable as LOCAL_UNAUTHENTICATED, never authenticated custody.

Legacy no-op invalidation receipts contain no ordinal anchor. They are accepted only if their empty affected set and exact unaffected products match an actual registration-prefix graph. Their precise timing/completeness remains unproved. Refinement kinds without a native emitting operation are refused during semantic checkpoint replay; only the existing native RECERTIFIES operation is replayable. No new refinement issuer was invented.

Snapshots copy owner projection containers on mutation; semantic recovery replays the history through native operations. This favors bounded correctness over throughput and can take quadratic aggregate work for large histories. No production-size performance or raw-source qualification was performed. Identity schemas/contract versions and constitutive M2 release identities remain unchanged for legitimate native operations.

This session previously authored S06FR and now implements S06G; its repair court is **implementer verification**, not the later independent adjudication. A **different reviewer** must review the exact pushed candidate before adoption. No canonical merge, source originals, protected CURRENT, real survey access or V3 execution occurred.

## Resource and publication record

Existing isolated sparse worktree: `/Users/matthewsmith/.codex/worktrees/hq284-s06fr-native-security-r1/Rawlsing`, reused only after verifying a clean completed reviewer checkout, then switched to the commissioned S06G branch at the sealed SHA. It remains Git-registered rather than app-managed. No clone, reset or broad fetch. Only the assigned branch was fetched and pushed.

Actual session: OpenAI Codex Desktop, GPT-6.1 Sol (`gpt-6.1-sol`), **medium** effort; user-designated secondary Mac account fingerprint `b4d51d8e`. Machine/runtime/quota timestamps and attestation fields are in `02_RESOURCES_AND_SCOPE.json`. Starting usage was 0% five-hour / 2% weekly; prepublication observation was 6% / 3% used. Reset credits used 0 (three remain), paid overflow 0, primary Astra account unused. Independent hardware-to-account mapping is unavailable; the secondary designation is user-provided. Go pool not used/UNKNOWN. The user's previously rescinded quota floor stays rescinded; this commission retains the no-reset/no-overflow constraints.

Only two native owners, the new named S06G test module, and this own return changed. Accepted/frozen test hashes and tested owner/test blob identities are recorded in the manifests. The exact pushed SHA is verified against the assigned remote ref and supplied in the handback; commit identity seals the complete tested source and return.
