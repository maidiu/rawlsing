# Real validator, Git refresh and adversarial receipts

## 1. Environment and isolation

```text
Host: mainMac.lan
OS: macOS 13.2.1 (22D68), x86_64
CPU: Intel(R) Core(TM) i9-9880H CPU @ 2.30GHz
Account: matthewsmith
Python: 3.11.3
Git: 2.43.0
pytest: 9.0.2
OpenCode: 1.18.34
Model: opencode-go/deepseek-v4.1-flash
Variant: max
Agent: build
Session: ses_e6c922f35ffet6XtlGF0v43LIw
Review base: 06f40a3eabb4acfc57f433144224695c2427c25f
Remote commission tip incorporated by fast-forward: e17ce303652efe8e4628f42387ab9d9a80c71c28
R3 base: 96af4f15c993c7a4f32da4cc31ef3175903a0d5c
Immutable subject: e50d32eb6816578145d17dcd637a0b90b3a1ef40
```

The candidate was copied to a temporary S2 root with the same relative
`SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1`
layout. A fresh temporary Git repository was initialized there and its
`.git/objects/info/alternates` was pointed at the real repository object
database, so `verify_source_manifest.py` and the refresh test resolved exact
Git objects without touching the active worktree or any other worktree.

The candidate files in the active worktree were not edited. SHA256 of every
candidate file before and after the full test run was identical.

The R3 receipt reports `oldMac`, Python 3.11.3, pytest 9.1.1. This independent
run is on `mainMac`, Python 3.11.3, pytest 9.0.2. The runtime differs; the
candidate still passes. `PYTHONDONTWRITEBYTECODE=1` and
`-p no:cacheprovider` were used.

## 2. Intact candidate

### 2.1 Offline validator

```sh
PYTHONDONTWRITEBYTECODE=1 python3 validate_index.py --output /tmp/sorok_r3ir_validation.json
```

Exit `0`, result `PASS`, 17 checks:

```text
sorok_rows=144
pyat_rows=23
pyat_f_gates=8
four_assets=4
l3_nodes=80
edges=461
traversals=3
owner_slots=46
priority_decisions_made=0
typed_index_cycles=66
source_manifest_sha256=b3d359f1bfe97a23b2c3fb356fde84c452ffe38ca874facbec7d5df086fdfa5c
registry_sha256=be9fcf6492c77b6fbe34260d7fac20c7e13d795a5934655f70d560bc2f083a17
orchestration_sha256=946b978d12656e40a76d8428fbf89d4dc524cdb1f1990f7496917fd7a6c38200
```

### 2.2 Git refresh verifier

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_source_manifest.py
```

Exit `0`:

```json
{
  "errors": [],
  "manifest_digest": "ec223ad4b65650be556e0f28c05bf94936635baa7efb3c39d4efabfb5fa3d028",
  "references": 3,
  "result": "PASS",
  "rows": 167,
  "schema": "SOROK_OINDEX_SOURCE_MANIFEST_REFRESH@1"
}
```

The verifier resolves every `commit:path`, checks `git cat-file -t`,
`git rev-parse`, `git show -s --format=%cI`, and for the one tree row checks
`git ls-tree -r --name-only` against `tree_files`. The independent reviewer
also recomputed all 170 object identities/timestamps directly, not merely by
trusting this script: zero errors. The manifest has 166 blobs + 1 tree, 21
distinct source commits, 167 rows and 3 reference sources.

### 2.3 Test suites

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -o addopts='' -q -p no:cacheprovider test_validate_index.py
# .....................
# 21 passed, 4 subtests passed in 8.54s

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_validate_index.py
# Ran 21 tests in 8.246s — OK
```

Both commands exited `0`. The 21 tests include the intact candidate, the
source manifest digest, forged non-S source path/blob/consumer, forged
timestamp/metadata, forged Pyat source, damaged B1/B3A/B3AS/S39_S52 lineage,
R15 tree-as-blob, ACTUAL consumer without evidence, missing product link,
generic-governance-only product path, missing owner/native/N11 collision,
dropped S16, original workstream source removal/wrong blob, native promotion,
orphan L3, missing Pyat N11, untyped cycle, priority decision, and refresh
verifier forged manifest blob.

These tests pass for the returned artifact. They do not include the
acceptance-grade consumer-provenance negatives below.

## 3. Required adversarial faults

Each mutation was applied to a fresh temporary copy. `joint` means registry
and `source_manifest.json` were both changed and `manifest_digest` was
recomputed. "Validator" is `validate_index.py`; "Verifier" is
`verify_source_manifest.py`.

| # | Fault | Digest reissued | Validator | Verifier | Exact reason / verdict |
|---:|---|---|---|---|---|
| 1a | A5 forged source path/blob/consumer, registry only | no | FAIL | PASS | `A5: path manifest mismatch`; caught by registry/manifest consistency |
| 1b | A5 forged source/consumer, joint | yes | PASS | FAIL | `SOROK:A5:git_object_missing` for `FORGED/NOT_A_SOURCE.py`; caught by Git |
| 2a | fake source timestamp, registry only | no | FAIL | PASS | `A5: source_timestamp manifest mismatch` |
| 2b | fake timestamp joint + metadata + digest | yes | FAIL | FAIL | `C0: source metadata timestamp manifest mismatch`; verifier `SOROK:A5:timestamp:2026-10-30T20:05:55-04:00!=1999-01-01T00:00:00+00:00`; caught by Git |
| 3 | wrong Pyat N11 source, registry only | no | FAIL | PASS | `PYAT_N11: path manifest mismatch` |
| 3b | wrong Pyat N11 source, joint | yes | PASS | FAIL | `PYAT:PYAT_N11:git_object_missing` for `FORGED/PYAT.py` |
| 4 | R15 tree falsely as blob, registry only | no | FAIL | PASS | `R15_V2: object_type manifest mismatch` |
| 4b | R15 tree falsely as blob, joint | yes | PASS | FAIL | `SOROK:R15_V2:object_type:tree!=blob` and object-id mismatch |
| 5 | B3A source path removed, registry only | no | FAIL | PASS | `B3A: source path` |
| 5 | B3AS source path removed, registry only | no | FAIL | PASS | `B3AS: source path` |
| 5 | S39_S52 source path removed, registry only | no | FAIL | PASS | `S39_S52: source path` |
| 6 | S0 registry row missing | no | FAIL | PASS | `expected 144 Sorok rows, got 143` |
| 7 | S16 program-map blob forged, registry only | no | FAIL | PASS | `S16: exact program-map blob` |
| 8 | fabricated `ACTUAL` consumer provenance, joint; source object unchanged | yes | **PASS** | **PASS** | **Required negative not caught**: fake consumer evidence and a changed 135/0 consumer count are accepted |
| 8b | `ACTUAL` consumer with a real but unrelated B1 Git object, joint | yes | **PASS** | **PASS** | **Required negative not caught**: resolvable but unrelated consumer evidence is accepted |
| 9 | R15 `tree_files` list mutated, manifest + digest | yes | PASS | FAIL | `SOROK:R15_V2:tree_files`; Git refresh catches what offline validation cannot see |
| 10 | `source_kind` forged jointly + digest | yes | **PASS** | **PASS** | **Source-type acceptance gap**: `source_kind` is consistency-checked, not Git-derived |
| 11 | required/current consumer claim forged jointly + digest | yes | **PASS** | **PASS** | **Consumer acceptance gap**: `required_consumer`/`first_consumer` are not externally anchored |
| 12 | different REAL Git blob substituted as A5 source, joint | yes | **PASS** | **PASS** | **Provenance limit**: object existence is proven, historical/owner authenticity is not |

### 3.1 Exact failing negative: accepted ACTUAL consumer

Base state: 135 `NONE_PROVEN_AT_PREMAIN` (112 Sorok + 23 Pyat), 0 `ACTUAL`.
The mutation set A5 to:

```json
{
  "actual_consumer_state": "ACTUAL",
  "actual_consumer_evidence": {
    "commit": "5fc1d43e3d5412194d1f1eaa30ff448f84635e99",
    "path": "FORGED/FAKE_CONSUMER.py",
    "object_type": "blob",
    "object_id": "3333333333333333333333333333333333333333"
  }
}
```

in both the registry row and the manifest row, then recomputed
`manifest_digest`. `validate_index.py` returned `PASS`; `verify_source_manifest.py`
returned `PASS` with `errors: []`. The same result occurred with a real,
resolvable but unrelated B1 blob
`c0f4588c158b40c8903b4aae2f292eae5238b8a0:WORKER_RETURNS/SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1/bfirst.py`
blob `94ffc52847e4c8ae760212d1bc8543594ba793fa`.

This does not satisfy the commission's "acceptance-grade check of first ACTUAL
consumer provenance" or the R2-IR requirement to "require evidence for the
actual `first_consumer`/edge." The R3 receipt's mutation #9 ("fabricated
ACTUAL consumer with no callable/source evidence") is not the same test: it
only removes or mismatches fields. A complete fabricated provenance object
passes.

### 3.2 Reissued digest and provenance

- A manifest-only change with a recomputed digest is caught by registry/manifest
  mismatch, because `validate_index.py` compares the two artifacts field by
  field.
- A joint change to a nonexistent source object is caught by Git object
  resolution (`git_object_missing`).
- A joint change to a different real source object is not caught. The manifest
  is a self-digested claim about which object is the source; it is not an
  owner-signed source list. This is an authenticity limit, not an object-
  identity failure. If the commission requires provenance substitution to fail,
  an external source-owner anchor is required.

## 4. Restore and GREEN

After all temporary mutations, a fresh copy of the untouched candidate was
re-executed:

```text
validate_index.py: PASS
verify_source_manifest.py: PASS, errors=[]
sorok_rows=144, pyat_rows=23, four_assets=4, l3_nodes=80,
edges=461, owner_slots=46, priority_decisions_made=0, typed_index_cycles=66
```

The active candidate files were byte-identical before and after the test run.
No mutation was applied to the active worktree.

## 5. What these receipts prove and do not prove

Proved at this execution scope:

- Exact Git object/type/id/timestamp identity for 167 manifest rows + 3
  references, including the R15 tree file list.
- The corrected source paths/blobs/tree are real in the exact historical cuts.
- The 21-test + 4-subtest suite passes under the selected harness.
- The source-object and tree-file faults fail for the claimed Git reasons.
- The offline validator + Git verifier separation catches absent/forged source
  objects after a digest regen.

Not proved:

- Git-resolved actual-consumer provenance.
- External source-owner authenticity against a different real object.
- Native product, scientific issuance, human A5, Pyat N11/N12, C9/C12 release,
  owner adoption or priority.
