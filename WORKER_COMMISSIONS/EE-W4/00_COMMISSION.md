# EE-W4 — A/B/C HOSTILE + OPERATIONAL MEASUREMENT HARNESS R1

Status: `COMMISSIONED`

Repository: `maidiu/rawlsing`

Exact branch: `agent/rabochii-prev3-ee-w4-abc-hostile-measurement-harness-r1`

Commission base: `40a79b595270a9a3bbec019ed1ef1867ccd505f5`

## Role

You are **A/B/C HOSTILE + OPERATIONAL MEASUREMENT HARNESS / EE-W4**.

Build the candidate-neutral execution/measurement shell needed for the eventual final Chetiri A/B/C decision. Do **not** run the final comparison and do not choose a winner.

This lane exists so that after EE-W1 freezes the exact semantic workload, the same manifest can be executed against A/B/C with identical logical work while capturing the physical quantities Chetiri actually needs.

## Canonical start

Read current HQ authority from `HQ_HANDOFF/LATEST.json`, then read:

- `.../PREV3_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1/01_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1.md`;
- `02_ABC_COMPARISON_AND_CLOSURE_SEQUENCE.md`;
- `04_REQUIREMENT_MATRIX.json`;
- accepted C09 measurement law, exact-order law, HB04/HB05 common A/B/C harnesses, Route A/B/C qualification returns, and D17 return;
- ASTRA-D02-R2 runtime receipt only insofar as runtime provisioning must remain candidate-neutral.

Do not reduce the final comparison to old OP014 alone. The final harness must be capable of consuming the expanded EE01–EE16 workload manifest once frozen.

## Exact grain

`IMPLEMENT_CANDIDATE_NEUTRAL_MANIFEST_DRIVEN_ABC_MEASUREMENT_AND_HOSTILE_NON_LOSS_HARNESS_ONLY`

## Required harness capabilities

The harness must accept a frozen workload manifest and execute each eligible `(candidate, universe_id, operation_id)` cell with no candidate-specific semantic branching.

It must capture at minimum:

- semantic result/oracle PASS/FAIL;
- typed missing-authority / ineligible / noncomparable state distinct from candidate failure;
- cold wall time;
- warm/repeat wall time;
- CPU where lawfully measurable;
- peak RSS;
- scratch bytes;
- durable bytes created/retained;
- source opens/decodes;
- bytes read where measurable;
- cache/index creation;
- replay time;
- delete/regenerate time;
- cold rebuild time;
- selective invalidation time and rewritten-byte count after one source change;
- selective invalidation time and rewritten-byte count after one semantic/routing-authority change;
- learned-product release/replay identity;
- deterministic output identity;
- explicit candidate/universe/operation identity;
- failure-class accounting.

The harness must support repeated-run schedules at least `cold`, `warm_1`, `warm_2`, `warm_5` or an equivalent exact schedule justified by current comparison law.

## Hostile non-loss shell

Provide executable fixture/oracle support for the hostile cases frozen in the common contract, including:

- equal marginals / different k-way joint;
- XOR-like higher-order structure;
- minority-supported configuration;
- recursive subgroup fork;
- denominator disagreement;
- observed zero vs unknown/null;
- source zero vs semantic zero;
- explicit noncomparability;
- routing ambiguity;
- same numeric value / semantically distinct source slots;
- ranked/multiselect topology;
- rebuild identity preservation;
- missing authority that must not count as candidate failure.

Do not invent substantive survey meanings merely to create fixtures; use synthetic fixtures only for the hostile structural property being tested, and keep them clearly distinct from real-source performance cells.

## Candidate neutrality

Hard law:

`SAME_MANIFEST + SAME_ELIGIBLE_UNIVERSE_CELL + SAME_OPERATION + SAME_ORACLE + SAME_METRIC_DEFINITION`

No candidate-specific pruning, warmup, caching allowance, source preprocessing, search budget, output weakening, or hostile-case exemption.

A candidate may have a physically different implementation only where the common contract allows physical variation.

## Deliverables

Under `WORKER_RETURNS/EE-W4/` produce:

1. `00_RETURN.md`
2. `01_HARNESS_CONTRACT.json`
3. `02_METRIC_DEFINITIONS.md`
4. `03_FAILURE_AND_INELIGIBILITY_TAXONOMY.json`
5. manifest-driven harness implementation + tests if feasible;
6. `04_HOSTILE_FIXTURE_ORACLE_INDEX.json`
7. `05_INTEGRATION_NOTES_FOR_EE_W1_MANIFEST.md`

Your tests must prove that:

- omitted semantic work cannot score as a win;
- missing source/semantic authority is typed as ineligible/unresolved, not performance failure;
- a semantic-oracle mismatch fails a cell regardless of speed;
- candidate ordering does not affect logical results;
- repeat/warm state is isolated and explicit;
- delete/rebuild and invalidation tests preserve semantic identity requirements;
- metric aggregation never pools empirical observations across distinct universes.

## Boundaries

No final A/B/C run.
No ranking.
No architecture retirement.
No workload-definition authority beyond consuming the current common contract and future EE-W1 manifest.
No source-semantic inference.
No Field Forge/Dva/V3 redesign.
No MAIN or semantic PRE-MAIN mutation.

PASS means the harness is ready to consume the eventual frozen EE-W1 manifest without semantic redesign.

Commit the governed return and report final branch tip.