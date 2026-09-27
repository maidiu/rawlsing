# PYAT HQ118 — I1 M1 LEARNED EMPIRICAL ADJUDICATION RUNTIME — R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-pyat-hq118-i1-m1-runtime-r1`

Exact sealed HQ118 base:

`6cd63ce6cd5bf697f76ff7e62c4681f16c062832`

**AGENT TYPE: SOURCE-FREE CODE IMPLEMENTATION / GITHUB**

## Governing authority

Read:

- `HQ_HANDOFF/LATEST.json`
- `PYAT_CONTROL_ROOM/17_HQD118_M01_AND_LEARNED_WORLD_OWNER_ADOPTION.md`
- `PYAT_HQ118_FANIN_R1/00_HQ_JOIN.md`
- M1 return at `80eb1f42294ec7d5b4ce1066903db04b3d10ff25`
  - `01_M1_CONSTITUTION.md`
  - `02_TYPED_DISPOSITION_SCHEMA.md`
  - `03_RULE_BINDING_AND_AUTHORITY_LAW.md`
  - `04_NEGATIVE_STATE_CONSERVATION.tsv`
  - `05_IMPLEMENTATION_CONTRACT.md`
  - `06_HOSTILE_ACCEPTANCE_TEST_PLAN.md`

## Mission

Implement only the adopted M1 generic adjudication runtime:

`EXACT_I05_DISCOVERY_EVIDENCE + EXPLICIT_EXACT_FAMILY_RULE_BINDING -> LearnedEmpiricalDisposition@1.0.0`

Preferred write surface:

- `rawlsing_next/pre553_learned_empirical_adjudication.py`
- `rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py`

Minimal internal helpers/fixtures are allowed only if source-free and M1-local.

## Required ownership ceiling

M1 may own:

- exact input-bundle verification;
- exact DiscoveryResultReceipt/DiscoveryAuthority/frontier/fact/query/predicate closure verification;
- exact family-rule binding verification;
- exact validator registry dispatch by immutable identity;
- typed disposition construction;
- determinant/replay/explanation receipt;
- negative/evidence-state conservation.

M1 must NOT own:

- source decoding or source semantics;
- I03/I05 execution;
- universal substantive validation criteria;
- M2 release/publication;
- B5 lifecycle/currentness;
- structural admission;
- Field Forge relation truth;
- consumer permission;
- causal/actor/V3 semantics.

## No universal validator

Do not implement defaults for:

- minimum N;
- p-value/significance;
- effect size;
- association metric;
- weighting;
- missingness;
- comparability;
- pooling;
- estimator;
- causal/structural interpretation;
- semantic polarity.

The runtime must dispatch only to an exact validator identity already named by `M1FamilyRuleBinding`.

Use synthetic test validators to qualify generic mechanics.

## Required public objects

Implement exact logical equivalents of:

- `M1FamilyRuleBinding@1.0.0`
- `M1AdjudicationInputBundle@1.0.0`
- `FamilyValidationResult@1.0.0`
- `LearnedEmpiricalDisposition@1.0.0`
- structured determinant/explanation receipt as required by the adopted constitution.

The disposition must preserve separate axes for:
1. adjudication outcome;
2. upstream evidence/authority states.

Required outcome family:
- RULE_SATISFIED
- RULE_NOT_SATISFIED
- ABSTAINED
- BLOCKED
- UNRESOLVED
- INTEGRITY_FAILURE

Do not turn RULE_NOT_SATISFIED into negative semantic truth automatically.

## Required hostile tests

At minimum prove:

1. exact rule binding required;
2. no latest/default/fuzzy validator selection;
3. wrong claim-family/rule/authority binding fails closed;
4. missing authority closure fails closed;
5. fact/query/predicate/frontier/ref substitution fails closed;
6. replay/root tamper fails closed;
7. validator-required comparability premise absent -> blocked, not inferred;
8. validator-required composition premise absent -> blocked;
9. coverage-limited evidence cannot satisfy a completeness claim unless rule explicitly permits;
10. VALID_EMPTY preserved;
11. OBSERVED_ZERO preserved;
12. ZERO_SUPPORT preserved and distinct from OBSERVED_ZERO;
13. NONCOMPARABLE preserved;
14. BLOCKED/UNKNOWN/UNRESOLVED preserved;
15. INTEGRITY_FAILURE preserved;
16. RULE_SATISFIED does not imply structural/causal/V3 truth;
17. RULE_NOT_SATISFIED does not mint negative semantic truth;
18. deterministic identical input/rule -> identical disposition ref;
19. different governing validator authority changes disposition identity where constitution requires;
20. no M2/B5/Field Forge side effects or imports.

Also test that M01 exact object graphs can supply the required M1 input surfaces using source-free synthetic fixtures, without M1 calling M01 itself as a semantic owner.

## Hard prohibitions

No raw survey source.
No real-source execution.
No Candidate A/B/C/P2X.
No Field Forge mutation.
No M2/M3 implementation.
No source-semantic inference.
No product current-selection.

## Return

Own only:

`WORKER_RETURNS/PYAT-HQ118-I1-M1-RUNTIME-R1/`

Return:
- `00_RETURN.md`
- `01_CHANGED_FILES.tsv`
- `02_PUBLIC_API_AND_OWNER_RECEIPT.md`
- `03_HOSTILE_TEST_LEDGER.tsv`
- `04_M01_TO_M1_INTERFACE_RECEIPT.md`
- `05_REPLAY_AND_EXPLANATION_RECEIPT.md`
- `06_ANTI_PROMOTION_RECEIPT.md`

Success:

`PYAT_HQ118_I1_PASS__M1_GENERIC_ADJUDICATION_RUNTIME_SOURCE_FREE_GREEN__NO_SUBSTANTIVE_RULE_INVENTION`

Block:

`PYAT_HQ118_I1_BLOCKED__M1_RUNTIME_CANNOT_SATISFY_ADOPTED_CONSTITUTION_WITHOUT_SCOPE_WIDENING`
