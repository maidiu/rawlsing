# Selected-world defect readback and bounded repair

## Original exact failure

Court:

```bash
cd <ed34944e exact tree>
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_r3_s02_seam_witness.py
```

Actual result:

```text
......................F....
1 failed, 26 passed
```

Failure:

```text
test_s00c_change_source_owned_synthetic_numeric_values_changes_result
KeyError: 'exact_probabilities'
```

The selected-world 24-test court at the same exact cut was separately green:

```text
24 passed
```

The two positives do not erase the seam RED.

## Producing field / consumer mismatch

The failing test constructs the sourcefree native 2x2 joint law:

```text
(Q86B, Q86A) cells: (0,0)=3, (0,1)=1, (1,0)=1, (1,1)=3
```

It then changes the Q86B=1 channel numerators to 2,2 and the saved step cells to
2,2, but **retains the original selected-world contract**, whose partition was
derived from the original cells 1,3. The consumer returns:

```text
{'status': 'REFUSED', 'reason': 'PRODUCER_VALUE_IDENTITY_MISMATCH',
 'scientific_claim_grade': 'SOURCE_FREE_SYNTHETIC'}
```

so `exact_probabilities` is absent and the test raises `KeyError`.

The mismatch is not a producer hole. It is a **selected-world contract rebind
gap**: the numeric source-owned values changed, but the saved contract still
binds the old source/risk/partition identity. The validation correctly refuses
to represent a changed numeric law under the old selected-world identity.

## Bounded sourcefree repair

`sourcefree_adapter/selected_world_repair.py` makes the contract part of the
source value identity:

- `build_source_owned_joint(cells)` binds contract hash to the exact 2x2 cells;
- `rebind_source_owned_joint(world, cells)` creates a **new** contract for the
  changed source-owned values;
- `stale_mutation_with_old_contract()` retains the old contract with changed
  channels and is refused with `SOURCE_VALUE_CONTRACT_MISMATCH`;
- zero denominator returns `ZERO_SUPPORT`; missing step returns `NO_SUPPORT`;
- cold restore verifies contract and receipt hashes; tampered payload is refused;
- live channel mutation/restoration is a named red/green fault negative.

Actual repair court:

```bash
cd WORKER_RETURNS/PYAT-P41-R08-RECOVERY
PYTHONPATH=sourcefree_adapter:../.. python3 -m pytest -q \
  tests/test_selected_world_repair.py
```

```text
..... 5 passed
```

Key assertions:

| Path | Actual |
|---|---|
| Original source-owned cells 3,1,1,3 | `P_Q86A_given_Q86B_1` = **3/4** |
| Rebound source-owned cells 3,1,2,2 | same step = **1/2** |
| Same denominator | 4 in both |
| Contract hash | changes with the source cells |
| Old contract + changed channels | `REFUSED / SOURCE_VALUE_CONTRACT_MISMATCH` |
| Zero denominator | `ZERO_SUPPORT / ZERO_DENOMINATOR_ABSTENTION` |
| Missing step | `NO_SUPPORT / NO_MATCHING_CHANNEL` |
| Cold restore | identical exact read |
| Tampered cold payload | `ValueError: RESTORED_CONTENT_HASH_MISMATCH` |
| Live channel tamper | refused; original world restored green |

## Interpretation

The original failing receipt is preserved, not erased. The seam was genuinely
red because the selected-world identity was not rebound when source-owned numeric
values changed. The bounded repair proves the missing transition:

```text
source-owned numeric value change
  -> new selected-world contract
  -> changed exact conditional output
```

It does **not** prove original N9 selection, real source values, production
consumer adoption or scientific equivalence. The original S3 contract and seam
modules remain historical branch material; no current production file was
overwritten.
