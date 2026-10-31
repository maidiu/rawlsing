# PYAT S7-FIX-I3 — independent hostile function-identity and source-relation consumer court

**Role:** fresh independent I3 hostile Python AST, sealed-owner security and
current-consumer reviewer. Not S6/S7/S7-FIX author, F7/P07 implementer, PRE-MAIN
integrator or own reviewer.

**Repository:** `maidiu/rawlsing` (private).

**Branch:** `review/pyat-s7fix-boundary-source-abi-hostile-20261031-r1`.

**Startup:** `d0342290b257f85c3e8931f9962e0aecabc84ed3`.

**Current PRE-MAIN recheck:** `8e44ca9c751049d65e6def47600b5c073ee04b29`.
The `rawlsing_next` tree is identical at both cuts:
`1d88d3fbb1d18dadfda946d9cd7f309d84afa479`.

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s7fix-i3-hostile-20261031-r1`.

**Fresh session:** OpenCode CLI, agent `build`, model
`opencode-go/deepseek-v4.1-flash`, variant `max`; `OPENCODE_PID=21995`;
`TERM_SESSION_ID=D259FC1D-3D1A-43E0-83F2-9AAE934EAF86`; isolated worktree; no
active S7-FIX worktree displaced. Sourcefree tests only.

**Write scope:** only
`PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7FIX_I3_HOSTILE/`.
No production source, PRE-MAIN, merge or self-adoption.

## Source cuts

| Artifact | Exact cut |
|---|---|
| S6 | `2c5cf86beb12b7dbeda5532614784737ad30d89d` |
| S7 | `026ca72c24d564d4dc203f68385df8c75b4bd3a7` |
| S7-FIX | `80bc5d9bf6624c2ea04027322947a41c347330aa` |
| Current source relations | `5b67e3f98a5faf95a6c82700af2346fef6e306a5` |
| Current physical decoder | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` |
| `pre553_temporal_comparability.py` | **ABSENT** |

## FINDING

### Historical six boundary repairs — PASS

The six historical defects are real and the S7-FIX correction is structurally
sound:

- five old S6 groups are **split** into outer `SourceRelationResolver` and nested
  `_make_sealed_source_relation_owner.SourceRelationResolver` families;
- one old S6 split is **joined** into
  `PhysicalSourceIncidence.iter_batches.emit`;
- 11 corrected families, 18 member rows, 1,881 old groups -> **1,885** corrected
  families; 3,135 exact-once function IDs; 845 branches.

Independent exact-AST results:

- outer `00f50ea5...` methods: **5/5** expected AST hashes;
- nested `d9fb2c48...` methods: **5/5** expected AST hashes;
- nested `__init__` variant `8053d30d...`: **1/1** `733bdba8...`, correctly same
  nested family;
- four historical decoder variants: **4/4** `4f7cd7cc...` for
  `PhysicalSourceIncidence.iter_batches.emit`;
- validator baseline: **PASS**, 11 checks; self-test: **PASS**, 8/8 mutations
  detected.

Introduced/lineage facts verified: outer blob `61acee605...`; nested blob
`d5e6d6ba...`; nested variant `c86ae335...`; outer qualname lineage
`ce4edcc8...`; nested qualname lineage `fbb735f6...`; join origin
`42ddc284...`/`901e3e77...`.

### Original negative custody — PASS at artifact scope

The nested F7/P07 adverse findings remain under the nested families:

- `_validate_positive`, `decide`, `resolve_exact`:
  `PROVEN_DEFECTIVE_AT_DECLARED_SCOPE`;
- nested `__init__`: review/revise;
- nested `require`: positive-author-only;
- outer S5 rows: contextual-only, not outer defects.

The validator preserves 2,595 negative records (digest
`93cdb8e28653e42aebc7fe2b2c511333e85320eecee2710a37fe833fb80122f7`).
HQ240/HQ245–HQ248/F7/P07 findings are preserved as historical evidence. No
native C was compiled or executed; no original survey corpus was read.

### Current ownership — RED

The current-ownership mapping still conflates outer/nested history:

- Every nested member's `current_implementation_candidate` points at current
  outer `SourceRelationResolver.<method>`, while the current source has **no**
  nested `_make_sealed_source_relation_owner` owner.
- S5 outer rows claim `EXACT_AST_SAME_PATH`, but all five current outer method
  ASTs differ from the historical S4 outer ASTs:
  - `__init__`: `e1fcc98f...` vs `828fbc7f...`
  - `require`: `47a40b20...` vs `1d789a2f...`
  - `_validate_positive`: `20385e92...` vs `52bf4943...`
  - `decide`: `90243295...` vs `8dd873c4...`
  - `resolve_exact`: `5c1d7f0b...` vs `7473e1e9...`
- Current `emit` AST is `77d9be6c...`; historical join AST is `4f7cd7cc...`.
  The join is historical AST identity, not current PR526 behavioral equivalence.
- Source-relations first-consumer evidence names
  `pre553_temporal_comparability.py`, which is absent. The current source
  relations consumer is test-only, plus a string map at
  `fiabc_succession_producer.py:59`.

### Current consumers and tests

- `pre553_source_relations.py`: **no production import**; only
  `rawlsing_next/tests/test_pre553_source_relations.py:13`. This is not a
  production first consumer.
- `pre553_physical_decoder.py`: production static imports exist in
  `pre553_source_native_preimage_adapter.py`, `pre553_source_backed_c11_facade.py`,
  `pre553_route_b_production.py`, `pre553_physical_c11_bridge.py` and others.
  Current execution path:
  `materialize_native_preimages -> iter_cells -> iter_batches -> emit`.
- Current sourcefree test receipts:
  - `test_pre553_source_relations.py`: **24 passed**
  - `test_universal_source_byte_custody.py`: **26 passed**
  - `test_universal_source_projection.py`: **31 passed**
  - `test_pre553_sr06_decoder_carrier.py`: **16 passed, 1 skipped**
- Current PR526 custody is genuine at test scope: private read-only `_SourceSnapshot`,
  `/dev/fd` reader, stable/rewind/hash checks, unlink/close. It is still a
  different implementation from the four historical `emit` variants.

## Actual commands and exits

Run from the review worktree with
`PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0` and
`pytest -q -p no:cacheprovider`:

```text
test_pre553_source_relations.py ........ 24 passed, exit 0
test_universal_source_byte_custody.py .. 26 passed, exit 0
test_universal_source_projection.py .... 31 passed, exit 0
test_pre553_sr06_decoder_carrier.py .... 16 passed, 1 skipped, exit 0
```

Validator, executed from a temp copy with `--dir` pointing at the existing S7-FIX
artifact directory (no 47 MB duplicate):

```text
validator.py --json      PASS, 11 checks, 3135 IDs, 1881 old groups, 1885 families, 845 branches
validator.py --self-test PASS, 8/8 mutations detected
```

Independent AST check, exact Git blobs:

```text
outer historical: 5/5
nested historical: 5/5
nested init variant: 1/1
historical emit variants: 4/4 same AST
current outer: 0/5 historical AST matches
current nested: absent
current emit: present but different AST
```

Full machine detail is in `SIX_BOUNDARY_SOURCE_AND_ABI_COURT.json`; source-level
provenance is in `ORIGINAL_OWNER_AND_NEGATIVE_PROVENANCE.md`; current call/test
evidence is in `CURRENT_CALL_CONSUMER_AND_FAULT_TESTS.md`.

## Split verdicts

**ENGINEERING:** `RED_ON_CURRENT_OWNER_MAPPING__PASS_ON_SIX_HISTORICAL_BOUNDARIES_AND_NEGATIVE_CUSTODY__CURRENT_ABI_HOLD`.

The six historical boundary repairs and negative custody pass. The current
ownership mapping is red because nested historical members are still candidate-
mapped to the outer current class and S5 outer `EXACT_AST_SAME_PATH` is false.
Current sourcefree tests pass at test scope but no production consumer or
behavioral equivalence is proven.

**SCIENTIFIC:** `ACCEPT_SCOPED_PRESERVATION__HOLD_ISSUANCE__STATIC_IDENTITY_NOT_SCIENCE`.

The original methodological limits and F7/P07/HQ240/HQ245–HQ248 adverse findings
remain under their actual owners. No source/scientific issuance is available or
claimed.

**AUTHORITY:** `ACCEPT_SCOPED_SOURCEFREE_REVIEW__HOLD_SOURCE_ACTOR_WORLD_ADOPTION__NO_MERGE`.

No source/native read, world/N9/N10W, actor, N11/N12, model use, production
adoption or self-review is granted. The 47 MB S7-FIX artifact remains on its own
branch and was not duplicated.

## DONE / REMAINING / BLOCKERS / NEXT

**DONE:** exact original AST identities for outer/nested methods and join;
introducing-commit/source-blob lineage; outer/nested qualname distinction;
negative custody check; current import/call map; current PR526 tests; current
sourcefree tests; source-level counterexamples; six deliverables.

**REMAINING:** correct current ownership mapping (nested -> historical-only; outer
-> path-only/different AST; source-relations first consumer -> current test-only);
owner decision on whether to implement a real current nested owner or retire it;
route F7/P07/native findings; independent HQ intake.

**BLOCKERS:** no current source-relations production consumer; no current nested
sealed owner; current outer AST differs from historical; current emit differs;
no original source/actor/science authority; no production merge.

**LARGEST MOVE:** correct the current ownership fields and treat the historical
six repairs as identity/custody evidence only; keep current PR526 decoder tests
and current test-only source-relations suite; do not transplant the old nested
owner or 47 MB artifact.

**FLIGHT:** `SIX_HISTORICAL_BOUNDARIES_PASS + NEGATIVE_CUSTODY_PASS + CURRENT_OWNER_MAPPING_RED + CURRENT_ABI_HOLD + SCIENCE_AUTHORITY_HOLD + NO_MERGE`.

**DELTA:** `+` exact outer/nested/join ASTs and lineages; `+` validator pass and
negative custody; `+` current sourcefree tests; `+` current PR526 test evidence;
`+` concrete current ownership conflation/false exact-AST findings; `−` no
current source-relations production consumer; `−` no current nested owner; `−`
no behavioral equivalence; `−` no source/science/actor adoption.

## Return artifacts

- `00_RETURN.md`
- `SIX_BOUNDARY_SOURCE_AND_ABI_COURT.json`
- `ORIGINAL_OWNER_AND_NEGATIVE_PROVENANCE.md`
- `CURRENT_CALL_CONSUMER_AND_FAULT_TESTS.md`
- `NONADOPTION_AND_SCIENCE_AUTHORITY.md`
- `COMPACT_INTEGRATION_RECOMMENDATION.md`

Exact pushed remote SHA is reported in the completion message and is not
self-referenced inside its own commit.

TERMINAL: `SIX_HISTORICAL_BOUNDARIES_PASS__NEGATIVE_CUSTODY_PASS__CURRENT_OWNER_CONFLATION_RED__CURRENT_ABI_HOLD__SCIENCE_AUTHORITY_HOLD__NO_MERGE`.
