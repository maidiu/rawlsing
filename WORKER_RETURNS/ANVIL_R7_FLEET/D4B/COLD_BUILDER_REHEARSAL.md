# COLD_BUILDER_REHEARSAL

Cold root: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/d4b_cold.dBvTF9/INSTRUMENT`
(a fresh `cp -R` of the private package; no author worktree, no hidden fixture).
Receipt: `COLD_RUN.log` (SHA-256 `63ed1a7aa2ebda245939b7899a3d531b4a618661b49cae99252efe57591b78d8`).

## 1. Current consumer — the R7 decision gate

**Declared ABI** (`29_R7_INTEGRATED_MISSION_AND_GATES.md`):

```
python3 tools/r7_integrated.py FRAME FRAME.json --evidence-root EVIDENCE/ --source-root EXACT_PINNED_SOURCE_SNAPSHOT/
python3 tools/r7_integrated.py DECISION DECISION.json --evidence-root EVIDENCE/ --source-root ...
python3 tools/r7_integrated.py C_INTEGRATED C.json --evidence-root EVIDENCE/ --source-root ...
```

**First fail (executed):** the package contains no `FRAME.json`, `DECISION.json`
or `C.json`, and no builder card or README supplies one. Running the documented
command in the cold copy returns:

```
status: RED
UNHANDLED_MALFORMED_PACKET:FileNotFoundError(2, 'No such file or directory')
FRAME_EXIT=2
DECISION_EXIT=2
```

So the current consumer cannot be instantiated from the package's own source
pins. `test_r7_integrated.py` constructs fixtures in Python memory instead;
that is an author test, not a builder handoff.

**Author suite in the cold copy:** `TEST_EXIT=0`.
**Quality runner in the cold copy:** `PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY`,
12/12 exit 0, scope string `NO_NATIVE_ORIGINAL_SOURCE_100K_FULL_PHYSICAL_RUN__NO_INDEPENDENT_C__NO_PROTECTED_H1`.
Copy digest changed (`SHA_BEFORE=4e951afe...` → `SHA_AFTER=20248608...`)
because `run_r7_quality.py` writes `tests/R7_QUALITY_REPORT.json` into the copy.
That is expected and is itself an observation: the runner is not read-only.

## 2. Owner-held future consumer — T7 / SOROK

**Required ABI** (`02_BOUNDARY_CONTRACTS.json` T7): producer = SOROK committed
activity plus a separately authorized shared-world effect; receiver = SOROK
subsequent world/actor; must preserve event clock, causal dependencies,
shared-world consequences, committed past, branch replay, and no retroactive
mutation of real survey observations; first effect = an eligible performed
action changes a later actor's opportunity while the alternative branch and the
original survey stay unchanged.

**Rights:** SOROK actor/consent/development owner; no actor grant exists in this
work or in the supplied packet. `T7.time_class = MUST_ALLOW_FUTURE_AND_OWNER_HELD`.

**First fail:** the supplied C packet can admit a design with the future card in
`EXACT_BUILDER_HOLD`; there is no executable actor/world ABI, no admitted event
record, no access witness and no owner receipt. My base packet therefore emits
`OWNER_HELD_FUTURE` for T7 and never claims an executed actor effect. Any card
that upgraded it to `EXECUTED_FIRST_READER_PROOF` would be a false authority
claim; the strict overlay rejects a bare-filename or non-existent runner, but no
local check can mint the SOROK grant.

## 3. Result

| Consumer | Instantiable from source pins? | Actually executed | Grade |
|---|---|---|---|
| R7 FRAME/DECISION/C | **No** (no packet files) | author synthetic suite only | `EXACT_BUILDER_HOLD` |
| T7/SOROK future | No (owner-held, no ABI/rights) | none | `EXACT_BUILDER_HOLD` |

No local H1, no independent C, no science/source/actor receiving is claimed.
