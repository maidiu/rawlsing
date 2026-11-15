# G1 — Exact source, owner and test contract

**Court:** PYAT J5 per-country many-operation reuse court, 2026-11-15
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-country-reuse-court-20261115`
**Branch:** `agent/pyat-country-reuse-court-20261115`
**Frozen base:** accepted S2-D `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`
**Accepted writer:** `b7b697b69f0acea12174937ee824c19ac34ac284`
**Grade:** `SOURCEFREE_TEST_ONLY`; author measurement, not G5 acceptance, not a production grant.

## 1. Custody and verified cuts

| Item | Exact value |
|---|---|
| Current HEAD | `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969` |
| Branch | `agent/pyat-country-reuse-court-20261115` |
| Accepted S2-D | `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969` |
| Accepted S2-C writer | `b7b697b69f0acea12174937ee824c19ac34ac284` |
| Accepted #1006 author evidence | `2beb2b894076510cdedf8981aa73d15eafc7c816` |
| Accepted #1006 code/test | `1ca1c735a577a7524a0a26c15df8879cd88704e3` |
| Accepted #1006 independent G5 | `3e0ed0794498506520ae62c997a5c852ac672061` |
| Corrected VOSKRES accounting | `7ebd363dedc36cdc34b3a6ef53e32603f291c84e` |
| Current runtime | Python 3.11.3; pyarrow 22.0.0; DuckDB 1.5.2; pyreadstat 1.3.2; NumPy 2.3.2; pandas 2.3.1 |

Production files were read-only. No production or accepted-test file was edited. The only writes are under `WORKER_RETURNS/PYAT_COUNTRY_REUSE_COURT_20261115/` and the disposable `.local-data/` estate scratch. The pre-existing deleted root files (`.gitignore`, `README.md`) were already deleted by the sparse worktree setup and were not touched.

## 2. Exact current production identities

`git hash-object` at the frozen HEAD:

| File | Git blob |
|---|---|
| `rawlsing_next/pre553_empirical_query.py` | `8885e637eb176946c8496671ff49ee70665b3bc6` |
| `rawlsing_next/_pre553_query_eval.py` | `9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920` |
| `rawlsing_next/pre553_direct_estate_i03.py` | `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e` |
| `rawlsing_next/pre553_saved_c11_admission.py` | `22749addc1fca5f0b90e12728847c390aafa7a84` |
| `rawlsing_next/pre553_carrier_execution.py` | `ad1164f21f5f7422a03a19b1b856636edb89cb03` |
| `rawlsing_next/pre553_source_direct_parquet_estate.py` | `0e4b34ce4973bb4d23b6105faea55b9056ecf373` |
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `rawlsing_next/pre553_c11_repository.py` | `c0cd4e835ceb8fe6c6025ebeb89e32223427f955` |
| `rawlsing_next/tests/test_pre553_i03_grouping.py` | `78683c4098f388eb72d686651b3282b9162e2ed2` |
| `rawlsing_next/tests/test_pre553_direct_estate_i03.py` | `970996b889e841d7e283b59ca245e9cac7594a55` |

The two decisive cold/grouped production blobs remain the accepted S2-D/native-reader blobs:
`pre553_direct_estate_i03.py` = `8b4d5ca2…` and `pre553_empirical_query.py` = `8885e637…`.

## 3. Accepted #1006 harness source reused via `git show`

The accepted author commit `2beb2b89…` was inspected with `git show`; the following test-only sources were extracted into `probe/` without changing their content:

| File | Blob |
|---|---|
| `WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/fixture_1006.py` | `1487ad233c871d973b2a64c9649c37f100c46832` |
| `WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/query_1006.py` | `5a15272043246e5293a51e2390adc038bd280e47` |
| `WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/instrument_1006.py` | `a7559deaef5fd9dc9ee6c4d3dc03466c1c971f48` |

The fixture is synthetic/sourcefree: 128 distinct respondents, 416 events, 640 routing facts, 128 weights, typed missing B, routed sparse D, repeated MR, A/B/C/D/MR, and complete 13-family Parquet emission through the accepted S2-C writer. It does not impersonate original35 or real country microdata.

The corrected VOSKRES accounting `7ebd363d…` was used only for the existing old→modern mapping: V550 per-country prefetch/harmonization and V550J prepared country substrate → `I03GroupedExecutionScope` + cold `DirectEstateI03Session` refusal. This court does not re-review the V551/V552/V553 science composition.

## 4. Exact existing cold saved capability

Lawful current call chain:

`SavedC11Admission.execute_i03` (`pre553_saved_c11_admission.py:424-445`)
→ `CarrierNeutralResearchExecutor.execute_i03` (`pre553_carrier_execution.py:442-490`)
→ `with DirectEstateI03Session(self.repository)` (a **new** session per operation)
→ `DirectEstateI03Session._build` (`pre553_direct_estate_i03.py:191-286`)
→ `indices_for` (`:380-414`)
→ `execute_empirical_query` (`pre553_empirical_query.py:734+`)
→ `_evaluate_index_group` / `_evaluate_index_group_core` (`_pre553_query_eval.py:404-...`, `:626-...`).

`SavedC11Admission.execute_i03` hard-codes `group_scope=None` at `pre553_saved_c11_admission.py:440`. The cold session builds a disposable SQLite posting index from every event-locator and event body row group, plus the required side-family row groups, then evaluates the exact I03 query. It does not build a full `C11Repository` or reopen the source.

## 5. Exact existing grouped capability

The lawful grouped path is `I03GroupedExecutionScope` (`pre553_empirical_query.py:490-731`):

- `_evaluate_index_group_core` computes the **measure-independent** exact core: routing/risk membership, condition truth, target cells, denominator members, used objects/authorities (`_pre553_query_eval.py:404-...`).
- `_materialize_grouped_evaluation` rebuilds the measure-specific weighted/raw cells and all per-operation fact/provenance/replay material (`:564-...`).
- `evaluate` revalidates exact identity/fingerprint/authority on every hit and falls back on any failure (`pre553_empirical_query.py:643-731`).
- `_core_key` excludes measure/weight/design but includes index identity, risk-set type, source-scope mode, response-state semantics, predicate identity, target plan, query authority refs and registry identity (`:592-627`). Therefore **only exact same-core measure variants (e.g. RAW vs GOVERNED_WEIGHTED) can share**. Different predicates or target plans do not share; the key is not a generic respondent-substrate cache.

The existing grouped path is only lawfully exercised on a sealed `C11Repository` index. The 16-test focused grouped suite `rawlsing_next/tests/test_pre553_i03_grouping.py` passes, including exact parity, measure sharing, capacity, special states, zero support, poisoned memo, authority deny, release separation and cleanup. `test_pre553_direct_estate_i03.py::test_cold_i03_rejects_grouped_cache_and_i05_outside_s2c_scope` also passes.

## 6. Exact cold refusal and missing reused-preparation identity boundary

Two public entry points refuse cold grouped execution before any grouped core is published:

1. `CarrierNeutralResearchExecutor.execute_i03`, `pre553_carrier_execution.py:464-466`:
   `CarrierExecutionBindingError("grouped saved I03 scope awaits distinct S2-D qualification")`
2. `execute_empirical_query`, `pre553_empirical_query.py:756-757`:
   `EmpiricalQueryExecutionError("grouped native I03 cache not yet qualified for cold sourcefree estate")`

Measured read-only diagnosis (no guard bypass, no grouped cache call):

- `DirectEstateI03Session._ReleaseIndex.release` is `_DirectReleaseIdentity` with only `release_ref` and `replay_manifest`.
- `I03GroupedExecutionScope._index_identity` (`pre553_empirical_query.py:562-582`) requires `release.semantic_release_hash`, `release.source_release_manifest_hash` and includes `id(index)`.
- The cold session's `indices_for` constructs a **new** `_ReleaseIndex` on every call (`pre553_direct_estate_i03.py:401-414`). Measured `same_index_object_across_two_calls = false`.
- Therefore the current cold saved estate does not expose a stable, exact grouped-core identity. Removing the guard would not by itself create lawful reuse; the operation would fall back because the key is neither complete nor stable. A versioned cold release/index identity and a lawful per-execution prepared-session contract are missing.

This is the exact legitimate reused-preparation identity boundary: **one source/wave/country saved estate is not yet one stable exact grouped-execution index across operations**. The barrier is a contract qualification, not a missing row or a merely slow path.

## 7. Explicit boundaries

- No production change, no guard removal, no 3-sort production patch.
- No new index/store/engine; no full-object reopen; no source reopen.
- No body-truth native edit (#999 successor still pending).
- No science/eligibility change; no original35 rights; no governed QUERY issuance (J3 remains separate).
- The 100 queries are TEST_ONLY sourcefree operations, not original governed issuance.
- Prior #1006 100k/10k locality numbers are cited only as prior accepted evidence; this court did not rerun them.
- No self-acceptance. G5 is pending a distinct reviewer.
