# R112 pre-code contract — per-prefix world-consuming native assertion

Status: frozen before the R112 code commit. Startup
`359ffcef4c2dbde0bea7233bdb8901e8ed28e9be`; High decision
`4b31a6f8e1281fe988bfd980b3f51de6250a0742:PYAT_CONTROL_ROOM/CONTINUOUS_DEVELOPMENT/R112_HIGH_P41_SUCCESSOR_DECISION.json`.
Only four paths are written: the two R06 paths and the new successor owner/test.

## New owner

`rawlsing_next/pre553_world_conditioned_progressive_service.py` exposes:

- `WorldConditionedPrefix` — actual target/conditioners/step for one admitted
  prefix;
- `consume_world_conditioned_prefixes(snapshot, catalog, prefixes)` — loads the
  exact pinned `product.nonparent.consume` (`f27d1101…`, nonparent blob
  `2181b832…`) and invokes it once per prefix through a prefix-bound service
  adapter;
- `WorldConditionedPrefixResult` — actual native receipt/material, N10E consumer
  hash, world snapshot hash, native structural routes and
  `source_balance_reads`.

The adapter reads actual catalog structural fields and actual computed prefix
cells. It does not accept caller-written final evidence or probabilities.

## R06 wiring

`progressive_world_view` builds actual world/prefix inputs, calls the new
successor owner, and attaches
`n10w.world_conditioned_prefixes` + `world_conditioned_state` to the same
progressive assertion. Each native material contains:

- actual modeled structural routes from the selected world (e.g. T0
  `ELIGIBLE`/`WITHIN_MODELED_BUDGET`, T1
  `BLOCKED_BY_MODELED_RULE`/`RESOURCE_CONSTRAINED`);
- actual source support from the prefix (`source_balance_count`, all cells,
  denominator, support state);
- `route_probability=null` and
  `NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`;
- the actual N10E consumer hash and world snapshot hash.

Prefix cell mutation changes native source support; world rule mutation changes
native structural routes; both are in the same per-prefix assertion. No
probability reweighting, smoothing, causal response or actor state is created.

## Trust / dependencies

Pinned P41 extraction, R110 world/prefix identity, actual N10E evaluator
binding, empirical/world permission checks and older owner boundaries remain.
Missing/revoked world or empirical dependency yields typed nonproductive native
material and an unavailable view; clean restore passes. Exact P41 N10W
`progressive_update_identity` remains target/ordered-only; the successor native
assertion is added by this owner, not faked into pinned historical packets.

## Qualification

Actual unlike target/prefix shape, prefix value mutation, T0/T1 world mutation,
foreign world identity, field/empirical revocation and restore, cold replay,
minority/zero retention, and the exact R109 probes. Sourcefree finite shape
only; full F5/F6/F7/F8/35/1890/actor/R09/CI/prod/N11/N12/Sorok/J52/W52 remain
held.
