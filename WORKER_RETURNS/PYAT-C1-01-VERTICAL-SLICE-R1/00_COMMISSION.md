# PYAT C1-01 — EXACT AT07 VERTICAL SLICE IMPLEMENTATION — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser/GitHub implementation worker, GPT-5.6 Sol High

Branch:
`agent/rabochii-pyat-hq130-c1-01-vertical-slice-r1`

Exact base:
`171200320b4acdbb8ba32106a992d76fa8ac7d8a`

C1-00 independent disposition at that base:
`APPROVE_AT_DECLARED_GRAIN`

This commission is the separate HQ implementation freeze required after C1-00 approval.

## Frozen contract/oracle authority

The following exact artifacts are binding and may not be reinterpreted by implementation:

- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
  blob `0abe15f7e7365832fdd1dcfab45d2e831774f99a`
- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
  blob `3ea3a5938c72e00bb35593f607e1bf33299085fc`
- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_products.json`
  blob `e29e1d5d99fcb14331b45297f32491d91711f0f2`
- `WORKER_RETURNS/PYAT-C1-00-R4-INDEPENDENT-REREVIEW-R1/04_FINAL_DISPOSITION.json`
  blob `25fbcca1862dfe2133bb35d6f8b9ad0c0bf5303a`

Exact owner surfaces at the frozen base:

- `rawlsing_next/pre553_empirical_query.py`
  blob `03facecf70890bfd13b80418620d274cbcd69d02`
- `rawlsing_next/source_backed_positioned_subject_possibility.py`
  blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7`
- `rawlsing_next/pre553_discovery_exact.py`
  blob `905f24d114419dbdd93879ad2bee5b59dd2f23af`
- `rawlsing_next/pre553_recursive_handoff.py`
  blob `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`

C1-01 itself is **AT07 vertical composition only**. Do not implement C1-02/C1-03.

## Exact write allowlist

You may create/edit only:

1. `rawlsing_next/pre553_analytical_composition.py`
2. `rawlsing_next/tests/test_pre553_analytical_composition.py`
3. `WORKER_RETURNS/PYAT-C1-01-VERTICAL-SLICE-R1/**`

Do not edit any existing producer, consumer, lifecycle, authority, discovery, recursive-handoff, physical-decoder, facade, workflow, court-spec or other test file.

If an existing owner must change for correctness, STOP and return the exact typed owner residual. Do not repair outside the allowlist.

## Mission

Build the smallest reusable C1 analytical composition that derives an actual `PossibilitySliceEvidence` from the current public empirical-query output and feeds that derived evidence into the actual public positioned-subject possibility consumer.

A wrapper that merely accepts a preconstructed final slice is a failure.

The implementation must preserve the exact accepted C1-00 identities and relation law rather than deriving new authority.

### Required public composition behavior

At minimum the new module must:

1. accept exact producer/consumer inputs sufficient to bind source, release, predicate/condition, target, risk/measure, authority and consumer rule/query;
2. execute the current public empirical-query producer rather than bypassing it with fixture-final counts;
3. verify the accepted exact value-bearing condition relation/witness before constructing the slice;
4. construct the current consumer's exact `PossibilitySliceEvidence` shape with the accepted noncircular evidence identity law;
5. set `raw_support` to the exact `EmpiricalFact.raw_denominator_support`, not target-cell numerator or a rounded quantity;
6. preserve exact source/release/target/condition/risk/measure/provenance determinants;
7. call `evaluate_positioned_subject_possibility(...)` with the derived evidence;
8. return a composition envelope that retains the producer result/evidence identity and consumer result without collapsing producer state.

Do not create learned/adjudicated structural claims. This is a competent direct empirical source-free fixture route.

## Required AT07 positive cases

Using the exact frozen source-free AT07 fixture, prove both directions:

Forward:
- condition `POSITION=P1`
- target `ANSWER`
- exact counts 54 yes / 6 no
- raw denominator 60
- exact forward evidence ref:
  `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`

Reverse:
- condition `ANSWER=yes`
- target `POSITION`
- exact counts 54 P1 / 8 P2
- raw denominator 62
- exact reverse evidence ref:
  `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`

The accepted slice projection schema hash is:
`c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`

The accepted query authority hash is:
`b59ef578314515268fa7b280a8480b4c95c80c9cfd831c39c2bfc4214b6fd767`

The accepted AT07 universe hash is:
`ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2`

The accepted release hash is:
`8afa807cc06a3a10e660d13bbd831f4f758ae829e835a454c62831bfd8f4d939`

## Mandatory hostile cases

The main test file must include hostile proof that fails closed or reidentifies correctly for:

- same conditioner semantic id but P1 subject paired to P2 producer leaf;
- changed exact condition value;
- changed pairing-ground-truth/witness;
- changed source or release;
- changed risk-set identity;
- changed measure kind/authority;
- different query conditions producing a different determinant/evidence identity;
- observed zero inside a nonzero supported denominator;
- zero support;
- incompatible source/release/risk/measure;
- unsupported authority scope.

The P1↔P2 value-relation hostile must fail before consumer invocation.

No float rounding may become semantic identity.

## Execution law

This is source-free only.

Do not use the user's Mac.
Do not open/materialize/decode raw survey files.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11 materialization.

If the worker has a lawful off-Mac source-free runtime, run the narrow test file plus only the owner tests required to prove no local regression and record exact environment/commands/counts.

If no lawful off-Mac execution surface is available, do not manufacture a PASS and do not broaden into infrastructure work. Return:
`PATCH_READY__SOURCE_FREE_EXECUTION_CAPABILITY_BLOCKED`
with exact unexecuted test command and patch identities.

## Required return

Under:
`WORKER_RETURNS/PYAT-C1-01-VERTICAL-SLICE-R1/**`

return:

- `00_RETURN.md`
- `01_IMPLEMENTATION_MANIFEST.json`
- `02_AT07_ASSERTION_MATRIX.json`
- `03_HOSTILE_CASE_MATRIX.json`
- `04_EXECUTION_RECEIPT.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_AT_IMPLEMENTED_SOURCE_FREE_GRAIN`
- `PATCH_READY__SOURCE_FREE_EXECUTION_CAPABILITY_BLOCKED`
- `CHANGES_REQUIRED_BY_EXISTING_OWNER`
- `BLOCKED_CONTRACT_COUNTEREXAMPLE`

Do not start C1-02.

Terminal:
`C1_01_VERTICAL_SLICE_RETURNED__HQ_ADJUDICATION_REQUIRED`
