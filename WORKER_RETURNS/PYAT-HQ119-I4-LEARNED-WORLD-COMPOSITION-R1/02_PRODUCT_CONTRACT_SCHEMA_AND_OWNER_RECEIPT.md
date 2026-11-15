# Product Contract Schema and Owner Receipt

## Exact schema

I4 introduces only the adapter contract `LearnedWorldProductContractBinding@1.0.0`. It is not a semantic stage.

Constitutive fields include:

- exact route;
- exact product-family ref;
- exact producer-owner ref;
- exact producer-contract ref;
- explicit semantic-subject/product/projection rules;
- exact release-subject kind;
- exact selection-scope ref;
- exact producer-permission-ceiling ref;
- exact consumer/product-purpose ref;
- exact M1 family-rule-binding ref when I4 is asked to perform M01->M1 adjudication;
- exact closure-construction rule;
- explicit lifecycle policy;
- explicit ordered lifecycle actions;
- exact registration/publication/selection authority and rule refs when those actions are requested;
- exact selection attestation/purpose/partition/prior receipt when selection is requested;
- exact direct-route authority and exact consumer acceptance when the direct-producer route is selected.

Every constitutive field participates in the deterministic contract ref. The hostile court proves that changing a constitutive consumer-purpose field changes both contract and composition-receipt identity while leaving the producer-owned M2 semantic release identity unchanged.

## Producer ownership

For an M1-derived disposition, I4 uses the deterministic transport identity:

`M1_DISPOSITION_PRODUCER_CONTRACT_REF`

This ref is derived only from the already-adopted `M1_ADJUDICATION_CONTRACT_ID` and states `i4_semantic_reownership = false`. I4 requires the product contract to name this exact producer contract for M1-derived composition; it does not fabricate a replacement semantic owner.

M1's disposition ref becomes the M2 `ProducerSubject.ref` exactly. The M2 subject's `semantic_anatomy_ref` is the same exact disposition ref. The M2 typed state is the exact M1 `adjudication_outcome`.

## Authority representation boundary

M1 authority closure is typed as `AuthorityRef`; M2 closure members are `ExactRef`. I4 therefore uses `I4AuthorityTransportRef@1.0.0` only as a lossless representation bridge.

For each M1 `AuthorityRef`:

1. its full `as_dict()` preimage is embedded in M2 authority-closure metadata;
2. a deterministic transport `ExactRef` is computed from that full preimage;
3. the transport ref is an M2 closure member;
4. M2->B5 restores the original `AuthorityRef` from the preimage;
5. I4 recomputes the transport ref and requires it to exist in the exact M2 closure before accepting restoration.

This is representation conservation, not authority aliasing or semantic reownership.

## No automatic lifecycle authority

The contract default is no lifecycle actions. Merely producing:

- an M2 `ProducerSubject`,
- M2 closures,
- an M2 `ReleaseCore`,
- or an M2 resolver/publication binding

does not stage, register, publish, or select anything in B5.

Lifecycle actions are an exact ordered prefix only:

`REGISTER -> PUBLISH -> SELECT_CURRENT`

Missing exact action authority blocks before I4 mutates B5.

## Side-effect ceiling

The composition receipt permanently carries false for:

- consumer permission;
- structural admission;
- causal truth;
- Field Forge;
- actor/V3;
- source/carrier retirement.

Those flags cannot be set true by I4 construction.
