# Executed tests, severance, and JUnit

All commands ran from `candidate/` on `oldMac` with:

```text
Python 3.11.3
pytest 9.1.1
SQLite 3.40.1
PYTHONDONTWRITEBYTECODE=1
```

## 1. Full same-consumer suite

```sh
cd candidate
BP4R_C9_DIR="$PWD" PYTHONPATH="$PWD" \
  python3 -m pytest -o addopts='' -q tests \
  --junitxml=evidence/cp_a5_junit.xml
```

Exit `0`; `59 passed in 30.50s`.

JUnit artifact: `candidate/evidence/cp_a5_junit.xml`.

```text
tests=59 failures=0 errors=0 skipped=0
```

## 2. Old regressions preserved unchanged

| Surface | Command | Result |
|---|---|---:|
| BP2P4J product | `pytest tests/test_joined_product.py` | 10 passed |
| BP2P4J security | `pytest tests/test_joined_security.py` | 12 passed |
| BP2P4J severance | `pytest tests/test_joined_severance.py` | 7 passed |
| source closure | `pytest tests/test_source_closure.py` | 4 passed |
| BP4R guard | `BP4R_C9_DIR=$PWD pytest tests/test_bp4r_candidate.py` | 9 passed |
| I1 guarded consumer | `pytest tests/test_i1_guarded_consumer.py` | 8 passed |
| CP-A5 new | `pytest tests/test_cp_a5_multicontext.py` | 9 passed |

The old 50 tests were copied from I1 without changing assertions or expectations.
The ten BP2P4J severance trials still report baseline PASS, edge-specific RED,
and restored PASS.

## 3. New A3-A5 tests

### Intact

```sh
pytest -o addopts='' -q tests/test_cp_a5_multicontext.py
```

`9 passed`, exit `0`.

The intact test asserts:

- 3 inspections, 2 contexts, test-only disposition `ESTABLISHED`;
- custody event `RETAIN_TOOL`, no `A4_CUSTODY_HELD`;
- C request and `REQUEST_UNMET` withdrawal;
- B tool-take, market commission, and tool-return events;
- B cash `58`, completed units `5`;
- A material `1`, completed units `5`, tool returned;
- A's blocked repair and later successful repair;
- A5 tool answer `OK`, B market answer `UNKNOWN`;
- read-only flag true and canonical digest stable.

### B activity severed

`include_b_activity=False` removes B's return/take/commission/return events and
their state effects at scenario construction. The same `run_a5_assertion` then
fails with:

```text
A4_B_INDEPENDENT_ACTIVITY_MISSING
```

The exact intact `c12.sqlite` is copied over the fault root. The same assertion
returns `PASS`. This is the claim-specific restore-green comparison.

### A access removed

`grant_a_access=False` omits A's perception of B's tool-taking event. A5:

```text
tool answer: UNKNOWN: A has no perceived event of who moved the workshop tool.
```

The same consumer assertion fails with `A5_A_TOOL_ACCESS_MISSING`; A cannot
report or remember the unaccessed transfer.

### Actor or branch identity swapped

- `EncounterReader(root, actor_id="B")` -> `ENCOUNTER_ACTOR_SWAP_REFUSED`.
- `EncounterReader(root, branch_id="not-a-branch")` -> `ENCOUNTER_BRANCH_REFUSED`.
- No state is written before either refusal.

### Renderer-only change

`render_encounter(view, "plain")` and `render_encounter(view, "compact")` produce
different text, while:

- canonical digest before/after is identical;
- view digest is identical;
- SQLite `total_changes` is unchanged;
- no event, perception, checkpoint or actor state is written.

### Missing custody rule

`custody_rule=False` records:

```text
A4_CUSTODY_HELD: state=HELD, code=MISSING_CUSTODY_RULE
```

No `RETAIN_TOOL` decision event is emitted. The assertion reports
`A4_CUSTODY_DECISION_MISSING`; it does not invent a decision.

### Single-context evidence

`context_profile="single_context"` records inspections in one context only.
The disposition is `INSUFFICIENT`; `A4_CUSTODY_HELD` is emitted; the assertion
reports `A3_CONTEXT_EVIDENCE_INSUFFICIENT`.

### Fork after acquired activity

After the intact history exists, the test forks `alt`, inspects, and speaks in
the child. The parent A5 assertion remains `PASS`; the child digest differs;
both guarded branches verify; the parent is not rewritten.

### Cold process CLI

```sh
python3 run_cp_a5.py --root <ROOT> scenario
python3 run_cp_a5.py --root <ROOT> encounter \
  "What happened to the workshop tool?"
python3 run_cp_a5.py --root <ROOT> assert
```

Each command is a separate Python process. The test checks the C12 file SHA-256
is unchanged across `encounter` and `assert`, verifies `read_only: true`, and
gets `PASS` from the assertion. The mix of `OK` for A's tool perception and
`UNKNOWN` for B's unperceived market commission is preserved.

## 4. Actual A5 output trace

`01_ACTUAL_A3_A5_LIFE_AND_ENCOUNTER_TRACE.json` contains the actual generated
scenario, encounter answers, assertion receipt, and cold verification. The
representative answers are:

```text
What happened to the workshop tool?
OK: A perceived B take the workshop tool, could not repair while it was away,
and perceived its return.

What did B do at the market?
UNKNOWN: A did not perceive B's market commission.
```

The same trace records the read-only C12 SHA-256 equality:
`0a6b71b68bef2285d72d0f8c490938436a7ce7db4b70bac31765a3694492750f`.

## 5. I1 zero-stock ambiguity

I1's existing offscreen event records `material_delta: -1` while stock is `0`;
that test remains unchanged. CP-A5 does not cite that event as new physical
consumption. The new B market commission records `material_delta: 0` and
depends on the actual workshop `tool_available` resource. No old assertion was
silently rewritten.

## 6. Not run

- Native C9/C12 anchor verification: no owner custodian.
- Durable C9 actor readset / C9 R3B integration: outside this return and held.
- Native CAN/ADP/SCI05 or Pyat N11/N12 issuance: no source grant.
- Original B/M35 producer and F1CR patched executable: not present/claimed.
