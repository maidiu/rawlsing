# A41 - executable whole-estate original35 / F1-F8 / N11 acceptance assembly

**Role:** bounded whole-estate evidence and executable integration builder. NOT the
competent N11 scientific acceptance issuer, semantic owner or HQ. **This return
builds the acceptance MACHINE and emits N11 CANDIDATE products at NOT_READY. It
does not self-adopt N11, wake N12, or issue any source/FF/model/actor permission.**

Branch `agent/rabochii-pyat-r41-a41-n11-whole-estate-assembly-r1`, created from the
exact sealed startup `c4934fd71120d37a4d06f7c830891e6e97fe4ecf` (HEAD verified).

## What actually runs

`python3 -m a41.cli assemble` ingests the frozen independent expected scope plus a
preimage-verified receipt bank and emits the three named N11 products:

- `f1_f8_acceptance_matrix.json` - 283 rows (280 per-wave F-axis + 3 global)
- `estate_acceptance_manifest.json` - the full 1,890-cell manifest, 35 waves, 151
  register rows, 101 ledger rows, the 151<->101 crosswalk, global relations and the
  finite blocker ledger
- `final_maturity_adjudication.md` - the human-readable candidate adjudication

`python3 -m a41.cli replay` assembles twice and requires byte-identical artifacts.

## Independent expected scope frozen first

`evidence/expected_scope_frozen.json` is built by `scripts/freeze_expected_scope.py`
from ONLY the four declared HQ estate documents, at their exact Git preimages:

| document | blob | role |
|---|---|---|
| ESTATE_35X_REQUIREMENTS_MATRIX.json | `2ad9a001…` | 35 x 54 = 1,890 scoped cells |
| GLOBAL_WORK_REGISTER.json | `7fb47b5d…` | 151 inherited obligation classes |
| TASK_LEDGER_101_MACHINE.json | `45be0f82…` | 101 current function tasks |
| GLOBAL_F6_F7_F8_RELATION_SCOPE_MATRIX.json | `88705457…` | global F6/F7/F8 obligations |

The scope freeze records `frozen_before_assessor_logic: true`. The assessor reads the
frozen scope read-only and never constructs its own expected universe.

## Real evidence ingested (not fake fixture PASS metadata)

Nine receipts, each anchored to real Git commits and re-hashed on ingestion:

| receipt | occupancy kind | origin |
|---|---|---|
| O35B-ORIGINAL35-ACCOUNTING | DOCUMENTARY_IDENTITY_RECONCILIATION | `c714af26` |
| O35B-C11-REPLAY-BLOCKER | DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER | `c714af26` |
| O35B-P1-M1-NATIVE-BINDING | SOURCEFREE_LOCAL_POSITIVE | `c714af26` |
| AS2B-LITS-HISTORICAL-POSITIVE | HISTORICAL_SCOPE_POSITIVE | `c714af26` |
| E04L-SOURCEFREE-READTHROUGH | SOURCEFREE_LOCAL_POSITIVE | `daf0d085` |
| F6P-SOURCEFREE-PARTIAL-BOUND | SOURCEFREE_LOCAL_POSITIVE | `912467aa` |
| I2-R39I-INDEPENDENT-COURT | SOURCEFREE_LOCAL_POSITIVE | `05c21c54` |
| WV1-SOURCEFREE-WORLD-CONSUMPTION | SOURCEFREE_LOCAL_POSITIVE | `23989684` |
| EE1-SOURCEFREE-TEMPORAL-NULL | EMPIRICAL_NULL_WITH_CAUSE | `affe600d` |

Occupancy kinds are non-substitutable. SOURCEFREE_LOCAL_PASS != ORIGINAL_ESTATE_OCCUPANCY.

## The exact held accounting (whole declared estate)

1,890 expected cells (35 x 54 = 30 source-native + 16 EE + 8 F):

| grade | cells |
|---|---|
| original measured occupancy | 0 |
| historical scope only | 2 |
| sourcefree local positive (not original occupancy) | 2 |
| accounted identity only (not occupied) | 70 |
| development blocker, narrow owner (C11, S19) | 35 |
| missing expected original science (not inapplicable) | 1,781 |
| **total** | **1,890** |

Global F6/F7/F8: 3 open, 0 closed; per-wave F-axis cells explicitly cannot close them.

**N11 state: N11_NOT_READY** with 1,784 finite blockers (1,781 missing expected cells
+ 3 open global relations). This is not a document containing 35 HOLDs: it is a
machine account of every cell, its identity, its frozen expected U/E_pre, the real
evidence that touches it (if any) and its exact remaining owner.

## Preserved boundaries

- Original35 U/E_pre remains unissued: eligible operation count is null with cause
  (never a fake zero); original35 PERMITTED = 0.
- The exact LiTS C11 missing-preimage issue is preserved as a narrow-owner blocker;
  the native validator is not bypassed and no source warrant is inferred.
- F6P remains a bounded TEST_ONLY F6 client; it does not join to original E04.
- E41/W41/P41 are concurrent and NOT accepted; their native output contracts are
  reserved in `e41_w41_p41_integration.json`.

## Falsifiers (same pass, shared proof gate)

Four claim-edge witnesses, all baseline PASS -> TARGET_ASSERTION_FAILED -> restored:

- delete the accounting receipt -> the 70 identity cells vanish (RED)
- promote a sourcefree receipt to original occupancy -> typed refusal (RED)
- drop the F6 unknown mass -> manifest loses the uncovered mass (RED)
- forge a consumer ref -> typed refusal (RED)

Plus in-suite controls: missing eligible receipt detected by the full-estate
assertion; stale currentness refused; archive/current consistency enforced; cold
replay identical.
