# C9-R3B source-bound recovery — actual GitHub Actions execution receipt

**Date:** 2026-10-28/29 UTC. **Evidence run** [40798932389](https://github.com/maidiu/rawlsing/actions/runs/40798932389) executed at `3eb4aeeab5c9a91d644449026b509169160f9b81`. **Grade:** `SOURCEFREE_TEST_ONLY__HISTORICAL_SOURCE_CUTS_SEPARATELY_ATTESTED__NO_NATIVE_OR_CAN_ADP_GRANT`. This document is an engineering record for draft PR #514, not product acceptance, current-Sorok HQ command, independent reviewer, or PRE-MAIN adoption.

## Source cuts and observed tests

| Source/consumer | Exact Git commit/source | Actually executed | Result |
|---|---|---|---|
| Current staged C9 writer and schemas | writer original `1e99681f58086f2784834df1186cfba71a2c50b9`; original code Git blobs enforced by `verify_recovered_source.py` | `verify_recovered_source.py --pytest` under separately checked-out old S36 and JOIN-E | **15 PASS, 0 SKIP, 0 FAIL**, JUnit gate `complete_proof:true` |
| Historical S36 receipt source (unaltered external checkout) | `8da78d8031a06a4bd7e1297fd713e573299c0860`, `WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1` | `test_c0_s36_seven_table_readset_is_unchanged` among above 15 | PASS, selected historical readset protected |
| Original writer-era JOIN-E C12 | `7bf2da302996491ddf34b9a039fea47ac982d135`, `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j` | three C12-dependent tests among 15 | PASS at original C12 semantics |
| Later reader-required repaired JOIN-E C12 | `68b058656254234f0af02df2a592aa6f8c6a8bd2`, entire `WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1` | `test_actor_fork_reader.py` with `C9_READER_SOURCE` and `C12_READER_SOURCE` env pointing to exact external source | **12 PASS**, 0 FAIL, 0 SKIP |
| Reader exact imported C12 source | SHA-256 hashes of `store.py`, `bp4/canon.py`, `bp1/canon.py`, `c12_integrity.py` | independent run diagnostic against `C12_SOURCE_HASHES`, before fork tests | **4 MATCH, 0 MISMATCH** |
| Existing portable suite, earlier CI | [40797111274](https://github.com/maidiu/rawlsing/actions/runs/40797111274) | C9 writer 11 PASS/4 SKIP; actor/dry/migration 40 PASS/1 DESELECTED | Scoped prior evidence. **Superseded for C9 writer by above no-skip court**, not a full historical V3 classification replay |

## Nontrivial version collision discovered by direct contrary tests

1. Original writer historical C12 JOIN-E `7bf2da3...` obtains **15/15 PASS** (run `40798932389` and initially `40798650310`). That C12 cut does **not** satisfy later `actor_reader.py` C12 hash contract: 12 fork-reader cases fail **before substantive assertion** with `C12_SOURCE_CHANGED_BEFORE_IMPORT` in run `40798650310`. This is a correct fail-closed source boundary.
2. Substituting repaired JOIN-E `68b0586...` as the **writer-era** source causes `test_c6_same_count_perception_substitution_is_held` to fail: historical assertion `len(perceptions(root)) == len(perceptions(child))` observes **2 != 3**. Run `40798810264`: 14 PASS, 1 FAIL. This is a real version-specific fork/perception distinction, not a missing library or CI noise.
3. Using **two explicitly pinned source checkouts**, old for historical writer court and later for reader/fork court, succeeds in bounded separate tests in `40798932389` (15/15 and 12/12). This is **not yet** a unified owner-selected single future C12 state version. Original tests are run at their intended source cuts; no test's expected value, error or source guard was deleted.
4. Therefore `SINGLE_CUT_REAL_PERFORMED_E2` remains **HOLD** until incumbent source owner resolves the perception/cold-fork semantic difference and independently proves one actual selected writer+reader+C12 external material E2 downstream. No reintroduction of obsolete initial C12 assumptions as an accidental migration invariant.

## Remaining original/current authority and proof obligations

- The original historical `v3/core/state.py` classification test remains **unexecuted** in portable runner because that source is referenced by an external Mac path and the exact SHA-256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` was not independently recovered into checkout. It was deliberately **deselected**, NOT passed or silently removed.
- Existing Rabochii Governed Bounded Court global `rawlsing_next` FIABC 144 PASS/3 FAIL at earlier staging cut is not part of the C9 suite. Unmodified PRE-MAIN baseline run required to allocate whether failures are preexisting; no canonical oracle was edited.
- No actual original Rule A/T, ADP event/actor issuer, SCI05 aftercall, native Pyat N11/N12/C11, real mother/B material life, or A5 human proof here; TEST_ONLY sourcefree code is the only validated grade.
- All actual historical Git cuts may be obtained from private repo in CI by checkout without knowing two Macs' absolute paths. The only source modifications in this staging are explicitly logged test portability, tightened self-comparison test, CI/harness/receipts. Original C9 writer B and R3 reader application code remain byte-identical to authors.
- Latest first adoption barrier for draft PR #514: current incumbent authorization, owner-specific single-cut requalification, independent I2 review, actually performed later E2 and eventually qualified CAN/ADP/Pyat human acceptance. **Do not merge due to 15+12 alone.**
