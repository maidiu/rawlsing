# HQ284 S06FR — Independent native B5/M2 security review

**Review complete. Candidate security acceptance: FAIL. External authenticated issuance/custody: HOLD.** Native public guards and several local invariants improved, but the candidate is not an integrity or principal-isolation boundary.

Reviewed candidate `6187d0a25f98370a3d78371fcdf1752a3b1ec80f`, sealed commission startup `90f59298a63523c4bdd5a6b46b8719c13afe928a`, against canonical `7f29aec36d24f16da52d84f17c00f08db3a55434`. Reviewer owns only this return and `rawlsing_next/tests/test_hq284_s06fr_native_review.py`; no production, accepted or frozen tests changed. This reviewer is not S06F's implementer or HQ. Author fixture constructors were reused solely for source-free records; reviewer expectations, schedules and injections are independently written after examining native source. The frozen expectations were retrieved separately, unchanged, from `7e96914ed6c9a186d5de8a778e8396e46a741eb2`.

## Executed result

Final command and per-suite counts are in `03_EXECUTION_AND_RESOURCES.json`; exact log and JUnit evidence are `repro/final_native.log` and `repro/final_native.xml`.

| Suite | Passed | Failed |
|---|---:|---:|
| S06F native authored | 18 | 0 |
| Accepted B5 | 39 | 0 |
| Accepted M2 | 26 | 2 |
| Independent native reviewer | 28 | 1 |
| Total | 111 | 3 |

Exit **1** is preserved. Twelve independent passing cases are explicitly named `OBSERVED`: they prove a defect remains, and are **not** successful security acceptance tests. The independent immutability expectation remains failing, with its original oracle intact. Earlier exploratory test failures included a reviewer event-kind typo and an overly specific exception-message pattern; the final source fixes those fixture issues. No candidate defect was corrected or hidden. Intermediate independent logs precede the final 29-case reviewer suite; final evidence controls.

The two accepted M2 failures are `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`. Their setup tries to insert records for releases absent from that repository. The new owner rejects with `RELEASE_UNAVAILABLE` before their later expected rejection. These are fixture contract incompatibilities, not observed permissive resolution. They remain failures and were not edited. The reviewer independently confirms foreign release/representation rejection at the native boundary. A future fixture update should preserve the original attack and arrange lawful registration before testing the later boundary.

## Risk-ranked findings and minimal correction

1. **P1 — public event snapshots mutate the internal ledger.** `events` and `release_history` expose the same frozen event objects, whose nested `payload` is still a mutable dictionary. Mutating `executor.events[-1].payload` changes the event's content-derived reference while `_events_by_ref` retains the old key. Reproduced through the public property without private access; `test_public_snapshots_are_immutable` fails and `test_OBSERVED_public_event_payload_changes_internal_identity` confirms identity drift. Deep-freeze payloads recursively at construction and return immutable or detached values. Test nested collections, not only the frozen dataclass shell.

2. **P1 — checkpoint replay does not bind all event and receipt semantics.** Independently rehashed checkpoints are accepted after changing publication `replay_root_ref`, `determinant_set_hash` or `producer_permission_ceiling` to values inconsistent with the unchanged subject. Also a rebuild eligibility receipt for release B can link release A's event: only the event kind is checked. Reproduced in three publication cases and `test_OBSERVED_rebuild_receipt_can_link_event_for_different_release`. This is internal semantic inconsistency, distinct from the unavoidable external-authenticity HOLD for a coherent whole-history replacement. Reconstruct event-specific expected fields and all receipt identities from replay; compare release, product, scope, payload, input sets and receipt cardinality, not just enum kind and projected status. Apply that audit to invalidation, rebuild-link and GC receipts too; those additional variants are static gaps, not separately demonstrated exploits.

3. **P1 — selection checks and commits are not serialized.** Two actual `select_current` calls can both validate `expected_previous_receipt_ref=None`, then both return successful receipts. A barrier around the existing predecessor-check helper controls an ordinary permitted interleaving; it does not replace the validation result or supply forged state. The resulting history fails cold restore, either at predecessor/ordinal validation or receipt predecessor replay depending on scheduling. Accepted `test_h10` proves sequential stale-call rejection only. Hold one lock/transaction across validation, event allocation and all projection writes; test both interleavings. This is local concurrency failure, not an authorized protected-current execution.

4. **P1 — torn mutations have no recoverable commit boundary.** An injected exception immediately after the real `_append_events` in `publish_product` leaves a committed publication event and an UNPUBLISHED projection. Exporting that state produces a checkpoint rejected on cold restore. The prior complete checkpoint restores correctly. This is a deterministic fault-injection model of the in-memory interruption point, not evidence of an actual OS-kill or durable-storage test. Stage an entire new state and atomically publish it, or provide a durable transactional log plus recovery protocol. Neither owner currently promises process-persistent storage; completeness beyond a saved checkpoint remains unproved.

5. **P2 — direct helper and Python access bypasses remain.** Saved `_append_events` accepts unregistered PRODUCT_PUBLISHED and CURRENT_SELECTED events even when `_native_security_mode` is set to a refused external mode. Saved M2 `_insert` inserts a non-ReleaseCore into `_releases` without preflight or type checks. `_commit_selection_transition_receipts` similarly writes indexes without a guard (static inspection). Native underscore helpers and dictionaries are reachable to a same-process Python caller. Do not present private naming as isolation. Add internal validation to reduce accidental bypass; authenticated operations require a separate principal/process boundary whose callers cannot mutate owner fields or replace methods. The negative external-mode probes grant no protected permission.

6. **P2 — M2 collision insertion is check-then-write.** Controlled two-thread scheduling of `_insert` with a test dictionary makes both colliding preimages read absence and write successfully; the later value wins. This demonstrates the helper's non-atomic algorithm under instrumentation, not a separately proven public writer exploit with immutable records or a durable multi-process store. Serialize collision comparison and insertion within the same repository transaction. Test public record collisions with a defined storage concurrency contract.

7. **External authority HOLD — no independent issuer, authenticated epoch, revocation stream or custody root.** Exact references, hashes, permission ceilings and replay grades are constructor-provided. A coherent replacement corpus round-trips as LOCAL_UNAUTHENTICATED and `require_external_issuer` refuses. That is appropriate refusal, not proof that the corpus is authentic or complete. No verifier, expiry policy, authenticated subject entitlement or independently anchored history was supplied. Do not promote any local PASS into issuer/custody acceptance.

## Method and route coverage

`01_METHOD_MATRIX.json` lists all **17 B5 mutators and five M2 store writers** individually, with native guard result, local evidence and external HOLD. Each saved class method is executed in three refused modes with required arguments supplied; all reach EXTERNAL_ISSUER_HOLD before validation. This verifies in-body guards without a detached monkey-patch. It does not prove authorization in the default LOCAL_UNAUTHENTICATED mode.

B5 local checks cover staged/register/publish separation, exact selection key/receipt, family/scope separation, explicit NO_CURRENT, supersession, withdrawal with explicit transitions, invalidation and blocked recertification, cache drop/materialize, GC class/retention constraints, rebuild eligibility/link and checkpoints. Additional positive reviewer cases exercise cache materialization and rebuild linking rather than relying on source inventory alone. All writers share event and store defects above; bounded local checks are not a blanket per-method PASS.

M2 module routes `register_producer_subject`, `constitute_closure`, `constitute_release`, `register_representation` and `publish_binding` call the five guarded repository methods; this is visible in native source and exercised by source-free fixture/accepted tests. Repository release registration checks exact subject, producer contract, closure kinds/members and replay grade; representations and bindings check same-release/subject and integrity linkage. Direct helper bypasses remain separately documented.

The actual M2 route is **release ref → `release_exact` → `release_subject_ref` → producer subject** through `resolve_subject_exact`. `test_actual_m2_release_to_subject_route_and_b5_crosscheck` exercises it and rejects direct lookup of a release as a subject. N04 `b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2` and N04R `fde95ee9275f9fe14b6868db363035757cffab48` owner-gap analyses were read as historical review evidence. Their detached overlay classifications do not determine native acceptance. B5's cross-owner check is explicit/optional, not automatically called by staging; it verifies release/producer consistency and does not independently authenticate a semantic projection or permission ceiling.

## Replay, applicability and recovery verdicts

| Requirement | Verdict and evidence |
|---|---|
| Ordinal and immediate predecessor | PASS for invalid append refusal without mutation; concurrent commit FAIL |
| Rehashed projection drift/truncation | PASS for authored negative cases; publication semantic/receipt mismatch FAIL |
| Wrong type, scope, duplicate exact subject | PASS bounded native rejection; duplicate identity tested without state mutation |
| Invalidated release recertification | PASS local refusal without mutation; external new authority HOLD |
| Current vs historical as-of | PASS sequential exact-event and checkpoint resolution; no issuer-time epoch policy |
| A→B→C and A→B/C→D | PASS local graph closure, unrelated sibling retained, cold roundtrip |
| Complete local checkpoint restore | PASS; coherent alternative also restores only as local unauthenticated |
| Authentic/complete external checkpoint | HOLD: no independent anchor; replay is not authentication |
| Torn process / concurrent writers | FAIL fault/schedule probes; no actual kill/durable recovery qualification |
| Python same-process adversary | FAIL as isolation boundary; mutable public payload is reachable even without private access |

`02_FROZEN_TO_NATIVE_MAP.json` preserves the original text of all **24** expectations and records native owner, status and evidence. An untouched snapshot plus its SHA256 is retained under `repro/`. The original detached S06R suite was read, **not executed as native acceptance**. S06T's prior detached failure is not counted here. Epoch/revocation expectations have explicit HOLD because native schemas do not provide authenticated issuer state; coherent forgery is not relabeled a locally detected attack.

## Resources and publication

Governed sparse worktree: `/Users/matthewsmith/.codex/worktrees/hq284-s06fr-native-security-r1/Rawlsing`, assigned branch `agent/reviewer-pyat-r3-hq284-s06fr-native-security-r1`. Startup and candidate objects verified; production files retain candidate bytes. Git registered this worktree; the app attachment API did not recognize it as an app-managed worktree. No clone, reset, broad fetch, shared-checkout edits or raw-source checkout was performed.

Actual session context attests OpenAI `gpt-6.1-sol`, effort `low`; host Matthews-MBP.lan, MacBookPro15,1, x86_64. Python 3.11.3 at `/usr/local/bin/python3`, pytest 9.1.1, macOS 13.7.8. No reasoning/model escalation. User designated the secondary account; no independent hardware/account registry was supplied. Initial usage 0%/0%, prior stop 7%/1%, resumed observation 10%/2% used. The user explicitly rescinded the quota floor (“bro fuck the quote and finish the work”, corrected to “quota*”). Historical stop evidence remains intact; it is superseded, not deleted. Reset credits used **0**, paid overflow **0**, primary account unused, Go pool UNKNOWN/not used. No survey originals, authenticated CURRENT, external credential or V3 execution.

Publication SHA is verified from the assigned remote ref after commit/push and reported in the handback. No canonical merge or production correction is part of this review.
