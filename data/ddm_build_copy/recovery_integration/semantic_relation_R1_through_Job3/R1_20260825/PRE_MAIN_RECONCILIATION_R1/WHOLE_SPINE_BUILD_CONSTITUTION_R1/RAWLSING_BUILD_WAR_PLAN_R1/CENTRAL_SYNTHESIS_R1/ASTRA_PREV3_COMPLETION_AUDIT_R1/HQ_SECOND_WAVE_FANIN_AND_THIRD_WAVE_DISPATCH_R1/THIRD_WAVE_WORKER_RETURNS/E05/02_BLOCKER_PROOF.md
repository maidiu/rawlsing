# E05 — Smallest Exact Code-Qualification Blocker Proof

Exact grain: `PREV3_OBJECTIVE_NON_EVENT_ADAPTER_INDEPENDENT_QUALIFICATION_R1_ONLY`

Primary blocker:

`E05_D05_STALE_CURRENTNESS_RECEIPT_REF_LAUNDERING`

## Frozen identities

- D05 implementation: `rawlsing_next/objective_non_event_publication_serving_adapter.py`
- implementation blob: `a1e2ae8775707eb30097279cde91f30271b6d243`
- inherited D05 return: `84861f42d51379d03702d996271b5d8c60719919`
- accepted M5 implementation used by C06 as the ingress/currentness constraint pattern: `rawlsing_next/m5_runtime_rsc_peer_prior.py`
- M5 blob: `18735bdb31a220aed032aa722574d685e2bdddf5`
- C06 candidate-contract blob adopted as the semantic contract source by D05: `a1bc0e483fb4a298ae803c192f51a00ddc19a029`
- E05 HQ fan-in authority: `018ef13413b24a3bc131fd0c769d37b832854135`

## Exact D05 path

D05's serving constructor accepts `currentness_receipt_ref_or_null` as only an `ExactRef | Mapping | None`, passes it through `_opt_ref`, and for a `CURRENT` item checks only that the resulting ref is non-null.

D05's serving validator likewise checks only:

1. a CURRENT receipt has a non-null world/release-root ref; and
2. a CURRENT receipt has a non-null currentness-receipt ref.

The D05 path does **not** consume or validate the referenced currentness receipt object. It therefore does not establish any of the following before serving CURRENT structural context:

- currentness-receipt schema/type;
- currentness-receipt content-addressed identity;
- exact binding to the selected resolution receipt;
- currentness authority/basis/effective-time binding; or
- `state == CURRENT`.

## Accepted M5 law that D05 weakens

M5's `StructuralCurrentnessReceipt` carries an explicit state with `CURRENT`, `STALE`, `REFRESH_REQUIRED`, and `INVALID` values. M5 `_validate_currentness(...)` recomputes the receipt identity, requires the exact selected resolution-receipt binding, and fails closed unless the state is exactly `CURRENT`.

C06's V3-ingress leg specifies the accepted shape as:

`exact M4 ResolutionResult + exact CURRENT structural-currentness receipt + exact V3 transition-owner declaration -> structural context eligibility`

and explicitly says historical/noncurrent objective material cannot be relabelled CURRENT merely to satisfy current-peer materialization.

## Deterministic stale-laundering witness

Take any valid M5 `StructuralCurrentnessReceipt` whose state is `STALE` (or `REFRESH_REQUIRED` / `INVALID`) and pass only its `.ref` as D05 `currentness_receipt_ref_or_null` for an otherwise valid CURRENT D05 selection.

M5 rejects that object because its state is not CURRENT. D05 accepts its exact ref because D05 never dereferences or validates the receipt and tests only non-null presence. The same D05 path also accepts a resolution-mismatched or unrelated exact ref.

Thus D05 does not preserve the accepted M5 currentness guard at least as strongly. This is a code-qualification blocker independent of E01's real-world-root materialization status.

## Scope disposition

No production repair is authorized or performed by E05. PRE-V3 remains objective-world only. No person/persona/subjective state is introduced. OBL063 quarantined driver/type/person-terminal semantics remain untouched.

`GATE-NON-EVENT-QUALIFIED` is **not satisfied** on the inherited D05 implementation.
