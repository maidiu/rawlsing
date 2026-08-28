# I08 — INDEPENDENT ANTI-CHEAT / REPLAY CONTRACT R1

Contract id: `I08_INDEPENDENT_VALIDATION_CONTRACT@1.0.0`

Status: `MERGE_INDEPENDENT__POST_MERGE_ADAPTER_REQUIRED`

## Purpose

This contract allows HQ to validate the integrated Authority-37 fracture-map implementation without letting the validation oracle become part of the controller's answer-generation path.

The contract is implementation-shape neutral. I08 did not read I01-I07 implementation findings and therefore does not freeze any sibling API, class name or file layout.

## Hard independence law

`ORACLE_MAY_JUDGE_OUTPUT_AFTER_RUN != ORACLE_MAY_SEED_CONTROLLER_INPUT`

The generation-side caller may provide only lawful root operation material such as root query/scope/source/authority/controller-policy refs. It may not provide or indirectly encode:

- modal response or modal pattern;
- a primary/winning predictor;
- respondent membership of a discovered branch;
- a secondary splitter;
- a desired grandchild path;
- cotravel/co-signature target pairs or triples selected because the oracle already knows them.

G04/L02/L03 expected answers remain acceptance-side evidence. They are not controller inputs.

## Required normalized bundle

A post-merge adapter must export one JSON-like bundle with these semantic sections. Field names may be translated by the adapter, but the evidence may not be fabricated.

### `contract_version`

Must equal `I08_INDEPENDENT_VALIDATION_CONTRACT@1.0.0`.

### `authority_identity`

Exact authority/policy identity governing the run. Exact replay comparison is meaningful only when this identity is unchanged.

### `caller_request`

The exact generation-side request after adapter normalization. This is inspected recursively for forbidden oracle-answer fields.

The adapter must expose supplied hints/overrides rather than silently dropping them before validation.

### `lawful_candidate_catalog`

Map:

`node_ref -> complete independently lawful candidate refs`

This is an independent acceptance-side catalog derived from exact source/instrument/coordinate/response authority. It MUST NOT be reconstructed from the controller's own declared frontier, because doing so would make score/top-k/prevalence pruning invisible to the validator.

### `generations`

Each generation/node must expose:

- `node_ref`;
- `frontier.declared_candidate_refs`;
- `frontier.sealed_hash`;
- `frontier.seal_event_index` or an information-equivalent total-order proof;
- `frontier_mutation_events`;
- `evaluation_events`, each with candidate ref and event order;
- `pruning.mode`;
- `pruning.removed_candidate_refs`.

Binding invariants:

1. declared frontier identity is canonical/hash-sealed;
2. seal precedes all candidate evaluation;
3. no mutation occurs after the seal while that I05 invocation is open;
4. declared refs exactly equal the independent lawful candidate catalog;
5. every declared candidate is evaluated;
6. no score, top-k, prevalence, topic relevance or caller hunch removes a lawful candidate;
7. no undeclared candidate is evaluated.

The normalized no-prune identity is:

`NONE_EXACT_EVALUATE_ALL`.

## Branch evidence

Each discovered branch entry must expose:

- exact `branch_ref`;
- exact `parent_ref`/ancestry relation;
- exact branch role if positively governed;
- normalized predicate evidence;
- `membership_source`;
- exact `handoff_ref` or replay-binding ref;
- `retained`;
- continuation disposition;
- exact stop reason where stopped.

### Predictor complement guard

For a `NOT P` branch the predicate evidence must include an exact resolved-coordinate guard such as `CR(P)` or an information-equivalent ref.

Missing, not-asked, inapplicable, unresolved, unavailable or unknown predictor states may not enter the predictor-absent complement.

Normalized forbidden predictor special states include:

`MISSING`, `NOT_APPLICABLE`, `INAPPLICABLE`, `UNKNOWN`, `NOT_ASKED`, `UNRESOLVED`, `UNAVAILABLE`.

### Substantive NM guard

`NM` must be an explicit set of substantive nonmodal response patterns/cells. It cannot be implemented as bare `NOT M` over every remaining response state.

DK/refusal/missing/not-applicable/unavailable/unknown remain typed separately and may not be swallowed into substantive NM.

### Exact branch handoff/replay

Every discovered branch in the normalized branch list must carry exact handoff/replay evidence:

`membership_source = EXACT_HANDOFF_REPLAY`

plus a nonempty exact handoff/replay ref.

The adapter may not reconstruct branch membership privately to make this check pass. If the integrated implementation lacks exact handoff evidence, return an explicit validation failure/unverifiable result.

## Retention contract

For any stop disposition:

- `RETAIN_REPORT_ONLY_STOP`;
- `RETAIN_TERMINAL_STOP`;
- `RETAIN_TYPED_NONPOSITIVE_STOP`;

the branch/result must remain retained and must carry an exact stop reason.

Every retained branch must also survive into the public map closure, represented by its exact branch ref in `public_map.retained_branch_refs` or a proven information-equivalent exact-ref closure.

`STOP_RECURSION != DELETE_BRANCH`.

## Higher-order topology contract

Each topology result exposes:

- `arity`;
- exact ordered/canonical `target_refs`;
- `source_kind`;
- direct exact `joint_fact_refs`;
- whether it was `derived_from_pairwise_only`.

For J=3 under Authority 37:

- arity is exactly 3;
- there are exactly three target refs;
- source kind is `EXACT_SAME_RESPONDENT_JOINT` or proven equivalent;
- direct joint fact/tensor/pattern refs exist;
- `derived_from_pairwise_only` is false.

A pairwise projection may never be relabeled J=3. J>3 fails closed under Authority-37 acceptance unless later authority explicitly supersedes this ceiling.

## Jurisdiction firewall

The normalized public output layer is empirical.

Forbidden nonempty fields include actor belief/state, persona, personality, V3 person/state and causal actor labels. Equivalent semantic leakage is also a failure even if a different implementation field name is used.

`EMPIRICAL_BRANCH_FIELD != ACTOR_BELIEF_OR_PERSONALITY`.

## Exact replay mode

Two normalized bundles with identical:

- determinant values;
- authority identity;

must have identical:

- per-node frontier identities;
- map identity;
- replay identity;
- dependency-addressable artifact identities.

Otherwise fail:

`NONDETERMINISTIC_REPLAY_IDENTITY`.

## Determinant mutation / noninterference mode

The adapter must provide:

- `determinant_values`;
- exact `dependency_graph`;
- `artifact_identities`.

The dependency graph is a DAG-like exact dependency declaration:

`artifact -> direct determinant/artifact dependencies`.

For a controlled mutation set C, compute transitive dependency closure for each artifact A.

If A does not depend on any member of C:

`IDENTITY_AFTER == IDENTITY_BEFORE`.

If A does depend on at least one member of C:

`IDENTITY_AFTER != IDENTITY_BEFORE`.

The dependency graph itself must remain identical across the paired comparison; it cannot be rewritten after seeing the mutation to excuse extra invalidations or hide missing ones.

This is the exact anti-cheat relation:

`DEPENDENT_ARTIFACT_MUST_INVALIDATE`

and

`INDEPENDENT_ARTIFACT_MUST_STAY_STABLE`.

The G04 R-only perturbation is the canonical acceptance example: only R-dependent topology may change.

## Adapter law

The future integrated adapter MAY:

- read exact evidence already emitted by the integrated implementation;
- canonicalize field names/order into this contract;
- independently enumerate the lawful acceptance candidate catalog from exact governed source/authority metadata;
- compare completed output to G04/L02/L03 expected oracles after the autonomous run.

It MUST NOT:

- execute a private branch predicate to fabricate missing handoff membership evidence;
- use controller output as the sole source of `lawful_candidate_catalog`;
- infer J=3 from J=2 results;
- fabricate public-map retention after a stopped branch was dropped;
- strip caller oracle hints before the anti-leakage check;
- synthesize missing replay identities;
- infer a pass where required evidence is absent.

Missing required observability is a fail/unverifiable disposition, not permission for the adapter to repair semantics.

## Production-independent executable

`independent_validation_prep.py` implements the normalized contract with Python standard library only. Its self-test is intentionally synthetic and tests the validator, not production Rawlsing.

The executable must remain sibling-independent until HQ explicitly points a later adapter at an integrated implementation.

`I08_INDEPENDENT_FRACTURE_MAP_VALIDATION_PREP_R1_COMPLETE`
