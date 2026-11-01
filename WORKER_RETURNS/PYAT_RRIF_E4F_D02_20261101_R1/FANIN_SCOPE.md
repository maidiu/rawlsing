# FAN-IN SCOPE — RRIF-E4F D02

## 1. Decision requested

`HOLD_FOR_INDEPENDENT_REVIEW_OF_EXACT_CORRECTED_SHA`

This engineer does not self-review, self-adopt, or self-fan-in. HQ owns the receiving and adoption decision. E4's independent reviewer or another distinct qualified reviewer should challenge the exact corrected commit SHA, not this narrative.

## 2. What this return establishes

At the exact corrected cut, source-free evidence establishes:

- Real pyreadstat SAV `DATETIME` cells reach `PhysicalSourceIncidence.iter_cells` as `R5OpaqueValue` with `python.datetime.datetime@1`, not `str`.
- Real pyreadstat DTA `DATETIME` cells do the same.
- The actual pinned first R5 seam consumer `iter_source_native_rows` emits `opaque` for those cells, not `str`.
- Naive `pandas.Timestamp` and other naive `date`/`time`/`datetime` subclasses canonicalize by exact built-in civil fields, preserving fold and microseconds.
- Timezone-aware `Timestamp`, aware plain subclasses, aware `time` subclasses, and one-level `.item()` wrappers returning them refuse with the explicit carrier-authority error and never stringify.
- `pandas.NaT`, sub-microsecond pandas precision, and hostile date-like subclasses that cannot preserve civil identity refuse with typed `R5CodecError`; no string fallback.
- Opaque date/time carriers with numeric range declarations now produce a typed `DecoderError`, not an uncontrolled `TypeError`.
- `_physical_value` is no longer in `__all__`; the public classifier remains.
- D01, PR526 custody, SAV float bits, C11/projection, and EE-P2X compatibility remain green.
- The two G01 hostile failures are identical on PREMAIN and the corrected cut and remain `HELD`.

## 3. What this return does not establish

- No scientific meaning, response state, encoding text semantics, survey meaning, estimand, or result. Date/time carriage is physical representation only.
- No source-use, license, rights, issuer/use, or source authority. The three D01 SHA/encoding pairs are physical identities only.
- No timezone-aware carrier authority. Aware values refuse; this return does not invent a timezone representation.
- No G01 representation-authority repair or authority.
- No R9, Sorok, native/protected source, actor, or PROGRAMMA authority.
- No PREMAIN merge, PR, adoption, or canonical integration.
- No claim of full-repository test coverage.
- No claim that recursive item chains are refused. One-level `.item()` wrappers are subclass-aware; recursive item chasing remains deliberately absent, preserving the E1 accepted non-carrier fallback. This is a scope boundary for review.

## 4. Files eligible for exact fan-in review

- `rawlsing_next/pre553_physical_decoder.py` — blob `4b89c4598f324834de064c1200c63698a20e3c5c`
- `rawlsing_next/pre553_r5_codec.py` — blob `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7`
- `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` — blob `c07c2019455e6264b4297c1c1d782bd887b96bdd`
- Return documents in this directory.

No other production or test file is changed. D01, PR526, and G01 files are not changed.

## 5. Required independent challenges

The reviewer should independently:

1. Recompute the two corrected source blobs and the new test blob from the exact pushed commit.
2. Re-run the real SAV/DTA fixture test and verify it reaches `iter_cells` and the pinned seam, not an import-only or mocked path.
3. Re-run the aware `Timestamp`/subclass and item-wrapper refusal tests and confirm no string fallback.
4. Re-run the original E1 33 and selected 194/1 suites from the exact corrected SHA.
5. Re-run the G01 hostile pair on PREMAIN and the corrected cut and confirm the same two failures.
6. Challenge whether canonicalizing a subclass to built-in civil fields is acceptable physical identity under the accepted D02 scope, including the explicit refusal of nonzero pandas nanoseconds.
7. Challenge the test-only loading of the historical pinned seam and model blobs from the local Git object database, and decide whether that satisfies the "actual first consumer" requirement or requires a different bounded evidence route.
8. Confirm that recursive item chains are outside the accepted one-level wrapper scope and are not a hidden fail-open for aware date-like values.

## 6. Authority statement

This worker is an I3 bounded independent physical decoder + R5 codec engineer. It is not HQ, E1 or E4 author/reviewer, canonical integrator, or source issuer. It does not grant scientific, source-rights, G01, timezone-aware carrier, adoption, merge, or self-review authority.

Terminal: `FANIN_HELD__D02_CORRECTION_READY_FOR_INDEPENDENT_REVIEW__SCIENCE_AND_AUTHORITY_HELD`
