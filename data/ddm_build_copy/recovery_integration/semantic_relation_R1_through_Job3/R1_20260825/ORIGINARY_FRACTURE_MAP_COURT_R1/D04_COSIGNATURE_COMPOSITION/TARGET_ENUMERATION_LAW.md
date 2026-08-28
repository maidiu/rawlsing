# D04 Target Enumeration Law R1

## Purpose

Close the G02/G03/G05 caller-knowledge gap without turning target selection into data-derived semantic search.

The controller must be able to ask, for an exact discovered branch, “which other lawful substantive response surfaces co-travel here?” without a human or fixture naming the answer in advance.

This law governs **reachability of target questions/responses**, not empirical support outcomes.

## Core law

`TARGET_REACHABILITY MUST PRECEDE TARGET OUTCOME INSPECTION`

For a discovered branch `B`, define an exact finite target catalog `C` from governed source/instrument metadata and positive response-semantic authority. `C` is sealed before any branch-conditioned co-signature query runs.

The controller then enumerates the complete authorized J=2 frontier from `C` mechanically.

No empirical result, diagnostic score, association value, language-model judgment, researcher intuition, historical cloud ranking, or semantic relation label may add or remove a target after co-signature evaluation begins.

## Required catalog identity

The target catalog must have a deterministic exact identity over at least:

- operation/contract id;
- source release/instrument refs;
- empirical universe refs;
- target question/response refs;
- response topology/semantic refs;
- routing/applicability refs or exact rules that resolve them;
- explicit inclusion/exclusion classification per target;
- authority refs governing inclusion;
- canonical target ordering;
- replay/source locator sufficient to regenerate the same catalog.

The catalog can be represented inside an adopted `DiscoveryAuthority.candidate_universe_definition` or another existing exact authority object if that surface preserves the entire finite target set and exclusion law. A new semantic target-registry family is not required merely for convenience.

## Positive eligibility

A target is eligible only if all conditions are satisfied:

1. **Substantive response identity** — target is an exact governed survey/opinion/attitude response or question surface, not a positional coordinate.
2. **Source legitimacy** — its source release/instrument/universe is authorized for the branch operation.
3. **Respondent binding** — the target can be joined to the branch by exact same-respondent identity under current source relation law.
4. **Routing closure** — applicability/routing semantics are exact enough to determine the target-question denominator.
5. **Response-state closure** — substantive, missing, source-specific special, refusal/DK/inapplicable and other governed states remain distinguishable.
6. **Topology closure** — multiplicity/order/multiselect/scalar semantics are known and compatible with the requested J=2 operation.
7. **Measure closure** — the requested RAW or governed weighted measure has exact authority; lack of weight authority cannot be repaired by default-one weighting.
8. **Replay closure** — target identity and its membership/evaluation basis can be replayed exactly.

## Mandatory exclusions

The following may not become co-signature attitude nodes:

- demographic coordinates;
- geographic/position/structural coordinates when used as empirical-position facts;
- branch role labels such as conformer/deviant/minority as if they were attitudes;
- actor/persona/personality/belief labels;
- inferred causal properties;
- diagnostic score fields;
- downstream semantic relation labels;
- missingness/routing/weight bookkeeping fields as substantive attitudes;
- targets lacking exact source/routing/response semantics.

Coordinates remain lawful **conditioners/branch-definers** where separately authorized. Excluding them from target nodes does not erase their branch ancestry.

## Anchor/self exclusion

The discovered branch may contain an anchor substantive response. The controller must not manufacture trivial “co-signature” by pairing a target with the exact same target identity or by retyping the branch predicate itself as another response node.

Rules:

- duplicate exact target refs collapse;
- self-pairs `(T_i,T_i)` are forbidden;
- if an anchor response ref is present in the target catalog, its relationship to other targets may be evaluated, but its identity must remain explicit;
- a derived branch cohort is a condition context, not itself one target slot.

## Canonical pair enumeration

Given canonical eligible target refs:

`T = sort_unique(C.eligible_targets, key = exact_ref_key)`

Current lawful pair frontier:

`P = {(T_i,T_j) | i < j and exact authority permits the pair}`

Every authority exclusion must be explicit and replayable. There is no implicit “not interesting,” “too weak,” “too far,” or “not semantically related” exclusion.

If no pair-specific exclusions exist:

`|P| = |T| * (|T|-1) / 2`

The ref-only topology closure must bind the exact catalog and expected/evaluated pair counts so completeness is auditable.

## Response-value enumeration inside a target

Question reachability and response-value/cell reachability are separate layers.

For each eligible target, allowed substantive response values/pattern cells must come from exact response-semantic/topology authority. The controller may not discover a new substantive code meaning from frequency shape alone.

For multi-select targets, preserve both when authorized:

- response-presence semantics;
- exact/governed response-pattern semantics.

Presence must not substitute for pattern identity.

## Relationship to current I05

Current I05 can mechanically expand declared atom/template pools and evaluate the complete declared frontier. That machinery may be reused after the controller has lawfully frozen the target catalog and generated exact query/candidate material.

The repair is therefore not “let I05 guess another question.” It is:

1. authorize the finite target universe;
2. enumerate it deterministically;
3. freeze exact J=2 branch-conditioned queries/rules;
4. hand the fixed frontier to current exact execution;
5. return exact result refs and coverage.

## No outcome-driven widening

A supported pair may become learned branch context, but it does not authorize a third target under current J=2 law.

A future adaptive controller may reorder evaluation of an already frozen target frontier if separately authorized, but it may not widen the target universe from diagnostics unless a new authority expressly governs that behavior and its replay/coverage semantics.

## Typed failure states

Target enumeration fails closed when:

- source/instrument target universe cannot be made finite and exact;
- substantive-versus-positional role is unresolved;
- same-respondent source relation is unresolved;
- routing/applicability is unresolved;
- response topology/multiplicity is unresolved;
- requested measure is unauthorized;
- replay identity cannot be sealed;
- requested target arity exceeds current authority.

A failure to authorize a target is not empirical evidence that the target does not co-travel.

## Output

Target enumeration returns only exact catalog/query refs plus typed inclusion/exclusion/closure metadata. It does not emit semantic interpretations of why targets co-travel.
