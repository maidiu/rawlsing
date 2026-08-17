# Cumulative Upstream Authority / Transformation Map

**Owner:** Vozhd Dva  
**Status:** seeded; populated only by adjudicated schematic rulings

## Purpose

This file is the inherited map carried from one schematic stage session to the next.

It records everything upstream that remains relevant to later reasoning, including original authority surfaces and the accepted outputs created by each adjudicated stage.

The map is **additive**, but direct-consumption permission is not.

A later stage may retain visibility of an earlier object for lineage/provenance while being forbidden to reinterpret or consume that object directly.

## Inheritance law

After S00 adjudication:

`pre-V553 upstream map + accepted V553 outputs → S01 inherited map`

After S01 adjudication:

`S01 inherited map + accepted V554 outputs → S02 inherited map`

Then continue identically through V555, V556, V557, V558, V3, and V2.

Each session must use this inherited map before constructing its own upstream availability envelope.

## Row model

| Producer stage | Object / surface | Grain / stable identity | Semantic / authority class | Derived from / lineage | Current epistemic state | Current-stage jurisdiction | Last adjudicated transformation | Named downstream need | Notes |
|---|---|---|---|---|---|---|---|---|---|

`Current-stage jurisdiction` must use one of:
- `DIRECT_INPUT_ALLOWED`
- `CONTEXT_ALLOWED`
- `LINEAGE_ONLY`
- `SUPERSEDED_BY_TRANSFORMED_OBJECT`
- `SHOULD_BE_CARRIED_THROUGH_HANDOFF`
- `DIRECT_REACH_BACK_FORBIDDEN`
- `UNRESOLVED`

## S00 seed

S00 is responsible for establishing the first adjudicated version of this map for the V553 frontier.

It must inventory at least:
- canonical V552J handoff objects/state;
- V552 structural-fact and temporal-key-source artifacts reachable by V553;
- semantic/directionality/position authority overlays used by V553 harmonization;
- thin-readiness / validation context actually consulted by V553;
- any other concrete upstream dependency discovered by the S00 workers;
- whether each object is payload, authority context, provenance context, validation context, redundant reach-back, forbidden reach-back, or unresolved.

No speculative row becomes authority before the S00 Vozhd ruling.

## Update discipline

At each seam synthesis, Vozhd Dva:
1. confirms/corrects inherited rows relevant to the active stage;
2. records the stage's admissible intake set;
3. adds accepted stage-created output objects and their lineage;
4. updates jurisdiction for earlier rows where the new transformed object supersedes direct access;
5. records named downstream dependencies preventing silent loss.

Do not duplicate the whole map inside every worker report. Workers receive the current inherited map and return only proposed changes/additions relevant to their seam.
