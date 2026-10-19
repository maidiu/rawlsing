# W41 native replay

Run from the branch root with Python 3.11, pytest and pandas. No raw source, package installation, network or producer edit is needed.

```bash
python3 WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/reconstruct_owners.py --verify
python3 WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/capture_products.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/tests/test_native_world.py WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/owners/wv1/native_courts/test_product.py WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/owners/f6p/tests
PYTHONPATH=WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/owners/native python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/owners/ee1/tests
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/tests/test_native_world.py.proof.json --root . --receipt /tmp/w41-proof.json
python3 WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/reconstruct_owners.py --verify
```

Run EE1 in its own process. Its accepted bootstrap intentionally refuses a WV1 bootstrap, even when both T35 owner blobs are identical. The exploratory combined-process run retained in `evidence/native_final.xml` has six such assertion failures; it is not reported as a passing suite. The separate EE1 run has 33 passes. The other 94 test cases in the combined run passed, including all 25 original W41 tests plus one later temporal replay regression, 37 original E04 tests and 32 F6P tests.

`native_owners.tar.gz` is the exact immutable dependency closure, with Git commit/path/blob/SHA256 identities in `owner_pins.json`. It contains sourcefree code, qualified retained constructor material, hash-only GT2 reference closure and test fixtures, never raw survey responses. Unpack before invoking the shared gate; its faults act on actual unpacked producer files. Reconstruct does not overwrite existing files, so mutations cannot disappear during testing. Explicit `--verify` checks restoration.

`current_historical_asof_world_consumer_receipts.json` contains the actual 84 original-client views, two retained context reads, native independent field reads, all eight F6 evidence cases and nine temporal method outcomes. The 84 views are synthetic test coverage, not source-estate occupancy. `capture_products.validate` rejects omission of any declared family/mode/budget/case or native positive. No issued original U/E_pre is inferred from this output register.

Six exact dependency controls are in `tests/test_native_world.py.proof.json`. Their named consumer assertions went RED after native FF, F6M, T35, selected-release, M4 and EE1 mutations; the gate restored the files. These are author proofs, not independent scientific acceptance. Source-qualified F6→N9 transport and broader original E04 world purposes remain held.
