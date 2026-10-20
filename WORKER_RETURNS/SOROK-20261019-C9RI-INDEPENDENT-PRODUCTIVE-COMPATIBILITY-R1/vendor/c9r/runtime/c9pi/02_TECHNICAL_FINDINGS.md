# C9PI technical findings on the exact target

These are sourcefree boundary findings, not demonstrated remote exploits or findings against production owners. A trusted internal API may legitimately take prevalidated objects; C9P has not supplied the missing authenticated external integration that would establish those preconditions. Its published complete/fail-closed boundary claim therefore exceeds the evidence.

| Module | Executed or inspected behavior | Disposition |
|---|---|---|
| `identity.py` | Canonical sealed schema, ACTIVE flag, nonempty standing and source strings; future currentness refused. Arbitrary resealed ADP007 reference/hash admitted. No source resolution, owner receipt or source-hash recheck; readset carries source ref only. | Technical shape checks usable; authentic actor eligibility unproved. |
| `events.py` | Content hash, time order and presented parent membership checked. Invented native receipt admitted; actor_role not bound to focal actor; no scene/encounter grant resolution. Same event ID can enter twice with different content/time. | P1 source/subject/occurrence identity gap. |
| `conditioning.py` | Actual guard call, subject/class/seal checks; guard denial only recorded. as_of unused; content not consumed; source_hash not checked against source content; mutable dictionaries inside frozen view. | P1 current/source/read-only boundary gap. |
| `response_rules.py` | Registry key and caller `issuer_verified` determine lookup. Predicates/readset policies/effect/numeric/stochastic declarations do not implement qualification. Nonempty strings/tuples emit fixed practice proposal; `prior_response_count` unused. | Scientific qualification absent; arbitrary registry labels are not issuance. |
| `target_rules.py` | Typed absent/unissued/missing/revoked/expired/prestate/subject/semantic/operation checks execute. `response_hash`, `issued_at`, scope and authenticated registry currentness are not checked. Hash-only fallback can select across authority/version keys; test A/T rules share one hash. Only history truthiness required. | P1 exact separate target/response/clock/issuer custody gap. |
| `transaction.py` | Existing occurrence and sealed response checked; BEGIN IMMEDIATE publishes response/target/journal/receipt/clock, rollback passes tested row/schema failures. Trusts caller TargetDecision and claimed record digest, with no full original readset or permission revalidation. Snapshot excludes schema definitions/metadata. | Useful bounded atomic scaffold; no inherited B3AS full readset guarantee. |
| `later_action.py` | Named object reads committed row and compares returned hash with independently stored row. Does not bind returned body to that hash, actor to expected subject, or consumer registration to a native owner. Any nonempty action-owner ref can make READ_OK; still not action admission. | P1 counterfeit-record defect; performed action unproved. |
| `action_admission.py` | Missing/invalid/mismatched actor/act/future time and empty consumed argument refused. Self-sealed imaginary occurrence/actuator admitted. Receipt's consumed_state_hash not compared to consumed argument. No lower commit time, genuine occurrence lookup or actuator authentication. | P1 fictitious performed-action and target-binding gap. |
| `release_gate.py` | Exactly seven default holds; fixture_supplied_authority ignored. Raw Boolean arguments directly remove holds; all-true returns AUTHORIZED. No authenticated-source inputs. | Preserve default holds, do not call this authentication. |
| `native_custody.py` | Imports all three native files, computes blob/SHA; optional expected blob can enforce mismatch. Original tests mostly assert nonempty fingerprints. | Reviewer probe independently checks exact bytes and imported paths. |
| `pipeline.py` | Composes all eight stages; occurrence admitted before response/target commit. Proceeds to later/action stages even after aborted effect commit. `committed` means transaction commit, not CREATE or genuine action. `no_ghost` is True for every successful commit and is not an external integrity attestation. | Reuse wiring carefully; result flags must retain scope. |
| `canon.py` and `__init__.py` | Deterministic public SHA sealing, public exports. No signature/issuer authentication. | Reusable integrity primitive; not authority evidence. |

## P1 — Exact target record is discarded and identity changes at publication

`evaluate_target` seals a record containing semantic object, effective time, lifecycle, registry, payload and causal parents. TargetDecision returns only the record hash and a few fields. `CandidateStore.commit` builds a **different** smaller row containing the claimed record_hash and before/after hashes. It does not store the sealed full preimage or validate that the published body hashes to the decision's record hash. A later reader therefore cannot establish what practice, when, or from which actual parents was accepted.

The supplemental cold-reopen assertion fails on missing semantic_object_ref. Its later effective-time and parent assertions are retained but not reached; those omissions are confirmed by the stored row/source, not counted as separate executed failures. When proposal.target_middle_state_id is explicit, evaluation uses that identity for duplicate checking/record construction but commit always uses proposal_hash. The exact identity roundtrip assertion is RED. A fabricated public TargetDecision with no permission source also publishes a target; this is an internal trust-boundary observation, not proof that untrusted requests reach that API in production.

## P1 — Source and grant identity are assertions by the caller

The first court independently reseals malformed-but-canonical actors/events/sources and fabricated registry bodies. They pass integrity because public digest equality authenticates bytes, not origin. CAN008 R2's semantic adoption record does not authorize the invented concrete rule. Target issuer allowlists and `issuer_verified` flags supplied alongside their own forged registry cannot establish separation.

The grants with WRONG_RESPONSE, future issued_at, and REVOKED_SCOPE each still CREATE. The response hash is carried but never compared, issued_at is carried but never bounded, and scope has no evaluated law. Source/permission changes after evaluation are absent from commit's arguments/readset revalidation. The revocation test mutates the presented grant, not a real registry (none exists); it therefore establishes the **missing reread API/invariant**, not the behavior of a nonexistent external revocation service.

The explicit source-removal test likewise does not simulate a genuine accepted source registry. It demonstrates that the store's commit boundary can operate with only an already constructed decision after the original actor/conditioning inputs disappear. An immutable authorized snapshot could be a legitimate design, but would need an exact snapshot identity, currentness/revocation law and accepted scope; none is supplied here.

## P1 — Historical labels suffice and material source content is ignored

History is passed directly as tuple[str]. No function resolves action ownership, independent witnesses, actor, project, opportunity, time, actual occurrence or distinctness. The independent single-invented, duplicate, and future-foreign tuples all produce CREATE. Offer and material opportunity are strings tested for presence. A's imagined offer satisfies the same condition as P's actual action would. Future-world, wrong-scene, access-denied and observer-private conditioning contents are not consulted in selection. Thus those scientific REDs expose missing implementation rather than testing a particular unissued empirical acquisition threshold.

## P1 — Later returned record and performed receipt can be fictitious

A reviewer consumer returns invented content plus digest(real_store_row). The existing independent store check accepts that pair and publishes the invented content in committed_record with a practice-mediated route. It needs a check of the actual returned body/preimage, not only a caller hash against another source. Omitting the mediator entirely correctly returns STATE_ABSENT (PASS).

A publicly sealed performed receipt can name an invented actuator/never-performed occurrence. The consumer argument can name a different consumed state from the receipt; admission returns the argument's hash anyway. An action at time 1 is accepted for an as_of=40 call without any supplied target commit lower bound. These are candidate admission failures; no actual action took place.

## Native guard and release gate

Native mutation is confined to a disposable exact file. The mutation changes `_deny`'s outcome enum while preserving all call signatures, source inputs and candidate implementation. The diagnostic test changes from PASS to AssertionError; the unmodified TEST_ONLY CREATE test remains PASS under that same fault. Default production transition authorities remain empty. Neither result authorizes positive native integration, and neither proves an installed actor-positive consumer was bypassed. That consumer is unbound.

The guard request also uses a fixed C9P subject sentinel and fabricated empty-baseline fingerprints, rather than the actual actor/store prestate. That is appropriate only as a diagnostic zero-effect request; it cannot attest the published transaction's actor-state conservation.

The release gate is ordinary Boolean aggregation. Its default seven holds are sound as a declaration of known missing authorities. Its all-true code path is not an independently authenticated release decision. The author suite's all-true fixture remains byte-exact evidence of this distinction; this review does not adopt that result.

## Atomicity, schema and cold replay scope

Both new row-trigger and schema-column-interference trials abort and preserve prior rows, including the admitted occurrence, through close/reopen. Original injected late failure and rollback checks pass. These are meaningful local transaction positives. Snapshot equality covers table names and rows, not sqlite_master definitions, indexes, triggers, views or PRAGMA metadata. Our schema trial provokes an insert-shape error; **it does not prove general schema-race rejection**. B3AS's stronger accepted full logical publication readset is available for reuse and remains separately scoped.

Cold replay uses two fresh builds and two fresh inspectors, each in a distinct interpreter and PID, against two databases. Snapshots, target hashes and later read receipts match exactly; integrity_check is ok. This proves deterministic TEST_ONLY persistence/reconstruction, not actual historical truth, power-loss durability, source rights or developmental science.

All case names, assertion statuses, logs, fault preimages and byte restores are machine-readable in `evidence/` and `custody/`. No fixed endpoint or test was repaired to improve a green count.
