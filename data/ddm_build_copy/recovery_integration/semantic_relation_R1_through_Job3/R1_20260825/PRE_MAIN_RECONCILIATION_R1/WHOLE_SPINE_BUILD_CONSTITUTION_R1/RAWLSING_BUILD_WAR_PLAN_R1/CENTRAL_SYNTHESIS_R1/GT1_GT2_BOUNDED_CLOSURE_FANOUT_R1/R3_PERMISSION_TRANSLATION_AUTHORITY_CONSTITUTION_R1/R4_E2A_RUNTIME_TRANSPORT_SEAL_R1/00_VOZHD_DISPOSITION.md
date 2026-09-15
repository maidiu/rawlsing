# GT12 R4 — VOZHD DISPOSITION: CURRENT E2A RUNTIME TRANSPORT-SEAL EXCEPTION R1

## Disposition

`AUTHORIZED__ONE_TIME_ACCEPTED_CARRIER_REPLAY_FOR_CONSTRUCTOR_COMPLETE_GT2_RUNTIME_TRANSPORT_SEAL`

This is a resource/executability disposition only. It creates no new empirical, FIELD FORGE, PRE-V3, M1, M4, V3, or V2 semantic authority.

## Triggering blocker

E2B returned:

`BLOCKED__GT12_FINAL_E2B_NO_LAWFUL_BANKED_E2A_RECEIPT_TO_CURRENT_EMPIRICALFACT_RUNTIME_MATERIALIZATION_SEAM`

Banked at central merge:

`0446710569c7b471c5d2e449628edadb396b45b4`

The candidate has exact current R1C/E2A identities and empirical-result evidence, but not constructor-complete runtime material for the canonical current `EmpiricalFact`.

## Why a pure no-Library loader cannot be constituted from the existing receipt

Current `EmpiricalFact@1.0.0` identity hashes the exact canonical semantic projection, including:

- exact authority snapshot refs;
- exact dependency refs;
- exact producer replay root;
- exact source empirical provenance refs;
- exact risk-member refs;
- exact denominator-member refs;
- target topology / complete-cell projection;
- all other identity-bearing semantic fields.

The existing E2A receipt intentionally banks closure counts/digests rather than the constructor-complete large ref sequences. Aggregate hashes are not reversible into those exact sequences.

Therefore:

`KNOWN_FINAL_FACT_HASH + AGGREGATE_CLOSURE_DIGESTS != CONSTRUCTOR_COMPLETE_EMPIRICALFACT_RUNTIME_MATERIAL`

A loader that merely injects the known final hash or invents unseen refs would violate canonical PRE553 identity law and the E2B actual-object requirement.

## Immediate FIELD FORGE consumer

The exact FIELD FORGE conditional-support producer requires both:

- an actual canonical `EmpiricalFact`;
- an actual canonical `EmpiricalQuerySpec`.

It recomputes both semantic hashes and checks exact fact→query, risk-set, universe, authority, replay, provenance, target-domain and dependency closure.

The transport seal therefore must cover the current query and fact, not merely the fact ref.

## One-time Library exception

The prior downstream no-Library rule is temporarily relaxed for exactly one purpose:

**replay the already accepted A1/E2A carrier substrate once and seal constructor-complete current query/fact runtime transport.**

Permitted external inputs are only the exact persistent governed carriers already accepted and used by A3/E2A:

- FFP014 R5 current respondent carrier;
- FFP017 governed response/exposure carrier material required to reproduce the exact A1 C11 claim-scoped release.

No raw `.sav` acquisition is permitted.

No new source is permitted.

No changed source/carrier version is permitted.

No new empirical query or semantic interpretation is permitted.

If the accepted carriers cannot reproduce the exact already-current R1C identities, fail closed.

## Current identities that replay must reproduce exactly

- predicate:
  `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query:
  `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- EmpiricalFact:
  `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- replay:
  `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`

R1C remains the authority for currentness. The replay does not get to choose different identities.

## Transport normalization law

The transport may normalize duplicated canonical material for storage efficiency only if reconstruction is exact.

Expected minimal form:

1. complete current `EmpiricalQuerySpec.as_dict()`;
2. fact header containing all small top-level and semantic identity material;
3. exact ordered `risk_set_member_refs` sequence;
4. exact ordered `denominator_member_refs` sequence, or a manifest declaration that it is byte/canonical-sequence identical to risk members, proven against the replayed fact;
5. exact canonical `source_empirical_provenance_refs` sequence/set;
6. exact dependency closure, either stored directly or deterministically reconstructed only where equality with the replayed fact is proven;
7. exact replay root/ref;
8. exact authority refs;
9. manifest and shard content hashes.

Normalization must be lossless. Re-expanded material must construct the ordinary existing `EmpiricalQuerySpec` and `EmpiricalFact` classes and reproduce the exact current object IDs/content hashes.

No proxy, fixture, subclass, semantic alias, alternate object family, or "equivalent enough" object is authorized.

## Data-minimization / governance ceiling

The sealed Git carrier may contain only semantic identity/ref material required to reconstruct the canonical current query/fact and the already-public 36-cell aggregate result.

Do not commit:

- raw source rows;
- raw respondent responses;
- raw weights;
- source `.sav` bytes;
- unnecessary carrier payload;
- new human-identifying material.

If exact canonical reconstruction requires committing a prohibited raw/governed value rather than opaque/content-addressed exact refs, fail closed and return that governance blocker. Do not silently redact identity-bearing material.

## Required runtime result

After sealing, the candidate must contain a no-Library runtime materializer which:

- reads only the banked content-addressed transport carrier;
- validates every manifest/shard hash;
- constructs ordinary current `EmpiricalQuerySpec` and `EmpiricalFact`;
- passes expected `object_id` and `content_hash` into canonical constructors so identity is independently recomputed;
- returns exactly the current query and fact refs;
- proves fact→query and replay/provenance/dependency closure;
- fails closed on missing/tampered/reordered/duplicated material where order is identity-bearing.

Once this seal is accepted, downstream E2B returns to **NO LIBRARY**.

## Non-authority

This disposition does not:

- change E2A empirical result semantics;
- change R1C identities;
- reopen FIELD FORGE;
- change PRE553 object schema;
- replace explicit canonical ref sequences with aggregate hashes in semantic identity;
- mint target-use permission;
- create structural relation meaning;
- authorize V3 transition;
- move PRE-MAIN or main.
