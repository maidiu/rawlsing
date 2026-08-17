# Cumulative Upstream Authority / Transformation Map

**Owner:** Vozhd Dva  
**Status:** seeded; populated only by adjudicated schematic rulings

## Purpose

This file is the inherited map carried from one schematic stage session to the next.

It records everything upstream that remains relevant to later reasoning, including original authority surfaces and the accepted outputs created by each adjudicated stage.

The map is **additive and reusable**.

A later stage may directly consume an earlier-stage object when that object is useful for the later stage's assigned operation and the use respects the earlier producer's authority, epistemic state, permissions, and semantic grain.

An intermediate stage does not automatically supersede or monopolize all earlier information.

## Inheritance law

After S00 adjudication:

`pre-V553 upstream map + accepted V553 outputs → S01 inherited map`

After S01 adjudication:

`S01 inherited map + accepted V554 outputs → S02 inherited map`

Then continue identically through V555, V556, V557, V558, V3, and V2.

Each session uses the inherited map to determine:
- what information is available anywhere upstream;
- which earlier objects the current stage may use directly;
- which transformed objects are authoritative for specific derived meanings;
- what new meaning the current stage still needs to create;
- what the next stage can obtain by combining earlier reusable objects with the current stage's new outputs.

## Governing reuse law

Direct cross-stage reuse is lawful when:
- the earlier object remains authoritative for the meaning being consumed;
- the later stage has a concrete use for it;
- the later stage preserves provenance, epistemic state, uncertainty, absence/noncomparability, and permissions;
- the use does not silently reinterpret the earlier object;
- no required intermediate transformation is being bypassed for the semantic purpose at hand.

Direct reuse is defective only when it creates an authority collision, strips governing state, uses an object superseded for that specific purpose, or bypasses a transformation needed to obtain the meaning the consumer claims to use.

Thus an object may be superseded **for one use** while remaining directly useful for another.

## Row model

| Producer stage | Object / surface | Grain / stable identity | Semantic / authority class | Derived from / lineage | Epistemic state | Available for direct reuse? | Reuse conditions / prohibited uses | Later transformed variants | Named downstream need | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

`Available for direct reuse?` should use:
- `YES`
- `YES_WITH_CONDITIONS`
- `NO_FOR_THIS_USE`
- `UNRESOLVED`

Do not encode blanket stage-level prohibitions when the real restriction is use-specific.

## Composed-input law

For a downstream stage `C`, its lawful input may be composed from outputs of several earlier stages:

`C_INPUT = selected useful earlier outputs + immediately prior stage outputs + contextual/authority material`

The immediately prior stage does not need to republish everything useful upstream merely to make C's input serially self-contained.

Instead, every current stage should contribute the **new meaning it uniquely creates**, with enough lineage to connect that meaning to the earlier objects on which it depends.

## S00 seed

S00 is responsible for establishing the first adjudicated version of this map for the V553 frontier.

It must inventory at least:
- canonical V552J handoff objects/state;
- V552 structural-fact and temporal-key-source artifacts reachable by V553;
- semantic/directionality/position authority overlays used by V553 harmonization;
- thin-readiness / validation context actually consulted by V553;
- any other concrete upstream dependency discovered by the S00 workers;
- whether each object is directly reusable semantic payload, authority context, provenance context, validation context, transformed/superseded for a named use, or unresolved.

S00 must also determine what V554 can lawfully reuse directly from this pre-V553 map, because that determines the **residual meaning V553 actually needs to create**.

No speculative row becomes authority before the S00 Vozhd ruling.

## Update discipline

At each seam synthesis, Vozhd Dva:
1. confirms/corrects inherited rows relevant to the active and next stage;
2. records direct-reuse conditions for earlier objects;
3. maps what the next stage already gets from cumulative upstream material;
4. identifies the residual need the current stage must satisfy through new transformation;
5. adds accepted current-stage outputs and their lineage;
6. records any use-specific supersession or authority precedence;
7. records named downstream dependencies preventing silent loss or unnecessary duplication.

Do not duplicate the whole map inside every worker report. Workers receive the current inherited map and return only proposed changes/additions relevant to their seam.
