# Replay and Explanation Receipt

## Deterministic identity chain

A successful M1 disposition is deterministic over:

1. full `M1AdjudicationInputBundle` preimage;
2. exact `M1FamilyRuleBinding` preimage;
3. exact validator registration identity;
4. exact `FamilyValidationResult` preimage;
5. authority and dependency closure;
6. conserved evidence/coverage/authority states;
7. exact prerequisite channel states;
8. exact validator determinants;
9. semantic ceiling;
10. the fixed all-false downstream-effect law.

The input bundle itself hashes the selected exact public-object preimages, frontier refs and discovery replay refs. It therefore cannot preserve its identity across exact fact/query/predicate/frontier/replay substitution.

## Structured determinant manifest

Each disposition carries an exact `M1DeterminantExplanationReceipt@1.0.0`.

Its determinant manifest includes:

- jurisdiction contract;
- claim family/rule;
- input bundle ref **and full preimage**;
- rule-binding ref and preimage, or typed missing binding;
- validator registration identity;
- FamilyValidationResult ref and preimage;
- receipt/authority/fact/validation-fact/query/predicate refs;
- frontier refs;
- discovery replay refs;
- coverage claims/states;
- conserved empirical state vector;
- conserved authority state vector;
- prerequisite state map;
- family validator determinant material;
- zero downstream effects.

`determinant_manifest_ref` is the exact hash/ref of this structured determinant material.

## Structured explanation

The explanation is machine-readable and records:

- what exact claim family/rule was adjudicated;
- exact requested scope;
- exact governing rule/binding/validator/current-selection authority;
- exact facts and validation facts;
- source universes, risk sets and measures;
- coverage states;
- upstream empirical states;
- prerequisite states;
- exact adjudication outcome and reason;
- validator-owned explanation material;
- semantic ceiling;
- the list of powers M1 does not have.

Narrative prose is not authoritative.

## Replay

The replay material binds:

- M1 contract;
- input bundle ref;
- exact binding or typed absence;
- validator registration identity;
- FamilyValidationResult ref;
- exact authority closure;
- exact dependency closure;
- determinant-manifest hash;
- semantic ceiling;
- downstream-effect firewall.

`verify_m1_disposition_replay(...)` rechecks the determinant/explanation/replay refs and the side-effect firewall and returns the exact replay content hash.

Qualification proves:

- same exact input + rule + registration -> same disposition ref;
- same exact input + rule -> same determinant ref;
- same exact input + rule -> same explanation ref;
- same exact input + rule -> same replay ref;
- exact replay/frontier substitution -> INTEGRITY_FAILURE;
- validator-authority change -> different disposition identity;
- that authority change may leave separately supplied P1 semantic claim identity unchanged.

This preserves the adopted separation:

`SEMANTIC_CLAIM_IDENTITY != M1_DISPOSITION_IDENTITY`.
