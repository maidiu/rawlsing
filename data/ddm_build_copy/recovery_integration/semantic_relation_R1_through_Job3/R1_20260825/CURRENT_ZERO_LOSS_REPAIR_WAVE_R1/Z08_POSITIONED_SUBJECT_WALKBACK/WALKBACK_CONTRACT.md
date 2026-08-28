# Z08 POSITIONED-SUBJECT POSSIBILITY / SPECIFICITY WALKBACK CONTRACT R1

Status: `CLOSED__BOUNDED_V1_SOURCE_BACKED_MODEL_AND_VISIBLE_WALKBACK`

## Governing distinction

`PROXY != EXACT FACT != ACTOR BELIEF`

Also binding:

`EMPIRICAL_POSSIBILITY != INDIVIDUAL_PREDICTION`

`EMPIRICAL_POSSIBILITY != NORMATIVE_RECOMMENDATION`

`GENERATED_SUBJECT_FACT = QUERY_CRITERION_ONLY`

This contract implements the Authority-40 Z08 closure only. It does not modify PRE553 I03 exact query semantics, QuerySpace, V3, actor state, structural meaning, or architecture selection.

## Two-lane law

The learned-world service has two logically separate lanes.

### Lane E — exact requested grain

The exact positioned-subject request is defined by:

- exact subject/generation correlation ref;
- exact target ref;
- exact empirical source-universe ref;
- exact release ref;
- every exact downstream-owned subject fact ref used as a criterion;
- an exact empirical coordinate ref for each criterion;
- an exact positive comparability-authority ref for each binding;
- exact effective-time material;
- exact requested empirical projection.

Lane E never broadens. Its state remains exact even when a proxy exists.

Possible V1 exact dispositions are:

- `SUPPORTED` — exact source-backed slice exists in upstream `SUPPORTED` state;
- `UNRESOLVED` — exact slice is absent, underpowered, unresolved or unavailable;
- `VALID_EMPTY` — exact slice was lawfully evaluated and is empty;
- `NONCOMPARABLE` — exact grain cannot lawfully be compared.

`UNDERPOWERED -> UNRESOLVED` for the exact requested grain. A later broader proxy does not rewrite that disposition.

`VALID_EMPTY` and `NONCOMPARABLE` are terminal exact states in V1 and are not rescued through proxy walkback.

### Lane P — explicit lower-specificity proxy

Lane P may run only when Lane E is unresolved and the invocation carries a positive, versioned walkback authority.

A proxy step must contain:

- a stable step id;
- the exact retained conditioner-id set;
- an exact positive proxy-authority ref;
- exact source-universe ref;
- exact release ref;
- a nonempty rationale.

Every step authority ref must also appear in the model rule's `positive_proxy_authority_refs`. An arbitrary `AuthorityRef` attached to a result is not enough.

The ladder must be strictly monotone toward lower specificity:

`REQUESTED_CONDITIONERS > STEP_1 > STEP_2 > ...`

Each retained set must be a strict subset of both the original requested set and the immediately preceding set. No step may widen back upward, reorder into a sibling surrogate, or silently replace the requested grain.

## Model rule closed by Z08

V1 model rule:

`POSITIONED_SUBJECT_EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK@1.0.0`

V1 algorithm:

`EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`

The model does not infer a new probability law from sparse observations. It resolves an exact source-backed conditional empirical slice already owned by upstream evidence. When that exact slice cannot support the requested positioned grain, it may inspect only the finite walkback ladder positively supplied by authority.

V1 therefore authorizes none of:

- nearest-neighbor substitution;
- statistical smoothing;
- interpolation;
- extrapolation;
- embedding similarity;
- LLM-selected surrogate choice;
- automatic demographic regrouping;
- hidden threshold invention;
- top-k or relevance-selected fallback;
- cross-source borrowing.

Upstream evidence states decide whether a slice is `SUPPORTED`, `UNDERPOWERED`, `VALID_EMPTY`, `UNRESOLVED`, `NONCOMPARABLE`, or `UNAVAILABLE`. Z08 does not invent a new raw-n adequacy threshold.

## Same-source / same-release V1 boundary

A V1 proxy must stay inside the exact query's source universe and release.

If a walkback step changes either source universe or release, evaluation returns:

`FAIL_CLOSED_UNAUTHORIZED_PROXY_SOURCE`

and no proxy is emitted.

Multi-universe disagreement and noncomparability therefore remain visible. Future cross-source proxying would require a later positive rule that explicitly consumes source-composition authority; Z08 does not create it.

## Specificity-loss receipt

Every attempted proxy step deterministically records:

- requested conditioner ids;
- retained conditioner ids;
- dropped conditioner ids;
- integer loss count;
- exact loss fraction `dropped/requested`;
- proxy authority ref;
- evidence ref when present;
- attempt state;
- detail/reason.

The descriptive loss fraction is not a confidence score and not actor probability.

A selected proxy is explicitly marked:

- `projection_kind = EXPLICIT_LOWER_SPECIFICITY_PROXY`;
- `is_exact_fact = false`;
- `is_actor_belief = false`.

The exact lane remains `UNRESOLVED` beside the proxy lane.

## Source-backed evidence contract

`PossibilitySliceEvidence` is a bounded input adapter over exact producer-owned empirical evidence. It carries:

- exact empirical evidence ref;
- exact source-universe ref;
- exact release ref;
- exact target ref;
- exact retained conditioner-id set;
- typed upstream evidence state;
- governed possibility geometry/projection if supported;
- raw support if available;
- uncertainty state;
- provenance refs;
- authority refs.

It does not re-own the empirical fact. The positioned-subject result references the fact and its governed projection.

## Replay law

Result identity is hash-sealed over:

- exact positioned-subject query identity;
- model-rule semantic hash;
- model and walkback authority refs;
- exact/proxy disposition;
- exact evidence actually consumed;
- every attempted walkback step and specificity loss;
- proxy evidence actually consumed;
- source/release/target identity;
- epistemic ceiling.

Evidence supplied to the function but never inspected is not a replay determinant. This prevents an unrelated available slice from invalidating an otherwise identical result.

`verify_positioned_subject_possibility_replay(...)` re-executes the rule and requires byte-equivalent semantic material/result hash.

## Result-state meanings

`EXACT_SUPPORTED`
: exact requested grain is supported. No proxy substitutes for it.

`EXACT_UNRESOLVED_PROXY_AVAILABLE`
: exact requested grain remains unresolved; a separately labeled lower-specificity proxy is available.

`UNRESOLVED`
: exact requested grain is unresolved and no admissible supported proxy was found.

`VALID_EMPTY`
: exact requested grain is lawfully empty. No positive branch/proxy is fabricated.

`NONCOMPARABLE`
: exact requested grain is noncomparable. No proxy is used to conceal this state.

`FAIL_CLOSED`
: rule/source/authority contract is violated, including unauthorized cross-source/release proxy behavior.

## Jurisdiction ceiling

The service does not assert or mutate:

- actor belief;
- actor response;
- actor disposition;
- actor preference;
- actor choice;
- actor biography/history;
- structural position;
- causal pathway;
- normative recommendation.

A downstream subject fact remains downstream-owned. Its ref enters this service only because a separate empirical-comparability binding authorizes that exact fact as an empirical query criterion.

## PRE553 non-mutation

Z08 deliberately adds no public family to `pre553_empirical_objects.py` and does not modify `pre553_empirical_query.py`.

The existing PRE553 deferred-family marker is not promoted by side effect. This service implements the learned-world terminal capability adjacent to, and consuming, exact source-backed empirical evidence.

`EXACT_QUERY_FAILURE != PERMISSION_TO_BROADEN`

`AUTHORIZED_PROXY != EXACT_QUERY_SUCCESS`

`Z08_POSITIONED_SUBJECT_WALKBACK_R1_COMPLETE`
