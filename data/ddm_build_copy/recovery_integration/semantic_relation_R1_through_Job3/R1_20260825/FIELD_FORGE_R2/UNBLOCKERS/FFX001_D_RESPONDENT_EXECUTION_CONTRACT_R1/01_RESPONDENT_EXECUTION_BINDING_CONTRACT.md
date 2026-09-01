# Candidate `CURRENT_RESPONDENT_EXECUTION_BINDING_CONTRACT@1`

Status: `DESIGN_CANDIDATE__NOT_ADOPTED_CURRENT_AUTHORITY`

This document specifies the minimum interface that a competent project-level authority would have to instantiate and admit before FIELD FORGE may execute respondent-level routing/exposure logic.

The candidate name is neutral and may be replaced by competent authority.

## 1. Contract purpose

The contract must support exactly the following lawful operation:

```text
CURRENT question implementation
+ CURRENT routing/predicate authority
+ CURRENT respondent empirical state
-> respondent-level predicate execution
-> governed respondent measurement exposure/opportunity
-> response fact if independently present
```

It must not turn physical data availability into semantic currentness.

## 2. Non-negotiable distinctions

```text
CURRENT_AUTHORITY != HISTORICAL_CAPABILITY
CURRENT_AUTHORITY != PHYSICAL_EXISTENCE
CURRENT_AUTHORITY != GIT_RECENCY
CURRENT_AUTHORITY != WORKER_PASS

SOURCE_PRESENCE != ELIGIBILITY
ELIGIBILITY != EXPOSURE
EXPOSURE != RESPONSE

MISSING_RESPONSE != NONEXPOSURE
PRESENT_RESPONSE != SOLE_PROOF_OF_EXPOSURE

RESPONDENT_LINKAGE != MEASUREMENT_PORTABILITY
ROUTING_SPECIFICATION != RESPONDENT_PREDICATE_EXECUTION
```

Any implementation that collapses one of these inequalities fails the contract.

## 3. Required logical interfaces

### 3.1 `RESPONDENT_ENTITY_CARRIER`

**Object:** a current-admitted carrier or relation exposing a stable respondent entity at the grain required by the source.

**Proposition proved:** this empirical row/entity is a governed respondent in exact carrier version `C`.

**Minimum key:** `(respondent_carrier_identity, respondent_local_id)` unless a separately governed canonical respondent entity ID already exists.

**Authority:** project current-selection/admission authority plus the admitted empirical/source owner. Code owns no respondent sameness semantics.

**Deterministic code may:** parse, validate uniqueness under the governed composite key, hash, index, and replay exact identity derivations specified by authority.

**Code may not:** infer identity from row order, matching demographics, same local ID across carriers, or historical database row alignment.

### 3.2 `RESPONDENT_SOURCE_SCOPE_BINDING`

**Object:** a lossless binding from respondent entity to every source-scope coordinate needed for the operation.

**Proposition proved:** respondent `R` belongs to the exact governed administration universe described by source family/release/wave/context/form/module/split coordinates that are relevant to this operation.

Coordinates are required only where they prevent ambiguity or encode routing/administration differences. They must not be added as decorative pseudo-precision.

**Authority:** empirical/source scope authority; project authority selects which carrier/scope is current.

**Code may:** project already-governed source metadata to respondent rows and validate it against carrier invariants.

**Code may not:** infer country/form/split from neighboring rows or from the question's expected scope.

### 3.3 `QIMPL_TO_EMPIRICAL_MEASUREMENT_BINDING`

**Object:** an exact, versioned binding between a current `question_implementation_id` and an exact empirical measurement identity inside the admitted respondent carrier.

**Proposition proved:** measurement `M` is the empirical representation of qimpl `Q` for exact scope `S` under current authority.

**Preferred grain:** schema/column/instrument-measurement grain, not respondent row grain, when one measurement column is shared by respondent rows. Row grain is required only if the source itself genuinely stores respondent-specific measurement identity.

**Minimum identity:** `binding_id`, current qimpl ID, empirical measurement ID, exact scope, source-variable identity, carrier/schema version, authority ref, validity/supersession state.

**Authority:** existing current qimpl/source-variable authority where an exact one-to-one identity already exists; otherwise a finite source-semantic/project adjudication. Runtime code may not create this semantics.

**Staleness law:** a qimpl lifecycle/current-selection change invalidates or requires recertification of every dependent measurement binding unless exact same-ID survival is explicitly governed.

### 3.4 `RESPONDENT_PREDICATE_INPUT_BINDING`

**Object:** exact respondent-level values for every input symbol named by the executable current predicate, each bound to a governed measurement/source-scope identity.

**Proposition proved:** predicate input symbol `X` for respondent `R` resolves to value/state `V` from exact governed empirical fact `F`.

**Key:** respondent entity + predicate ID + predicate input symbol + input measurement identity + carrier version.

**Authority:** the predicate specification owns which symbols are required; the respondent carrier/input measurement authority owns the values; a finite mapping authority is required if symbol-to-measurement identity is not already exact.

**Code may:** fetch values and execute typed conversions explicitly authorized by the predicate contract.

**Code may not:** convert unresolved/null/not-collected into `FALSE`, substitute a neighboring variable, or infer an input from response missingness.

### 3.5 `RESPONDENT_EXPOSURE_MATERIALIZER`

**Object:** a deterministic derived execution surface/receipt, not an independent semantic authority.

**Proposition proved:** for exact respondent/qimpl/scope/predicate/binding versions, all prerequisites were evaluated and a lawful exposure state was emitted under an exact governed administration/exposure rule.

**Required execution identity:** respondent entity key; qimpl; empirical measurement; routing/predicate authority ref; predicate ID; predicate input facts; source-scope binding; exposure-rule/administration-semantics ref; executor version/hash; carrier version; execution receipt ID.

**Code may:** execute the exact predicate and exact current exposure rule, then emit one of the contract exposure states.

**Code may not:** decide which carrier is current, invent qimpl->measurement meaning, define administration semantics, or use response presence/absence to repair an unresolved predicate.

### 3.6 `RESPONDENT_RESPONSE_BINDING`

**Object:** a response fact/state independently joined to respondent + empirical measurement.

**Proposition proved:** exact response state/value `Y` is recorded for respondent `R` and measurement `M` in carrier version `C`.

**Key:** respondent entity + empirical measurement ID + response-state identity/version.

**Authority:** admitted empirical carrier/source semantics.

**Code may:** join response facts after exposure state is independently determined.

**Code may not:** use response existence as the sole exposure proof or missingness as nonexposure.

### 3.7 `MEASUREMENT_ANCESTRY_BINDING`

**Object:** immutable provenance graph tying respondent carrier, schema/measurement identity, qimpl binding, source variable, predicate inputs, and response representation to exact source/ref/hash and supersession events.

**Proposition proved:** the current operation is replayable and its identities can be distinguished from predecessors/successors.

**Authority:** each semantic owner contributes its own authoritative edge; project lifecycle/current-selection authority governs currentness/supersession.

**Code may:** hash, traverse, validate, and compare exact refs.

**Code may not:** infer semantic equivalence because two versions have the same raw variable code or similar labels.

### 3.8 `WEIGHT_AND_DESIGN_BINDING` — conditional

**Object:** respondent + exact sample/design/weight identity needed by a stated estimand.

**Proposition proved:** this design/weight fact belongs to the respondent universe and purpose required by the estimand.

This interface is mandatory only when the downstream estimand requires it. Unweighted respondent-level routing/exposure proof must not be blocked merely because no weight is needed for that exact canary.

Weight/design authority does not grant measurement portability or respondent identity authority.

## 4. Minimum identity law

### 4.1 Respondent identity

A source-local respondent identifier is lawful if and only if its namespace is explicit and collision-safe.

Preferred minimum:

```text
respondent_entity_key := (respondent_carrier_identity, respondent_local_id)
```

A global respondent ID is not required.

If different source files use different IDs for the same respondent, they are different entities for joining purposes until a governed finite identity crosswalk proves sameness. Matching row number, demographics, or apparent one-to-one ordering is forbidden.

### 4.2 Carrier identity

`respondent_carrier_identity` must identify an exact immutable logical carrier version or an exact immutable snapshot/manifest of a mutable physical system. It must include or resolve to checksums/provenance sufficient for replay.

A rematerialized carrier receives a new carrier identity unless competent authority proves an exact identity-preserving succession relation. The old and new rows must be bijectively or otherwise explicitly mapped under the source's real identity semantics; row-order equality is insufficient.

### 4.3 Measurement identity

A raw variable code alone is not a durable measurement identity when meaning or administration can change across wave, release, country, form, module, split, or schema version.

`empirical_measurement_id` must therefore be governed at the smallest grain that prevents a false join. It may be a pre-existing stable ID or a current-authorized composite identity. The contract does not require all potential coordinates when they are semantically redundant.

### 4.4 Qimpl binding grain

The qimpl->measurement relation normally belongs at schema/measurement grain. It must not be duplicated per respondent merely to make a row table look complete. A row joins through respondent scope + empirical measurement identity.

## 5. Currentness and authority law

No artifact satisfies this contract merely by existing.

An admitted package must identify:

- authority level and owner;
- exact current-selection/admission act;
- exact proposition/grain governed;
- immutable artifact identity/hash;
- predecessor/supersession relationship where any;
- negative ceiling: what the admission does **not** authorize.

A delegated-current carrier may be sufficient inside its delegated scope if the target FIELD FORGE operation lies inside that scope. Project-wide/global use requires the authority level demanded by PRE-MAIN governance. Delegated authority cannot silently escape its charter.

## 6. Exposure law

The materializer may emit only:

- `EXPOSED__PROVED`
- `NONEXPOSURE__PROVED`
- `EXPOSURE__UNRESOLVED`

`OUTSIDE_GOVERNED_OPERATION_SCOPE` is a typed pre-execution stop, not an exposure state.

`EXPOSED__PROVED` requires all of:

1. current respondent identity;
2. current qimpl->measurement binding;
3. exact governed respondent administration scope;
4. all required predicate inputs resolved;
5. exact predicate execution result;
6. exact current administration/exposure semantics proving that this result and scope establish opportunity/exposure.

`NONEXPOSURE__PROVED` requires the same chain plus an exact current rule proving that the executed result entails nonadministration/nonopportunity. Predicate `FALSE` cannot be called nonexposure unless the predicate's governed semantics actually carry that consequence.

`EXPOSURE__UNRESOLVED` is mandatory when respondent and qimpl are in the candidate operation scope but any required input/binding/exposure rule remains unresolved. It cannot be coerced to false.

Response state is orthogonal and joined afterward.

## 7. Absence versus unresolved

The contract must distinguish:

- `GOVERNED_EXCLUSION`: authority proves the entity/measurement is outside the relevant universe;
- `PROVED_ABSENCE_IN_COMPLETE_CARRIER`: completeness authority proves the expected object is absent;
- `UNRESOLVED_BINDING`: required mapping exists neither positively nor as a governed exclusion;
- `VALUE_MISSING_OR_UNRECORDED`: respondent input/response fact carries a missing/unknown source state;
- `UNAVAILABLE`: source artifact/value is not available under current evidence;
- `BLOCKED_OR_UNRESOLVED`: exact dependency prevents adjudication.

Only the first two are absence propositions. None means predicate false unless the predicate explicitly defines that typed state as a value.

## 8. Provenance, replay, and supersession

A passing package must support exact replay from immutable inputs or immutable manifests.

Replay receipt must freeze at least:

- carrier identity/hash;
- scope binding version;
- qimpl current identity/ref;
- qimpl->measurement binding version;
- predicate ID/spec hash;
- input binding identities;
- exposure-rule identity;
- executor code/version/hash;
- emitted exposure state;
- response binding identity if consumed;
- weight/design identity if consumed.

Supersession is typed. Newer carrier/qimpl/schema versions do not silently overwrite earlier identities. A successor must either preserve exact identity under governed same-ID survival or supply an explicit supersession/crosswalk relation and trigger dependent recertification.

## 9. Backend neutrality

The contract defines information and function, not storage architecture.

It may be implemented in repository-native files, relational tables, DuckDB, PostgreSQL, Arrow/Parquet, or another lawful carrier. No backend wins merely because historical Rawlsing used it.

Historical PostgreSQL/DuckDB behavior may reveal required functions and joins; it cannot own current empirical truth without a current admission act.

## 10. Acceptance

A project-level restoration passes this contract only if:

1. competent authority explicitly admits the respondent carrier/current scope;
2. every mandatory logical interface is materialized or provably supplied by an existing current authority;
3. every semantic mapping is precomputed/adjudicated rather than silently invented at runtime;
4. all runtime work is deterministic from frozen inputs;
5. the exposure state machine is honored;
6. all hostile tests in `08_HOSTILE_ACCEPTANCE_TESTS.tsv` pass;
7. the bounded canary in `11_BOUNDED_ACCEPTANCE_CANARY.md` proves the full qimpl->measurement->respondent->predicate-input->predicate-result->exposure chain;
8. no claim of global FIELD FORGE, P3, OBL040, or Position Role Authority closure is made.
