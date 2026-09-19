# FIABC-B01 — Duplicate or Ambiguous Owners

## Finding

No duplicate independent semantic owner was proved in the inspected current PRE553 core at base `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`.

The repository contains several places where the same semantic material can appear in more than one carrier, but the current contracts distinguish those carriers from semantic ownership.

## 1. Physical decoder versus semantic projection

`rawlsing_next/pre553_physical_decoder.py` owns physical incidence only. It explicitly does not map raw values to C11 response states or interpret labels.

`rawlsing_next/pre553_source_backed_c11_facade.py` requires an explicit `GovernedC11Projection`. Response, coordinate and weight meanings are supplied through exact caller-owned rules and authority refs. Therefore decoder metadata and projected semantic facts are not competing owners.

## 2. Physical slot with more than one semantic family

The source-backed facade contains an explicit duplicate-owner guard:

- each projected physical slot can emit response, coordinate and/or weight semantic families;
- if more than one family uses the same slot, an explicit `PhysicalSlotOwnerSet` is mandatory;
- the declared owner family set must exactly equal the emitted semantic owner family set;
- every owner authority must be in the projection's required authority closure and packaged snapshots;
- an implicit/unapproved second owner is rejected.

This is the strongest current executable evidence that multiple semantic uses of one physical column are not silently treated as multiple independent authorities.

## 3. AuthoritySnapshot versus AuthorityRegistry

`AuthoritySnapshot` is the immutable semantic permission/decision content. `AuthorityRegistry` is an exact-key validator/resolver. It cannot select latest/default authority or manufacture adjacent permissions. The registry is therefore enforcement infrastructure, not a duplicate semantic owner.

## 4. C11 release versus C11Repository

`rawlsing_next/pre553_c11_repository.py` states that repository presence is not semantic authority. It stores only I02-validated sealed releases and provides exact lookup. C11 persistence is therefore derivative of the validated release and its authority closure.

## 5. C11Repository versus SourceBackedC11SessionCache

The session cache is keyed by exact source SHA and projection cache identity, validates source/release consistency, and rebuilds through the governed validation path on a miss. It is a materialization optimization, not a second semantic owner.

## 6. I03 executor versus bounded GT1/GT2 adapter

`rawlsing_next/wave1_gt12_i03_positive_facts.py` explicitly says it does not create a new empirical engine. It binds one frozen Afrobarometer R5 Q86 canary to `execute_empirical_query` / `replay_empirical_query`. The resulting `EmpiricalFact` remains producer-owned I03 empirical truth.

Disposition: `SUPERSEDED_IMPLEMENTATION_FUNCTION_PRESERVED` is **not** asserted here because the bounded adapter is not shown to supersede generic I03; it is a special consumer/binder of it.

## 7. I03 facts versus I05 receipts

Exact I05 discovery calls I03 for candidate evaluation. Its output contains discovery receipts and exact references to I03 `EmpiricalFact` objects. The I05 module explicitly forbids diagnostic ranking/scoring from becoming empirical fact authority. Discovery receipt ownership is distinct from fact semantic ownership.

## 8. Exact I05 versus adaptive discovery

The two discovery modes own different execution contracts:

- exact I05: complete exact declared frontier;
- adaptive mode: exploratory search order over sealed evaluation units, with unvisited territory explicitly unknown.

Adaptive ranking has zero semantic-truth authority and cannot create a global negative claim. These are separate search/coverage contracts, not competing owners of the same empirical truth.

## 9. Repo-native payload/seal versus ordinary query/fact objects

`pre553_repo_native_current_payload.py` and `pre553_repo_native_seal.py` reconstruct or transport ordinary `EmpiricalQuerySpec` / `EmpiricalFact` identities. Both explicitly deny authority minting or an alternate empirical engine. They are carriers, not independent semantic owners.

## Ambiguity retained

The current tree contains both generic PRE553 components and bounded/historical integration surfaces. B01 proves the owner distinction at the implementation-contract level, but does not prove which of those surviving surfaces every P2X or A/B/C court process actually invokes. That live-consumption question is intentionally left to FIABC-B02/B03 rather than converting survivorship into an ownership claim.
