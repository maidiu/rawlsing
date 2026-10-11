# PYAT HQ280 PV3 A05 — Independent expected-work and consumer no-drop adversarial oracle

**TERMINAL:** `HQ280_PV3_A05_INDEPENDENT_EXTERNAL_NODROP_ORACLE_ADVERSARIAL_PASS_OR_EXACT_HOLD__GITHUB_PUSHED`
**RESULT:** `PASS__STANDALONE_EXTERNAL_ORACLE_BUILT_AND_ADVERSARIALLY_VERIFIED__18_OF_18_CASES_AS_EXPECTED__NONISSUING`
**Branch:** `agent/rabochii-pyat-hq280-pv3-a05-independent-nodrop-oracle-r1` @ `921a17130002e741d25824a19ce39412399a51a5`
**Control:** HQ280 parallel seal `908ee4e74849884b1d4c2f532209a0ca57538b67`; inherited HQD-2026-10-10-280; canonical baseline `a70a069fa948e0f3c041b389edcc732b6b948a4f`; PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated).
**A04 code modified:** **NO.** A04 was not present on this branch; the oracle is standalone and imports nothing from the repository or from A04's binder, exactly as the commission permits.

## 1. What was built

A **standalone, deterministic, source-free** expected-work oracle plus an adversarial court, authored **before and apart from** any submitted manifest:

| artefact | role |
|---|---|
| `repro/a05_oracle.py` | the oracle: external frozen universe (`E`/`H`/`D`/`NA`), five key kinds, and `verify()` |
| `repro/a05_hostiles.py` | 18-case adversarial court (16 must-FAIL mutations + 2 must-PASS controls) |
| `repro/a05_hostile_results.json` | the actual run record |

Both scripts import only the Python standard library — **no repository import, no A04 import, no raw survey**.

## 2. Key separation (the A04 schema-compatible contract)

The oracle keeps five identity kinds strictly distinct, as `ACTION_PLAN.md:103` requires:

```
documentary_item_key   source|wave|item|form|slot                    (what the instrument asked)
operation_key          op_class|roles|target                         (what operation is proposed)
expected_work_key      item+op+authority+risk+topology+SCHEMA_VERSION (the frozen expectation)
execution_attempt_key  expected+n                                      (one attempt at that work)
output_identity        expected+result_type+value                      (the produced identity)
```

`SCHEMA_VERSION = "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"`; all hashes are SHA-256 over canonical JSON (`sort_keys`, compact separators), so preimages are complete and collision handling is explicit by construction.

## 3. The no-drop verifier and what it catches

`verify(universe, manifest)` compares the external `E` set against `J` (jobs), `R` (typed results), `A` (products) and `C` (required consumers), while requiring `H`/`D`/`NA` to remain **visible but never runnable**. It raises eleven distinct failure codes:

`EXPECTED_OPERATION_OMITTED` · `UNAUTHORIZED_EXTRA_JOB` · `EXPECTED_MULTIPLICITY_MISMATCH` · `MISSING_TYPED_RESULT` · `FALSE_EMPIRICAL_NULL` · `PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS` · `ZERO_DENOMINATOR_NOT_TYPED` · `PRODUCT_ABSENT` · `REQUIRED_CONSUMER_OMITTED` · `HELD_OR_DENIED_WORK_EXECUTED` · `HELD_OR_DENIED_WORK_NOT_VISIBLE` · `CANDIDATE_OWN_DK_JOINT` · `EXPECTED_SET_OUTPUT_DERIVED` · `SOURCE_IDENTITY_MISMATCH`.

## 4. Adversarial result — 18/18 as expected

`python3 repro/a05_hostiles.py` → **exit 0, `all_expectations_met: true`**.

| # | hostile | oracle verdict |
|---|---|---|
| H0 | honest manifest | **PASS** (control) |
| T1 | expected operation omitted | FAIL `EXPECTED_OPERATION_OMITTED` |
| T2 | **missing B and missing J2** (B1-R witnesses) | FAIL `EXPECTED_OPERATION_OMITTED` |
| T3 | injected unauthorized extra job | FAIL `UNAUTHORIZED_EXTRA_JOB` |
| T4 | **A-only projection** while both source items eligible | FAIL `EXPECTED_OPERATION_OMITTED` |
| T5 | **wrong keys, same total count** | FAIL `OMITTED` + `UNAUTHORIZED_EXTRA_JOB` |
| T6 | false null from `AUTHORITY_UNAVAILABLE` | FAIL `FALSE_EMPIRICAL_NULL` |
| T6b | false null from zero denominator | FAIL `FALSE_EMPIRICAL_NULL` |
| T7 | `PARTIAL` reported as success | FAIL `PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS` |
| T7b | `UNVISITED` reported as success | FAIL same code (partial/adaptive ≠ success) |
| T8 | candidate own-`_dk` joint (`v176`→`v176_dk`) | FAIL `CANDIDATE_OWN_DK_JOINT` |
| T9 | expected set derived from the emitted manifest | FAIL `EXPECTED_SET_OUTPUT_DERIVED` |
| T10 | **required consumer omitted though the product exists** | FAIL `REQUIRED_CONSUMER_OMITTED` |
| T11 | held obligation executed | FAIL `HELD_OR_DENIED_WORK_EXECUTED` |
| T11b | held work not visible at all | FAIL `HELD_OR_DENIED_WORK_NOT_VISIBLE` |
| T12 | backward/wrong source identity | FAIL `SOURCE_IDENTITY_MISMATCH` |
| T13 | **stable reordered expected set** | **PASS** (order invariance control) |
| T14 | multiplicity mismatch | FAIL `EXPECTED_MULTIPLICITY_MISMATCH` |

**The commission's key requirement is satisfied:** the oracle fails **even where a local per-shard test would pass** — T4 and T5 both preserve plausible local counts while breaking external set equality; T10 fails with every product correctly present; T11b fails with every job correct.

## 5. Stage separation proved

The oracle's verdicts demonstrate the distinctions the commission demands, by *failing* when they are conflated:

- **expected operation ≠ constructed job** — T3 (unauthorized extra) and T5 (same count, wrong keys);
- **constructed job ≠ typed result** — T7/T7b (`PARTIAL`/`UNVISITED` reported as success);
- **typed result ≠ released product** — products are a separate set (`PRODUCT_ABSENT`);
- **released product ≠ satisfied consumer** — **T10** is the decisive case: every product present, one required consumer missing → FAIL;
- **null ≠ unavailable** — T6/T6b: only a genuinely measured null qualifies; `AUTHORITY_UNAVAILABLE` and zero denominators cannot be laundered into an empirical null;
- **held/denied/NA stay visible and non-runnable** — T11/T11b.

## 6. Graded real-source precedents (exact scopes only)

See `04_GRADED_REAL_SOURCE_PRECEDENTS.json`. In summary: the B1-R A/B 8-respondent 4-case XOR slice is `SOURCE_FREE_SYNTHETIC_FIXTURE`; WGA-R's 600 misleading `UNVISITED` and 2,980 topic-pair traps are `DOCUMENTARY_ACCOUNTING`; the WVS7 46 pre-I05 frontier / 58 `UNAVAILABLE` distinction is `RETAINED_REAL_PRODUCT_AT_DECLARED_SCOPE`; WGC/WGD holds are `DOCUMENTARY_CORRECTED_LEDGER`. **None of these licenses an all-35 scientific eligible frontier**, and this return does not claim one.

## 7. Ceilings

No original source read, no raw `SAV`/`DTA`, no semantic/model/use, G0b, EE12 or operative publication permission; no new runtime producer or manifest planner; no repository import; no A04 code touched; no canonical/PRE-MAIN mutation; no self-adoption. The oracle is a **development-grade verification instrument**, not an issued expected-work authority — adopting its frontier for any real slice remains a competent owner's act.

**Terminal:** `HQ280_PV3_A05_INDEPENDENT_EXTERNAL_NODROP_ORACLE_ADVERSARIAL_PASS_OR_EXACT_HOLD__GITHUB_PUSHED`.
