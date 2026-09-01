# FFX002 R2 — VIEW ABLATION CONTRACT

Status: `PREREGISTERED_DESIGN__NO_EXECUTION`

## 1. Rule

No view earns architectural weight because it is attractive, interpretable, technically sophisticated, or capable of answering a question that no downstream consumer needs.

For each declared query family, evaluate the weakest lawful information source first, then add and remove views.

## 2. Baseline ladder

### S0 — substrate/marginal baseline

Uses the common observation/provenance substrate only to provide exact risk set, source facts, marginals, support, and provenance. It makes no higher representation claim.

### C1 — direct conditional baseline

Adds Core C. This is the weakest mandatory analytical view capable of answering bounded redistribution questions.

### A1 — exact configuration augmentation

Adds Core A to C1. Tests whether exact conjunction/minority/higher-order facts change or improve the bounded answers.

### B1 — geometry augmentation

Adds Core B to the weakest baseline that can state the query. For position→disposition possibility queries the main comparison is `C1+A1` versus `C1+A1+B1`.

### MV — multi-view package

Contains only views that individually pass their admission/loss contracts. Optional views D/E/F may be added only in later preregistered phases.

## 3. Mandatory add/remove comparisons

For every target view V:

1. `WEAKER_BASELINE`
2. `WEAKER_BASELINE + V`
3. `FULL_ADMITTED_SET`
4. `FULL_ADMITTED_SET - V`
5. query-level comparison on frozen holdout
6. complexity and loss comparison
7. hostile-test comparison

The "weaker baseline" is query-specific. A view cannot be credited for answering a query whose prerequisites the baseline intentionally lacks unless that query was preregistered as downstream-needed.

## 4. Core first-canary questions

### Does geometry add anything over exact configuration + direct conditional?

Compare:
- `A+C`
- `A+B+C`

Geometry adds material value only if it supplies a needed stable relation or improves heldout fidelity/compression under `08_INCREMENTAL_VALUE_METRICS.tsv` without violating a critical invariant.

### Does exact configuration add anything over geometry + direct conditional?

Compare:
- `B+C`
- `A+B+C`

Configuration adds material value if exact minority/contradictory/higher-order facts or query accuracy unavailable from B+C are required and preserved by A.

### Is direct conditional already sufficient?

Compare:
- `C`
- `A+C`
- `B+C`
- `A+B+C`

If A/B add no material bounded query value and do not preserve a required invariant unavailable in C, return a weaker-view-sufficient result. Do not preserve stronger views by prestige.

## 5. Optional-arm admission by ablation

### Measurement topology graph
First canary default: control, not competitor. Promote to analytical arm only when a predeclared topology query cannot be represented more weakly.

### Motif
Admit only if motif retrieval produces stable, null-distinct, query-relevant gain beyond A+C.

### Latent/model
Admit only if heldout/compression or multimodality value survives model/seed/specification perturbation beyond A+C.

## 6. No beauty metric

Forbidden evidence:
- visual elegance;
- sociological suggestiveness;
- easy narrative axis labels;
- compactness without fidelity;
- more discovered objects;
- algorithmic complexity itself.

## 7. Loss veto

A target view can be `ADDS_VALUE_BUT_DESTROYS_CRITICAL_INVARIANT`. Such a result may justify a supplementary role or multi-view retention; it cannot justify replacing the weaker view that preserves the required invariant.

## 8. Output

Each ablation row must include:
- query_id;
- baseline_views;
- added_or_removed_view;
- invariant requirements;
- loss delta;
- heldout metric delta;
- complexity delta;
- hostile-test status;
- uncertainty;
- materiality ruling;
- claim ceiling.
