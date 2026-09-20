# FIABC-R35-I02 — Test / Qualification Protocol

## Browser-only commission status

The tests were authored on the worker branch but not executed during this commission. No local source carrier was opened and no measured P2X was run.

## Focused qualification command

On an authorized repository execution surface:

```bash
python -m unittest discover -s tests -p 'test_fiabc_derivative_parentage.py'
```

Expected result: all tests PASS.

## Required hostile dispositions

| Case | Required result |
|---|---|
| derivative payload asserts canonical SHA but has no external bundle | reject |
| WVS structural JSON is changed and its own self-hash recomputed | reject |
| row/variable geometry is correct but source receipt closes to wrong ancestor | reject |
| reader/config differs from frozen expected config | reject |
| compatibility-decoded persisted copy lacks derivation receipt | reject |
| old R5 root is supplied under current LiTS-A requirements | reject |
| scope/currentness determinants drift | reject |

## Positive controls

The suite also requires:

- a WVS7 source receipt + structural-preimage receipt + bundle to close under exact producer/config/currentness/ownership;
- a LiTS-I source receipt + R5 derivative receipt + bundle to close under exact carrier/root/current runtime determinants.

## Integration qualification

After fan-in with sibling R35 work, rerun the focused test and the R35 hostile court. Do not treat this test as source certification or I05 semantic parity.

The LiTS-A live execution path additionally requires qualification to provide the actual external first-build parentage bundle and its frozen derivative receipt identity. Absence is an expected hard stop, not a test workaround.

## Prohibited qualification shortcuts

Do not:

- mint a new receipt from the preserved R5 root merely because the root is internally self-consistent;
- accept WVS structural JSON because its `structural_input_identity` recomputes;
- compare only row/column counts;
- treat an asserted `source_sha256` as raw ancestry;
- drop the compatibility-only authority-status tag;
- run measured P2X as part of this worker's qualification.
