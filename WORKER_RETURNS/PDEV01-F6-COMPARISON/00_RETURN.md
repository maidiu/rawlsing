# PDEV-01 F6 receiver comparison — GAP-031/GAP-032/S-F6

**Branch:** `agent/pyat-pdev01-f6-compare-r1`  
**Startup SHA:** `773bb412a820949f13a7178b6671327cd56a3bf1`  
**Role:** bounded integration engineer; sourcefree TEST_ONLY comparison; not reviewer, issuer or adopter.  
**Write root:** `WORKER_RETURNS/PDEV01-F6-COMPARISON/`  
**Review resolved:** `23edffb32141c133c8b45b723bb23f092928115c`

## Result

The actual **named consumer** of the repaired F6M partial-bound product in this
scope is:

```text
f6p_partial_bound_evidence_consumer.consume_f6m_evidence
WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py:189
```

This is not a chronology assertion over all history. It consumes the actual
F6M bundle, not a fixture reimplementation. Reviewed partial bounds and
uncovered target mass reach it:

| world | F6P state | uncovered target mass | point |
|---|---|---:|---|
| W1 full coverage | `SUPPORTED_SYNTHESIS` | `0` | `{formal: 5/8, informal: 3/8}` |
| W2 mixed eligibility | `PARTIAL_IDENTIFICATION` | `1/4` | `None` |
| W7 source excluded | `PARTIAL_IDENTIFICATION` | `1/2` | `None` |
| W3 minority absent | `PARTIAL_IDENTIFICATION` | `1/5` | `None` |

The current WP2 transport expression at `wp2.py` blob
`55e567e4d0780c251bf949268d3d477abdc76a9b`, line 94 expects:

```python
{"bundle_hash": value["native_bundle"]["content_hash"],
 "conditional": value["native_conditional_consumer"]}
```

Applying that exact expression to the actual F6P W2 result produces the raw
receiver exception:

```text
type: KeyError
args: ("native_bundle",)
str:  'native_bundle'
```

The label `COMPARISON_LOCAL_BOUNDARY_SHAPE_DIFFERENCE__NOT_EMITTED_BY_F6P_OR_WP2`
is authored by this comparison harness. No typed receiver exception is claimed.
WP2 `product()` was not executed; no `NONPARENT_OPTIONS` read and no F6M→E04
effect is claimed. The exact-tree scope supports only "no current F6P receiver
found at this tree", not absence in unmerged branches.

The F6C historical receipt is not self-contained. Its exact pinned outputs are
now present separately under `evidence/f6c/`; they show the nonparent consumer,
generic input without `f6_sidecars`, C1 returns and cases invariant across
A/A0/B while F6 sidecars differ. The current N9/N10W progressive candidate has
no F6 import or partial-bound read.

## Review corrections addressed

1. Raw `KeyError('native_bundle')` is recorded as raw `type`, `args` and `str`; no typed exception is claimed.
2. The diagnostic label is explicitly comparison-local and absent from F6P/WP2 behavior.
3. The unexecuted receiver-read effect claim was removed; `wp2_receiver_executed=false` and `observed_effect=null`.
4. `replay/test_review_corrections.py` asserts the raw exception identity and the authored diagnostic boundary.
5. Historical F6C outputs are separate under `evidence/f6c/`; the copied receipt is not treated as self-contained.
6. Checkout-root-dependent F6P output hashes are recorded in `evidence/checkout_root_hash_limit.json`.

## Five historical-function tests

| Test | GAP-031 — current F6 nonpooled composer | GAP-032 — historic F6M/F6P/A | S-F6 — N5→N7 selected field |
|---|---|---|---|
| 1. Current necessity | S07.2/S-F6 requires a nonpooled field product preserving `uncovered_target_mass`; current guard is insufficient. | Historical variant disposition is unresolved; no current adoption. | N5→N7 is required only when the selected N9 world demands a source-qualified field. |
| 2. No lawful adequate successor | `guard_estimand_composition` returns an `OperationGuardReceipt`, not source-qualified bounds or a producer. | F6M is sourcefree historical; F6P is its evidence consumer; neither is current production. | Current WP2 is an uninstalled test port; current N9 candidate has no F6 read. |
| 3. Real receiving need / consumer | F6P is the actual named consumer; tested bounds reach it; no current N7/N9 receiver exists. | F6P consumes F6M; reviewed W2/W7 partials and W3 exclusions are preserved. | No actual current N9 F6 consumer. `NONPARENT_OPTIONS` is not a first F6P read and does not move. |
| 4. Suitability under constraints | Sourcefree TEST_ONLY; no population, weights, transport or source permission. | Sourcefree TEST_ONLY; A/A0 retained negatives; F6P point refusal and bounds preserved. | TEST_ONLY; no source-qualified common-world product, no N9/N11/N12 authority. |
| 5. Comparative gain / disposition | Reuse F6M/F6P only as an oracle; no production patch. **`TRUE_CURRENT_GAP__OWNER_DECIDE_NO_BUILD`**. | Reuse F6M/F6P as a test oracle; reject A/A0. **`HISTORICAL_REJECTED_PRESERVE__NO_ACTION`**. | Preserve evidence; no fabricated receiver. **`NO_JUSTIFIED_CONSUMER__NO_ACTION`**. |

## Exact executable evidence

- F6P implementation `7d7ed1cb0`: `26 passed` on seeds 0 and 1.
- F6P publication/review target `912467aaa`: `32 passed` on seeds 0 and 1.
- Independent F6P review `2e00c8c9e`: `8 passed` on seeds 0 and 1.
- Five historical-function tests: `5 passed`.
- Review-correction tests: `4 passed`.
- Combined correction/five-test run: `9 passed`.
- Comparison output is byte-identical on seeds 0 and 1 within this checkout:
  `evidence/run-comparison.seed0.json` SHA-256
  `a7aa424764a7eb8639efaaa1bfe6be34e99e111ac69f11390e77ed23f3654029`.
- Test logs: `logs/`; JUnit `logs/five_tests_junit.xml` and `logs/review_correction_tests_junit.xml`.
- Exact commands: `COMMANDS.md`; source pins: `SOURCE_PINS.json`.

## Checkout-root hash limit

F6P `output_hash` embeds the absolute `source_product.module_file`. Candidate
and reviewer checkout roots produce different W1/W2/W3/W7 output hashes with
equal normalized semantics; this is recorded in
`evidence/checkout_root_hash_limit.json`. Only same-checkout seed0/seed1 byte
identity is claimed. No cross-checkout-root byte identity claim is made.

## Refusal, severance and limits

- W2/W7/W3 with uncovered mass produce no point; W2/W7 retain source exclusions and W3 retains both source-stratum exclusions.
- `REAL_USE`, self-declared transport permission, and self-declared admission return `PROHIBITED_MODEL_USE` with no point.
- Removing the F6M candidate produces `UNIDENTIFIED_JOINT`/`NO_CANDIDATE_JOINT`, not a partial point.
- No route probability, selection weight, common-respondent inference, population claim or output distribution is created.
- No original SAV/DTA or original-source read; no production code edit; no pooled population.
- F6M/F6P and WP2 details remain at their exact sourcefree review ceilings; no independent adoption is claimed.

## Precise missing dependency

An owner-authorized **F6P evidence → current receiver** contract is absent.
WP2 has no F6P branch; it accepts only F6M `native_bundle` and
`native_conditional_consumer`. A real N9/N7 receiver additionally requires a
source-qualified population/target/estimand bridge, transport permission and
selected-world demand. This comparison does not supply those rights or invent
that adapter. F6M→E04 and F6P→N9 remain unjoined.

**Post-return independent review required before acceptance.**
