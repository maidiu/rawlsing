# FFIF006 — CLAIM BUNDLE AUTHORITY

## Atomic claims first

A bundle never repairs an underspecified claim. Each component must first possess its own CIM, proposition hash, assertion slot, invariant, support regime, and CITC row.

## Separate bundle object

```text
BUNDLE_REQUIREMENT_CONTRACT {
  bundle_id
  bundle_version
  atomic_claim_refs_hashes[]
  bundle_purpose_class
  co_requirement_predicate
  noncompensation_rules[]
  authority_basis
  authority_ref
  evidence_refs[]
  allowed_uses[]
  forbidden_uses[]
  frozen_before_output_refs[]
  bundle_hash
  supersession
}
```

## Two kinds of co-requirement

### `EMPIRICAL_PROPOSITION_BUNDLE`

The proposition itself is conjunctive: all component claims must hold to answer the stated empirical question. This may enter a claim-scoped bounded nonreducibility court if independently authorized before results.

### `CONSUMER_REQUIREMENT_BUNDLE`

An actor-independent downstream query needs several outputs together. This can support `DOWNSTREAM_MULTI_VIEW_REQUIREMENT` or consumer packet sufficiency. It does not by itself prove empirical bounded nonreducibility or make consumer usefulness truth.

## Lawful authority bases

- an explicitly conjunctive normalized research proposition;
- a frozen actor-independent query contract, with the consumer-only ceiling preserved;
- a source/measurement conservation requirement where multiple invariants are logically necessary to avoid misstatement;
- a pre-existing competent project requirement independent of compared outcomes.

## Forbidden bundle manufacture

Reject when:

- components are selected after seeing which view uniquely wins each;
- one broad prose label is used instead of atomic normalization;
- theory nouns make unrelated invariants appear co-required;
- a preferred method's capabilities define the bundle;
- downstream aesthetics, persona realism, or narrative richness supply the requirement;
- compensation lets high utility erase a critical empirical failure.

## Example

`exact minority branch retention + local neighborhood ordering + conditional redistribution reconstruction` is not automatically one claim.

If a predeclared empirical proposition logically requires all three, issue an `EMPIRICAL_PROPOSITION_BUNDLE`. If a PRE-V3 packet needs all three, issue a `CONSUMER_REQUIREMENT_BUNDLE`; the empirical claims remain atomic.

## Anti-laundering state

If co-requirement authority is absent:

`CLAIMS_RELATED_BUT_NOT_AUTHORIZED_AS_CO_REQUIRED`.

No multi-view necessity or bounded nonreducibility conclusion may be manufactured from that state.

