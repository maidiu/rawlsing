# ASTRA-D17 — STORAGE / EXECUTION COMPARISON — GOVERNED RETURN

Status: `BLOCKED__D17_LOCAL_RUNTIME_DEPENDENCY_ONLY`

Exact blocker:
`D17_BLOCK__FROZEN_DECODER_RUNTIME_PYREADSTAT_UNAVAILABLE`

Exact grain:
`C09_FROZEN_TWO_SOURCE_PARITY_FIRST_PHYSICAL_COMPARISON_ONLY`

Branch:
`agent/rabochii-prev3-astra-d17-physical-comparison-r1`

Commission tip:
`601225c16f92bf5cc24ee7d4aafd22c0b554dbb5`

## 1. Canonical HQ authority

Current canonical control-branch `HQ_HANDOFF/LATEST.json` resolved to:

- checkpoint: `20260915T1600-0400`
- handoff commit: `e2778f178cfbb47fdb59ec367a666efc95b9d1a5`
- semantic PRE-MAIN tip: `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

At that immutable checkpoint D17 is active at exactly this grain, with `EXACT_ONLY` Library access, `D17_LOCAL_ONLY` blocker effect, and hard forbiddances `WORKLOAD_SUBSTITUTION`, `ARCHITECTURE_RETIREMENT`, and `PROJECT_WIDE_RANKING`. D16 is already in the adopted PASS set.

The older branch-local copy of `LATEST.json` was not substituted for current control-branch authority.

## 2. Frozen semantic/execution identities preserved

Accepted D16 / qualified OP014 identities:

- D16 accepted return: `d6a49a6e3991701c3fbd9d2c5d52609823ad9360`
- OP014 program: `C09_HB05_OP014_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY_PROGRAM_R1`
- program payload SHA-256: `5ccdde46139acbc94b07afd23db62450b997deffbc094617e5a61010b3e853c8`
- accepted I05 engine Git blob: `b2b99460cc5991bc26aa2ffe5bda129b408fc197`
- accepted engine contract: `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0`
- qualified semantic candidate: `da1c728a4f25777090ed12e3740e268cce2a53ea`
- D16 evidence execution SHA: `50b64a8794d90908fcbe22288a7672ced4ac0c9d`
- D16 workflow run: `34817464330`
- D16 job: `104511796776`
- D16 artifact: `10412545756`

Frozen comparison spine:

- HB05 manifest payload SHA-256: `9c99ad778020edf5ed67f4da1f30e4eb14647d46535663a6f027bd04ef8417af`
- C09 measurement-law Git blob: `2729ab4dca887f22fb3c90265f10c70020afdd3e`
- C09 exact-order Git blob: `e200a9aed7dbdf103ab9306d0dd19b74662faf1b`
- qualified A/B/C intake SHA-256: `906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88`
- HB04 common-harness SHA-256: `138482116b566482075e191800229f81357541d674646552e8c269e7640a755e`
- current frozen decoder Git blob on D17 branch: `13aa733b511dc23e00bfcdf288c5b920e3f09983`

No OP014 redesign, primitive-only substitution, candidate-specific search budget, or post-outcome tuning occurred.

## 3. Exact source materializations

Only the two commission-authorized Library carriers were materialized.

### WVS7

- Library file id: `file_00000000386c820d8760e748b25ad7e1`
- Library version: `1`
- Library container: `WVS Wave 7.sav.zip`
- container SHA-256 observed locally: `ce92993a022edbe39823f4a95d3f33522179ce4f388e2de2c1778c4ae6f1059a`
- authoritative extracted payload: `WVS Wave 7.sav`
- extracted bytes: `185163494`
- extracted SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- frozen expected SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- source identity preflight: `PASS`

The ZIP also contained only a 312-byte `__MACOSX/._WVS Wave 7.sav` sidecar besides the authoritative SAV payload; it was not treated as source data.

### LiTS-I

- Library file id: `file_0000000036dc81f8b8b546e356590a03`
- Library version: `1`
- authoritative payload: `LITS-2006-data.dta`
- bytes: `139531180`
- observed SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- frozen expected SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- source identity preflight: `PASS`

No other Library retrieval or source substitution occurred.

## 4. Equal-work proof

The equal-work gate was preserved before any candidate measurement:

1. the exact two source identities match the HB05/C09 frozen proving sources;
2. the exact qualified OP014 program and accepted I05 engine remain unchanged;
3. OP014 requires the complete precompiled declared frontier, canonical candidate-hash order, `NONE_EXACT_EVALUATE_ALL`, no RNG, no pruning, and one terminal coverage receipt for every candidate;
4. the frozen C09 fairness law requires identical semantic requests and equivalent outputs/receipts before physical comparison;
5. the frozen HB05 manifest binds A/B/C to `IDENTICAL_LOGICAL_REQUEST__PHYSICAL_MECHANICS_MAY_DIFFER_ONLY_WHERE_EXPLICITLY_PERMITTED`;
6. D17 executed no candidate after the shared physical-decoder preflight failed, so no candidate received less work, warmer state, a surrogate primitive workload, or a different search frontier.

Disposition of equal-work proof:
`PASS__CONTRACT_AND_INPUT_PARITY_FROZEN__EXECUTION_NOT_REACHED`

This is deliberately not represented as performance parity or as a completed bakeoff.

## 5. Runtime preflight and smallest exact blocker

The frozen decoder path on the D17 branch is `rawlsing_next/pre553_physical_decoder.py`, Git blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`.

That decoder calls the accepted runtime dependency `pyreadstat` for both authoritative formats:

- WVS7: `decode_sav(source_path)`
- LiTS-I: `decode_dta(source_path, encoding="latin1")`

D17 execution surface:

- Python: `3.13.5`
- `pandas`: present
- `pyreadstat`: absent
- `pyarrow`: absent

A bounded attempt to install `pyreadstat==1.2.8` failed before installation because the execution container has no package-index network resolution (`Temporary failure in name resolution`). No alternate decoder was substituted.

The missing `pyarrow` is not promoted into an additional blocker because the first mandatory source-decoder boundary already fails on `pyreadstat`.

Smallest proved blocker:

`D17_BLOCK__FROZEN_DECODER_RUNTIME_PYREADSTAT_UNAVAILABLE`

This is a runtime-surface blocker only. It does not reopen D16, HB05/HB06/HB07, OP014 semantics, source identity, candidate definitions, MAIN, semantic PRE-MAIN, OBL063, or PRE-V3 person/V3 state.

## 6. D17 execution/run identities

D17 benchmark dispatch did not lawfully begin after the shared decoder preflight failed.

Therefore:

- D17 GitHub Actions run: `NONE__NOT_DISPATCHED`
- D17 job: `NONE__NOT_DISPATCHED`
- D17 benchmark artifact: `NONE__NOT_MINTED`
- candidate A execution: `NOT_STARTED`
- candidate B execution: `NOT_STARTED`
- candidate C execution: `NOT_STARTED`

Inherited D16 qualification run/job/artifact identities are recorded above only as the accepted gate proving the OP014 program was already independently qualified; they are not misreported as D17 performance execution.

## 7. Measurements

Lawful preflight measurements:

| item | measurement |
|---|---:|
| WVS7 authoritative SAV bytes | `185163494` |
| LiTS-I authoritative DTA bytes | `139531180` |
| WVS7 source SHA match | `PASS` |
| LiTS-I source SHA match | `PASS` |
| candidate physical timing | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| candidate peak RSS | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| candidate scratch | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| candidate persistent-byte delta | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| OP014 throughput | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| audit/replay time | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |
| cacheless rebuild time | `NOT_MEASURED__RUNTIME_BLOCKED_BEFORE_DISPATCH` |

No surrogate numbers were generated from pandas, primitive-only execution, old C09 results, fixtures, or prior source-backed certification runs.

## 8. Bounded comparison result

`NO_PHYSICAL_COMPARISON_RESULT__SHARED_FROZEN_DECODER_RUNTIME_UNAVAILABLE`

The only lawful conclusion is that the exact two sources and equal-work semantic contract preflight successfully, but this D17 execution surface cannot cross the shared frozen decoder boundary. Consequently there is no measured A/B/C physical ordering, no candidate disqualification on performance, no architecture retirement, and no project-wide ranking.

## 9. Successor / wake

D17 may be retried at the same exact grain once an execution surface can run the frozen `pyreadstat` decoder against these same exact source bytes. The retry must preserve the same OP014 payload/engine and frozen comparison identities unless HQ separately issues newer authority.

Current effect:
`BLOCKER_LOCAL_TO_D17__NO_OTHER_LANE_BLOCKED_BY_THIS_RETURN`

Terminal:
`ASTRA_D17_BLOCK__EXACT_SOURCES_AND_EQUAL_WORK_GATE_PASS__FROZEN_PYREADSTAT_RUNTIME_UNAVAILABLE`
