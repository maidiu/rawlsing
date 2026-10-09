# HQ262 G01 — G1 owner-only C1→F8 selected ingress — owner callsite and implementation

**STOP: `HQ262_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`**
**`G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY`**

## Control and blobs

- live canonical `origin/integration/pre-main-reconciliation-r1` = `64b4e7ab1e67c139c7115430c711d459474cf31a` (diverged from the tip; reported, not reconciled)
- commission tip `63cdc0b5bb4c382acf558e040b3669b787fc245f`, startup base `1ff7c74f6bef580ba3ce0738b7a9ac6b560ca2d7` (verified ancestor)
- commissioned blobs, all verified **exact** at the tip:
  - C1 `pre553_analytical_composition.py` = `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`
  - F8 `source_backed_positioned_subject_possibility.py` = `62e5eced47b64512f47b004e3e13a6ef3fe21de7`
  - `pre553_service_source_applicability.py` = `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`
- No existing owner was edited. The only new code is the one module and one test the
  commission permits.

## Why a new ingress was genuinely required

My HQ260 G01 review returned `BLOCKED_REQUIRE_TRUST_ROOT` because `evidence` was a
caller-supplied argument to F8 and `PossibilitySliceEvidence.authority_refs` /
`.provenance_refs` were validated but never read — so substitution was invisible to F8
**and survived the replay verifier**. I banked that as evidence and stopped, because no
in-process binding over caller-held material is unforgeable by that caller.

HQ262 changes the threat model to a bounded **external data-only service client**. Under
that model an unforgeable ingress *is* constructible, because the client can supply nothing
forgeable at all. So a new module is genuinely required and lawful here — not a redundant
adapter, and not a reinterpretation of the HQ260 diagnostic.

## The implementation

`rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py`.

**Public surface.** `serve(request)` accepts only a frozen `SelectedRequest(cell, stratum_ids)`
— two closed fields, plain scalars and a tuple of plain strings. There is no field for
evidence, a C1 result, a hash, an authority, a registry, a predicate, a witness, a
callback, a model rule, an applicability receipt, a grant ref, a currentness token, or any
schema that could embed an executable object.

**Owner-held.** Construction registers the repository, predicate, registry, releases,
consumer query, model rule, witness, per-cell inputs and the applicability/G2 scope. This
is a trusted-harness operation and is explicitly **not** runtime remote proof.

**Owner route, per request:**
1. validate the request against the closed enumeration;
2. **the owner executes C1 itself** — the client names only a cell;
3. take `possibility_slice_evidence_or_null` from `AnalyticalCompositionResult` — the
   **C1-originated** evidence, never client-supplied;
4. verify the complete original C1 evidence preimage (ref, source universe, release,
   target, conditioner ids, state, geometry, raw support, uncertainty, provenance, authority)
   and require non-empty authority **and** provenance custody;
5. verify the requested grain equals the C1-produced grain — no substitution;
6. build the applicability/G2 scope hash from **owner-held** preapproved TEST-ONLY UNISSUED
   material;
7. pass the **exact C1 evidence object, unchanged**, to F8;
8. emit a technical origin receipt binding C1 identity + C1 evidence preimage + risk set +
   denominator + applicability scope + F8 result hash.

The receipt is `authorizing=False` and carries no grant ref, no EE14 grant and no
currentness.

## Actual runtime, governed interpreter 3.11.3

```
contract       : HQ262_G1_OWNER_ONLY_C1_F8_SELECTED_INGRESS@1
c1_identity    : 01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd
c1_evidence    : C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1|urn:rawlsing:c1:posit...
  authority    : C1-AT07-COMPARABILITY|1.0.0|69cb88..., C1-AT07-QUERY|1.0.0|b59ef5...,
                 C1-AT07-ROUTING|1.0.0|a71a90..., C1-AT07-SOURCE|1.0.0|4d565f...
  provenance   : 7 owner-produced C1 provenance refs
f8_result_hash : 47b51a3b6df4ec051b5b9fb04a92760c791f4ac761f20a157966cbe1b481a4be
f8_state       : EXACT_SUPPORTED
origin_receipt : 1c59198c3ac621f2ec9e205cee906a94a8c4b0c23b0947631ce972657d07adf9
authorizing    : False
```

The authorities are genuine C1-AT07 producer authorities and the C1 identity hash differs
from the F8 result hash — the receipt binds **both**, so the F8 number alone cannot
reconstruct a selected receipt. That is the specific gap HQ260 identified.
