# SOROK S35 — sourcefree actor-access bridge into the pinned C9R consumer

**RESULT:** `S35_REVISE_REPAIRED__A_LOCAL_PERCEPTION_AND_A_OWNED_ACTION_RECEIPTS_EXPLICIT__NO_B_OPERATION_DEFAULT__TYPED_HOLDS_FOR_UNAVAILABLE_ACTUAL_A_INPUT__CONTROLLED_EVIDENCE_SEPARATELY_GRADED__CONSUMER_INPUTS_VALIDATED__PUBLIC_RECEIPT_PRIVACY__51_OF_51_TESTS__ZERO_TARGET_PROPOSALS__NATIVE_HOLD`.

This is one isolated TEST_ONLY engineering bridge. It is not a native CAN008/CAN011 rule, not an issued target grant, not ADP/C8/C12 authority, not acquired-practice science and not a new engine. It writes only inside `WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/**`.

## 1. Identity, base and read-only inputs

- Repository: private `maidiu/rawlsing`.
- Base commit: `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`.
- Branch: `codex/sorok-s35-c9r-access-r1`.
- Exclusive worktree: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`.
- Repair scope: only the S35 REVISE findings at prior evidence commit `e1cea3f03555dd96d5b78dd0d8833e993e87ae5a`; no unrelated changes.
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

Pinned C9R blob identities and install-verified SHA-256:

```text
candidate/response_rules.py  a5c30af336116863e2e6805299b772c89a2ad841
  sha256 aa8d978f43bd14a11430371e68e2ce4e2ebf1adb385ee52230a4c23a16c49dfc
candidate/target_rules.py    c33fc2a6a58efd422cb5289c080205b9e0183102
  sha256 e5d38865d2a4d50a904a387b2a8770bda55567dcef670e97c0dd696c8f7475a5
candidate/pipeline.py        cb0350909dedd9f7159dce145ba216b211a8185c
  sha256 b5da655ca03cdc9dc6dad11b88dfadd22101836cffc7993f530e6148ded0695c
candidate/conditioning.py    3a5c83ae35bb4d8ca26f40e00ca1fe10868deb23
  sha256 edc3a5690c4ed281a41b877119af63397b6348c54a407276eee020005b849887
M35 firstclass.py            acfdc42daec3e701e017664caef370780db47c72ed1bc85fcc26999f8a38a3db
native zero-positive guard   12b2c49f664662cbfe993fc4817751ed9edfff3ce89c44cac489a00cb5e42177
```

The C9R files are used from the pinned staged cut. `candidate.pipeline.evaluate_response` is replaced in-process by the S35 selector adapter; the pinned pipeline source itself is not edited. The selector is bypassed when no S35 context is present, so the legacy path remains the pinned one.

## 2. Repair of the scoped REVISE findings

### 2.1 Explicit A-local perception and A-owned action receipts

- `bridge/access.py` now accepts two sealed TEST_ONLY receipts, not inferred witnesses:
  - `S35_A_LOCAL_PERCEPTION_RECEIPT@1`: `perception_ref`, A actor, exact E1 event id/hash, C12 root/branch/clock binding, `perceived_at`, `access_status`, owner, grade and revocation.
  - `S35_A_OWNED_ACTION_OCCURRENCE@1`: `action_ref`, A actor, exact E1 event id/hash, C12 root/branch/clock binding, `action_kind`, explicit `performed`, `action_time`, owner, grade and revocation.
- Neither receipt is generated from B's operation. The bridge does not use `SHARE_TOOL`/`REFUSE_TOOL` to choose access status, action kind or `performed`.
- Missing actual A input is a typed hold:
  - no perception receipt -> `A_LOCAL_PERCEPTION_HOLD` / `ACTUAL_A_LOCAL_PERCEPTION_UNAVAILABLE`;
  - access receipt present but no action receipt -> `A_OWNED_ACTION_HOLD` / `ACTUAL_A_OWNED_ACTION_UNAVAILABLE`.
- A `QUALIFIED_ACTUAL_A_INPUT` claim without an owner resolver is also a typed hold; a resolver rejection is `A_LOCAL_PERCEPTION_UNVERIFIED` or `A_OWNED_ACTION_UNVERIFIED`.
- Explicit controlled evidence is accepted only as `evidence_grade=TEST_ONLY_CONTROLLED_FIXTURE`, `actual_actor_input=false`, `qualification=CONTROLLED_ENGINEERING_EVIDENCE_NOT_ACTUAL_A_INPUT`. The positive P1 is controlled evidence, not actual A input.

### 2.2 Public-value privacy

- The S35 receipt no longer contains B's operation in any key or value. Public source refs are A-local/A-owned names only.
- The C12 episode and run summary were sanitized to carry `source_binding` (`b_actor`, `b_owner`, `b_event_ref`, `b_event_hash`, `b_to_actor`, `b_clock`) and no `b_operation` value.
- `public_privacy_error` recursively scans S35 receipts, run manifests and C12 episode bodies for `SHARE_TOOL`/`REFUSE_TOOL`; the evidence generator and cold replay both assert this.
- The only later source difference retained in C12 is the opaque B event ref/hash, not B's private operation.

### 2.3 Actual consumer argument validation

`pipeline_selector` now compares the actual consumer call against the preflight causal readset before returning the prepared response:

- `rule_lookup` status/id/version/content hash/authority/issuer/grade/reason;
- `event_ref`, `subject`, `event_time`;
- `conditioning_readset`, `material_eligible`, `eligible_material_refs`;
- `actor_history_refs`, `other_person_offer_ref`, `material_opportunity_ref`;
- `prior_response_count`.

Any mismatch raises `S35_CONSUMER_INPUT_MISMATCH:<field>` and the prepared response is not used. With no S35 context, the selector delegates to the pinned `evaluate_response`; the legacy delegation is executed and compared in evidence.

### 2.4 Causal cuts, forgeries and cold replay

- Same-world perception cut: controlled `NOT_WITNESSED` -> `UNKNOWN_RECEIVABILITY`; restore `ACCESSIBLE` -> positive.
- Same-world action cut: missing A action receipt -> `A_OWNED_ACTION_HOLD`; explicit `NO_OBSERVED_ACTION` -> `RECEIVABLE_NO_OBSERVED_UPTAKE`; restore performed `REQUEST_TOOL` -> positive.
- Forged A receipts: wrong actor/event/root/branch/clock, invalid status/kind, missing ref, foreign owner, broken seal/source hash, revocation, controlled-grade actual-claim and native claim all refuse before any C9 database is created.
- Consumer-argument negatives: all nine mutated inputs reject with `S35_CONSUMER_INPUT_MISMATCH:<field>`.
- Cold replay: C9 response/receipt rows, zero target tables, C12 root/branch/clock and the S35 receipt episode all revalidate after close.

## 3. Exact execution evidence

Commands actually run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tests \
  --junitxml=WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/evidence/s35_full.xml
# 51 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tools/capture_evidence.py
# vectors=12, foreign perception refusals=19, foreign action refusals=16,
# cold_all_ok=true, consumer_all_negative=true, legacy delegation all equal,
# fault trials perception PASS/RED/PASS and action PASS/RED/PASS
```

Evidence files:

- `evidence/test_run.txt` — exact pytest transcript.
- `evidence/s35_full.xml` — JUnit, 51 tests, 0 failures/errors/skips.
- `evidence/s35_evidence.json` — vectors, same-world bindings, fault trials, foreign/forged refusals, consumer binding, public privacy, cold replay, source manifest and file hashes.

### P1 controlled positive

```text
B source event hash (M35 share)  16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486
C8 state digest                  e472d9f9331cd827e70902232419eb0cc8dc590c9503e2f3040501eec84bb6fb
E1 event                         TEST_ONLY_BP2_E1_OCC-0001
E1 hash                          442c6222dd8fbd7202707cea6767f4bbeae0c56a426c66d60a7bb4e2974dcf48
C12 root / branch                root / s35
root branch hash                 602e191a79c713d4dd3ec7ba93caf7d7b6ee7db0fb17e2b673b23ca40abb0dc6
root state hash                  406a019d868884a1797c44e59b3bf9a2bb3547afc0b46fe0695e3938ef78573d
branch hash                      2f7016268ff5ed9a73075ed0c25c0d5bd5ac072a2356f68980633ae266f35523
branch fork / frame clock        242 / 244
actor                            TEST_ONLY_BP1_R26V_ACTOR_A
perception ref / hash            TEST_ONLY_A_PERCEPTION_P1 / 21d96f0b2c99f060bfbe433cae821ea2a845b71fc5ead5d77dc6121aae281681
action ref / hash                TEST_ONLY_A_ACTION_P1 / a48372518b36176b1b5cc0353b71108372db806f3dfa23cbdb8e8f46e3c5d313
action kind / performed          REQUEST_TOOL / true (explicit controlled receipt)
evidence grade                   TEST_ONLY_CONTROLLED_FIXTURE
actual actor input               false
qualification                    CONTROLLED_ENGINEERING_EVIDENCE_NOT_ACTUAL_A_INPUT
S35 outcome                      OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
S35 receipt hash                 bc8c24f00b615d34bf309a1385f998d1e04b7159d072ac7f6aea141c821fcf17
C9 response row hash             586095c0d7757e5ad6218cfa6fa47d65ad21b3fa4ab1e51dcf49173071e1348b
C9 commit receipt hash           142847d46ddfe0d9b0f4eb524008dfebd664a2634158f87b1003d0d601801f67
CAN011                           NO_CHANGE / NO_PROPOSAL, target id ""
target rows                      0
objective material eligible      true
objective material ref           TEST_ONLY_BP2_MATERIAL_A
objective implies uptake         false
```

### Typed holds and same-world severance

| Run | Input state | S35 outcome | Grade | C9 status | CAN011 | Target rows |
|---|---|---|---|---|---|---|
| `p1` | controlled ACCESSIBLE + performed REQUEST_TOOL | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | controlled | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `actual-a-hold` | no actual A receipts | `A_LOCAL_PERCEPTION_HOLD` | unavailable | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `access-fault` | controlled `NOT_WITNESSED` + action | `UNKNOWN_RECEIVABILITY` | controlled | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `access-restored` | controlled ACCESSIBLE + action | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | controlled | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `action-missing` | controlled ACCESSIBLE + no action | `A_OWNED_ACTION_HOLD` | unavailable | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `action-not-performed` | controlled ACCESSIBLE + `NO_OBSERVED_ACTION` | `RECEIVABLE_NO_OBSERVED_UPTAKE` | controlled | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `action-restored` | controlled ACCESSIBLE + performed action | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | controlled | `RESPONSE_COMMITTED` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `contradictory` | controlled ACCESSIBLE + bound contradictory project | `AMBIGUOUS_CONTRADICTORY` | controlled | `RESPONSE_EFFECTS_VALID_EMPTY` | `NO_CHANGE/NO_PROPOSAL` | 0 |

Access fault kept objective material `eligible=true`; the positive response disappeared anyway. The action fault kept access `ACCESSIBLE`; the positive response disappeared anyway. Fault trials on the same assertion:

```text
a-local perception gate  PASS -> RED -> PASS
a-owned action gate      PASS -> RED -> PASS
```

### REFUSE_TOOL and public surface

| Run | B source | A action kind | S35 outcome | CAN011 | Target rows |
|---|---|---|---|---|---|
| `refuse` | M35 `REFUSE_TOOL` | `EXPLICIT_REFUSAL` | `OBSERVED_CURRENT_REFUSAL` | `NO_CHANGE/NO_PROPOSAL` | 0 |
| `share-explicit-refusal` | M35 `SHARE_TOOL` | `EXPLICIT_REFUSAL` | `OBSERVED_CURRENT_REFUSAL` | `NO_CHANGE/NO_PROPOSAL` | 0 |

The public S35 receipt has no B operation in any value. B's operation is retained only in the internal M35 world input; C12 carries the opaque B event ref/hash and no `b_operation`.

### Forged/foreign refusals and consumer negatives

- 19 perception mutations and 16 action mutations refuse before any C9 database exists: root/branch/actor/event/clock binding, owner, status/kind, time, revocation, grade, actual-claim, native-claim and broken seal/source hash.
- Qualified actual-grade input without an owner resolver is a typed hold; resolver rejection is `A_LOCAL_PERCEPTION_UNVERIFIED`.
- All nine consumer-argument mutations reject with `S35_CONSUMER_INPUT_MISMATCH:<field>`: rule_lookup, event_time, conditioning_readset, material_eligible, eligible_material_refs, actor_history_refs, other_person_offer_ref, material_opportunity_ref, prior_response_count.
- Legacy no-context delegation is exercised: `candidate.pipeline.evaluate_response` matches `candidate.evaluate_response` on status, reason, proposals, receipt hash and route.

### Public privacy and cold replay

- `public_value_privacy` is true for all share vectors, the refuse vector, all run manifests and all C12 episodes.
- Cold replay is green for positive, holds, access/action faults, restoration, contradictory, history, refusal, qualified hold/refusal and source-hash mismatch runs.
- The C9 `target_state` and `target_journal` tables are empty in every committed run.

### Source/custody hashes

```text
install.py                         8e194dcf2de4049bf074c5457800db65d4193b34e8e89a763ef0231c377fb5dd
bridge/access.py                   1040ae13cb5942bdf54cb2e62fda30cfb84bf4e1a35debb277df42fa9b37ab77
bridge/world.py                    0a13fae99239fbe57783752972c11a51e5867fdd50c5ab4192b62028f312a63f
bridge/readback.py                 81d12609c1ada8058a24d3d0eafc9b98d71bd766305808a5832650f9387e4719
tests/test_s35_access_bridge.py    a808dd34ff24173a312cb014e19f1e6a817c748c36c019617a28f427c8498296
tools/capture_evidence.py          8eeca8645cf06ae9e1bbade507a82c8cf4457a602b2aac41d989d10530318825
evidence/test_run.txt              99fee59f52769f019fce9631a3326579bac4c7cce0746ad02a0ab2c4eb7465ae
evidence/s35_full.xml              9c83f4979462ed69455d58f5f4701cb3c1517c6e40a6dac4cbfb3e81eaafd8f4
```

Install-verified pinned SHA-256:

```text
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
| **F1 — The repair removes invented A input.** A positive now requires an explicit sealed A-local perception receipt and an explicit sealed A-owned action occurrence receipt; `performed` is a receipt field, not a constructor constant. Missing actual input is a typed hold. | Rival: a controlled fixture is close enough to actual actor input. The bridge marks it `TEST_ONLY_CONTROLLED_FIXTURE`, `actual_actor_input=false`, and the default path holds. | Keep controlled evidence separately graded; do not call it actual A input. | S35 engineering + ADP017/ADP019 owner |
| **F2 — Public receipts no longer carry B's private operation.** Source refs, action refs and C12/run public values are clean; only the opaque B event ref/hash remains. | Rival: removing keys but leaving operation-bearing values is enough. The recursive privacy scan rejects the old value leak. | Preserve public-value privacy on any later consumer. | S35 engineering + C12 owner |
| **F3 — The selector now validates the actual consumer readset.** A prepared response cannot be used if rule lookup, event time, conditioning, material, history or offer inputs differ from the qualified preflight. Legacy no-context delegation is preserved. | Rival: matching output shape proves consumer correctness. The consumer-argument negatives and legacy delegation falsify that. | Keep the validation at the actual consumer call site. | C9R consumer owner + S35 engineering |
| **F4 — Objective availability, A perception and A action remain distinct.** Access fault with eligible material becomes `UNKNOWN_RECEIVABILITY`; action fault with accessible material becomes `A_OWNED_ACTION_HOLD`; restore returns the positive. | Rival: material eligibility or B's operation determines A's response. The same-world cuts and restore falsify that. | Do not infer psychology, motive or learned practice. | S35 science owner + CAN008 issuer |
| **F5 — Targetless commit remains real.** The pinned `evaluate_target(proposal=None)` route stays `NO_CHANGE/NO_PROPOSAL`; target tables and cold replay confirm no ghost target. | Rival: the hold/valid-empty path is only a shape test. The named C9 response/receipt assertions and zero target rows are the behavioral evidence. | Preserve; native CAN011 remains unissued. | C9/CAN011 owner + C12 consumer owner |

## 5. Courts and disposition

| Court | Grade |
|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_SOURCEFREE_ACTOR_ACCESS_BRIDGE_REPAIR__EXPLICIT_PERCEPTION_ACTION_RECEIPTS__CONSUMER_INPUT_VALIDATION__PUBLIC_PRIVACY__51_OF_51_TESTS__ZERO_TARGETS__COLD_REPLAY` — author evidence only, not independent adoption. |
| **SCIENTIFIC** | `TEST_ONLY_CONTROLLED_FIXTURE_ORIENTATION_ONLY__ACTUAL_A_INPUT_UNAVAILABLE__NO_ACQUIRED_PRACTICE__H0_LIVE`. |
| **AUTHORITY** | `HOLD` — no native CAN008/CAN011 rule, no grant, no ADP017/ADP019 owner receipt, no C8 native custody, no C11/C12 native consumer, no Pyat N11/N12, no human A5. |

**DONE:** REVISE findings repaired; explicit sealed A-local perception and A-owned action receipts; no B-operation defaults; typed holds for unavailable actual A input; controlled evidence separately graded; public-value privacy; actual consumer rule_lookup/event/conditioning/material/history/offer validation; legacy no-context delegation; causal cuts/restoration; forged A receipt and consumer-argument negatives; public privacy; cold replay; zero target proposals; empty production registries.

**REMAINING:** independent reverify of this exact repair; actual qualified A-local perception and A-owned action owner receipts; native CAN008/CAN011 issuer and grant; native C8/C11/C12 custody; H1 empirical acquisition study; human A5.

**CRITICAL BLOCKER:** actual qualified A-local perception and A-owned action receipts are unavailable; native CAN008/CAN011 authority is unissued. Neither is fabricated here.

**LARGEST MOVE:** one proportionate independent review of this exact sourcefree repair cut while all native/owner lanes stay held.

**FLIGHT:** sourcefree local only; no external provider, native lane, production or human subject.

## 6. Limits / NOT_RUN

- Only this return's 51 focused tests and the evidence generator were run. No 444-file corpus rebuild, no M35/DEV-R/JOIN-E/staged-input edits.
- The positive P1 is explicitly controlled TEST_ONLY evidence, not actual A input. Actual qualified A-local perception and A-owned action occurrence/receipt are NOT_RUN; default/absent actual input is a typed hold.
- The C9R consumer is the pinned code; only its in-process `evaluate_response` name is pointed at the S35 selector. `candidate.pipeline.py` bytes are unchanged and hash-verified.
- All witnesses, C8/E1/C12 records, response receipts and target decisions are TEST_ONLY sourcefree. A sealed TEST_ONLY receipt proves local integrity, not issuer authenticity.
- No native CAN008/CAN011, ADP017/ADP019, C8/C11/C12, Pyat N11/N12, original source rights, human A5, production activation or external model/browser call.
- No claim that B's act is perceived by A, that objective material implies uptake, that REFUSE_TOOL implies a private motive, or that one or two witnessed acts create durable practice.
- H1 acquired practice and defeating H0 remain NOT_RUN/HOLD; no positive practice assertion exists to sever.

## 7. PROGRAMMA_DELTA

`PROGRAMMA_DELTA:` S35 now has a repaired TEST_ONLY sourcefree actor-access bridge that requires explicit sealed A-local perception and A-owned action occurrence receipts (never B-operation defaults or constructor `performed=True`), returns exact typed holds when actual A input is unavailable, keeps controlled fixture positives separately graded, validates the actual C9R consumer rule/time/conditioning/material/history/offer inputs, removes B's private operation from public receipt values and C12/run public values, and still commits `NO_CHANGE/NO_PROPOSAL` with zero target proposals; exact limits: actual qualified A input, native CAN008/CAN011, ADP017/ADP019, C8/C11/C12, Pyat N11/N12, H1 acquired practice and human A5 remain NOT_RUN/HOLD.

## 8. Publication

The prior evidence commit `e1cea3f03555dd96d5b78dd0d8833e993e87ae5a` and its ordinary-push readback remain recorded. The repair commit SHA and direct remote readback are recorded in `PUBLICATION_RECEIPT.json` after publication and returned in the final worker handback.
