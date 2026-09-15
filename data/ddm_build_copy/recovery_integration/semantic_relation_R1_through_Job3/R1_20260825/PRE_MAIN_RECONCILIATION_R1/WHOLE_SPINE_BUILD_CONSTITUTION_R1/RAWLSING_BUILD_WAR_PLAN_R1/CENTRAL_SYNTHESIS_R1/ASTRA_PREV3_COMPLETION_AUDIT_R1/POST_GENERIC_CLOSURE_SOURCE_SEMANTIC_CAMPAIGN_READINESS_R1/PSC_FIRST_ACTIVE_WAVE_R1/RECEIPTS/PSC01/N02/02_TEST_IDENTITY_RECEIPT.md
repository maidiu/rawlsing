# N02 test identity receipt

Registry command: `python -m pytest -q tests/test_prev3_psc_w1_n02_routing_applicability_ledger_r1.py`

At exact commission tip `d56613cbcbe4d2655cd4e5f28f70d697a13d8a5a`, the registered test path was not present (GitHub content lookup returned 404), so no PASS is claimed for that court.

Bounded replay validator committed at `ARTIFACTS/PSC01/N02/replay/validate_positive_subset.py`; its scope is only conservation of the 2,104 positively proved exact-current bindings and it does not establish the full 18,276-row join.
