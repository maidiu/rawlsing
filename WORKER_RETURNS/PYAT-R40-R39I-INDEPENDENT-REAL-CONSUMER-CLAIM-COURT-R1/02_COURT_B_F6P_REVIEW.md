# Court B — F6P partial-bound evidence consumer over actual F6M — independent review

**Verdict: ACCEPT** at exact source-free TEST_ONLY I2 grain.
**Target:** `912467aaacb715fd6e80ebc8c2bdd7285c26120b` (branch tip; implementation commit `7d7ed1cb0`).
**Claim:** the named `consume_f6m_evidence` consumer reads the **actual repaired F6M** native product and candidate (not a duplicate fixture calculation), calls the actual F6M `conditional`, and exposes supported point / partial bounds / unknown mass / source exclusions / transport and model-use refusals with no fabricated route probability or selection weight.

## 1. Provenance verified independently

| Object | Reviewer check | Result |
|---|---|---|
| F6M `native/rawlsing_next/pre553_heterogeneous_synthesis.py` | `git hash-object` + `shasum -a 256` | blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`, sha256 `2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871` — matches claim |
| Comparison A (corrected S03FO) `…_A.py` | `git hash-object` | blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c` (== `1428c2e9:rawlsing_next/pre553_heterogeneous_synthesis.py`) |
| A0 historical control `…_A0.py` | `git hash-object` | blob `182cc7970d7624f6614015f5a51d0602e1630d52` (== repo `HEAD:rawlsing_next/pre553_heterogeneous_synthesis.py`) |
| Consumer `f6p_partial_bound_evidence_consumer.py` | blob after gate | `8fa992899293f454d7abded36831a4b4a362df8e` — restored verbatim |
| F6M blob after gate | `git hash-object` | `2df811d7…` — restored verbatim |

**A0 is never comparison A.** Comparison A is `MODULES["A"]` = the corrected blob `fc5e37fa…`; A0 is imported only as `MODULES["A0"]` and is invoked by **no** test. This is checked in the reviewer module.

## 2. Author court reproduced and cold-replayed

- Native court `tests/` (27 consumer + 5 A/B/C oracle): **32 passed / 0 fail / 0 error / 0 skip**.
- Cold replay, `PYTHONHASHSEED` 0 and 1: **32 passed** each.
- Author's own `.proof.json` witness reproduced: `baseline=PASS`, `TARGET_ASSERTION_FAILED`.

## 3. Reviewer's independent exact-rational oracle (not candidate output)

The reviewer re-derived every number from the frozen world inputs by hand (weights, target shares, aggregate support gate, planned-share loss, mapped cell masses) in `evidence/court_b/test_court_b_f6p_independent.py` (**8 passed**); no candidate or author oracle output is used as the expectation.

| Case | Reviewer independent result | Consumer / F6M |
|---|---|---|
| W1 full coverage | covered `{5/16, 3/16, 17/80, 23/80}`, uncovered `0`; point `{formal 5/8, informal 3/8}` | `SUPPORTED_SYNTHESIS`, point matches |
| W2 mixed eligibility | covered `{1/4, 1/8, 3/16, 3/16}`, uncovered `1/4`, no point; S_A minority excluded (`AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT`) | `PARTIAL_IDENTIFICATION`, matches |
| W7 source excluded | covered `{3/20, 1/10, 1/8, 1/8}`, uncovered `1/2`, no point; S_A excluded both strata | `PARTIAL_IDENTIFICATION`, matches |
| W3 minority absent | covered `{6/25, 4/25, 1/5, 1/5}`, uncovered `1/5`, no point; S_A/S_B `NO_SOURCE_STRATUM` | `PARTIAL_IDENTIFICATION`, matches |

Covered mass + uncovered mass = 1 in every case; the reviewer's `_point_from_joint` recomputation gives exactly `5/8, 3/8` for W1.

The corrected A negative control is independently confirmed: W2/W7 yield `uncovered 0` with excluded source present → consumer `FALSE_FULL_COVERAGE`; W3 decision/coverage mismatch → `PRODUCT_INCONSISTENT`. No point is emitted in any of these.

## 4. Reviewer-written falsifiers that turn RED (independent of the author's witness)

| Claim | Genuine defect injected | Named reviewer test | Result |
|---|---|---|---|
| Consumer partial state depends on the actual F6M uncovered mass | drop the uncovered-mass read (`uncovered = F(0)`) in the consumer | `test_uncovered_mass_preserved_independently` | baseline PASS → **TARGET_ASSERTION_FAILED** → restored PASS |
| Consumer follows the actual F6M producer decision | mislabel the real F6M decision as `SYNTHETIC_CANDIDATE` for a partial bundle | `test_consumer_responds_to_actual_producer_decision` | baseline PASS → **TARGET_ASSERTION_FAILED** → restored PASS |

The second witness corrupts the **actual F6M producer** module while unrelated world inputs are fixed, and shows the named consumer's asserted dependency is load-bearing (its response changes). A third independent product-boundary check (`test_consumer_requires_real_f6m_bundle_identity`) confirms a non-rehashed tampered bundle raises `BUNDLE_REPLAY_MISMATCH`, while a rehashed drop-of-uncovered-mass product is refused (no `PARTIAL` point served).

## 5. Required behaviours independently confirmed

- **Unknown target mass preserved:** W2 `1/4`, W7 `1/2`, W3 `1/5`, all > 0, no point.
- **Partial identification:** `supported_point is None` whenever uncovered > 0; `PARTIAL_IDENTIFICATION` state; explicit `source_disagreement_and_uncovered_bounds`.
- **Minority evidence:** all four covered categories retained (no minority pruning); W2 S_A-minority exclusion named with reason.
- **Unsupported transport / model-use refused:** request-level `transport_permission` / `admission` / `REAL_USE` → `PROHIBITED`; F6M `conditional(use="REAL_USE")` → `UNAVAILABLE / UNVERIFIED_OWNER_ADMISSION`.
- **No fabricated behavioural probability:** no `route_probability` or `selection_weight` anywhere in output; `no_route_probability`/`no_selection_weight` true; point only for complete supported synthesis.

## 6. Recorded residuals / honest limits

1. **No F6M → original E04 join.** F6P is a bounded, read-only TEST_ONLY F6 evidence client; it does **not** feed original E04 `NONPARENT_OPTIONS`, and no such claim is made. The unmatched-world/general-consumer residual and the absent owner transport/admission remain open.
2. **C cross-channel native primitive NOT_RUN.** `f6c_method_c._load_native_primitive` resolves `ROOT/staging/cand_A/…`, which is not present in the published tree (only `stage/`), so `unidentified_cross_channel` is `None` here. The no-pooling marginal bounds themselves are exercised and reproduce `total_unknown_mass = 1`; the native-primitive reuse for the cross-channel interval is unexecuted in this publication. Recorded as a bounded evidence-completeness gap, not a defect in the consumer claim.
3. W1's supported point is a `SOURCEFREE_EXPERIMENT_ONLY` experimental quantity, not a real-use/population estimate; sampling design/weight are exposed as unknown, never defaulted to 1.
4. R35 sealed-commission obsolete A pin remains an HQ succession matter (already corrected by R40 HQ memo to `fc5e37fa…`); this return does not re-seal the commission.

Verdict **ACCEPT** is scoped precisely to the source-free TEST_ONLY partial-bound evidence consumer over the actual F6M product.
