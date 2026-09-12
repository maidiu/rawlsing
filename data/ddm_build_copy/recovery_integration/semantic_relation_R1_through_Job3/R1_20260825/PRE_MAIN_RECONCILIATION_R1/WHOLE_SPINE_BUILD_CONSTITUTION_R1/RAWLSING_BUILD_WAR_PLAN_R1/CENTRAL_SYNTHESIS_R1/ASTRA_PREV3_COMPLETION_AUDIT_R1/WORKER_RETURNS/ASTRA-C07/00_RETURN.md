# ASTRA-C07 Rabochii Return — PRE-V3 producer-result firewall / contract-drift court R1

STATUS: `PASS__PREV3_PRODUCER_RESULT_FIREWALL_AND_CONTRACT_DRIFT_REPAIR_COURT_R1__GATE_FIREWALL_IMPLEMENTATION_BOUNDED`

Authorized grain:

`PREV3_PRODUCER_RESULT_FIREWALL_AND_CONTRACT_DRIFT_REPAIR_COURT_R1_ONLY`

Branch: `agent/rabochii-astra-c07-producer-firewall-contract-drift-r1`

Commission/start tip: `eafced006fbad2ddb92c83e27bd7713f9fbac028`

Frozen semantic floor examined: `3468673673db2f3de804d6e825585f86ff98e870`

This is a **court/specification PASS only**. It does not claim the production M3 firewall is repaired. No production code was changed under C07.

## 1. Court holdings

### H1 — the M3 alias leakage class is real and exact

At the frozen floor, `rawlsing_next/m3_v556_higher_order_structural.py` uses `_contains_forbidden_person_semantics(...)` as the positive-boundary guard. The guard recursively inspects mapping **keys** for a finite token list. It does not establish that a positive result conforms to a competent objective-world result schema.

The accepted hostile probe establishes the exact class:

| governed result | current M3 result | positive object |
|---|---|---|
| `{"actor_state":"x"}` | denied | no |
| `{"psychometric_type":4,"motivation":"approval"}` | supported | yes |
| `{"subject_ref":"urn:audit:subject:1","preference":"deference","psychological_trait":"submissive"}` | supported | yes |
| `{"relation_kind":"TEST_HIGHER_ORDER"}` | supported | yes |

The two alias-person-state positives are stamped `actor_independent=true`. Therefore the current generic M3 lexical guard cannot qualify as the PRE-V3 / V3 semantic firewall.

This is a **schema/authority-binding defect**, not merely an incomplete blacklist.

### H2 — a larger forbidden-word list is not an admissible repair

Adding more strings such as `psychometric`, `motivation`, `preference`, `trait`, `temperament`, or `drive` only moves the alias surface and risks false positives against lawful objective actor-indexed facts.

The constitutional distinction is semantic:

`OBJECTIVE_ACTOR_POSITION != PERSON_STATE`

PRE-V3 may resolve objective facts indexed to an actor while remaining forbidden from constructing that actor's belief, preference, motivation, affect, appraisal, psychometric type, uptake, interpretation, response, or durable person-state.

Therefore GATE-FIREWALL must bind positive M3 output to an **exact competent objective result contract**, not infer jurisdiction from field-name spelling.

### H3 — objective actor indexing is a required positive control

An exact, source/authority-backed statement that actor `A` occupies institutional position `P`, is subject to objective rule `R`, or has objective opportunity/constraint `O` is not person-state merely because it contains an actor identifier.

The successor firewall must distinguish at least:

- `NO_ACTOR_INDEX`;
- `OBJECTIVE_ACTOR_INDEXED`;

while maintaining an independent hard exclusion of subjective/person-state semantics.

The present unconditional `actor_independent=true` representation is too coarse to carry that distinction honestly. GATE-FIREWALL must version the affected contract/schema rather than silently reinterpret the existing flag.

### H4 — the two PRE553 source-relation failures are stale test expectations

`SourceRelationResolver.resolve_exact(...)` deliberately raises `SourceRelationIntegrityError` when a supplied exact relation ref is unavailable. That preserves exact-ref integrity and the explicit rule `no label/ID/latest/default inference`.

The two failing regression tests instead expect `SourceRelationAuthorizationError` while passing dangling exact refs into exact-ref-required guards.

Court disposition:

- keep production behavior;
- update those two tests to expect exact-reference integrity failure at this invocation grain;
- do **not** catch/downgrade the integrity error into authorization merely to make the tests green.

Authorization-state behavior remains appropriate on decision surfaces where the exact object exists but is nonpositive, or where an API intentionally asks whether positive authority exists without pretending an unavailable exact ref exists.

### H5 — the relation-M1 caller-use failure is stale caller/test behavior

`rawlsing_next/m4_m1_evaluation_binding.py` correctly rejects caller-selected `producer_allowed_uses` for the relation-M1 contract and requires an opaque, evaluation-bound `ValidatedM1ProducerUseBinding`.

The existing GT12 governed wrapper already supplies the lawful positive path:

`rawlsing_next/gt12_d_to_m4_typed_bridge.py::publish_and_resolve_relation_v554_at_current_m4(...)`

It derives the adopted permission binding, verifies exact downstream use shape and relation-M1 lineage, internally issues the sealed producer-use binding, then calls `structural_objects_from_accepted_m1(...)` with that binding.

Court disposition:

- preserve the M4 shared-boundary rejection of raw relation-M1 uses;
- convert the stale raw-use positive unit test into a negative boundary test;
- test the positive relation-M1 path through the governed GT12 wrapper, or another owner-approved wrapper with equivalent authority proof;
- do not call the private issuer directly from an ordinary test merely to restore positivity;
- do not alter the empirical-M1 branch, whose explicit caller-use contract is a distinct inherited behavior.

## 2. Exact GATE-FIREWALL implementation handoff

The implementation successor is bounded by `01_M3_FIREWALL_REPAIR_SPEC.md`.

Minimum authorized implementation surfaces are:

- `rawlsing_next/m3_v556_higher_order_structural.py`;
- `rawlsing_next/tests/test_m3_v556_higher_order_structural.py`;
- the smallest owner-approved schema/authority-binding support needed to make M3 positive results prove exact objective-world conformance;
- `rawlsing_next/tests/test_pre553_source_relations.py` **only** for the two stale exception expectations in `02_ERROR_AND_CALLER_CONTRACT_DISPOSITION.tsv`;
- `rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py` **only** for the stale relation-M1 caller-use expectation and an owner-governed positive-path assertion if that remains the correct test home.

Not authorized merely to obtain green tests:

- weakening `rawlsing_next/pre553_source_relations.py` exact-ref integrity semantics;
- weakening `rawlsing_next/m4_m1_evaluation_binding.py` relation-M1 sealed-use boundary;
- inventing caller-mintable semantic/use labels;
- reinstating a blanket ban on actor identifiers;
- adding PRE-V3 person-state, psychological transmission, driver/type terminals, or V3 realization behavior.

## 3. Required successor qualification

GATE-FIREWALL is not complete until an independent court proves all of the following:

1. every hostile alias case in `03_HOSTILE_CASES.json` fails closed unless it conforms to an exact adopted objective result contract;
2. objective actor-indexed positive controls succeed under exact objective authority;
3. missing, stale, mismatched, or unresolvable result-contract bindings cannot emit a positive M3 object;
4. lexical filtering, if retained, is defense-in-depth only and never positive authority;
5. existing exact source-relation integrity behavior remains unchanged;
6. relation-M1 raw caller-selected uses remain rejected;
7. the governed relation-M1 positive path remains positive;
8. targeted regression and full relevant PRE-V3 regression are green without guard weakening;
9. replay/object identity commits to the result-contract binding so a payload cannot be rebound under a different semantic jurisdiction without identity change.

## 4. Stop line after C07

The audit STOP remains in force on **broad M3 firewall qualification / new untyped positive M3 promotion** until GATE-FIREWALL implementation and hostile qualification pass.

C07 does not block independent C02–C08 work that does not rely on broad M3 firewall qualification.

## 5. Governed return artifacts

- `00_RETURN.md` — this disposition and handoff.
- `01_M3_FIREWALL_REPAIR_SPEC.md` — exact semantic repair contract for GATE-FIREWALL.
- `02_ERROR_AND_CALLER_CONTRACT_DISPOSITION.tsv` — three regression/contract-drift dispositions.
- `03_HOSTILE_CASES.json` — required hostile and positive-control qualification vectors.

No production files were mutated by this commission.
