# A — universal35 source-pack current port — ordinary return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-A-20261106-R1`
**Branch:** `codex/pyat-universal35-a-20261106-r1`
**Start:** `d119045f4169439b4ba02d0870bc328f8beb3aaa`
**Pinned source pack:** `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`
**P6 review:** `d81bc2c67baf933461ae6cfca468f24779cc7e44`
**Status:** `AUTHOR_TESTED__INDEPENDENT_REVIEW_REQUESTED__NO_PROTECTED_MERGE`
**Implementation/evidence SHA:** reported by terminal push readback; a file cannot contain the SHA of its own commit.

## What is delivered

- Selective current port of the missing generic R157 source-configuration layer:
  `SourceConfigLibrary`, closed schema/validator, factory, fixture loader, reader
  transport, CLI, evidence accessors, and `pre553_source_read_admission.py`.
- No source-specific engine branches, no 35 loaders, no second compiler, no
  compiler/issued_workload/query/FF edits, no raw original source bytes in Git.
- Large R157 configuration/fixture blobs remain in their immutable Git objects and
  are read through `rawlsing_next/source_configuration/provider.py`. No duplicate
  huge fixtures or carriers were committed.
- Public source selector with a separate effective source-root override.
- Frozen ABI for B/D: `rawlsing_next/source_configuration/ABI.json`.

## Frozen ABI and first consumer

`ABI.json` publishes the exact signatures. The first consumer is:

`SourceConfigLibrary.build_fixture_release`
→ `factory.build_validated_c11_release_from_config`
→ `rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream`
→ `C11LogicalRelease`.

Source-pack input is a validated `PYAT_R157_SOURCE_CONFIGURATION@1.0.0` document
plus a permitted `ExactPhysicalCellStream` or `PhysicalSourceIncidence`; output is
the existing `GovernedC11Projection` / `C11LogicalRelease` / source-backed
repository. B can build its operation adapter against `SourceConfigLibrary.select`,
`build_governed_c11_projection`, `build_validated_c11_release_from_config` and
`row_native_keys_from_transport` without editing A files.

## 35/35 coverage and proof

| Check | Result |
|---|---|
| Index / discovery | 35 available, 0 pending; 18,276 original items, 18,413 physical slots, 18,250 exact joins, 26 unmatched |
| Status | `{'available': 35, 'available_original_items': 18276, 'available_physical_slots': 18413, 'other_incomplete': 0, 'pending': 0}` |
| Validate | 35/35 passed, 0 failures, 47.03s |
| Real C11 fixture calls | 35/35 release receipts matched the recorded native fixture receipt, 0 failures, 117.76s |
| Targeted tests | 38 passed in 77.64s |

Evidence: `evidence_all35_index.json`, `evidence_all35_status.json`,
`evidence_all35_validate.json`, `evidence_all35_fixture_calls.json`,
`evidence_pytest.txt`.

These are nonrespondent fixture/regression-floor calls. They are **not** original
respondent execution, C11 native acceptance, or scientific issuance.

## Effective source-root override

`SourceConfigLibrary.select` / `resolve_source_path` / `original_plan` and
`reader.decode_config_with_source_read_permission` accept an explicit
`source_root` distinct from the repository artifact root. Resolution changes with
the override; no file is opened. `source_locator_bindings.json` contains only
relative source locators for SRC01–SRC35, never a personal absolute path. The
caller supplies the effective root at runtime.

Evidence: `evidence_source_root_override.json`, `evidence_source_specific_exceptions.json`.

## 119 R157 path fate

`R157_119_PATH_FATE.json` maps all 119 historical paths (118 source-configuration
paths + the admission module; 19 code paths):

- `PORTED_EXACT`: 16
- `PORTED_ADAPTED_CURRENT_ABI`: 7
- `PINNED_R157_OBJECT_PROVIDER`: 88
- `HOLD_SOURCE_SPECIFIC_BUILDER_NOT_RUNTIME`: 2
- `HOLD_BUILD_TOOL_NOT_RUNTIME`: 6

No path is silently dropped. The 88 pinned paths are large configs/fixtures read
from immutable R157 Git objects, not copied into this branch.

## Source-specific facts preserved

`SOURCE_PACK_35_ROWS.json` records the 35 rows, counts, held summaries, exception
paths/hashes and relative source locators. `evidence_source_specific_exceptions.json`
records representative preserved facts: SRC25/26 exact item/name differences and
one-to-many physical slots (SRC26 195 items / 332 slots), LiTS SRC27 household
subject unit and repeated `q101_1` field, and SRC13’s exact source-bound Latin-1
reader configuration. No default source absence shortcut was introduced.

## Negative and fault evidence

- Wrong source SHA → `SourceArtifactError: SHA mismatch`.
- Nonexistent pinned object → `ProviderError`; unknown source → `SourceNotPrepared`.
- Non-exact serialized path → `SourceArtifactError: non-exact path component`.
- Occurrence/wrong physical slot and empty occurrence → schema refusal.
- Source-read permission refusal before decode → zero decoder/source-open calls
  (inherited `test_pre553_source_read_admission.py`).
- No source-root override → typed `NO_SOURCE_ROOT_OVERRIDE`; explicit override
  resolves under the caller root; artifact root remains unchanged.
- Restore/positive: valid fixture call after wrong-SHA refusal still matches the
  recorded release receipt.

## FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| R157 generic code/resources were absent at current protected cut. | The missing layer is a data-driven configuration/factory/reader surface, not a new engine. | Ported generic code; pinned large resources by immutable Git object; no per-source loaders. | HQ review / later independent reviewer |
| 35/35 registry and fixture floor pass. | Structural regression floor only; original source execution remains separate. | Preserved 18,276/18,413/18,250/26 and exact fixture receipts. | Pyat HQ / D integrator |
| Source-root override was not previously explicit. | Artifact root and original-source root are different custody concepts. | Added selector/resolver/plan/decode override with relative locator bindings. | A implementation; HQ review |
| B/D need a stable ABI. | Operation adapter must consume the same frozen source-pack surface. | Published `ABI.json` and first-consumer chain. | B and D owners |

## PROGRAMMA_DELTA

- **Identity:** `PYAT_R157_SOURCE_CONFIGURATION@1.0.0` + `PYAT_R157_SOURCE_PACK_ABI@1.0.0`.
- **Function:** select source pack → validate config → project governed C11 → validated C11 release/repository.
- **Input → typed output:** validated `SourceConfig` + permitted physical transport → `GovernedC11Projection` / `C11LogicalRelease`.
- **Root:** artifact root = pinned R157 Git objects; effective source root = caller override, separate.
- **Schema:** frozen R157 schema retained; current owner mapping SHA updated to the actual current facade.
- **Clock:** no clock or replay payload mutation.
- **Permission:** metadata/plan only; no original source bytes opened; no native grant.
- **Actual first consumer:** `SourceConfigLibrary.build_fixture_release` → existing C11 facade.
- **Evidence:** `evidence_all35_*`, `R157_119_PATH_FATE.json`, `SOURCE_PACK_35_ROWS.json`, `evidence_source_root_override.json`.
- **Affected existing IDs:** SRC01–SRC35; no compiler/query/FF shared-module edits.
- **Conditional unlocks:** B can build the operation adapter; D can integrate after B/A frozen ABI.
- **Next action:** independent nonauthor review of this exact head; then B/D integration.

## Verdicts

**ENGINEERING — author-tested; independent acceptance not issued.**
The named producer→first-consumer chain and 35/35 fixture/validate/index terminal
checks pass at the tested head. This is author evidence only; HQ plus a later
distinct nonauthor reviewer owns acceptance.

**SCIENTIFIC — no new issuance.**
R157 source-specific semantics/risk/response/RAW distinctions are preserved as
configuration facts. No population, structural, native, or human claim is made.
SRC13/SRC14 Latin-1 configurations remain exact source-bound compatibility facts,
not general encoding authority.

**AUTHORITY — isolated lease only; no protected merge.**
All35 physical custody is externally observed under the caller root; A did not
open original respondent bytes. No source leak, global settings change, self-review,
native grant, or protected mutation occurred.

## Remaining finite dependencies

1. B operation adapter consuming `ABI.json`.
2. D original-source execution under separately authorized source root; actual
   original decode/native facts remain NOT_RUN here.
3. Independent nonauthor review of this exact branch head.
4. Protected receiving/merge by the authorized integrator.
5. Source-specific held/residual semantics remain at their exact R157 spans; no
   blanket source absence or global stop.
