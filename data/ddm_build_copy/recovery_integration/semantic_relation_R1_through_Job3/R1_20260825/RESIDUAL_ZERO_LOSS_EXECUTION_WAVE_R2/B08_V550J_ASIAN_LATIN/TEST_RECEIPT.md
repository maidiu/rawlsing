# B08 — TEST / SERIALIZATION RECEIPT

Status:
`PASS__BLOCKED_SERIALIZATION_FAILS_CLOSED`

Tested commit:
`e369754bb6a1f7f407ae43a34d3d9e496943518c`

GitHub Actions run:
`33217005922`

Job:
`99002782555`

Runner:
`ubuntu-latest`

Python:
`3.11`

Pytest command:

`python -m pytest -q data/ddm_build_copy/tests/test_v550j_b08_asian_latin_authority.py data/ddm_build_copy/test_v550j_w03_authority.py`

Result:

`17 passed in 2.58s`

Standalone validator:

`python data/ddm_build_copy/validate_v550j_b08_source_family_authority.py`

Result:

`PASS_BLOCKED_SERIALIZATION_FAILS_CLOSED`

Validator receipt:

- Asian SHA-256: `284b5a75cf165a948372ee5d58caf5571ddeea5406f048629cfea85ead58d9bb`
- Latin SHA-256: `8dd949afedd14fb5131d0bb9725ae3bc4749f3b3d8d74cecf84fefd3f6bc118d`
- R14 evidence ledger SHA-256: `ff8f59c60c7208eb1f9e5866451ec63d5c59b14b0acb8528cf65b5e4a6c22176`
- R14 evidence rows: `73`
- product executable registries: `0`
- denominator disposition complete: `false`

Hostiles prove:

1. Asian W6 cannot enter the exact W1/W4/W5 scope.
2. Latin scope remains exactly 1995/2011/2024.
3. 2,499/15,990 aggregate recovery counts cannot become exact source-family row authority.
4. missing routing/member-applicability cannot become product execution authority.
5. bounded Section85 canaries remain bounded and cannot become product registries.
6. Archive08/V3/architecture promotion remains false.
7. false product-executable status is rejected.
8. the existing W03 bounded V550J authority regression remains green.

Infrastructure-only failed attempts:

- run `33216911388`: collection stopped on missing `dotenv`;
- run `33216962554`: collection stopped on missing `sklearn`.

Neither run reached semantic execution. The final runner installed those existing test dependencies and then passed the unchanged test command.

The temporary GitHub Actions workflow is removed in the final seal.
