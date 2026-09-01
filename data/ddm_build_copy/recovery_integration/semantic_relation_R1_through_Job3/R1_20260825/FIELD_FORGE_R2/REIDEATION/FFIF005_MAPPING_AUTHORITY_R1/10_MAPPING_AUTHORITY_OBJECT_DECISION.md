# FFIF005 — MAPPING AUTHORITY OBJECT DECISION

## 1. Decision

`NO_NEW_MAPPING_AUTHORITY_TYPE`.

The required function is losslessly expressible through:

1. exact source/project semantic identity where available;
2. TTAR for every nonidentity correspondence/group/order/coarsening/transport-equivalence proposition;
3. PRA/other role authority where a local analytic or social-position role is invoked;
4. a normalized claim identity;
5. the FFIF003 transport contract, extended with an outcome-blind mapping-plan block.

## 2. Why a dedicated MAR is rejected

A candidate `MAPPING_AUTHORITY_RECEIPT` would contain endpoint refs, authority basis, map family, selection rule, firewall, alternatives, TTAR/PRA refs, and validity.

Its fields split cleanly into two existing owners:

- semantic permission fields already belong to TTAR/PRA/source authority;
- design/selection/test fields already belong to the transport contract.

Making MAR an authority would create at least three hazards:

1. **duplicate semantic sovereignty** — MAR could admit an edge TTAR would reject;
2. **authority laundering** — a complete-looking map plan could be consumed as evidence that its edges are lawful;
3. **lifecycle divergence** — TTAR/PRA supersession might not invalidate a separately authoritative MAR.

## 3. Materialized receipt that may still be useful

Rawlsing may materialize a `MAPPING_PLAN_RECEIPT` (`MPR`) for replay, preregistration, and firewall attestation.

Exact status:

`DESIGN_AND_SELECTION_RECEIPT__NO_INDEPENDENT_SEMANTIC_AUTHORITY`.

It is valid only if every edge resolves to exact identity or typed authority and every role resolves to its competent owner. MPR validity is downstream of those refs and is automatically invalidated by their supersession.

## 4. Minimal MPR schema

- `mapping_plan_id`
- `transport_claim_ref` / `claim_identity_hash`
- exact origin/destination context, local-view, local-object, invariant, risk-set, and estimand refs/hashes
- candidate-generation log
- correspondence type per edge
- exact edge authority refs
- rejected-edge log
- admissible family spec/cardinality/bounds
- selection feature manifest and authority refs
- selection/tie/unresolved rule
- selected map or retained finite set
- target-outcome firewall and seal time/hash
- alternative maps and null family
- multiplicity decision rule/status
- allowed invariants and forbidden inferences
- validity/invalidation, provenance, and supersession

The MPR must not contain a field whose value alone says `AUTHORIZED=true`. Authorization is resolved from the typed refs.

## 5. Irreducibility test

| function | existing owner | residue requiring new authority? |
|---|---|---|
| exact semantic identity | source/project authority | no |
| bounded nonidentity treatment | TTAR | no |
| local social-position function | PRA | no |
| claim/invariant identity | claim manifest | no |
| candidate enumeration and exclusions | transport mapping plan | no |
| outcome-blind selection | transport mapping plan executing authorized rules | no |
| target firewall/preregistration | transport mapping plan | no |
| alternative-map/multiplicity/null test | transport contract/result | no |
| homology/structural interpretation | downstream court | no |

No irreducible authority residue survives.

## 6. Supersession

An MPR becomes invalid if any endpoint hash, TTAR, PRA/role receipt, claim scope, estimand/risk set, selection feature authority, or map-family rule is superseded. It is never silently edited; a new plan version references and preserves the old one.

## 7. Terminal sentence

**Materialize the bridge for audit, but do not crown the bridge as a new source of meaning.**

