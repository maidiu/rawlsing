# PYAT HQ122 — J2I ROLE / CERTIFICATION MINIMAL SOURCE-FREE IMPLEMENTATION — R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-pyat-hq122-j2i-role-certification-implementation-r1`

Exact sealed HQ122 base:

`bd766654fac632190a5c62c68ba98c909c395c3f`

**AGENT TYPE: SOURCE-FREE CODE IMPLEMENTATION / GITHUB**

## Governing authority

Read:

- `HQ_HANDOFF/LATEST.json`
- `PYAT_CONTROL_ROOM/21_HQD122_J_ROLE_CERTIFICATION_SUCCESSION_ADOPTION.md`
- J2R return at `79faa4969469a25ad8263835380b412b90bbe076`:
  - `01_FAMILY_ITEM_ROLE_SUCCESSION_CONTRACT.md`
  - `02_ROLE_VOCABULARY_AND_MAPPING.tsv`
  - `03_M1_CERTIFICATION_CONTRIBUTION_RULE.md`
  - `04_PREREQUISITE_AND_CONSUMER_BINDING.md`
  - `06_IMPLEMENTATION_CONTRACT.md`
  - `07_HOSTILE_TEST_PLAN.tsv`

Current generic runtimes:
- `rawlsing_next/pre553_component_authority_vector.py`
- `rawlsing_next/pre553_learned_empirical_adjudication.py`
- `rawlsing_next/pre553_learned_world_composition.py`

## Mission

Implement only the HQ-adopted J role/certification succession law.

The required current path is:

```text
exact current J subject + exact governed component set
+ exact current family-role authority/mapping
-> ComponentAuthorityVectorReceipt(J_FAMILY_ITEM_ROLE)
-> M1PrerequisiteChannel("j_family_item_role_vector")
+ exact current component evidence/match/eligibility premises
-> PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0
-> exact ordered six-state contribution determinant
-> existing M1 FamilyValidationResult / LearnedEmpiricalDisposition
```

This is the last source-free implementation needed to close the historical J role/certification succession burden.

## Preferred write surface

Prefer adding:

- `rawlsing_next/pre553_j_role_certification.py`
- `rawlsing_next/tests/test_pre553_j_role_certification.py`

Modify generic modules only if absolutely required by a proved integration defect.

Do not widen M1 core schema unless the adopted contract is impossible to realize otherwise. If that happens, stop and return the exact witness.

## Part A — family-role vector producer

Implement one exact source-free producer/adapter for:

`PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0`

It must accept only explicit exact inputs:

- exact current joint subject ref;
- exact governed component IDs/order;
- exact current family-role authority ref;
- exact mapping contract ref;
- exact predecessor/current component mapping refs where succession is invoked;
- exact current per-component role assignments or typed negative/unresolved states;
- exact value-authority refs;
- exact replay/dependency refs.

It must emit one:

`ComponentAuthorityVectorReceipt@1.0.0`

under authority dimension:

`J_FAMILY_ITEM_ROLE`.

Exact positive role vocabulary:

- exception_case
- elective_case
- social_condition
- family_size_condition
- economic_condition
- target_case

No synonym expansion.

No fallback to target_case.

No ordinal/name/proximity inference.

`ComponentAuthorityBinding.role` is nonsemantic metadata only.

The semantic positive value must be represented through the exact `authoritative_value_digest(role_token)` plus exact `value_authority_ref`.

Typed states must preserve:

- VALUE
- UNRESOLVED
- DENIED
- NONCOMPARABLE

A required role premise may not be satisfied by `GOVERNED_EMPTY`.

## Part B — named M1 prerequisite channel

Implement a helper/builder for:

channel id:
`j_family_item_role_vector`

channel kind:
`PRE553_J_FAMILY_ITEM_ROLE_VECTOR`

Required relation kinds:
- `GOVERNED_FAMILY_ITEM_ROLE_FOR_COMPONENT_SET`
- `ROLE_VECTOR_PREMISE_FOR_J_CERTIFICATION`

The channel must carry exact:

- role-vector ref;
- role contract ref;
- mapping refs;
- replay refs;
- exact adopted role authority;
- exact current subject/family authority;
- exact per-value authority refs as required;
- exact governed component IDs;
- exact role vocabulary/version;
- exact semantic ceiling.

Channel SATISFIED only when:
- exact authorities match;
- component coverage is complete and one-to-one;
- every required role binding is VALUE;
- every VALUE digest resolves to one allowed role token;
- mapping/replay closure is exact.

Missing/unknown role -> UNRESOLVED.

Denied/noncomparable/conflicting/ambiguous/tampered role -> BLOCKED or stronger typed state.

## Part C — exact J M1 validator

Register exactly:

claim family:
`PRE553_J_JOINT_RELATION_EVIDENCE`

claim rule:
`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0`

validator algorithm:
`PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0`

selection purpose:
`CURRENT_GOVERNED_USE`

No latest/default/fuzzy selection.

The validator must consume:
- the exact named role-vector prerequisite channel;
- exact current component match/evidence/eligibility premises supplied by the caller;
- exact component set/order;
- exact replay/authority refs.

It must derive exactly one contribution token per governed component:

- relation_component
- context_component
- special_or_missing_component
- explained_nonrelation_component
- blocked_component
- unresolved_component

## Exact contribution law

For each component:

1. authority/mapping conflict, ambiguity or explicit denial -> `blocked_component`
2. missing/unknown/unresolved role/evidence premise -> `unresolved_component`
3. exact special/missing response premise -> `special_or_missing_component`
4. exact governed context/nonrelation premise -> `explained_nonrelation_component`
5. exact accepted relation match + VALUE role authority + relation eligibility + no context/nonrelation exclusion -> `relation_component`
6. exact accepted match otherwise -> `context_component`
7. otherwise -> `unresolved_component`

Negative/unknown role authority can never promote to `relation_component`.

## Aggregate M1 outcome law

Freeze exact precedence:

1. integrity mismatch -> `INTEGRITY_FAILURE`
2. blocked_count > 0 -> `BLOCKED`
3. unresolved_count > 0 -> `UNRESOLVED`
4. relation_count < 2 -> `RULE_NOT_SATISFIED` / `INSUFFICIENT_JOINT_RELATION_COMPONENTS`
5. relation_count >= 2 and context_count > 0 -> `RULE_SATISFIED` / `J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT`
6. relation_count >= 2 and context_count == 0 -> `RULE_SATISFIED` / `J_JOINT_RELATION_EVIDENCE`

Exact context-like set:

- context_component
- special_or_missing_component
- explained_nonrelation_component

## Determinant/replay law

The M1 result determinant must freeze exact ordered:

- component ref;
- ordinal;
- family role token or typed state;
- contribution token;
- evidence-match disposition;
- relation-eligibility disposition;
- authority refs;
- dependency refs;
- negative/limit refs.

Also bind:

- role-vector ref;
- role-vector coverage proof hash;
- relation/context/blocked/unresolved counts;
- contribution rule id/version;
- prerequisite-channel ref;
- replay-contract ref.

No second contribution-vector object is required.

## Required hostile qualification

At minimum implement and pass every case from J2R `07_HOSTILE_TEST_PLAN.tsv`, plus:

1. deterministic role-vector reload equality;
2. deterministic M1 result replay equality;
3. exact validator registration mismatch rejection;
4. exact current-selection authority mismatch rejection;
5. unknown role token fails closed;
6. missing mapping fails closed;
7. duplicate/ambiguous role binding fails closed;
8. component-set mismatch fails closed;
9. role-vector replay mismatch fails closed;
10. relation-bearing matched component;
11. matched context component;
12. special/missing component;
13. governed nonrelation/explained context;
14. ambiguous match;
15. unresolved match;
16. one relation component -> RULE_NOT_SATISFIED;
17. two relation components -> RULE_SATISFIED;
18. relation + context -> RULE_SATISFIED_WITH_CONTEXT;
19. negative role authority cannot relation-promote;
20. changed family-role authority changes exact determinant/binding identity;
21. zero production side effects;
22. no Field Forge imports/effects;
23. no B5 imports/effects for certification;
24. no historical packet executor dependency;
25. no raw-source access.

Also rerun targeted current regressions for:
- component authority vector;
- M1 learned empirical adjudication;
- I4 learned-world composition.

## Completion meaning

Success closes the last source-free implementation burden in the six-stage conservation theorem.

It does NOT prove:

- positive role occupancy for all 1,411 J candidates;
- live source coadministration/applicability/load;
- positive current J-family execution authority;
- all-source J execution;
- Field Forge relation truth.

Those remain the later current-scope source-capable authority/load court.

## Hard prohibitions

No raw survey source.
No real respondent execution.
No Candidate A/B/C.
No measured P2X.
No source-family role inference.
No historical target_case fallback.
No M1 schema widening without stopping on a proved defect.
No Field Forge mutation.
No B5 mutation.
No product publication/current-selection.
No V3/person semantics.

## Return

Own only:

`WORKER_RETURNS/PYAT-HQ122-J2I-ROLE-CERTIFICATION-IMPLEMENTATION-R1/`

Required:

- `00_RETURN.md`
- `01_CHANGED_FILES.tsv`
- `02_ROLE_VECTOR_PRODUCER_RECEIPT.md`
- `03_M1_PREREQUISITE_CHANNEL_RECEIPT.md`
- `04_J_VALIDATOR_AND_DETERMINANT_RECEIPT.md`
- `05_HOSTILE_TEST_LEDGER.tsv`
- `06_REPLAY_DETERMINISM_RECEIPT.md`
- `07_ANTI_INFERENCE_AND_NONPROMOTION_RECEIPT.md`
- `08_SIX_STAGE_SOURCE_FREE_COMPLETION_PACKET.md`

Success:

`PYAT_HQ122_J2I_PASS__J_ROLE_CERTIFICATION_SUCCESSION_RUNTIME_SOURCE_FREE_GREEN__READY_FOR_SIX_STAGE_COMPLETION_COURT`

Block:

`PYAT_HQ122_J2I_BLOCKED__ADOPTED_ROLE_CERTIFICATION_SUCCESSION_CANNOT_BE_IMPLEMENTED_WITHOUT_SCOPE_OR_SCHEMA_WIDENING`
