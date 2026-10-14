# 04 — implementation, pinned blobs, and real execution record

## 1. What was implemented (sourcefree, return terrain only)

```
port/
  contracts.py       two contract identities (GENERIC_WORLD_SELECTION@1.0.0,
                     GENERIC_ORDERED_POSSIBILITY@1.0.0) + transport-only facade;
                     semantic/possibility/consumer projections and conserved-field
                     comparison; allowed-provider-variant vs not-normalizable lists
  world_baseline.py  maximal-distinction invented municipal-2008 value-bearing world
                     (AH, native strata, n-ary triad, F2 predicate/history, four+
                     clock axes, public categories/sanctions, negative algebra,
                     contradictory alternatives, route VALUES, generated-binding echo)
  provider_a.py      Provider A — single tagged object map (tuple-store), stages
                     stage_one/stage_two, independent construction
  provider_b.py      Provider B — normalized rows, split temporal/n-ary tables,
                     shuffled record order, stages renamed_data/join_index
  world_laws.py      signature-ordered structural conservation laws mapping 1:1 to
                     the 28 frozen K10 classes; freshness law for the two H2 refresh
                     channels; frozen classes loaded FROM the pinned oracle file
  consumers.py       CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY (finite scenario) and
                     NONPARENT_APPRENTICESHIP_ENTRY (nonparent), each ACTUALLY reading
                     selected world VALUES with a values-read receipt
  adapter.py         TwoContractAdapter: two distinct tagged receipts + strictly
                     lossless reversible round-trip; provider-equivalence reporter
  test_k9_provider_swap.py         8 frozen K9 cases
  test_k10_structural_conservation.py  28 frozen K10 mutations
```

No non-equivalent/missing-value provider is normalized: K9_04 variants are rejected by the same laws that accept A/B equivalence.

## 2. Pinned blobs and verified import locations

Staging manifest (all `git hash-object` SHA-1 verified against pinned preimages, actual NUL `blob <len>\0` header): `staging/staging_manifest.json` — 27 entries, `all_match: true`.

Key pins:

| Object | Git blob SHA-1 | Source commit | Staged path |
|---|---|---|---|
| C1 composition | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` | `7f29aec36d24f16da52d84f17c00f08db3a55434` | `staging/ns/rawlsing_next/pre553_analytical_composition.py` |
| N10E provider | `23167aa25291fb148b1e3cf210ac33fe7769b783` | `7f29aec36d24f16da52d84f17c00f08db3a55434` | `staging/ns/rawlsing_next/pre553_empirical_possibility_provider.py` |
| PE candidate | `58484f4c3d9aae148d4116dcf00420c432aefcbd` | `b497f85713847cecc169d4d71c7629655d562dc0` | `staging/ns/rawlsing_next/pre553_postastra_pe_generic_world_possibility.py` |
| PE fixture | `c9674d5fe9d01621eda0fdb4a999391eba422d92` | `b497f8571…` | `staging/ns/rawlsing_next/tests/test_postastra_pe_fixture.py` |
| PE 21-test module | `92f59875583bf513c6fdbcd3ad7fe2b49e45e212` | `b497f8571…` | `staging/ns/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py` |
| HQ297 reviewer 13-test module | `d2fe653dadf94893b0fdfd268f36683f8dfed9af` | `4fb21a8108d29f4c820326204bfcfee41500788c` | `staging/ns/rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py` |
| N10E fixture | `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a` | `7f29aec36…` | `staging/ns/rawlsing_next/tests/n10e_empirical_slice_fixture.py` |
| K9 oracle (frozen) | `9ccb66f9b08a4aa8b96582295bb2966d250fd72d` | `241d35fa8a13ea03c68fbe55554ce81c210b745f` | `oracles/02_K9_PROVIDER_SWAP_ORACLES.json` |
| K10 oracle (frozen) | `e78b3ee91da1fb18deaf8d8f226800ad855adbae` | `241d35fa…` | `oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json` |
| Two-contract envelope | `610ac870fde6cfe63796592b3c6b1e1bf1e37150` | `241d35fa…` | `oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json` |

Live in-tree owners verified by exact import `module.__file__` (not staged): `m4_v557_v558_publication_repository.py` blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`; `m5_runtime_rsc_peer_prior.py` blob `18735bdb31a220aed032aa722574d685e2bdddf5`; `source_backed_positioned_subject_possibility.py` blob `62e5eced47b64512f47b004e3e13a6ef3fe21de7` — matching the SC0 owner-binding pins exactly.

Namespace staging: `conftest.py` + `PYTHONPATH` add `staging/ns` (and `staging/ns/rawlsing_next/tests`) so staged owners import as `rawlsing_next.*` with **zero owner file mutation**; the staged set is disjoint from the live tree (no shadowing).

## 3. Real commands and observed results

Battery driver: `bash repro/run_battery.sh` (exact commands + raw logs retained under `repro/`).

| Step | Command | JUnit | Result |
|---|---|---|---|
| earliest discriminating port tests | `pytest port/test_k9_provider_swap.py::test_k9_01_two_providers_same_meaning port/test_k10_structural_conservation.py::test_k10_03_dyadize_nary` (executed inside [1]) | `repro/port_k9_k10.junit.xml` | A/B swap equivalence PASS + hostile dyadize mutation detected with frozen class |
| [1] port K9 8 + K10 28 | `python3 -m pytest port/ -q --junitxml=repro/port_k9_k10.junit.xml` | `repro/port_k9_k10.junit.xml` | **36 passed in 0.22s** |
| [2] N10E 43 + C1 13 | `python3 -m pytest staging/ns/.../test_pre553_empirical_possibility_provider.py staging/ns/.../test_pre553_analytical_composition.py` | `repro/n10e_c1.junit.xml` | **56 passed in 20.34s** |
| [3] PE author 21 | `python3 -m pytest staging/ns/.../test_postastra_pe_generic_world_possibility.py` | `repro/pe_21.junit.xml` | **21 passed in 2.18s** |
| [4] HQ297 reviewer 13 | `python3 -m pytest staging/ns/.../test_hq297_k9k10_sc0_pe_independent.py` (env `HQ297_EXACT_PE_ROOT=staging/ns`, PE blob gate passed) | `repro/reviewer_13.junit.xml` | **4 passed, 9 failed** — executed PE REDs (see below) |

## 4. The 9 reviewer REDs are findings against the PE candidate, not against the port

Each failure is an executed confirmation of a gap the HQ297 review found statically:

| Reviewer test | Observed | Meaning |
|---|---|---|
| `test_strict_reverse_scoped_issuer_forgery_must_refuse` | `STATIC_EXPECTED_FAILURE__PE_ACCEPTS_ANY_NON_NULL_REVERSAL_AUTHORITY` | PE shape-checks any non-null reversal ref; my port dereferences issuer/target/risk/denominator and refuses forged grants (K9_06 PASS) |
| `test_strict_selected_world_nary_F2_AH_strata_roundtrip` | `SC0_REQUIRED_N9_VALUE_ABSENT:absolute_horizon` | PE carries no value-bearing N9 selection (my port does; K10_01/02/03 PASS) |
| `test_strict_generated_runtime_fact_echo_not_source_promotion` | `KeyError: binding_echo` | no H3 echo slot in PE |
| `test_strict_two_distinct_world_refresh_receipts` | `KeyError: structural_publication_refresh_receipt` | no dual H2 refresh channel in PE |
| `test_strict_four_clocks_historical_knowledge` | `KeyError: clocks` | no four-clock axes in PE |
| `test_strict_negative_status_algebra_and_source_risk` | `KeyError: scoped_status_rows` | no negative algebra in PE |
| `test_strict_values_read_not_only_hash_or_inferred_label` | `KeyError: n9_values_read_receipt` | PE proves refs, not values-read |
| `test_strict_nonparent_apprenticeship_world_effect` | `KeyError: generic_consumers` | no generic consumer effects in PE |
| `test_strict_parent_scenario_remains_input_only` | `KeyError: generic_consumers` | idem |

The 4 reviewer PASSes are PE's genuine positive edges: multi-condition N100/N110 + null control, nonparent reverse with own denominator, world-ref-change is carry-only, invalidated snapshot refusal.

## 5. Reused evidence honesty

- PE2's own "21/21 + 373 owner regression" and HQ297 K9E's "36/36 fixture helper" are **fixture/helper passes**; they are NOT cited here as port execution. What is newly executed here: the K9 8 + K10 28 **against the two-contract port** (36/36) and the previously unreachable 13+21+43 families (now 4+9/13 executed, 21/21, 56/56).
- Fixture data closure (C1 authority freeze JSONs, AT07 successor spine JSONs) staged blob-verified; no fixture bytes altered.
