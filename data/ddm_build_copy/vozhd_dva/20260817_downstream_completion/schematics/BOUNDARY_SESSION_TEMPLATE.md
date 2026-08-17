# Boundary Session Template

**Seam:** `<UPSTREAM> → <CURRENT_STAGE>`  
**Current stage downstream consumer:** `<NEXT_STAGE>`  
**Session status:** `UNOPENED | BREAKOUT_ACTIVE | READY_TO_RECONVENE | VOZHD_ADJUDICATED | IMPLEMENTATION_BOUND`  
**Canonical code ref:** `<sha/ref>`

## A. System position

One paragraph: what has already been established upstream, what new responsibility belongs to the current stage, and what the next stage is supposed to do.

## B. Upstream outgoing authority

| Object / field / state | Grain | Authority / epistemic state | Why it matters downstream |
|---|---|---|---|

## C. Current intake

| Upstream object | Current consumer path | Loss / distortion / mismatch | Disposition |
|---|---|---|---|

## D. Transformation equation

`<input grain> → <stage-authorized operation> → <output grain>`

Explain what new information becomes knowable here and why this stage, specifically, owns that transformation.

## E. Preservation / transformation ledger

| Incoming distinction | PRESERVE / DERIVE / REFORMAT / AGGREGATE_WITH_LINEAGE / DROP_EXPLICITLY / FORBIDDEN_TO_INFER / UNRESOLVED | Output representation | Reason |
|---|---|---|---|

## F. Required stage output

Define the minimum object(s) this stage must emit. Include stable identity, provenance, uncertainty/authority state, and typed negative states where needed.

## G. Next-stage backward requirements

| Next-stage operation | Information it requires from this stage | Why | Must not be pre-resolved here |
|---|---|---|---|

## H. Forward / backward reconciliation

For each requirement, classify `MEETS`, `UPSTREAM_INFORMATION_LOSS`, `MISSING_AUTHORITY`, `MISPLACED_RESPONSIBILITY`, `CONTRACT_GAP`, or `REPRESENTATION_GAP`.

## I. Worked transformations

### Ordinary case
Follow one concrete upstream object through intake, operation, and output.

### Adversarial / ambiguous case
Use contradiction, absence, noncomparability, temporal ambiguity, or inference pressure to show what must remain unresolved or fail closed.

## J. Current seam defects

Finite defect list, each with producer, consumer, evidence, required behavior, and owner.

## K. Proposed implementation obligations

Only concrete obligations that could be handed to an implementation worker after Vozhd adjudication.

## L. Unresolved questions for reconvening

Questions workers may disagree about. Do not bury them in prose.

## M. Adjacent seam notifications

State which neighboring boundary sessions must consume this result and what they need to know.

## N. Vozhd ruling

Filled only after reconvening:
- accepted transformation equation;
- accepted output grain;
- accepted preservation law;
- rejected alternatives and why;
- implementation owner(s);
- tests that must prove the ruling.
