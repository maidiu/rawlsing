# SRC04 carrier two-defect focused recheck — PASS_SCOPED_CHANGED_ISSUER_CARRIER_BOUNDARY

## Scope and custody

- Same distinct C/D reviewer; not a C/D author.
- Branch: `agent/pyat-src04-actual-carrier-review-20261028`
- Verified focused-recheck HEAD: `2d011ad450894b266c44b28cdabd93513df10718`
- Repair candidate: `d03a1d78d488807b6b946e000df10c1c88dc4bea`
- Prior reviewed candidate: `d48ddf93f6642b80e8d9f0399dbc0abd5ec66742`
- Prior review artifact: `434211cc09cd8b57c3087319d5de878640890604`
- Accepted D dependency: `39c713a1396c7184afec5cb81519b151357c4a8e`
  - Current `consumers/consumer.py` SHA-256: `728fbc9a09291ae9c9d578fbed7641acd4499a2ff4158b7588e1cc5afa18f8ae`

Only `campaign_src04_completion/empirical/actual_review/**` was written. Author/native/consumer code is read-only. The prior frozen RED artifacts are unchanged.

## Verdict

**PASS_SCOPED_CHANGED_ISSUER_CARRIER_BOUNDARY** — both prior defects are closed for the labelled nonrespondent fixture boundary:

1. The actual receipt/pickle adapter → authenticated fixture-scoped issuer → native executor → accepted D consumer path now executes end to end.
2. Missing pinned receipt files and malformed/truncated carrier streams now return typed `ActualCarrierRefusal` codes, while intact carriers work and original-source gates remain strict.

This is scoped engineering acceptance only. It is not original-source qualification and does not authorize or execute the original workload.

## Fixture end-to-end measurements

- Fixture config SHA-256: `7f69af5cfafe07123c211707df353b37da4e9375adfa6e55c5df42a930cfebaa`
- Fixture file SHA-256: `e02e85388de86aa0ce66fa37ac59a6d3071537ea514788a54baf3964cbb44353`
- Fixture stream SHA-256: `506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b`
- Fixture release: `9026fa33bb5739b87b06309f12e1d31fe6fd21fb471237eda870d6d278d47f42`
- Fixture grant: `38e82f943bee3b2e649e91beb0dee97ca343538f6c903a286adda81c5df84f7f`
- Issued contract: `7d8780332ba981f6baf55352b29f36a2af6656d553dc0a8c9c4cc9ee5425ef41`
- Issued state: `fixture_only=true`, `NONRESPONDENT_FIXTURE_ONLY`, source SHA fixture stream.
- Workload: 44 operations, 44 executed, 0 refused.
  - 3 unary: all `SUPPORTED` 7/7, 8 scoped respondents, 7 observed, 1 unobserved.
  - 3 same-person joints: all `CO_OBSERVED_TARGETS`, denominators 6, 6, 7.
  - 38 conditional operations across all 6 ordered target directions; condition ledger/count equality verified.
- D product: `FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE`, effect `SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED`, `fixture_only=true`, `source_local_claim=false`.
- D primary fact: `ed4ae641a033a6847b3db5511ad3be4e99e7343e115f96cd2fe5fbb4486bebaa`.
- D observed status: `OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION`; `not_eligible_population_estimate=true`; exact contract ref `7d878033...`; full ledger.
- Discovery facts: `65021ceb...`, `865b2d2a...`; each carries `OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION`, not-eligible, and its own observed ledger.
- Source-literal topology discriminator: wrong binding yields `TOPOLOGY_REF_MISMATCH`; 2 valid bindings remain.

## Carrier refusal measurements

With receipt pins matching the malformed/truncated files:

- Missing pinned receipt → `ActualCarrierRefusal: CARRIER_FILE_UNREADABLE`
- Malformed pickle → `ActualCarrierRefusal: CARRIER_STREAM_UNREADABLE`
- Truncated pickle → `ActualCarrierRefusal: CARRIER_STREAM_UNREADABLE`
- Intact carrier → successful rehydration of the exact fixture release.
- Wrong receipt pin → `LOCAL_RECEIPT_SHA256_MISMATCH`
- Wrong source → `LOCAL_SOURCE_MISMATCH`
- Mutated stream without updated receipt → `LOCAL_RECEIPT_PUBLIC_OBJECTS_SHA_MISMATCH`

No raw `FileNotFoundError` or `UnpicklingError` leaked in these cases.

## Original-source gate proof

- Original grant + fixture release → `RELEASE_SOURCE_IDENTITY_MISMATCH`
- Original grant passed to fixture issuer → `FIXTURE_GRANT_REQUIRED`
- Fixture grant forced through `fixture_mode=False` → `NO_SOURCE_QUALIFIED_TARGETS`; no original-grade execution
- Wrong fixture-grant SHA → `FIXTURE_GRANT_SHA256_MISMATCH`

The original accepted release `9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1` was not read, requalified, or executed here.

## Preserved prior RED and value proof

- Frozen prior review test: `97278b24a8378674c7312b4d4f66972eedd18bb9ecec749ade797fdade69de67` (unchanged)
- Frozen prior `REVIEW.json`: `a9e8bd8756e81f05001249322b96dfeec0cb6e0b9abfbd70597e0c01bba53ce0`
- Frozen prior measurements: `85af81c7ce6de31f474a9d409edc058d5ff33cb9a3b7d2d9159307712b9e8c4a`
- Frozen prior test run: `9314078b109ec98a1e2a10e1323b928acacf6a1de85e77f6dcd220f8b47429a4`
- Prior accepted C/D value change/restoration remains recorded at focused review `9b66083f89a6881f296be7fd1a8ff04c9718951b`: changed fact `c14eb163...` restored to original `1754358a...`; this unchanged accepted path was not reopened.

## Exact focused test

```sh
PYTHONPATH=. python3 -m pytest campaign_src04_completion/empirical/actual_review/test_carrier_focused_recheck.py -q -o addopts=''
```

**5 passed in 21.98s** (exit 0; no intentional skip in the successor suite). The successor executes the actual fixture end-to-end and the repaired carrier refusal cases. The frozen historical `_DEFECT` suite was not rewritten or used as acceptance.

- Successor test SHA-256: `8a5b6ee49562fcdc9e9979b73061bff2819c07b196a6f828a91db95188c13380`
- Test run SHA-256: `980335dc8af51337f88ebd88eb2f464e2a77bf7ecda9c4f2de82cb74e621914c`
- Measurements SHA-256: `a10dc2f99b3e150cbb9b74bef3533fc2fc94d4a3c5fec30b7b499eef19c8a35a`

## Limits

- SRC04 labelled nonrespondent fixture only; no original SAV, original respondent rows, original product, or original workload.
- Scoped engineering PASS only; no source-local, population, weighted, causal, structural, Field Forge, N11/N12, actor, or original-execution claim.
- The original source release remains independently accepted; this review does not requalify it.
- No new engine, worker, provider, model, permission, polling, or unrelated source investigation.
