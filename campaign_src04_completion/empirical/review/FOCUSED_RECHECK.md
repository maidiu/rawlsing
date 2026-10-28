# SRC04 C/D focused provenance recheck — PASS_SCOPED_NATIVE_NONRESPONDENT_BOUNDARY

## Scope and custody

- Reviewer: same distinct C/D native-boundary reviewer, not C/D author.
- Branch: `agent/pyat-src04-cd-native-review-20261028`
- Verified startup HEAD: `c8bfdf9268e42727122595c8e6ca39a1ae1cef0a`
- Prior review commit: `a65446a0f259bf84d26a6b3e04645eccd14d997f`
- Repaired D code commit: `6a2c304e23c4d6c9f65e48d2734e2149b6a124cd`
- Repaired D return/head: `39c713a1396c7184afec5cb81519b151357c4a8e`
- Pinned C candidate remains `44aaf2be06e026547e9b32d880ac588e84acc9e4`; C files are unchanged.
- Only focused D observed-provenance behavior was reviewed. No original SRC04 source was accessed; no C/D author file was edited.

## Verdict

**PASS_SCOPED_NATIVE_NONRESPONDENT_BOUNDARY** — the prior D defect is repaired for the actual C-observed nonrespondent fixture -> D native/discovery path. This is a scoped engineering verdict only, not original-source, B-configuration, population, structural, or science acceptance.

## Exact primary equality

The actual D product now carries `observed_response` equal to the source C fact projection:

- C/D fact ref: `1754358a977d6112e2acddec188e65ac9ed8ec2a88cbb06ca2462c7ad47f149a`
- Status: `OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION`
- `not_eligible_population_estimate`: `true`
- Contract ref: `c2c8caa48b95e1833350ea5845943631cb37c39153ec987b743e3e27c8e0df26`
- The projection, including the entire ledger, is equal to the actual C fact.
- Canonical projection SHA-256: `99cabe1dbd2f6c10f679f0f91de70a2d5cadc7cb178ee24c865dd213720a1888`
- D status: `FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE`
- Downstream effect: `SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED`

The query's `observed_response_contract_ref` equals the carried projection contract ref exactly.

## Exact discovery equality

Two actual discovery facts retain their **own** C projections:

| Fact ref | Own projection equal | Ledger equal | Contract ref equal |
|---|---|---|---|
| `c8e6a4fa4813eab7321c5b5a381b611b41384fc00c262accbee13f139431a69e` | yes | yes | yes |
| `ea80f68425503fadb775ea56f70164b1ff9415454a6859a4ecf4b5b13bf86d94` | yes | yes | yes |

Their projection SHA-256 values are `99cabe1...a1888` and `cc9ff25a...08e8b` respectively. The first is the baseline projection; the second is the discovery fact's own conditional projection. Both preserve `not_eligible_population_estimate=true`, their own ledgers, and the exact observed contract provenance.

## Wrong-projection refusals

All exact owner refusals were measured under the observed profile:

- Missing projection → `OBSERVED_RESPONSE_PROJECTION_MISSING`
- Wrong status → `OBSERVED_RESPONSE_STATUS_INVALID`
- Top-level population claim → `OBSERVED_RESPONSE_POPULATION_CLAIM_REFUSED`
- Wrong contract ref → `OBSERVED_RESPONSE_CONTRACT_REF_MISMATCH`
- Missing ledger → `OBSERVED_RESPONSE_LEDGER_MISSING`
- Incomplete ledger → `OBSERVED_RESPONSE_LEDGER_INCOMPLETE`
- Wrong ledger contract ref → `OBSERVED_RESPONSE_LEDGER_CONTRACT_REF_MISMATCH`
- Ledger population claim → `OBSERVED_RESPONSE_LEDGER_POPULATION_CLAIM_REFUSED`
- Projection present without query grain → `OBSERVED_RESPONSE_PROJECTION_WITHOUT_QUERY_GRAIN`

An actual consumer call with a mutated primary projection refuses with `OBSERVED_RESPONSE_STATUS_INVALID`.

## Preserved prior evidence

- Frozen historical RED test file is byte-identical: `campaign_src04_completion/empirical/review/test_cd_boundary_review.py`, SHA-256 `4385981dd616bf94e5af8df9dad6a07ff6f299ce29799a75558041645b2994c8`.
- Frozen prior `REVIEW.json` is byte-identical: SHA-256 `331b43cafe53287e274a056dac7c5f54e13a94ae1fe5b7de65a3dd097c5969cc`.
- Frozen prior `TEST_RUN.txt` is byte-identical: SHA-256 `f294e01cfa0a0576aa522af3ef840df757643f3098972ba3041326f39f90fc95`.
- The historical defect test still asserts the old omission; it was not edited. The successor test is separate.

## Preserved value and firewall proof

- In-memory q236 fixture mutation changed the D primary fact and discovery refs; restoring the original fixture reproduced the exact original refs and projection.
- Nonobserved B0 SRC09 fixture path remains `FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE`, with no observed projection on the primary or discovery facts.
- Wrong source → `NATIVE_SOURCE_IDENTITY_MISMATCH`; wrong release → `WRONG_RELEASE_IDENTITY`; wrong fact → `FACT_SET_MISMATCH`; missing authority → `MISSING_AUTHORITY`.
- Fixture-only observed authority remains unable to promote to `ORIGINAL_SCIENTIFIC` (`Pre553AuthorityError`).

## Exact tests

```sh
PYTHONPATH=. python3 -m pytest campaign_src04_completion/empirical/review/test_cd_boundary_focused_recheck.py -q -o addopts=''
```

Result: **6 passed in 14.43s** (exit 0).

Successor test SHA-256: `6273e9a01452d0ae2378ddded661ed582b9245ac9c9160eb8789e927956e6b12`.

## Limits

- Source is the labelled SRC04 NONRESPONDENT fixture only; no original SAV stat/hash/open/decode/read and no original respondent rows or workload.
- No original source qualification, source-local claim, B-configuration acceptance, weighted population, FF/V553 structural adoption, N11/N12, actor adoption, new law, engine, worker, provider, or model.
- C authority and C files are unchanged; only the focused D provenance repair was checked.
- The passing scoped verdict does not convert the prior RED receipt into original-source acceptance.
