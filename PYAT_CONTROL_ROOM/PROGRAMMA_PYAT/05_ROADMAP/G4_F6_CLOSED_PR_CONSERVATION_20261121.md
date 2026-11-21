# F6 and Q017–Q020 closed-PR conservation

DeepSeek source inspection against PRE-MAIN `fbc208040` and the existing G4 records found the following scoped succession in isolated candidate `dd1f5a45830c09ac21f577aa97351d639be1af0d`.

| Closed PR | Exact head | Disposition |
| --- | --- | --- |
| #1219 | `acb7fa6a58af2b62774a34b40c59bcdabf4fd9c1` | Q018 finite-frame bounds and compatibility reader conserved by the replay-hardened successor. |
| #1223 | `429cfc5f47e04a82302860f6f33ad48e53daf45d` | Q017 and Q018 conserved. Q019 intentionally retired by #1231. |
| #1224 | `1330328ccaa481681d18d2cc6c173cc47fe3fefe` | Q020 issued-interval consumer survives in #1225 and the isolated successor at blob `172643f6`. |
| #1225 | `358d558086946fb0e7a8681e8813ccd10fecfc38` | Hardened Q018 and Q020 code and tests conserved without the retired Q019 coupling. |
| #1231 | `b29aa8d4a569d5fc579bdd87f1b1ff03204926b4` | Q019 retirement, Q016 MI reuse and Q015 receipt promotion guard remain tracked. |

The CORR-006/007 note in the successor queue asserting that Q020 code and tests are absent is stale at this cut. Its tree contains the Q020 source and tests and the runner lists RMT-Q020. The REMONT queue owner owns the source-note correction. Q019 retirement remains operative. This is source conservation evidence. Independent execution, protected adoption and original-source rights remain held.
