# Revision: no-drop and core ABI reconciliation (2026-11-21)

**CURRENT FEATURE CODE CUT (before this documentary amendment):** `f2c2bbd0d0d4f052626cc5ecfd9f01a02dd5c3bd` · draft [#1247](https://github.com/maidiu/rawlsing/pull/1247). This remains **COMMITTED_UNTESTED**; #1243's report of 374 local PASS is not proof of this new tree. The code branch is an exact descendant of #1243, NOT a merge of its history.

**Important source reconciliation after the initial 18-file transplant:** A complete `rawlsing_next/*.py` filename/blobs anti-join against #1244 exposed three further genuinely existing producer modules omitted by #1243, plus five older source-level semantic improvements overwritten in #1243's recovery. Exact original blobs and corresponding historical tests are now preserved in #1247:

- **S2-F (durable result closure):** `pre553_durable_empirical_closure.py` (`ceeb8589cf785d2a24fe468073bd5f68df405be1`) and lossless `pre553_durable_empirical_fragments.py` (`b29ef20ba71ecb193ba39bbb5df33718ed3792c8`), with FOUR original sourcefree test files. Preserves real I03/I05 output closure and cold reopening; does not self-issue CURRENT or scientific permission.
- **S2-G (learned product lifecycle):** `pre553_durable_learned_lifecycle.py` (`c261db4f13b6a63d0b41d0cb87855287f3c06347`), with FIVE original lifecycle/cold/hostile test files. Uses existing M1/M2/B5 and N10E owner compositions; no new model/actor authority.
- **Batch owner ABI:** `pre553_batch_runner.py` (`8320f28458fb85aec655d154a2527a161282f56b`) recovers exact `SavedC11Admission | PreparedSavedC11Admission` acceptance **only with `saved_mode=True`**. Without it, the prepared saved Batch adapter cannot run on #1243 even though all imports exist. Normal accepted C11Repository behavior remains the default.
- **I05 terminal fate:** `pre553_discovery_exact.py` (`65e9baea00b7ad8d1d6bfde910553eb65dbedf20`) retains a distinct `UNRESOLVED` fact→`EVALUATED_UNRESOLVED` / coverage-limited result instead of collapsing it into `UNAVAILABLE`. Preserve typed ignorance rather than manufacturing an absence.
- **Original asked/eligible source states:** `pre553_native_workload_binding.py` (`56919f78327ac4480de186004bb8f3c579db7659`) conserves source-typed nonanswers in RAW scalar query roles with the existing `pre553_asked_eligible_raw_distribution` producer; does not invent administered eligibility.
- **Bounded Stata decoder:** `pre553_physical_decoder.py` (`85ce3290d1dc8e1eb1362c22f200715b3d22758a`) restores bounded DTA extended-missing-declaration probing, capped cells per reader chunk and the source custody checks. Avoids silently dropping extended missingness from source material.
- **Source-backed cache semantics:** `pre553_source_backed_c11_facade.py` (`f29247b33cb78e5f1e620620d6968ab433ce407a`) restores producer-only first admission, immutable governed-input snapshot, exact current/source/transport binding, no silent rebind, and locked idempotence. The recovered #1243 simpler public `put` may otherwise retarget cached C11. This is a scoped safety/identity difference that MUST be regression tested; no unconditional production assertion.
- **Hostile regression coverage:** exact original S1-D CURRENT/caching, cache differential, physical-order, wide-DTA-cell-cap tests are retained, including the 19-case `test_pyat940_s1d_current_permissions.py` fixture imported by two cache tests. Existing `test_pyat919_s2e_b2_fate_counterexample.py` also restored.

**All other `rawlsing_next/*.py` file names/blobs** are now matched to #1244's source cut on the author branch (file-level source comparison, not execution/scientific equivalence). Q015 code and R03-v2 issuer were already identical and not touched independently.

### Exact runnable sourcefree courts (must be executed on the final HEAD)

The existing REMONT/OpenCode runner still owns QIDs. Its new/extended tests on #1247 are Q008 (physical journal) and Q023 (prepared saved-Batch, distinct cold I03/S04, open-ended dynamic research, R03-v2 v1-to-v2 and new joined saved C11→S04→FF01); unchanged Q014/Q015/Q021 preserved. From clean worktree:

```bash
EXPECTED_PREFF_C0_HEAD=<ACTUAL_FINAL_COMMIT_SHA> \
  bash rawlsing_next/tests/run_preff_remont_batch.sh \
  RMT-Q008 RMT-Q013 RMT-Q014 RMT-Q015 RMT-Q016 RMT-Q017 RMT-Q018 RMT-Q020 RMT-Q021 RMT-Q023

PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a*.py \
  rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py \
  rawlsing_next/tests/test_pyat940_s2f_*.py \
  rawlsing_next/tests/test_pyat960_s2g_*.py \
  rawlsing_next/tests/test_pyat940_s1d_*.py \
  rawlsing_next/tests/test_pyat940_s1b_b08_wide_dta_cell_cap.py \
  rawlsing_next/tests/test_c1_agent_b_cache_differential.py \
  rawlsing_next/tests/test_pyat1006_verified_native_physical_order.py
```

These tests are **not observed running here**. Do not regard pytest skips as a complete PASS, copy earlier 374/41/14/1 results to the new SHA, infer original35 rights, or grant scientific/actor validity. Source-diff evidence identifies *candidate* improvements but does not adjudicate potential native compatibility regressions from replacing the five core modules; red tests are real first faults for REMONT, not excuses to discard the restored function unexamined.

**The next P0 criterion** is an exact sourcefree and then authorized high-width native C11 saved Batch 1/10/100 **distinct** query run (one prepared index, live respondent-coherent results, no invalid asked/eligible denominators, measured RSS/wall/source reopen and cold recovery) feeding actual S04→FF01, with source and scientific rights separately granted. S2F/G durability is independently required downstream but cannot pretend to be this P0 performance proof.

---

# PYAT selective forward-construction over REMONT #1243 — 2026-11-21

**Single isolated source candidate.** Parent [REMONT #1243](https://github.com/maidiu/rawlsing/pull/1243) `3b27f559e70c1de95426e40a8ee6bbe30011455d`, source donor [PYAT #1244](https://github.com/maidiu/rawlsing/pull/1244) `ede4ed7fc4b3c4a4de1767e6fbd9e0a4c2343550`. No wholesale merge of either history. This branch is not protected and is NOT owned by REMONT.

## Preserved only because the exact function was absent/inferior on #1243

- Existing cold native query evaluator untouched. `PreparedSavedC11Admission.from_verified_admission` and saved Batch `reuse_prepared_session=True` provide a new real normal-workload consumer of the inherited single-posting-index operation; default Batch semantics unchanged. Original R03 v2 QUERY issuer blob identical on both inputs and **not modified**.
- `pre553_distinct_cold_i03_batch` (bounded 1/10/100 distinct) and `pre553_distinct_cold_s04_batch` (actual I03→S04 and optional FF01); `pre553_s04_dynamic_research` (unbounded, catalog-issued sequences over one cold session, with CURRENT on original source and optional interpretation). These are distinct access modes, not new numeric/scientific authorities.
- Physical journal v2 `physical_metadata.json` carries original decoder dictionary, unlike v1 digest only. The carried implementation **retains v1's anonymous pinned compressed-byte snapshot, full typed validation before first yield, private owned/no-follow reader and adverse mutation/symlink tests**. Source-I02 one-pass close-before-publish/independent rollback is carried **exact from REMONT R16** (`4bed962724efdf68c31f7a13e697533c7552c8aa`), not a new builder invention.
- Existing S2-E verifier `pre553_s2e_exact_conservation` and its four historical test modules are restored byte-exact from #1244: this resolves the **source-file missing-import** identified on #1243, NOT proof that the full optional native S2-E path runs.
- Exact existing Q015 code blob `eaf83cf340ddbe10fc8c53c4dd57d0f1afd247c2`, existing R03 v2 issuer `a55275c4b5f824496f7d18df9d013e1ab883a317`, S04→FF01 `527eecbd3d5c0e980fe63b95229565441c310ce8` are identical across both and **untouched**. Q015 remains REMONT-owned. SORACLE #1234 untouched. Q019 retired.

## Runnable tests / negative conservation

Original transplanted suites: 1/10/100 **distinct SOURCEFREE** cold I03, cold I03→S04/FF01, dynamic 103 original catalog queries, 257 conditioned followups over same S04 joint, CURRENT revocation between calls, no original survey rights, exact source/predicate refusal, physical v2 dictionary/corruption/symlink/cold mutation, S2-E corpus/identity/false-complete refusals, R03 v2 issuer/saved Batch, prepared admission and revocation. One **new** connected sourcefree first-consumer test binds an ordinary saved C11 admission to one physical posting session and TWO original RAW k-way query facts, checks S04→existing FF01 semantic exact-ref parity with the original generic ingress and no second native I03.

Existing REMONT/OpenCode runner on THIS candidate HEAD adds Q023 (new shared cold-consumer integration), extends existing Q008 with actual physical journal; Q015 and all other historical QIDs remain same. Execute only from a clean checkout with `EXPECTED_PREFF_C0_HEAD=<exact SHA> bash rawlsing_next/tests/run_preff_remont_batch.sh RMT-Q008 RMT-Q014 RMT-Q015 RMT-Q021 RMT-Q023`. Run the 4 S2-E test files explicitly via `python -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_pyat919_s2e_a*_*.py` (shell glob depends on actual checkout; do not claim green without real logs). **This author cannot run the repo's Python tests in this GitHub-backed environment**; source is COMMITTED_UNTESTED until OpenCode/host executor produces exact immutable proof.

## Still missing and not represented as green

Original SAV/DTA source and survey-scientific issuance, a real high-width source-shaped 1/10/100 distinct CPU/RSS/cold-read measurement under ≤6 GiB, complete native S2-E optional consumer, original source FF02 material/world/actor consumption, independent review, protected code/paired receiving. Preserve #1243's reported 374 local PASS ONLY at its own SHA; this new SHA has NO inherited PASS receipt.
