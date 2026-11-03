# PDEV-01 F6 receiver comparison — GAP-031/GAP-032/S-F6

**Branch:** `agent/pyat-pdev01-f6-compare-r1`  
**Startup SHA:** `773bb412a820949f13a7178b6671327cd56a3bf1`  
**Role:** bounded integration engineer; sourcefree TEST_ONLY comparison; not reviewer, issuer or adopter.  
**Write root:** `WORKER_RETURNS/PDEV01-F6-COMPARISON/`

## Result

The actual first consumer of the repaired F6M partial-bound product is:

```text
f6p_partial_bound_evidence_consumer.consume_f6m_evidence
WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py:189
```

It consumes the actual F6M bundle, not a fixture reimplementation. Reviewed
partial bounds and uncovered target mass reach that consumer:

| world | F6P state | uncovered target mass | point |
|---|---|---:|---|
| W1 full coverage | `SUPPORTED_SYNTHESIS` | `0` | `{formal: 5/8, informal: 3/8}` |
| W2 mixed eligibility | `PARTIAL_IDENTIFICATION` | `1/4` | `None` |
| W7 source excluded | `PARTIAL_IDENTIFICATION` | `1/2` | `None` |
| W3 minority absent | `PARTIAL_IDENTIFICATION` | `1/5` | `None` |

The current WP2 receiver does **not** accept that product. Exact WP2 transport
(`wp2.py` blob `55e567e4…`, line 94) expects:

```python
{"bundle_hash": value["native_bundle"]["content_hash"],
 "conditional": value["native_conditional_consumer"]}
```

F6P supplies `F6P_PARTIAL_BOUND_EVIDENCE@1` with `input_bundle`,
`covered_subprobability`, `uncovered_target_mass`, `conditional`, etc. The
first typed mismatch is therefore:

```text
code: F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR
exception: KeyError: 'native_bundle'
read effect: NO_NONPARENT_OPTIONS_READ; NO_F6M_E04_JOIN
```

The F6C receipt independently records `NONPARENT_OPTIONS` material invariance
across A/A0/B and no installed F6M→E04 join. The current N9/N10W progressive
candidate has no F6 import or partial-bound read. Thus the reviewed partial
bounds and uncovered mass reach **F6P only**, not the current N9/N7 consumer.

## Five historical-function tests

| Test | GAP-031 — current F6 nonpooled composer | GAP-032 — historic F6M/F6P/A | S-F6 — N5→N7 selected field |
|---|---|---|---|
| 1. Current necessity | S07.2/S-F6 requires a nonpooled field product preserving `uncovered_target_mass`; current guard is insufficient. | Historical variant disposition is still unresolved; no current adoption. | N5→N7 is required only when the selected N9 world demands a source-qualified field. |
| 2. No lawful adequate successor | `guard_estimand_composition` returns an `OperationGuardReceipt`, not source-qualified bounds or a producer. | F6M is sourcefree historical; F6P is its evidence consumer; neither is current production. | Current WP2 is an uninstalled test port; current N9 candidate has no F6 read. |
| 3. Real receiving need / first consumer | F6P is the actual first consumer; tested bounds reach it, but there is no current N7/N9 receiver. | F6P consumes F6M; reviewed W2/W7 partials and W3 exclusions are preserved. | No actual current N9 F6 consumer. `NONPARENT_OPTIONS` is not a first F6P read and does not move. |
| 4. Suitability under constraints | Sourcefree TEST_ONLY; no population, weights, transport or source permission. | Sourcefree TEST_ONLY; A/A0 retained negatives; F6P point refusal and bounds preserved. | TEST_ONLY; no source-qualified common-world product, no N9/N11/N12 authority. |
| 5. Comparative gain / disposition | Reuse F6M/F6P only as an oracle; no production patch. **`TRUE_CURRENT_GAP__OWNER_DECIDE_NO_BUILD`**. | Reuse F6M/F6P as a test oracle; reject A/A0. **`HISTORICAL_REJECTED_PRESERVE__NO_ACTION`**. | Preserve evidence; no fabricated receiver. **`NO_JUSTIFIED_CONSUMER__NO_ACTION`**. |

## Exact executable evidence

- F6P implementation `7d7ed1cb0`: `26 passed` on seeds 0 and 1.
- F6P publication/review target `912467aaa`: `32 passed` on seeds 0 and 1.
- Independent review `2e00c8c9e` test: `8 passed` on seeds 0 and 1.
- Five historical-function tests: `5 passed`.
- Comparison output is bit-identical on `PYTHONHASHSEED=0` and `1`:
  `evidence/run-comparison.seed0.json` SHA-256
  `bf5f45fee142b46f302e3384371fee4ff651a7facb46e63893069e6afcc00f73`.
- Test logs: `logs/`; JUnit `logs/five_tests_junit.xml`.
- Exact commands: `COMMANDS.md`.
- Source pins: `SOURCE_PINS.json`.

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
