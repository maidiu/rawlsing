# W56G — TRANSITIVE CANONICAL-PREDECESSOR REPAIR

Status: `LOCAL_COMPLETE_UNRECONCILED`

Input hostile audit:

`W56F @ d7f1c44693e3baad124cdfc3b54fe0dfb4422453`

W56F blocker:

`BLOCKED__CANONICAL_PREDECESSOR_TRANSITIVE_DEPENDENCY_GAP`

## Exact repair

The canonical-predecessor meta-validator is now a standalone Python-stdlib program.

It imports **no Rawlsing governance helper** and does not execute candidate-side governance code.

The predecessor gate now obtains every trusted governance dependency directly from exact immutable live-canonical objects using `git show <LIVE_CANONICAL_SHA>:<path>`.

Trusted dependency closure is explicitly limited to and machine-checks at minimum:

- the predecessor script itself;
- `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`;
- `HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json`;
- `HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`.

The two hostile-audit schemas are validated by a schema-subset engine embedded in the standalone canonical predecessor script. Candidate-side `governance_r2_support.py`, candidate-side schema loaders, candidate-side Git/ref helpers, and candidate-side schema files therefore cannot influence predecessor authorization.

The standalone gate requires all trusted dependency paths to be present in the **live canonical protected manifest** and fails closed if any required canonical dependency is absent/unparseable.

## Prior W56D bounded-parent repair

Preserved unchanged: bounded execution requires exact parent/child decision-domain equality in addition to deep parent grounding and scope inclusion.

## Authority / runtime effects

- Ground changes: `0`
- PROJECT_STATE changes: `0`
- OPEN_OBLIGATIONS changes: `0`
- runtime changes: `0`
- serving changes: `0`
- semantic authority promotions: `0`
- PRE-MAIN movement: `0`
- main movement: `0`

## Disposition

This repair is not self-certified and is not yet PRE-MAIN.

Required next action:

`fresh hostile W56H audit of exact final W56G candidate, focused on canonical predecessor dependency closure and regression of the already-closed bounded-parent seam.`
