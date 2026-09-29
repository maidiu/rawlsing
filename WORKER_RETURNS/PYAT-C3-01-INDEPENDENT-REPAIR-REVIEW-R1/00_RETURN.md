# PYAT C3-01 — independent representation-repair acceptance review — R1

Status: `APPROVE_AT_DECLARED_GRAIN`

Reviewer branch: `agent/reviewer-pyat-hq126-c3-01-repair-acceptance-r1`

Commission tip: `2b7dd60cf220ccac0424501028587d48610177f9`

Exact reviewed C3-01 return: `d9462674d45f228b5985a5ce3158723b87ca6fa6`

## Holding

I independently approve **G01, D01 and D02 at their declared physical-representation grains only**.

- G01: `APPROVE_AT_DECLARED_GRAIN`
  - `EXACT_NINE_SURFACE_SAV_NATIVE_INT_RULE_TO_FLOAT64_PHYSICAL_REPRESENTATION_SUCCESSOR`
- D01: `APPROVE_AT_DECLARED_GRAIN`
  - `EXACT_SOURCE_SHA_PLUS_DECLARED_ENCODING_PHYSICAL_DECODER_ADMISSION`
- D02: `APPROVE_AT_DECLARED_GRAIN`
  - `EXPLICIT_OPAQUE_DECODER_NATIVE_NAIVE_DATE_TIME_CARRIER__REPRESENTATION_ONLY`

Overall: `APPROVE_AT_DECLARED_GRAIN`.

This review does **not** authorize semantic widening, source execution, historical-snapshot integration, whole-file decoder replacement, or C3-02 implementation outside the exact allowlist in `03_ALLOWLIST_REVIEW.json`.

## Independent review sequence

The controlling C3 execution/review law was read before the worker narrative. The worker's commission-to-return diff was then inspected independently.

From original C3-01 commission `afffba327286a3f49ce852409d520bf944efed3c` to reviewed return `d9462674d45f228b5985a5ce3158723b87ca6fa6`:

- 10 commits ahead;
- exactly 10 files changed;
- every changed file is under `WORKER_RETURNS/PYAT-C3-REPRESENTATION-REPAIR-ACCEPTANCE-R1/**`;
- no production code was modified by C3-01.

The accepted CLOSED35 representation audit remains the independent oracle. It freezes G01 as a nine-surface noncoercive physical-successor problem, D01 as exact-SHA declared-encoding physical admission debt, and D02 as opaque date/time physical-carrier debt. It does not authorize semantics.

## G01

The candidate at `8ed091e1323f46335a4bcbf6ab92ac9e3f228848` is bounded correctly.

The authority module requires exact source SHA + variable + ordinal and exact Python `int` native code. It enumerates only the nine accepted surfaces over sources 02, 06 and 21. It uses explicit float64 representation literals/R5 tokens and exact physical binding keys; it does not equate integer and float typed identity.

Hostile coverage rejects float/string/bool/Decimal substitutes, wrong source, variable, ordinal and code. The module itself names the relevant negative ceilings: no generic numeric coercion, no DTA applicability, no other source/variable/code, no label/display semantics, no missing-state reinterpretation, no cross-wave inheritance.

Disposition: `APPROVE_AT_DECLARED_GRAIN`.

## D01

The candidate at `f6613cbef8c23148c14d9464e9b6a869474a418f` admits exactly:

- source 08 SHA `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2` → `BIG5`;
- source 11 SHA `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2` → `WINDOWS-1252`;
- source 12 SHA `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec` → `WINDOWS-1252`.

Those SHA identities and declared encodings independently match the authoritative census receipts.

The implementation keeps this lane separate from compatibility-only decoding; rejects wrong SHA, wrong encoding, `auto`, `guess`, and `fallback`; leaves `encoding=None` unprivileged; and emits only `SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY`.

Disposition: `APPROVE_AT_DECLARED_GRAIN`.

## D02

The candidate at `e2d7674701e1b743dc513ce3bd525ee181bfda17` closes the exact observed physical-carrier defect without creating date/time meaning.

Only exact built-in naive `datetime.datetime`, `datetime.date`, and `datetime.time` receive deterministic opaque carriers. Timezone-aware datetime/time reject. Bare date/time still reject at the ordinary R5 codec boundary. Ordinary strings remain strings; int/float lanes remain distinct.

The current baseline already has `R5OpaqueValue`; the current codec parent is byte-identical to the historical D02 parent. The current decoder, however, differs from the historical decoder and must receive only the narrow `_physical_value` route. The current facade is byte-identical and needs no edit.

Disposition: `APPROVE_AT_DECLARED_GRAIN`.

## Fresh execution identity review

All four cited fresh source-free qualifications correspond to their exact execution commits.

| Court | Semantic candidate | Execution commit | Run | Job | Fresh result |
|---|---|---|---:|---:|---|
| G01 | `8ed091e...` | `a9069d0...` | 35884185279 | 109531459446 | protocol 20; governed 25 |
| D01 | `f6613cb...` | `4a19af8...` | 35883052865 | 109531476500 | protocol 20; governed 14 |
| D02 | `e2d7674...` | `76ce34c...` | 35883745809 | 109531487944 | protocol 20; governed 24 |
| combined | `3cefb4e...` | `3d6d45e...` | 35887617559 | 109531501528 | protocol 20; governed 42 |

For every run, GitHub reports success at the exact `head_sha`; the job log checks out that SHA and reports the same `RABOCHII_EVIDENCE_EXECUTION_SHA`. G01, D01 and combined have one court-spec-only commit above their semantic candidate. D02 has two commits above its semantic candidate, and **both** individually change only `.rabochii/court_spec.json`.

No raw survey source was executed by these courts.

## C3-02 allowlist ruling

The worker's **production** allowlist is accepted, with one reviewer tightening to the test layer.

The current baseline lacks both:

- `rawlsing_next/closed35_representation_census_harness.py`;
- the historical CLOSED35 qualified-census receipt tree consumed by the old G01 test.

Therefore C3-02 must not copy those historical dependencies into the current baseline merely to make historical tests runnable.

HQ may freeze the exact semantic-candidate allowlist in `03_ALLOWLIST_REVIEW.json`:

1. `rawlsing_next/closed35_g01_sav_numeric_representation_authority.py`
2. `rawlsing_next/pre553_physical_decoder.py`
3. `rawlsing_next/pre553_r5_codec.py`
4. `rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py` — **current-baseline port only; no historical receipt-tree dependency**
5. `rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py`
6. `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py` — **current-baseline port only; no historical census-harness dependency**

The current facade is explicitly **not** allowlisted for edit.

If the governed court route is used, a separate execution commit may alter only `.rabochii/court_spec.json` above the C3-02 semantic candidate; that execution metadata is not semantic implementation.

C3-02 must rerun the three current-ported repair tests together, the existing SAV representation and physical-metadata regressions, and `test_pre553_source_backed_c11_facade.py` against the exact current-baseline-derived port.

## Boundaries preserved

This review does not establish:

- raw-source executability today;
- semantic correctness of decoded text;
- date/time meaning;
- generic int/float equivalence;
- future-source applicability;
- source-wide PASS for sources 08, 11, 12 or 14;
- full CLOSED35 or F1 closure;
- C3-02 success before the current-baseline port is built and freshly qualified.

## Terminal

`C3_01_INDEPENDENT_REVIEW_COMPLETE`
