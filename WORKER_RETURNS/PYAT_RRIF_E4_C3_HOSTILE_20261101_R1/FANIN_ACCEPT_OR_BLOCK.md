# FAN-IN ACCEPT OR BLOCK — RRIF-E4 HOSTILE REVIEW

## Binary decision

`REJECT_WITH_MINIMAL_DEFECTS`

Exact full sourcefree fan-in of E1 head `ffd03934d0a86c98ed095d973e45587bd5751013` is BLOCKED. D01, PR526 custody, SAV float representation, C11/projection, EE-P2X integration, and G01 severance are green; D02 is not correct for the current decoder's real `DATETIME` output and is fail-open for aware `datetime` subclasses.

This is a reject of the exact full fan-in, not a rejection of accepted C3 D01, not a science/source-rights decision, and not a claim that E1 introduced a PREMAIN regression. The accepted-C3 code is faithfully restored; the current-decoder D02 claim is not met.

## Separate grades

- ENGINEERING: `FAIL_AT_D02_CURRENT_DATETIME_AND_AWARE_SUBCLASS`.
  - D01: `PASS`.
  - D02 exact built-in carrier: `PASS_AT_ACCEPTED_C3_BUILTIN_SCOPE`.
  - D02 current SAV/DTA `DATETIME` and aware subclass refusal: `FAIL`.
  - PR526/custody/SAV float/C11/EE-P2X: `PASS`.
  - G01 hostile: `2 FAIL on both E1 and PREMAIN`; pre-existing, `HELD`, out of D01/D02 scope.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`.
- AUTHORITY: `HELD`. No source-use, rights, license, issuer/use, G01, adoption, merge, or PR authority is granted by this review.
- SOURCEFREE SCIENCE/RIGHTS: `HOLD`. D01 SHAs are physical identities only; no raw source was opened; the three declared encodings remain unqualified against real raw source.

## Exact blocking defect

### Lines

- `rawlsing_next/pre553_physical_decoder.py:428-441` — the new `_physical_value` gate.
  - `:431`: `if type(value) in {_dt.datetime, _dt.date, _dt.time}:`
  - `:433-440`: one-level `.item()` check also uses exact `type(...)`.
  - `:441`: `return _jsonable(value)` stringifies every non-exact date/time subclass.
- `rawlsing_next/pre553_r5_codec.py:39-78` — the carrier primitive and normalizer.
  - `:41,50,55` in `opaque_decoder_value` and `:67` in `normalize_decoder_physical_value` use exact `type(...)`, so pandas `Timestamp`/subclasses are rejected or left unchanged.
- Secondary, not the primary blocker: `rawlsing_next/pre553_physical_decoder.py:173,570` — `classify_physical_value` cannot compare an `R5OpaqueValue` with range bounds and raises `TypeError` if an opaque date/time cell also has a declared range. This is pre-existing for stringified dates; record and guard during rework.
- API hold: `rawlsing_next/pre553_physical_decoder.py:852` — `_physical_value` is exported in `__all__` even though it is a private helper and tests import it directly. Remove unless a public API is intended.

### Negative witness

Real source-free SAV and DTA files containing `datetime.datetime(2008,4,5,6,7,8)` decode as pandas `Timestamp` in this environment. E1's real consumer then yields:

```
SAV: {'d':'opaque','t':'opaque','dtm':'str','f':'float64_finite'}
DTA: {'d':'opaque','t':'opaque','dtm':'str','f':'float64_finite'}
```

The decoder cell itself is `str '2008-04-05 06:07:08'`, not an `R5OpaqueValue`.

Plain subclass controls, with no pandas dependency:

```
NaiveDT(dt.datetime) -> decoder._physical_value: str '2008-04-05 06:07:08'
AwareDT(dt.datetime, tzinfo=UTC) -> decoder._physical_value: str '2008-04-05 06:07:08+00:00'
ItemWrapper(AwareDT(..., tzinfo=UTC)) -> decoder._physical_value: str '2008-04-05 00:00:00+00:00'
```

The aware cases do not raise `separate explicit decoder carrier authority`; they fall into the ordinary string lane. This contradicts E1 `00_RETURN.md`/`ORIGINAL_TO_CURRENT_SEMANTIC_DIFF.md` ("No date/time stringification occurs in the decoder cell route") and the unqualified authority sentence in `SOURCE_RIGHTS_AND_SCOPE.md` that timezone-aware values are refused. It also means the 33 green D02 tests, which use only exact built-ins, do not establish the claimed current-decoder behavior.

E1's `_physical_value`, `_compatibility_config`, and declared allowlist are byte-identical to accepted C3, and the R5 file is C3 blob `6000a1704…` byte-for-byte. The failure is the interaction of that exact-builtin scope with the current pyreadstat/pandas reader, not a hidden deviation from C3. pyreadstat 1.3.2 returns `Timestamp` under default, `apply_value_formats=False`/`user_missing=True`, and `dates_as_pandas_datetime=False`; only `disable_datetime_conversion=True` returns numeric offsets and is not used by E1.

## Minimal rework acceptance criteria

Do not launch a broad redesign. A minimal correction is sufficient:

1. Make the decoder/R5 date-time gate subclass-aware for naive `datetime.datetime`/`date`/`time` subclasses (at minimum pandas `Timestamp`). Either canonicalize to the exact built-in fields already used by the carrier (preserving `fold`, refusing `tzinfo is not None`), or explicitly refuse any unsupported subclass before the `_jsonable` fallback. Do not silently stringify.
2. Ensure an aware `Timestamp`/`datetime` subclass and an item wrapper returning one raise the explicit carrier-authority refusal, not a string.
3. Add a real pyreadstat SAV and DTA `DATETIME` regression test that reaches `iter_cells`/the real seam consumer and asserts `opaque`, not `str`.
4. Add an aware `Timestamp`/plain-`datetime`-subclass item-wrapper refusal test.
5. Decide and guard the `classify_physical_value` opaque-carrier-versus-range case (or explicitly document the refusal), and remove `_physical_value` from `__all__` unless public export is intended.
6. Correct the E1 return language to state the exact supported type scope; do not claim blanket "no stringification" or blanket aware refusal beyond the tested types.

Acceptance evidence should include the exact test names, real-consumer tags, and a negative witness showing the previously observed `str` now becomes the carrier or the explicit refusal.

## What is accepted now

- D01 exact three physical SHA/encoding pairs, wrong-pair refusal, no guessing/fallback, compatibility-lane conservation, physical-only authority status, and no legal source grant.
- Exact built-in D02 carrier bytes/fold, nested tuple/list/mapping and mapping-key normalization, string non-reinterpretation, one-level item unwrap, recursive item non-manufacture.
- PR526 content-bound snapshot, `O_RDONLY`, `/dev/fd`, unlink, stability/hash verification, idempotent close, tamper behavior.
- SAV finite float representation and current R5 `float64_finite`; no int/float coercion.
- Selected C11/source-projection, PR526, SAV representation, and EE-P2X suites.
- G01 severance: identical 2 failures on E1 and PREMAIN, not repaired, not in scope.

## What is blocked

- Exact full fan-in of E1 production/test/documentation as an unqualified D02 repair.
- Any claim that D02 currently carries the real decoder's `DATETIME` or that all timezone-aware datetime values fail closed.
- Any use of the D01 physical encoding admission as source-use, text-semantics, science, rights, issuer, or family/wave authority.

## Authority statement

HQ owns final adjudication. This reviewer does not self-adopt, merge, force-push, open a PR, or authorize production/source action. Recommendation to HQ: hold exact E1 full fan-in for the minimal D02 subclass correction above; D01 and the custody/float/C11/EE-P2X evidence remain usable, but the D02 claim must be narrowed or repaired before any exact fan-in is treated as a current-decoder D02 restoration.

Terminal: `FANIN_BLOCKED__D01_ACCEPT__D02_CURRENT_DATETIME_AND_AWARE_SUBCLASS_REWORK_REQUIRED__SCIENCE_AND_AUTHORITY_HELD`
