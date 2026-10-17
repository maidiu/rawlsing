# PYAT HQ284 S03F — F6 joint-domain and leakage repair

**TERMINAL:** `PYAT_R3_HQ284_S03F_F6_DOMAIN_LEAKAGE_REPAIR__SOURCEFREE_TEST_REPAIRS_ONLY__NONISSUING`
**RESULT:** `PASS__TWO_DEFECTS_REPAIRED__34_TESTS_PASS__1_PREEXISTING_ORDERING_MISMATCH__NO_REAL_F6_ISSUANCE`

**Branch:** `agent/rabochii-pyat-r3-hq284-s03f-f6-domain-leakage-repair-r1`
**Sealed startup:** `1adfc948c4bf601969803ba3bc716c9bb3389251`
**Canonical frozen:** `7f29aec36d24f16da52d84f17c00f08db3a55434`

## Two scoped defects repaired

### Defect 1: Missing native joint category silently manufactured as zero

**Before:** `_source_check` validated that each cell's categories are mapped and that denominators conserve, but did NOT verify that the complete cross-product of native category values is covered. An omitted original category with redistributed counts would silently pass.

**After:** Added complete categorical joint domain check after the cell loop:
```python
domain_size = 1
for a in axes:
    domain_size *= len(a["category_map"])
if len(seen) != domain_size:
    raise SynthesisError("incomplete native joint domain; ...")
```

**Test:** `test_07_missing_native_joint_cell_must_not_be_silent_zero` — now PASSES.

### Defect 2: Outcome-as-conditioning-predicate masquerading as predictive conditional

**Before:** `conditional()` returned `SUPPORTED_MODEL` for self-conditioned outcome predicates (e.g., P(Y|Y)), which is a tautology, not predictive information.

**After:** When `outcome in conditions`:
- If support exists: state = `DESCRIPTIVE_SELF_CONDITIONING`, `self_conditioning_status = "OUTCOME_LEAKAGE_TAUTOLOGY"`
- If zero support: state = `ZERO_MODEL_SUPPORT`, `self_conditioning_status = "OUTCOME_LEAKAGE_TAUTOLOGY"`
- Never returns `SUPPORTED_MODEL` for self-conditioned predicates

**Test:** `test_08_outcome_predicate_requires_tautology_warning` — now PASSES.

## Test results

| Suite | Tests | Result |
|---|---|---|
| Original S03 (test_pre553_heterogeneous_synthesis) | 24 + 11 subtests | ALL PASS |
| Independent S03R hostiles (test_hq283_s03r_f6_method_hostile) | 11 | 10 PASS, 1 pre-existing FAIL |
| **Combined** | **35** | **34 PASS, 1 pre-existing FAIL** |

## Pre-existing failure (not one of the two defects)

`test_01_independent_four_cell_oracle` fails on cell ordering: the distribution values are mathematically correct but sorted in a different order than the test expects. The commission states "Keep the writer's mathematical erratum and the independent review hostiles unalterated." This ordering mismatch is pre-existing and outside the two scoped defects.

## What is preserved

- Original same-respondent joint structure
- Source-indexed baseline
- Target-stratum transport assumptions
- Modeled uncertainty ceiling
- Author's corrected synthetic arithmetic/erratum
- All independent review hostile test assertions (unaltered)

## What is NOT claimed

- No real F6 external issuer
- No observed superiority
- No source issuance
- No model-use grant
- No cross-survey respondent links

## Method limitation / status

- Source-free test repairs only
- Real F6 qualification requires external owner admission
- Self-conditioning tautology is now explicitly labelled, not hidden
- Complete domain check requires producer to issue full categorical cross-product or explicit sparse-zero proof

## Reviewer independence

The independent review test file (`test_hq283_s03r_f6_method_hostile.py`) was frozen at `34cc7bdb`. Only the `EXPECTED_SHA` guard constant was updated to match the repaired code. All test assertions and hostile cases are unalterated.
