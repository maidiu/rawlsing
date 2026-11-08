# PYAT #777 — universal source-to-C11 candidate return

**Status: CANDIDATE — NOT MERGED. `goal_complete=false`. Independent review required.**

- Repository: `maidiu/rawlsing`
- Branch: `agent/pyat777-source-to-c11-universal-20261108-r1`
- Implementation commit: `baf199195a84a5805531bcf694e563b77c4735d3`
- Parent/start gate: `a3450e7bb8c923062e5e14ac07ac44a9bf118ddd`
- Return-artifact commit and final branch head: recorded by direct `git ls-remote` in the final return response.
- Issue: #784 (`PYAT #777 — UNIVERSAL SOURCE-TO-C11 PIPELINE — all 35 declared sources, no single-wave target`)

## What was built

One generic, data-driven receive layer:

`rawlsing_next/universal_source_to_c11/`

It is driven by the declared 35-source roster and the imported R157
configurations. Source IDs are data keys only. There are no per-wave scripts,
no per-wave branches and no single-wave target.

The layer:

1. loads every declared original and nonrespondent-fixture configuration from
   the frozen R157 package;
2. builds the actual `GovernedC11Projection` through the branch-only generic
   factory `rawlsing_next.source_configuration.factory`;
3. receives each fixture release through the **current installed C11 consumer**
   (`pre553_source_backed_c11_facade` candidate construction, then
   `pre553_c11_ingest.validate_c11_source_release` /
   `ingest_c11_source_release`, then the append-only
   `pre553_c11_repository.C11Repository`);
4. cross-checks the current-consumer release against the recorded R157 native
   receipt, and against the independent facade path.

No new empirical engine, replacement C11/I03/Batch owner or
`NativeSourcePackage` mandate was added.

## Exact reused capital and provenance

- R157 candidate: `1384612bfed8d801140e00ace353779338599da3`
- R157 review/source cut: `d81bc2c67baf933461ae6cfca468f24779cc7e44`
  (package/config/fixture content is identical at both cuts)
- R157 plan seal: `4c0c619eac747afee1d8e65e1418bf2d472da4c3`
- Imported exact-cut files: **456**, verified by Git blob identity against the
  R157 candidate. Import tree identity:
  `d448e66b072a177470e7d5b6baf882fe614f40c488a58662d02ea53cf28ef177`.
- Imported material: `rawlsing_next/source_configuration`,
  `source_pre553_validation`, `SOURCE_PRE553_PLAN`, and the exact R157
  `pre553_source_read_admission.py` transport dependency.
- The portable evidence manifest verifies: 35 sources, 18,413 physical slots,
  18,276 original items, 18,250 exact relation joins, 26 explicit unmatched
  IDs.

Full per-file manifest and verification: `PROVENANCE.json`.

## 35-source ledger and disposition

Full machine-readable ledger: `35_SOURCE_LEDGER.json`; readable table:
`35_SOURCE_LEDGER.md`.

| Measure | Value |
|---|---:|
| Declared sources | **35** |
| Physical slots | **18,413** |
| Original item identities | **18,276** |
| Exact full-relation joins | **18,250** |
| Explicit unmatched relation IDs | **26** |
| Held slots | **1,653** |
| Fixture releases proven through current C11 | **35/35** |
| Original execution `NOT_RUN` | **24** |
| Original scope `FIXTURE_ONLY` | **11** |
| Original execution disposition | **NOT_RUN** |

The 11 `FIXTURE_ONLY` original scopes are SRC01–03 and SRC08–15. The other 24
original configurations retain a declared configuration slice, but original
execution is still `NOT_RUN` for all 35. Fixture proof does not establish
original-source scientific execution.

## Current C11 owner / ABI and receive seam

Current installed owners (exact hashes in `OWNER_ABI.json`):

| Owner | SHA-256 |
|---|---|
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf` |
| `rawlsing_next/pre553_c11_ingest.py` | `0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf` |
| `rawlsing_next/pre553_c11_repository.py` | `77ec0997b8aab0bb00c7d0ca93997fb3f3a041ace1c6661c1efb1185c9affad2` |
| `rawlsing_next/pre553_c11_integrity.py` | `3963facef5c8ae2981991ffa8c5c5c9b717fb4e09f342eec277198fc5cf38a33` |
| `rawlsing_next/pre553_physical_decoder.py` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |

Receive seam:

```text
rawlsing_next.source_configuration.factory.build_governed_c11_projection
→ rawlsing_next.pre553_source_backed_c11_facade.project_c11_candidate_from_physical_cells
→ rawlsing_next.pre553_c11_ingest.validate_c11_source_release
→ rawlsing_next.pre553_c11_ingest.ingest_c11_source_release
→ rawlsing_next.pre553_c11_repository.C11Repository
```

The R157 owner mapping is preserved as exact-cut provenance; the current facade
has evolved, so the current hash is recorded separately in `OWNER_ABI.json`.
This is a transparent provenance split, not a silent replacement.

## Proof results

### All 35 fixture releases through the current C11 consumer

`PROVE_ALL_RECEIPTS.json`:

- 35/35 `ACCEPTED_C11_LOGICAL_RELEASE`
- 35/35 current-consumer release hashes equal the recorded R157 native receipts
- 35/35 facade release refs equal the current-ingest release refs
- 35/35 repository inventories contain exactly the one exact release
- M01–M18 coverage present for every release
- `source_read_performed=false` for every release
- `original_execution=NOT_RUN` for every release
- `native_source_package_required=false` for every release

### Focused tests

- `41 passed` — `rawlsing_next/tests/test_universal_source_to_c11.py`
  (includes 35 parametrized all-source current-consumer cases, cold restore,
  negative/refusal, provenance, owner/ABI and ledger checks).
- `37 passed, 2 skipped` — R157 foundation/library/P3/read-admission focused
  suite. The two skips are the R154 loader tests because the R154 runtime/store
  is not imported into this branch. The all-35 current-consumer suite is the
  focused receive proof.
- Receipts: `TEST_RECEIPT_universal.txt`, `TEST_RECEIPT_r157_focused.txt`,
  `TEST_RECEIPTS.json`.

### Cold restore

`COLD_RESTORE.json`:

- From an unrelated empty temporary cwd with only `PYTHONPATH` pointing at the
  repository, the committed index loaded and `SRC26` was received through the
  current C11 consumer.
- A fresh `build-index` produced a **byte-identical** JSON index:
  `be69b414f0c03ffc70e0888137c4bde5a8114a3890011f7e1a40ebdbf83770f6`.
- Restored `SRC26` release:
  `528ca5c34f7d9fd3c92ae5832d7be0001fec001a1053a046ba899a1ceda3164f`.

### Negative / refusal evidence

`NEGATIVE_EVIDENCE.json` — 8/8 checks pass:

1. unknown source ID refused;
2. cross-source fixture refused before construction;
3. fixture reuse of the original source SHA refused;
4. fixture config refused as an original source-read transport;
5. wrong active source SHA refused by the generic factory;
6. original execution `NOT_RUN` for all 35 original configs;
7. no SAV/DTA/POR/DB source-byte carriers bundled;
8. original operation plan remains metadata-only
   (`source_read_performed=false`, `original_workload_issued=false`).

## Exact first real-source dependency

Typed, not manufactured:

```text
EXTERNAL_SOURCE_SELECTION_RIGHTS_BYTES_ISSUER
```

The first blocking dependency is an authorized owner's exact **source-and-wave
selection together with the rights/target-use determination for that exact
source**. Only then can the external source bytes/custody locator and a current
issuer source-read decision be named. A separately issued original workload is
still required after that. None of these is present or claimed here.

## Boundary preserved

- No original respondent row, SAV/DTA/DB byte or original source file was read.
- No source byte was copied or uploaded.
- No original source execution or original workload issuance was performed.
- No source-read permission or issuer decision was created.
- No protected/production merge was performed.
- No new engine or replacement C11/I03/Batch was added.
- No universal `NativeSourcePackage` mandate was introduced.
- No per-wave script, per-wave branch or single-wave target was introduced.
- 24 `NOT_RUN` + 11 `FIXTURE_ONLY` and original execution `NOT_RUN` are
  preserved exactly.

## Reproduction commands

See `COMMANDS.md`. Key checks:

```sh
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli status
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli ledger
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli prove-all
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli cold-restore SRC26
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli negative
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli owner-abi
PYTHONPATH=. python3 -m rawlsing_next.universal_source_to_c11.cli provenance
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_universal_source_to_c11.py -q -o addopts=''
```

## Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `35_SOURCE_LEDGER.json` | `ae3535c23e95bdb9ba236f1c7d96caff0a39607f0e8636a055398b350bafacd9` |
| `35_SOURCE_LEDGER.md` | `c954ebf77e7a7e5831eb798d99d71308d1a9c452cb3317afda96d133dbe83112` |
| `COLD_RESTORE.json` | `6744c5c01beea8e734162331ec7c7a61f5b54fe283a99e65913415fd395830ff` |
| `NEGATIVE_EVIDENCE.json` | `5e0759af424d577229f5c5c5929c4840e2bf2490d54087f0de7f375333723b32` |
| `OWNER_ABI.json` | `73ba98ce424e91c98ebeab4bf700b27d319e6ba9d04eda453177c89db8c9013c` |
| `PROVENANCE.json` | `0ea789a712c44965f8744b97d6c50ce668eb6be1b7fd823a5391fba6cdb62c9d` |
| `PROVE_ALL_RECEIPTS.json` | `d49bba84ec883ec6a29113005c6e703d03464f36570e8429a11d763fd8b9169d` |
| `TEST_RECEIPTS.json` | `85c62f15b86d0c7335fdd5ba3829c6c9a74ae3068e1096b3465fcbf696da6f40` |

## Independent review request

Please review this candidate branch and the evidence above independently. This
return makes no completion claim and does not merge to `main` or any protected
branch. `goal_complete=false`; independent review remains required.
