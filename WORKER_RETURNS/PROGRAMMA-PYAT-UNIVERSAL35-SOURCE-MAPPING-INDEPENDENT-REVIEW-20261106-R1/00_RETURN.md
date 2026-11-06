# Universal35 A — independent SRC31 source-mapping review

**ROLE:** existing nonauthor F reviewer; not A author.
**FROZEN CHECKOUT:** `ef43bbbbb16ac8925056f7c5bed522d6b1200ea5` (tree `6406069235ee3b66c3275b343370536186034f6e`).
**BASE:** `115fe70e660fb19a65ca49b4a12ffc8876be065c`.
**STATUS:** `A_FACTUAL_MAPPING_ACCEPT_SCOPED__A_BINDING_CONTRACT_REVISE__SOURCE_NEUTRALITY_ACCEPT_SCOPED__NATIVE_SCIENCE_HOLD__NO_PROTECTED_MERGE`.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| Old SRC31 selected mapping is RED; corrected selected original columns PASS with 92,862 events. | The correction repairs the exact unbound response-value/state boundary. | Accept factual mapping scoped. | A + HQ |
| 14 declared user-missing values become DK/NOT_ASKED/SOURCE_SPECIFIC_SPECIAL; 17 unlabelled observed codes remain INVALID_UNRESOLVED. | Exact SAV labels/declarations support the states; unknown codes are not substantive or label-inferred. | Preserve typed states; no downstream substantive coercion. | A + D |
| Actual SAV labels match all 14 replacement labels (`98: DK`, `99/9: NA`, `No opinion`, `Could not understand`). | State meanings are source-declared, not frequency-invented. | Keep exact labels/declarations; no generic label inference. | A + source owner |
| Registry carries `base_commit` and `base_config_path`, but corrections apply from a different path and from a registry with changed commit/path when the canonical hash matches. | Base path/commit are not actually enforced; the claim is stronger than the code. | Enforce both or narrow the binding claim to source SHA + base canonical hash. | A + HQ |
| Only SRC31 original has 31 corrections; SRC31 fixture has 0; 35/18,276/18,413 preserved. | The correction is source/hash-scoped and does not alter unrelated sources or denominators. | Preserve; do not generalize the correction. | A + HQ |
| Full release remains behind positive-authority DEFER. | Mapping repair is not native/science/actor acceptance. | Keep HOLD; no native facts claim. | Original authority owner |

## 2. Exact verdicts

### A factual mapping — `ACCEPT_SCOPED`

- 31 changes: 14 replacements, 17 `INVALID_UNRESOLVED` additions.
- Old pinned config RED: `SourceBackedC11FacadeError: unbound response value/state; no label/frequency/missingness inference`.
- Corrected selected original-column PASS: 92,862 response events; state totals DK 13,497; MISSING 6,387; NOT_ASKED 1,111; INVALID_UNRESOLVED 325; SUBSTANTIVE 71,542.
- `c10ai` 98=DK, 99=NOT_ASKED.
- 43 targeted tests pass: 5 correction tests + 38 current-port/library/foundation/admission tests.
- Estate: 35 sources / 18,276 items / 18,413 slots / fixture SRC31 corrections 0.

### A binding contract — `REVISE`

`apply_source_config_corrections` matches source_id, source SHA, base canonical hash, purpose and identity class, but not `base_commit` or `base_config_path`. Repro:

```text
path_variant_corrections 31
changed_commit_path_corrections 31
```

A byte-identical config loaded from a different path, or a scratch registry with changed `base_commit`/`base_config_path`, still receives all 31 corrections. The factual mapping is unaffected (canonical hash is exact), but the claimed base path/commit authority binding is not enforced. Fix by comparing both, or narrow the claim.

### Source neutrality — `ACCEPT_SCOPED`

- `corrections.py` has no survey-name branch; it applies versioned resource data only.
- Only `ORIGINAL_SOURCE / SOURCE_PREPARATION` is eligible; fixture and other originals unchanged.
- `SourceConfig.corrections_applied` and library `select`/`validate_source` expose the applied list.
- No source-specific factory/facade/kernel branch added.

### Native/science — `HOLD`

- Full release validation: `NOT_RUN__POSITIVE_AUTHORITY_DEFER_EXPECTED`.
- No native facts, scientific/structural meaning, actor grant or protected merge.
- Selected-column proof only; not all35 native execution.

## 3. Probe and test receipts

```text
probe_src31_boundary.py (authorized SRC31 selected affected columns; aggregate output)
# old config RED
# corrected 92,862 events; DK 13,497; MISSING 6,387; NOT_ASKED 1,111;
# INVALID_UNRESOLVED 325; SUBSTANTIVE 71,542; 73.75s

pytest -q rawlsing_next/tests/test_source_configuration_corrections.py
# 5 passed in 1.59s

pytest -q test_source_configuration_current_port.py test_source_configuration_library.py \
  test_source_configuration_foundation.py test_pre553_source_read_admission.py
# 38 passed in 109.11s
```

Evidence is in `01_EXACT_IDENTITIES.json`, `02_REVIEW_VERDICTS.json`, `03_FINDINGS_AND_REPRO.md`, `04_TEST_RECEIPTS.json`, and `revisions/r1/evidence/`. No rows, native keys or raw source bytes are output/committed. The actual source root is runtime-only and is not embedded in product or Git evidence. No full all35 decode, 600s rerun, product repair or guide/protected write was performed.

## 4. PROGRAMMA_DELTA

See `05_PROGRAMMA_DELTA.json`. It records A's factual scoped acceptance, binding-contract REVISE, source-neutrality acceptance, native/science HOLD, exact source/config identities and finite next correction.

## 5. Boundary

This is an independent review, not self-acceptance, source repair, protected merge, native/science/actor issuance or full-release acceptance. The previous F/D/G reviews remain independent evidence. Exact published review head is returned in final chat after commit/push.
