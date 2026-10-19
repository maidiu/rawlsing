# Court A — E04L selected release read-through — independent review

**Verdict: ACCEPT** at exact source-free TEST_ONLY I2 grain.
**Target:** `daf0d085e930696708c755e687879b155653c215` (branch tip; implementation commit `14135c1f5`).
**Claim:** unchanged `product.nonparent.consume()` obtains empirical material through the actual B5 current-selected / M2-exact / I4-conserved / producer-owned fact-query-predicate resolution, and refuses when that release edge is severed rather than serving cached source.

## 1. Provenance verified independently (not taken on the author's word)

| Object | Reviewer check | Result |
|---|---|---|
| Original consumer `vendor/product/nonparent.py` | `git hash-object` vs E04JR `b39b75656` and WP2 author `f7824794` | `2181b832d3c4376d4b9428e13f4354f273be8f32` all three — **unchanged** |
| Original service `vendor/product/service.py` | same | `facf1c86911a8a4c37db112be51d8c7109cd9f3b` all three — **unchanged** |
| `vendor/product/{__init__,empirical,world,scenario}.py` | same | identical to E04JR / WP2 |
| `vendor/aux/pre553_n9_n10w_progressive_candidate.py` | vs E04JR | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` — **unchanged** |
| M1 `pre553_learned_empirical_adjudication.py` | vs `2e6c189f` | `761db592…` match |
| M2 `pre553_learned_product_release.py` | vs `2e6c189f` | `f76c3906…` match |
| B5 `pre553_learned_product_lifecycle.py` | vs `2e6c189f` | `a11c9eb7…` match |
| I4 `pre553_learned_world_composition.py` | vs `2e6c189f` | `4a8e27a2…` match |
| Reviewer fault-witness restores `readthrough.py` | `git hash-object` after gate | `f8e73a6a65713c968c1427381c62ced54de9150c` == committed blob — **restored** |

The adapter `readthrough.py` (`f8e73a6a…`) is the only new executable edge; the original consumer bytes and all owner modules are unchanged.

## 2. Author court reproduced

- New read-through/hostile tests: **22 passed / 0 fail / 0 error / 0 skip**.
- Exact rehydrated original E04 native consumer court (from E04JR `b39b75656`): **7 passed / 0 / 0 / 0**.
- Cold replay, `PYTHONHASHSEED` 0 and 1: **29 passed** each.
- Author's own two `.proof.json` witnesses reproduced through the shared gate: both `baseline=PASS`, `evidence_state=TARGET_ASSERTION_FAILED`.

## 3. Reviewer's independent oracle (not the author's expectations)

Recomputed directly from the frozen source rows (`pre553_n9_n10w_progressive_candidate.synthetic_world_rows()`), n=58:

- base prefixes Y|A=1, Y|A=1,B=1, Y|A=1,B=1,C=1 → denominators `[32,16,8]`, Y=1 counts `[18,10,6]`;
- same-marginal variant (two opposite Y flips) → `[32,16,8]`, `[19,11,7]`, with equal global Y marginals preserved.

The consumer's served cells/denominators equal the reviewer oracle for both worlds; route probability remains `None`; structural routes are equal across worlds. Reviewer module: `evidence/court_a/test_court_a_e04l_independent.py` (**10 passed**).

Materiality was checked by the reviewer, not assumed: for every step the served cell counts equal the numeric content of the exact catalog `EmpiricalFact` referenced by the record, that fact/query/predicate are members of the resolved release subject **and** the release dependency closure, and the emitted `learned_release_binding` refs equal the live B5 selection ref, the resolved M1 subject ref and the actual M2 resolution receipt ref. Independent I4 recomposition returns `RULE_SATISFIED` on the same release.

## 4. Reviewer-written falsifiers that turn RED (independent of the author's two witnesses)

| Claim | Genuine defect injected | Named reviewer test | Result |
|---|---|---|---|
| Severed selected release must refuse | resurrect the cached composition release when the live M2 repository lacks it | `test_original_consumer_refuses_when_selected_release_removed_source_fixed` | baseline PASS → **TARGET_ASSERTION_FAILED** → restored PASS |
| Stale B5 selection must not serve | bypass live `resolve_selection_exact` with a frozen composition-time selection | `test_stale_b5_current_selection_is_load_bearing` | baseline PASS → **TARGET_ASSERTION_FAILED** → restored PASS |

Additional independent hostiles that all refuse as required (no source fallback): substituted well-typed shallower producer fact for the deepest query; shallower predicate for the deepest query; forged source-universe binding; missing producer predicate object; unreleased reverse/extra-conditioner query (`RELEASE_QUERY_NOT_INCLUDED`); consumer executes correctly with the original source provider/`execute_empirical_query` patched to raise, and the original provider trace is unchanged.

The severance test removes only the selected immutable release (`del repository._releases[ref.key]`), holds the original empirical source fixed (world `rows_hash` and provider trace unchanged) and drives the **unchanged** `product.nonparent.consume`; it refuses and, after exact re-registration, returns a byte-identical receipt.

## 5. Recorded residuals / honest limits

1. **Not a payload release.** The selected M2 release is an authorization/binding gate; the numeric material is the producer-owned `EmpiricalFact` objects built from the source at preparation. This matches the author's stated design ("does not inline payloads into M2") and the commission wording ("exact producer-owned fact/query/predicate objects"), but a downstream reader must not read "read-through" as "release-stored numbers."
2. Synthetic fixture source, explicit fixture lifecycle selection and `TEST_ONLY_E04_SOURCE_ROOT` remain; no real source/clock, no all-35, no N9/OC05 installation, no issuer/source/model grant. The author's own HOLD list is preserved, not widened.
3. M1 uses explicit synthetic fixture validator/authority constructors; the edge proves owner execution and reference conservation, not a new substantive scientific validation rule.

Verdict **ACCEPT** is scoped precisely to the source-free TEST_ONLY read-through edge above. No production promotion or owner/semantic issuance is implied.
