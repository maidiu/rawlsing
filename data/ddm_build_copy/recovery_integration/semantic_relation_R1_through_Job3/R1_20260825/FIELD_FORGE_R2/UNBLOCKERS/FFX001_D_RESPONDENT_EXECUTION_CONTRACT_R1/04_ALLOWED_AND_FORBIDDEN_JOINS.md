# Allowed and Forbidden Joins

Status: `DESIGN_CONSTRAINT__NO_RUNTIME_CHANGE`

## 1. Join principle

A join is lawful only when every semantic equality used by the join is already governed. Deterministic code may execute equality; it may not decide what equality means.

A physical shared column name is not authority.

## 2. Allowed joins

### A. Respondent entity -> respondent scope

Allowed on exact `respondent_entity_key` from the same current-admitted carrier identity, or through an explicit current identity crosswalk.

Required cardinality/invariant must be declared. If a respondent may have multiple form/module memberships, one-to-many is lawful only when that multiplicity is source-governed and retained.

### B. Qimpl -> empirical measurement

Allowed only through a current `QIMPL_TO_EMPIRICAL_MEASUREMENT_BINDING` or an already-governed exact identity relation that deterministically yields the same mapping.

Raw variable code may participate as evidence/key material only with every disambiguating scope/schema coordinate required by the source semantics.

### C. Respondent -> predicate input

Allowed through respondent entity + governed input measurement identity + exact scope.

Every predicate symbol must resolve exactly once to either:

- a governed value/state;
- a governed not-applicable/exclusion state; or
- a typed unresolved/unavailable state.

A many-match or zero-match without governed exclusion fails closed.

### D. Respondent/qimpl -> exposure materialization

Allowed only after current respondent identity, source scope, qimpl->measurement binding, predicate spec, all required predicate inputs, and an exact exposure/administration rule are frozen.

### E. Respondent/measurement -> response

Allowed independently of exposure using the same respondent entity and empirical measurement identity. The result is a response fact, not exposure evidence by itself.

### F. Respondent -> weight/design

Allowed only when the estimand declares the channel required and the weight/design artifact proves the same respondent universe/purpose.

## 3. Forbidden joins

The following are categorically forbidden absent a separately governed crosswalk/authority:

1. same source-local `respondent_id` across different carrier identities -> same person;
2. row N in historical carrier -> row N in rematerialized/current carrier;
3. source family + wave + raw variable code -> qimpl when country/form/module/split/schema meaning can differ and those coordinates are dropped;
4. same raw variable code in neighboring waves -> same empirical measurement;
5. same human-readable question text -> same qimpl/measurement;
6. positive routing disposition -> respondent exposure without respondent predicate execution and governed exposure semantics;
7. source membership -> exposure;
8. response nonmissing -> exposure as sole proof;
9. response missing -> nonexposure;
10. predicate input null/unresolved -> predicate false;
11. current qimpl -> historical V542/Postgres column merely because historical code used that variable;
12. weight/design row -> respondent using an ID namespace not proven identical;
13. two current-claiming respondent carriers -> union/coalesce without explicit project current-selection/succession;
14. measurement portability from respondent linkage, pooling, common scale labels, or semantic similarity.

## 4. Scope-coordinate law

Coordinates such as country, form, split, module, release, and instrument are neither universally mandatory nor optional decoration.

For every join, the authority artifact must answer:

> Which coordinate set is the smallest set that makes this identity relation unambiguous and lossless for this source/operation?

Dropping a required coordinate is a hostile failure. Requiring an irrelevant coordinate is unnecessary but not a substitute for the real discriminators.

## 5. Cardinality law

Every binding declares expected cardinality:

- respondent entity -> primary source scope: source-governed one-to-one or explicit one-to-many;
- qimpl -> empirical measurement: normally one-to-one per exact scope, with explicit one-to-many only if the source genuinely represents one qimpl through multiple measurements;
- respondent + measurement -> response fact: source-governed cardinality, never deduplicated by arbitrary `first`/`latest`;
- predicate symbol -> input measurement: exactly one current binding per predicate/scope unless the predicate itself declares a structured multivalue input.

Unexpected cardinality is a hard stop, not an invitation to deduplicate.

## 6. Historical carriers

Historical V542/DuckDB/Postgres rows may be joined internally for historical replay/functional archaeology under their historical identities. They may not be joined into a CURRENT FIELD FORGE respondent operation until competent authority returns a current admission/succession relation satisfying this contract.
