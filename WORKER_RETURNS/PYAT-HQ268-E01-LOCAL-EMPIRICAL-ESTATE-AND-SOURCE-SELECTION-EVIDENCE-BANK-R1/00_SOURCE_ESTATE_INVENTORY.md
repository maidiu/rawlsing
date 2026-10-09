# 00 — LOCAL SOURCE ESTATE INVENTORY (PYAT R1)

**Mode:** read-only local filesystem investigation. No raw survey decoding, no row extraction, no source transformation, no repository mutation.
**Machine:** this Mac (`/Users/matthewsmith`), which holds the actual Rawlsing source estate.
**Date:** 2026-10-09.

---

## 1. The `Data` directory (located without a hardcoded home assumption)

Discovered by walking the working tree from the current project root:

```
/Users/matthewsmith/Desktop/Rawlsing/data/Data
```

Not to be confused with:

| Path | What it is |
|---|---|
| `/Users/matthewsmith/Desktop/Rawlsing/data/` | Parent estate: survey-family subfolders, codebooks, manifests, `ddm_build_copy` |
| `/Users/matthewsmith/Desktop/Rawlsing/data/Data/` | **The 44-file flat source release directory (this report)** |
| `/Users/matthewsmith/Desktop/Rawlsing/data 2/` | Unrelated (`ddm_build_copy` stub only) |
| `/Users/matthewsmith/Desktop/Rawlsing/data/GSS/`, `data/LiTS/`, `data/Latinobarometro/`, `data/Asian Barometer/` | Additional/alternate physical copies — see §5 |

Directory mtime `2026-08-21 19:37`; contains **44 regular source files** plus one `.DS_Store` (excluded from all counts).

## 2. Headline result

| Quantity | Value |
|---|---|
| Source files present and readable | **44 / 44** |
| CLOSED35 registry identities physically present | **35 / 35** |
| Additional releases / country files not in CLOSED35 | **9** (all Asian Barometer Wave 6 country files) |
| Files with a previously recorded SHA-256 in an established manifest | **44 / 44** |
| Files whose current byte size matches that manifest exactly | **44 / 44** |
| Files whose current mtime matches that manifest exactly | **44 / 44** |
| Files physically re-hashed in this pass | **2** (narrowly scoped — see §4) |
| Genuinely missing / inaccessible sources | **0** |

Composition: **40 SAV + 4 DTA**. The four DTA files are LiTS I–IV; every other release is SAV.

## 3. Family breakdown (44 = 35 CLOSED35 + 9 additional)

| Family | Files in `data/Data` | CLOSED35 ids | Additional |
|---|---|---|---|
| Afrobarometer | 3 (R1, R5, R9) | 01–03 | — |
| Arab Barometer | 4 (W1, W2, W5, W8) | 04–07 | — |
| Asian Barometer | 12 (W1, W4, W5 + 9×W6 country) | 08–10 | 9× Wave 6 country files |
| EVS | 5 (1981, 1990, 1999, 2008, 2017) | 11–15 | — |
| GSS | 8 (1972…2024) | 16–23 | — |
| Latinobarómetro | 3 (1995, 2011, 2024) | 24–26 | — |
| LiTS | 4 (I, II, III, IV — `.dta`) | 27–30 | — |
| South Asia | 2 (W1, W2) | 31–32 | — |
| WVS | 3 (W1, W4, W7) | 33–35 | — |
| **Total** | **44** | **35** | **9** |

CLOSED35 registry source: `WORKER_RETURNS/ASTRA-PYAT-INTEGRATED-DEVELOPMENT-ATLAS-R1/data/closed35.json`
Horizontal matrix and grade legend: `WORKER_RETURNS/ASTRA-PYAT-INTEGRATED-DEVELOPMENT-ATLAS-R1/report/K_CLOSED35_HORIZONTAL_MATRIX.md`
(Grade letters are **historical representation-census PASS/BLOCKED — 20 PASS, 15 BLOCKED — not DDM maturity**, and not a statement about file presence.)

## 4. Identity: recorded vs. actually verified

**Established manifest used (no bulk re-hashing):**
`/Users/matthewsmith/Desktop/Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt`
— "Combined Rawlsing tree manifest with SHA-256, size, and date", generated `2026-08-23T15:27:12.888083-04:00`, columns `SHA256 | SIZE_BYTES | DATE | TYPE | PATH`.

For **all 44** files the manifest records a SHA-256; for all 44 the **current on-disk byte size and mtime match the recorded values exactly**. That is a strong documentary corroboration, but size+mtime is not byte identity.

**Narrow physical hashing performed in this pass (2 files only):**

| File | Bytes | SHA-256 computed now | Result |
|---|---|---|---|
| `LiTS_I.dta` | 139,531,180 | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | Matches manifest **and** the `source_identity.sha256` recorded inside the 3.4 GB retained checkpoint |
| `South Asia Wave 1.sav` | 595,974 | `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571` | Matches manifest (probe that manifest SHAs still describe current bytes) |

Rationale: `LiTS_I.dta` was hashed because a **specific identity dispute required it** — it is the only file whose bytes are named in a retained checkpoint's recorded source identity. The smallest file was hashed once as a manifest-corroboration probe. **The remaining 42 files were deliberately not hashed**; their identity status is `DOCUMENTARY_ONLY_NOT_REHASHED`.

Per-file detail (path, bytes, extension, readability, CLOSED35 mapping, recorded SHA, provenance, verification status) is machine-readable in `01_SOURCE_IDENTITIES.json`.

## 5. Alternate physical copies (equal filename ≠ equal bytes — checked)

Equal *sizes* were first observed, then identity was established **documentarily** from the same manifest (both sides hashed in the same 2026-08-23 run). No new hashing was done.

| Alternate copy | Canonical `data/Data` file | Recorded SHA-256 (both sides) |
|---|---|---|
| `data/LiTS/LITS-2006-data.dta` | `LiTS_I.dta` | `7cac43e2…8efc09` |
| `data/LiTS/lits2.dta` | `LiTS_II.dta` | `c43d0e18…b6130e9` |
| `data/LiTS/lits_iii.dta` | `LiTS_III.dta` | `368ae5d0…0065bcc8` |
| `data/LiTS/lits_iv.dta` | `LiTS_IV.dta` | `14e10327…223cd1c` |
| `data/GSS/GSS{1972,1973,1984,1993,2002,2010,2016,2024}.sav` (8) | matching `GSS*.sav` | identical per pair |
| `data/Latinobarometro/Latinobarometro_1995_data_english_spss_v2014_06_27.sav` | `Latinobarometro 1995.sav` | `4b7fc6da…e95926f7` |
| `data/Asian Barometer/v_merged.sav` | `Asian Barometer Wave 5.sav` | `2576e428…2bc4b5e63` |
| `data/Asian Barometer/W1 Merged Data/Merge/Wave1_20170906.sav` | `Asian Barometer Wave 1.sav` | `ac0b8bc1…f48e0ae1a2` |

These are **documentary duplicates only** — recorded as equal, not re-proven equal in this pass. They are *not* additional source identities and are not counted in the 44.

## 6. Why the estate was reported "missing" before is irrelevant here

HQ's earlier conclusion concerned a *different machine*. On this machine every one of the 44 files, and all 35 CLOSED35 identities, is physically present, readable, and size/date-consistent with the established manifest. **No source-family absence claim survives contact with this filesystem.** Ghana was not investigated and is not a required service input.

## 7. Storage condition (physical, not documentary)

`/System/Volumes/Data`: **466 GiB total, 433 GiB used, 12 GiB available (98 % capacity)**. This is a real constraint on any future large write, and is recorded as an environmental fact, not a missing file.
