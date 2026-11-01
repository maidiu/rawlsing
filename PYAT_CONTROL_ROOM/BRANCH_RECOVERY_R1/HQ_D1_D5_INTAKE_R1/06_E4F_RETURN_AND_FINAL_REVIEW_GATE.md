# RRIF E4F return intake — sourcefree D02 repaired candidate; not adopted

**Checked 2026-11-01.** PREMAIN remains `8e44ca9c751049d65e6def47600b5c073ee04b29` in remote branch readback. Only RRIF; no PROGRAMMA action authorized.

## Exact object
E4F branch `agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1` exact returned `f2c0af3273d612bff0a7bd2407532b52caf4348b` above E1 `ffd03934d0a86c98ed095d973e45587bd5751013`, 1 commit; two production files and one 314-line new sourcefree test, plus five worker return docs. E4 independent prior review `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60` rejected uncorrected E1 D02 for actual pyreadstat pandas Timestamp being stringified.

Files E4F:
- `rawlsing_next/pre553_physical_decoder.py` blob `4b89c4598f324834de064c1200c63698a20e3c5c`;
- `rawlsing_next/pre553_r5_codec.py` blob `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7`;
- `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` blob `c07c2019455e6264b4297c1c1d782bd887b96bdd`.

Engineer reports real synthetic SAV+DTA pyreadstat Timestamp -> R5OpaqueValue `python.datetime.datetime@1` and `opaque` tag at historical pinned first R5 seam consumer, explicit aware subclass and one-item refusal, typed refusal of NaT/submicrosecond loss and incomparable missing ranges. E1 33 pass; new E4F 12 pass; combined selected 194 pass/1 skip. Preexisting G01 2 fail reproduced identically against PREMAIN and E4F. No native source/data/semantic/actor rights.

**HQ test-gate caveat:** historical `pre553_r5_seam.py` is not installed in E4F current source tree; sourcefree test loads verified historical Git object as an *actual test-executed historical consumer*. This is not evidence of current production importer. Independent re-review must establish correct scoped claim. Also specifically inspect nested two-or-more-level `.item()` chain falling through `_jsonable`, which itself recursively calls `.item()`: could an aware date-like value be stringified despite scoped one-level refusal? No blanket safety inference until reviewer adjudicates.

**Gate:** new exact independent E4FR review prepared `review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1` from PREMAIN; issue #601. E4F code not fan-in approved. E6 B5/M2 reviewer #597 and F0 receiving preflight #600 still no returned remote SHA at this check; do not infer process status. No protected PREMAIN write.

**Next:** E4FR accepts/fails precise E4F hunk; E6 independently resolves unchanged accepted-M2 foreign release fixture contract; F0 prepares the receiving allowlist/CAS. On actual receipt, HQ integrates only approved, exact code and tests or records named owner HOLD, then emits finite RRIF terminal ledger. **No PROGRAMMA until RRIF terminally closed and fresh user go-ahead.**

ENGINEERING: candidate corrected, independent review pending. SCIENTIFIC: source-native and meaning HELD. AUTHORITY: protected CAS/source/actor HELD.
