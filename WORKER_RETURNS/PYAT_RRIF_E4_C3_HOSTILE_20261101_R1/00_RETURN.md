# PYAT RRIF-E4 — FINAL HOSTILE REVIEW OF E1 EXACT C3 PATCH — RETURN R1

Status: `ENGINEERING_REJECT_AT_D02_CURRENT_DATETIME_AND_AWARE_SUBCLASS__D01_PASS__SCIENTIFIC_AND_AUTHORITY_HELD`

Binary fan-in recommendation: `REJECT_WITH_MINIMAL_DEFECTS`

One-line reason: D01 is exact and green, but E1's D02 decoder gate handles only exact built-in `datetime` subclasses at the helper-test level; the real SAV/DTA decoder produces pandas `Timestamp` for `DATETIME`, which E1 silently stringifies through the unchanged `_jsonable` fallback. An aware `Timestamp` (and an item-wrapped aware `Timestamp`) therefore bypasses the claimed fail-closed timezone refusal. This falsifies E1's statement that no date/time stringification occurs in the decoder cell route and its unqualified claim that timezone-aware values fail closed. No production, PREMAIN, E1, Sorok, native/protected source, or other worktree was modified.

## 1. Review identity and execution envelope

- Role: fresh independent I3 hostile current-decoder/R5-codec reviewer. Not HQ, original C3 author, E1 author, integrator, issuer, or self-reviewer.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e4-c3-exact-patch-hostile-20261101-r1`
- Branch: `review/pyat-rrif-e4-c3-exact-patch-hostile-20261101-r1`
- Reviewer branch start: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- PREMAIN/startup: `8e44ca9c751049d65e6def47600b5c073ee04b29` (verified live at start; unchanged at end)
- E1 candidate head: `ffd03934d0a86c98ed095d973e45587bd5751013`
- Original accepted C3 code: `30686b185d4ceb2c94f61815ef70d8c8e76255d6`
- Host: `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Harness: OpenCode 1.18.34, agent build.
- Runtime model evidence, live process argv: `--model opencode-go/deepseek-v4.1-flash --variant max --agent build`.
- Runtime model evidence, read-only session DB (`~/.local/share/opencode/opencode.db`, session `ses_e6a83623fffem6ygKUq43tr0q1`):
  `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`, agent `build`, version `1.18.34`, directory equal to this reviewer worktree. MAX was genuinely active; no model/provider/host/account/editor/effort switch occurred.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- Execution surface: temporary detached Git worktree at E1 exact head `ffd03934d0a86c98ed095d973e45587bd5751013`, created outside the E1 working tree. Sparse checkout was limited to `rawlsing_next/`, top-level `tests/`, `WORKER_RETURNS/EE-P2R6S/`, `WORKER_RETURNS/FIABC-LM2/`, and the R1I inventory. The 83,340,882-byte content-addressed R1F carrier fixture was read-only symlinked from the E1 worktree after both paths were verified as blob `665fb2ae2f254e2e66014ede840ca55d275296d5` (sha256 `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`). The E1 worktree was read-only throughout; its HEAD remained `ffd03934d0a86c98ed095d973e45587bd5751013` and its status remained clean.
- Canonical main worktree was not touched: `/Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical` remained at `25830fe7462bb9e29bc4087e6ae14f3f84cec377` on `main`.

## 2. Exact production identities

| Path | PREMAIN blob | E1 blob |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` |
| `rawlsing_next/pre553_r5_codec.py` | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |

E1's `pre553_r5_codec.py` is byte-for-byte original accepted C3 blob `6000a1704d713f65e07610d81e9b3fd8bdd515ca` (`git cat-file -p ... | shasum -a 256` both `3ecaadb5b4e9100229e674967c6df3422145e860cbc4ff4acff264742d0be358`).

The E1 and accepted-C3 `_physical_value` functions are byte-identical (sha256 `d9a716c63eac1e3f94a79e7bc847ee75616809d0eb4012ea3f328dc50ddb03bd`, 16 lines). The `_compatibility_config` functions are byte-identical (sha256 `9cd25a55293e2558424f91bb5524a1efb97d46c38c3fb2562ba6809d5033dd8f`, 14 lines). The `DECLARED_ENCODING_ALLOWLIST` blocks are byte-identical (sha256 `b9b82cab7246699c74bb33731a272b934c83c7999b9ee4ba48313247159c2713`). This is an exact accepted-C3 restoration at the source-free code grain.

## 3. Mandate-results summary

| Area | Result |
|---|---|
| D01 exact three SHA/encoding pairs | PASS. Pairs are byte-identical to C3 and C3 parent `1f9990f`. Wrong SHA, wrong encoding, cross-pair, lowercase/alias, and `auto`/`guess`/`fallback` all refuse. No legal source-use grant: authority string is physical-decoding-only. |
| D01 synthetic end-to-end admission | PASS for both `BIG5` and `WINDOWS-1252` on SAV and DTA using a test-only in-memory SHA binding. No production pair was invented. |
| D02 exact built-in carrier bytes/fold | PASS. Date `>HBB`, time `>BBBIB`, datetime `>HBBBBBIB`, including `fold=1`; nested tuple/list/mapping and mapping-key normalization work; strings are not reinterpreted; bare codec date/time rejection remains. |
| D02 aware exact built-ins and item wrappers | PASS for exact built-ins: carrier and decoder route raise `separate explicit decoder carrier authority`. |
| D02 current decoder `datetime` | **FAIL/RED.** Real SAV and DTA `DATETIME` cells arrive as pandas `Timestamp`, not exact built-in `datetime`. `_physical_value` sends them through `_jsonable` and produces a string. |
| D02 aware subclass refusal | **FAIL/RED.** `AwareDT` (plain `datetime` subclass), aware `pandas.Timestamp`, and item-wrapped aware values are silently stringified, not refused. |
| PR526 snapshot / O_RDONLY / `/dev/fd` | PASS. Content-bound private snapshot, reader fd O_RDONLY, `/dev/fd`, unlink, stability/hash verification, idempotent close. |
| Wrong-source / tamper | PASS. Tamper before governed decode refuses on expected SHA; tamper of original path after acquisition does not change snapshot or cells. |
| pyreadstat regression | PASS for selected synthetic reader path; no signature or read-shape regression observed. |
| Current R5/SAV float representation | PASS. SAV finite floats remain Python `float` and encode `float64_finite`; exact bits preserved. G01 int-vs-float authority remains HELD and unchanged. |
| Real first decoder consumer | Confirmed, not just an import. Pinned WVS7/A consumer `pre553_r5_seam.iter_source_native_rows` (blob `cef326ebbc40468428378f7fdbe76e4756179f39` at owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`) was executed over synthetic SAV/DTA. It emits `date`/`time` as `opaque` but `datetime` as `str`. `ee_p2x_darwin_stage_backend._decode` was also exercised by the selected integration test. |
| G01 hostile baseline | 2 FAIL on E1 (`47f141e4…` float projection key vs `b9b72033…` int physical key; missing int special-state rule) and identical 2 FAIL on PREMAIN `8e44ca9c` (`-k "native_to_canonical or special_states"`, 6 deselected). Not repaired and not in D01/D02 scope; G01 authority HELD. |
| 33 targeted E1 tests | 33 passed, exit 0. |
| Selected PR526/SAV/C11/EE-P2X suite | 194 passed, 1 skipped, exit 0; per-module counts match E1's receipt. |

## 4. Decisive negative witness

The real SAV/DTA decoder path produces pandas `Timestamp` for `DATETIME`. On synthetic source-free files:

- SAV cells: `date -> R5OpaqueValue(date@1)`, `time -> R5OpaqueValue(time@1)`, `datetime -> str "2008-04-05 06:07:08"`.
- DTA cells: same tags.
- Pinned seam consumer tags: `{'d': 'opaque', 't': 'opaque', 'dtm': 'str', 'f': 'float64_finite'}` for both formats.

The exact gate is:

- `rawlsing_next/pre553_physical_decoder.py:431` — `if type(value) in {_dt.datetime, _dt.date, _dt.time}:`
- `rawlsing_next/pre553_physical_decoder.py:433-440` — one-level `.item()` check also uses exact `type(...)`.
- `rawlsing_next/pre553_physical_decoder.py:441` — fallback to `_jsonable(value)`, which returns `str(value)` for subclasses.
- `rawlsing_next/pre553_r5_codec.py:41,50,55,67` — carrier and normalizer also use exact `type(...) is ...` and reject/leave subclasses unchanged.

Additional subclass witness independent of pandas:

```
NaiveDT(2008,4,5,6,7,8)                    -> _physical_value: str '2008-04-05 06:07:08'
AwareDT(2008,4,5,6,7,8,tzinfo=timezone.utc) -> _physical_value: str '2008-04-05 06:07:08+00:00'
ItemWrapper(AwareDT(..., tzinfo=timezone.utc)) -> _physical_value: str '2008-04-05 00:00:00+00:00'
opaque_decoder_value(AwareDT(...))         -> R5CodecError: unsupported opaque decoder value type AwareDT
```

The last line is not the required carrier-authority refusal at the decoder route because `_physical_value` never calls the carrier for subclasses; it stringifies first.

This is not a new PREMAIN regression: PREMAIN `_jsonable` also stringified these values, and accepted C3 has the same exact-type scope. The RED is against E1's current-decoder D02 claim and real first consumer, not against historical C3 byte fidelity. E1's own `SOURCE_RIGHTS_AND_SCOPE.md` narrows D02 to built-in types, but `00_RETURN.md` and `ORIGINAL_TO_CURRENT_SEMANTIC_DIFF.md` state without qualification that no date/time stringification occurs and that aware values fail closed. The current decoder does not satisfy those statements.

Secondary residual boundary (not the primary blocker): `classify_physical_value` compares range declarations with `lo <= value <= hi`; with an `R5OpaqueValue` date carrier carrying a user-missing range this raises `TypeError: '<=' not supported between instances of 'int' and 'R5OpaqueValue'` (`pre553_physical_decoder.py:173,570`). This was already reachable for stringified date values; it is recorded as `HOLD`, not claimed as a new regression.

## 5. Per-hunk verdict

Full hunk reasoning is in `EXACT_PATCH_REVIEW.md`.

- Decoder D-1 import, D-2 constant, D-3 allowlist, D-4 call site, D-6 config: `ACCEPT`.
- Decoder D-5 `_physical_value` current-decoder gate (`428-441`): `RED`.
- Decoder D-7 public constants in `__all__`: `ACCEPT`.
- Decoder D-8 private `_physical_value` export (`852`): `HOLD` (unnecessary API surface).
- R5 R-1 import and R-4 `__all__`: `ACCEPT`.
- R5 R-2/R-3 carrier/normalizer (`39-78`): `ACCEPT` at exact-built-in accepted grain; `HOLD` for current-decoder subclass integration.

## 6. Grades

- ENGINEERING: `FAIL_AT_D02_CURRENT_DATETIME_AND_AWARE_SUBCLASS`; D01, custody, SAV float, C11, EE-P2X and G01 severance are green. Exact fan-in is blocked pending the minimal correction named in `FANIN_ACCEPT_OR_BLOCK.md`.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. No raw source was opened, no encoding text semantics, survey meaning, estimand, U/E_pre, or result was issued. D01 SHAs are physical identities only.
- AUTHORITY: `HELD`. No source-use/license/rights grant, G01 authority, issuer/use, adoption, merge, PR, or self-review. D02 timezone-aware carrier authority is absent and not implicitly granted by stringification.

## 7. Return files and commit discipline

Only these four files are added on this reviewer branch under `WORKER_RETURNS/PYAT_RRIF_E4_C3_HOSTILE_20261101_R1/`:

- `00_RETURN.md`
- `EXACT_PATCH_REVIEW.md`
- `TEST_RECEIPTS_AND_BASELINE_SEVERANCE.md`
- `FANIN_ACCEPT_OR_BLOCK.md`

No production code, tests, PREMAIN/main, E1 branch/worktree, Sorok, native/protected source, or other worker state was modified. The exact pushed return-commit SHA is read back with `git ls-remote` after normal push; it is not embedded here because embedding it would change the commit it identifies.

## 8. Holds and NOT_RUN

- NOT_RUN: actual raw survey-source decode under the three exact declared encodings. No raw source was opened. Actual source-use qualification remains HELD to the PRE-MAIN physical-decoder/native-source-rights owner.
- NOT_RUN: actual WVS7/LITS raw-source date/time presence or decode; synthetic source-free fixtures only.
- NOT_RUN: full repository test suite; only the mandated 33 and selected 194/1 suites plus G01 were run.
- NOT_RUN: timezone-aware carrier authority; absent by design and not authorized by this review.
- NOT_RUN: G01 repair/integration; the two known hostile failures remain identical and out of D01/D02 scope.
- HOLD: D02 pandas `Timestamp`/`DATETIME` carriage and aware-subclass refusal, pending minimal rework.
- HOLD: opaque-date carrier versus range-declaration classification (secondary, pre-existing).
- HOLD: scientific/source meaning, source rights, issuer/use, G01, R9/Sorok/native, adoption/merge/PR.

Terminal: `RRIF_E4_C3_EXACT_PATCH__D01_ACCEPT__D02_CURRENT_DATETIME_RED__EXACT_FANIN_BLOCKED__HQ_ADJUDICATION_REQUIRED`
