# R10 PV2 — Original-scope identity and prospectively frozen E_pre binding

**Repository:** `maidiu/rawlsing` (private) · **Platform:** OpenCode · Kimi K2.7 Code
**Branch:** `agent/userdirect-pyat-20261015-r10-pv2-original-expected-scope-binding-r1`
**Exact sealed startup:** `ebf12778684aa9489eb9d8dc0da1e7ca2fbe3ec8`
**Disposition:** `SOURCEFREE_ORIGINAL_SCOPE_CANDIDATE_NOT_ADOPTED__REAL_SOURCE_RIGHTS_UNISSUED`

## Outcome

All five post-Astra PV defects are productively repaired inside a bounded
sourcefree implementation, and the previously proven V2K/P01 identity and
conservation law is routed through the **existing accepted owners** (real C11
ingest, real I03 query, real I05 discovery, real P01 Field Forge consumer)
rather than reimplemented.

| Suite | Result | Detail |
|---|---|---|
| PV2 hostiles + defect closures | **33 PASS** | `tests/test_pv2_original_scope_binding.py` |
| V2K author baseline (unmodified) | **24 PASS** | historical baseline |
| Frozen PV 21 diagnostics (re-graded) | **21 PASS** | still reproduce/observe limitations |
| Accepted owner suites | **111 PASS** | 5 suites, unmodified |
| Genuine cold process (`first` then fresh-interpreter `replay`) | **PASS** | `[3,3]` → `[0,0]`, byte-identical |
| Register precommit | **PASS** | committed before any owner call |
| **Total** | **189 PASS / 0 FAIL** | |

## The five defects, closed

| Defect | Proved by PV court | PV2 closure |
|---|---|---|
| (a) coherent foreign U/E refs accepted | 4 cases accepted `ok=True` with textual holds only | Register reconciliation binds each obligation's `original_U_ref`, `independent_E_ref`, `independent_custody_ref` and `original_operation_scope_ref` to the independently precommitted authorized refs; a foreign ref raises `PV2_*_ISSUER_NOT_AUTHENTICATED` **before** any durable call |
| (b) dropping ALL HELD original E members accepted | `nonrunnable == []`, `ok=True` | The complete obligation multiset (runnable **and** HELD) must equal the precommitted multiset: `PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN` |
| (c) cherry-picking an A-only E accepted | single-record E passed `ok=True` | Same multiset anti-join, so any omitted label, slot or namespace is refused with `missing`/`extra` diagnostics |
| (d) reversed semantic-role mask accepted | `(TARGET, CONDITIONER)` accepted against the unchanged X→Y producer | The declared mask is validated against the register, against the real query's target order (positional conditioner/target), and against the actual Field Forge consumer role material |
| (e) foreign native form / respondent unit accepted | `FOREIGN-FORM`, `HOUSEHOLD` accepted | `form`, `respondent_unit`, `language`, `instrument_release`, `administered_occurrence` and `option_scope` are bound to the precommitted trusted original metadata |

## What is anchored before execution

`01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json` is authored
**independently** (`repro/pv2_original_scope_register.py`, never derived from an
owner result) and committed before any owner call.  It carries the complete
original test-only opportunity scope: two synthetic namespaces × four slots
(6 RUNNABLE, 2 HELD `ORDERED_OWNER_NOT_ISSUED`), the authorized test-only
issuer refs, and the independently spelled source-native inventory root
(`904f30758890a1a68e6f1ef943e01cd80434ebe6c261e16406a54e19a21ddb16`).
A candidate caller cannot relabel, rekey, suppress or cherry-pick by supplying
its own E: the register is a separate argument to the gate and is recomputed
from its own binding (`49f0f51866d3327aca2b7d8910517c0317a85c6b7fd3f011c9ffd6634c6218bf`).

TEST_ONLY fixture-owner custody is kept strictly distinct from genuine
prospective original source U/E issuers, which remain HELD
(`04_COMPETENT_U_EPRE_SOURCE_RIGHTS_HOLDS.md`).

## Preserved and newly proven positives

* Six distinct sourceful original work identities are preserved despite only
  three legacy V2 keys, reaching **six distinct Field Forge consumers**, with
  **two HELD obligations retained**.
* Numerical producer-to-consumer witness: PAIR/B joint profiles
  `0 → {0:1, 1:0}` and `1 → {0:0, 1:1}`, denominator 1 each; audits independently
  spelled from the register's declared synthetic rows.
* `link['producer_result_ref'] == link['consumer_material']['producer_fact_ref']`
  for every link; `relation_family` is the real
  `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`.
* Exact replay in a genuinely separate process: identical links, HELD records,
  register roots and expected-payload digest, with **zero** additional durable
  executor calls and zero re-executed owner units.

## Files

| Path | Purpose |
|---|---|
| `repro/pv2_original_scope_register.py` | register, reconciliation gate, role/topology validation, fixture-use grant |
| `repro/pv2_sourcefree_fixture.py` | two-namespace sourcefree original-scope fixture on pinned owner factories |
| `repro/emit_pv2_register.py` | precommits the register to `freezes/` before execution |
| `repro/run_pv2_suites.py` | executes every graded suite |
| `repro/pv2_cold_process.py` | genuine separate-process cold `first` / `replay` |
| `tests/test_pv2_original_scope_binding.py` | 33 PV2 tests |
| `freezes/01_PRECOMMITTED_*.json` | precommitted register |
| `observations/*.xml`, `*.log`, `cold_*.json` | JUnit, stdout, cold-run evidence |
| `observations/cold_ledger/{0,1}/` | durable B01E checkpoint + side-effect journal the fresh process recovered |
| `environment_passport_delta.json` | environment, pinned blobs and runtime deltas |
| `environment_passport_delta.json` | environment, pinned blobs and runtime deltas |
| `01_`…`04_` | precommitted set, consumer proof, hostiles, source-rights holds |

No real original survey respondent data, source/E/EE permission, 35 waves,
N11/N12/V3, actor or canonical adoption was created or claimed.  New separately
independent review is required before adoption.
