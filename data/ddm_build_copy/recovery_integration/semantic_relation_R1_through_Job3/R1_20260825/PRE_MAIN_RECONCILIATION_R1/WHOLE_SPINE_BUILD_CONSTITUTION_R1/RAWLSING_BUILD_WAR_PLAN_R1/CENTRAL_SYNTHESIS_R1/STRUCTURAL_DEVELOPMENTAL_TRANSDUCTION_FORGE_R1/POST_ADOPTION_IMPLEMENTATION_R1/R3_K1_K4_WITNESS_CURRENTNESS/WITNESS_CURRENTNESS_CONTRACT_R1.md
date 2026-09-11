# WITNESS CURRENTNESS CONTRACT R1

Status: `IMPLEMENTED_CANDIDATE__R3_G3_ONLY`

Authorized grain:
`SDTF_R4_K1_K4_PROOF_AND_TYPE_SPECIFIC_WITNESS_CURRENTNESS_INTERFACE_R1_ONLY`

Interface identity:
`SDTF_R4_K1_K4_WITNESS_CURRENTNESS_INTERFACE_R1@1.0.0`

## Frozen authority consumed

- R4 HQ launch base: `315ec8ba942cbf356bf1ef57471441299ae1a875`
- adopted companion blob: `4e77479afa3cce4cce7e38168f7ee9c6bf021cd0`
- OBL060 witness/source-separation pattern blob: `7f5901639107abf2ca40142f76b8fecb44b4c755`
- OBL060 R1 schema blob: `1d01a35347950688dbff5913d10614928e72a764`
- M1 temporal admission/dedup reuse blob: `e8bd6376720a2de132b384e7771d71d8d39cf261`

The three reuse blobs remain untouched.  Their source/type separation pattern is reused; none is promoted, replaced, or generalized into a universal witness ontology.

## Orthogonal assertion grammar

The interface preserves the adopted axes exactly and independently:

- assertion kind: `K1_CONSTITUTIVE_POSITIONAL`, `K2_QUALIFIED_POSSIBILITY`, `K3_REALIZED_OCCURRENCE`, `K4_ACTIVE_DURATIVE`;
- polarity: `POSITIVE | NEGATIVE`;
- fact currentness: `CURRENT | HISTORICAL_NONCURRENT`;
- modality: `ACTUAL | PROJECTED_COUNTERFACTUAL`;
- proof adjudication: `PROVEN | UNKNOWN_NOT_PROVEN`.

`UNKNOWN_NOT_PROVEN` is an adjudication result only.  This interface constructs no actor fact.  Bare `ACTIVE` is retained only as an opaque umbrella descriptor and never reclassifies an assertion to K4.

## Type-specific adapter contract

There is no universal witness record schema.  Each native witness/state owner supplies a `TypeSpecificWitnessAdapterR1` with exact owner-contract and witness-type refs and maps its own native record to:

1. proof-visible currentness evidence;
2. ordinary positive proof for K1/K2/K3;
3. explicit negative proof when negative truth is asserted;
4. one of the two adopted K4 proof paths when K4 positive truth is asserted.

The adapter, not shared code, decides which replay inputs are invalidating for its witness type.  Therefore unrelated replay churn cannot silently invalidate Path B, while owner-declared source/type/contact/substitute or other adopted invalidating dependencies can be surfaced explicitly.

## Witness currentness contract

Proof-visible witness currentness is evaluated before proof use.

Required lifecycle states:

- `CURRENT`
- `REVOKED`

Derived interface outcomes:

- `CURRENT`
- `STALE_REQUIRES_REPLAY`
- `REVOKED`
- `UNKNOWN_NOT_PROVEN`

Every current witness proof requires at least one exact authority-currentness check.  Each owner may additionally expose zero or more exact invalidating-dependency checks.  A check is one of:

- `CURRENT` with exact expected == observed ref;
- `REPLACED` -> `STALE_REQUIRES_REPLAY`;
- `REVOKED` -> `REVOKED`;
- `UNKNOWN_NOT_PROVEN` -> fail closed.

Owner-contract or witness-type mismatch also fails closed.  The first failing role is returned proof-visibly for replay/invalidation diagnosis.

## K4 Path A

Positive K4 Path A proves only when all are exact `YES`:

- competent current/interval witness;
- asserted interval coverage;
- required freshness/recurrence semantics.

Any stale/replaced/revoked/unknown currentness fails before Path-A proof is consumed.

## K4 Path B

Positive K4 Path B proves only when:

- owner semantics declare a continuing state = `YES`;
- type-compatible state support = `YES`;
- supportable validity interval overlaps asserted/query interval = `YES`;
- authoritative termination/supersession/invalidation coverage is complete through query time = `YES`;
- defeating closing fact = `NO`.

Old establishment evidence plus silence is insufficient.  Incomplete closure coverage, absent overlap, unknown support, or a defeating closing fact returns `UNKNOWN_NOT_PROVEN`.

Unrelated replay churn is not a shared invalidation rule.  A Path-B owner reports only dependencies that its own contract makes currentness-relevant.  Explicit owner/source/type revision or revocation remains invalidating.

## Negative proof law

Negative truth is a separate proof obligation.  Only the owner adapter's explicit negative-proof result `YES` can prove a negative assertion.  Failed positive proof, stale/expired/revoked positive proof, or termination of a positive proposition never manufactures an opposite fact.

## Unsupported / malformed cases

Missing owner/type bindings, absent authority-currentness proof, malformed adapter output, missing K4 path evidence, or unknown decisive checks return `UNKNOWN_NOT_PROVEN`.  No semantic inference is attempted across witness families.
