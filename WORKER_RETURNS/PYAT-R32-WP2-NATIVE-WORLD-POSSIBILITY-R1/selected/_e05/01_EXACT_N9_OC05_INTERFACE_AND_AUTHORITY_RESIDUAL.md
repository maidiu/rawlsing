# R11 E05 — exact N9/OC05 interface and authority residual

## 1. Narrowest versioned interface identified

The narrowest interface that would let an actual lawful N9 owner consume a
coherent multi-field empirical + structural snapshot, without reinventing
N10E/C1, Field Forge, N5/N6 or publishing a parallel estimator, is a
three-part versioned request / acceptance / receipt contract:

```
R11_E05_N9_SELECTED_WORLD_INTERFACE@1
  N9_SELECTED_WORLD_REQUEST@1    (caller -> adapter)
  N9_SELECTED_WORLD_ACCEPTANCE@1 (adapter -> caller; binds one atomic snapshot)
  N9_SELECTED_WORLD_RECEIPT@1    (adapter -> caller; the result-bearing object)
```

It is deliberately minimal: the caller names **which** structural fields, which
empirical target with which ordered conditioner/value bindings, which
separately-native field roles, which explicit synthetic clock pair, and which
purpose; it cannot supply any value.  The adapter refuses pooling, person
exposure and model promotion outright.

## 2. What the real installed OC05 manifest says (read, never edited)

`rawlsing_next/objective_consumer_bounded_evidence.installation_manifest()`
(blob `f30fca20e7b56e00348e82765d95f974b4b6a195`, byte-identical startup vs
staged):

| policy | state | seam |
|---|---|---|
| `OC01_PRE553_SOURCE_LOCAL_EMPIRICAL_QUERY_R1` | `APPLICABLE_CURRENT` | `rawlsing_next.pre553_empirical_query.execute_empirical_query` |
| `OC02_LEARNED_STRUCTURAL_ADMISSION_R1` | `APPLICABLE_CURRENT` | `rawlsing_next.pre553_structural_admission` |
| `OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1` | `NOT_YET_APPLICABLE` | `None` |
| `OC04_OCCURRENCE_NONEVENT_WORLD_FACT_R1` | `NOT_YET_APPLICABLE` | `None` |
| `OC05_TERMINAL_OBJECTIVE_WORLD_RESOLUTION_R1` | **`NOT_YET_APPLICABLE`** | **`None`** |

`evaluate_current_consumer(policy_id=OC05, …)` raises
`NotYetApplicableConsumer` before any values-read, because the seam is `None`.
This E05 adapter therefore does **not** route through OC05 and does not install
anything; it routes through M4/M5 + N9C + E04 as a noninstalling candidate.

## 3. Request schema (exact)

```
contract, purpose, structural_keys, empirical_target, empirical_conditions,
native_field_roles, clock{mode, valid_at, published_asof, test_now},
requested_pooling, requested_person_exposure, requested_model_use
```

Refusals: `UNKNOWN_N9_INTERFACE_CONTRACT`, `SOURCEFREE_ONLY_PURPOSE_REQUIRED`,
`PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN`,
`NONEMPTY_EXACT_STRUCTURAL_READSET_REQUIRED`, `DUPLICATE_STRUCTURAL_KEY_REQUIRED`,
`UNKNOWN_STRUCTURAL_FIELD_KEY`, `EXACT_NATIVE_TARGET_REQUIRED`,
`EXACT_NONEMPTY_UNIQUE_ORDERED_CONDITIONERS_REQUIRED`,
`ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED`,
`NONEMPTY_EXACT_NATIVE_FIELD_READSET_REQUIRED`,
`DUPLICATE_NATIVE_FIELD_ROLE_REQUIRED`, `UNKNOWN_NATIVE_FIELD_ROLE`,
`TWO_SEPARATELY_NATIVE_UNITS_REQUIRED`, `TYPED_SELECTION_CLOCK_REQUIRED`,
`UNKNOWN_SELECTION_MODE`, `EXACT_ISO_DATE_REQUIRED`,
`EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED`,
`REQUEST_RECORD_FIELDS_MISSING_OR_UNKNOWN`, `REQUEST_SCHEMA_VERSION_MISMATCH`.

Selection clocks are explicit synthetic inputs; the wall clock is never read.
`mode='TEST_CURRENT'` is accepted only when `valid_at == published_asof == test_now`.

## 4. Acceptance schema (exact)

```
request_hash, snapshot_hash, catalog_hash, structural_keys, native_field_roles,
native_field_refs, empirical_source_identity{source_universe_ref, release_ref,
risk_set_ref, rows_hash, permission_root, publication, field_time,
native_geography, native_unit, grade, state}, permission_roots,
publication_clocks, effective_clocks, field_clock_bindings, acceptance_state,
inconsistencies
```

Atomicity refusals: `NATIVE_FIELD_REFUSAL:<code>`, `FRAGMENTED_PERMISSION_ROOT`,
`MISSING:<field>`, `UNREGISTERED:<role>`,
`FIELD_EFFECTIVE_CLOCK_OUTSIDE_SELECTION:<field>`,
`FIELD_PUBLICATION_CLOCK_OUTSIDE_SELECTION:<field>`,
`EMPIRICAL_PUBLICATION_CLOCK_OUTSIDE_SELECTION`,
`NATIVE_FIELDSET_OUTSIDE_REQUEST`, `NATIVE_DEPENDENCY_READSET_ARM_NOT_EXACT`,
`ORIGINAL_SOURCE_CLASS_COLLISION`, `NATIVE_UNIT_COLLISION`,
`ACCEPTED_SNAPSHOT_SUBSTITUTION`, `ACCEPTANCE_BINDING_MISMATCH`,
`SELECTED_SNAPSHOT_CONSTRUCTION_REFUSED:<owner code>`,
`NATIVE_FIELD_READSET_REFUSED:<N9C code>`.

Distinct `effective_from` values across fields are reported, never refused: a
legitimate structural revision has an effective date; the invariant is that each
field's clock pair sits **inside the one selection clock pair**.

## 5. Receipt schema (exact)

Two explicit identities are emitted for every receipt:

* `receipt_hash` — a total float-free semantic identity (published decimals are
  carried as exact decimal literals inside the projection);
* `receipt_payload_sha256` — a byte digest over the verbatim receipt, which
  preserves every published decimal exactly.

Result-bearing content: `structural_readset`, `structural_values`
(value, unit, revision, publication, effective_from, epistemic_class,
currentness_grade, rsc_ref, validation_ref), `structural_value_refs`,
`empirical_target`, `empirical_condition_order`, `empirical_state`,
`empirical_steps` (target, conditioners, binding_order, route, denominator,
cells with exact fractions, release/risk/source refs, evidence ref, uncertainty,
measure), `empirical_native_time`, `native_field_readset` (roles, refs,
dependency_readset, successful_value_refset, values_read, refusals, as_of,
state), `claim_ceiling`, `permission_roots`, `publication_clocks`,
`effective_clocks`, `native_units`, `source_families`, `consumers`
(the two real E04 consumer materials), `selection`, `inconsistencies`, `state`.

## 6. Existing owner modules this interface routes through

| Module | Symbols used | Git blob |
|---|---|---|
| `rawlsing_next/objective_consumer_bounded_evidence.py` | `installation_manifest`, `POLICY_BINDINGS`, `evaluate_current_consumer`, `NotYetApplicableConsumer` | `f30fca20e7b56e00348e82765d95f974b4b6a195` |
| `rawlsing_next/m4_v557_v558_publication_repository.py` | `make_structural_object`, `govern_v557`, `make_producer_locator`, `build_v557_publication_bundle`, `build_v558_repository_bundle`, `make_context_query`, `exact_resolution_key`, `resolve_v558`, `V557DecisionState`, `V557PublicationEntry`, `RepositoryEntry`, `AuthorityRef`, `ExactRef` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` |
| `rawlsing_next/m5_runtime_rsc_peer_prior.py` | `make_structural_currentness_receipt`, `StructuralCurrentnessState`, `materialize_resolved_structural_context`, `validate_resolved_structural_context` | `18735bdb31a220aed032aa722574d685e2bdddf5` |
| `rawlsing_next/pre553_hq297_n9c_two_field_reader.py` | `TestOnlyRegistry`, `read_historical_test_only`, `fixture_invalidation`, `GSS`, `NCA` | `03eb46efccadd6880cb34b2e2ac609ffc9b16c59` |
| `rawlsing_next/pre553_empirical_objects.py` | `semantic_hash` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| E04 sealed `product.service` / `product.world` / `product.empirical` | `GenericSelectedWorldService`, `SelectedWorldCatalog`, `GenericProgressiveProvider` | E04 commit `9c96f201f…` |
| `rawlsing_next/pre553_empirical_possibility_provider.py` | `provide_empirical_possibility_slice` | `23167aa25291fb148b1e3cf210ac33fe7769b783` |
| `rawlsing_next/pre553_analytical_composition.py` | `compose_positioned_subject_possibility` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` | `evaluate_positioned_subject_possibility` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` |
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | `synthetic_world_rows` | E03 commit `0e0ed50db…` |

## 7. Smallest competent adoption decision

The smallest decision that would make a real N9-shaped consumer operative is a
competent N9/OC05 owner granting **actual adoption of the OC05 seam**: flipping
`OC05_TERMINAL_OBJECTIVE_WORLD_RESOLUTION_R1` from `NOT_YET_APPLICABLE` with
`seam=None` to `APPLICABLE_CURRENT` with a named seam.  That single decision
requires, and does not replace:

1. a competent prospective original **U** (real respondent/universe principal,
   signed, with a real namespace);
2. a signed real **source / operation** with source licence and a real
   `raw_wave`;
3. two independently produced immutable N5/N6 `ExternalPublishedAggregateField`
   products with source roots, numeric values and exact refs;
4. an independent **EE13/N7** decision authorising this exact nonpooled
   co-presence pair.

This E05 return performs none of those and claims none of them.

## 8. Residual issuer authority

`operative_N9`, `operative_OC05`, `issued_N5N6`, `issued_EE13`, `new_issuer` are
all hard `False` in every receipt, and the live manifest is embedded so a later
reader cannot claim a state this return never observed.  Source/actor
permissions are kept separate throughout; no actor permission is exercised.
