# Z04 CURRENT TEST RECEIPT

Tested commit:
`d70ee2753392b5418a29817b84d29b63d5986fbb`

GitHub Actions run:
`33203260325`

Job:
`98957764746`

Runner:
`ubuntu-latest`

Python:
`3.11`

Command:

`python -m pytest -q data/ddm_build_copy/test_z04_denominator_projection_role_closure.py data/ddm_build_copy/test_w06_v552j_join.py data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py data/ddm_build_copy/tests/test_postg5_v550_v551_response_semantics_contract.py rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`

Final result:

`71 passed in 2.19s`

Covered hostile obligations:

1. independent joint denominator survives distinct from per-component denominator;
2. context-only component remains denominator-null rather than receiving a relation denominator;
3. denominator-vector substitution fails closed even if envelope hash is recomputed;
4. relation-component authority-role erasure fails before ALLOW;
5. authority-role erasure is rejected again by actual V553 consumer even after a valid rehash;
6. V552 projection output is invariant to contradictory response labels/codes/order/raw-intensity metadata when V551 canonical signed projection is held fixed;
7. missing/invalid V551 canonical signed projection blocks instead of being reconstructed;
8. existing V552J/V553 consumer contract remains green;
9. existing V550/V551 response-semantics contract remains green;
10. existing M4 role/permission/cardinality/order regression suite remains green.

Prior run:
- run `33203162016`: 66 passed / 5 failed because the old V553 fixture constructed a pre-Z04 row without the now-required conservation envelope.
- The fixture was updated to a valid current envelope.
- No production guard was removed or weakened.

The temporary branch-only CI workflow and trigger file are deleted in the final seal.
