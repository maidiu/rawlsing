# PYAT HQ280 PV3 A04 — Source-free authorized workload binder CANDIDATE

**TERMINAL:** `HQ280_PV3_A04_REAL_CURRENT_OWNER_BINDER_CANDIDATE_MEASURED__SOURCEFREE_ONLY__GITHUB_PUSHED`
**RESULT:** `PASS__CANDIDATE_BUILDS_AND_RUNS_AGAINST_REAL_CURRENT_OWNERS__41_TARGETED_TESTS_PASS__17_OF_17_HOSTILES_DETECTED__SOURCEFREE_ONLY__NON_ISSUING`
**Branch:** `agent/rabochii-pyat-hq280-pv3-a04-sourcefree-authorized-binder-r1`
**Sealed startup SHA (verified before mutation):** `ce2d85a087aff43c45981e00ab822446d69daed9`
**Control:** HQ280 parallel seal `908ee4e74849884b1d4c2f532209a0ca57538b67`; inherited HQD-2026-10-10-280; canonical baseline `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).
**A05 oracle consulted:** `agent/rabochii-pyat-hq280-pv3-a05-independent-nodrop-oracle-r1` @ `9491d0296c95ee2942fe80eadc6aa9f54b07c634` (verified on remote; **contract read only, no code imported**).

## 1. What was built

Two NEW files. **No accepted production owner was edited** (verified: `git diff HEAD` empty; owner blobs in §6).

| File | Blob | Lines | Role |
|---|---|---|---|
| `rawlsing_next/pre553_original_workload_binder_candidate.py` | `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5` | 1154 | the binder candidate |
| `rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py` | `6c06a5b013d3713af7d7ba9bf143c3ef7a6245a2` | 961 | 41 tests |

The binder is a **data-only binder**, not an issuer and not a replacement engine. It binds an *independently declared, source-scoped expected-work preimage* onto the real owners, using only already-implemented factories.

## 2. Real owner APIs actually used (introspected signatures)

| Stage | Real owner call | Introspected signature |
|---|---|---|
| Projection | `bind_governed_c11_projection` | `(projection_fields: Mapping[str, Any]) -> GovernedC11Projection` |
| Catalog | `RuntimeObjectCatalog` | `(authorities, predicates, queries, discovery_authorities)`; `resolve_query_exact` / `resolve_predicate_exact` / `resolve_discovery_authority_exact` |
| I03 request | `I03ExecutionRequest` | `(query_ref: ExactRef, predicate_ref: ExactRef)`; `.request_identity` |
| I05 | `DiscoveryAuthority` via the catalog | `execute_exact_bounded_discovery(*, repository, discovery_authority, authority_registry, release_refs, predicate_catalog, query_template_catalog)` |
| Compositor | `execute_route_b_production` | `(*, source, projection, runtime_catalog, i03_requests, discovery_authority_ref, cache=None, batch_size=10000)` |
| Batch | `BatchUnitSpec` / `BatchManifest` / `BatchExecutionRunner` | `(job_kind, job_ref, release_refs, semantic_input_refs=())`; `.run(*, executors, max_units=None)` |

No scheduler, engine or manifest planner was invented. The binder emits owner inputs; the owners still do all semantic work.

## 3. Genuine positive run (actual measured output)

Executed on an honest **synthetic source-free** fixture reused from the accepted Route B test corpus (`rawlsing_next/tests/test_pre553_route_b_production.py::_fixture`) — 4 respondents, items X/Y/O/R, 3 physical rows. **No raw SAV/DTA was read.**

```
PYTHONPATH=. python3 repro/a04_sourcefree_binder_repro.py
```

- expected frontier ref hash: `76bd0a91f8ab17a1c1c4ec08cc9c4dfbde973d3ccbd60386fa5bf01e8d326983`
- sealed C11 release ref: `95de34f09fa9ae4aac6c6a3c73ea7ff9dff5ef18189bac940805f30126fce88c`
- batch manifest hash: `db9e029e36489d390e07ab36eba43dd3f92d04b6be59c642230118263b7622f3`
- Route B dependency root: `db804020ef4d4577ff1eac590a0c9531fd812be3bded56aae36d5c69fdac6eaa`
- I03: **5 queries executed**, real `EmpiricalFact` typed states produced
- I05: **1 candidate, 1 covered**, typed state `DISCOVERED_RESULT_SUPPORTED`
- Batch: `COMPLETED`, `FULL_MANIFEST_COVERAGE`, **6/6 units**, 6 real execution receipts
- Reconciliation: **ok=True**, 6 expected keys, 6 job keys, 0 omitted, 0 extra

**Effects, both layers:** binder emits 8 false-effect flags and Route B's own replay receipt independently reports all 6 of its effects false. No structural, causal, model, publication, currentness or actor effect.

## 4. Five identity kinds kept distinct

| Kind | Basis |
|---|---|
| `documentary_item_key` | source + wave + item + form + slot |
| `operation_key` | op_class + roles + target + **condition_order** + **measure_kind** |
| `expected_work_key` | item + operation + source identity + authority + risk + topology + consumer + **explicit version** |
| execution attempt | `execution_attempt_key(expected_work_key, attempt_index)` |
| produced output | `output_identity(expected_work_key, result_type, value)` |

The expectation is hashed **before any owner is invoked**, and reconciliation is an **outer join**, so an expected operation with no constructed job stays visible instead of vanishing.

## 5. Hostile court — 17/17 detected, 4/4 controls pass

`repro/a04_sourcefree_runs.json` records every case with its real observed verdict.

| # | hostile | observed |
|---|---|---|
| H1 | A-only submission, A+B independently expected | FAIL `EXPECTED_OPERATION_OMITTED` |
| H2 | missing B | FAIL `EXPECTED_OPERATION_OMITTED` |
| H3 | missing J2 joint | FAIL `EXPECTED_OPERATION_OMITTED` |
| H4 | missing B **and** J2 together | FAIL `EXPECTED_OPERATION_OMITTED` |
| H5 | unauthorized extra work | FAIL `UNAUTHORIZED_EXTRA_JOB` |
| H6 | **same count, different keys** | FAIL `EXPECTED_OPERATION_OMITTED` + `UNAUTHORIZED_EXTRA_JOB` |
| H7 | condition-order substitution q(C\|A) vs q(C\|A,B) | FAIL both omission and extra |
| H8 | candidate own-`_dk` co-topic fake joint | FAIL `CANDIDATE_OWN_DK_JOINT` |
| H9 | altered document version | FAIL `EXPECTED_OPERATION_OMITTED` |
| H10 | source identity mismatch | FAIL `SOURCE_IDENTITY_MISMATCH` |
| H11a | post-result laundering **self-certified** | **PASS — deliberately** (see below) |
| H11b | same execution vs the frozen universe | FAIL `EXPECTED_OPERATION_OMITTED` |
| H12 | required consumer omitted, every job present | FAIL `REQUIRED_CONSUMER_OMITTED` |
| H13 | held/denied/NA removed entirely | FAIL `HELD_OR_DENIED_WORK_NOT_VISIBLE` |
| H14 | duplicate semantic job | FAIL at bind time |
| H15 | multiplicity without justification | FAIL at bind time |
| H16 | undeclared authority | FAIL at bind time |
| H17 | missing I05 expected work | FAIL at bind time |
| P0/P1/P2 | honest submission / stable reorder / restart identity | **PASS** |

**H11a is the decisive court.** The truncated manifest reconciled *against itself* shows **zero omissions** — it self-certifies. The identical execution reconciled against the independently frozen universe shows **4 omitted operations**. That gap is the measured proof that manifest self-certification is not no-drop evidence.

## 6. Owner integrity

`pre553_route_b_production.py` blob is `2385cd327dced3c5b887b59085aa0d21b04d78c3` — **identical to E18** in the HQ280 evidence ledger. `pre553_discovery_exact.py` is `905f24d114419dbdd93879ad2bee5b59dd2f23af` — **identical to E19**. No owner file was modified; `git diff HEAD` against the sealed startup is empty.

## 7. Two real defects found and fixed during binding

These were **found by running**, not by inspection:

1. **Measure kind was not identity-bearing.** RAW and GOVERNED_WEIGHTED on the same administered item collided on one `expected_work_key`. Fixed by making `measure_kind` part of the operation grammar.
2. **Declared condition order was unverified.** A caller could relabel q(C\|A) as q(C\|A,B) without changing the executed query. Fixed by requiring the declared `condition_order` to equal the **issued owner's own exact semantic target order**.

## 8. A05 compatibility (contract only, no derivation)

`A05_COMPATIBLE_SCHEMA_VERSION = "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"` is recorded as a **declarative token**. A04 imports **nothing** from A05 (`test_binder_does_not_import_or_depend_on_the_a05_oracle` asserts the import surface contains no `a05`), and A04's expected universe is declared **documentarily before any manifest exists** — never derived from its own generated workload or from A05's fixture. The failure vocabulary matches A05's published codes.

## 9. Unresolved — repository-wide suite: INCONCLUSIVE

Per HQ direction, the repository-wide regression investigation was **stopped**. A partial full-suite run was observed to report failures, but **the baseline worktree was not demonstrably comparable**, so **I do NOT claim those failures are proven pre-existing and I do NOT claim they are caused by this change.** Recorded as **INCONCLUSIVE**.

What *is* proven: the 6 directly-relevant suites pass together — **118 passed** (`route_b_production`, `batch_runner`, `discovery_exact`, `empirical_query`, `carrier_execution`, plus A04's own 41).

**Exact command:**
```
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py -q
→ 118 passed in 6.88s
```
```
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q
→ 41 passed
```
Environment: Python 3.11.3, `.pv3-venv`, macOS-13.7.8-x86_64, pytest 9.1.1. Three consecutive runs byte-identical (deterministic).

## 10. Ceilings

Source-free development only. No original-source read, no raw SAV/DTA, no all-35 scientific eligibility claim, no new model permission, no G0b/EE12, no operative publication, no canonical mutation, no self-adoption, no branch merge. WGC 78,037 annotations, WGD 81,179 keys and WGE retrospective CONTEXT replay are **not** treated as ready workloads. This is a development-grade binder candidate; adopting its frontier for any real slice remains a competent owner's act.

**Terminal:** `HQ280_PV3_A04_REAL_CURRENT_OWNER_BINDER_CANDIDATE_MEASURED__SOURCEFREE_ONLY__GITHUB_PUSHED`.