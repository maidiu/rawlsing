# Court 11 — Independent CI Evidence Audit

## Result

**PASS for the tested source-free tree.**

The CI evidence is genuine and was inspected from GitHub Actions jobs/logs rather than worker-authored markdown.

## Focused run

Run:

`35826661112`

Job:

`107069779873`

Job name:

`governed-court`

Conclusion:

`success`

Protocol self-test log:

`20 passed in 0.08s`

Focused governed court:

`80 passed in 39.12s`

Receipt artifact:

- name `rabochii-court-receipt-35826661112`
- artifact id `10734634330`

Focused court spec targets exactly:

- `test_fiabc_lits_astra_substantive_parity.py`
- `test_fiabc_lits_i_i03_operation_authority.py`
- `test_fiabc_w3_i04_runtime_packaging_rebind.py`
- `test_fiabc_final_oracle_freeze_producers.py`

## Broad run

Run:

`35826798791`

Job:

`107070206829`

Conclusion:

`success`

Protocol self-test:

`20 passed in 0.10s`

Broad source-free court:

`309 passed, 28 subtests passed in 90.19s`

Receipt artifact id:

`10734874232`

The broad target list explicitly includes:

`rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py`

alongside the parity/jurisdiction/oracle and wider FIABC/PRE553 source-free courts.

## Exact tree relationship

Both focused and broad court specs declare semantic candidate:

`9f12ebde3b0c3b074d219cdc1f9fb397475c2157`

Focused evidence execution SHA:

`1fd62c501c5d9b6c1281ec6e81f01d48697ccd8c`

Broad evidence execution SHA:

`10e1baf8db9a464dc565febf4310538f5abae4e1`

Those execution commits add only temporary bounded-court specification/workflow material around the semantic candidate.

Direct Git comparison:

`9f12ebde...` → qualified `516643348...`

shows **no file differences**.

Therefore the qualified implementation tree is exactly the tested semantic tree after temporary court infrastructure was restored.

## Why green CI does not cure the blocker

The CI faithfully passed the test suite that exists.

The candidate-domain defect is a test-law omission, not evidence that the CI job lied.

The parity suite's synthetic current fixture accepts candidate hashes as injected strings and uses the historical ASTRA/G02 values.

It therefore never exercises the actual current PRE553 candidate-hash constructor against historical candidate identity.

Likewise it does not require P2 historical `parameters` or current CONDITION/BASELINE predicate/query identities in the normalized row.

So the green CI receipt is valid, but its court specification is insufficient to satisfy the stricter acceptance law commissioned here.
