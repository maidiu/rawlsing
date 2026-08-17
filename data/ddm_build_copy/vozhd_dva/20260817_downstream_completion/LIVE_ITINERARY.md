# Live Itinerary

**Status:** WAVE_0_REVIEW_AND_SCHEMATIC_PREP  
**Canonical base:** `main`  
**Coordinator:** Vozhd Dva

## Current Wave-0 state

- Integration branch: `agent/vozhd-dva-wave0-integration`
- R0-02 / PR #35: accepted + integrated.
- R0-03 / PR #36: accepted + integrated.
- R0-04 / PR #38: accepted + integrated.
- R0-05 / PR #37: accepted + integrated.
- R0-01 / PR #39: returned for a narrow fail-closed integrity fix before integration.

Wave-0 results establish concrete information-loss and runtime-starvation evidence; they do not by themselves freeze the replacement ontology.

## Immediate sequence

### 1. Finish R0-01 review loop

Require the canonical V552J→V553 adapter to distinguish missing/unreadable/malformed canonical artifacts from valid empty data and to fail closed rather than silently normalizing read failure to emptiness. Preserve the core V553-side `POSTG5-004` repair direction.

### 2. Run schematic transformation breakouts

Use `schematics/SESSION_INDEX.md` and `schematics/TRANSFORMATION_METHOD.md`.

The primary question at every seam is:

`what upstream actually establishes → what this stage lawfully consumes → what new meaning this stage creates → what it must emit → what the next stage needs`

Sessions:
- S00 V552J→V553
- S01 V553→V554
- S02 V554→V555
- S03 V555→V556
- S04 V556→V557
- S05 V557→V558
- S06 V558→V3
- S07 V3→V2

Launch forward and backward perspectives independently. Add hostile critics at S02/S03. Production semantics remain read-only during breakout work.

### 3. Reconvene with the class

Vozhd Dva compares breakout models in `schematics/synthesis/`.

Reconcile upstream-to-downstream because the accepted output of one seam becomes the input law of the next. Pay particular attention to shared object grains across:
- S01/S02;
- S02/S03;
- S04/S05/S06.

For every seam, freeze only:
- transformation equation;
- output object grain;
- preserve/derive/reformat/aggregate/drop/forbid/unresolved law;
- implementation obligations;
- explicit unresolved authority;
- tests proving the seam.

No worker-local proposal becomes system law before this synthesis.

### 4. Update the common capability matrix

Map accepted seam contracts onto the five vertical slices and verify that every required field has a lawful producer and downstream consumer.

### 5. Launch Wave 1 implementation

Only after schematic adjudication, produce non-overlapping implementation packets for the accepted transformations:
- V553/V554;
- V555;
- V556;
- V557/V558;
- vertical production adapters/tests.

Implementation workers should not be asked to solve unresolved ontology while coding.

### 6. Vertical court

Use the Wave-0 harness as the standing court. Convert each production-gap XFAIL only when actual stage outputs prove the corresponding semantic chain.

### 7. Horizontal qualification

Once the representative chain works:
- representative multi-wave/source families;
- adversarial source structures;
- broad corpus qualification;
- common defects first, source-specific exceptions only where governed evidence requires them.

### 8. Runtime rebuild

After V558 is proven sufficient:
- V3 causal/temporal state, pressure-flow, actor-specific attractor realization;
- genealogy/household orchestration;
- V2 phenomenology/conversation against a read-only V3 state/history boundary.

### 9. App/demo completion

Optimize for one polished, auditable, demonstrable vertical path. Defer nonessential breadth.

## Active risks

- R0-01 canonical consumer repair must preserve fail-closed integrity semantics.
- Schematic expansion must terminate in implementable seam rulings; no general ontology encyclopedia.
- Downstream needs cannot authorize unsupported upstream invention.
- Stage-local elegance cannot substitute for end-to-end semantic continuity.
- Workers must receive enough neighboring context to understand consequences without acquiring neighboring implementation authority.

## Decision log

- 2026-08-17: current `main` established as implementation authority/frontier.
- 2026-08-17: rejected serial independent stage completion; adopted bounded verticalization.
- 2026-08-17: Enneagram-like attractor formation affirmed as intended design component; V556 supplies structural prerequisites/topology and V3 realizes actor-specific formation.
- 2026-08-17: established Vozhd Dva control room with isolated prongs, Rabochii cells, integration state, reviews, and restart state.
- 2026-08-17: made worker-context selection a Vozhd Dva responsibility.
- 2026-08-17: Wave 0 launched as five concurrent bounded assignments.
- 2026-08-17: R0-02/R0-03/R0-04/R0-05 accepted into Wave-0 integration; R0-01 held for narrow integrity correction.
- 2026-08-17: added a dedicated schematic transformation layer and made seam-by-seam forward/backward adjudication a required pre-implementation phase.

## Next Vozhd Dva action

Close R0-01's narrow review issue, then construct and launch the S00–S07 schematic breakout packets from the canonical seam workspaces.
