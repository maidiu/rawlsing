# S09 — Maximal lawful software adaptation, legacy migration and ordered build flights

**S status:** DESIGN_ONLY / new engineering packages PROPOSED / no production edits. Integrates B0–B7 with D T0.1–T0.5, rather than serial independent backbones. Existing S36 CandidateStore/C9 transaction and S37 QualifiedC12Store/branch ledger must be extended rather than replaced. Implementation owners choose exact language/import location after finding current canonical assembled source branch. Estimated durations below are **planning ranges derived from B indicative B0–B7**, not measured staffing predictions or commitments. Original source, science and native permissions are separate.

## Dependency-resolved first tranche: maximum allowed sourcefree engineering
| Ordered joint tranche | Exact proposed code-edit set and functions | Reuse/boundary | First working consumer, acceptance, gate | Indicative size/duration/risk |
|---|---|---|---|---|
| **F0 = B0 + T0.1** Portable source identity and module custody | new source_registry.py: SourceRef, resolve_source, verify_owner_role, verify_hash, injection root map; refactor S48 ProductTransport settings and S52 bootstrap absolute G18 reference only in versioned new adapter | Keep B 59-file old hash manifest, S37/S52 source evidence; reject unpinned syspath and hardcoded Mac provider/model | S48/S52 test bootstrap and C9 adapter; wrong hash/source ROLE rejects, same cut deterministic | 3–5 engineering days, ~250–600 LOC proposed, LOW-MED |
| **F1 = B1 + T0.2** One actor state, ledger and transaction/migration | actor/schema.py ActorVersionV1; actor/ledger.py append_event; actor/decision.py commit_decision/true_nochange/held; actor/storage_adapter.py bridge_existing_candidate_c12_store; migration/v3_reader.py read_old_as_archive; derived.py pure_registry; readiness.py gates | S36 CandidateStore keeps response/target authority; S37 C12Store/QualifiedC12Store remains one event lineage; no second ActorSnapshot and Version store | C9 test generic reader + C12 receipt; sourcefree valid-empty, missing rule hold, outbox/recovery/cold-fork, no old V3 psyches auto-populated | ~700–1400 LOC, 10–16 days schema + 8–14 transaction overlap, HIGH integrity |
| **F2 = B2 + T0.3** Access-filtered memory/read boundary and one-way V2 | memory/access_projector.py select_accessible_features, projection_no_leak; surface/actor_view.py read_only; event/receipt tests; exclude M37 annotation from memory | ADP016/017 owned semantic feature types; serialization-only before new rule | Inject S48/old V2 port an actual actor-safe packet; remove one accessible feature and no direct/indirect leakage, no analyst event IDs/count/order | 5–10 engineering days, ~300–650 LOC, MED-HIGH |
| **F3 = B3 + T0.5** Sequential proposal, source/clock and no-ghost batch shell | batch/schema.py 3to5_validate; batch/realize.py per_source_owned_step, advance_interval_port, read_prestate; batch/receipt.py hold_suffix/commit_policy_unselected; test-only injection S42 and S46/47 | Reuse S42 event admission, S46 actual interval, S47 conditioner, S48 one-call transport; prospect text never event truth | test controlled source events with 3/4/5, source-invalid E2, world-committed/actor-held and actor access failure. POLICY=UNDECIDED cannot auto-choose prefix | 12–18 days for shell, ~500–1000 LOC, HIGH |
| **F4 OPTIONAL = T0.4** Typed composition/relation STORAGE ONLY | organization/procedure_index.py typed PRACTICE/MEDIATOR contained composite and context query; provenance and version index, candidate-only relation evidence | No new CAN011 kind, no Rule A/T, default relation store absent; optional until owner demonstrates benefit | query manually issued test-only payload by scope with fixed readset; no coactivation auto writes | 5–10 days ~250–500 LOC if needed, MED; optional not prerequisite for F3 |

The exact candidate LOC is a **rough architectural budget**, not a code inspection claim. Each flight has acceptance when it improves portable, deterministic, fail-closed engineering under qualified test-only fixtures, with science/source/native gates explicitly unresolved. Flight F0–F3 may be split for independent review but form one canonical schema and coordinated unit of work. Do not start with a separate GraphMind, ActorStateV1 and PersonState store independently.

## Competing sequence resolved
B recommended B0 custody→B1 schema/pure derived/migration→B2 ledger/surface→B3 event transport; D recommended T0.1 resolver→T0.2 actor/ledger→T0.3 memory→T0.4 graph→T0.5 batch. We **merge** B0/T0.1, B1/T0.2, B2/T0.3, B3/T0.5, with T0.4 relation storage deferred unless sanctioned after functional-organization proof. Rationale: a memory packet needs a trustworthy event/actor receipt; a batch shell needs one authoritative ledger; a relation registry without original science is not the highest-leverage dependency. Pure derived, migration and true nochange/held statuses belong inside F1; memory and batching belong inside F2/F3 rather than competing ledgers. Extensible typed ports preserve future modules without prematurely attributing subjectivity.

## Later source/science/native owner-controlled tranches
| Later tranche | Precise dependency | Owner and right | Finite acceptance |
|---|---|---|---|
| G1 B4: real people/world/care activity | C0/SDTF position and actual resource/time + real C8 B-owned events; S49 adapter current [] | Pyat/source custodian, C8/ADP019, care/actor source | independent B act/decline, actual labor/care/rest/source and actor reception separated |
| G2 B5: concrete Rule A/T formed practice | existing CAN008/011 v1 with issued domain operands, negative and nochange; optional composite | original CAN008/010/011 scientist, independent reviewer, C9 engineer | E1 positive *and* evaluated nochange, missing-rule HOLD; E2 semantic consumed; rival external-only |
| G3 B6: rupture/meaning/trace | CAN012 real event, ADP016/017 accessible memory, SCI05 source and postcall admission | original CAN012/ADP/SCI05 owner | false belief sourced, no fabricated memory; narrator-only perturbation no psyche; SCI05 denial invalidation |
| G4 B7/T2: C0/C11 native weld and C12 | PRE-MAIN source-local release, C11 facade/Route B permits, security and original actor grants | Pyat C0/C11, C8/C9/C12/A0–A5 authority | verified source→real event→actor history→C9 Rule A/T→C12 fork/cold/V2/A5; NOT sourcefree fixture |

The sourcefree flights cannot waive or simulate original C11/Pyat law. Source rights, actor ownership and competent domain science may be withheld while engineering still progresses.

## Migration/historical compatibility contract
1. Verify immutable original old file hashes against B register; mismatch quarantines it. Preserve original yearly JSON, Wound/Framework/Crack/Practice, V2 output and Enneagram only as read-only historical artifacts.
2. For each M row select mapping: SOURCE_VERIFIED, CARRIER_ONLY, DERIVED_VIEW_ONLY, OLD_FORMULA_UNAUTHORIZED, UNKNOWN, SOURCE_HELD. Never import class/type/religion/age psychological seeds, 50 baseline, static hopeful parent, one-valence shard, forced crack, age rupture or prose support as formed state.
3. Separate objective material facts from actor received meaning and current acting B. A current qualified event can be stored in existing C12 world ledger; old state cannot be promoted merely because historically serialized.
4. Derive pure views from canonical actor snapshot; no hidden writes to state.metabolic_style or registers; cache keyed exact source state hash and version. Read-only render with actor-access envelope.
5. Reconcile existing CandidateStore C9 transaction and C12 append-only event lineage with one actor Version/Receipt mapping. If distributed stores cannot atomically commit, outbox recovery and partial status. Preserve old C12 hashes and branch lineage; no in-place overwrite.
6. On migration error return archived original + migration HOLD; no partial new psyche. Repeat same source/hashes idempotent; changed source hash forced fresh qualified migration decision and old actor untouched.

## Acceptance tests with exact grade
| Test | Input, visible assertion | Status under S |
|---|---|---|
| T01 portable source | mismatched B/D source hashes, missing root or changed role fail closed | NOT_RUN |
| T02 canonical state | one actor id/branch/version, one decision receipt, duplicate commit identical, changed payload rejects | NOT_RUN |
| T03 pure derived | M26 state/registers/metabolic_style unchanged by view, old migrator quarantines writes | NOT_RUN |
| T04 true nochange | actually applicable issued test Rule T returns TRUE_NO_CHANGE_EVALUATED vs held missing rule | NOT_RUN |
| T05 external success | unchanged actor, changed sourced B tool/aid produces externally assisted activity | NOT_RUN |
| T06 positive learned operation | E1 admitted practice value read by E2 Rule A with world/B controlled, cut learned read effect vanishes | NOT_RUN |
| T07 absent original source | missing B/C0 Rule produces SOURCE_HELD, no ghost person/world action | NOT_RUN |
| T08 mixed episode | physical deprivation + affection + independent co-care; ambiguous child receipt permissible | NOT_RUN |
| T09 memory | ADP feature removed blocks direct and indirect retrieval including IDs/count/order | NOT_RUN |
| T10 N batch | 3–5 proposals, sequential 4 real intervals, fault E2, no invented suffix, policy UNDECIDED remains hold | NOT_RUN |
| T11 SCI05 | deny half1 internal act after N+1 call, invalidate dependent half2 prospects | NOT_RUN |
| T12 rendering | V2-only prose/annotation perturbation cannot change later psyche; postcommit render failure not CLEAN | NOT_RUN |
| T13 S52 verifier | _OPENING base_ok true plus S52-only error must produce verifier failure | NOT_RUN, earlier static risk |
| T14 native source | separate Pyat release, actual B, C9 rules, C11 weld and A0–A5; real actor continuity | NOT_RUN/NATIVE HOLD |
| T15 existing regression | RB observed 116/116 sourcefree, preserve via future isolated rerun after code | RB EXECUTED; S NOT_RUN |

## Release gating and worker independence
All F1→F3 schema, migration and batch code must use one owner-held integration spec and independent hostile test reviewer before adoption. Code owner may implement on a fresh isolated branch after HQ authorization; no SYN02-S implementation, no issued science. Preserve immutable original user models and reviewer evidence; do not repurpose active Sorok/Pyat/Codex sessions, nor auto-switch model/harness/account. No production toggle, PR merge, force push or common atlas write authorized.
