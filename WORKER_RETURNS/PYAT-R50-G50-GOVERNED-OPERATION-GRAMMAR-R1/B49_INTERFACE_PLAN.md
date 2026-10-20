# B49 -> G50 candidate interface plan (compatibility proposal only)

## Contract versions

* `SourceDecisionBundle@candidate1` — source scope, item occurrences (id/label/unit/topology/forms/
  domain/target+conditioner roles/route/semantic state), measure plans, risk/route/unit/state map,
  authority refs/current selection, inventory completeness + gaps, held/unresolved.
* `ScientificGrammarPolicy@candidate1` — allowed/separate classes, role lists, J/K/D bounds,
  population-requires-weight, exclusions, validation/exploration/stop policies, owner/authority refs,
  grade.
* `ScientificFrontier@candidate1` — U_item/U_unit/U_app roots, symbolic E_pre multiset/root or
  NULL-with-cause, dispositions, deferred hierarchy, budget PARTIAL, source/policy identity.
* `NativeConstructionPlan@candidate1` — exact existing-owner refs (I05 grammar/authority/queries,
  C11/Batch/U43 boundary), unsupported classes.

## Normalization

1. Read B49's issued bundle; refuse incompatible schema versions.
2. Map B49 item occurrences 1:1 into `ItemOccurrence`; preserve unknown/held states as typed gaps.
3. Map B49 measure plans; POPULATION without weight/design stays held.
4. Do **not** copy B49 source permissions into the policy. The policy is a separate competent
   scientific artifact; G50 only enumerates from it.
5. Feed the bundle+policy into `g50.enumerate.enumerate_frontier`; compare the resulting E_pre root
   against the independent oracle before any native lowering.
6. Lower only native-supported operations through `g50.native_i05`; keep unsupported classes as
   `SPEC_ONLY_NATIVE_UNSUPPORTED` or `POLICY_ONLY` with exact fields.
7. Emit `NativeConstructionPlan@candidate1`; B49/U43 own C11/catalog/Batch materialization. G50 does
   not write them.

## Refusal rules

* incompatible schema / missing authority refs / unissued inventory -> typed refusal;
* B49 bundle claiming a complete original U root without independent issuance -> refused;
* any attempt to use the sourcefree synthetic bundle as original science -> refused by grade;
* policy grade `PROPOSED_TEST_ONLY` can never stamp `CURRENT_ISSUED`.

## Hand-back

Return the frontier root/ids, native rule coverage, canary matrix and exact unsupported fields to
the integration owner. Original measured occupancy remains 0 absent a separate S44 source-positive
receipt and competent D1–D5 issuance.
