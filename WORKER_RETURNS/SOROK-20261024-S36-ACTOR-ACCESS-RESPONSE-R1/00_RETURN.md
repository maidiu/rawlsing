# SOROK S36 — TEST_ONLY actor-access / witnessed immediate-response bridge

**RESULT:** `S36_TEST_ONLY_S35_ACTOR_ACCESS_RESPONSE_BRIDGE_IMPLEMENTED__39_OF_39_FOCUSED_TESTS_PASS__SCENE_BINDING_ORACLE_3_OF_3__ZERO_TARGET_PROPOSALS__CAN011_NO_CHANGE_NO_PROPOSAL__NATIVE_AND_SCIENCE_HOLD`.

This is an isolated TEST_ONLY engineering bridge of the S35 conditional actor-access/immediate-response specification into the actual existing C9R `run_candidate_path` pipeline. It is not a native CAN008/CAN011 rule, not an issued target grant, not acquired-practice science, and not a new engine. It writes only inside `WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1/**`. The original C9R return at `WORKER_RETURNS/SOROK-20261019-C9R-WHOLE-ACTOR-BOUNDARY-AND-CONSUMER-REPAIR-R1/**` was read from the pinned Git object store and was not altered.

## Identity, pinned source and scope

- Repository: private `maidiu/rawlsing`; assigned branch `agent/rabochii-sorok-20261024-s36-actor-access-response-r1`.
- Startup/prior local commit: `888ccae53ec02ca572cbb7ba208956e2c99170b9`.
- Pinned C9R code cut: `6fa2939972ce5a2c0cc4f2b033946b276f1c2934`.
- Reused pinned blobs: `candidate/response_rules.py` `a5c30af336116863e2e6805299b772c89a2ad841`, `candidate/target_rules.py` `c33fc2a6a58efd422cb5289c080205b9e0183102`, `candidate/pipeline.py` `cb0350909dedd9f7159dce145ba216b211a8185c`, `candidate/conditioning.py` `3a5c83ae35bb4d8ca26f40e00ca1fe10868deb23`, plus the other pinned candidate and native-guard files.
- Four S35 files read directly from `WORKER_RETURNS/SOROK-20261024-S35-A-T-SCIENCE-CANDIDATE-R1/`: `00_RETURN.md`, `01_S35_CONDITIONAL_A_T_SCIENTIFIC_RESOURCE_CANDIDATE.json`, `02_SCHOLARLY_WARRANT_SOURCE_RIGHTS_AND_H0.md`, `03_C9R_EXACT_CONSUMER_CONTRACT_AND_TEST_VECTORS.md`.
- Pinned candidate and native-guard bytes were materialized with `git archive` from the pinned commit into this return. No full transitive tree was read. Warm closures were not modified.
- No M35, language, controller, PRE-MAIN, Pyat, original C9P/C9PI, original C9R, native CAN008/CAN011, ADP, C8, C11, C12 or human-study files were edited.

## Independent review repair — REVISE25fdc92

Reviewer `f3f87d9ab0cd91338874e5643c681c151cc070df` reported `REVISE25fdc92` with reproduced `2 PASS / 1 FAIL`: an empty access-witness scene was accepted for an actual garage event because `_access_error` compared scene only when both strings were truthy. The reproducer is `/Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S36/oracles/s36_scene_binding_oracle.py`.

Exact repair:

- Access scene is now required to be a nonempty string before any response commit. An empty or missing scene returns `S35_ACCESS_SCENE_MISSING`.
- The admitted event scene is also required to be a nonempty string. An empty/missing event scene returns `S35_ACCESS_EVENT_SCENE_MISSING`.
- A nonempty scene that differs from the exact admitted event scene still returns `S35_ACCESS_SCENE_MISMATCH`.
- Exact nonempty scene still yields the positive observed-response result, zero target proposals and `NO_CHANGE/NO_PROPOSAL`.
- Added regression coverage for empty and missing access scenes, plus an empty actual event scene. No other hardening or redesign was made.

Oracle command and actual result:

```text
PYTHONPATH=<S36 return>:<S36 return>/runtime/native \
python3 /Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S36/oracles/s36_scene_binding_oracle.py
# counts: {"PASS": 3, "FAIL": 0}
# scene_wrong  REFUSED  S35_ACCESS_SCENE_MISMATCH
# scene_empty  REFUSED  S35_ACCESS_SCENE_MISSING
# scene_exact  RESPONSE_COMMITTED  OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
```

## What was actually implemented

### New bridge module

`candidate/actor_access_response.py` adds an S35-specific response selector:

- `S35ActorAccessRequest` carries `access_witness`, `response_witness`, `contradictory_context`, `contradictory_refs` and `revoked_source_refs`.
- Access witness schema `S35_ACTOR_LOCAL_E1_ACCESS@1` binds `source_ref`, `source_class`, `actor_id`, exact `event_ref`, `access_time`, access status, scene, content and revocation through a sealed source hash.
- Response witness schema `S35_ACTOR_OWNED_IMMEDIATE_RESPONSE@1` binds `source_ref`, `source_class`, `actor_id`, exact `event_ref`, `response_ref`, response kind, response time, content and revocation through a sealed source hash.
- Accepted response kinds are exactly `ATTEND_OBJECT`, `REQUEST_TOOL` and `EXPLICIT_REFUSAL`.
- Test-only namespaces are `TEST_ONLY_ADP017_ACCESS*` and `TEST_ONLY_A_RESPONSE*`.
- Positive result requires exact actor-local E1 access and a separately witnessed actor-owned response. Missing access is `UNKNOWN_RECEIVABILITY`; missing response after access is `RECEIVABLE_NO_OBSERVED_UPTAKE`; contradictory context without a response is `AMBIGUOUS_CONTRADICTORY`.
- Wrong actor, wrong event, wrong source hash, wrong scene, wrong time, invalid kind and revoked source/field are typed `REFUSED`.
- Every result has `target_proposals=()`. The S35 receipt explicitly carries `target_proposals: []`, `belief_update: null`, `emotion_update: null`, `durable_update: null`, `objective_material_implies_uptake: false` and claim ceiling `OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A`.

### Minimal C9R pipeline overlay

Two pinned files changed in the isolated overlay only:

- `candidate/pipeline.py` adds optional `s35_request` to `run_candidate_path`. When present, the existing C9R pipeline calls the S35 selector instead of legacy `evaluate_response`; S35 refusals abort before occurrence/response/target commit; the committed C9R response body carries the sealed `s35_receipt`. When `s35_request` is absent, the existing legacy path is unchanged.
- `candidate/response_rules.py` adds the optional `s35_receipt` field to `ResponseResult`; its default is `None`, so legacy constructors and behavior are unchanged.

The actual C9R stages still run: actor ingress, event-witness ingress, read-only conditioning, material eligibility, response lookup, target evaluation, atomic commit, later target read and performed-action admission. The S35 path always produces `proposal=None`; `candidate.target_rules.evaluate_target(proposal=None, ...)` returns `NO_CHANGE/NO_PROPOSAL`. The `CandidateStore` response row contains the sealed S35 receipt. No V3MS target row is created.

## Actual execution evidence

Commands run with the normal shell, no wall-clock timeout:

```text
PYTHONPATH=.../SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1:.../runtime/native \
python3 -m pytest -q -p no:cacheprovider .../tests
# 39 passed

PYTHONPATH=... python3 .../run_s36_evidence.py
# {"faults_all_pass": true, "legacy_proposals": 1,
#  "refusals": 21, "s35_proposals": 0,
#  "tests": {"ERROR": 0, "PASS": 39, "RED": 0, "SKIP": 0, "tests": 39},
#  "vectors": 9}
```

JUnit and machine evidence:

- `junit/s36_full.xml` — 39 PASS / 0 RED / 0 ERROR / 0 SKIP.
- `evidence/vectors.json` — nine executed rows covering the six S35 vector families and subcases.
- `evidence/refusals.json` — 21/21 refusals, all with zero target proposals, `committed=false`, `no_ghost=true`, empty store tables.
- `evidence/fault_trials.json` — two same-assertion source-mutation trials, both PASS → RED → PASS.
- `evidence/legacy_path.json` — legacy two-history response still yields one CREATE proposal; S35 two-history route yields zero proposals and `NO_CHANGE/NO_PROPOSAL`.
- `evidence/source_manifest.json` — pinned blobs, byte-exact files, changed files and new files.
- `evidence/test_run.json` — exact full-suite counts and per-test status.
- `logs/` — full-suite and fault-phase logs.

### Six S35 vectors: actual outcomes

| Vector | Actual S35 response | Proposals | CAN011 | Evidence note |
|---|---|---|---|---|
| P1 observed immediate positive | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | 0 | `NO_CHANGE/NO_PROPOSAL` | exact access + actor-owned `REQUEST_TOOL`; response row committed |
| N1 B share but A unaware | `UNKNOWN_RECEIVABILITY` | 0 | `NO_CHANGE/NO_PROPOSAL` | same material/B share, no actor-local access; objective material did not imply uptake |
| N2 contradictory project, no response | `AMBIGUOUS_CONTRADICTORY` | 0 | `NO_CHANGE/NO_PROPOSAL` | contrary project ref preserved in receipt/readset |
| N3A B share, same public refusal | `OBSERVED_CURRENT_REFUSAL` | 0 | `NO_CHANGE/NO_PROPOSAL` | A-owned `EXPLICIT_REFUSAL`; B motive not inferred |
| N3B B refuse, same public refusal | `OBSERVED_CURRENT_REFUSAL` | 0 | `NO_CHANGE/NO_PROPOSAL` | same public surface, different objective B cause; no forced speech contrast |
| N4A label baseline | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | 0 | `NO_CHANGE/NO_PROPOSAL` | fixed actor/event/access/action/world |
| N4B label-only perturbation | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | 0 | `NO_CHANGE/NO_PROPOSAL` | class/demographic/Enneagram labels did not change response receipt |
| N5A prior history, no current access | `UNKNOWN_RECEIVABILITY` | 0 | `NO_CHANGE/NO_PROPOSAL` | two history refs did not create a practice or a response |
| N5B prior history, current witness | `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION` | 0 | `NO_CHANGE/NO_PROPOSAL` | outcome based on current access/response only; declared history refs empty |

For P1, the committed response row was read back from SQLite (`response` table) and its nested S35 receipt was revalidated with the sealed-record validator. The receipt contains no target proposals. The CAN011 decision and commit receipt both report `NO_CHANGE` / `NO_PROPOSAL`, and the store's `target_state` table remains empty. A named later consumer reads `STATE_ABSENT`, not a ghost target.

### Same-assertion faults

Both trials use the actual implementation source, not a test edit:

| Claim | Positive | Fault | Restore |
|---|---|---|---|
| Access witness gate | PASS | RED | PASS |
| Response witness gate | PASS | RED | PASS |

The access fault forces the valid access path to the typed empty branch; the response fault forces the valid response path to empty. The positive test is `test_p1_observed_immediate_positive_zero_proposals`. Source restoration is in a `finally` block. JUnit per phase is under `junit/faults/`.

### Refusals

21 source-bound cases all return `REFUSED` with zero target proposals, no target decision, `committed=false`, `no_ghost=true` and empty store tables:

- access: wrong actor, wrong event, wrong source hash, wrong nonempty scene, empty scene, missing scene, before-event time, after-as-of time, revoked field, revoked source set, invalid source namespace;
- response: wrong actor, wrong event, wrong source hash, before-access time, after-as-of time, revoked field, revoked source set, invalid response kind, invalid source namespace;
- contradictory context with no bound contradictory ref.

These are TEST_ONLY source-integrity refusals, not native DENY issuance. The bridge never converts an invalid witness into a positive or a target.

### Legacy path and no-new-grant checks

- `evaluate_response` with two distinct TEST_ONLY history refs still returns its legacy one-proposal `CREATE` behavior. This is preserved as an isolated legacy adapter and is not invoked by the S35 route.
- The S35 route with the same two history refs still returns zero proposals and `NO_CHANGE/NO_PROPOSAL`, even though the pipeline receives the history refs.
- Both production registries still contain zero entries. No native rule or grant is added.

## Source integrity of this return

`evidence/source_manifest.json` records:

- 14 files byte-identical to pinned C9R blobs (including `candidate/conditioning.py` `3a5c83ae...`, `candidate/target_rules.py` `c33fc2a6...`, and the three pinned native-guard files);
- 2 changed files: `candidate/pipeline.py` (additive S35 branch/abort/receipt integration) and `candidate/response_rules.py` (optional `s35_receipt` field with `None` default);
- 8 new files: `.gitignore`, `candidate/actor_access_response.py`, `s36_harness.py`, `run_s36_evidence.py`, three test modules and `tests/conftest.py`.

The original C9R path was not present in this sparse checkout and was not modified. All S36 work is under the assigned return directory.

## Limitations and not-claimed

- Every rule, witness, source hash and receipt here is TEST_ONLY. A source hash proves local integrity of a TEST_ONLY record, not issuer authenticity.
- No native actor, encounter, ADP010/ADP017/ADP019 receipt, CAN008 rule, CAN011 rule, target grant, Pyat source, C8 witness, C11 weld, C12 consumer or human subject was issued or used.
- No generative psychological RuleA, belief, emotion, motive, memory, trait, competence or durable practice is inferred. The positive is recognition of a separately witnessed, actor-owned present response only.
- No H1 acquired-practice claim. The two-history legacy CREATE behavior is preserved as legacy adapter behavior, not as S35 science and not as a target committed by the S35 route.
- No claim that objective tool availability, B's action, class labels or historical acts produce uptake.
- No production installation, no native promotion, no cold replay, no power-loss durability, no external consumer beyond the pinned C9R path and local SQLite store, and no review/adoption by another owner.
- No M35, language, controller or PRE-MAIN work.

## Return files

1. `00_RETURN.md` — this return.
2. `candidate/actor_access_response.py` — S35 TEST_ONLY access/response selector and receipt.
3. `candidate/pipeline.py` — isolated additive pipeline integration.
4. `candidate/response_rules.py` — additive optional `s35_receipt` field.
5. `candidate/` remaining files and `runtime/native/rawlsing_next/` — byte-exact pinned C9R candidates/native guard.
6. `tests/` — 39 focused tests, including empty/missing access-scene and empty-event-scene regression.
7. `s36_harness.py`, `run_s36_evidence.py` — shared TEST_ONLY fixtures and evidence generator.
8. `evidence/` and `junit/` — actual execution evidence.
9. `logs/` — test and fault logs.

**Terminal:** `S36_TEST_ONLY_ACTOR_ACCESS_RESPONSE_BRIDGE_IMPLEMENTED__TESTS_39_OF_39__SCENE_BINDING_ORACLE_3_OF_3__ZERO_TARGET_PROPOSALS__CAN011_NO_CHANGE_NO_PROPOSAL__NATIVE_SCIENCE_AND_SOURCE_GRANTS_HOLD`. Final commit and remote branch HEAD SHA are verified after push with `git rev-parse HEAD` and `git ls-remote origin refs/heads/agent/rabochii-sorok-20261024-s36-actor-access-response-r1`; the exact SHA is reported in the final handback.
