# SOROK S35 — sourcefree actor-access bridge into the pinned C9R consumer

**RESULT:** `S35_TEST_ONLY_ACTOR_ACCESS_BRIDGE_IMPLEMENTED__M35_EXACT_B_E1_SOURCE_VALIDATION_REUSED__PINNED_C9R_CONSUMER_REUSED__POSITIVE_AND_SAME_WORLD_SEVERANCE_PASS__ZERO_TARGET_PROPOSALS__CAN011_NO_CHANGE_NO_PROPOSAL__COLD_READBACK_PASS__NATIVE_HOLD`.

This is one isolated TEST_ONLY engineering bridge. It is not a native CAN008/CAN011 rule, not an issued target grant, not ADP/C8/C12 authority, not acquired-practice science and not a new engine. It writes only inside `WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/**`.

## 1. Identity, base and read-only inputs

- Repository: private `maidiu/rawlsing`.
- Base commit: `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`.
- Branch: `codex/sorok-s35-c9r-access-r1`.
- Exclusive worktree: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`.
- Role: one bounded sourcefree implementation engineer; not HQ, original CAN/ADP/science issuer, protected C8/C11/C12/native owner, or independent reviewer.
- Host: macOS, Python 3.11.3, pytest 9.1.1, SQLite local. No Codex, no subagent, no external provider/browser/model call.
- `.s35-sources/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1` is a read-only staged input. It is not staged in this commit.

Pinned sources actually used:

| Source | Cut | Role |
|---|---|---|
| M35 `firstclass.py` | `4170fbf19a9d5a64bc728f5b22156bbffcec51e5` | exact B/E1 source projection and preimage validation |
| R31J staged cut | `64fec28c374d8f77fb0b412d0c934d798ede03e8` | BP1/BP2/BP4 native-free sourcefree closure |
| C9R consumer | `6fa2939972ce5a2c0cc4f2b033946b276f1c2934` | exact response/target/pipeline/conditioning consumer |
| JOIN-E history | `7bf2da302996491ddf34b9a039fea47ac982d135` | inherited targetless C12/E history only |

Pinned C9R blobs verified at install:

```text
candidate/response_rules.py  a5c30af336116863e2e6805299b772c89a2ad841
candidate/target_rules.py    c33fc2a6a58efd422cb5289c080205b9e0183102
candidate/pipeline.py        cb0350909dedd9f7159dce145ba216b211a8185c
candidate/conditioning.py    3a5c83ae35bb4d8ca26f40e00ca1fe10868deb23
```

The C9R files are used from the pinned staged cut. `candidate.pipeline.evaluate_response` is replaced in-process by the S35 selector adapter; the pinned pipeline source itself is not edited. The selector is bypassed when no S35 context is present, so the legacy path remains the pinned one.

## 2. What was implemented

- `install.py` resolves only the M35 return, the staged R31J cut and the pinned C9R/native/BP4 closures. It verifies exact SHA-256 for M35 `firstclass.py`, the four pinned C9R blobs and the native zero-positive guard before import. Missing inputs fail as a named dependency, not as fabricated authority.
- `bridge/access.py` is the source-neutral S35 selector over the pinned C9R `ResponseResult` contract. It seals actor-local access and actor-owned timely immediate-response witnesses, binds both to the exact actor, event id/hash, C12 root, C12 branch and clock frame, and always returns `target_proposals=()`.
- `bridge/world.py` reuses M35 `firstclass.validate_source`, the M35 BP2 producer C8/OUT9 stages, the pinned C9R `run_candidate_path`, and a TEST_ONLY BP4 C12 root/branch. One world is created once; positive, access-severed, request-severed and restored evaluations use that same C8/E1/root/branch/clock context.
- `bridge/readback.py` reopens the committed C9 SQLite rows read-only and the C12 root/branch, validates sealed response/receipt rows, the exact S35 receipt, zero target rows, and the C12 episode binding after close.
- `tests/test_s35_access_bridge.py` executes 32 focused tests: exact M35 source validation, P1, access severance/restoration, request severance/restoration, contradictory valid-empty and unbound refusal, foreign root/branch/actor/event/clock/hash/revocation refusals with no commit, REFUSE_TOOL, label invariance, history non-practice, shared public refusal surface, empty production registries, and cold reopen.

The bridge accepts only TEST_ONLY source witnesses. A foreign root, branch, actor, event, clock, source namespace, source hash, response kind or revoked source is a typed refusal before any C9 row is created. Objective material eligibility is recorded separately and never creates uptake.

## 3. Exact execution evidence

Commands actually run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tests \
  --junitxml=WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/evidence/s35_full.xml
# 32 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tools/capture_evidence.py
# vectors=10, foreign access refusals=13, foreign response refusals=11,
# cold_all_ok=true, fault trials access PASS/RED/PASS and request PASS/RED/PASS
```

Evidence files:

- `evidence/test_run.txt` — exact pytest transcript.
- `evidence/s35_full.xml` — JUnit, 32 tests, 0 failures/errors/skips.
- `evidence/s35_evidence.json` — vectors, same-world bindings, fault trials, foreign refusals, cold readback, source manifest and file hashes.

### P1 positive

B `SHARE_TOOL` from the actual M35 source produces the same C8/E1 world used by every fault:

```text
source B event hash (M35 share)  16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486
C8 state digest                  e472d9f9331cd827e70902232419eb0cc8dc590c9503e2f3040501eec84bb6fb
E1 event                         TEST_ONLY_BP2_E1_OCC-0001
E1 hash                          5e7f4b43a8a1e61daa6e263ef228a3f904c4948e67e060dac8f986db42ec1a69
C12 root / branch                root / s35
root branch hash                 602e191a79c713d4dd3ec7ba93caf7d7b6ee7db0fb17e2b673b23ca40abb0dc6
root state hash                  406a019d868884a1797c44e59b3bf9a2bb3547afc0b46fe0695e3938ef78573d
branch hash                      2f7016268ff5ed9a73075ed0c25c0d5bd5ac072a2356f68980633ae266f35523
branch fork / frame clock        242 / 244
actor                             TEST_ONLY_BP1_R26V_ACTOR_A
access source                    TEST_ONLY_ADP017_ACCESS_S35_SHARE_TOOL
response source                  TEST_ONLY_A_RESPONSE_S35_SHARE_TOOL_REQUEST_TOOL
response kind                    REQUEST_TOOL
S35 outcome                      OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
S35 receipt hash                 007381d8f856b41946d0d6dcaace0c689559eed0367a175c61af70819d36aea2
C9 response row hash             68e4ea8295138c5014ef5fda8a99e9ea076388fc0331656c87be7a38607ecbea
C9 commit receipt hash           b38905c18b4206112f5c9d250349ff846e4d15acddb569c5ff71a55fc08f523d
CAN011                           NO_CHANGE / NO_PROPOSAL, target id ""
target rows                      0
objective material eligible      true
objective material ref           TEST_ONLY_BP2_MATERIAL_A
objective implies uptake         false
```

The C9 response row status is `RESPONSE_COMMITTED`; the C9 receipt row is `NO_CHANGE` / `NO_PROPOSAL` with `target_state` and `target_journal` empty. Cold reopen of the same rows and the C12 episode passed.

### Same-world severance table

| Run | Witness change | S35 outcome | C9 status | CAN011 | Target rows | Receipt |
|---|---|---|---|---|---|---|
| `p1` | none | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 | `007381d8…` |
| `access-fault` | only ADP017 access removed | `UNKNOWN_RECEIVABILITY` | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 | `ee3d374b…` |
| `access-restored` | access restored | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 | `007381d8…` |
| `request-fault` | only A-owned request removed | `RECEIVABLE_NO_OBSERVED_UPTAKE` | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 | `9d04c25e…` |
| `request-restored` | request restored | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 | `007381d8…` |
| `contradictory` | access only, no response, bound contradictory project | `AMBIGUOUS_CONTRADICTORY` | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 | `a5d5776e…` |

Access fault kept the objective material result `eligible=true`; the positive response disappeared anyway. The request fault kept access `ACCESSIBLE`; the positive response disappeared anyway. This is the direct separation of objective availability, actor access and actor-owned performed response.

Fault trials on the same assertion:

```text
access witness gate     PASS -> RED -> PASS
response witness gate   PASS -> RED -> PASS
```

### REFUSE_TOOL and public surface

| Run | B source | A response kind | S35 outcome | CAN011 | Target rows |
|---|---|---|---|---|---|
| `refuse` | M35 `REFUSE_TOOL` | `EXPLICIT_REFUSAL` | `OBSERVED_CURRENT_REFUSAL` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `share-explicit-refusal` | M35 `SHARE_TOOL` | `EXPLICIT_REFUSAL` | `OBSERVED_CURRENT_REFUSAL` | `NO_CHANGE/NO_PROPOSAL` | 0 |

Refusal objective material is `false`; the public refusal surface is reachable from both B histories without inferring B's private motive. No B operation or motive is present in the S35 receipt.

### Foreign-root/refusal and cold readback

All 13 access mutations and 11 response mutations refused before any C9 database was created:

```text
ACCESS_BINDING_MISMATCH:root_id / root_branch_hash / root_state_hash /
branch_id / branch_hash / branch_parent_id / branch_fork_clock / clock /
actor_id / event_ref / event_id
ACCESS_SOURCE_NAMESPACE_INVALID
ACCESS_REVOKED
RESPONSE_BINDING_MISMATCH:root_id / root_branch_hash / branch_id / branch_hash /
clock / actor_id / event_ref / event_id
RESPONSE_KIND_INVALID
RESPONSE_NOT_PERFORMED
RESPONSE_REVOKED
```

A separately resealed source-hash mismatch also refused `ACCESS_SOURCE_HASH_MISMATCH` with no C9 commit. Cold verification passed for every refused run (no C9 database, `committed=false`, zero target rows) and for the positive/fault/restored/contradictory/refusal runs.

### Label and history non-effects

- Changing only `social_role` and `demographic_label` left `firstclass.case_preimage` and `firstclass.source_from_case` byte-identical. A separately built altered-label world still produced `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` with zero target proposals and zero target rows.
- Adding two independent TEST_ONLY enacted history refs to the same C9 call produced the same S35 receipt hash as the no-history baseline, zero target proposals and zero target rows. No learned-practice presumption exists.

### Source/custody hashes

```text
install.py                         8e194dcf2de4049bf074c5457800db65d4193b34e8e89a763ef0231c377fb5dd
bridge/access.py                   c88a23f4e94f08f6ea1029b802470fd9b6672eaf408cee14a03fe1c2c454e053
bridge/world.py                    614803037c48a68d1818d5940e56b0bf50a8667ddbb43f20ee5f76657956711a
bridge/readback.py                 ccddffb00665f176e42f28962710d31f5f4ec194f5499b2e2efcad55d4c8bb6e
tests/test_s35_access_bridge.py    1ac961ff32a6f863d5ca314d45e6e02cad2705059424cb9e119a7c25d58862e8
tools/capture_evidence.py          b38470ac62e881f87e5c32c897b677429e2241a2ab7a9bc54dfe3446effb2f19
evidence/test_run.txt              18f7c9663a7309c2a93c7abf22a9f6fa18b80bc2c59ff78388ec10bfedac310b
evidence/s35_full.xml              156719fc2f298345db74cfb9512f0a3d5d59f7d6efc8bde406d44e42e67ff680

M35 firstclass                     acfdc42daec3e701e017664caef370780db47c72ed1bc85fcc26999f8a38a3db
C9R response_rules                 aa8d978f43bd14a11430371e68e2ce4e2ebf1adb385ee52230a4c23a16c49dfc
C9R target_rules                   e5d38865d2a4d50a904a387b2a8770bda55567dcef670e97c0dd696c8f7475a5
C9R pipeline                       b5da655ca03cdc9dc6dad11b88dfadd22101836cffc7993f530e6148ded0695c
C9R conditioning                   edc3a5690c4ed281a41b877119af63397b6348c54a407276eee020005b849887
C9R native guard                   12b2c49f664662cbfe993fc4817751ed9edfff3ce89c44cac489a00cb5e42177
```

## 4. Findings, interpretation and owner

| FINDING | INTERPRETATION AND RIVAL | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **F1 — M35 exact B/E1 validation is reusable before C8.** `firstclass.validate_source` rejects wrong owner/event/hash/quantity/clock/E1 fields with `MATERIAL_SOURCE_PREIMAGE_MISMATCH` before the producer root exists. | Rival: a valid-looking stand-alone witness envelope could be forged against a fixed case. The source-preimage tests reject that rival. | Accept scoped sourcefree engineering. | M35 engineering + BP2 source owner |
| **F2 — Actor access and actor-owned timely response are now actual selector inputs, not inferred from material eligibility.** Removing only access yields `UNKNOWN_RECEIVABILITY` with material still eligible; removing only request yields `RECEIVABLE_NO_OBSERVED_UPTAKE` with access still `ACCESSIBLE`. | Rival: the C9R legacy `evaluate_response` already represents S35 because the output shape fits. The selector is needed because the legacy fields have no access/reception argument and can emit declared uptake plus a practice proposal; this bridge emits zero proposals. | Keep the adapter isolated; do not treat it as a native registry. | S35 engineering + C9R consumer owner |
| **F3 — Root, branch and clock binding is actual.** Access and response witnesses carry the exact C12 root branch hash, root state hash, branch hash, parent, fork clock and frame clock; foreign root/branch/clock/actor/event refusals occur before C9 commit. | Rival: binding only actor and event is enough. The foreign-root/foreign-branch evidence falsifies that for this bridge. | Preserve the binding on the same consumer. | S35 engineering + C12 lineage owner |
| **F4 — Objective availability and uptake are separate.** Share world with eligible material remains `UNKNOWN_RECEIVABILITY` when access is severed; REFUSE_TOOL has material `false` and still produces the observed current refusal when A's own refusal is witnessed. | Rival: objective tool availability or B's operation determines A's speech. The REFUSE/SHARE public-refusal pair shows the same observed refusal surface from different B causes with no B motive in the receipt. | Do not infer psychology, gratitude, liking or learned practice. | S35 science owner + CAN008 issuer |
| **F5 — Targetless commit is real.** The pinned C9R `evaluate_target(proposal=None)` returns `NO_CHANGE/NO_PROPOSAL`; the C9 target tables remain empty and cold reopen confirms no ghost target. | Rival: a missing-target crash or shape-only output could be mistaken for the negative. The named C9 response and receipt assertions and zero target rows are the behavioral evidence. | Preserve; native CAN011 remains unissued. | C9/CAN011 owner + C12 consumer owner |

## 5. Courts and disposition

| Court | Grade |
|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_SOURCEFREE_ACTOR_ACCESS_BRIDGE__PINNED_C9R_CONSUMER__32_OF_32_TESTS__ZERO_TARGETS__COLD_READBACK` — author evidence only, not independent adoption. |
| **SCIENTIFIC** | `TEST_ONLY_WITNESSED_CURRENT_ORIENTATION_ONLY__NO_ACQUIRED_PRACTICE__NO_HUMAN_MEASURE__H0_LIVE` — no hidden emotion, motive, belief, durable practice or cross-context transfer is inferred. |
| **AUTHORITY** | `HOLD` — no native CAN008/CAN011 rule, no grant, no ADP017/ADP019 owner receipt, no C8 native custody, no C11/C12 native consumer, no Pyat N11/N12, no human A5. |

**DONE:** exact M35 B/E1 source validation reused; pinned C9R consumer reused; actor/event/root/branch/clock-bound access and response witnesses; positive P1; same-world access severance RED/restoration; same-world request severance RED/restoration; contradictory valid-empty; foreign-root/branch/actor/event/clock/revocation refusals with no commit; REFUSE_TOOL targetless consumer; cold C9/C12 readback; zero target proposals; empty production registries.

**REMAINING:** independent reverify of this exact cut; native CAN008/CAN011 issuer and grant; ADP017/ADP019 owner receipts; native C8/C11/C12 custody; H1 empirical acquisition study; human A5.

**CRITICAL BLOCKER:** no native actor-access owner receipt and no issued CAN008/CAN011 authority. Neither is fabricated here.

**LARGEST MOVE:** one proportionate independent review of this exact sourcefree bridge cut while all native/owner lanes stay held.

**FLIGHT:** sourcefree local only; no external provider, native lane, production or human subject.

## 6. Limits / NOT_RUN

- Only this return's 32 focused tests and the evidence generator were run. No 444-file corpus rebuild, no M35/DEV-R/JOIN-E/staged-input edits.
- The C9R consumer is the pinned code; only its in-process `evaluate_response` name is pointed at the S35 selector. `candidate.pipeline.py` bytes are unchanged and hash-verified.
- All witnesses, C8/E1/C12 records, response receipts and target decisions are TEST_ONLY sourcefree. A sealed TEST_ONLY source proves local integrity, not issuer authenticity.
- No native CAN008/CAN011, ADP017/ADP019, C8/C11/C12, Pyat N11/N12, original source rights, human A5, production activation or external model/browser call.
- No claim that B's act is perceived by A, that objective material implies uptake, that REFUSE_TOOL implies a private motive, or that one or two witnessed acts create durable practice.
- H1 acquired practice and defeating H0 remain NOT_RUN/HOLD; no positive practice assertion exists to sever.

## 7. PROGRAMMA_DELTA

`PROGRAMMA_DELTA:` S35 now has an executed TEST_ONLY sourcefree actor-access bridge that reuses M35's exact B/E1 validation and the pinned C9R consumer, binds A access and A's own timely performed request to the same actor/event/C12 root/branch/clock, survives same-world access and request severance RED/restoration and cold readback, and commits `NO_CHANGE/NO_PROPOSAL` with zero target proposals while all native authority remains unissued.

## 8. Publication

The exact commit SHA and ordinary-push readback are recorded after publication in `PUBLICATION_RECEIPT.json` and the final worker handback.
