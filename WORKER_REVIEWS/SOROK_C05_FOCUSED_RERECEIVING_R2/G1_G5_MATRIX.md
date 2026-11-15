# C05 focused R2 — scoped G1–G5 matrix

**Verdict:** `ACCEPT_SCOPED_SOURCEFREE_C05_OPERATION_CUSTODY`
**Accepted source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Frozen final report:** `1cf1a37113cb7a48137734648b523a0a6deccd92`
**Frozen start:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Original review:** `b5b810cdd7b51b20efcc42d4ce76960f9e410706`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`

| Gate | Status | Evidence | Scoped limit |
|---|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | final report and implementation source pins exact; only product change from `bc45f699a` is the one-line `promote_relation` state-machine input; `supporting_actor.py` unchanged `98cb4ce...`; no owner/transaction/schema/ledger/actor change; metadata-only commits after code; product read-only | sourcefree mechanical repair only; no native ADP-015/C4 owner |
| G2 build/actual first consumer | `PASS_FOCUSED_CLOSURE_AND_NORMAL` | focused R2 test 1 passed; original C05 5, C01 6, C04 identity 6, C04 custody 12, P2 owner 5 passed; byte-identical 89/89 normal/negative/cold probe; independent closure probe 12/12; real P2 owner event and later consumer preserved | event content inherited sourcefree P2/S45/S39; not G2 language or autonomous selection |
| G3 falsification | `PASS_DEFECT_CLOSED` | byte-identical original defect probe at corrected source: exit 2 expected, `RELATION_PROMOTION_NOT_DEEPER`, no write, zero episode/change/head/world/perception/checkpoint delta, relation `QUALIFIED`, history/context byte-exact, original retry `UNCHANGED`; base RED preserved from `b5b810c` and author receipt semantically matches | caller exposure/append boundaries remain; no owner signature or perception proof |
| G4 preservation/restore/cold | `PASS_PRESERVATION_SCOPED` | earlier event contexts, normal promotion depth 1→2, partial exposure, private boundaries, later real event, change/head sever-restore and fresh-process cold all remain green in the byte-identical 89-check probe; C01/C04/P2 suites pass; refusal leaves C12 verify ok | concurrency, branch-fork replay, depth >2 and whole-life C05 unproved/unobserved |
| G5 independent receiving | `ACCEPT_SCOPED_SOURCEFREE_C05_OPERATION_CUSTODY` | exact in-scope defect closed at the same public writer path with zero write; no material regression observed; one final verdict | operation/custody of caller-authorized sourcefree illustrative relations only; original full C05 actor qualification unproved |

## Scope that is actually accepted

- caller-authorized sourcefree illustrative relation value/change/exposure,
- both relation parties mandatory in caller exposure,
- dated append-only continuity/history, finite depth 1→2, qualified custody
  holds, and the existing later P2 event consumer,
- bounded mechanical operation/custody only.

## Scope that is not accepted

- an owner receipt qualifying relation knowledge (none exists),
- relation `PERCEIVED` actor truth (reader remains `DATED_EXPOSURE_ONLY`),
- coherent append authority as owner authentication (self-hash, not a signature),
- native ADP-015/C4 relation authority, autonomy, psychology, generated
  language, G2 selection, complete J1, J2, D04/D05, human/science/source
  rights, protected merge, fork/concurrency uniqueness, depth >2, or whole C05
  person life.
