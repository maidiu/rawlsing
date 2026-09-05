# GT12 E2B R3 — ADOPTED PUBLICATION/GOVERNANCE BINDING IMPLEMENTATION WAVE R1

Exact working start for all workers:

`8100f700737ce33706b4678974543f7bb8d33569`

Instruction evidence only. Worker ancestry begins at the exact start above.

## Frozen HQ adoption

Adoption terminal:

`ADOPTED__GT12_E2B_R3_MINIMAL_F1_PUBLICATION_GOVERNANCE_BINDING_CURRENT`

Machine record:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/E2B_R3_PUBLICATION_GOVERNANCE_ADOPTION_R1/01_ADOPTION.json`

Human disposition:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/E2B_R3_PUBLICATION_GOVERNANCE_ADOPTION_R1/00_VOZHD_ADOPTION.md`

Exact adopted identities:

- governed use:
  `GT12_GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_F1_CONTEXT_PUBLICATION@1`

- V554 rule:
  `GT12_V554_SIG004_ADMITTED_RELATION_CONTEXT_PUBLICATION_RULE@1.0.0`
  hash:
  `da431544e57ed4b418cd746be3f0a9aa486cd3c2fb2007a022005821b25e194b`

- publication authority:
  `GT12_RELATION_V554_TO_V557_F1_CONTEXT_PUBLICATION_AUTHORITY@1.0.0`
  hash:
  `1b2c1238139287e30acaa418e28967585a34a7fae9c937a9322b7c9e9a76322a`

- V557 current binding:
  `GT12_CAN003_V557_F1_CONTEXT_ONLY_CURRENT_BINDING@1.0.0`
  hash:
  `b071d9b34825b2c73fefa47cdef0ba23003d79cf5a2fa78cab802e02ee0cd6f4`

- immutable bundle:
  `GT12_E2B_R3_CURRENT_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0`
  hash:
  `f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14`

- adoption content hash:
  `ff3c0db1ee346b176f240523f36048d88beb6216722988ea087040b4840cd492`

Publication family exactly:

`("F1",)`

V557:

`ALLOW_CONTEXT_ONLY`

uses exactly:

`("CONTEXT",)`

The V557 binding is an exact current selection/narrowing of accepted CAN-003 semantics. It does not create a new V557 semantic regime.

The already-adopted permission translator remains separate:

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

hash:

`d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`

---

# WORKER I1 — ADOPTED BINDING IMPLEMENTATION R1

Branch:

`agent/rabochii-gt12-e2b-r3-adopted-binding-implementation-r1`

Profile:

`IMPLEMENT -> VERIFY_REGRESSION`

No Library.
No source data.
No empirical reexecution.
No real E2B terminal execution.
No new authority.
No authority redesign.

## First action

1. verify exact HEAD;
2. read only this worker section and the two adopted authority files;
3. inspect only:
   - `rawlsing_next/gt12_d_to_m4_typed_bridge.py`
   - `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py`
   - `rawlsing_next/m1_temporal_v554_admission_dedup.py`
   - `rawlsing_next/m4_v557_v558_publication_repository.py`
   - `rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py`
   - directly relevant tests;
4. externalize the first coherent implementation checkpoint early.

## Mission A — production current-binding provider

Implement one small repo-native module, preferably:

`rawlsing_next/gt12_e2b_publication_governance_binding.py`

or an equivalently narrow module.

It must:

- encode the exact adopted semantic materials, refs, and hashes;
- recompute every adopted semantic hash using the repository canonical semantic hash law;
- fail closed if any embedded material drifts;
- expose one no-argument current provider;
- return one immutable typed or structurally exact bundle;
- derive:
  - `governed_use_id`
  - `v554_rule_ref`
  from the adopted publication authority;
- construct the exact M4 `AuthorityRef` for the adopted V557 current binding;
- expose no caller-selected authority, path, current selector, permission tuple, object-family set, or rule override.

Do not read the authority JSON from arbitrary caller paths at runtime.
A fixed repo-native semantic constant/provider is the current selection.

## Mission B — real E2B entry binding

Change the real actual-object E2B entry so callers no longer supply:

- `governed_use_id`
- `v554_rule_ref`
- `publication_authority`
- `v557_authority_ref`

The real entry must accept only the actual current ordinary query/fact objects and project all four values from the adopted current bundle internally.

Low-level generic bridge APIs may remain parameterized if needed for generic tests; the production/current real entry may not expose those knobs.

The real entry must still derive CONTEXT permission through the separately adopted permission translator. Do not bake permission atoms into the new bundle as new authority.

## Mission C — Astra target-ref representation repair

Astra identified and HQ independently confirmed a representation bug in:

`rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py::require_current_r1c_actual_objects`

Current logic normalizes topology component refs to `ExactRef`, then compares them directly to `query.target_refs`.

But `CanonicalSemanticObject` canonicalizes ordinary semantic-field ExactRefs into dictionary material. Therefore ordinary `query.target_refs` are canonical dictionaries, not `ExactRef` instances.

Repair this comparison in the smallest representation-correct way.

Requirements:

- normalize BOTH sides to the same exact-ref representation before equality;
- preserve exact Q86B -> Q86A order;
- do not weaken content-hash/object-id/kind equality;
- do not special-case the current hash;
- synthetic reversed/mismatched target tests must still fail;
- add an actual-current repo-native test proving the exact current query passes this boundary.

This is a harness/interface repair only. Do not alter PRE553 identity law.

## Exact publication law

The provider must force:

- producer = `V554`
- publisher = `V557`
- decision = `AUTHORIZED`
- allowed object families = exactly `("F1",)`
- conditions = exactly empty
- route = `V554_TO_V557_DIRECT`
- relation M1 contract = `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- basis = `ADMITTED_FIELD_FORGE_RELATION`
- signature = `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`

Any F2/B1 publication attempt fails.

Any nonempty condition set fails this adopted contract rather than widening families.

## Exact V557 law

The provider's M4 AuthorityRef must be exactly:

- id:
  `GT12_CAN003_V557_F1_CONTEXT_ONLY_CURRENT_BINDING`
- version:
  `1.0.0`
- hash:
  `b071d9b34825b2c73fefa47cdef0ba23003d79cf5a2fa78cab802e02ee0cd6f4`

The semantic binding must remain:

- source authority CAN-003 / CAN-003.v1;
- producer V554;
- semantic class F1;
- source stage `M1_RELATION_V554_TO_V557`;
- `ALLOW_CONTEXT_ONLY`;
- `("CONTEXT",)`;
- no exception.

## Hostile tests

At minimum prove:

1. all adopted hash inputs recompute exactly;
2. bundle hash recomputes exactly;
3. adoption hash recomputes exactly;
4. no-argument current provider returns exact adopted bundle;
5. caller cannot override use/rule/publication/V557 authority;
6. governed-use drift fails;
7. rule id/version/hash drift fails;
8. publication authority hash drift fails;
9. producer/publisher/decision drift fails;
10. families empty fail;
11. any family set other than exactly F1 fails;
12. nonempty conditions fail this binding;
13. F2/B1 injection fails;
14. V557 authority id/version/hash drift fails;
15. REVIEW/ACTIVE_CAUSAL fails;
16. V553/V555/V556 fails;
17. translator cannot impersonate V557 authority;
18. real E2B entry signature exposes no four authority-selection parameters;
19. actual current repo-native query/fact pass exact current-object boundary after target-ref normalization;
20. wrong target order/ref still fails;
21. ordinary current object identity remains exact.

Run the smallest relevant inherited regression set plus this hostile court.

## Terminal

PASS only as:

`PASS__GT12_E2B_R3_ADOPTED_PUBLICATION_GOVERNANCE_BINDING_IMPLEMENTED__REAL_ENTRY_CALLER_NONSELECTABLE`

Return exact terminal SHA and tests/court evidence.

Do not execute the final real E2B chain in this worker.

---

# WORKER I2 — ADOPTED BINDING HOSTILE AUDIT R1

Branch:

`agent/rabochii-gt12-e2b-r3-adopted-binding-hostile-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

No production changes.
No real E2B execution.

## Mission

Independently hostile-audit the exact HQ adoption at working start.

Do not re-prove H1's broad absence search or H2's full contract from scratch.
Attack the concrete adopted values.

Questions:

1. Do all recorded rule/publication/V557/bundle/adoption hashes recompute under repository semantic-hash law?
2. Is the V554 rule merely binding accepted SIG-004 behavior, or does it accidentally introduce new semantics?
3. Is F1-only publication sufficient for the exact no-condition positive path?
4. Does excluding B1/F2 preserve the actual V557/V558 path?
5. Is the publication authority exactly relation/use-specific and non-widening?
6. Is the CAN-003 V557 binding a lawful exact current selection/narrowing of accepted semantics rather than unauthorized semantic extension?
7. Does CAN-003 explicitly cover CONTEXT-only governance and monotonic narrowing sufficient for this use?
8. Does the new V557 binding remain distinct from the PRE-V3->M4 permission translator?
9. Can any adopted component be used to authorize REVIEW, ACTIVE_CAUSAL, V553/V555/V556, actor, V3 positive, or V2?
10. Are governed use and V554 rule correctly redundant projections from publication authority rather than independent authority sources?
11. Does the bundle prevent cross-provider mixing/drift?
12. Is the existing production API capable of implementing the adoption mechanically without reinterpretation?

Explicitly check the accepted CAN-003 artifact blob:

`64fb18f01a1caa69fd3553dc62b056c0efe1ff47`

and distinguish its broader validation vocabulary from the exact narrowed current binding.

The fact that CAN-003 knows REVIEW or ACTIVE_CAUSAL vocabulary does not itself invalidate the binding; the question is whether this adopted current selection can widen to those states.

## Terminal

PASS only as:

`PASS__GT12_E2B_R3_ADOPTED_PUBLICATION_GOVERNANCE_BINDING_HOSTILE_AUDIT__LAWFUL_NONWIDENING`

Otherwise:

`FAIL__GT12_E2B_R3_ADOPTED_PUBLICATION_GOVERNANCE_BINDING_HOSTILE_AUDIT__EXACT_DEFECT`

Commit only:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/E2B_R3_ADOPTED_BINDING_HOSTILE_AUDIT_R1/00_RETURN.md`

Return exact terminal SHA and exact dispositions.

---

# FAN-IN

I1 and I2 run concurrently.

If both pass:

1. bank implementation and audit;
2. run one combined regression on the integrated tree if needed;
3. resume ONLY the real E2B delta from accepted repo-native current objects;
4. do not rerun empirical GT2;
5. persist actual E2B execution checkpoint immediately;
6. then consume G's already-completed final hostile-audit preflight and perform only the remaining E2B audit delta.
