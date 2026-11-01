# FIRST CONSUMER AND TESTS

**Rule used:** an exact blob is not a consumer; a static import is not a proved live consumer. “UNKNOWN” is recorded rather than invented.

## Consumer table

| Lineage | Current first consumer | Kind | What it actually consumes | Status |
|---|---|---|---|---|
| **B5_OWNER_TRUST** | `rawlsing_next/pre553_learned_world_composition.py:33/40` | production import | accepted `pre553_learned_product_lifecycle` and `pre553_learned_product_release` owners | **B5 candidate has no consumer.** Accepted owners are consumed; mandatory ingress/issuer is not present. |
| **EE14_G1_OWNER_INGRESS** | `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py:57` | test import only | current HQ268 owner-only C1/G2/F8 ingress | **No production consumer.** Test-only owner-internal candidate. |
| **R56_SOURCE_NATIVE_ADAPTER** | `rawlsing_next/pre553_native_workload_binding.py:50`; `rawlsing_next/pre553_universal_workload.py:23` | production imports | `NativePreimageBundle` and source-native preimage material | **Current exact adapter consumed.** Test consumer `test_universal_source_projection.py`. |
| **R157_SOURCE_CONFIGURATION** | none found | — | historical `source_configuration/cli.py` entrypoint only | **No current consumer.** PRE-MAIN has no `source_configuration` directory. |
| **SRC04_EMPIRICAL_QUERY** | `rawlsing_next/pre553_carrier_execution.py:57`; `pre553_analytical_composition.py:26`; `pre553_discovery_exact.py:37`; others | production imports | current `execute_empirical_query` / query core | **Current query core consumed. `pre553_observed_response.py` has no current consumer and is absent.** |
| **S00D_VALUE_QUARANTINE** | none found | — | historical `s00d_producer_binding_quarantine.py` | **No current consumer; dependency `r3_s02_seam_witness.py` absent.** |

## Static path probe

Command:

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-d2-source-ingress-custody-20261031-r1
PYTHONPATH=. python3 WORKER_RETURNS/PYAT_RRIF_D2_20261031_R1/probes/lineage_state_probe.py
```

Result (summary):

```text
LIN-B5_OWNER_TRUST             paths 13 present 0 absent 13
LIN-EE14_G1_OWNER_INGRESS      paths  1 present 1 absent  0
LIN-R157_SOURCE_CONFIGURATION  paths 19 present 0 absent 19
LIN-R56_SOURCE_NATIVE_ADAPTER  paths  1 present 1 absent  0
LIN-S00D_VALUE_QUARANTINE      paths  1 present 0 absent  1
LIN-SRC04_EMPIRICAL_QUERY      paths  5 present 4 absent  1
```

The full per-path JSON also records the current Git blob and disk SHA-256; see `probes/lineage_state_probe.py` output when run.

## Test runs actually executed (current PRE-MAIN only)

All runs used Python 3.11.3, pytest 9.0.2, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.`, and `-p no:cacheprovider`. No branch candidate code was imported or executed.

| Court | Command (abridged) | Result |
|---|---|---|
| B5/M2 accepted owners | `pytest -q rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py` | **67 passed** |
| R56 current adapter | `pytest -q rawlsing_next/tests/test_universal_source_projection.py` | **31 passed** |
| SRC04 current query core | `pytest -q rawlsing_next/tests/test_pre553_empirical_query.py` | **32 passed** |
| EE14 current ingress | `pytest -q rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py` | **96 passed** |
| EE14 focused wrong source/authority/denominator | `pytest -q .../test_pre553_ee14... -k 'f3_denominator_substitution or f3_authority_substitution or f1_real_binder_refuses_substituted_release or positive_control_rejects_the_query_snapshot_substitute'` | **4 passed, 92 deselected** |
| R56 focused normalized collisions / missingness / mutation | `pytest -q .../test_universal_source_projection.py -k 'r02v_normalized_duplicate_respondent_key or r02v_ambiguous_normalized_source_key or mutation_flips or s3_missingness'` | **4 passed, 27 deselected** |
| SRC04 focused weight/denominator/observed-zero | `pytest -q .../test_pre553_empirical_query.py -k 'raw_and_authorized_weighted_measure or missing_or_invalid_weight or observed_zero_is_not_zero_support or equal_denominator_counts'` | **4 passed, 28 deselected** |

**Total full-suite current PRE-MAIN tests executed: 226 passed, 0 failed.** Focused subsets above are not added to that total.

## What the tests establish

- **B5/M2:** accepted lifecycle/release owners behave as tested, including currentness, historical as-of, withdrawal, checkpoint replay and unknown-currentness refusal. They do **not** establish mandatory ingress, issuer, separate principal or external expectation root.
- **EE14:** current HQ268 ingress runs the accepted C1→applicability→G2→bound F8 chain. The 96-test court includes wrong source, query-snapshot substitute, wrong authority, provenance substitution, denominator substitution and forged composed identity. No production consumer or native grant is claimed.
- **R56:** current exact adapter refuses normalized duplicate respondent keys and ambiguous normalized source keys before C11/I03; missingness is typed; mutation flips the same assertion and fresh restore returns baseline. The R02V-R2 independent requalification accepted this affected repair.
- **SRC04:** current query core distinguishes eligible denominator, raw vs authorized weighted measure, observed zero vs zero support, and equal denominator counts with different risk-member sets. It does **not** carry the absent observed/co-observed response contract; a recorded response is not treated as a denominator or population estimate in these tests.
- **R157/S00D:** no current test execution because no current path/dependency/consumer exists. This is recorded as absence, not as a pass.

## Unavailable reviews

At this cut, the sealed review branches for #564/#565/#569–#571/#575–#579 were still at their dispatch SHAs (no returned review). #577’s unchanged remote does not prove the worker is idle. #580–#584 remain held. No review return from those branches was used as a decision.
