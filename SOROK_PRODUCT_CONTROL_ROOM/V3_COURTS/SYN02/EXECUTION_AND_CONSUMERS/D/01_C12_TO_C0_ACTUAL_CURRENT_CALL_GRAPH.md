# SYN02-D / 01 — current C12→C0 source and call-path map

**Status:** `SOURCE_INSPECTED / EFFECTIVE IMPORT TRACED / NOT NATIVE / CURRENT C12-C11-C0 EDGES INCOMPLETE`.
**Author:** SYN02-D independent I3 current-system investigator; not HQ, original issuer, production editor or reviewer.
**Sealed startup:** `cd1f4fd8158c2771d7c565b06ee397a7a60dc779`.
**Current source cuts inspected:** PRE-MAIN `integration/pre-main-reconciliation-r1` at `c5e0e5755b68acecae7964f349abecfb15c569fd`; S37 `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`; S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`; S39 `e41513fa65601a37e7b3b430d26c626ae0217d90`; S40 `79b0357c7af9b66ad8a28f5b77b46b0348094a23`; S41 `c72a10d284f8869b990db3e6849ed174a51bd784`; S42 `2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91`; S43 `3edd631fb6c31751dfd2143ba2faa9fc31561e54`; S44 `923278fbe6b030e2ffdd10fe42d7a18266344611`; S45 `f26a138e20d53c809d611cf8d834ec647b0804bf`; S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`; S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`; S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`; S49 `6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43`; S51 `2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65`; S52 `c821b488b3a9a3f0fa01b1981989cc17af637dc1`; JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`; M35 `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`.
**Claim grade:** direct static source/import inspection plus 116 sourcefree tests. No current native C11/C12/A5 execution, source grant, provider call, survey data or production edit.

---

## 0. Executive finding

The current Sorok source is **not one assembled C0→C12 runtime**. It is a layered set of test-only child classes and vendored predecessors:

```text
A0/A5 user surface (S45 SAY/DO/HELP/ATTEND, test only)
  -> C12 product / user session (S37TargetlessProduct; S44/S45/S46/S47/S48/S49/S51/S52)
  -> C10 coupled product (S37 product, S48 one-call envelope)
  -> C9 E1/Rule A/Rule T/NO_CHANGE/E2 (S36 pipeline; S37 stage_s36)
  -> C8 keyed occurrence/world writer (BP2/BP3/BP4; C12Store)
  -> C4 sampled antecedent root (S44; BP1/G18; not full genealogy)
  -> C0 Pyat possibility/empirical world (pre553 modules; no import into S37/S52)
  -> C11 native/Route-B projection (pre553 C11 facade; no native C12 weld)
```

The **only currently effective end-to-end path** is TEST_ONLY sourcefree S37/S42/S44/S45 source: it can create a sampled root, C8/C9 targetless response, C12 episodes, user encounters and interval condition receipts. It cannot currently produce a native C12 person, a concrete CAN008 Rule A, a concrete CAN011 Rule T, an independently sourced B positive, or a C11 weld. C0/possibility and C11 projection code exists in PRE-MAIN, but no inspected S37/S44/S52 module imports it.

---

## 1. Layer-by-layer current map

| Layer | Current source/object | Exact public entry | Actual consumer | Observed status | Evidence / restriction |
|---|---|---|---|---|---|
| **A0–A5** | `S45Session.say/do_help/attend`; `S44Session` user path; `BP4Product` user actions | `say(text)`, `do_help()`, `attend()` | Test consumer, C12 world/C9, language writer | `PARTIAL / TEST_ONLY` | S45 tests say/do/attend; no human A5, no native participant |
| **C12** | `S37TargetlessProduct` over `QualifiedC12Store`; C12 episodes/world/checkpoint/perception | `S37IntegratedSession.start/open`, `_append_episode`, `_checkpoint`, `_world` | S44/S45/S46/S47/S48/S49/S51/S52 sessions | `PARTIAL / TEST_ONLY`; targetless, no native C12 | `S37/product.py:39`; `C12Store` `store.py:38`; `QualifiedC12Store` `c12_integrity.py:28` |
| **C10** | `S37TargetlessProduct`; `S48Session.run_turn` one-call product | `S37IntegratedSession.start`, `S48Session.run_turn` | S45 user product; S48 product envelope | `PARTIAL / TEST_ONLY`; one-call, no batch | `S37/session.py:39`; `S48/session.py:202` |
| **C9** | `candidate.pipeline.run_candidate_path`; `S37 IntegratedProducer.stage_s36` | `run_candidate_path(...)`, `stage_s36()` | C12 binding; S37 product | `IMPLEMENTED_UNWIRED / TEST_ONLY`; production Rule A/T registries empty; targetless NO_CHANGE | `candidate/pipeline.py:120`; `S37/producer.py:243`; `target_rules.py:110`; `response_rules.py:123` |
| **C8** | `bp2_joined.JoinedProducer.stage_world/stage_c8/stage_out9`; BP3 keyed journal; BP4 `C12Store.world_event/perception` | `stage_world`, `stage_c8`, `stage_out9`; `record_perception` | S37 C9 E1; S42 event consumer; S49 B | `PARTIAL / TEST_ONLY`; no protected D1/D2/D3 custodian | `bp2_joined/producer.py:550-590`; `store.py:160-238` |
| **C4** | `S44` `generate_root` / `SampledRoot`; BP1 `TwoActorLife`; G18 joint | `S44Session.start`; `generate_root(bundle)` | S43/S42/S37 C12 | `PARTIAL / TEST_ONLY`; sampled antecedent, not full genealogy | `S44/session.py:43`; `S44/root.py:96` |
| **C0** | PRE-MAIN `source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility`, `pre553_empirical_possibility_provider`, `pre553_source_local_universe_admission` | `evaluate_positioned_subject_possibility(query, rule, evidence)`; `provide_empirical_possibility_slice(...)` | Pyat/pre-V3 analytical consumer; **no S37/S52 consumer found** | `IMPLEMENTED_UNWIRED / PARTIAL` | `PRE-MAIN/rawlsing_next/source_backed_positioned_subject_possibility.py:417`; `pre553_empirical_possibility_provider.py:531` |
| **C11** | PRE-MAIN `pre553_source_backed_c11_facade`, `pre553_c11_repository`, `pre553_route_b_production`, `pre553_physical_c11_bridge` | `build_validated_source_backed_c11_release`, `execute_route_b_production`, `C11Repository` | Pyat C11/Route-B analytical consumers; **no current C12 consumer** | `IMPLEMENTED_UNWIRED / PARTIAL / NATIVE HOLD` | `pre553_source_backed_c11_facade.py:587,642,656`; `pre553_route_b_production.py:494`; current progress C11=0 |
| **C1/C3/C7** | Generic CAN008 R2 adoption; `response_rules.py`/`target_rules.py` registries | `ResponseRuleRegistry.production()` empty; `TargetRuleRegistry.production()` empty | C9 pipeline | `PARTIAL / RULE UNISSUED` | RC `ddea756…`; `response_rules.py:29`; `target_rules.py:28` |
| **C2/C5/C6** | No current durable functional-organization or full N/N+1 implementation | — | — | `MISSING` | S42 is sequential single events; S48 one call; no functional relation registry |
| **ADP016/017/019/020/SCI05** | Test witnesses/ports only; S44 ADP020 RNG; S48 SCI05 hold | `make_actor_local_access_witness`, `ADP019EventPort`, `S48Session.run_turn` | C9/S48 | `PARTIAL / TEST_ONLY`; no native memory/access/admission | `candidate/actor_access_response.py`; `bp2_joined/ports.py:260`; `S48/session.py:326-349` |
| **V2/expression** | S40 language registry, S43 historical repertoire, S45 help language; old V2 not on current path | `perform_generated_attempt`, `compile_historical_plan`, `S45Session.say` | A0 user surface | `TEST_ONLY`; finite phrases, no native competence/translation | S40/S43/S45 source; no human A5 |

**Important:** C12 here is the `S37TargetlessProduct` C12, not a native pipeline-produced person. Its C12 grade is `TEST_ONLY_SOURCEFREE_TARGETLESS_C12_NOT_NATIVE`; C11 native weld and C12 native person are zero in the current progress record.

---

## 2. Actual effective import graph

The following was verified by source inspection and by executing `s52.bootstrap.roots()` (no provider/state mutation):

```text
s52.bootstrap
  -> s51.bootstrap -> s49.bootstrap -> s48.bootstrap -> s47.bootstrap
  -> s46.bootstrap -> s45.bootstrap -> s44.bootstrap -> s43.bootstrap
  -> s42.bootstrap -> s41.bootstrap -> s40.bootstrap -> s39.bootstrap
  -> s37.bootstrap -> S36/M35/JOIN-E/language roots
```

`s52.bootstrap.roots()` returned:

- `s52_return` and `s51_return`/`s49_return` under the S52 author tree;
- `g18_source` hardcoded to `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18`
- cuts `s51=2a4cdd2…`, `s49=6604f2d…`.

The S52 bootstrap file (`s52/bootstrap.py:5-27`) is **not portable**: the G18 path is an absolute Mac path. S48 product (`s48/product.py:15-37`) also hardcodes an OpenCode CLI and provider/model:

```text
PRODUCT_CLI = /Users/matthewsmith/.opencode/bin/opencode
PRODUCT_MODEL = opencode-go/deepseek-v4.1-flash
PRODUCT_VARIANT = max
```

These are test/authority configuration choices, not production deployment contracts. A runtime architecture must replace them with an injected `ProductTransport`/source registry; otherwise a different host cannot reproduce the same effective import graph.

---

## 3. Actual call path from a user-visible encounter back to C12/C9

### 3.1 S45 encounter path

`S45Session` subclasses `S44Session`; `say`, `do_help`, `attend` route to accepted R31E semantic/action interfaces and the actual C12 world/session (`s45/session.py:37-120`). The path is:

```text
user SAY / DO_HELP / ATTEND
 -> S45 source/access/language plan
 -> BP4 C12 world/event writer
 -> C12 episode/checkpoint
 -> S42 event-keyed reader / C9 result
```

`S45` does not create a second actor history or a new C9 rule. It is a **test-only user adapter** over the S44 root and S42/S43 events.

### 3.2 S44 root path

```text
S44Session.start
 -> generate_root(default/declared bundle)                    # s44/session.py:43-65
    -> explicit S44 RNG (ADP-020-style HMAC)                  # s44/rng.py
    -> BP1 TwoActorLife / build_actor_history / ledgers       # s44/root.py:96-215
    -> G18 material joint opportunity + performed witness
 -> S43/S42/S40/S39 accepted start
 -> S44_ROOT_BINDING C12 episode + checkpoint
```

The root is an **explicit sampled antecedent**, with initial material/cash/hours/birth and conditional B-refusal/A-decline draws. It is not a historically generated genealogy, childhood, family history or actual source person. Its own receipt says `selected_finished_life=false`, `psychology_claim=false`, `native=false` (`s44/session.py:176-221`).

### 3.3 S37 producer and C9 path

`S37IntegratedSession.start` (`s37/session.py:39-154`) runs:

```text
IntegratedProducer(root, case, source, variant)
 -> stage_m35()                                             # producer.py:110
    -> stage_world()       # BP1 TwoActorLife / world occurrence
    -> stage_c8()          # BP3 keyed exclusive append
    -> stage_out9()        # OUT9 read + proof verifier
    -> _bind_e1()          # ADP019 test-only E1 + event
 -> stage_s36()                                             # producer.py:243
    -> evaluate_s36()
       -> candidate.pipeline.run_candidate_path(...)         # pipeline.py:120
          -> ingress_actor / ingress_event
          -> bind_conditioning / material eligibility
          -> CAN008 response-rule lookup
          -> occurrence admission (CandidateStore)
          -> CAN011 target evaluation
          -> atomic target/occurrence commit
          -> later E2 read
       -> requires response status RESPONSE_COMMITTED
       -> requires target NO_CHANGE / NO_PROPOSAL / zero target rows
 -> S37TargetlessProduct C12 store + S37 episode/checkpoint
```

Current production registries are empty:

- `ResponseRuleRegistry.production()` has `rules=DEFAULT_ISSUED_RESPONSE_RULES`, which is an empty `MappingProxyType({})` (`response_rules.py:29,123-130`).
- `TargetRuleRegistry.production()` is likewise empty (`target_rules.py:28,110-117`).

S37 compensates with a **TEST_ONLY** response rule (`TEST_ONLY_S37_CAN008_A`) and the empty production target registry, which forces the observed response into `NO_CHANGE/NO_PROPOSAL`. This is an engineering targetless path, not a rule-issued developmental transition. `S37/producer.py:243-267` explicitly enforces zero target proposals/rows.

### 3.4 C8/C12 path

`stage_c8` uses BP3's keyed journal; `stage_out9` reads a committed occurrence under the proof verifier. The C12 product (`S37TargetlessProduct`) opens `QualifiedC12Store` and persists:

- `branch` (root/branch identity, actor IDs, fork clock);
- `episode` (C12 action/response/language/interval/encounter records);
- `world_event` (objective world events);
- `perception` (which actor observed which event);
- `checkpoint` (world state snapshots).

The C12 store is append-only at SQLite trigger level; `QualifiedC12Store.verify` checks row preimages and contiguous sequence. Its external checkpoint witness is TEST_ONLY and same-user; it is **not** a protected production KMS (`c12_integrity.py:83-139`).

### 3.5 S42 and later-event path

`S42Session.admit_event` (`s42/session.py:112-330`) adds a later event:

```text
admit_event(case, source, history_event_refs, source_records, rule, event_time)
 -> validate predecessor chain
 -> validate history refs / source C8/C9/access
 -> build C8 occurrence from current C12 world + predecessor
 -> S39/S40 generate/selection and S43/S40 language
 -> source-bound performer; denied attempt -> no action/C9
 -> normal S42/S37 C9 consumer
 -> append event-keyed binding + C12 checkpoint
```

It supports repeated events and cold reopen. It does **not** implement a batch, first-half retrospective, or 3–5 conditional proposals. It is one event per call. The S42 `_extra_conditioning_sources` hook (`s42/session.py:79-81`) is the current seam used by S47 to inject an interval condition.

### 3.6 S46/S47 interval path

`S46Session.produce_interval` (`s46/session.py:30-31`) calls `produce_interval` (`s46/producer.py:136`) to emit:

- domain issuance;
- actor attempt receipt (`ATTEMPT`, `CONSTRAINED_ATTEMPT`, `DECLINED`, `NOT_ATTEMPTED`, `BLOCKED`, `UNKNOWN`);
- world-period receipt (actual action/event or `NOT_PERFORMED`);
- `S46_INTERVAL_STATE` C12 episode with coverage/gaps/currentness/supersession.

`S47Session._extra_conditioning_sources` (`s47/session.py:26`) injects `current_interval_source` into the S37 C9 `conditioning` readset; `read_c9_conditioning` (`s47/session.py:33`) returns the event-bound interval source. This is a real material-conditioner path, not a new response rule or a learned practice. It is scoped to the current workshop domain.

### 3.7 S48 one-call path

`S48Session.run_turn` (`s48/session.py:202-450`):

```text
current source event
 -> build_payload / build_prompt
 -> one product CLI call (or injected runner)
 -> parse envelope {narrative, self_account, prospective[]}
 -> reject world mutation
 -> if self_account_present: SCI05_HOLD, no C8
 -> if no allowed source: SOURCE_OWNER_HOLD, no C8
 -> if len(prospective) != 1: UNRESOLVED / NO_PROSPECTIVE_PROPOSAL
 -> if one allowed candidate and source owner exists: admit one S42 event
```

Current `candidate_specs()` returns `[]`; `issue_current_source()` raises `SOURCE_OWNER_HOLD` (`s48/sources.py:17-26`). Thus the current ordinary path is a **one-call transport/refusal**, not an event batch. It also has no first-half retrospective packet and no SCI05 postcall dependency invalidation; `self_account` immediately becomes `SCI05_HOLD`.

### 3.8 S49 independent B path

`S49Session.produce_b_turn` (`s49/session.py:173-260`) uses:

- `root_b_sources()` -> `[]` (`s49/actor.py:111-117`);
- `controlled_b_sources()` -> one synthetic `PRIOR_B_REFUSAL` (`s49/actor.py:120-139`);
- accepted S39 `FULL_RULE`, B access, performer and normal S42 source adapter (`EXPLICIT_REFUSAL -> REFUSE_TOOL`).

The actual root path is `B_CONTEXT_HOLD`/`S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT`; controlled B is test-only. The source has a real independent-B performer and normal-C8 adapter, but **no actual current B source** in the inspected root. This is a content/source gap, not a missing interface.

### 3.9 S51/S52 object and paid-activity path

`S51Session` adds object relevance over the S49 person: `consume_generation` (`s51/session.py:426`) computes a relevance relation from canonical C12 state, but the paid finishing-equipment relation remains `OPEN_CHOICE_SET`; no option-specific rule. `S52Session` adds `compile_candidate` (`s52/session.py:137-224`) and `perform_paid_participation` (`s52/session.py:247`) for a conditional paid candidate. The normal path is `CONDITIONAL_ON_INDEPENDENT_PARTICIPATION`; no independent counterpart is observed. `S52Session.verify` has a static cold-open acceptance risk: `_OPENING` plus `base_ok` forces `ok=True` at `s52/session.py:315-317` even while errors are retained. This must not be used as a readiness proof.

---

## 4. Current C0/C11 source is real but disconnected

PRE-MAIN contains substantive source-backed Pyat stacks:

- `source_backed_positioned_subject_possibility.py`: `PositionedSubjectPossibilityQuery`, `PositionedSubjectPossibilityModelRule`, `PossibilitySliceEvidence`, `evaluate_positioned_subject_possibility`; epistemic states `EXACT_SUPPORTED`, `EXACT_UNRESOLVED_PROXY_AVAILABLE`, `UNRESOLVED`, `VALID_EMPTY`, `NONCOMPARABLE`, `FAIL_CLOSED`; explicit ceiling `PROXY != EXACT FACT != ACTOR BELIEF`.
- `pre553_empirical_possibility_provider.py`: `provide_empirical_possibility_slice`, exact determinants, no precomputed geometry.
- `pre553_source_local_universe_admission.py`: source-local universe admission; refuses population/generalization uses without separate authority.
- `pre553_source_backed_c11_facade.py`: physical cells -> validated C11 release/query; no inferred source meaning.
- `pre553_route_b_production.py`: Route-B execution compositor over already-governed C11/I03; no actor/V3 state.
- `pre553_c11_repository.py`: logical C11 repository.
- `pre553_learned_world_composition.py`: PFF/learned-world composition with exact contracts; no actor state.
- `sdtf_r4_world_response_redrive.py`: external occurrence/world-response admission and invalidation/rederivation request seam; explicitly does not admit events or author world responses.

No inspected S37/S44/S48/S52 module imports any `pre553_*` or `source_backed_positioned_subject_possibility` module. `grep` over the S39–S52 author sources found no such import; `S52.bootstrap.roots()` names S52/S51/S49/G18 only. Therefore:

- C0 and C11 exist as **current PRE-MAIN resources** at their own source/tests grade;
- they do **not** currently feed C4/C8/C9/C12;
- a C12→C0 real data path is not established by this source tree.

This is `IMPLEMENTED_UNWIRED / PARTIAL`, not global code absence and not a native grant.

---

## 5. What is current versus what is author/test-only

| Object | Current status | Why |
|---|---|---|
| S37 targetless C12 product | TEST_ONLY, current on S37 branch | `S37TargetlessProduct`; product grade; no native C12 |
| S44 sampled root | TEST_ONLY, current on S44 branch | explicit synthetic bundle, no actual genealogy |
| S45 user encounter | TEST_ONLY, current on S45 | finite help language; no human A5 |
| S46 interval | TEST_ONLY, current on S46 | bounded workshop domain; actual material attempt but no general care schedule |
| S47 C9 conditioning | TEST_ONLY, current on S47 | interval material readset; no learned practice |
| S48 one-call | TEST_ONLY, current on S48 | empty source specs; one prospective candidate check; SCI05 hold |
| S49 B | TEST_ONLY/controlled | actual root B source `[]`; controlled refusal only |
| S51 relevance | TEST_ONLY/partial | object relevance; paid relation `OPEN` |
| S52 paid activity | TEST_ONLY/conditional | independent counterpart not observed; cold-open verifier risk |
| S50 historical V3 projection | separate fixture | not current C12; read-only historical adapter (RC) |
| PRE-MAIN C0/C11 | implemented resource, unwired to C12 | no import path; native C11=0 |

---

## 6. Specific current source defects that constrain the architecture

1. **C9 production registries are empty.** `ResponseRuleRegistry.production()` and `TargetRuleRegistry.production()` have no issued rules; S37's targetless path uses a TEST_ONLY response rule and empty target registry. A real C9 semantic read requires concrete owner-issued rules.
2. **C12 is targetless and lacks an actor-state table.** `C12Store` stores branch/episode/world/perception/checkpoint, not a versioned `ActorState` or functional organization. Actor state is embedded in world/checkpoint/episode bodies.
3. **S48 is one-call/one-prospective and has no retrospective first half.** `S48Session.run_turn` rejects more than one prospective and returns `SCI05_HOLD`; no `RetrospectivePacket`, no `DependencyInvalidator`.
4. **Actual B source is absent.** `S49.root_b_sources()` returns `[]`; controlled B uses `PRIOR_B_REFUSAL`; S42 default predicates (`repair_urgent=True`, `avoid_debt=True`) remain a caller-injected model premise.
5. **C0/C11 are disconnected.** PRE-MAIN C0/C11 modules are not imported by S37/S52; no actor/world bridge.
6. **Current bootstraps are non-portable.** S52 hardcodes `/Users/.../rawlsing-r31j`; S48 hardcodes the OpenCode binary/model; this prevents deterministic multi-host assembly.
7. **No dynamic functional organization.** The current code has value/scalar state, event history, language repertoire and relevance candidates, but no versioned sparse `FunctionalRelation` store or recruitment trace.
8. **S52 cold-open verifier risk.** `S52Session.verify` sets `ok=True` when `_OPENING` and base is OK, even if its own accumulated S52 errors are present. This is a readiness/observer defect, not a native positive.

---

## 7. Actual source identity table

Selected hashes (SHA-256 unless noted); source branches at the cuts above.

| Source | Hash / identity |
|---|---|
| `WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1/s37/producer.py` | `cbc1a9531caf73b2c70c5ca4e6767b7f2c9e87f3756278555f27dfaee815c42d` |
| `.../s37/session.py` | `3e8ffe0325cd441b2fc05586e6a9cb3676982ea809d4c2fbd288524cf253fb37` |
| `.../s37/product.py` | `4d49453848a7f7e60ad0f2c724ccf5d36d4eb068ae4f7d0cde70a2e1af6993fc` |
| `.../s37/reader.py` | `1da9ea459734b6489a68bdcfba8d10bf889bc76dff5fc84fec22356b29fe4c67` |
| `S36.../candidate/pipeline.py` | `ba8577ae77ed9f3ec291da91caebae1b2a809edb970d22f29db1173747ce05b6` |
| `S36.../candidate/transaction.py` | `d8d5d36ff68a1fa254c829ffa07a8d19699533769791a6d49b0cdfdd23baa803` |
| `S36.../candidate/target_rules.py` | `e5d38865d2a4d50a904a387b2a8770bda55567dcef670e97c0dd696c8f7475a5` |
| `S36.../candidate/response_rules.py` | `a1067e97b7309c543029406035e2233dcefb38d571ca198d38f17d86b024889c` |
| `S36.../candidate/actor_access_response.py` | `987352a620e944e88b8d5112b1b5c37d6dcc7f523076b9683d5cab6526f2d04a` |
| `S36.../candidate/conditioning.py` | `edc3a5690c4ed281a41b877119af63397b6348c54a407276eee020005b849887` |
| `S42.../s42/session.py` | `4772a1a10b37dd494610f8f650a3271097e052957f3e2257a997ee3f1db6be0a` |
| `S42.../s42/reader.py` | `d8548d7317f63aa6e999e867626c509d9b0b99599479bba5ba4212f0440c867b` |
| `S42.../s42/event.py` | `b33389a298f828610d04e45bde08fc1a8577a23275b4475cb8e5749cb68589ce` |
| `S44.../s44/session.py` | `eccc8d6a420d1715ebb972407505397d930e898ce4ecec9ec7ca64beaaf75259` |
| `S44.../s44/root.py` | `a52dbe79b848f02714ccedb176529a58e5bf5365fdc5edde1aa4e044a7a53226` |
| `S44.../s44/bundle.py` | `82e433cbbcc23eb51664c1189ab0c4f7e6126d5bb458eb1879ef1dad80917af8` |
| `S44.../s44/rng.py` | `d4c858890f90c31cd50915fb673e27fc9aa932015a2670393eb0fc053f483468` |
| `S45.../s45/session.py` | `fad26a91d4368d8de665b815bc174678bca97ece6a5a78cc131a5ef6e6db7ab9` |
| `S46.../s46/session.py` | `d8b51e5700666dbda9122c1ec89984df112abd4930247a9c7f1eff5baece95cf` |
| `S46.../s46/producer.py` | `6e8fdc28a9171d9f9287dd49b86c9aa4e5de6745d24906c6e376baf6551454c2` |
| `S47.../s47/session.py` | `467e91a1f4488ab47d46212473d228ddcd93444b78f007501e4f4a123c915d39` |
| `S47.../s47/conditioning.py` | `97e78287422307b9c7ab1736c2b1ba9b688b115c8ebaa3cf1fcab5a33b15803a` |
| `S48.../s48/session.py` | `8fc4e3f3c8f32a99174e06c28e1e7bfe046746a73fb7fdf6b57a57b985c450cb` |
| `S48.../s48/sources.py` | `c29fffb9e2b9a08f24900d8c196197315414bcf424fa8d70d28fb11cdf48d670` |
| `S48.../s48/product.py` | `dcb7a26f7012b83d2b1bc1259830a0c32a10ca3eb03a1d53983546a5a343a71b` |
| `S49.../s49/session.py` | `9932029c529a399ffedb24545ea5d0f6884a5fe8719ffc39c8af9fe1db0f3625` |
| `S49.../s49/actor.py` | `c2a889c825807c174cdc91ce4ec08cde07c2e6e0575fadf9ee97185324c5eb95` |
| `S51.../s51/session.py` | `6ef8e92eb3ea2d83cfdb5aba1121ed42f1706a0df9bc3f36aff2b91a47596a82` |
| `S52.../s52/session.py` | `3ed6dadf2c809a0f6e2d4094c41e34be3e51b4a984a219898e20f6a7b299e32e` |
| PRE-MAIN `rawlsing_next/source_backed_positioned_subject_possibility.py` | `9c041cb134a7b9198d12f75a1eb82a7e37cdb781adf5f68033b5ad21e62dbc01` |
| PRE-MAIN `rawlsing_next/pre553_source_backed_c11_facade.py` | `03b88d258d21c403542756db7316923aa392871442d99294de904b1744da1d01` |
| PRE-MAIN `rawlsing_next/pre553_c11_repository.py` | `84a71fe43307cca30f9eeaaedb269d8390468a4744a0fac251aebc2cda7b498e` |
| PRE-MAIN `rawlsing_next/pre553_route_b_production.py` | `3a677b4d7a9083ce627f9c773d8a1697f949deebc550bc8f072cff011589f18b` |
| PRE-MAIN `rawlsing_next/pre553_source_local_universe_admission.py` | `377b4d767da0c7cac5caa97bfff60febc6c525220c41a1638f2ace13f7d58cdd` |
| PRE-MAIN `rawlsing_next/pre553_learned_world_composition.py` | `bde80b1fa2936c3bd9d18fa73ece913da1561cfd707692cc46e83004f42c4fc2` |
| PRE-MAIN `rawlsing_next/sdtf_r4_world_response_redrive.py` | `63f3dd0f2471c8d2067f83d786049bc84ca2c07e845ca4d001d0df4a58950d58` |

C12 store source path: `rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j/candidate/vendor/bp4/bp4/store.py` at JOIN-E `7bf2da30…`; `C12Store` begins line 38, `append_episode` line 160, `record_perception` line 203, `checkpoint` line 224, `latest_state` line 270. `QualifiedC12Store` is at `.../vendor/j/r26e/c12_integrity.py:28`.

---

## 8. Findings at the actual current-source grain

1. **C12/S37 is a real test machine, not the target whole-person runtime.** It is a targetless C12 product with a genuine C9 transaction path and a C12 episode/world store, but no native rule and no full actor-state or functional-organization table.
2. **C9 is the strongest reusable component.** `run_candidate_path` already separates actor ingress, event ingress, conditioning, CAN008 lookup, occurrence/target transaction and later E2; it needs concrete rules, a real B/source and a durable actor-state extension, not a rewrite.
3. **C8/C4 are test-only.** BP2/BP3/BP4 writers and the S44 sampled root exist; protected C8 custody and actual genealogy are absent.
4. **S42 is a real sequential-event seam, but not the N/N+1 batch.** It supports repeated single events, source/history binding, event-keyed reads and cold reopen; it does not supply 3–5 proposals, intervening activity or retrospective memory.
5. **S48 is transport only.** It has one call and one prospective slot; it is not N11. Its `candidate_specs=[]` and `SOURCE_OWNER_HOLD` are honest source boundaries.
6. **S49 has the right B adapter but no actual B source.** Controlled `PRIOR_B_REFUSAL` must not be represented as actual life.
7. **C0/C11 exist but are disconnected.** Pyat C11/Route-B and possibility modules are source-real in PRE-MAIN; no current C12 consumer imports them.
8. **No functional-organization layer exists.** Current S43/S47/S51/S52 carry repertoire, interval conditioning, relevance and paid candidate data, but not a versioned set of recruited/inhibited operations or relation edges.

---

## 9. What this map licenses and does not license

**Licenses for architecture work:** reuse S37/S36 C9 transaction and C12 episode store; reuse S42 event sequencing; reuse S44/S45/S46/S47 sources as test-only actor/world adapters; reuse S49 B adapter behind an owner source; reuse pre553 C0/C11 interfaces as unwired services; add new versioned actor/functional-organization/event-ledger APIs.

**Does not license:** calling the current S37 C12 a native person; using `TEST_ONLY_S37_CAN008_A` as a developmental rule; using controlled B as actual B; using S48 as N11; using S52 as independent paid life; importing C11 without source/Pyat permission; or treating a sourcefree test as empirical psychology.
