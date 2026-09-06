# GT3/GT4 O2 — SHARED I03 / M1->M4 AUTHORITY BOUNDARY REPAIR R1 — RETURN

Terminal disposition:

`PASS__GT34_O2_ASTRA002_SHARED_AUTHORITY_BOUNDARIES_CLOSED__NO_AUTHORITY_WIDENING`

Exact working-ancestry start:

`3aaf6759f270c9b730db5d09bb6a87f92ec34345`

Instruction ref:

`15f1a470843ffe322c054a115c0685cb8a4e26e8`

The instruction ref was evidence only. All implementation ancestry began from the exact working start above.

The exact terminal branch SHA is reported by final branch readback after this return is committed; the return file cannot contain its own commit SHA without changing that SHA.

---

# Holding

ASTRA-002 is closed at both shared operation boundaries without changing accepted authority meaning.

The repair does **not** add semantic authority.

It makes two previously weak shared gates enforce already-existing authority law:

1. ordinary/shared I03 execution now requires exact authority fitness rather than treating a resolvable `ALLOW` snapshot as sufficient by itself;
2. shared relation M1->M4 publication no longer accepts caller-selected producer-use labels as authority.

The adopted GT12 relation path remains exactly CONTEXT-only because its existing adopted permission-translation authority derives that use.

The shared M1->M4 adapter itself does **not** hardcode CONTEXT and does not impose GT2 permission semantics on the empirical M1 contract or on any future separately governed relation contract.

---

# 1. ASTRA-002 defect reproduced from banked audit

Astra proved one root enforcement defect in two shared APIs.

## I03

The ordinary query executor validated:
- exact object identity;
- authority-reference existence;
- positive `ALLOW` state;

but did not itself require the authority to be fit for:
- the exact public object family;
- the exact source/universe scope;
- the exact operation/use.

Therefore a syntactically valid, correctly hashed ALLOW authority could reach execution even when a stronger GT12 builder would reject it.

## M1->M4

`structural_objects_from_accepted_m1(...)` accepted a caller-provided `producer_allowed_uses` tuple on the relation branch.

Thus a caller could provide a correct-looking raw label such as `REVIEW` even though the governed GT12 relation wrapper correctly derives only `("CONTEXT",)` from the adopted permission-translation authority.

The defect was enforcement placement, not missing semantic authority.

---

# 2. Shared I03 boundary repair

Production file:

`rawlsing_next/pre553_empirical_query.py`

Primary repair commit:

`4e3a6058534e67033ad490f83807f8bbb7468331`

Added the shared boundary validator:

`_require_exact_i03_authority_fitness(...)`

The ordinary exported:

`execute_empirical_query(...)`

now invokes this validator before target-plan evaluation.

## Exact query-authority requirements

For every exact query authority ref, the shared executor now requires:

- exact authority ref resolution;
- positive authority state under existing `require_positive_authority`;
- authority kind = `PREDICATE_GRAMMAR`;
- exact governed operation;
- governed family includes `EmpiricalPredicate@1.0.0`;
- governed family includes `EmpiricalQuerySpec@1.0.0`;
- governed family includes `EmpiricalFact@1.0.0`;
- exact source/universe scope for every query universe.

There is no label, latest, nearest, or generic-ALLOW fallback.

## Operation binding without identity mutation

If a query explicitly carries `requested_output_grain.query_operation`, that exact operation is required.

For existing current queries that predate an explicit operation field, the shared gate accepts only the identity-preserving compatibility case where:

- every exact query authority has exactly one governed operation; and
- all exact query authorities agree on that one operation.

An ambiguous multi-operation or disagreeing authority set fails closed.

This closes the shared operation check without modifying the current GT1/GT2 query semantic projection.

## Predicate grammar linkage

The predicate's exact grammar authority must be one of the query's exact query-authority refs.

A positive but unrelated grammar authority cannot be substituted.

## Exact target-use permission

Target-use material is optional only for query contracts that do not declare a target-use permission model.

If any one of:
- `target_use_ref`;
- `target_use_authority_ref`;
- `target_use_operation`;

is declared, all three are required.

The shared executor then requires:

- exact target-use ref;
- exact target-use authority ref;
- exact target-use operation;
- target-use authority present in the query's exact authority closure;
- target-use ref present in the query's exact dependency closure;
- authority kind = `TARGET_USE_PERMISSION`;
- governed family includes `EmpiricalFact@1.0.0`;
- exact source/universe scope;
- exact target-use scope;
- exact operation.

Thus a correct-looking positive target-use authority for another use cannot authorize the query.

## Typed negative preservation

Authority-fitness failures remain typed nonpositive I03 results under the preexisting failure law.

The hostile controls observed:

`MISSING_REQUIRED_AUTHORITY`

rather than positive `SUPPORTED`.

No new negative state was invented.

---

# 3. Shared M1->M4 boundary repair

Production file:

`rawlsing_next/m4_m1_evaluation_binding.py`

Primary boundary commit:

`5187c55fb91000360f886c08077506811db3a40d`

Capability-hardening commit:

`e05876fceae467482a4d98c082cd17496ff81de7`

GT12 governed wrapper integration:

`rawlsing_next/gt12_d_to_m4_typed_bridge.py`

Integration commit:

`3400c3b97a423a4e8a5d68a08cbdfaf4972f220b`

## New validated binding contract

Introduced:

`ValidatedM1ProducerUseBinding`

This is an enforcement capability, not semantic authority.

For the relation M1 contract, the shared adapter no longer accepts raw `producer_allowed_uses`.

Instead it requires an exact validated capability that is:

- issued only through the internal governed-binding issuer;
- bound to the exact relation M1 contract;
- bound to the exact M1 evaluation semantic material;
- bound to the authority binding's exact content hash;
- bound to the exact upstream relation-admission ref;
- bound to the exact FIELD FORGE relation ref;
- immutable after issuance.

The capability is evaluation-specific. A capability for another M1 evaluation cannot be replayed against the current evaluation.

The public/supported shared adapter cannot turn a raw mapping or raw use tuple into this capability.

## Relation raw-label rejection

For the relation branch, direct shared calls supplying any raw producer-use tuple now fail before structural-object materialization.

Hostile controls prove rejection of:

- `("REVIEW",)`;
- `("ACTIVE_CAUSAL",)`;
- `("CONTEXT", "REVIEW")`;
- raw `("CONTEXT",)` itself;
- absent validated binding;
- an unsealed caller-constructed token;
- a raw authority-binding mapping substituted for the token.

This is intentional:

**even the correct label is not authority.**

## Exact GT12 governed issuance

The existing GT12 wrapper still performs, before capability issuance:

1. `derive_adopted_permission_binding(...)`;
2. exact translation-authority ID/version/hash verification;
3. exact adoption-receipt ID/version/hash verification;
4. exact positive PRE-V3 relation-admission validation;
5. exact relation family/owner/hash validation;
6. exact source/risk-set/participant validation;
7. exact target-use and singleton permission-ceiling validation;
8. exact downstream-use shape validation.

Only after those existing validations does the wrapper issue the M1-evaluation-specific capability and call the shared adapter.

Existing hostile tests continue to reject:
- wrong translation-authority identity/version/hash;
- wrong adoption-receipt identity/hash;
- wrong PRE-V3 authority/rule/current selection;
- wrong relation family/owner/hash;
- wrong source/risk set/participant order;
- widened upstream permission;
- nonpositive admission.

## No global CONTEXT rule

The shared adapter does not contain a rule saying relation M1 means CONTEXT.

The capability carries the producer-use tuple that was proved by its governing wrapper.

The current adopted GT12 authority happens to prove:

`("CONTEXT",)`

and the current GT12 wrapper still asserts that exact singleton.

This preserves the existing GT12 permission-translation semantics without converting them into a universal M4 law.

## Empirical M1 preserved

The already-existing empirical M1 contract remains on its prior path:

- it rejects a relation-use capability;
- it continues to require its existing explicit governed producer-use input;
- it delegates unchanged to the frozen empirical M4 adapter.

No GT2 CONTEXT ceiling was imposed on empirical M1.

---

# 4. Mandatory hostile controls

Test files:

- `rawlsing_next/tests/test_pre553_empirical_query.py`
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py`

I03 hostile controls prove:

1. ALLOW authority, exact ref/hash, wrong governed family -> nonpositive;
2. correct kind/operation, source universe excluded -> nonpositive;
3. correct-looking positive target-use authority for another target use -> nonpositive;
4. `DENY` authority -> nonpositive;
5. `OUT_OF_SCOPE` authority -> nonpositive;
6. `SUPERSEDED_NOT_REPLAYABLE` authority -> nonpositive;
7. exact lawful target-use authority -> positive behavior unchanged.

M1->M4 hostile controls prove:

1. raw caller REVIEW rejected;
2. raw caller ACTIVE_CAUSAL rejected;
3. mixed CONTEXT+REVIEW rejected;
4. raw CONTEXT rejected;
5. absent validated binding rejected;
6. raw authority-binding mapping rejected;
7. caller-forged/unsealed capability rejected;
8. issued capability is immutable;
9. wrong translation authority rejected;
10. wrong adoption receipt rejected;
11. lawful adopted GT12 CONTEXT path unchanged.

No shared relation path can produce a governed structural object from caller-selected use labels alone.

---

# 5. Focused hostile court

Final hostile execution commit:

`768d1ef58ad0786378593fae0fba1799dcced9c1`

Governed court run:

`34000813391`

Governed court job:

`101399229288`

Result:

`89 passed in 1.23s`

Suites:

- `test_pre553_empirical_query.py`
- `test_wave1_gt12_i03_positive_facts.py`
- `test_gt12_d_to_m4_typed_bridge.py`

This final matrix includes the stale/superseded authority control.

---

# 6. Inherited regression

Regression execution commit:

`f305efdf9a2c0fb0f5ef3ab886b0dbf7eec97f85`

Governed court run:

`34000718325`

Governed court job:

`101398972840`

Result:

`231 passed in 17.08s`

Executed suites:

- `test_pre553_empirical_query.py`
- `test_pre553_i03_scale_equivalence_repair.py`
- `test_wave1_gt12_i03_positive_facts.py`
- `test_wave1_gt12_a2_real_gt1.py`
- `test_pre553_empirical_objects_authority.py`
- `test_pre553_replay_audit.py`
- `test_pre553_repo_native_current_rehydration.py`
- `test_m4_v557_v558_publication_repository.py`
- `test_gt12_d_to_m4_typed_bridge.py`
- `test_gt12_e2b_publication_governance_binding.py`

The later hostile-only change adds test coverage for additional nonpositive authority states; production code is identical to the code exercised by this regression.

---

# 7. Identity ceiling proved unchanged

The regression includes the fixed repo-native current GT2 reconstruction court.

Exact current identities remain:

Predicate:

`bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`

Query:

`e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`

Fact:

`540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`

Replay:

`c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`

The current fact still reconstructs:
- raw denominator support `19,210`;
- exact risk-set member refs `19,210`;
- exact denominator refs `19,210`;
- source empirical provenance refs `76,843`;
- dependency refs `76,846`.

No current GT1/GT2 semantic identity changed.

---

# 8. Explicit non-widening statement

O2 changes enforcement only.

O2 does not change:

- GT1/GT2 current query;
- GT1/GT2 current fact;
- GT1/GT2 current replay;
- current predicate;
- FIELD FORGE relation semantics;
- PRE-V3 relation-admission semantics;
- adopted permission-translation mapping;
- adopted translation authority identity;
- adopted translation receipt identity;
- V557 decision semantics;
- V558 resolution semantics;
- empirical M1 permission semantics;
- V3 zero-positive law;
- actor state;
- PSEPF;
- comparator authority;
- metabolism authority;
- CAN-008 authority.

No authority was widened.
No new semantic permission model was created.

Therefore:

`NEEDS_HQ_DECISION__GT34_O2_ASTRA002_REPAIR_REQUIRES_AUTHORITY_MODEL_CHANGE`

does not apply.

---

# Terminal

`PASS__GT34_O2_ASTRA002_SHARED_AUTHORITY_BOUNDARIES_CLOSED__NO_AUTHORITY_WIDENING`

ASTRA-002 shared I03 boundary:

**closed**

ASTRA-002 shared M1->M4 relation-use boundary:

**closed**

Raw caller use treated as authority:

**no**

Generic ALLOW treated as sufficient authority:

**no**

GT12 adopted CONTEXT path preserved:

**yes**

GT2 CONTEXT imposed globally:

**no**

Current GT1/GT2 identities changed:

**no**

Authority widening:

**none**
