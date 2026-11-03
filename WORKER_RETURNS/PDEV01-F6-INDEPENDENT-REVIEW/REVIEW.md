# PDEV-01 F6 comparison — independent review

**Candidate:** `aa18b6b8547c954d844bb0dcf94f70e2e14f15b0`
**Review checkout:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6-review`
**Role:** distinct independent reviewer; sourcefree TEST_ONLY; not issuer or adopter
**Write scope:** `WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/` only

## Verdict

**`REVISE_ENGINEERING__SCIENCE_AND_AUTHORITY_HOLD_UNCHANGED`**

The candidate's central receiver comparison reproduces: actual F6M bundles reach
the actual F6P consumer with the stated bounds, uncovered mass and point refusal;
the pinned WP2 expression does fail on the F6P shape with a raw `KeyError` for
`native_bundle`. This verifies F6P as an actual named consumer; it does not
independently establish a history-wide claim that F6P was chronologically first.

The candidate's engineering evidence is **not accepted as written** because it
labels that raw exception as a "typed mismatch" with the code
`F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR`. That code is authored by the
candidate's own `run_comparison.py:68`; it is not emitted by F6P, not emitted by
WP2, and not a typed refusal. The candidate also records
`NO_NONPARENT_OPTIONS_READ` as a read effect without executing WP2's receiver.

Science and authority are unchanged: F6M/F6P remain sourcefree TEST_ONLY
evidence; no original source, population, transport, model-use, N9/N11/N12,
adoption or downstream wake is created. The core comparison is useful and
replayable at semantic level, but the diagnostic wording and test coverage must
be corrected before independent acceptance.

## Independent replay

The reviewer imported the candidate's staged F6P implementation and actual F6M
fixture producer, not a fixture reimplementation. The candidate's
`run_comparison.py` was deliberately not invoked because it writes its own
evidence file; the reviewer reproduced the same calls in its own replay script.

| World | F6P state | uncovered | point | bounds |
|---|---|---:|---|---:|
| W1 full coverage | `SUPPORTED_SYNTHESIS` | `0` | `{formal: 5/8, informal: 3/8}` | 4 rational cells |
| W2 mixed eligibility | `PARTIAL_IDENTIFICATION` | `1/4` | `None` | 4 rational cells |
| W7 source excluded | `PARTIAL_IDENTIFICATION` | `1/2` | `None` | 4 rational cells |
| W3 minority absent | `PARTIAL_IDENTIFICATION` | `1/5` | `None` | 4 rational cells |

Verified independently of the candidate's summary:

- W1 point equals the frozen oracle `5/8, 3/8`.
- W2 covered subprobability is `1/4, 1/8, 3/16, 3/16`; `S_A / minority` is
  excluded for `AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT`; no point.
- W7 covered subprobability is `3/20, 1/10, 1/8, 1/8`; `S_A` is excluded in
  both strata; no point.
- W3 has `1/5` uncovered and `S_A` and `S_B` minority exclusions for
  `NO_SOURCE_STRATUM`; no point.
- In every world, covered mass + uncovered mass = 1 exactly; every bound has
  rational `lower <= upper`; the covered cell lies inside its bound; the bias
  bounds widen the base bounds.
- F6P records the exact F6M source blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`
  and SHA-256 `2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871`.
- `real_use_authorized=false`, `no_route_probability=true`,
  `no_selection_weight=true`, transport unpermitted, weight never defaulted.

W2 exact bounds observed: `secure|formal [1/5, 11/20]`,
`secure|informal [3/40, 17/40]`, `insecure|formal [3/16, 7/16]`,
`insecure|informal [3/16, 7/16]`. Full bounds for all worlds are in
`evidence/replay_f6_review.json`.

## WP2 boundary — raw exception vs authored label

The pinned WP2 blob is `55e567e4d0780c251bf949268d3d477abdc76a9b` (commit
`f7824794bc6674c662734c9a8b110dd3df224be7`); line 94 contains the exact F6M
sidecar expression:

```python
dict(bundle_hash=v["native_bundle"]["content_hash"],
     conditional=v["native_conditional_consumer"])
```

Applying that expression to the actual F6P W2 result produces:

```text
type: KeyError
args: ("native_bundle",)
str:  'native_bundle'
first missing field: native_bundle
```

There is **no** `F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR` exception type in
F6P or WP2. The string occurs only in the candidate's comparison harness at
`run_comparison.py:68` (and in the candidate's own evidence/return). The
candidate's use of `except Exception` would also label unrelated failures with
the same code. The candidate's test suite asserts the authored code rather than
the raw exception, so it does not independently test the distinction.

The structural conclusion survives: F6P supplies `input_bundle` and
`conditional`, not WP2's `native_bundle` and `native_conditional_consumer`.
`NO_NONPARENT_OPTIONS_READ; NO_F6M_E04_JOIN` is an authored structural inference;
this review did not run WP2's full `product()` receiver, so it does not report
that string as an observed read effect.

## Current receiver absence — exact scope

At the exact candidate tree `aa18b6b85`:

- There are **zero** `rawlsing_next` matches for
  `F6P_PARTIAL_BOUND_EVIDENCE`, `consume_f6m_evidence`,
  `uncovered_target_mass`, `f6_sidecars`, or `native_bundle`.
- The only tracked `wp2.py` is the candidate's staged historical test port
  `WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py`; the repository has no
  current production WP2 source.
- The current N9/N10W progressive candidate has no F6 schema/import reference.
- `pre553_source_relations.py::guard_estimand_composition` returns an
  `OperationGuardReceipt` and has no F6P composer or bounds reader.

This supports "no current F6P receiver at this exact tree." It does **not**
prove absence in unmerged branches, remotes or untracked worktrees; no such
global claim is made.

The candidate's F6C independence claim was also checked at its pinned historical
commit `c1ebe091fa2bd12b254e5599cf37975fe438d462`. The copied
`f6c-wp2-substitution-receipt.json` names `wp2_sub_{B,A,A0}.json` but does not
embed those outputs. Reading the pinned historical outputs shows the nonparent
consumer, generic input without `f6_sidecars`, actual C1 returns and cases are
invariant across B/A/A0; the F6 sidecars differ by method variant. Thus the
claim is supported by the historical outputs, but not by the copied receipt
alone.

## Determinism qualification

The candidate's `run-comparison.seed0.json` and `seed1.json` are byte-identical
in the author root. Independent replay from a different checkout root reproduces
all semantic fields, but not the F6P `output_hash`: F6P embeds the absolute
`source_product.module_file` and includes it in the hash. For example, W1 is
`20f1d417...` in the candidate evidence and `2fbe5cff...` in this review. The
difference is path-only; normalized summaries are equal. This is a
reproducibility qualification, not a changed estimand. The candidate did not
claim cross-root byte identity, but its evidence should not be treated as
portable output-byte identity.

## Exact test receipts

| Suite | Result | Log |
|---|---:|---|
| Reviewer replay/tests | **7 passed** | `logs/review_tests.log` |
| F6P implementation 7d7, seed 0 | **26 passed** | `logs/f6p_impl_seed0.log` |
| F6P implementation 7d7, seed 1 | **26 passed** | `logs/f6p_impl_seed1.log` |
| F6P publication 912, seed 0 | **32 passed** | `logs/f6p_pub_seed0.log` |
| F6P publication 912, seed 1 | **32 passed** | `logs/f6p_pub_seed1.log` |
| F6P independent reviewer, seed 0 | **8 passed** | `logs/f6p_reviewer_seed0.log` |
| F6P independent reviewer, seed 1 | **8 passed** | `logs/f6p_reviewer_seed1.log` |
| Candidate five historical tests | **5 passed** | `logs/five_tests_review.log` |

Exact pins: candidate HEAD `aa18b6b85`; startup `773bb412a`; WP2 blob
`55e567e4...`; F6P consumer blob `8fa99289...`; F6M blob `2df811d7...`;
corrected A blob `fc5e37fa...`; A0 blob `182cc797...`; independent F6P test blob
`3b42b05e...`.

## Required engineering corrections

1. Replace `first typed mismatch` / `code:
   F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR` with the observed raw
   `KeyError('native_bundle')`.
2. Remove or qualify `NO_NONPARENT_OPTIONS_READ` as an authored structural
   inference unless a full WP2 receiver execution is supplied.
3. Narrow `except Exception` to the observed boundary or explicitly label any
   diagnostic as comparison-local; do not imply WP2/F6P emitted it.
4. Add a test that asserts the actual exception type/args and that the authored
   label is absent from both receiver sources.
5. State the F6C outputs separately: the copied receipt is not self-contained;
   the pinned historical `wp2_sub_{B,A,A0}.json` outputs are the evidence.
6. Record that F6P output hashes are checkout-root-sensitive because of the
   absolute `module_file`.

## Science and authority holds

- No original SAV/DTA or original-source read was performed.
- F6M/F6P are sourcefree TEST_ONLY artifacts; no population, weights,
  transport, model-use, route probability or selection weight is created.
- No pooling, common-respondent inference or point under uncovered mass.
- F6M remains `PARTIAL_IDENTIFICATION_ONLY_WHEN_UNCOVERED`; F6P remains a
  sourcefree evidence consumer, not an installed receiver.
- No production code, compiler, prior accepted evidence, CI, merge or
  downstream wake was changed.
- Independent acceptance is not granted by this review; the candidate remains
  subject to correction and re-review.
