# GT12 Closure A1 — real 19,210 C11 scale closure R1 — return

## Scope

Branch: `agent/rabochii-gt12-closure-a1-real-c11-scale-r1`

Exact starting HEAD: `42c4a1ed753071026a5186e8c1770b6359a9e48c`

Owned lane only:

`governed R5 carriers -> exact governed 19,210-member claim-scoped C11 materialization -> genuine-scale C11 construction/validation performance closure`

GT1 I03 and GT2 I03 were not executed.

## Governed artifact proof

The supplied `field_forge.zip` was used only as the governed Library-artifact source.

FFP017 `deterministic_replay_receipt.json` binds:

- source path: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source rows: `51,587`
- respondent carrier semantic identity: `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- respondent carrier rows: `51,587`
- respondent physical member SHA-256: `f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be`
- exact common-risk member count: `19,210`
- risk-set semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`

Byte hashes rechecked from the supplied governed files:

- FFP014 `carrier-00000.tsv.gz`: `f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be`
- FFP017 `core_claim_common_risk_set.tsv.gz`: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
- FFP017 `selected_response_facts.tsv.gz`: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- FFP017 `selected_exposure_facts.tsv.gz`: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`

The raw `.sav` bytes were not present in the supplied artifact bundle, so the source SHA itself was checked against the immutable FFP017 deterministic replay receipt plus the frozen GT12 binding; no new source data was acquired.

Exact claim membership was re-proved from all `51,587` admitted source-carrier rows against the governed risk-set member artifact before C11 materialization. The C11 release contains exactly `19,210` governed claim members while retaining the full source identity/row count as provenance.

## Live defects reproduced and repaired

1. `GovernedC11Projection` rebuilt the complete respondent-ref set inside the per-row membership predicate: accidental O(n^2). Repaired by one immutable exact membership set.
2. Frozen C11 internal records repeatedly recomputed deterministic `content_hash` / `object_id` / `ref`. Repaired with immutable `cached_property` identity memoization.
3. Claim-scoped materialization previously assumed replay row ordinals had to be `1..row_count`. Repaired so row-count is claim cardinality while exact original source row ordinals remain identity-bearing.
4. Replay sealing and validation materialized a giant nested list of fresh ref dictionaries before hashing. At real 19,210 scale this reproduced a >600 s/no-release cliff. Repaired by a streaming canonical SHA-256 encoder over exact sorted immutable refs. The legacy materialized projection remains available as the semantic oracle.

No authority validation, canonicalization, provenance, typed-negative handling, replay law, ref identity, source binding, or hash comparison was weakened.

## Semantic identity oracle

On the deterministic small fixture:

`_candidate_projection_semantic_hash(candidate) == semantic_hash(_candidate_projection(candidate)) == candidate.candidate_replay_manifest.semantic_projection_hash`

At 8,000 genuine governed members the legacy materialized and streaming hash paths also produced the exact same hash:

`859762cfeccccec1379e1df8de8044675b979b82d61ba9efd9c08df37600cee7`

The streaming path is a memory-scale repair, not a changed semantic projection.

## Genuine 19,210 execution

Exact committed source snapshot used for the acceptance run: `b22e18d450619d81945766e11408360ec1ecb7e7`.

Stage timings on that exact committed snapshot:

- governed FFP014/FFP017 load + exact source/risk proof: `4.779981720 s`
- exact 19,210 projection construction: `5.539304465 s`
- C11 candidate + sealed replay manifest: `9.570162514 s`
- complete C11 validation: `12.695985125 s`

Official public helper:

`build_validated_claim_scoped_r5_q86_c11_release(...)`

wall clock: `28.907190153 s`

Before repair, the live 19,210 path reproduced the inherited large-scale failure and did not produce a release inside a `>600 s` execution gate.

### Exact release identity

C11 release ref:

- kind: `C11LogicalRelease`
- object_id: `R5_GT12_Q86A_Q86B_FROZEN`
- content_hash: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`

Semantic release hash:

`8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`

Replay manifest ref:

- kind: `C11Internal:ReplayManifest`
- object_id: `urn:rawlsing:pre553:c11:ReplayManifest:sha256:c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- content_hash: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`

### Exact object counts

Public C11 objects: `96,057`

- EmpiricalUniverse: `1`
- RespondentEvent: `38,420`
- RoutingEligibilityFact: `38,420`
- EmpiricalCoordinateFact: `19,210`
- AuthoritySnapshot: `6`

Internal C11 records in sealed release: `19,212`

- RespondentIdentity: `19,210`
- QuestionVariableBinding: `2`

ReplayManifest is sealed separately as the release replay manifest.

All M01-M18 coverage atoms closed.

## Regression / hostiles actually executed

Committed branch regression at `b22e18d450619d81945766e11408360ec1ecb7e7`:

`pytest -q rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`

Result: `20 passed in 0.96s`.

After the final test-only hostile strengthening, the same command was rerun locally against the exact exported committed source plus the final test delta:

Result: `20 passed in 0.35s`.

Covered hostile/regression surfaces include:

- respondent/source row reordering
- exact-member ordering changes
- duplicate source respondent identity
- duplicate exact risk-set respondent ref
- risk-set semantic hash tamper
- source hash tamper
- respondent carrier hash tamper
- selected response carrier hash tamper
- selected exposure carrier hash tamper
- missing exact member
- extra exact member
- exact respondent-ref tamper
- required authority closure failure
- response-presence cannot substitute for exposure authority
- source-native DK / refusal / not-asked / missing typed states
- noncontiguous preserved source row ordinals
- deterministic release/ref equality under logical reordering
- byte/semantic equality of legacy and streaming replay projection hashes

No GT1, GT2, EmpiricalFact acceptance, FIELD FORGE/PRE-V3/M1 semantics, new source data, source data in Git, backend/database architecture, sibling closure branch, PRE-MAIN/main movement, or retained Actions/export scaffold is present.

## Files changed from exact start

- `rawlsing_next/pre553_c11_ingest.py`
- `rawlsing_next/pre553_c11_integrity.py`
- `rawlsing_next/pre553_source_backed_c11_facade.py`
- `rawlsing_next/wave1_r5_q86_c11_projection.py`
- `rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py`
- this return receipt

## Terminal

`PASS__GT12_A1_REAL_19210_C11_BUILD_SCALE_CLOSED`
