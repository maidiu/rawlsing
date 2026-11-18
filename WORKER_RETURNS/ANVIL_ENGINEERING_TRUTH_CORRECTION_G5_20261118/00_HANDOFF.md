# ANVIL truth correction — focused independent G5

**Decision:** `ACCEPT_SCOPED_10K_FULL_SEMANTICS_AND_WIDTH128_OBSERVATION`  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc`  
**Author correction:** `a933a96e646b59276707b6a8de2bb8192e7f75ac`  
**Prior review:** `073cb420…`; raw execution `7cc824ea…` preserved

The correction manifest verifies **9/9** payload hashes with no bad entries. I executed my own frozen postprocessor over the immutable author payloads; exit **0**, `all=true`, `semantic_all=true`, `width_all=true`.

## Closed defect 1 — full 10k semantic sets

`EXPECTED_SETS.json.gz` and `ACTUAL_SETS.json.gz` now contain complete expected/actual risk and denominator identity sets for all four corrected operations:

| Op | Risk | Denom | Cells |
|---|---:|---:|---:|
| selected_weighted | 10,000 | 5,000 | 2 (+ exact weighted cells) |
| f2_forward_raw | 10,000 | 5,000 | 2 |
| f2_reverse_raw | 10,000 | 3,333 | 2 |
| repeated_mr_raw | 770 | 385 | 770 repeated-event cells |

Every check is true: cells, raw numerator/denominator, risk set, denominator set, replay ref and payload SHA; selected_weighted also has exact weighted masses. Expected identities are derived by the postprocessor from pinned `fixture_1006`/`ctx._respondent` construction, not copied from actual payload membership. Same-count member replacement fails; restoration passes. F4 is the previously independently verified e97 result; no F4 rerun.

## Closed defect 2 — width128 observed-zero cell

The corrected expected and actual width payload both contain:

- cell `0`: **39**, `OBSERVED_POSITIVE`
- cell `1`: **0**, `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`
- risk **128**, denominator **39**

Cell deletion is RED; check restoration/all is true. The actual payload, expected truth and `CORRECTED_RESULT` now agree. Width is one **128R × 600** observation only.

## History and visibility

Prior raw stdout `all_expected:false` and prior false check labels remain immutable; `SUPERSESSION.json` explicitly supersedes them without rewriting history. The one Python source-open event is a temporary native I03 session directory (`.s2c-native-i03-*`), **not raw source**; Arrow/SQLite internal opens are not fully observable.

## Cost (reused frozen observations; no new native execution)

- Semantic closure: H 0.575 s, S 12.651 s, Q external 106.187 s; O 0.441/0.379/0.358/0.161 s; RSS 722,276,352 B; scratch 122,591,630 B.
- Width128: build 293.956 s; query external 45.226 s, S 22.847 s, Q 21.239 s, O 0.0048 s; sampled RSS 200,609,792 / 158,609,408 B; scratch 826,683,762 / 248,680,671 B; retained 55,187,741 B; no abort.
- Cumulative semantic closure + width build + width query = **445.369 s** under 900 s; caps 600/600/6 GiB/4 GiB. Width H was not separately timed.

## Verdict and next

Both exact defects are closed at the frozen-payload, full-set, full-cell/weighted, zero-cell grade. This is sourcefree TEST_ONLY engineering, not original35/native science, production service/CURRENT/actor or protected acceptance.

The measured remaining resource is the width build/query plus semantic closure; the smallest next real question is **one bounded 600-column × 10k respondent observation**. Do not linearly extrapolate from 5Q or 128R; no new grant, backend, engine or production patch is created by this review.
