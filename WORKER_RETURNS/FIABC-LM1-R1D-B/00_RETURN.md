# FIABC-LM1-R1D-B — C11 Float Ban / Physical-Binding Contract Archaeology Return

## Disposition

`FIABC_LM1_R1D_B_C11_CONTRACT_ARCHAEOLOGY_COMPLETE__R5_REUSE_AND_RERUN_BOUNDARY_PROVED`

Repository: `maidiu/rawlsing`

Base:

- branch: `agent/rabochii-premain-fiabc-lm1-r1c-governed-r5-rebuild-r1`
- exact tip: `ca3630f5f7146f611c8cdc30b010eab509a5145b`

Worker branch:

`agent/rabochii-premain-fiabc-lm1-r1d-b-c11-contract-archaeology-r1`

This worker used GitHub/browser evidence only. It did not open LiTS source bytes, access the local `/tmp` R5 carrier, rebuild R5, execute Candidate A/B/C, run I03/I05, or run measured P2X.

## Holding

The C11 binary-float prohibition was introduced as a **semantic-identity canonicalization law**, not as a prohibition on deterministic representation of raw physical binary-float states.

The present failure is a later composition contradiction:

1. `canonicalize()` was introduced on 2026-08-20 for deterministic **semantic** material and explicitly rejected Python binary floats as lossy/unfit semantic identity.
2. R5 Authority 56, frozen on 2026-08-21, separately required exact physical typed-value representation, including finite decoder float bits and signed-zero preservation, while preserving raw-versus-canonical separation and stating that physical-buffer identity is not C11 semantic identity.
3. C05R2A authority on 2026-08-23 required physical carriers to remain nonsemantic and required explicit governed semantic projection.
4. The C05R2A facade nevertheless implemented `physical_value_binding_key()` by sending raw physical values through the generic semantic `canonicalize()`.
5. Its bounded tests used string-valued response fixtures and integer weights; they did not exercise decoder-observed binary-float physical states.
6. The accepted R5 runtime/Route-A adapter later supplied exactly those physical states: the accepted typed codec preserves float64 bits/non-finite lanes, then the mechanical adapter decodes them back into `PhysicalCell.raw_value` before the source-backed facade.
7. R1C therefore reaches a lawful exact physical value and fails only when the old facade attempts to treat that value as semantic-canonical hash material.

This history does **not** support globally widening `canonicalize()` to accept Python floats. It supports restoring the already-authorized physical/semantic boundary.

## Provenance anchors

### C11 semantic float ban

Commit:

`b349b6979949aee82a2bfa23226f78fd558daffe`

Date: 2026-08-20

Message:

`Implement PRE553 canonical empirical object model`

Introduced `rawlsing_next/pre553_empirical_objects.py` with the current rule:

`float/NaN/Infinity forbidden in semantic identity`

and the explicit docstring law that binary floats are forbidden from deterministic JSON-safe **semantic material**.

The accepted test `test_float_rejected_but_exact_decimal_is_deterministic` confirms the purpose: Python `0.1` is rejected while exact Decimal representations canonicalize deterministically.

### R5 typed physical-value authority

Authority 56:

`56_POST_R4_ROUND2_FINAL_SYNTHESIS_AND_R5_CARRIER_CONTRACT.md`

Commit:

`29c0573a6347ee88ce2b9d69c11bdc2799d2981f`

Date: 2026-08-21

Message:

`Freeze post-R4 Round-2 final R5 carrier contract`

It froze:

- exact typed physical incidence;
- raw versus authorized canonical value separation;
- physical missingness versus semantic response-state separation;
- `DECODER_FLOAT_BITS` for finite decoder-observed floats;
- signed `-0.0` distinct from `+0.0`;
- an exact inverse/escape law;
- the rule that a physical buffer digest is not a C11 semantic hash.

Authority 57 immediately authorized implementation under the same boundary.

The currently accepted codec implementation is:

`rawlsing_next/pre553_r5_codec.py`

accepted owner lineage:

`0b96b8de9aac774566f872cf0630ebd4ddeb70e6`

accepted blob:

`72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`

It currently distinguishes:

- bool from int;
- int from float;
- finite float64 by exact big-endian bits;
- `+0.0` from `-0.0`;
- decoder-observed NaN state without fabricating payload bits;
- positive and negative infinity;
- strings, including string `"inf"`, from floating infinity.

Its `typed_key()` is explicitly an equality key that avoids host-language bool/int/float/string collapse.

The **authority** for this typed physical seam predates C05R2A. The concrete Route-A runtime import/transposition of the accepted codec appears later in the owner lineage, including commit `c935c7003c6081f699968ee4385d6a91bba5f13e` on 2026-09-08.

### Source-backed C11 facade

C05R2A implementation authority:

`d16d988ea51e02482e9f6887fa8ecdcde3c7eb66`

Date: 2026-08-23 07:05:49Z

Facade implementation commit:

`91315bd3df9bd7f5e710d9791cc8be0bb96173fb`

Date: 2026-08-23 07:44:01Z

The facade was explicitly commissioned to keep physical carriers nonsemantic and to require exact caller-owned authority for semantics. However its original implementation already contained:

`physical_value_binding_key(raw_value, ...) -> semantic_hash({"raw": canonicalize(raw_value), ...})`

That line therefore imported the semantic-number admissibility rule into a physical binding-key seam without an authority stating that physical binary floats themselves were forbidden.

Subsequent facade revisions preserved this key law. The 2026-09-11 multi-owner repair still left `physical_value_binding_key()` unchanged.

## Why bounded C05R2A proof did not catch it

The current C05R2A synthetic fixture uses string response values:

- `"1"`, `"0"`, `"AB"`, etc.

and integer weights.

The fixture therefore proves semantic projection mechanics for canonicalizable host values but is not a binary-float physical-value court.

The banked LiTS projection builder introduces a second historical seam: it constructs response `physical_key` values for q301_2/q301_7 from `Decimal(1)` through `Decimal(7)`, while the actual R5 physical carrier preserves decoder float64 type/bits. That mismatch requires physical-key representation revalidation after the boundary repair. It does not make the existing physical members invalid.

## Exact present failure

R1C proved the failure occurs after:

- exact R5 root verification;
- exact member verification;
- exact typed codec decode;
- exact Route-A reconstruction of `PhysicalCell`.

The failing path is:

`_cell_key -> physical_value_binding_key -> canonicalize(cell.raw_value)`

The exception is:

`Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity`

R1C explicitly reports that no semantic conversion was invented.

## R5 reuse holding

The accepted fresh carrier remains authoritative physical evidence:

- physical root: `7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`
- logical stream: `076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba`
- canonical rows: `34,745,595`
- members: `2,121`
- member inventory: `04dce8c3e942fc81a0558354c21a4b4a56faab417ce362657286f978b6686703`
- current parentage bundle: `8b63de4ea902350ce197bc3ed49b59259bef2ad400c9f3c7db65ac96b015ace7`

The C11 boundary repair is downstream of member construction. No lawful narrow repair discovered here requires changing R5 typed member payloads.

R1C already supplies direct precedent that root metadata may be resealed without rebuilding members: adding the required canonical source object id changed the physical root from `acb0...` to `7d85...` while the member bytes and logical stream remained unchanged.

Therefore:

`FULL_MEMBER_REBUILD_REQUIRED`

is **not** the historical consequence of the present boundary defect.

## Rerun boundary

### Narrow repair class N1 — physical seam only, no authority/projection identity change

If the repair:

- keeps generic `canonicalize()` unchanged;
- introduces/uses a physical-value canonical material function at the physical seam;
- does not alter semantic authority refs;
- does not alter the accepted LiTS projection authority identity;
- does not alter the R5 release-identity determinants;

then:

- R5 root/member/inventory/logical stream remain unchanged;
- current derivative parentage bundle remains valid;
- physical-key/projection rules must be revalidated against the repaired seam;
- current consumer admission must be rerun;
- downstream succession completion must be recomputed.

### Narrow repair class N2 — boundary contract/version identity is deliberately rebound into R5 root metadata

If HQ requires a changed compiler/C11 contract digest to be recorded in the R5 root release identity, the lawful consequence is:

- `MANIFEST_RESEAL`;
- revalidate existing members;
- member bytes remain unchanged;
- logical-stream digest remains unchanged;
- derivative receipt and parentage bundle identities recompute because derivative identity/root changes;
- consumer admission and succession receipts recompute.

Still no physical member rebuild.

### Narrow repair class N3 — source-specific projection identity/authority is versioned because the physical-key preimage changes

If the source-specific projection authority itself is intentionally versioned, then:

- projection identity and C11 authority digest recompute;
- the R5 embedded release identity consequently changes;
- root manifest must be resealed;
- existing members are revalidated, not rebuilt;
- logical stream remains unchanged;
- derivative parentage receipt/bundle recompute;
- consumer admission and succession recompute.

This is the strongest plausible narrow downstream ripple found. It still does not require rebuilding physical R5 members because the member payload already preserves the exact physical distinctions the repaired C11 seam needs.

## Important identity-name distinction

The R5 root field named `semantic_release_hash` is not the later `C11LogicalRelease.semantic_release_hash`.

In the current backend it is derived as:

`sha256({source, source_sha256, projection_identity, candidate:"A", owner_commit})`

The actual C11 logical release hash is constructed later from the canonical refs of the validated semantic objects. The latter must be freshly computed after the repaired consumer successfully projects the real source. There is no accepted current real-source C11 logical-release hash to preserve because R1C fails before one exists.

## Claim boundary

This worker proves historical contract lineage and the reuse/rerun boundary only.

It does not:

- select the exact implementation patch for Worker A/C/HQ;
- certify that a particular typed-token shape is the final semantic raw-witness representation;
- run the repaired consumer;
- execute A/B/C;
- consume the one-success replacement authority;
- run I03/I05;
- run measured P2X.

## Terminal

`FIABC_LM1_R1D_B_C11_CONTRACT_ARCHAEOLOGY_COMPLETE__R5_REUSE_AND_RERUN_BOUNDARY_PROVED`
