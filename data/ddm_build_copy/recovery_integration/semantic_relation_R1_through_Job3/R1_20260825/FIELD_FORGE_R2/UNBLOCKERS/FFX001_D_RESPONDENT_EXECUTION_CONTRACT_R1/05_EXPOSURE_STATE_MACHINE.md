# Respondent Exposure State Machine

Status: `CANDIDATE_EXECUTION_SEMANTICS__NOT_ADOPTED`

## 1. Four different propositions

The state machine preserves:

```text
SOURCE_PRESENCE != ELIGIBILITY != EXPOSURE != RESPONSE
```

These are separate proposition families and must remain separately queryable.

### Source presence

Question/measurement exists in a source/instrument/scope.

This says nothing by itself about a particular respondent.

### Eligibility

The exact routing predicate, executed on a governed respondent input vector, yields the predicate consequence defined by current routing authority.

Eligibility can be `TRUE`, `FALSE`, or `UNRESOLVED` at execution time.

### Exposure

A governed administration/exposure rule establishes whether the respondent had measurement opportunity/exposure.

Eligibility may be a prerequisite for exposure. It is not exposure unless current administration semantics explicitly make it sufficient for the exact instrument/scope.

### Response

A response state/value is independently recorded for respondent + measurement.

No response state rewrites the exposure state.

## 2. Pre-execution gates

Before any exposure state can be emitted, validate:

1. current respondent carrier admission;
2. current respondent entity key;
3. exact respondent source/scope binding;
4. current qimpl identity;
5. current qimpl->empirical measurement binding;
6. current predicate ID/specification where routing is conditional;
7. exact predicate input-symbol bindings;
8. exact exposure/administration semantics;
9. immutable execution dependency identities.

If the respondent is positively governed outside the operation's source/scope universe, emit typed stop:

`OUTSIDE_GOVERNED_OPERATION_SCOPE`

This is **not** `NONEXPOSURE__PROVED`.

## 3. Predicate execution states

For conditional routing:

- all required inputs resolved + predicate true -> `ELIGIBLE__PREDICATE_TRUE`;
- all required inputs resolved + predicate false -> `INELIGIBLE__PREDICATE_FALSE` only to the extent routing authority gives false that meaning;
- any required input or binding unresolved -> `ELIGIBILITY__UNRESOLVED`.

For an unconditional administration rule, the routing authority must identify that fact explicitly; code must not infer unconditionality from a missing predicate row.

## 4. Exposure states

The materializer may emit exactly three respondent-level exposure states:

### `EXPOSED__PROVED`

Emit only when an exact current administration/exposure rule says the resolved respondent scope + routing execution outcome proves measurement opportunity/exposure.

Required evidence is frozen into the receipt.

### `NONEXPOSURE__PROVED`

Emit only when an exact current administration/exposure rule positively proves nonadministration/nonopportunity for this respondent.

A predicate false result is insufficient unless the current routing/administration semantics explicitly state that false means the measurement was not administered.

### `EXPOSURE__UNRESOLVED`

Emit when the respondent/qimpl relation is within the candidate operation universe but evidence is insufficient to prove either exposure or nonexposure.

Mandatory triggers include:

- unresolved required predicate input;
- unresolved qimpl->measurement binding;
- ambiguous respondent scope;
- stale binding after qimpl/schema/carrier evolution;
- incompatible current-carrier claims;
- absence of an exact rule connecting routing result to administration opportunity.

`EXPOSURE__UNRESOLVED` may not be collapsed to false or filtered away as if it never existed.

## 5. Response overlay

After exposure is independently emitted, attach an optional response overlay:

- source-governed observed value/state;
- source-governed explicit missing/refusal/don't-know/not-recorded state where the carrier distinguishes it;
- no separately bound response fact.

The overlay does not change exposure.

Examples:

```text
EXPOSED__PROVED + no response fact
```

is lawful if exposure was proved independently.

```text
EXPOSURE__UNRESOLVED + observed response
```

must remain unresolved unless a separate current authority declares that this response representation itself is sufficient administration evidence for this source. The response may be corroborative evidence but is not automatically sole proof.

## 6. Forbidden transitions

Never permit:

```text
missing response -> NONEXPOSURE__PROVED
observed response -> EXPOSED__PROVED   [as sole rule]
source membership -> EXPOSED__PROVED
positive routing spec -> EXPOSED__PROVED without respondent execution
unresolved input -> predicate FALSE
historical row match -> current respondent identity
```

## 7. Replay receipt

Every exposure state records enough dependency identity to replay exactly:

- respondent carrier and entity key;
- source/scope binding;
- qimpl/current-selection ref;
- empirical measurement binding;
- predicate ID/spec hash;
- predicate input values/states + provenance;
- predicate result;
- exposure rule ID/ref;
- executor version/hash;
- emitted state;
- execution timestamp as provenance only, never currentness.

A dependency supersession invalidates the old receipt for CURRENT claims until replay/recertification occurs; the historical receipt remains immutable history.
