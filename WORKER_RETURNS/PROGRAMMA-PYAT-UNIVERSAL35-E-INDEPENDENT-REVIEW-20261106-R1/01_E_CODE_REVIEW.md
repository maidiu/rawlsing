# 01 — E code/owner review detail

## Owner chain

`pre553_field_forge_empirical_ingress.ingest_empirical_fact` is a thin facade:

1. `_exact_fact_query` checks object classes, fact/query content hashes, and
   `fact.empirical_query_spec_ref == query.ref`.
2. It checks two-target arity/target-ref count.
3. It delegates to
   `field_forge_conditional_support.produce_exact_conditional_support_profile`.
4. On success, optionally delegates to
   `gt12_c_to_d_relation_bridge.bridge_gt12_c_relation_to_d_evidence` only.
5. It returns the frozen `ExactConditionalSupportProfile` or a typed refusal.
6. `structural_grant=False`; `structural_state=WITHHELD...`; no
   `admit_gt12_c_relation` or structural-admission call.

The implementation contains no fixture count constants, source-ID branches,
target-role invention, or alternate statistics. Test fixture expected values are
test-only.

## Existing-owner checks (what is already covered)

`field_forge_conditional_support._validate_common_closure` checks:

- fact/query types and content hashes;
- fact→query ref exact equality;
- risk-set exact equality;
- one exact identical universe and SINGLE_UNIVERSE grain;
- RAW query/fact and null weighted fields;
- query authority closure subset of fact authority closure;
- producer replay root vs fact replay ref;
- fact dependency closure includes query and replay;
- nonempty provenance retained in dependencies;
- target plan: arity 2, SEMANTIC_ORDERED, exact target role order, SCALAR_SINGULAR,
  exact domains, replay refs, complete cell domain, target domain identity;
- cell counts sum to numerator/resolved support and do not exceed denominator;
- cell zero/positive state consistency.

## Missing link (defect)

Neither E nor the existing owner compares:

- `fact.condition_predicate_ref` ↔ `query.condition_predicate_ref`;
- `fact.measure_basis_ref` ↔ `query.measure_basis_ref`;
- `fact.response_state_semantics_ref` ↔ query grain response-state semantics;
- `fact.source_scope_mode` exactly ↔ query grain source scope;
- `fact.measure_kind` exactly ↔ query grain measure kind.

The owner accepts `None` for fact source scope/measure kind and does not compare
the condition/measure/response refs. E's D contract lists these as required exact
fields, so the ingress claim of exact semantic linkage is not enforced.

Reproducer `evidence/e_ingress_defect_probe.json` creates five self-consistent
facts with the same bound query and different semantic fields. All five return
`CONDITIONAL_SUPPORT_PROFILE` with empty refusal; only the relation ref changes
because the fact ref changes. This is a false positive ingress admission.

## Minimal repair guidance

Apply exact equality checks in E `_exact_fact_query` before owner delegation (see
00_RETURN section). Raise `FieldForgeEmpiricalIngressError` on mismatch or return a
consistent typed refusal. Add one negative test per field and a positive control.
Do not change the existing owner unless a separate owner decision is made; do not
weaken arity/role/cell/weighted/provenance/structural-withheld behavior.

## Honest status distinctions

- The reviewed 11+25 tests and selftest pass; that is author-focused test evidence,
  not a waiver of the missing linkage gate.
- GT2 is a real 2-target RAW existing-owner limit; one/3+ targets are refusals,
  not generic F4/N10E/all35 completion.
- D authentic facts are NOT_RUN/NOT_RECEIVED; no native acceptance.
- Structural/GT12-D admission is not issued; `structural_grant` remains false.
- The default permission tuple is a caller ceiling, not source authority.
