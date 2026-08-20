# PRE553 P09 — DISCOVERY AUTHORITY RESULT

Assignment: `PRE553-W01-P09-001`  
Agent: `PRE553_P09_DISCOVERY_AUTHORITY`  
Class: `SEAM_PREFLIGHT_SPECIALIST`  
Branch: `agent/vozhd-trii-pre553-w09-discovery-authority-preflight`  
Exact base: `e51730e461a15b0ad20f02f2efb4bccd751c2c81`  
Runtime writes: **none**  
Semantic authority: **none**

## Disposition

`AUTONOMOUS_DISCOVERY_AUTHORITY_AND_COVERAGE_RECEIPTS_FROZEN`

Return token:

`PRE553_P09_DISCOVERY_AUTHORITY_COMPLETE`

## What is frozen

P09 freezes the authority/coverage seam for the D12/D15 autonomous discovery service without selecting or implementing a runtime algorithm.

The controlling distinction is:

> the authority defines the lawful finite/finitely constructible frontier before search; the data selects which relationships inside that frontier survive exact empirical validation.

A winning relationship does not need to be individually named in advance. An unbounded search is not lawful. Individual semantic permissions do not automatically compose into arbitrary conjunction authority.

## EXACT_BOUNDED

`EXACT_BOUNDED` may claim:

`COMPLETE_FOR_EXACT_DECLARED_FRONTIER`

only when every candidate in the declared frontier `F` is evaluated, or is covered by a separately accepted mathematically equivalent/safe theorem that yields the same exact candidate-specific disposition.

The mode may share scans, factor calculations, parallelize, or use indexes. It may not skip a candidate for cost, top-k, beam width, proposal order, weak unary score, or absent unary signal while retaining the complete-for-`F` claim.

Therefore, whenever the declared frontier includes them, the exact mode must be able to reach:

- XOR / zero-unary-signal interactions;
- conditional reversals / Simpson structures;
- supported minority and non-top categories;
- recursive branch-local forks;
- same-respondent cotravel;
- branch-conditioned cotravel;
- higher-order configurations up to the declared arity/depth.

`VALID_EMPTY` means no candidate **inside the declared frontier** survived the declared validation law. It does not mean no relationship exists outside the frontier.

## ADAPTIVE_EXPLORATORY

`ADAPTIVE_EXPLORATORY` may claim:

`EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE`

Every authorized-frontier candidate must be truthfully partitionable as:

- **EVALUATED** — exact query/validation executed;
- **PRUNED** — deliberately not evaluated because a declared pruning rule fired;
- **UNEVALUATED** — neither evaluated nor explicitly pruned before the run ended.

The receipt may represent large sets by deterministic, nonoverlapping replayable set descriptors rather than enumerating every ID, but those descriptors must reconstruct the same frontier partition.

`UNEVALUATED` is never negative evidence. `PRUNED_HEURISTIC`, top-k, beam, budget, and ordinary screening are also not negative evidence. A broader completeness claim requires a separately accepted no-false-negative theorem applicable to the exact discovery class and exact input semantics.

A unary-signal screen cannot generically provide that theorem for XOR.

## Empirical fact versus diagnostic

D08 controls the empirical substrate: the canonical empirical basis is the typed respondent-conditional/joint fact with exact condition predicate, target topology, respondent/risk-set identity, routing/applicability law, measure basis, support, typed absence, authority, provenance, and replay identity.

MI/NMI, Cramer's V, entropy reduction, lift, heuristic confidence, modal-cell summaries, top-k rankings, and cloud association scores are derived diagnostics. They can be authorized to rank or propose candidates. Their numerical magnitude does not make them canonical facts and their absence/low value does not make an unevaluated relationship false.

This is required by the genealogy/correctness record: D01 shows unrestricted-pair/XOR losses under primary-star selection; D02 shows greedy/top-two recursive loss of minority and alternative branch structure; D03 shows branch-conditioned and higher-order information lost in current cloud/signature artifacts; D04 shows processing-order, replay, topology, and score defects in the current cloud implementation.

## Workload/materialization boundary

D07 remains intact. P09 does **not** create a `MATERIALIZE_ALL_PERMITTED` law.

- exact query/discovery replay must remain reconstructible;
- discovery may run on demand;
- candidate facts and score tables may be caches;
- cache/materialization policy is separate from discovery authority;
- permission to form a semantic object is not itself a command to precompute it.

## Recursive discovery

A recursive branch is a replayable discovered predicate/membership receipt, not a mandatory historical tree ontology. Each reached branch replays exact membership, constructs its own authority-bounded local frontier, and then executes under either the exact or adaptive coverage contract. Unreached adaptive branches are not negative evidence.

## Cross-source boundary

Respondent-bound discovery stays inside one empirical universe unless exact linkage authority exists. Cross-universe discovery compares source-indexed facts; shared labels, provenance adjacency, or harmonization do not create same-person linkage or pooled-universe authority.

## Files

- `DISCOVERY_AUTHORITY_CONTRACT.json`
- `EXACT_BOUNDED_COVERAGE_ORACLE.json`
- `ADAPTIVE_COVERAGE_RECEIPT_CONTRACT.json`
- `DIAGNOSTIC_NONAUTHORITY.md`
- `RESULT.json`
- `RESULT.md`

No conflict with D12/D15 was found. No runtime, semantic contract, governance, dispatch, or production code was changed.
