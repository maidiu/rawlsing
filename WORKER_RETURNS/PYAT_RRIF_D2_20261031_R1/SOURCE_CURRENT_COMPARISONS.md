# SOURCE — CURRENT COMPARISONS

**Canonical PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**RRIF-C lineage reduction:** `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`
**RRIF-V hostile A×B:** `bec050449f0b38606718e4e9691caa1721fcd94f`
**A source location:** `84182f9fa7044d67689ea4f80eabf7e9337f15c2`
**B decision ledger:** `59e6e62600814d82cfefd1a2137b7aa63316bc95`
**A×B HQ crossjoin:** `f5a9facd189af6756c2b15c8daebe680016f658a`
**E8 functional disposition:** `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`

This comparison uses the six RRIF-C lineage rows and the exact historical cuts named there/on the branches. It does **not** recount the 845-branch estate. It independently checks only the paths introduced by each of the six lineages against current PRE-MAIN.

## 1. Six-lineage path comparison

| Lineage | Historical source cut | RRIF-C reported | Independent PRE-MAIN check | Current owner / consumer |
|---|---|---|---|---|
| **B5_OWNER_TRUST** | N04 root `b5a6b6409`; C02J `8959803`; C02H `82309fe`; C02E `20213bef` | 14 branches, 8 code-introducing, 7 signatures; 0 exact / 1 modified / 13 absent | **0 exact / 0 modified / 13 absent**. The RRIF-C “modified” path `rawlsing_next/repro/b5_mandatory_patch.py` is absent at PRE-MAIN. | Accepted B5/M2 owners `pre553_learned_product_lifecycle.py` and `pre553_learned_product_release.py`; consumed by `pre553_learned_world_composition.py`. No mandatory/issuer candidate and no candidate consumer. |
| **EE14_G1_OWNER_INGRESS** | HQ262 `22cd4976`; HQ266 `bdc65ff8`; HQ268 `f10523e1` | 5 branches, 3 code-introducing, 3 signatures; 0 exact / 1 modified / 0 absent | **0 exact / 1 modified / 0 absent**. Current blob `74e6ee82` is HQ268 (historical `e1c09957`); +923/−127, real C1→applicability→G2→F8 chain and D1/D2 completeness. | Current file present; only test import `test_pre553_ee14...`; no production import. |
| **R56_SOURCE_NATIVE_ADAPTER** | R02 `6f4be338`; R02V review `a287674b`; R02V-R2 `e1f0aeb6`; C1 `a5489365` | 11 branches, 3 code-introducing, 2 signatures; 1 exact + 1 modified variant | **1 exact / 0 modified / 0 absent**. Current blob `a6299c1a` equals the R02 repair/C1 qualification. The review branch variant `2d83cea` is not PRE-MAIN. | Production imports in `pre553_native_workload_binding.py` and `pre553_universal_workload.py`; test consumer `test_universal_source_projection.py`. |
| **R157_SOURCE_CONFIGURATION** | Final review `d81bc2c67`; foundation `519355ec`; integration `056849e2`; LITS `c868cc73`; source handoff `6be64d7e` | 23 branches, 5 code-introducing, 3 signatures; RRIF-C says 0 exact / 2 modified / 17 absent and prose says 4 exact / 6 modified / 24 absent | **0 exact / 0 modified / 19 absent**. No `rawlsing_next/source_configuration/` directory and no `pre553_source_read_admission.py` at PRE-MAIN. The RRIF-C “2 modified” paths are not present; its 4/6/24 prose is not reproduced. | No current consumer. Historical `cli.py` is an entrypoint only. |
| **SRC04_EMPIRICAL_QUERY** | Observed empirical `b6be4058`; actual carrier review `751fece9`; CD native review `9b66083f`; consumers `39c713a1` | 4 branches, 4 code-introducing, 3 signatures; 0 exact / 4 modified / 1 absent | **0 exact / 4 modified / 1 absent**. `_pre553_query_common.py`, `_pre553_query_eval.py`, `_pre553_query_predicate.py`, `pre553_empirical_query.py` are modified/refactored successors; `pre553_observed_response.py` is absent. | Query core has production imports (`pre553_carrier_execution.py`, `pre553_analytical_composition.py`, `pre553_discovery_exact.py`, and others). Observed-response extension has no current consumer. |
| **S00D_VALUE_QUARANTINE** | HQ285 S00D `4c8168b7` | 1 branch, 1 code-introducing, 1 signature; 0 exact / 0 modified / 1 absent | **0 exact / 0 modified / 1 absent**. `rawlsing_next/s00d_producer_binding_quarantine.py` is absent; its `r3_s02_seam_witness.py` dependency is also absent at PRE-MAIN. | No current consumer. |

## 2. Exact current blobs for the retained paths

| Path | Current blob | Historical blob | Status |
|---|---|---|---|
| `rawlsing_next/pre553_learned_product_lifecycle.py` | `a11c9eb73abab9be118ef4f0b6e325e676059f27` | n/a (accepted owner) | accepted B5 owner |
| `rawlsing_next/pre553_learned_product_release.py` | `f76c390665f06ef126968ccf1a6b2d816f43ae92` | n/a (accepted owner) | accepted M2 owner |
| `rawlsing_next/pre553_learned_world_composition.py` | `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` | n/a | B5/M2 consumer |
| `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py` | `74e6ee826e8b6a2adebe84969fedcea5716d5b63` | `e1c09957519f10b29ae2635f3277b4f3af0912c9` | HQ268 successor, test-only |
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` | exact current |
| `rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` | n/a | production importer |
| `rawlsing_next/pre553_universal_workload.py` | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` | n/a | production importer |
| `rawlsing_next/_pre553_query_common.py` | `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92` | `a2e8e9a99a4ec67d349a00204ffb1ad68dfd0220` | modified query core |
| `rawlsing_next/_pre553_query_eval.py` | `f808dfcd2008cc71e9203de3cadf1abe14223974` | `bfc6be969adf71b0bedf491a62ff6a50160accb3` | modified query core |
| `rawlsing_next/_pre553_query_predicate.py` | `8590bacf464b2c61f319f581820a3af76ed1e60c` | `17dde8bdf93c773bc8a472aa33e75d593b1009a6` | modified query core |
| `rawlsing_next/pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` | `0453f92c312cce488f8e86f96d1c9ecbd135ce12` | modified query core |
| `rawlsing_next/pre553_observed_response.py` | absent | `7f3ed06988888eba1c01b9d99d182f0796e922dd` | unique extension absent |
| `rawlsing_next/s00d_producer_binding_quarantine.py` | absent | `8df44663ad2e79634f15f805ea9f53c74aef99d5` | branch-only module absent |

## 3. RRIF-V corrections applied

These are used as constraints, not as a new census:

- A’s **2,269 “current source subtraction” is rejected**. It included **1,333 branch-only exact implementations** that are not PRE-MAIN integration; only **199 same-path exact** records are current source-identity evidence.
- A’s **291 exact-other-path** matches are source-copy/fixture-related (11 AT07 `INPUTS/*_law.py`/fixture copies, 65 test/fixture targets), not runtime/ABI equivalence. They require owner/path/ABI/consumer review.
- B’s **155 is branch rows, not 155 unique decisions**: 155 rows / 122 unique primary IDs / 135 decision records / 151 fate-classified / 4 unclassified / 5 `HQ_OTHER`. Multi-subject decision IDs are not separate acceptances.
- `CKPT-20261009-HQ274` is **documentary intake with candidate NOT_ADOPTED**, not code acceptance.
- The 45 exact-present / 276 stranded split is branch-location triage, not unique implementation or consumer proof.
- E8 mechanical `RETIRE`/`HOLD_EXACT_DECISION` labels were **not** used as authentic decisions in this return.

## 4. What this comparison does not prove

- Exact blob identity is not behavioral or semantic equivalence.
- A static import is not a proved live consumer.
- Absence at `8e44` is not a global absence claim; a renamed/rewritten successor may exist.
- No raw survey, original U/E_pre, native source, CAN/ADP/SCI05, Pyat N11/N12 or C11 authority was accessed.
