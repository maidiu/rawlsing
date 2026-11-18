# ANVIL 10k four-op semantic closure + width128 — independent G5

**Decision:** `REVISE_EXACT_DEFECT`  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc` · same OWNER branch/model  
**Author execution:** `7cc824eaca28771ec60f6d3d77236774237124ac`  
**Integrated product:** `68aa7cac…` / G5 `d74b641f8…` (unchanged)

All frozen payload manifests verify: **18/18** semantic-closure files and **14/14** width128 files, zero bad hashes.

## Material defects

### 1. Four-op expected identity sets are not actually frozen

`EXPECTED_TRUTH.json` for each operation contains `expected_cells`, counts and `checks`, but **no expected full risk/denominator identity sets**. `RESULT.json` rows contain only counts and SHA-256 hashes, not the full member lists. `derive_expected.py` indexes `row['risk_set_member_refs']` and `row['denominator_member_refs']`, which are absent from the frozen RESULT. The claimed full-set derivation is therefore not runnable against the frozen evidence. Actual full sets exist only in the payloads; expected sets cannot be compared.

This is not an entire benchmark rerun: the fix is truth/export only (derive expected sets from the pinned fixture pattern, add them to EXPECTED_TRUTH or expose actual lists in RESULT, repair derive_expected, re-freeze).

### 2. Width128 expected truth omits the observed-zero cell

Actual `f4.payload.json.gz` contains:
- cell `0`: 39, `OBSERVED_POSITIVE`
- cell `1`: 0, `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`
- risk 128, denominator 39

`WIDTH128/RESULT.json` `expected.cells` contains only cell `0`; nevertheless `checks.cells=true` and `all_expected_match=true`. The raw `query.json` stdout says `all_expected:false`. The expected truth is incomplete and the post-hoc true label is inconsistent with the raw output.

Fix: add the expected zero cell, recompute the cells check from the actual payload, correct the stale stdout label, and re-freeze; no query rerun.

**Runnable witness:** `measurement-defect-witness.py` / `.json` (exit 1).

## Residual observations

- Semantic closure raw stdout `all_expected:false`; final RESULT true. The inline check omitted cells/weighted; later truth expanded to full cells but not identity sets.
- One source-open event is `os.open('/.../.s2c-native-i03-xchwzfxa')` — a temporary native I03 session directory, **not raw source**. Python `builtins.open/os.open` only; Arrow/SQLite internal opens are not fully observable.
- Semantic closure: H 0.575 s, S 12.651 s, Q 106.187 s external; O timers 0.441/0.379/0.358/0.161 s; RSS 722,276,352 B; scratch 122,591,630 B.
- Width128: build 293.956 s, query external 45.226 s, S 22.847 s, Q 21.239 s, O 0.0048 s; sampled build RSS 200,609,792 B, query RSS 158,609,408 B; scratch 826,683,762/248,680,671 B; retained 55,187,741 B; no abort. Width H not separately timed.
- Width source pattern 80/10/10: 60,928 valid / 7,616 MISSING / 7,616 NOT_ASKED of 76,160 added cells; 68,960 events / 76,800 routing / 128 weights.
- Cumulative semantic closure + width build + width query = **445.369 s** < 900 s; caps 600/600/6GiB/4GiB. One width build, no hidden second build observed; accepted 10k estate unchanged.

## Next action

Re-export and re-freeze expected/actual full member sets for the four 10k ops and the width zero cell; correct raw `all_expected` labels. Then, if still warranted, ask **one bounded 600-column × 10k respondent resource question**; do not linearly extrapolate 10k×5 or 128×600, and do not claim full-width/science/100k.

No product edit, native rerun, new backend/engine, source/science/actor/protected grant, 100k or review campaign.
