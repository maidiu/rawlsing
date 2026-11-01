# PYAT RRIF-E1 C3 D01/D02 CURRENT-DECODER REPAIR — RETURN — R1

Status: `ENGINEERING_PASS_AT_DECLARED_SOURCEFREE_SELECTED_GRAIN__SCIENTIFIC_AND_AUTHORITY_HELD__INDEPENDENT_REVIEW_REQUIRED`

Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e1-c3-decoder-repair-20261031-r1`
Branch: `agent/pyat-rrif-e1-c3-decoder-repair-20261031-r1`
Startup/PREMAIN base: `8e44ca9c751049d65e6def47600b5c073ee04b29` (verified live at start; no merge or mutation)
Implementation commits:
- `2edf5df01fd9de66abca2733c0878c4ea981707d` — D01/D02 code and frozen tests
- `1401bc7e0f5988bdeda9250e56ffe9fe26e306b1` — R5 codec byte-aligned to accepted C3 blob `6000a1704`
- `90c1c0eefc66263981ba9066faab22c35dc57f9f` — minimal D01 decoder patch surface
Remote readback for `90c1c0eefc66263981ba9066faab22c35dc57f9f`:
`90c1c0eefc66263981ba9066faab22c35dc57f9f` (exact 40-hex via `git ls-remote origin refs/heads/agent/pyat-rrif-e1-c3-decoder-repair-20261031-r1`)
Return-documentation commit: the commit that adds these five files after the implementation commits; its final remote readback is reported in the execution return.

## Provenance and execution grain

- Host: `mainMac.lan`, macOS 13.2.1, Darwin 22.3.0, x86_64.
- Execution surface: S2 exclusive local Git worktree; original-sourcefree pytest.
- Model: `opencode-go/deepseek-v4.1-flash` (runtime model ID). Variant/effort: `UNKNOWN` from the shell; no model, provider, host, account, editor, or effort switch occurred.
- Harness identity supplied by the envelope: OpenCode 1.18.34, agent build.
- Runtime: Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1.
- No raw survey source, native/protected source, CAN/ADP, N11/N12, Sorok, PREMAIN authority, S3/native execution, issuer, use, science, merge, PR, or self-review was performed.

## D01 result — exact declared-encoding admission restored

The three exact full pairs were recovered from original authoritative sourcefree code at candidate decoder blob `37013eb52efb8b61ef202b0d686f729f459d79c5` (`3cefb4ebf61ccdb6a8c5a03815438bdcda021292`) and accepted D01 integration `1f9990fec3d305ea89dfe25bdeae89a967adb21b`:

| Exact source SHA-256 | Declared encoding |
|---|---|
| `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` | `BIG5` |
| `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` | `WINDOWS-1252` |
| `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` | `WINDOWS-1252` |

No pair is `HOLD`: all three full 64-hex values are present in the original code. The source SHA is a physical identity only; it is not legal source-use authorization.

Current `_compatibility_config` now preserves the existing compatibility lane and adds the exact declared lane:

- `encoding is None` -> `{"encoding": None, "authority_status": None}`
- `auto`, `guess`, `fallback` -> `DecoderError` (guessing/fallback forbidden)
- exact `COMPATIBILITY_ALLOWLIST` SHA+encoding -> `COMPATIBILITY_ONLY`
- exact `DECLARED_ENCODING_ALLOWLIST` SHA+encoding -> `SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY`
- any other SHA+encoding -> `DecoderError`; no auto fallback

The declared lane authorizes physical decoding only, not text semantics, family/wave inheritance, or source use.

## D02 result — opaque naive date/time carriage restored

Exact current semantics:

- `opaque_decoder_value` accepts only exact built-in naive types via `type(value) is ...`:
  - `datetime.datetime` -> type id `python.datetime.datetime@1`, big-endian `>HBBBBBIB` (year, month, day, hour, minute, second, microsecond, fold)
  - `datetime.date` -> type id `python.datetime.date@1`, big-endian `>HBB` (year, month, day)
  - `datetime.time` -> type id `python.datetime.time@1`, big-endian `>BBBIB` (hour, minute, second, microsecond, fold)
- Timezone-aware `datetime.datetime` and `datetime.time` are refused when `tzinfo is not None`, including item-unwrapped variants.
- `normalize_decoder_physical_value` recursively normalizes nested tuples, lists, and mappings; tuple/list container types are preserved, mapping keys and values are normalized, and `fold` is carried exactly.
- The decoder route `_physical_value` normalizes direct built-in date/time values and one-level `.item()` unwrapped date/time values, then falls back to the unchanged `_jsonable` route. It does not recursively chase `.item()` chains to manufacture an opaque carrier.
- `R5TypedValueCodec.encode` still rejects bare date/time objects; only explicit `R5OpaqueValue` carriers cross as `{"t": "opaque", ...}`. No date/time stringification occurs in the decoder cell route.
- The R5 codec file is now byte-for-byte the accepted C3 codec blob `6000a1704d713f65e07610d81e9b3fd8bdd515ca`.

## Current receiver and real first decoder consumer

- Actual decode call consumer: `rawlsing_next/ee_p2x_darwin_stage_backend.py:708` (`_decode`), calling `decode_dta(..., encoding="latin1")` or `decode_sav(...)` at line 724.
- Real first decoded-cell consumer: `_compose_lits` at `rawlsing_next/ee_p2x_darwin_stage_backend.py:1335`, using `incidence.iter_cells(batch_size=20_000)` at lines 1403 and 1409.
- PR526 custody is preserved: content-bound private snapshot, `O_RDONLY`, `/dev/fd` reader path, stability/hash verification, unlink, and idempotent close. No R9 broker/session or raw-path transplant was introduced.

## Exact changed blobs

Production and tests:

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` |
| `rawlsing_next/pre553_r5_codec.py` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` |

Documentation blobs:

| Path | Blob |
|---|---|
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/00_RETURN.md` | `SELF_REFERENTIAL_NOT_EMBEDDED` |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/ORIGINAL_TO_CURRENT_SEMANTIC_DIFF.md` | `b28a5fe793b7cc64a4bdce52cf343a59bd6edeb4` |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/POSITIVE_AND_NEGATIVE_TESTS.md` | `9fa4531663ca0b534e55c9c0d201baf02c7b4a04` |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/SOURCE_RIGHTS_AND_SCOPE.md` | `bdd0b1bcff089364b347297b9dc034b5a12434ea` |
| `WORKER_RETURNS/PYAT_RRIF_E1_C3_20261031_R1/PROPOSED_FANIN.md` | `SELF_REFERENTIAL_NOT_EMBEDDED` |

The three non-self-referential documentation blob IDs are final. `00_RETURN.md` and `PROPOSED_FANIN.md` cannot embed their own final blob IDs without changing those IDs; their authoritative blobs are the committed tree entries for the return commit.

## Test evidence

Final targeted suite (three new files):

```
python3 -m pytest -q \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

Result: `33 passed`, exit `0`.

Final combined selected regression suite:

```
python3 -m pytest -q \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  tests/test_ee_p2x_darwin_court_driver.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py
```

Result: `194 passed, 1 skipped` in 151.98s, exit `0`.

Per-module passed counts in that run: new D01/D02/consumer `33`; PR526 custody `26`; SR06 `16` plus `1 skipped`; SAV physical boundary `7`; SAV representation authority `9`; LITS representation authority `10`; universal source projection `31`; universal workload `16`; R35 physical metadata `6`; source-backed C11 facade `10`; EE-P2X court driver `19`; final measurement telemetry `11`.

Pre-existing out-of-scope G01 hostile red:

```
python3 -m pytest -q \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Result: `2 failed, 7 passed`, exit `1`. The failures are the known G01 int-vs-float hostile expectations (`47f141e4...` float projection key versus `b9b72033...` int physical key, and the missing int special-state rule). The same two failures were reproduced with the two production files stashed to startup `8e44ca9c751049d65e6def47600b5c073ee04b29`:

```
python3 -m pytest -q rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py \
  -k "native_to_canonical or special_states"
```

Baseline result: `2 failed, 6 deselected`, exit `1`, identical assertion values. Stash pop exit `0`. This is causal severance: the G01 red is pre-existing and out of D01/D02 scope; G01 authority remains HELD.

## Grades

- ENGINEERING: `PASS_AT_DECLARED_D01_D02_SOURCEFREE_SELECTED_GRAIN`. The exact D01 pairs and D02 carrier are restored at the current decoder/codec; 33 new tests and 194 selected regression cases pass; PR526 custody, SAV float representation, and the actual stage-backend consumer are green. The two pre-existing G01 hostile failures are unchanged at baseline and are not claimed as repaired.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. Encoding is physical decoding only; date/time carriage is representation only. No raw survey source, survey semantics, estimand, U/E_pre, or measured result was issued.
- AUTHORITY: `HELD`. No source-use/rights authorization, G01 authority, issuer/use, adoption, merge, PR, or self-review. D01 SHAs are physical decoder identities, not legal authorization.

## Unresolved owner choices and holds

1. G01 nine-surface native-int to float64 representation authority remains a separate current G01/C11 owner choice. The current code and its two pre-existing hostile failures were preserved unchanged; numeric coercion was not broadened.
2. Actual raw-source execution under the three declared encodings remains HELD to the PRE-MAIN physical-decoder/native-source-rights owner. No raw source was opened.
3. Timezone-aware date/time carrier authority remains absent and fail-closed. A future explicit carrier authority is a separate owner decision.
4. R9 broker/session/binding, source permission, issuer/use, and science remain outside this return.
5. `#580`–`#584`, PREMAIN/main, Sorok, native/protected source, and all other worker/worktree state remain untouched.

## Review and terminal

A different hostile reviewer must inspect the exact final commit; this worker did not review itself. No PR or automatic merge was created.

Terminal: `RRIF_E1_C3_D01_D02_CURRENT_DECODER_REPAIR__SOURCEFREE_SELECTED_GREEN__G01_PREEXISTING_HOSTILE_RED_HELD__INDEPENDENT_REVIEW_REQUIRED`
