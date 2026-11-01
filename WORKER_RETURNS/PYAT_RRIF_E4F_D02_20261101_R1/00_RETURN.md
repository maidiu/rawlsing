# PYAT RRIF-E4F — D02 REAL DATETIME AND AWARE-SUBCLASS REPAIR — RETURN R1

Status: `ENGINEERING_PASS_CANDIDATE__D02_REAL_DATETIME_AND_AWARE_SUBCLASS_REPAIRED__PENDING_INDEPENDENT_REVIEW__SCIENTIFIC_HELD__AUTHORITY_HELD`

Binary fan-in recommendation: `HOLD_FOR_INDEPENDENT_REVIEW_OF_EXACT_CORRECTED_SHA`

One-line result: Naive pandas `Timestamp` and other naive `date`/`time`/`datetime` subclasses now canonicalize to the existing versioned opaque carrier by exact built-in civil fields, preserving fold and microseconds; timezone-aware subclasses and item wrappers refuse explicitly; real source-free SAV and DTA `DATETIME` fixtures now reach `PhysicalSourceIncidence.iter_cells` and the actual pinned first R5 seam consumer as `opaque`, never `str`. D01, PR526 custody, SAV float bits, C11/projection, and the selected suite remain green. The two G01 hostile failures remain identical on PREMAIN and the corrected cut and are not repaired.

## 1. Identity and execution envelope

- Role: bounded independent I3 physical decoder + R5 codec engineer. Not HQ, E1 or E4 author/reviewer, canonical integrator, or source issuer.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`
- Branch: `agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`
- STARTUP_SHA / branch start: `ffd03934d0a86c98ed095d973e45587bd5751013`
- PREMAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- E4 hostile return: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`
- Host: `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Harness: OpenCode 1.18.34, agent `build`.
- Session DB evidence (`~/.local/share/opencode/opencode.db`, read-only): session `ses_e680bf28effeGdJ4hyA8lvBrk7`, `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`, version `1.18.34`. MAX was observed active; no model/provider/account/editor/effort switch occurred.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- Execution surface: isolated sparse Git worktree, source-free pytest only. No raw survey source, native source, Sorok, PROGRAMMA, R9, actor, or production route was opened or executed.

## 2. Exact correction

Changed production files only:

- `rawlsing_next/pre553_physical_decoder.py`
- `rawlsing_next/pre553_r5_codec.py`

Added bounded D02 test:

- `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py`

D01 acceptance fixtures, the three SHA/declared-encoding pairs, PR526 custody, `_compatibility_config`, and the declared-encoding allowlist were not changed. The E1 33-test suite remains byte-for-byte green.

Behavior now:

- Exact naive built-in `datetime`/`date`/`time`: unchanged opaque carrier route.
- Naive pandas `Timestamp` and other naive subclasses: canonicalized by exact built-in civil fields into the existing versioned carriers `python.datetime.datetime@1`, `python.datetime.date@1`, `python.datetime.time@1`; fold and microseconds preserved.
- Timezone-aware `Timestamp`/`datetime`/`time` subclasses: explicit `R5CodecError` (`separate explicit decoder carrier authority`); never stringified.
- One-level `.item()` wrappers returning a supported naive value: canonical carrier; returning an aware value: explicit refusal.
- Sub-microsecond pandas precision (`nanosecond != 0`), `pandas.NaT`, and hostile subclasses with unreadable `tzinfo` or civil fields: typed `R5CodecError`; never stringified.
- Recursive item chains: still not chased into a carrier. The E1 accepted non-carrier fallback is preserved.
- `classify_physical_value` range declarations: incomparable values, including opaque date/time carriers, raise a typed `DecoderError` instead of an uncontrolled `TypeError`.
- `_physical_value` removed from `pre553_physical_decoder.__all__`; it remains a private helper used by the decoder cell route and direct tests.

## 3. Mandate results

| Area | Result |
|---|---|
| Real SAV `DATETIME` at `iter_cells` | PASS. Source-free pyreadstat fixture; cell type `R5OpaqueValue`, type id `python.datetime.datetime@1`, codec tag `opaque`, never `str`. |
| Real DTA `DATETIME` at `iter_cells` | PASS. Same opaque carrier and tag. |
| Actual first R5 seam consumer | PASS. Exact pinned `pre553_r5_seam.iter_source_native_rows` blob `cef326ebbc40468428378f7fdbe76e4756179f39` at owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` executed over the real fixtures; `dtm` rows are `opaque`, never `str`. |
| Naive `Timestamp`/subclass carriage | PASS. Exact payload, fold and microsecond tests. |
| Aware `Timestamp`/subclass refusal | PASS. Direct and one-level item wrapper both explicit-refuse. |
| Aware item-wrapper refusal | PASS. |
| Lossy date-like subclass refusal | PASS. `NaT`, sub-microsecond `Timestamp`, hostile `tzinfo`, hostile civil field. |
| Opaque carrier vs missing range | PASS. Typed `DecoderError`, not `TypeError`. |
| `_physical_value` export | PASS. Removed from `__all__`; public classifier remains exported. |
| E1 original 33 tests | PASS. 33 passed, exit 0. |
| Selected PR526/SAV/C11/EE-P2X suite | PASS. 194 passed, 1 skipped, exit 0. |
| G01 two hostile failures | UNCHANGED/HELD. Identical 2 failures on PREMAIN and corrected cut; out of D02 scope. |
| D01 SHA/encoding pairs and custody | PASS/UNCHANGED. No D01 or PR526 file changed; selected custody tests green. |
| SAV finite float exact bits | PASS. Python `float`, `float64_finite`, exact bits in new real fixture and selected suite. |
| Wrong-source tamper | PASS. Snapshot survives post-acquisition tamper; pre-decode tamper refuses. |

## 4. Test receipts (summary)

- E1 33: `33 passed`, exit `0`.
- E4F new D02: `12 passed`, exit `0`.
- Selected suite: `194 passed, 1 skipped`, exit `0`.
- G01 PREMAIN hostile-only: `2 failed, 6 deselected`, exit `1`; same two assertions as E1/E4.
- G01 corrected full pair: `2 failed, 7 passed`, exit `1`; same two assertions.

Exact commands, environment, per-module counts, logs, and hashes are in `COMPATIBILITY_AND_G01_BASELINE.md`.

Pre-patch RED witness at STARTUP_SHA `ffd03934d`:

```
sav str '2008-04-05 06:07:08' str
dta str '2008-04-05 06:07:08' str
AwareDT str '2008-04-05 00:00:00+00:00'
Wrapper str '2008-04-05 00:00:00+00:00'
```

Corrected witness:

```
sav R5OpaqueValue python.datetime.datetime@1 opaque
dta R5OpaqueValue python.datetime.datetime@1 opaque
AwareDT REFUSED timezone-aware datetime requires a separate explicit decoder carrier authority
Wrapper REFUSED timezone-aware datetime requires a separate explicit decoder carrier authority
```

## 5. Exact source identities

| Path | STARTUP blob | Corrected blob | Corrected sha256 |
|---|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |
| `rawlsing_next/pre553_r5_codec.py` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | absent | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` |

Full patch rationale and hunks are in `EXACT_PATCH_AND_SOURCE_BLOBS.md`.

## 6. Grades

- ENGINEERING: `PASS_CANDIDATE__D02_REAL_DATETIME_AND_AWARE_SUBCLASS_REPAIRED`. All requested D02 behaviors are demonstrated on real source-free SAV/DTA fixtures and the pinned seam consumer. This is an engineer return, not an independent review or adoption.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. No raw source was opened. No encoding text semantics, survey meaning, estimand, response state, or result is issued. The date/time carrier is physical representation only.
- AUTHORITY: `HELD`. No source-use/license/rights grant, timezone-aware carrier authority, G01 authority, issuer/use, adoption, merge, PR, or self-review is granted. Aware values remain refused because no such authority exists.

## 7. Holds and NOT_RUN

- HOLD: independent review of the exact corrected SHA by E4's independent reviewer or another distinct qualified reviewer.
- HOLD: HQ receiving/adoption decision. This return does not self-adopt or self-fan-in.
- HOLD: scientific/source meaning, source rights, issuer/use, G01, R9/Sorok/native/protected/actor/PROGRAMMA, and PRE-MAIN merge.
- HOLD: timezone-aware carrier authority. Aware subclasses now refuse; no representation was invented.
- NOT_RUN: actual raw survey-source decode under any declared encoding. Real fixtures are synthetic source-free pyreadstat files.
- NOT_RUN: full repository test suite. Only the mandated 33, selected 194/1, new 12, G01, and independent probes were executed.
- NOT_RUN: G01 repair. The two pre-existing failures are recorded, not repaired.
- NOTE: `rawlsing_next/pre553_r5_seam.py` is not tracked at STARTUP_SHA. The test loads the exact pinned historical seam and model blobs from the local Git object database read-only, verifies Git blob and SHA-256 identity, and executes them as the actual first consumer. No production file was added and no network source was read.

## 8. Return discipline

Only the two production files, one bounded test, and these five return documents are changed. No PREMAIN/main, D01, PR526, E1/E4 worktree, Sorok, native/protected source, or other worker state was modified. The final return commit SHA is read back from origin with `git ls-remote` after push and reported in the worker terminal response; it is not embedded here because embedding it would change the commit it identifies.

Terminal: `RRIF_E4F_D02__REAL_DATETIME_AND_AWARE_SUBCLASS_REPAIRED__E1_33_GREEN__SELECTED_194_1_GREEN__G01_TWO_PREEXISTING_FAILURES_UNCHANGED__INDEPENDENT_REVIEW_AND_HQ_HELD`
