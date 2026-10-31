# Source-exact validator and mutation receipts

## 1. Environment and source cut

```text
Device: oldMac
OS: macOS 13.7.8 x86_64
Python: 3.11.3
pytest: 9.1.1
Candidate base: 96af4f15c993c7a4f32da4cc31ef3175903a0d5c
Repair commission head: 024f3b09b17ca5769c0bdee8d5eec459e31bb247
Build PRE-MAIN: 5fc1d43e3d5412194d1f1eaa30ff448f84635e99
Last-verified PRE-MAIN: 87755f02ec5c37499b09e80db6fbdcc9316a6b15
Refreshed PRE-MAIN: d0342290b257f85c3e8931f9962e0aecabc84ed3
```

All commands ran in the candidate directory with `PYTHONDONTWRITEBYTECODE=1`.
The repaired candidate is under
`SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1`.

## 2. Frozen source manifest

`source_manifest.json` contains:

```text
167 source rows = 144 Sorok + 23 Pyat
3 reference sources = current Program Map, earlier Program Map, HQ synthesis
166 blob objects + 1 tree object
manifest_digest = ec223ad4b65650be556e0f28c05bf94936635baa7efb3c39d4efabfb5fa3d028
```

Source kinds: 112 definition/evidence JSON, 23 definition documents, 17
documentary S definitions, 9 executable source files, 4 returned-return
evidence files, 1 evidence document, 1 source tree.

Actual consumer states are typed, not conflated:

```text
NONE_PROVEN_AT_PREMAIN              135
NOT_A_RUNTIME_MODULE                 17
HISTORICAL_OR_AUTHOR_TESTED_ONLY      8
AUTHOR_TESTED_ONLY                     4
HISTORICAL_SOURCE_ONLY                 3
```

The manifest is frozen and digest-bound. Offline validation checks
registry/manifest consistency. The separate `verify_source_manifest.py` command
resolves every row against real Git; an unchecked manifest is not proof.

## 3. Intact validator run

```sh
python3 validate_index.py --output /tmp/oindex-r3-validation.json
```

Exit `0`, result `PASS`:

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
```

## 4. Actual test suite

```sh
python3 -m pytest -o addopts='' -q test_validate_index.py
# 21 passed, 4 subtests passed

python3 -m unittest -v test_validate_index.py
# Ran 21 tests in 9.196s — OK
```

The old 9-test suite and old `VALIDATION_RESULTS.json` /
`VALIDATOR_TEST_RESULTS.txt` are superseded. They are not cited as proof of the
repaired candidate.

## 5. Git refresh verifier

```sh
python3 verify_source_manifest.py
```

Exit `0`:

```text
result=PASS
rows=167
references=3
errors=[]
manifest_digest=ec223ad4b65650be556e0f28c05bf94936635baa7efb3c39d4efabfb5fa3d028
```

This resolved every `commit:path`, checked actual Git object type and object id,
checked commit timestamps, and checked the R15 tree file list against Git.

## 6. Required adversarial mutations

Each mutation was applied to a temporary copy. The original candidate was not
modified.

| # | Mutation | Result | Actual reason |
|---:|---|---|---|
| 1 | A5 forged commit/path/blob plus fabricated first consumer | REJECTED | `A5: path manifest mismatch` |
| 2 | forged non-empty source timestamp | REJECTED | `A5: source_timestamp manifest mismatch` |
| 3 | forged source metadata timestamp/path | REJECTED | `C0: source metadata timestamp manifest mismatch` / unknown metadata field |
| 4 | PYAT_N11 forged path/blob under real commit | REJECTED | `PYAT_N11: path manifest mismatch` |
| 5 | missing S0 source | REJECTED | `S0: missing evidence source` |
| 6 | forged S16 primary-source blob | REJECTED | `S16: exact program-map blob` |
| 7 | damaged B1/B3A/B3AS/S39_S52 evidence | REJECTED | manifest mismatch for each |
| 8 | R15_V2 tree falsely identified as file blob | REJECTED | `R15_V2: object_type manifest mismatch` |
| 9 | fabricated ACTUAL consumer with no callable/source evidence | REJECTED | `A5: ACTUAL consumer lacks source evidence` |
| 10 | missing ownership | REJECTED | `A5: missing owner` |
| 11 | native promotion without permission | REJECTED | `A5: native promotion` |
| 12 | Pyat/Sorok N11 identity collision | REJECTED | `Pyat N0-N12/F1-F8 id set` |
| 13 | S5 product link removed | REJECTED | `S5: missing product link` |
| 14 | S5 generic-governance-only edge substitution | REJECTED | `S5: missing product path L1_S5_FLOURISHING->S5` |

The B1/B3A/B3AS/S39 subtest covers all four damaged lineage sources; its
subtests passed. Each negative failed for its manifest/object/consumer/product
reason, not an incidental exception.

## 7. Restore

After all temporary mutations, the original candidate was revalidated:

```text
result=PASS
144 Sorok rows, 23 Pyat rows, 4 assets, 80 L3 nodes, 461 edges, 46 slots,
0 priority decisions, 66 typed cycles
```

The candidate source files were not modified by any mutation.

## 8. NOT_RUN

- Full R6/R7 branch test suites and all four engineering-asset tests; their
  returns are cited at the declared author-tested grain only.
- Any native source, survey, provider/model call, native actor/world, C9/C12
  adoption, PRE-MAIN merge or production import.
- The old source-blind `VALIDATION_RESULTS.json` is not used.
