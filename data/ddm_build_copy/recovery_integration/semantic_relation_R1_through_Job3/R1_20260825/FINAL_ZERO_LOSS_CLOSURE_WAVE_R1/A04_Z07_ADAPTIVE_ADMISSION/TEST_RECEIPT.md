# A04 Z07 — REPOSITORY-NATIVE TEST RECEIPT

Status:
`PASS`

Tested current-line commit:
`d567cabefad079ac01b61c8613d718718d4ca769`

GitHub Actions run:
`33208286874`

Job:
`98974884085`

Runner:
`ubuntu-latest`

Python:
`3.11`

Command:

`python -m pytest -q rawlsing_next/tests/test_pre553_discovery_adaptive.py rawlsing_next/tests/test_pre553_discovery_adaptive_admission.py rawlsing_next/tests/test_pre553_discovery_exact.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py rawlsing_next/tests/test_pre553_empirical_query.py`

Result:

`63 passed in 1.80s`

Executed acceptance coverage:

1. budget truncation -> typed partial completeness + exact unvisited refs;
2. interruption -> typed partial completeness + exact unvisited refs;
3. result-driven widening only after complete sealed unit;
4. explicit incomplete/unsealed outcome rejection;
5. partial valid-empty result cannot create a global empirical negative;
6. deterministic schedule under reordered storage input;
7. canonical checkpoint round-trip and restart without silent skip;
8. one-shot vs bounded interrupted/resumed eventual completion equivalence;
9. deterministic replay -> `REPLAY_VERIFIED`;
10. nondeterministic evaluator -> `NONDETERMINISTIC_REPLAY`;
11. policy-version drift invalidates old checkpoint;
12. same-version policy-content drift invalidates old checkpoint;
13. determinant-state drift invalidates old checkpoint;
14. exact mode is rejected by adaptive service;
15. exact I05 regression suite passes on unchanged blob;
16. current empirical authority/object/query closure surfaces pass.

Exact Z07 production blob tested:
`58e32770381fa8d901701d6a2c676f28261aa3e3`

Exact Z07 committed hostile test blob tested:
`fb7d00ad0ee2690dede339dd029476b64158824b`

A04 admission-only hostile blob:
`e67799c337e0b2ebe838707781bbdee3001be934`

Exact I05 blob at tested commit:
`b2b99460cc5991bc26aa2ffe5bda129b408fc197`

No I05 mutation occurred.

The temporary A04 GitHub Actions workflow is deleted in the final documentary seal.
