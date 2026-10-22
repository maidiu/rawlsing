# R31J/R31E evidence comparison and proposed HQ decision docket

**Status:** `PROSPECTIVE_NOT_ADOPTED__NOT_A_COMMISSION__NOT_AN_HQ_VERDICT`
**Read cut:** R31J `64fec28c374d8f77fb0b412d0c934d798ede03e8`; R31E `a2760d3687b063513fe0a5b9589c56c998d4ccb5`; PRE-MAIN `fcbb2ee1d7a6eae040e0964bb8474e8d04d47989`. The worker did **not** independently rerun their tests.

## 1. Actual return identity

| Item | R31J | R31E |
|---|---|---|
| Worker branch | `agent/rabochii-sorok-20261021-r31j-gm01-pre-c9-owner-source-first-person-r1` | `agent/rabochii-sorok-20261021-r31e-actor-expression-binding-first-neighbor-r1` |
| Exact startup | `9a9b8a61daf4bf78e2885436924e5235f26f5772` | `9a9b8a61daf4bf78e2885436924e5235f26f5772` |
| Substantive commit | `b186105367089cfde03c5e6ee6600e42f3c40279` | `cdc0825600cebc99c8acb1f54ea1b0ee0cbae7a8` |
| Final remote head | `64fec28c374d8f77fb0b412d0c934d798ede03e8` | `a2760d3687b063513fe0a5b9589c56c998d4ccb5` |
| Return blob / SHA-256 | `b65f2809...` / `22429ad446fbedaec8f4791bca4976be999001309b0072a5e4732cbf76522fa7` | `5a6f7ac4...` / `189529e54dc491f06c8137afc9595c0d6967dd6fb962bd307296e0a5e0e8e764` |
| Author claims | 202 distinct tests; pre-C9 GM01 source bound in C8; C9 target/NO_CHANGE; E2; cold C12/A0/A2 | 15 new + 10 R30A + 5 R29P; 6 faults; exact expression admission; first-session/refusal/offscreen/return; 60 templates |
| Author-declared limits | owned adapter, no first-class BP2 cutover; no native issuance; no CAN/ADP/C8/C11/C12 | no external model; full 155 NOT_RUN; no human A5; no native CAN/ADP/C8/C11/C12; deterministic template grammar |
| Return status | `RETURNED_AUTHOR_REMOTE_VERIFIED`; local process UNKNOWN | `RETURNED_AUTHOR_REMOTE_VERIFIED`; local process UNKNOWN |

## 2. Finding vs implementation vs strongest rival

### R31J

| Author finding | What the code/receipt actually shows | Strongest rival / limit |
|---|---|---|
| GM01 B source is pre-C8, not a post-C9 overlay | `PreC9Producer.stage_world` sets `self.historical_life`; `stage_c8` commits the C8 payload with `gm01_pre_c9_source`; the C8 digest changes with share/refusal. Code: [stable_actor_binding.py:34–48](https://github.com/maidiu/rawlsing/blob/64fec28c374d8f77fb0b412d0c934d798ede03e8/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/stable_actor_binding.py#L34-L48); [producer.py:550–583](https://github.com/maidiu/rawlsing/blob/64fec28c374d8f77fb0b412d0c934d798ede03e8/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/bp2_joined/producer.py#L550-L583). | This is an **owned adapter**, not a first-class upstream BP2 constructor. The original producer is unchanged. Acceptance must not call it a BP2 cutover. |
| C9 decision changes on B refusal | Refusal C8 `22bc08...`; E1 `739113...`; C9 `NO_CHANGE`/`NO_PROPOSAL`; `RESPONSE_EFFECTS_VALID_EMPTY`/`NO_ELIGIBLE_MATERIAL_SOURCE`; no target. Receipt: [r31j_chain.json](https://github.com/maidiu/rawlsing/blob/64fec28c374d8f77fb0b412d0c934d798ede03e8/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/evidence/r31j_chain.json). | The target is separately authorized TEST_ONLY; GM01 CAN011 remains `NO_CHANGE`. A valid-empty is not proof of a native learned practice. |
| A's own E2 is independent | Share+E2: tools 1→0, completed 4→5, material 4→3, B 4, `OFFSCREEN_NO_CHANGE`; share+omit: tools 1, completed 4, B 5, `OFFSCREEN_REPAIR`. Source: [02_SOURCE_FAULTS](https://github.com/maidiu/rawlsing/blob/64fec28c374d8f77fb0b412d0c934d798ede03e8/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/02_SOURCE_FAULTS.md). | Opportunity is not action, but the action is still a TEST_ONLY fixture. No native ADP019/E2. |
| Cold C12 preserves source/material | Cold reopen shows tools 0, completed 5, material 3, GM01 episode, verifier `ok=true`. | Local SQLite/same-user witness; no protected custody. |
| No psyche or native grant | `psyche_delta={}`, `v3ms_created=0`, `rule_t_result=NO_CHANGE`, `rule_t_grant=None`, native registries 0/0. | This is a scientific/HOLD result, not proof that no psychology exists. |

### R31E

| Author finding | What the code/receipt actually shows | Strongest rival / limit |
|---|---|---|
| Actor contract replaces keyword-only canned lines | `compile_contract` builds actor/material/world/B/knowledge/history/features; `propose` selects strategies/templates; `validate` re-renders and checks facts/knowledge/private tokens; `admit` writes exact event/C12 admission. Code: [expression.py:154–315](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/r31e/expression.py#L154-L315), [451–603](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/r31e/expression.py#L451-L603), [650–838](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/r31e/expression.py#L650-L838). | The template set is still bounded (60), and the “strategy” transducer is feature-gated. It is materially better than a single keyword line but not general NLU or whole-person V2. |
| Same text differs under actual history/material state | 12 contrasts show `EXPLAIN_WORK`/`DEFER_WORK`/`RECALL_WORK`, contact grant/defer/refuse, boundaries, unknown/observed B. [contrasts.json](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/evidence/contrasts.json). | The contrasts are authored and deterministic; they do not prove empirically formed human motive. |
| Exact occurrence before user lens | `admit` writes `SPEECH`/`REPAIR`/`MESSAGE`/`SILENCE` before `_surface`; attention contrast keeps event ids/hashes. | This is a real seam at TEST_ONLY grade; no live renderer/two-call. |
| First-session/cold works | Available 26 episodes/11 world events/20 checkpoints/27 perceptions; pressed 23/10/19/24; cold text preserved. | One workshop/market ecology; B's offscreen life is a source-owned event, not a rich agenda. |
| 6/6 faults | Committed-utterance tamper, recomputed identity, attention-only surface, private boundary, unsupported memory, chronological rewrite. [faults.json](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/evidence/faults.json). | C12 local-custody residual; same-user witness; trailing-row deletion not protected. |

## 3. Tests: what can and cannot be added

- R31J receipts sum to **202** (8+8+29+2+9+7+10+33+50+15+21+2+8). They are distributed across R31J, R30G, R29M, R29P, R27P, R26V, R26E/BP2P4J/N1. This is not one 202-test joined suite.
- R31E reports **30 executed** (15 new + 10 R30A + 5 R29P), with **5 of the R29P tests exactly shared** with R31J's 9-test R29P receipt. Thus the receipts imply at most **227 distinct test identities** if no other name collision exists (202 + 15 + 10). Do not present 232 as a clean union.
- **R31E full inherited 155: NOT_RUN.** **R31J/R31E joint consumer: NOT_RUN.** **No independent rerun by this worker.**
- R31J's 202 tests are author-executed at declared suites; R31E's 30 are author-executed. Neither is independent acceptance. The fact that both are green does not prove their join.

## 4. Prospective four-column HQ intake

**Not adopted. For a future incoming HQ to accept, revise, or reject.**

| FINDING | INTERPRETATION + ALTERNATIVES | PROPOSED HQ ACTION | ACCOUNTABLE OWNER |
|---|---|---|---|
| R31J physically binds GM01 B source inside C8, creates a source-dependent C9 target or `NO_CHANGE`, and reaches C12 A0/A2 at TEST_ONLY grade. | H2 material mediation is supported within the simulator. Alternative: an owned adapter is enough for sourcefree evidence but not an upstream BP2 cutover. | `ENGINEERING ACCEPT_SCOPED` for the adapter and sourcefree product; request a first-class BP2 GM01 envelope from the BP2 owner. Do not call it native. | R31J engineering + BP2 semantic owner + Sorok HQ intake |
| R31E binds exact actor-conditioned expression before the user lens, with boundary/privacy/fault/cold behavior. | It is a real expressive admission seam, not whole-person V2. Alternative: a future authorized external renderer can propose richer prose through the same port. | `ENGINEERING ACCEPT_SCOPED` for the deterministic baseline; `REVISE` any claim of general NLU, live model, or human fidelity. | R31E engineering + V2/renderer owner + Sorok HQ intake |
| The two returns are separate and do not consume each other. | A unified first encounter is a missing **adapter/consumer**, not a third worker's isolated green test. Alternative: run R31E only on R29P and never touch R31J; that fails the intended source-governed expression join. | Propose one joined consumer test (below); do not auto-launch. | New join owner + R31J/R31E owners + Sorok HQ |
| Canonical Sorok rev29 still says R31J/R31E sealed. | This is a stale board, not a contradiction of the returns. | Correct the next current progress pair only after lawful intake; do not rewrite rev29 history. | Sorok HQ / progress owner |

**Proposed three-court verdicts**

| Court | R31J | R31E | Basis |
|---|---|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_ADAPTER_AND_SOURCEFREE_PRODUCT` | `ACCEPT_SCOPED_DETERMINISTIC_EXPRESSION_AND_FIRST_SESSION` | Real code, tests, cold/fault receipts at declared scope. Not independently rerun by R32H. |
| **SCIENTIFIC** | `TEST_ONLY_MATERIAL_FEASIBILITY__H0_LIVE__NO_ACQUIRED_PRACTICE` | `TEST_ONLY_SITUATED_EXPRESSION__NO_HUMAN_PSYCHOGENESIS` | Both are sourcefree; no native empirical rule, no human validation. |
| **AUTHORITY** | `HOLD` | `HOLD` | No CAN008/CAN011/ADP/C8/Pyat/C11/native C12. |

## 5. Strongest alternative and RED

**RED — currentness:** Sorok rev29 labels both branches “PHYSICALLY SEALED EXACT BRANCH” at startup `9a9b8a...`; the actual branches returned at `64fec...` and `a2760...`. An incoming HQ that repeats rev29 as the worker ledger is factually stale. This is a documentary RED, not a retroactive revocation of either worker.

**RED — false unification:** R31J target `59ff0a4e59f57bfb3ba132657fe3f9a62eb90abd764f74a62eec1f15045e7278`; R31E target `8f1614f592ffb2075401ffd4b249bd6e7f5b41d752dec028a3448df63d4c5dbb`. Different C12 roots. R31E's [08_R31J_EXPRESSION_PORT](https://github.com/maidiu/rawlsing/blob/a2760d3687b063513fe0a5b9589c56c998d4ccb5/WORKER_RETURNS/SOROK-20261021-R31E-ACTOR-EXPRESSION-FIRST-NEIGHBOR-R1/08_R31J_EXPRESSION_PORT.md) explicitly says “does not import unreturned sibling code.” A claim that two greens equal one executed first encounter is **not supported**.

**Alternative:** the first lawful next positive could be a **join adapter test**, not a new CAN/ADP commission and not a generic review. The adapter must not fake native authority. If the join cannot be made without changing an owner's semantics, return a typed owner-hook HOLD instead of a post-hoc overlay.

## 6. Proposed largest lawful future joined consumer

**Name:** `R31JE_FIRST_ENCOUNTER_P01` (proposal only).
**Purpose:** one user-facing first encounter over the same C12/M6 root that R31J produced, with R31E's admission port compiling from that root.

**Minimum chain:**

```text
R31J GM01 pre-C9 source -> C8 -> E1 -> TEST_ONLY CAN008 RULE_A
  -> separate TEST_ONLY CAN011 RULE_T/target -> later E2
  -> C12/M6 -> R31E compile_contract -> propose/validate/admit
  -> exact actor speech/action -> user SAY/DO/ATTEND -> same C12
  -> cold reopen
```

**Required acceptance evidence**

1. **Positive:** the same named assertion (`JOINED_P01`) passes on the same C12 root. The actor's expression strategy is derived from the R31J C10/C12 state, not from R29P's separate target.
2. **Source-edge RED:** cut the B GM01 source or the C9 target; the **same** `JOINED_P01` assertion must fail, and restore must pass. The failure must not be a constructor/import crash that never reaches the assertion.
3. **Attention contrast:** focused vs distracted user surface may differ; admitted event ids/hashes must be identical.
4. **Cold:** reopen the same SQLite DB, preserve exact admitted text and target/material state.
5. **Privacy:** no actor cash/debt/free-hours/source/history hashes in the user surface.
6. **Honest limits:** `LIVE_ACTOR_MODEL_NOT_RUN` unless separately authorized; `NATIVE_C12=False`; `HUMAN_A5=NOT_RUN`; 60-template baseline remains.

**Not authorized by this proposal:** any new worker launch, native grant, CAN/ADP issuance, C11 weld, Pyat N11/N12, or production deployment. It is a test design for a future HQ to commission only after 00E/00C and duplicate-worker checks.

## 7. Other workstreams that remain independent

| Workstream | Current state | Next lawful owner action |
|---|---|---|
| CAN008 concrete RULE_A | `REQUEST_EVIDENCE`; no native rule | Competent CAN008 issuer: one bounded person×event rule with receivability/appraisal/currentness/revocation. |
| CAN011 RULE_T/grant | `NO_CHANGE`; grant none | Separate CAN011 owner: concrete durable target or explicit no-change; no GM01 transfer. |
| ADP actor/event | ADP007/010/015/019 native absent | ADP owners: actual actor initialization, encounter, genealogy, event admission. |
| C8 trust | D1/D2/D3 held; test key only | C8 custodian: all-process writer cutover, independent protected key/monotonic anchor, real event admission. |
| C12 custody | SQLite test verifier; same-user | C12 custodian: protected production trust, external witness, deletion/rollback resistance. |
| Pyat N11/N12 | `NOT_READY`/`HOLD`; R56 narrow code unpause | Pyat HQ only; Sorok must not dispatch or reinterpret. |
| C11 native weld | 0 | Separate competent C11 act after Pyat/Sorok grants. |
| Human A5 | `NOT_RUN` | Authorized human study; no claim from sourcefree tests. |

## 8. What this docket does not do

It does not mark either worker accepted, does not mark any 15-gate category PASS, does not revise Sorok law, does not mutate a worker branch, and does not launch a new commission. It prepares a prospective intake and one finite join test for an incoming HQ.
