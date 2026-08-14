# V552 Blocker C4: Asian Barometer W1/PH Source Contract

## Terminal blocker

`Asian Barometer_W1_PH` remains `BLOCKED_V552_OUTPUT_CONTRACT` after the C0 repair. All four selected distributions have certified upstream directionality metadata, but each contains `scale_direction=descending` together with semantic response directions that the V552 signed-component consistency check rejects. The compiler therefore produces `no_eligible_components|direction_scale_inconsistency` for every distribution.

The resulting readiness is:

- pressure candidates: 4
- observed pressure: 0
- noncomputable pressure: 4
- invalid output-contract rows: 202
- input contract: PASS
- semantic/scale consistency: BLOCKED

## Why execution stops

The failure is in the governed input contract, not in V552J and not in the validator. Correcting it requires deciding whether the source scale direction or the certified semantic direction is authoritative, or supplying a reconciled authority row. The bounded task forbids inferring or rewriting that authority. V552J is therefore not run.

## Required next action

Resolve the four Asian Barometer W1/PH distributions in the upstream governed atom/scale authority, then rerun the same frozen V552 scope. Do not suppress the inconsistency or treat zero observed pressure as acceptance.
