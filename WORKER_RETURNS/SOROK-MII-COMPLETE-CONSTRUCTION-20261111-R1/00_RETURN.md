# SOROK MII complete construction — sourcefree checkpoint

**Status:** `SOURCEFREE_ENGINEERING_COMPLETE__INDEPENDENT_RECEIVING_PENDING`
**Branch:** `agent/sorok-mii-complete-construction-r1`
**Start:** `9366b42a61a383808071106d70aa1255a769390a`
**Final sourcefree checkpoint commit:** reported in the HQ response after this return commit.

## What is implemented

- **E1:** P6/P5/P4 committed observations and exact speech remain the source;
  no second world. Source/root/branch checks remain in `read_house` and the
  existing P4/P6 path; committed house source denial refuses and restores
  through the real reader.
- **E2:** viewer-specific `presentation_conditions.observer` gates glance and
  close availability. Per-object `presentation_conditions.objects` can qualify
  one feature/object separately. Occlusion removes optional detail while
  preserving the object's existence/affordance. `look` refuses close detail
  without the qualified viewer source. House, gallery and symbolic fixtures are
  supported.
- **E3:** versioned `exposures[]` records availability, the full eligible
  `candidates` map, the actually `offered` detail, `selected`, rendered event
  IDs, selection basis, prior exposure, scope, request ID and policy. Entries
  are append-only in normal operation; duplicate requests do not add a second
  exposure. Legacy/corrupt/scope-mismatched/hash-tampered profiles reset to
  neutral without touching world history. Actual P2 fork and interrupted
  exposure-write replay are exercised.
- **E4:** recognition is rebuilt from committed user inspections and exact
  object evidence. Persisted `recognized` data is not trusted; forged rows do
  not render as earned. User-taught and corrected labels are separate acquired
  knowledge.
- **E5:** neutral is the default and performs no implicit update. Explicit
  adaptive mode updates only performed `look` targets, distinguishes previously
  offered from independently chosen targets, keeps competing hypotheses,
  applies simple stale-evidence decay, and supports correction/stop/reset.
- **E6:** `SOROK_MII_SURFACE@1` separates mandatory event lines from at most one
  optional detail, records omitted available details, and preserves exact
  accessible speech. No extra model call is added.
- **E7:** existing P4/P6 ingress remains the action path for `say`, `go`, `look`,
  `attend`, `wait`, and outward operations. MII changes only presentation and
  derivative user state.
- **E8:** `mii-status`, `mii-export`, `mii-reset`, `mii-stop-learning`,
  `mii-enable-learning`, `mii-learn-label`, `mii-correct-label`, and
  `mii-correct-attention` are available. Reset/export/control operations do not
  rewrite the P4 ledger or actor state.
- **E9:** `measure_mii.py` produced `measurements.json`: cold CLI n=13,
  p50 6.340 s, p95 9.688 s, max 12.873 s; warm import n=5, p50 3.101 s,
  p95 3.106 s, max 7.629 s; provider calls/tokens 0; peak child RSS 50.730 MiB;
  state 1,600,669 bytes; gallery fixture look returned
  `the stamped brass hinge`. Cold replay failures: 0. Component warm p50:
  initialization 3.095 s, availability 0.000042 s, ledger 0.001862 s,
  recognition/update 0.000168 s, composition 0.002021 s. Raw component
  samples are in `measurements.json`; cold CLI component timing is explicitly
  not separated because each command is a new process.
- **E10:** runnable P6 path, this README, versioned schemas, controls, tests and
  measurement artifact are included.

## Executed tests

```text
test_mii.py                         17 passed in 514.29s
test_house.py                        8 passed in 447.19s
test_actor_initiative.py + scene     7 passed in 207.30s
test_actor_initiative_hostile.py    20 passed in 556.50s
test_recognition_surface.py          5 passed in 253.49s
test_gaze_proof.py                   1 passed in 88.65s
```

The early-review and independent R2 regressions are corrected:
- foreign `observer=B` now yields no optional detail for user `U`;
- forged persisted recognition no longer renders as `COMMITTED_INSPECTION`;
- an omitted available target gets independent weight `2`; the previously
  offered target gets weight `1`;
- durable exposure records preserve full `candidates` separately from the
  actually `offered`/`selected` detail.

## Original 44 mapping

PASS_SCOPED unless marked otherwise. Evidence abbreviations: `MII` =
`test_mii.py`; `HOUSE` = `test_house.py`; `GAZE` = `test_gaze_proof.py`;
`REC` = `test_recognition_surface.py`; `MIII` = actor initiative tests.

| ID | Evidence |
|---|---|
| O01 | GAZE same-world counterfactual |
| O02 | HOUSE exact speech preservation |
| O03 | HOUSE private-key exclusion; MIII actor isolation |
| O04 | MII occlusion/positive detail; REC committed evidence |
| O05 | MII controls/ledger unchanged; GAZE snapshot invariant |
| O06 | HOUSE silent interval; MIII actor action independence |
| P01 | GAZE differing attention histories |
| P02 | MII occlusion/restore |
| P03 | MII omitted available look |
| P04 | REC plain category before evidence |
| P05 | REC committed inspection; MII gallery hinge |
| P06 | MII taught-label acquired confidence |
| P07 | MII adaptive hypothesis vs explicit `look` task |
| P08 | MII surface budget/omitted list |
| P09 | MII omitted available look |
| G01 | MII offered=1 vs independent=2 |
| G02 | MII only performed `look` updates; unavailable/unshown no update |
| G03 | MII correct-attention correction |
| G04 | GAZE/MII bounded optional selection |
| G05 | MII surface budget; no corrective detail insertion |
| G06 | MII omitted available look; existing ingress |
| G07 | MII prior-offered vs independent evidence |
| G08 | MII competing adaptive hypotheses |
| M01 | MII symbolic fixture: watch identified; no status/desire/vulgar/admirable inference |
| M02 | MII symbolic fixture: icon detail; no religious-belief assertion |
| M03 | MII neutral bench/mug practical detail |
| M04 | MII user-derivative isolation: same actor movement with/without false user label |
| M05 | MII user-derivative isolation: Nadia action unchanged by private user model |
| M06 | GAZE/MII hidden history not used for salience |
| N01 | MII derivative profile separate; no essence fields |
| N02 | MII controls leave P4/actor ledger unchanged |
| N03 | GAZE same committed snapshot under differing gaze |
| N04 | MII neutral default; no update without explicit enable |
| N05 | MII controls/export/reset; world history unchanged |
| N06 | MII export/reset/delete derivative controls |
| N07 | MII corrupt/reset profile leaves neutral encounter usable |
| N08 | MII has no retention-optimization selection path |
| N09 | MII no model call; surface only owner facts |
| N10 | MII actual P2 fork: parent/child derivative scopes isolated; no cross-branch exposure reuse |
| T01 | MII measurement provider calls 0; warm p50 2.929 s |
| T02 | MII cold profile reopen/exposure hash; actual P2 fork scope replay |
| T03 | MII duplicate request/exposure immutability; interrupted write replay |
| T04 | MII taught label vs earned inspection |
| T05 | MII surface/exposure provenance |

## Limitations / remaining authority

- **NOT_RUN:** native science, live model/provider, human validity, protected
  merge, production privacy approval, independent receiving.
- The sourcefree engineering scope is complete; the remaining gates are
  independent receiving and the separately authorized native/human/production
  authorities. No known sourcefree behavioral gap is represented as a PASS
  by absence.

## PROGRAMMA_DELTA

- **Identity:** sourcefree MII construction on `9366b42a…`; implementation
  checkpoint committed after this return.
- **Function:** viewer-qualified finite surface, exposure ledger, earned/taught
  recognition, neutral/adaptive derivative controls, house and gallery fixtures.
- **Verdict:** `E1_E10_SOURCEFREE_ENGINEERING_COMPLETE__44_EXECUTED_EVIDENCE__INDEPENDENT_RECEIVING_PENDING`.
- **Limits:** sourcefree only; no native/science/human/production/protected claim.
