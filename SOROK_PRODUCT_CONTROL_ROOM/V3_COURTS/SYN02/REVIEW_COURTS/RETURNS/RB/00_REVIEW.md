# RB — independent hostile review of SYN02-B and SYN02-D

**Review branch:** `agent/sorok-syn02-review-rb-source-runtime-migration-r1`  
**Sealed startup:** `1ede5e7e814b22e6e652fb01549d4a10f5dec18c`  
**Pinned targets:** SYN02-B `d8f8b4f7610a4a28d86cf6d0c08f5d297d74d6e3`; SYN02-D `f904955e1c6f4db2d7fdebf8d2a6b78029274a5f`  
**Role:** independent I3 historical/current-source and execution-architecture reviewer; not SYN02 A/B/C/D author, Sorok HQ, production editor, native scientific/source issuer or own reviewer.  
**Surface/model:** local macOS OpenCode / DeepSeek V4.1-Flash selected session; read-only source and sourcefree tests; no provider/model call, prompt switch or paid account assumption.  
**Terminal:** `SYN02_RB__B_40_DISPOSITIONS_REVISE_REUSE_SEMANTICS__D_CURRENT_SOURCE_AND_116_TESTS_REPRODUCED__ARCHITECTURE_MERGE_HOLD__SCIENCE_HOLD__NO_NATIVE_GRANT`.

---

## 0. Preflight, independence and custody

- The review branch was created from the exact sealed startup `1ede5e7e814b22e6e652fb01549d4a10f5dec18c`; the pinned B and D targets were verified at their exact commits before review.
- A dedicated isolated worktree (`syn02-rb-wt`) was used. The B and D author worktrees were read-only; no author branch, source, production, CAN/ADP/Pyat, atlas, sequencer, PRE-MAIN or other worker file was modified.
- The B source plane was checked against the historical staging tree: **59/59 declared paths SHA-256 exact**; the TD-R05 selected manifest is **31/31 exact**. The local ZIP is not the TD-R05 archive; whole-archive identity is not claimed.
- The D current-source path was inspected at the exact cuts in D/01. Key source hashes match D's table, including S37/S36/S42/S44/S46/S47/S48/S49/S51/S52 and PRE-MAIN C0/C11. The 116 claimed sourcefree tests were independently rerun by RB: **116 passed, 0 failed**, in the same group counts as D.
- No raw respondent/survey data, LLM call, current native C11/C12/A5 execution, production edit, source grant or self-adoption occurred.
- B's 59-source identity and D's current source/test receipts are therefore accepted at their **source/test-only** grain, not as native personhood.

---

## 1. Executive verdicts

### 1.1 ENGINEERING

**`ACCEPT_SCOPED_WITH_PRECISE_CORRECTIONS`.**

B's 59/59 and 31/31 identities are exact. B's 40-family disposition matrix is actionable and largely well-grounded. D's current C12/C9 map, key hashes, 116 sourcefree tests, empty production Rule A/T registries, S48 one-call/refusal, S49 empty B root, S52 path/verifier risks and C0/C11 disconnect are independently confirmed.

The major engineering corrections are:

1. **B's `3 REUSE` count conflates literal old-function reuse with reusable invariants.** M26's literal `compute_all_derived` writes `state.registers` and `state.metabolic_style` and the old invariant checks only six names; M30's literal V2 has age/parent/narrator problems; M29's `render_year` is immediately nonmutating but the surrounding band is not transactional and later prose feeds psyche. Only M29's immediate surface function is literal-reuse-safe at a scoped grain; M26/M30 are invariant/jurisdiction reuse only.
2. **B's "40/40 selected-source/focused-test" is overbroad.** 40/40 selected-source review is accepted, but focused-test coverage is uneven: RX03 found no focused topology/boundary/coherence tests and no mechanism-specific status/lifecycle tests for M19; M16 spawn/retire and M09 lifecycle are likewise not covered by focused tests.
3. **B's M37 server re-render correction is imprecise.** `server/generation/simulation.py` does call `render_year` in its non-LLM branch; `v3/run_and_print.py` has a separate final band/re-render after its loop. The distinction is where the render occurs, not that the server never renders a non-LLM year.
4. **B's `ActorSnapshotV1` and D's `ActorStateVersion`/`PersonState` are overlapping candidate actor stores.** B's `CanonicalEventV1`/`TransitionReceiptV1` and D's `CanonicalEventLedger`/`DurableDecision` also overlap. A future SYN02-S implementation must choose one canonical actor/ledger/receipt schema; parallel stores would violate one-psyche/no-duplicate-actor-system.
5. **D's S52 cold-open `ok=True` is a real static code path but not exercised by the 13 passing S52 tests.** It remains a readiness defect, not a reproduced failure. D correctly labels it static; do not upgrade it to a native positive.
6. **D's `PREFIX_CONTIGUOUS` is an engineering recommendation, not a user-adopted policy.** External world/B actions are irreversible; the batch policy remains a C6/C9/C12 owner decision.

### 1.2 SCIENCE

**`HOLD / RULE_UNISSUED`.**

No concrete CAN008 Rule A, CAN011 Rule T/NO_CHANGE, care/activity/interval rule, functional-relation formation/recruitment law, memory/SCI05 admission rule or developmental coefficient is issued. B's “functional connection” remains a candidate representation, not a scientific law. D's `FunctionalRelation` store may be built as storage, but coactivation must not create a relation; a competent owner must issue formation/recruitment or withhold. The 116 sourcefree tests are engineering evidence only.

### 1.3 AUTHORITY

**`NO_NATIVE_GRANT / CURRENT C9-C12 HOLD`.**

B and D correctly preserve source/actor/native separation. C0/C11 PRE-MAIN modules exist but are not imported by S37/S52 and do not grant a C12 person or Pyat weld. C9 production registries are empty; S49 natural B source is `[]`; S48 is one-call transport; S52 is conditional and its verifier is risky. Current progress records native C12=0, C11=0, A5 NOT_RUN. No production, source edit, merge or native grant.

---

## 2. B claim adjudication

| # | B claim | Verdict | Independent evidence / correction |
|---|---|---|---|
| B-01 | 59 source paths accessed/hashed; 31/31 S50 exact; ZIP vs file-level caveat | **AGREE_SCOPED** | RB verified 59/59 SHA-256 exact and 31/31 selected exact. Whole-ZIP identity not claimed. |
| B-02 | 40-family disposition matrix complete; 3 REUSE / 31 ADAPT / 3 REPLACE / 3 REMOVE | **AGREE_SCOPED at design grain; REVISE_PRECISE on REUSE semantics** | All 40 are dispositioned; the 31 ADAPT and 6 REPLACE/REMOVE are appropriate at design level. The three REUSE entries do not all mean literal source reuse. |
| B-03 | M26 is REUSE of pure derived invariant | **REVISE_PRECISE** | Literal `compute_all_derived` writes `state.metabolic_style` and `state.registers`; `assert_no_derived_fields_in_backbone` checks only six names. RB probe: `metabolic_style` changed from `{}` to `{current:compartmentalizing, trend:stabilizing}`; no six protected names stored. The **invariant** is reusable; the literal function is not. Disposition should be `REUSE_INVARIANT / ADAPT_BODY`. |
| B-04 | M29 is REUSE immediate render-only | **AGREE_SCOPED for `render_year`; REVISE_PRECISE for the band** | `render_year` immediately writes only `rendered_output`; RB probe confirmed backbone hash unchanged. But `run_llm_band` can apply psychic deltas before Pass 2 and has no rollback on Pass 2 failure; next-year prose→psyche is outside `render_year`. Literal reuse is scoped to the surface function, not the band. |
| B-05 | M30 is REUSE one-person V2 jurisdiction | **REVISE_PRECISE** | The one-person/read-only **jurisdiction** is real, but literal old V2 contains age<17→35 chat override, LLM parent narrative in backstory, and the narrator-prose→psyche edge. The old `build_persona_sheet`/V2 path is not reusable unchanged. |
| B-06 | M31/M33/M39 REPLACE | **AGREE_SCOPED** | M31 causal type/parent effects, M33 mechanical sampler, M39 age-band rupture are not the target mechanism; replacement is appropriate. M39's crosswalk correction is correctly flagged rather than silently inserted. |
| B-07 | M34/M35/M36 REMOVE | **AGREE_SCOPED** | Forced fallback, placeholder repair and unknown-parent defaults are historical fabrication/default defects. Removal is appropriate; valid-empty/unknown must replace them. |
| B-08 | M14/M15/M17/M21/M22 deep ADAPT rather than field addition | **AGREE_SCOPED** | M14 scalar/enum topology is not a relation; M15/M22 inherited baselines/child model are wrong-meaning; M17 one-valence shard is not mixed impression; M21 route trace is not conserved psychological substance. Deep rework is warranted. |
| B-09 | 40/40 have selected-source/focused-test review | **REVISE_PRECISE** | 40/40 selected-source is accepted. Focused-test coverage is uneven: RX03 found no focused topology/boundary/coherence tests, no M19 status/IRR tests, no M16 spawn/retire tests, no M09 lifecycle tests. “Focused-test” must not imply mechanism-specific tests for all 40. |
| B-10 | M37 server non-LLM-year re-render correction | **REVISE_PRECISE** | `server/generation/simulation.py` does call `render_year` in its non-LLM branch; `v3/run_and_print.py` has a final band re-render after the loop. The correction should say “server per-year render and separate run_and_print final re-render,” not “server non-LLM re-render is incorrect.” |
| B-11 | Migration schema `ActorSnapshotV1`, event/receipts, LegacyV3Reader, archive, valid-empty | **AGREE_SCOPED as design; HOLD on schema merge** | The design correctly separates durable/derived/surface/diagnostic and quarantines synthetic/default/type/placeholder/narrator atoms. However, `ActorSnapshotV1` overlaps D's `ActorStateVersion`/`PersonState`; `CanonicalEventV1` overlaps D's `CanonicalEventLedger`; `TransitionReceiptV1` overlaps D's `DurableDecision`. One canonical actor/ledger/receipt owner must be selected before implementation. |
| B-12 | B0–B7 tranche plan; B0+B1+B2+B3 shell largest lawful immediate | **AGREE_SCOPED as design; HOLD on exact merge** | The plan correctly separates source/schema/ledger/surface from science/native rules. It must be merged with D's T0.1–T0.5; see §4. |
| B-13 | No new scientific law; no native grant; no implementation | **AGREE_SCOPED** | B does not issue a rule or claim native execution. The dynamic relation question remains SYN02-C/science. |

### 2.1 All forty B dispositions

**ADAPT rows are accepted at disposition level** (`AGREE_SCOPED`), subject to the semantic owners/rules and the corrections above. The non-ADAPT rows are adjudicated explicitly.

| M | B disposition | RB verdict | Reason |
|---|---|---|---|
| M01 | ADAPT | AGREE_SCOPED | explicit state/provenance carrier; end field conflation |
| M02 | ADAPT | AGREE_SCOPED | typed material carrier; no care/schedule |
| M03 | ADAPT | AGREE_SCOPED | regulation carrier; no fixed law |
| M04 | ADAPT | AGREE_SCOPED | concrete constraints; one support-load authority |
| M05 | ADAPT | AGREE_SCOPED | appraisal projection only; no universal domains |
| M06 | ADAPT | AGREE_SCOPED | fix phantom fields/clamp loss |
| M07 | ADAPT | AGREE_SCOPED | access/expression; no narration memory |
| M08 | ADAPT | AGREE_SCOPED | scoped sensitivity; no demographic seed |
| M09 | ADAPT | AGREE_SCOPED | episode-linked tension; remove placeholder/seeds |
| M10 | ADAPT | AGREE_SCOPED | support/cost with actual source |
| M11 | ADAPT | AGREE_SCOPED | keep acute/chronic operator; acquisition/history missing |
| M12 | ADAPT | AGREE_SCOPED | move institutions/ties to world owner |
| M13 | ADAPT | AGREE_SCOPED | practice carrier requires actual activity |
| M14 | ADAPT | AGREE_SCOPED | keep hysteresis; reject global enum |
| M15 | ADAPT | AGREE_SCOPED | finite need vocabulary; scoped expectation |
| M16 | ADAPT | AGREE_SCOPED | object identity; remove age/random spawn |
| M17 | ADAPT | AGREE_SCOPED | witnessed event shell; mixed impression |
| M18 | ADAPT | AGREE_SCOPED | rupture carrier; exact admission |
| M19 | ADAPT | AGREE_SCOPED | process carrier; real lifecycle missing |
| M20 | ADAPT | AGREE_SCOPED | entity/relation binding; no labels |
| M21 | ADAPT | AGREE_SCOPED | route/trace technique; reject conserved substance |
| M22 | ADAPT | AGREE_SCOPED | fallible orientation; no infant adult theology |
| M23 | ADAPT | AGREE_SCOPED | condition/gap history; no 65/68 defaults |
| M24 | ADAPT | AGREE_SCOPED | residue/hysteresis; no universal drain |
| M25 | ADAPT | AGREE_SCOPED | ordering only; not event time |
| **M26** | **REUSE** | **REVISE_PRECISE** | literal derived writes; invariant is reusable, body must be repaired |
| M27 | ADAPT | AGREE_SCOPED | proposal only; no premerge |
| M28 | ADAPT | AGREE_SCOPED | hard admission; no forced fallback |
| **M29** | **REUSE** | **AGREE_SCOPED for immediate `render_year`; REVISE_PRECISE for band** | direct render nonmutating; Pass2 failure/rollback and later prose are not |
| **M30** | **REUSE** | **REVISE_PRECISE** | one-person jurisdiction only; literal V2 has age/parent/narrator issues |
| M31 | REPLACE | AGREE_SCOPED | causal type/parent effects rejected |
| M32 | ADAPT | AGREE_SCOPED | inert carrier; fail closed |
| M33 | REPLACE | AGREE_SCOPED | mechanical event causality rejected |
| M34 | REMOVE | AGREE_SCOPED | fallback fabrication |
| M35 | REMOVE | AGREE_SCOPED | placeholder causal atoms |
| M36 | REMOVE | AGREE_SCOPED | unknown-parent defaults |
| M37 | ADAPT | AGREE_SCOPED with M37 wording correction | annotation metadata only; not memory/scene |
| M38 | ADAPT | AGREE_SCOPED | schedule equality; one registry |
| M39 | REPLACE | AGREE_SCOPED | age-band injection |
| M40 | ADAPT | AGREE_SCOPED | multi-gate readiness |

**Conclusion on the 3-REUSE count:** the count should not be read as three literal unmodified source-function reuses. At literal grain, only M29's immediate `render_year` surface function is directly reusable with a scoped caveat; M26 and M30 are reusable **invariants/jurisdictions** whose old bodies require repair. B's own B03 (`D11`, `D17`, `D23`) states the repairs. The correct disposition vocabulary is `REUSE_INVARIANT` vs `REUSE_BODY`.

---

## 3. D claim adjudication

| # | D claim | Verdict | Independent evidence / correction |
|---|---|---|---|
| D-01 | Current C12→C0 path is layered, not one assembled pipeline; exact cuts | **AGREE_SCOPED** | Key source hashes in D/01 match; effective imports and S52 roots reproduced. |
| D-02 | 116 sourcefree tests passed: S44/45 31, S46/47 34, S48 12, S49/51 26, S52 13 | **AGREE_SCOPED / REPRODUCED** | RB independently ran the same suites: 31 (81.88s), 34 (107.48s), 12 (8.90s), 26 (45.81s), 13 (53.29s) = **116/116**. Counts match; times differ. Test-only, not native. |
| D-03 | C9 `run_candidate_path` separates actor/event/conditioning/CAN008/occurrence/CAN011/E2; `CandidateStore` real transaction | **AGREE_SCOPED** | Source inspection confirms; production Rule A/T registries empty, so this is test-only/targetless. |
| D-04 | S37 targetless C12 product; uses `TEST_ONLY_S37_CAN008_A`; empty target registry; NO_CHANGE/NO_PROPOSAL/zero target rows | **AGREE_SCOPED** | `S37/producer.py:243-267`; `response_rules.py:29`; `target_rules.py:28`. |
| D-05 | S48 one source event/one prospective; `self_account` SCI05_HOLD; candidate_specs `[]`; `SOURCE_OWNER_HOLD`; one-call transport | **AGREE_SCOPED** | `s48/sources.py:17-26`; `s48/session.py:326-349,381-404`; tests 12 passed. |
| D-06 | S49 root B sources `[]`; controlled `PRIOR_B_REFUSAL` test-only; normal S42 guard | **AGREE_SCOPED** | `s49/actor.py:111-139`; tests. |
| D-07 | C0/C11 PRE-MAIN source exists but no S37/S52 import; native weld 0 | **AGREE_SCOPED** | Grep found no S37/S52 import; `s52.bootstrap.roots()` returns S52/S51/S49/G18 only; current progress native C12=0/C11=0. |
| D-08 | C12 store has branch/episode/world_event/perception/checkpoint; no actor-state/functional table | **AGREE_SCOPED** | `bp4/store.py:38-80`; tables only. |
| D-09 | S42 single-event sequential; S46/S47 interval/conditioning; no N11 batch | **AGREE_SCOPED** | `s42/session.py:112`; `s46/producer.py:136`; `s47/session.py:26-33`; tests. |
| D-10 | S52 hardcoded roots and cold-open verifier risk | **AGREE_SCOPED_STATIC_RISK_NOT_REPRODUCED** | `s52/bootstrap.py:5-27` hardcodes `/Users/.../rawlsing-r31j/...`; `s52/session.py:315-317` forces `ok=True` when `_OPENING` and `base_ok`. The 13 S52 tests pass; the risk is a static path not exercised by `base_ok=True` + S52-only error. |
| D-11 | No functional-organization layer; current stores are value/episode/world/checkpoint | **AGREE_SCOPED** | No `ActorStateVersion`/relation table; S37 store tables confirm. |
| D-12 | `T0.1` source registry, `T0.2` actor/event transaction, `T0.3` retrospective packet are the recommended first tranche | **REVISE_PRECISE** | The components are sound, but they must be merged with B's B0/B1/B2/B3 shell and one canonical actor schema. T0.1+T0.2+T0.3 alone under-scope the immediate lawful tranche; see §4. |
| D-13 | `PREFIX_CONTIGUOUS` recommended default; `INDEPENDENT_SUFFIX`/`WHOLE_BATCH_ATOMIC` owner-only | **HOLD / AGREE_AS_RECOMMENDATION** | The external-B irreversibility argument is correct; the policy is not user-adopted. C6/C9/C12 owner must decide. |
| D-14 | `FunctionalRelation` store, no automatic Hebbian; coactivation candidate evidence only | **AGREE_SCOPED as storage; HOLD on formation** | D's design correctly forbids automatic edge creation. No formation/recruitment law is issued; C court/science owner required. |
| D-15 | `T0.4` sparse relation store and `T0.5` batch skeleton can follow T0.1–T0.3 | **AGREE_SCOPED as later tranche; HOLD on relation semantics** | Storage can be built; relation creation/recruitment cannot be a default. Batch skeleton can precede concrete rules if it returns HELD. |
| D-16 | 116 tests are test-only, not native C12/A5 | **AGREE_SCOPED** | Reproduced; no native. |
| D-17 | S48 hardcodes OpenCode CLI/model | **AGREE_SCOPED** | `s48/product.py` `PRODUCT_CLI` default `/Users/.../.opencode/bin/opencode`, `PRODUCT_MODEL=opencode-go/deepseek-v4.1-flash`. |
| D-18 | C9 production Rule A/T empty; targetless NOT a native positive | **AGREE_SCOPED** | Verified; no rule issuance. |

### 3.1 D current path accepted facts

The following D/01–D/04 facts are independently confirmed at source/test grain:

- `S37TargetlessProduct` / `QualifiedC12Store` persist branch, episode, world event, perception and checkpoint; they do not persist a versioned actor state or functional organization.
- `S37` C9 path uses a TEST_ONLY response rule and empty production target registry; `stage_s36` requires `NO_CHANGE`/`NO_PROPOSAL` and zero target rows.
- `S42Session.admit_event` admits one event per call with predecessor/history/source binding and cold reopen; it is not a 3–5 batch.
- `S46Session.produce_interval` and `S47` conditioning provide a bounded workshop material interval and a C9 conditioning readset; not a general care/work/schedule system.
- `S48Session.run_turn` is one-call/one-prospective transport with source-owner and SCI05 holds; it has no retrospective packet or dependency invalidation.
- `S49Session.produce_b_turn` has a normal B adapter but `root_b_sources=[]`; controlled `PRIOR_B_REFUSAL` is test-only.
- `S52Session` is conditional on an independent counterpart; hardcoded roots and `_OPENING` verifier override are real static risks.
- C0/C11 PRE-MAIN modules exist but no S37/S52 import; no C12→C0 path.

These support D's `CURRENT C9-C12 HOLD`, not a native person.

---

## 4. B/D integration conflicts that must be resolved before implementation

### 4.1 One actor state, one ledger, one receipt

B proposes:

- `ActorSnapshotV1` with durable `material/needs/expectations/mediators/tensions/practices/relations/motives/ruptures/processes/access/memory_refs/diagnostics`;
- `CanonicalEventV1` + `EpisodeV1` + `ImpressionV1` + `TransitionReceiptV1`;
- `DerivedViewValue` and `SurfaceRecord`.

D proposes:

- `ActorStateVersion` + `PersonState` with material/needs/practices/expectations/relations/functional organization/memory/access/claims/metadata;
- `CanonicalEventLedger` holding world/access/response/durable/interval/memory/reflective/batch records;
- `DurableDecision` and `CanonicalWorldEvent`.

These are compatible in spirit but not one schema. A future SYN02-S implementation must choose **one** canonical actor snapshot, **one** append-only event/transition ledger and **one** durable-decision/receipt record. Parallel stores would create two actor worlds and a new source of hash/identity conflict. The likely minimal resolution is:

- D's `ActorStateVersion` as the version envelope and pointer set;
- B's `ActorSnapshotV1` as the durable payload (or a merged `PersonState`);
- one canonical event ledger = D's ledger with B's `CanonicalEventV1`/`EpisodeV1`/`ImpressionV1` event shapes;
- one `DurableDecision`/`TransitionReceiptV1` record with exact parent, before/after hash, rule/permission and no-change/held status;
- one `SurfaceRecord`/`DerivedViewValue` boundary.

This is a **HOLD/SYN02-S integration decision**, not a defect in either design alone.

### 4.2 Largest lawful immediate tranche

B proposes B0+B1+B2+B3-shell as the largest lawful immediate tranche; D proposes T0.1+T0.2+T0.3, then T0.4/T0.5. The RB recommendation is to merge, not choose:

1. **B0 + D T0.1** — source/custody baseline and portable `SourceRegistry`/hash resolution. This removes S52/S48 absolute-path/CLI hazards and is purely engineering.
2. **B1 + D T0.2** — one actor schema (`ActorStateVersion` envelope + `ActorSnapshotV1`/`PersonState` payload), pure derived registry, migration reader/archive, actor/event/state transaction, no-ghost rollback. No scientific rule required for the shell.
3. **B2 + D T0.3 + B3 shell/T0.5 skeleton** — canonical event ledger, one-way surface, access-limited retrospective packet, 3–5 batch orchestrator with owner-injected ports, explicit `HELD`/`NO_CHANGE`/`SOURCE_OWNER_HOLD` outcomes. The per-event CAN008/011 calls must return `HELD_MISSING_RULE` if registries are empty; no fabricated transition.
4. **D T0.4** — sparse relation/activation store may be built as **storage only** after schema unification. No formation/recruitment rule, no automatic coactivation, no all-to-all graph. The science/formation law remains HOLD (B5/T1.3).
5. **B4–B7, T1, T2** — HOLD on actual care/world/B/C0/C11/native rules/permissions; B6/T1.4 memory/SCI05 after owner; B7/T2 after native.

This merged tranche is the maximal lawful engineering work that does not invent psychology. It must not claim a C12 person, a learned relation or a native C11 weld.

### 4.3 Batch policy

D's `PREFIX_CONTIGUOUS` is a defensible engineering recommendation because external B/world actions cannot be rolled back. But it is not user-adopted and cannot be silently installed as the product law. The C6/C9/C12 owner must choose among prefix, independent suffix and atomic, with explicit handling of an external B act that occurs after a failed prefix. The retrospective packet must never expose the unseen suffix as if it happened.

### 4.4 Functional relation representation

D's sparse `FunctionalRelation` store and B's optional `FunctionalConnectionRecord` are representation options, not a scientific law. The target must allow:

- a state-value change with no new relation;
- a temporary coactivation with no durable relation;
- a new composite practical procedure;
- a new typed relation under an owner rule;
- external support that changes outcome without internal learning;
- no change.

The current architecture has no functional-organization table. Building a store is lawful engineering; declaring coactivation a cause is not. This remains HOLD for SYN02-C/science and CAN/ADP owners.

---

## 5. Positive, NO_CHANGE/external-support and severed-edge evidence

### 5.1 Executed sourcefree positives

- **SYN02-D 116 tests:** independently reproduced, 116/116. These prove the current test-only S37/S36/S42/S44–S52 paths execute and enforce their stated targetless/controlled boundaries. They do not prove a native person.
- **M29 immediate render:** `render_year` after `compute_all_derived` leaves the backbone hash unchanged; only `rendered_output` changes. This is a real reusable surface invariant.
- **M26 falsifier:** `compute_all_derived` changes `metabolic_style` from `{}` to `{current:compartmentalizing, trend:stabilizing}` and rewrites `registers`; the six-name invariant does not catch them. This falsifies literal M26 reuse.
- **M19/M30 edge:** warm prose with a raw process produced `narration_support.warmth=30` and aperture 55; neutral prose produced 20 and 54; no process produced 50 aperture in both. The immediate render is nonmutating; the later step is causal.

### 5.2 Lawful NO_CHANGE / external-support alternative

- **No process:** warm/neutral prose with no metabolization process leaves psychological capacity unchanged; the narrator signal exists but there is no target. This is a sourcefree no-target boundary, not a native CAN012 `NO_CHANGE`.
- **External support:** a later change may be due to actual co-carer/resource support while the actor's durable organization is unchanged. The architecture must record that as external support, not as internal learning. This is **specification-only**.
- **Missing rule:** an absent CAN008/CAN011 rule must produce `HELD_MISSING_RULE`, not `NO_CHANGE`. D's design says this; B's migration says this. No executed native case.

### 5.3 Severed upstream fault

- **Executed sourcefree:** RX03 monkeypatched `_analyze_narrative_for_support_quality` to constant `(50,50,50)`; warm and neutral both produced aperture 54. The warm/neutral difference disappeared when the exact narrator reader was severed. This is a sourcefree reader fault, not a native E1→E2 semantic consumer.
- **D current path:** S48 source-owner refusal, S49 empty B, S52 conditional and targetless C9 are real severed/held outcomes; none is a native negative.
- **Design-only:** remove the exact earned CAN011 state→later C9 semantic read while holding world/B/E2 fixed; the later semantic difference must disappear or produce a precise missing-conditioner/integrity status. Not run.

---

## 6. Three court verdicts in detail

### 6.1 ENGINEERING — `ACCEPT_SCOPED_WITH_PRECISE_CORRECTIONS`

- B: 59/59 source hashes and 31/31 S50 exact; 40/40 disposition matrix; migration/tranche design; no new tests. Corrections: 3 REUSE semantics, 40/40 focused-test overstatement, M37 wording, B/D schema merge.
- D: current source/call graph and 116 tests; C9 empty production rules; S48 one-call; S49 B empty; S52 static verifier/path risks; C0/C11 unwired. Corrections: 116 tests are test-only, not native; S52 static risk not reproduced; T0 tranche must merge with B; prefix policy owner-held.
- No production or source edit. No full original V3 suite rerun by RB; B's historical source claims rely on reviewed X/RX evidence. No current native C12/A5.

### 6.2 SCIENCE — `HOLD / RULE_UNISSUED`

- B/D are architecture/engineering; no concrete Rule A/T, care/activity rule, functional-relation formation/recruitment, memory/SCI05 admission, or developmental coefficient.
- The functional-organization candidate must not become a universal graph or automatic Hebbian law. Coactivation is candidate evidence only.
- The user-settled 3–5 N/N+1 boundary is represented correctly at architecture grain by D; no native execution.
- The actual C12 person, independent B and A0–A5 are not proved.

### 6.3 AUTHORITY — `NO_NATIVE_GRANT / CURRENT C9-C12 HOLD`

- B/D do not issue source/actor/CAN/ADP/Pyat/C8/C9/C11/C12 grants; they preserve HOLD.
- C0/C11 source exists in PRE-MAIN but is unwired; current progress native C12=0/C11=0/A5 NOT_RUN.
- S49 controlled B, S48 transport, S52 conditional and S37 targetless C9 are test-only; no native transfer.
- No production, no merge, no self-adoption.

---

## 7. FINDING → INTERPRETATION → ACTION → OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| B 59/59 source hashes; 31/31 S50; D 116 tests reproduced | Source/test evidence is credible at historical/test-only grain | Accept scoped; keep native labels separate | RB / SYN02-S |
| B's 3 REUSE includes M26 literal writes and M30 literal V2 issues | `REUSE` conflates literal body with invariant/jurisdiction | Reclassify M26/M30 as `REUSE_INVARIANT`/`ADAPT_BODY`; scope M29 to `render_year` only; preserve B03 repairs | SYN02-B author / SYN02-S |
| B's 40/40 focused-test claim | Source review is 40/40; focused-test coverage is uneven | Restate as selected-source 40/40; list mechanism-specific NOT_RUN tests | SYN02-B author / RB |
| B's M37 server re-render wording | Server per-year render and run_and_print final re-render both exist | Correct wording; do not claim server never renders non-LLM years | SYN02-B author |
| B `ActorSnapshotV1` vs D `ActorStateVersion` | Two candidate actor/ledger schemas could duplicate the person | Choose one canonical snapshot/ledger/receipt in SYN02-S before code | SYN02-S / C9-C12 architecture |
| B B0–B3 vs D T0.1–T0.5 | Overlapping tranche plans; neither alone is the maximal lawful shell | Merge into B0+T0.1, B1+T0.2, B2+T0.3+B3/T0.5; T0.4 storage only; B4–B7/T1/T2 HOLD | SYN02-S / C9-C12 engineering |
| D 116 tests | Real test-only current path; not native | Preserve as engineering receipt; no native claim | C9/C12 engineering |
| D C9 production Rule A/T empty | Current C9 is targetless | Issue/withhold concrete rules with source/scope/positive/NO_CHANGE/rivals | CAN008/CAN011 owners |
| D S48 one-call, S49 B [], S52 hardcoded/verifier | Current target not N11/native B/paid life | Reuse transport/adapter/storage; obtain actual B/source; fix paths/verifier | C9/C12; ADP019/C8/world; S52 engineer |
| D C0/C11 unwired | No C12→C0 world/weld path | Build C0/C11 adapter only under Pyat/source permission | Pyat C11/source custodian; C8/C9 |
| Functional relation store/formation | Representation option, not law | Storage may follow; no automatic coactivation; owner rule or HOLD | Science issuer + CAN/ADP + C12 |
| Prefix vs atomic batch | External B actions irreversible; policy not user-adopted | C6/C9/C12 owner chooses; record truthful prefix; no suffix leakage | C6/C9/C12 |
| Memory/SCI05 | Self-account is pending text; no native admission | Postcall admission/invalidation; no narrator state write | ADP016/017/SCI05/V2 |
| No native C12/C11/A5 | Architecture and sourcefree work only | Keep native gates; no production | C9/C12/Pyat/A0–A5 |

---

## 8. Recommended finite next actions

1. **SYN02-S** must first reconcile B and D into one actor snapshot/ledger/receipt schema and one merged tranche. Do not implement before that.
2. **SYN02-B author** should correct the 3 REUSE semantics, the 40/40 focused-test wording and M37 wording; preserve B03's repairs. These are precise corrections, not a rewrite.
3. **SYN02-D author** should correct the tranche merge, mark S52 cold-open as static/unreproduced, and keep `PREFIX_CONTIGUOUS` as a recommendation with owner decision.
4. **C9/C12 engineering** may then build the merged B0/B1/B2 + D T0.1/T0.2/T0.3 + batch shell on an isolated branch. It must not implement CAN008/CAN011 semantics, actual B/C0/C11 or native C12.
5. **CAN008/CAN011/CAN010/CAN012/ADP/SCI05/Pyat owners** must issue or withhold their finite rules/sources; no reviewer may substitute.
6. **Independent reviewer** after the SYN02-S implementation must reproduce the current 116 tests, the M26/M29 probes, the schema/ledger identity and the batch fault cases.

---

## 9. Limitations

- RB independently reproduced the 116 current sourcefree tests and the M26/M29/M30 historical probes; it did **not** run a native C12/C11/A5, a live provider, raw survey data or the full original V3 suite.
- B's 40/40 selected-source review is accepted at source/reviewer grain, not full-body by RB; B explicitly limits its own body-read claim.
- D's 36 source hash table was key-verified; not every row was rehashed, but the exact imported modules exercised by the 116 tests were inspected.
- S52 cold-open risk is static; no test executed `base_ok=True` plus an S52-only error.
- No empirical psychology, source right, actor grant or production acceptance is created by this review.

### Required future reviewer

A distinct independent I2/I3 reviewer after the immutable return SHA must verify the B/D corrections, the 116-test reproduction, the M26/M29/M30 source boundary and the SYN02-S merged schema. Then a separate SYN02-S integrator and competent owners must decide; this RB return is not self-adopted.

---

## 10. Artifacts and remote verification

**Review artifacts:**

- `SYN02/REVIEW_COURTS/RETURNS/RB/00_REVIEW.md` (this file)
- `SYN02/REVIEW_COURTS/RETURNS/RB/INDEPENDENT_EVIDENCE.json`
- `SYN02/REVIEW_COURTS/RETURNS/RB/LOCAL_PROBES.md`
- `SYN02/REVIEW_COURTS/RETURNS/RB/REMOTE_READBACK.json` (added after push)

**Review startup:** `1ede5e7e814b22e6e652fb01549d4a10f5dec18c`. **Targets:** B `d8f8b4f7610a4a28d86cf6d0c08f5d297d74d6e3`; D `f904955e1c6f4db2d7fdebf8d2a6b78029274a5f`. **Branch:** `agent/sorok-syn02-review-rb-source-runtime-migration-r1`. **Final reviewer commit/readback:** reported in handoff after commit/push; no self-referential SHA is embedded. **NO_SELF_ADOPTION.**
