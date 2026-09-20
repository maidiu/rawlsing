# FIABC-LM1-R1D-B — Existing R5 Reuse Holding

## Holding

The R1C fresh LiTS-I R5 physical carrier may remain authoritative physical evidence after a lawful C11 physical/semantic boundary repair.

`FULL_MEMBER_REBUILD_REQUIRED` is not supported by the contract history.

Current accepted physical identities:

- root: `7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`
- logical stream: `076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba`
- canonical rows: `34,745,595`
- members: `2,121`
- member inventory: `04dce8c3e942fc81a0558354c21a4b4a56faab417ce362657286f978b6686703`
- parentage bundle: `8b63de4ea902350ce197bc3ed49b59259bef2ad400c9f3c7db65ac96b015ace7`

Replacement-success authority remains unconsumed.

## 1. Why the member bytes survive

The R5 member payload is upstream of the failing C11 seam.

Its contract is physical:

- exact source-cell coordinates;
- exact decoder-observed typed value;
- exact physical missing state/declaration;
- selected raw label where applicable;
- deterministic physical ordering/root/inventory law.

The accepted Route-A adapter verifies those bytes, decodes the typed value, reconstructs `PhysicalCell`, and only then invokes the source-backed C11 facade.

R1C's failure occurs after those steps.

No evidence shows:

- corrupted member bytes;
- typed codec round-trip failure;
- logical stream mismatch;
- inventory mismatch;
- source-parentage mismatch;
- R5 builder defect.

The current defect is:

`VALID_PHYSICAL_VALUE -> WRONG_CANONICALIZATION_DOMAIN_AT_C11_BINDING_SEAM`

not:

`INVALID_R5_PHYSICAL_VALUE`.

## 2. Authority 56 makes rebuilding conceptually backwards

Authority 56 deliberately required R5 to preserve distinctions that semantic C11 values may not directly admit:

- raw versus canonical;
- physical versus semantic missingness;
- binary float bit identity;
- signed zero;
- source-cell versus semantic occurrence.

Rebuilding the R5 carrier merely because C11's semantic canonicalizer cannot consume a host float would punish the layer that correctly preserved the evidence and would not resolve the ontology defect.

The physical member is exactly what the repaired seam needs.

## 3. Existing proof that member reuse across root reseal is lawful

R1C initially built physical root:

`acb0b287f1504a19a714b93f511b83db818b8de9b05c8b60e84fe58fb2285f59`

The accepted Candidate-A consumer required `source_artifact_ref.object_id = CANONICAL_SOURCE::<SHA>`.

R1C lawfully repaired only the root manifest.

Final root became:

`7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`

while:

- `members_rebuilt = false`;
- `logical_stream_changed = false`;
- member inventory remained exact;
- full single-pass audit passed.

Therefore the current carrier architecture already demonstrates the relevant dependency separation:

`ROOT_METADATA_CHANGE != MEMBER_REBUILD`.

## 4. Three lawful downstream cases

### Case A — facade-only physical material repair

If the repair changes only the physical-value material function in the C11 facade and leaves:

- source-specific projection authority identity;
- R5 release identity;
- accepted Route-A adapter blob/currentness;
- R5 compiler contract;

unchanged, then the current R5 root and parentage bundle remain valid as-is.

Minimum recovery work begins at:

`CURRENT CONSUMER ADMISSION`

with added regression/revalidation of LiTS physical-key rule construction.

### Case B — adapter/currentness repair without R5 release-identity change

If exact physical token material must be carried differently across the Route-A adapter boundary, then:

- R5 root stays unchanged;
- member bytes stay unchanged;
- logical stream stays unchanged;
- derivative parentage receipt must be reminted because it currently seals the accepted consumer adapter blob/currentness;
- parentage bundle must be reminted;
- consumer admission reruns.

No source reopen or member rebuild follows from the adapter change.

### Case C — projection/embedded release-identity versioning

If HQ decides the repaired physical-key law changes an identity intentionally embedded in the R5 release identity, then:

1. preserve all current member bytes;
2. preserve member inventory content if byte identities remain the same;
3. preserve logical-stream digest;
4. reseal root manifest with the new release-identity fields;
5. revalidate all existing members/inventory under the resealed root;
6. remint derivative parentage receipt and bundle against the new root;
7. rerun current consumer admission;
8. recompute succession completion.

This is:

`MANIFEST_RESEAL + REVALIDATE_EXISTING_MEMBERS`

not:

`FULL_MEMBER_REBUILD_REQUIRED`.

## 5. Projection physical-key revalidation is mandatory

The accepted LiTS builder creates q301 response physical keys from `Decimal(1..7)`.

The current exact physical R5 values may be decoder float64 values.

A lawful repaired key representation must not silently equate those two host types merely because their mathematical values compare equal.

Therefore before consumer success is adopted, the source-specific projection builder must demonstrate that each governed response rule is keyed to the exact physical source representation law selected by the repair.

Possible outcomes are outside this worker's authority:

- mechanical regeneration of physical keys under unchanged semantic authority;
- versioned projection-preimage identity;
- explicit projection-authority revision.

Whichever is chosen, the operation acts on projection/binding identity. It does not require changing R5 member payload.

## 6. Raw-witness identity consequence

`RespondentEvent.raw_response_value` and `EmpiricalCoordinateFact.raw_coordinate_value` are fields of canonical semantic objects.

Therefore a repaired exact physical-witness representation may legitimately produce different C11 object/content hashes for float-bearing source observations than a hypothetical string/Decimal representation.

That does not imply semantic reinterpretation if:

- the field is explicitly typed as raw-source witness material;
- canonical semantic values remain separately authority-governed;
- physical tokens do not acquire numerical/response meaning by themselves.

R1C never produced an accepted current real-source C11 logical release, so there is no successful real-source semantic release hash whose identity would be retroactively invalidated.

A new successful consumer must compute its C11 logical-release identity afresh.

## 7. R5 release metadata is not the C11 logical release

The R5 root carries a field called `semantic_release_hash`.

Current backend construction proves that field is:

`hash(source + source_sha256 + projection_identity + candidate A + owner_commit)`

It is a build/release determinant for the physical carrier, not the actual `C11LogicalRelease.semantic_release_hash` produced by C11 ingestion.

This distinction prevents a false rebuild conclusion.

A changed future C11 object hash does not automatically mutate the existing R5 physical row stream.

Only an explicit change to the R5 root's own release-identity determinants requires a root reseal.

## 8. Minimum rerun boundary proved by Worker B

After Worker A/C/HQ seals the lawful representation contract and implementation:

1. run focused physical-value seam regressions;
2. revalidate/recompute source-specific LiTS physical keys against accepted projection authority;
3. if root identity is unchanged, verify/open existing `7d85...` carrier and existing parentage;
4. if root release identity changed, manifest-reseal + revalidate existing members + remint derivative parentage;
5. rerun `CURRENT CONSUMER ADMISSION`;
6. only after consumer admission passes, recompute succession completion and determine whether the one-success replacement authority is consumed;
7. downstream Candidate/I03/I05/P2X work remains outside this worker.

No step above contains “rebuild 34,745,595 R5 rows.”

## 9. Stop condition that would change this holding

A full physical member rebuild would become justified only if a later court proved that the existing typed member payload itself lacks a physical distinction required by the repaired contract or is cryptographically/structurally invalid.

No such evidence exists in the current record.

The current evidence proves the opposite: R5 already preserves the float/non-finite distinctions at issue.

## Final holding

`EXISTING_R5_MEMBER_BYTES_REUSABLE__CURRENT_FAILURE_IS_DOWNSTREAM_C11_BOUNDARY__AT_MOST_MANIFEST_RESEAL_AND_MEMBER_REVALIDATION_BEFORE_CONSUMER_RERUN`
