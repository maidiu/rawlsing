# FIABC-R35-I02 — Implementation Diff Inventory

## Production additions

### `rawlsing_next/fiabc_derivative_parentage.py`

New generic, source-family-neutral receipt layer.

It implements:

- canonical JSON sealing and SHA-256 receipt identities;
- `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`;
- exact source receipt identity pinning;
- exact derivative receipt identity pinning;
- exact producer/operation/reader-config comparison;
- scope/currentness/ownership comparison;
- parent and optional replay-parent closure;
- R5 root metadata projection;
- WVS structural-preimage metadata projection;
- explicit R5 embedded-parent check.

The module contains no source semantics and no source-family branch in the generic verifier.

### `rawlsing_next/ee_p2x_darwin_stage_backend.py`

Bound the generic contract at the two current dangerous consumer edges.

WVS changes:

- freeze pyreadstat `1.3.6` in the receipt contract;
- bind materializer Git blob `11b28416aac5a4899706150721f2f8ac8bb6ee43`;
- create source verification + derivative receipt when canonical WVS bytes are actually inspected by the accepted materializer;
- persist external `wvs7_projection_structural_input.parentage.json`;
- freeze bundle/source/derivative/structural identities into candidate durable state;
- on source-free reopen require exact receipt/state/doc agreement before materialization.

LiTS changes:

- preserve existing exact R5 root self-integrity checks;
- additionally verify embedded canonical source SHA and member-inventory SHA/length;
- require an external parentage bundle path and an independently pinned derivative-receipt identity;
- bind R5 physical root, logical stream/member inventory metadata, exact builder identity/blob, Candidate-A owner blob, LiTS projection, runtime catalog, active binding, runtime release, and physical-only latin1 reader/config;
- fail as a common source blocker when parentage is missing or inconsistent.

## Tests

### `tests/test_fiabc_derivative_parentage.py`

Synthetic hostile/positive receipt fixtures only. No raw source input and no measured P2X.

## Deliberately unchanged

No change was made to:

- C11 semantic mappings;
- I03/I05 meanings;
- source certification law;
- weighting/population authority;
- Candidate-C architecture;
- canonical source SHAs;
- source-native semantic interpretation;
- the contents of any raw SAV/DTA carrier.
