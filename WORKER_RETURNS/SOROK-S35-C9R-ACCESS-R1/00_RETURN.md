# SOROK S35 — sourcefree actor-access bridge into the pinned C9R consumer

**RESULT:** `S35_REVISE_REPAIRED_AGAIN__PUBLIC_SOURCE_PROJECTION__PRIVATE_WORLD_CUSTODY__NO_ACTION_CLOCK_VALIDATED__UNRESOLVED_OWNER_EVIDENCE_NOT_ACTUAL__FRESH_PROCESS_COLD_REPLAY__57_OF_57_TESTS__ZERO_TARGET_PROPOSALS__NATIVE_HOLD`.

This is one isolated TEST_ONLY engineering bridge. It is not a native CAN008/CAN011 rule, not an issued target grant, not ADP/C8/C12 authority, not acquired-practice science and not a new engine. It writes only inside `WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/**`.

## 1. Identity, base and read-only inputs

- Repository: private `maidiu/rawlsing`.
- Original S35 base commit: `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`.
- JOIN-E x S35 compatibility base: `a6b1f10b37c0748b0b6880e1870a2c4f07844be9`.
- Branch: `codex/sorok-s35-c9r-access-r1`.
- Exclusive worktree: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`.
- Prior publication base: `67d5363870bf180515f59ced341b8cdffb0c755a`.
- Repair scope: only the S35 REVISE findings; no unrelated changes.
- Role: one bounded sourcefree implementation engineer; not HQ, original CAN/ADP/science issuer, protected C8/C11/C12/native owner, or independent reviewer.
- Host: macOS, Python 3.11.3, pytest 9.1.1, SQLite local. No Codex, no subagent, no external provider/browser/model call, no outside checkout or extra worktree.
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

## 2. Repair of this scoped REVISE

### 2.1 Public projection; private world custody

- Added `S35_PUBLIC_B_SOURCE_PROJECTION@1` and `public_source_projection(source)`.
- Public projection contains only `source_commitment`, `b_actor`, `b_to_actor`, `b_clock`, `operation_disclosed=false`, `native=false`. It contains no `b_owner`, no `b_event_ref`, no `b_event_hash` and no `b_operation`.
- `world.json` is explicitly private custody: `custody.grade=PRIVATE_TEST_ONLY_WORLD_INPUT`, with the full source and case preimage inside `custody`.
- The public run manifest and C12 episode carry `source_binding` equal to the public projection and `private_custody_ref=world.json`.
- Public-value privacy is recursively checked over S35 receipts, run manifests and C12 episode bodies. Tokens checked include `SHARE_TOOL`, `REFUSE_TOOL`, `TEST_ONLY_OWNER_share`, `TEST_ONLY_OWNER_refuse`, `TEST_ONLY_EVENT_share` and `TEST_ONLY_EVENT_refuse`.
- The only later source distinction retained publicly is the opaque `source_commitment`, not B's owner or event identifier value.

### 2.2 No-action clock validation

- `ACTION_TIME_INVALID` now applies to every action receipt, including `performed=false` / `NO_OBSERVED_ACTION`.
- A no-action receipt with `action_time=-1` or `action_time > clock` refuses before any C9 database exists.
- Performed actions additionally require `action_time >= perceived_at` and `action_time >= event_time`.

### 2.3 Unresolved owner evidence

- Qualified actual-grade evidence without an owner resolver remains a typed hold.
- The hold receipt is `evidence_grade=ACTUAL_A_INPUT_UNAVAILABLE`, `actual_actor_input=false`, `qualification=UNRESOLVED_OWNER_EVIDENCE_NOT_ACTUAL`. It is never represented as qualified or actual.
- Resolver rejection paths are tested:
  - perception resolver false -> `A_LOCAL_PERCEPTION_UNVERIFIED`, no commit;
  - perception resolves but action resolver false -> `A_OWNED_ACTION_UNVERIFIED`, no commit.
- No actual A producer is claimed; no actual positive is asserted from a resolver test double.

### 2.4 Fresh-process cold replay and non-mutating verification

- `bridge/readback.py` now reads both C9 and C12 through read-only SQLite URIs; no `C12Store` write-capable object is opened during verification.
- `tools/cold_replay.py` runs cold verification in a fresh Python process, hashes `world.json`, `c12.sqlite`, `c9.sqlite`, `run.json` and `s35_receipt.json` before and after, and reports `store_mutated`.
- Evidence records a fresh process (`fresh_process=true`) with `store_mutated=false` and identical before/after hashes.
- The in-process cold test also asserts byte-identical store files before and after `cold_verify`.

## 3. Exact execution evidence

Commands actually run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tests \
  --junitxml=WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/evidence/s35_full.xml
# 57 passed, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1/tools/capture_evidence.py
# vectors=12, foreign perception refusals=19, foreign action refusals=16,
# cold_all_ok=true, consumer_all_negative=true,
# fresh_process_cold_replay_ok=true, store_mutated=false,
# legacy delegation all equal, fault trials PASS/RED/PASS for both gates
```

Evidence files:

- `evidence/test_run.txt` — exact pytest transcript.
- `evidence/s35_full.xml` — JUnit, 57 tests, 0 failures/errors/skips.
- `evidence/s35_evidence.json` — vectors, same-world bindings, fault trials, foreign/forged refusals, consumer binding, public projection, no-action clock, qualified-owner paths, fresh-process cold replay, public privacy and source manifest.
- `evidence/join_e_s35_compat.json` — bounded JOIN-E x S35 compatibility proof, exact clock incompatibility, B material/E help contrast, cold replay and no-new-store evidence.

### P1 controlled positive

```text
B source event hash (M35 share)  16f11d2e849cbb3abcbfd8c76d32a509a38e74e3b503361dddeb2adf9403a486
C8 state digest                  e472d9f9331cd827e70902232419eb0cc8dc590c9503e2f3040501eec84bb6fb
E1 event                         TEST_ONLY_BP2_E1_OCC-0001
E1 hash                          77b8874d68810b835c680f85dbcb4fd3019012ac0ac8d1990a6758967fa10146
C12 root / branch                root / s35
root branch hash                 602e191a79c713d4dd3ec7ba93caf7d7b6ee7db0fb17e2b673b23ca40abb0dc6
root state hash                  406a019d868884a1797c44e59b3bf9a2bb3547afc0b46fe0695e3938ef78573d
branch hash                      2f7016268ff5ed9a73075ed0c25c0d5bd5ac072a2356f68980633ae266f35523
branch fork / frame clock        242 / 244
actor                            TEST_ONLY_BP1_R26V_ACTOR_A
perception ref / hash            TEST_ONLY_A_PERCEPTION_P1 / c45fba70492aed0b27ee506a3623ba32715c64047b525b1fe2789596a1d96164
action ref / hash                TEST_ONLY_A_ACTION_P1 / 476c13c80722b134893708dee8a013d2eaa52cebce79d4cd4f568c0109dfbe38
action kind / performed          REQUEST_TOOL / true (explicit controlled receipt)
evidence grade                   TEST_ONLY_CONTROLLED_FIXTURE
actual actor input               false
qualification                    CONTROLLED_ENGINEERING_EVIDENCE_NOT_ACTUAL_A_INPUT
public source projection         source_commitment 7f5a08b2e7f0d482092a92a66261aaa560959fd169188408fa35ffe434561eec
S35 outcome                      OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
S35 receipt hash                 c5bc1aa1a89b7852024dde968fea076d306cf2f90f354515e6e1746735f5db5d
C9 response row hash             404b3389fbdd8dd8e3b8eabfc2fba5c47678ffabdf206ebdc7b7f7305f6a8477
C9 commit receipt hash           dcd6f7e4b2ec71c511db1e1d6e59f28e441f0f5c9e61da5e86bac1203ddbc258
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

Fault trials on the same assertion:

```text
a-local perception gate  PASS -> RED -> PASS
a-owned action gate      PASS -> RED -> PASS
```

### No-action clock and qualified-owner paths

```text
no-action action_time=-1  -> REFUSED / ACTION_TIME_INVALID, no C9 database
no-action action_time>clock -> REFUSED / ACTION_TIME_INVALID, no C9 database
qualified owner unresolved hold -> ACTUAL_A_INPUT_UNAVAILABLE,
  actual_actor_input=false, qualification=UNRESOLVED_OWNER_EVIDENCE_NOT_ACTUAL
qualified perception resolver false -> A_LOCAL_PERCEPTION_UNVERIFIED, no commit
qualified action resolver false -> A_OWNED_ACTION_UNVERIFIED, no commit
no actual A producer or actual positive is claimed
```

### Public projection, privacy and cold replay

- `world.json` private custody: `PRIVATE_TEST_ONLY_WORLD_INPUT`; full source operation is present only there.
- `public_projection` has no `b_owner`, `b_event_ref`, `b_event_hash` or `b_operation`; `operation_disclosed=false`.
- Public privacy is true for every S35 receipt, run manifest and C12 episode; no owner/event share/refuse tokens are present in public values.
- Fresh-process cold replay: `fresh_process=true`, `store_mutated=false`, before/after hashes identical for `world.json`, `c12.sqlite`, `c9.sqlite`, `run.json` and `s35_receipt.json`.
- In-process cold verification also leaves the same files byte-identical.

### Forged/foreign refusals and consumer negatives

- 19 perception mutations and 16 action mutations refuse before any C9 database exists.
- Source-hash mismatches refuse `PERCEPTION_SOURCE_HASH_MISMATCH` / `ACTION_SOURCE_HASH_MISMATCH`.
- All nine consumer-argument mutations reject with `S35_CONSUMER_INPUT_MISMATCH:<field>`: rule_lookup, event_time, conditioning_readset, material_eligible, eligible_material_refs, actor_history_refs, other_person_offer_ref, material_opportunity_ref, prior_response_count.
- Legacy no-context delegation is exercised: `candidate.pipeline.evaluate_response` matches `candidate.evaluate_response` on status, reason, proposals, receipt hash and route.

### Source/custody hashes

```text
install.py                         8e194dcf2de4049bf074c5457800db65d4193b34e8e89a763ef0231c377fb5dd
bridge/__init__.py                 d334157bcff6f84c7609d5f3ccf41aacfca162617e27a808891889ef95b1de44
bridge/access.py                   5265e5a0fd5b16043f599b6da2ee960cb3faf2c07447858819f853c2ffb02458
bridge/world.py                    7077ee3105d8c6488b619bfc2f60c39d2490da7166b254350e8dfad845f8746f
bridge/readback.py                 e291ca5bd200ba582f357766b4f290be5c852b37f4cc16a855fc84e8e8f5175f
tests/test_s35_access_bridge.py    9cbb93221d4c8e13472eb9d10eab233cae531ed1031891647d9c40fe046b2179
tools/capture_evidence.py          104376ad40bf43a22879e1fd2da791061e0772ed5ba7ae058d11ea523307f3d1
tools/cold_replay.py               a374e53d8926757959f0ab8da92a2f3ead55f73cf3a24b26dcc5dfc3c4f0ad59
bridge/join_e_source.py            c8a6c05f34d5983045a05c65e5a816cd82149a8af0d7d60ab07195d7ec0ff72e
bridge/join_e_compat.py            fa81377367e423e1b130dad678f7faa46e6235dcbd4230adefa3177d697d3d56
bridge/occurrence_consumer.py      619c83e031355076c8d5f8188d39ad69ca0733f72a973dda5414cd1e7c9a7e36
tests/test_join_e_s35_compat.py    4d50a4afcd43792e881a2d2c605fd0b4899c4337bb96f53f659a8a8c419ee07c
tests/conftest.py                  4f90d4bf36fe486ed75dcfdf670e8e2b033b8d77afc70759fedb10c8b112bdc1
tests/test_occurrence_consumer.py  f4102c10b65e0afc661d341ed77daf7dc3cbe7c8595ceff41e6cc95a301214c0
tools/join_e_encounter.py          2c04feffe071f26828f915ba94cb95bfa83a5eeed7b941fbee24a59ed88f3998
tools/join_e_s35_compat.py         bc6f3ac8b25b48795d84d9d79e6d63ca7512454bf12184902909921cf85f5d5b
tools/occurrence_consumer_proof.py 70185a7f7ae1ab47c55dfeb7f5dc108eedf903ea4c7245199580826873a11499
evidence/test_run.txt              23052e9c9f035322c5b3622c9b73c397f03cca312da24f2782a20e78152def34
evidence/s35_full.xml              f29ec031d1a3c29a59fe5ae0b1c4b93ed03e87eaca67f3b0f20004d7441c1ca9
evidence/s35_evidence.json         7c882145de70cb21580519d1ccbe9c1f5eda283e6423e8c23f7e65971d19dbe7
evidence/join_e_s35_compat.json    1d0c97c693a1fd73515833dc21ec4d3613585c96e30348cb1e70754db7af6350
evidence/occurrence_consumer.json  51bc098e6110ac38021249de4bca0e6bf54a76f65da7ee4e5a0e79ac10a7fc1a
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

## 3A. Bounded JOIN-E x S35 compatibility proof

- JOIN-E source was read from Git commit `5e63672543973ce2533129e1ca3224d82af0dffc` with `git archive` inside this checkout into a gitignored runtime tree. No external checkout was read.
- Three selected persistent JOIN-E roots were used: `PERFORMED` (B performed `SHARE_TOOL`), `OMITTED` (B sealed `SHARE_TOOL` with `performed=false`), and `REFUSED` (B performed `REFUSE_TOOL`). Source and clock bindings came from the persisted C9 occurrence and C12 branch rows.
- Evidence: `evidence/join_e_s35_compat.json`.

| Disposition | B source | material_feasible_after | performed-aware access | operation-only would grant | E help | tools |
|---|---|---|---|---|---|---|
| `PERFORMED` | `SHARE_TOOL`, performed=true | true | true | true | accept | 1 |
| `OMITTED` | `SHARE_TOOL`, performed=false | false | false | true | refuse | 0 |
| `REFUSED` | `REFUSE_TOOL`, performed=true | false | false | false | refuse | 0 |

No operation-only material grant was observed in JOIN-E: the omitted source would grant under a naive operation-only rule, but the actual persisted source has `material_feasible_after=false`, the performed-aware compatibility access is false, and the actual E consumer refuses help with tools 0. The compatibility adapter therefore uses the performed-aware rule, not B's operation alone.

### Exact same-root incompatibility

The JOIN-E E1 event is at time `242`, while the selected C12 branch clock is `10`; the existing C9 last clock is also `242`. The persisted event is already admitted. A second full S35 `run_candidate_path` execution on that same C9 store is refused by the pinned consumer with `CLOCK_OUTSIDE_FRAME`, and the event identity is already occupied. Reusing the existing store cannot lawfully execute the full S35 C9 commit; creating a second C9 store is prohibited by this bounded proof. `same_root_c9_reexecution_lawful=false`.

The lawful S35 result on the JOIN-E root is therefore a typed hold:

- baseline (no actual A producer): `A_LOCAL_PERCEPTION_HOLD` for all three dispositions;
- controlled A perception/action receipts bound to the actual E1 time/root/clock refuse `PERCEPTION_TIME_INVALID` because `event_time=242 > clock=10`;
- independent perception/action severance diagnostics remain `PERCEPTION_TIME_INVALID` for the same clock reason and are not admitted as a positive;
- the later actual E help consequence remains the JOIN-E world consequence: accept for performed share, refuse for omitted and refused;
- cold reopen verifies each session and repeats the same E help and S35 hold/clock outcomes;
- S35 creates no store and the JOIN-E C9/C12 files are byte-identical before and after S35 evaluation.

**Exact incompatibility:** `JOIN_E_E1_TIME_242_OUTSIDE_C12_CLOCK_10__C9_EVENT_ALREADY_ADMITTED__FULL_S35_REEXECUTION_CLOCK_OUTSIDE_FRAME`. A same-root full-pipeline weld is not lawful without a new C9 store or an explicitly authorized clock/branch migration; neither is fabricated here. The distinct-clock reader in section 3B is the lawful admitted-occurrence read; it does not claim a full C9 re-execution.

## 3B. Smallest same-root admitted-occurrence consumer

**Exact first consumer:** `bridge/occurrence_consumer.py:read_occurrence->evaluate_occurrence`.

The consumer reads the already-admitted JOIN-E C9 occurrence and C12 branch root read-only. It does not call `CandidateStore`, does not admit the event again, and does not create a second store. It validates, in order:

1. event hash/id/time against the persisted C9 occurrence and event identity;
2. C12 root branch and selected branch hashes, parent, fork clock and branch clock;
3. source operation/perform/quantity/clock and the performed-aware material access;
4. an explicit sealed clock-domain binding;
5. qualified A perception and A action receipts separately;
6. only then the normal S35 response selector and targetless CAN011 decision.

### Distinct source clocks

| Field | Value | Source |
|---|---|---|
| `event_clock` | `242` | `JOIN_E_C9_OCCURRENCE_TIME` |
| `event_clock_domain` | `JOIN_E_E1_ACTOR_EVENT_CLOCK` | admitted E1 occurrence |
| `branch_clock` | `10` | `JOIN_E_C12_BRANCH_LAST_CLOCK` |
| `branch_clock_domain` | `JOIN_E_C12_WORLD_CLOCK` | selected C12 branch |
| `distinct_sources` | true | sealed clock binding |
| `substitution` / `equality_claimed` | false / false | sealed clock binding |
| clock binding hash | `e107e8408e39997d9ad09721307656d212379c5dfe8283be3b8a425734152534` | all three dispositions |

The S35 response is evaluated in the E1 actor/event clock frame (`clock=242`); the C12 root/branch identity is validated in its own world clock frame (`branch_clock=10`). No clock is substituted for the other.

### Persisted JOIN-E provenance binding

`read_occurrence` no longer treats caller-supplied path/source/event/actor fields as authority. It reads `state_root/session.json`, the persisted JOIN-E product provenance (`bp2_join.json` or `refusal.json`), the exact C8 journal occurrence and the C12 root/branch rows, then:

- derives the canonical C9 path (`<state_root>/bp2/c9.sqlite` for JOIN, `<state_root>/source/bp2/c9.sqlite` for REFUSAL) and C12 path (`<state_root>/product/c12.sqlite`);
- requires the C9 occurrence hash/time/id and C8 journal occurrence clock/state digest to equal the persisted session values;
- requires the bundle source to equal `session.j_source`, the C8 journal `gm01_pre_c9_source` and the product sidecar source;
- requires the bundle branch id, source actor map, C8 state digest and event identity to equal the persisted session/provenance values;
- binds the actor snapshot source ref/hash and actor id to the persisted C8 journal and C12 actor block; the caller actor snapshot is not used as authority;
- uses the persisted C8 journal/C12 actor state to construct the occurrence actor snapshot.

The exact reviewer mix was reproduced: performed C9 path/event/hash/time/id combined with refused `source`, `c12_path`, `branch_id`, `source_actor_map` and `actor_snapshot`. It is refused before response evaluation. Because the branch id and actor source are the same across these sourcefree roots, the discriminating persisted checks are the source and C12/canonical path bindings.

| Substitution test | Result | Missing persisted binding |
|---|---|---|
| performed C9 + refused source | refused | `bundle_source_matches_session`, `bundle_source_matches_journal` |
| performed C9 + refused C12 path | refused | `c12_path_canonical` |
| performed C9 + refused source/C12/actor fields | refused | `c12_path_canonical`, source bindings |
| performed C9 + refused C9 path/event | refused | `c9_path_canonical`, `bundle_event_hash_matches` |
| refused C9 + performed source | refused | source bindings |
| mutated actor snapshot source/id | refused | actor source/actor-id bindings |
| cold performed C9 + refused source/C12 | refused | `c12_path_canonical`, source bindings |

The intact read-only path, distinct-clock binding, perception/action severance/restoration and cold replay remain unchanged. No store is written.

### Intact, severed, restored and cold

| Disposition | Intact outcome | Controlled intact | Perception severed | Action severed | Restored | E help / tools | Cold |
|---|---|---|---|---|---|---|---|
| `PERFORMED` | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | same | `UNKNOWN_RECEIVABILITY` | `A_OWNED_ACTION_HOLD` | intact | accept / 1 | intact |
| `OMITTED` (`SHARE_TOOL`, performed=false) | `A_LOCAL_PERCEPTION_HOLD` | `A_OWNED_ACTION_HOLD` | `UNKNOWN_RECEIVABILITY` | `A_OWNED_ACTION_HOLD` | intact | refuse / 0 | intact |
| `REFUSED` | `OBSERVED_CURRENT_REFUSAL` | same | `UNKNOWN_RECEIVABILITY` | `A_OWNED_ACTION_HOLD` | intact | refuse / 0 | intact |

- Performed share controlled S35 receipt: `97b471c58fa6c5fe89bd7f47c4d055a17566c44651f3523fb758ba657a9e9423`.
- Omitted typed hold receipt: `9e3f1877835c0c80318067bca6e6b36e5fe1043e1f2d2bad5ee7d85fb74c02bb`; material access false.
- Refused controlled S35 receipt: `80f6e36b0ec79a639c69b141c64c44de5c491bcabc0451b29c892cfecc2ff3f9`.
- All CAN011 decisions are `NO_CHANGE/NO_PROPOSAL` with zero target proposals.
- A clock-substitution binding (event clock force-equal to branch clock) refuses in all three worlds.
- Cold reopen verifies each JOIN-E session and reproduces the same S35 outcomes; E help remains accept/refuse/refuse.
- C9/C12 files are byte-identical before and after S35 evaluation; no duplicate admission and no new store.

### Missing actual A source-owner contract

Actual qualified A perception and A action are unavailable and are not fabricated. The reader returns the exact contract:

```text
qualified_a_perception_receipt  S35_A_LOCAL_PERCEPTION_RECEIPT@1
  owner=A local perception source owner
  event hash/id, event clock 242, root/branch, domain JOIN_E_E1_ACTOR_EVENT_CLOCK
qualified_a_action_receipt      S35_A_OWNED_ACTION_OCCURRENCE@1
  owner=A action occurrence owner
  event hash/id, event clock 242, root/branch, performed flag required
clock_domain_binding            S35_SAME_ROOT_CLOCK_BINDING@1
  event clock 242 vs branch clock 10, distinct sources, no substitution
actual_a_producer = NONE_VERIFIED
```

Controlled inputs above are explicitly `TEST_ONLY_CONTROLLED_FIXTURE`, `actual_actor_input=false`, and are usable only as bounded engineering evidence.

## 4. Findings, interpretation and owner

| FINDING | INTERPRETATION AND RIVAL | HQ ACTION | COMPETENT OWNER |
|---|---|---|---|
| **F1 — Public owner/event identifiers are projected away.** Private custody remains in `world.json`; public run/C12 values carry only an opaque source commitment plus neutral actor/clock fields. | Rival: removing the literal operation token is sufficient. The old `TEST_ONLY_OWNER_share` / `TEST_ONLY_EVENT_refuse` identifier values falsify that. | Keep the public projection for any later consumer. | S35 engineering + C12 owner |
| **F2 — No-action clocks are validated.** A no-action receipt with `action_time=-1` or beyond the frame refuses before C9, not commits. | Rival: performed-only time validation is enough. The no-action negative-clock test falsifies that. | Preserve the all-branches clock check. | S35 engineering + C12 clock owner |
| **F3 — Unresolved owner evidence is not actual/qualified.** Holds are `ACTUAL_A_INPUT_UNAVAILABLE` with `UNRESOLVED_OWNER_EVIDENCE_NOT_ACTUAL`; resolver false paths refuse. | Rival: a qualified receipt remains qualified while held. The hold receipt grading falsifies that. | Do not promote unresolved owner evidence. | ADP017/ADP019 owner + S35 engineering |
| **F4 — Verification is non-mutating and fresh-process replayable.** C9/C12 are opened read-only; fresh process hashes before/after and reports no mutation. | Rival: in-process replay could reuse warm state. The fresh PID/process and identical hashes falsify that. | Preserve read-only verification and cold replay evidence. | S35 engineering + C12 custody owner |
| **F5 — Controlled positives, targetless outcomes and prior negatives remain.** P1 is controlled evidence, CAN011 stays `NO_CHANGE/NO_PROPOSAL`, target tables stay empty, and all prior foreign/consumer/legacy negatives stay green. | Rival: the privacy/clock repair loosened the prior bridge. The 57-test and evidence reproduction falsify that. | Keep native authority held. | C9/CAN011 owner + C12 consumer owner |
| **F6 — JOIN-E × S35 same-root weld is clock-incompatible.** JOIN-E E1 time `242` exceeds C12 branch clock `10`; the existing C9 event is admitted and re-execution refuses `CLOCK_OUTSIDE_FRAME`. JOIN-E itself is performed-aware: omitted `SHARE_TOOL` has no material grant and E refuses help. | Rival: a selector-only positive can stand in for the unavailable full pipeline. The exact clock refusal and existing admitted event falsify that; no second store is fabricated. | Record the typed incompatibility; require an authorized clock/branch migration or a new store decision from the owner before any full weld. | JOIN-E/C12 owner + S35 engineering |
| **F7 — The admitted occurrence is readable when clocks are explicitly distinguished.** `bridge/occurrence_consumer.py` reads the existing C9 occurrence at E1 `242` and C12 branch at `10`, binds both source domains explicitly, validates event/root/branch/source/clock and A perception/action separately, then calls the normal S35 response. No duplicate admission or new store. | Rival: the earlier `PERCEPTION_TIME_INVALID` proves no same-root read is possible. The distinct-clock reader falsifies that for a read; full C9 re-execution remains incompatible. | Preserve the distinct-clock reader as the exact first consumer; keep the full weld owner-held. | JOIN-E/C12 owner + S35 engineering |
| **F8 — Occurrence authority is persisted JOIN-E provenance, not self-hashed caller input.** `read_occurrence` derives paths/source/event/actor from `session.json`, the JOIN-E product provenance, the C8 journal and C12 rows; cross-root/source substitutions are refused live and cold. | Rival: binding the C9 row to caller-supplied source and paths is sufficient. The reproduced performed-C9/refused-source-and-C12 mix is refused, falsifying that. | Keep provenance binding mandatory for any later reader. | JOIN-E/C8/C12 owner + S35 engineering |

## 5. Courts and disposition

| Court | Grade |
|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_SOURCEFREE_ACTOR_ACCESS_REPAIR__PUBLIC_PROJECTION__NO_ACTION_CLOCK__UNRESOLVED_OWNER_HOLD__FRESH_PROCESS_COLD_REPLAY__57_OF_57_TESTS__ZERO_TARGETS` — author evidence only, not independent adoption. |
| **SCIENTIFIC** | `TEST_ONLY_CONTROLLED_FIXTURE_ORIENTATION_ONLY__ACTUAL_A_INPUT_UNAVAILABLE__NO_ACQUIRED_PRACTICE__H0_LIVE`. |
| **AUTHORITY** | `HOLD` — no native CAN008/CAN011 rule, no grant, no ADP017/ADP019 owner receipt, no C8 native custody, no C11/C12 native consumer, no Pyat N11/N12, no human A5. |

**DONE:** public projection and private world custody; no owner/event identifier leak; no-action clock validation; unresolved owner evidence held as unavailable/not actual; resolver false paths; fresh-process cold replay; non-mutating verification; controlled positives; zero target proposals; prior foreign/consumer/legacy negatives preserved; bounded JOIN-E x S35 performed/omitted/refused material/E-help contrast; exact same-root clock incompatibility recorded; smallest read-only admitted-occurrence consumer with distinct event/branch clock binding, separate A perception/action gates, intact/severed/restored/cold proof and exact missing A-owner contract; no new store.

**REMAINING:** independent reverify of this exact repair; actual qualified A-local perception and A-owned action owner receipts; a lawful same-root clock/branch migration decision if the owner wants a full C9 weld rather than the read-only admitted-occurrence consumer; native CAN008/CAN011 issuer and grant; native C8/C11/C12 custody; H1 empirical acquisition study; human A5.

**CRITICAL BLOCKER:** actual qualified A-local perception and A-owned action receipts are unavailable; full same-root C9 re-execution remains blocked by the already-admitted E1 event and distinct clock frame (`242` vs `10`); native CAN008/CAN011 authority is unissued. None of these is fabricated here.

**LARGEST MOVE:** one proportionate independent review of this exact sourcefree repair cut while all native/owner lanes stay held.

**FLIGHT:** sourcefree local only; no external provider, native lane, production or human subject.

## 6. Limits / NOT_RUN

- Only this return's 57 focused tests and the evidence generator were run. No corpus rebuild, no M35/DEV-R/JOIN-E/staged-input edits.
- The positive P1 is explicitly controlled TEST_ONLY evidence, not actual A input. Actual qualified A-local perception and A-owned action occurrence/receipt are NOT_RUN; absent actual input is a typed hold.
- The C9R consumer is the pinned code; only its in-process `evaluate_response` name is pointed at the S35 selector. `candidate.pipeline.py` bytes are unchanged and hash-verified.
- All witnesses, C8/E1/C12 records, response receipts and target decisions are TEST_ONLY sourcefree. A sealed TEST_ONLY receipt proves local integrity, not issuer authenticity.
- No native CAN008/CAN011, ADP017/ADP019, C8/C11/C12, Pyat N11/N12, original source rights, human A5, production activation or external model/browser call.
- No claim that B's act is perceived by A, that objective material implies uptake, that REFUSE_TOOL implies a private motive, or that one or two witnessed acts create durable practice.
- H1 acquired practice and defeating H0 remain NOT_RUN/HOLD; no positive practice assertion exists to sever.

## 7. PROGRAMMA_DELTA

`PROGRAMMA_DELTA:` S35 keeps B owner/event identifiers and operation in private `world.json` custody and publishes only an opaque source commitment; validates no-action clocks as strictly as performed-action clocks; holds unresolved owner evidence as `ACTUAL_A_INPUT_UNAVAILABLE` / `UNRESOLVED_OWNER_EVIDENCE_NOT_ACTUAL`; demonstrates fresh-process cold replay with non-mutating read-only verification; and provides the smallest same-root admitted-occurrence consumer `bridge/occurrence_consumer.py:read_occurrence->evaluate_occurrence`. It binds the occurrence to persisted JOIN-E `session.json`, product provenance, the exact C8 journal source/occurrence and C12 root/branch/actor rows, rejects cross-root and source substitution live/cold, reads the already-admitted E1 `242` while keeping the C12 branch clock `10` as a distinct source domain, validates A perception/action separately, then calls the normal S35 response; intact/severed/restored/cold preserve performed/omitted/refused and E-help outcomes with no duplicate admission, second store or clock substitution. Full C9 re-execution remains incompatible: `JOIN_E_E1_TIME_242_OUTSIDE_C12_CLOCK_10__C9_EVENT_ALREADY_ADMITTED__FULL_S35_REEXECUTION_CLOCK_OUTSIDE_FRAME`. Actual A inputs remain `NONE_VERIFIED`; the exact missing source-owner contract is returned. Exact limits: actual qualified A input, full same-root C9 weld, native CAN008/CAN011, ADP017/ADP019, C8/C11/C12, Pyat N11/N12, H1 acquired practice and human A5 remain NOT_RUN/HOLD.

## 8. Publication

Occurrence-consumer base `c5602ec87ba6e951540b89a49404db76c128eb50`, compatibility base `a6b1f10b37c0748b0b6880e1870a2c4c4f07844be9`, PROGRAMMA disposition `29aa0f9e81fe1f371f2773d4750e1838bdd63daf` and JOIN-E source commit `5e63672543973ce2533129e1ca3224d82af0dffc` remain recorded. The provenance repair for REVISE at `eb2255231df00393d33cc0223bc5d79320360f88` was committed as `d504231674fe02fb765502b0cb4e187d4a5e0560` and pushed with an ordinary non-force push to `origin/codex/sorok-s35-c9r-access-r1`. Direct remote readback:

```text
git rev-parse HEAD
d504231674fe02fb765502b0cb4e187d4a5e0560
git ls-remote origin refs/heads/codex/sorok-s35-c9r-access-r1
d504231674fe02fb765502b0cb4e187d4a5e0560  refs/heads/codex/sorok-s35-c9r-access-r1
```

`PUBLICATION_RECEIPT.json` records that push, readback, exact first consumer, distinct-clock read, persisted provenance binding and the remaining full-pipeline incompatibility. The staged `.s35-sources` input and the extracted `.runtime` JOIN-E source were not committed. This return-metadata update is a follow-up scoped commit; the final branch tip SHA is returned in the worker handback.
