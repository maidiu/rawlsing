# HQ262 E01 — two-source location and checksum receipts

**RESULT: `PHYSICAL_CUSTODY_HOLD__AUTHORIZED_TWO_SAV_CARRIERS_ABSENT_ON_THIS_HOST`**
**TERMINAL:** `HQ262_E01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`

**Agent:** existing DeepSeek-Harness/OpenCode governed source-metadata custodian
**Branch:** `agent/deepseek-harness-pyat-hq262-ghana-sav-dictionary-only-r1`
**HEAD at inspection:** `7c4a87c84a2350980293e6192626ce96e81864d5` (startup base `1ff7c74f…`)
**Live control:** `integration/pre-main-reconciliation-r1 @ 64b4e7ab1e67c139c7115430c711d459474cf31a`
**Sealed HQ262 checkpoint:** `20261009-PYAT-HQ262-G3-ADOPTED-G1-BOUNDARY-GHANA-DICTIONARY-LITS-CUSTODY-R1 @ b394b431…`
**Sealed worker row:** `HQ262_E01_GHANA_METADATA_ONLY` — branch and `commission_tip 7c4a87c8…` match.
**Laws read:** `PYAT_CONTROL_ROOM/HQ262_G1_DATA_ONLY_ENTRYPOINT_AND_GHANA_METADATA_INSPECTION_LIMITS_R1.md` (Part B custody);
prior adopted Ghana documentary return `8c9aefe11f294169c8d1c003cf1a0b96124c65b2`.
**Runtime:** governed CPython 3.11.3, macOS 13.7.8 x86_64, isolated sparse shared-store worktree
(`HEAD 7c4a87c8…`, clean). The worktree is used only for this return; **no source file was opened.**

## 1. Outcome

The HQ262 Part B conditional authorization permits a **memory-bounded streaming SHA256 and a
metadata-dictionary-only SAV read** of exactly two carriers. **Neither carrier exists on this host.**
Both were looked for at their own repository-recorded absolute paths; the containing directory is gone.

| carrier | expected sha256 | expected bytes | recorded path | observed |
|---|---|---|---|---|
| `Afro Barometer Round 5.sav` | `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651` | 49 689 458 | `/Users/matthewsmith/Desktop/Rawlsing/data/Data/Afro Barometer Round 5.sav` | **ABSENT** |
| `Afro Barometer Round 9.sav` | `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8` | 70 621 348 | `/Users/matthewsmith/Desktop/Rawlsing/data/Data/Afro Barometer Round 9.sav` | **ABSENT** |

`/Users/matthewsmith/Desktop/Rawlsing/data/Data/` itself **does not exist**. The recorded codebook
directory `data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/` is also absent.

Per Part B — *"If physical sources are unavailable locally … return a precise custodian/physical
locator HOLD; do not hunt Library or silently regenerate/download"* — **I stopped.** No SHA256 was
computed, no SAV header was parsed, no dictionary was read, and **no metadata finding is asserted**.

## 2. How the locators were established (primary, this run)

The two carriers are **not** Git-tracked (`git ls-tree` over the integration tree: no `*.sav`). Their
absolute paths are recorded in the repository's own manifests, which I read as custody documents, not
as source data:

- `data/ddm_build_copy/manifests/file_accounting_manifest.csv` — rows `raw_data,Afrobarometer,Round 5/9` carry
  `path = /Users/matthewsmith/Desktop/Rawlsing/data/Data/Afro Barometer Round {5,9}.sav`, sizes
  49 689 458 / 70 621 348, and a `green_metadata_read` disposition.
- `data/ddm_build_copy/manifests/source_dataset_manifest.csv` and `.yaml` — same two absolute paths and sizes.
- `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_BYTE_INVENTORY.csv`
  — `Afro Barometer Round 5.sav,49689458,c9200ba3…` and `Afro Barometer Round 9.sav,70621348,3afcecd0…`,
  confirming the expected sizes/hashes that HQ262 Part B cites. This inventory records **no filesystem path**.

## 3. Exhaustive absence evidence (primary, this run)

| check | result |
|---|---|
| exact recorded R5 path | `ABSENT` |
| exact recorded R9 path | `ABSENT` |
| `ls /Users/matthewsmith/Desktop/Rawlsing/data/Data` | `No such file or directory` |
| `find <repo>/data -iname "*.sav"` | none |
| `find ~ -iname "*afro*.sav" -not -path "*/Library/*"` (depth 10) | none |
| `find ~ -iname "*.sav" -not -path "*/Library/*"` (depth 8–10) | **2 files only** |
| Git tree | both carriers untracked |
| Library | **not searched** (forbidden) |

The only two `.sav` files on this host under the non-Library home are:

- `/Users/matthewsmith/Desktop/EVS 2008.sav` (63 832 833 bytes) — **different source**
- `/Users/matthewsmith/Desktop/WVS Wave 7.sav` (185 163 494 bytes) — **different source**

**Neither is a substitute.** The commission forbids silently substituting another source file; no
substitution was made.

## 4. Reader availability (recorded for the eventual resumed lane)

The governed interpreter is CPython 3.11.3. `pyreadstat` is **not installed**
(`ModuleNotFoundError: No module named 'pyreadstat'`). Even had the carriers been present, the
approved metadata-only reader would need to be provisioned in an already-authorized environment
before any dictionary read; the environment must not be expanded opportunistically.

## 5. What was NOT done

- No SHA256, no byte read, no header parse, no dictionary read, no case data, no respondent row,
  no column response value.
- No count, share, weight, trend, variance or uncertainty computation of any kind.
- No source download, no Library access, no regeneration, no source re-release.
- No substitution of the two present (`EVS`, `WVS`) carriers.
- No release-edition claim; no official binary↔release match from a filename.
- No FF02 LiTS work, no EE12/C7 pair use, no EE14 model use, no G0b grant, no V3, no N9/world claim.
- No code/test/source mutation outside this return directory.

## 6. Consequence

The two-wave instrument-to-retained-variable mapping **cannot be produced** on this host: the actual
Ghana country selector, native Q43/Q31 column mapping, native missing codes, weight candidate names
and PSU/stratum metadata are all **UNVERIFIED by this lane**. Documentary statements about Q43/Q31
codes and `withinwt`/`withinwt_ea`/`withinwt_hh` remain at the **already-adopted secondary
documentary grade** of `8c9aefe1…` and are **not** upgraded by this return.

See `03_DISPOSITION.json` for the exact custodian restore request and the conditions to resume.

**Terminal:** `HQ262_E01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.
