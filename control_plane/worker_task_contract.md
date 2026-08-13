# Worker task contract

Worker execution is intentionally **broad in implementation scope and narrow in interpretive discretion**.

A worker assignment may cover an entire bounded stage/campaign. It must not require the worker to repeatedly return for ordinary implementation decisions.

## Mandatory opening sequence

1. Read `RAWLSING_CONTROL_PLANE.md`.
2. Run:
   ```bash
   python3 control_plane/rawlsingctl.py verify --tier repo
   python3 control_plane/rawlsingctl.py status
   python3 control_plane/rawlsingctl.py next
   ```
3. Read the exact governing authority/receipt references named for the stage.
4. Resolve the current accepted implementation entrypoint and exact bounded inputs from repository/artifact evidence.
5. Freeze the run court and scope before inspecting outcome-bearing respondent results.
6. Make no code modification until the worker can state:
   - stage;
   - entry gate;
   - court;
   - exact acceptance predicates;
   - exact claim ceiling;
   - forbidden changes.

## Implementation autonomy

Fix autonomously and continue when the defect is ordinary and semantics-preserving, including:
- path/loader bugs;
- checkpoint/resume bugs;
- serialization/adapter bugs;
- caching/vectorization/performance bugs;
- dtype/index/regex inefficiency;
- schema-shaped valid-empty handling;
- deterministic output/manifest defects;
- tests that fail because the implementation violates an already-governed contract.

Every repair needs a regression/equivalence test. Do not return for micro-adjudication.

## Hard central stop

Stop only when proceeding would require changing:
- semantic authority;
- frozen denominator/topology membership;
- respondent routing/universe truth;
- source/wave/country scope for semantic reasons;
- missingness meaning;
- weights/support thresholds or design rules;
- semantic eligibility;
- validator/court predicate meaning;
- privacy boundary;
- layer ownership/inference ceiling/architecture.

A hard stop return must identify the exact authority/gate and smallest decision needed. "The code is inconvenient" is not a governance blocker.

## Change classification

Before editing, classify the change using `control_plane/change_policy.json`.

- C0 implementation: worker may normally repair.
- C1 interface: worker may repair only if semantic meaning is unchanged and seam tests prove it.
- C2 authority: central stop.
- C3 architecture: central stop.
- C4 data execution: worker may repair exact affected scope under unchanged authority.

## Return discipline

One consolidated return, not a stream of micro-questions.

A terminal return records:
- stage and court;
- base commit and final commit;
- exact inputs/authority hashes;
- exact scope;
- commands executed;
- files changed;
- tests and pass/fail counts;
- differential findings;
- accepted terminal or honest blocker;
- allowed claim now established;
- forbidden claims still forbidden;
- privacy result;
- output/reproduction manifest hashes;
- successor obligations/technical debt discovered.

If accepted, add a new immutable privacy-safe receipt and only then advance `control_plane/current.json`.

Never edit an accepted receipt in place.
