#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--current-premain", default="750548ddbb9b4392a16ce93097b856f349e16182")
    ap.add_argument("--timestamp", default="2026-10-31T00:00:52Z")
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    branches = [json.loads(l) for l in (args.src / "BRANCH_DISPOSITIONS.jsonl").read_text().splitlines()]
    functions = [json.loads(l) for l in (args.src / "FUNCTION_COURT.jsonl").read_text().splitlines()]
    branch_by_name = {b["branch"]: b for b in branches}
    fclass = Counter(f["classification"] for f in functions)
    bdisp = Counter(b["branch_disposition"] for b in branches)
    source_branches = [b for b in branches if b["changed_paths"]["source"]]
    no_source = [b for b in branches if not b["changed_paths"]["source"]]
    no_source_with_returns = [b for b in no_source if b["changed_paths"]["returns"]]
    no_evidence = [b for b in branches if not b["changed_paths"]["source"] and not b["changed_paths"]["returns"]]
    return_branches = [b for b in branches if b["changed_paths"]["returns"]]
    multi = [f for f in functions if f["inherited_repetition"] == "MULTI_BRANCH_REPETITION"]
    exact = [f for f in functions if f["classification"] == "EXACT_ALREADY_IN_PREMAIN"]
    superseded = [f for f in functions if f["classification"] == "SUPERSEDED_BETTER"]
    held = [f for f in functions if f["classification"] == "UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY"]
    adapt = [f for f in functions if f["classification"] == "UNIQUE_USEFUL_NEEDS_ADAPTATION"]
    unknown = [f for f in functions if f["classification"] == "EVIDENCE_UNKNOWN"]
    no_current = [f for f in functions if f["successor"] == "NONE_FOUND"]
    unresolved = [f for f in functions if f["compatibility"]["unresolved_imports"]]
    neg_branches = [
        b for b in branches
        if b["historical_review"]["negative_tokens"] and b["changed_paths"]["source"]
    ]

    # FIRST_CONSUMER_AND_SUCCESSOR_MAP
    entries = []
    for f in functions:
        entries.append({
            "function_id": f["function_id"],
            "historical_path": f["path"],
            "symbol": f["symbol"],
            "classification": f["classification"],
            "branches": f["branches"],
            "current_equivalent": f["current_equivalent"],
            "current_owner": f["current_owner"],
            "owner": f["owner"],
            "original_owner_locator": f["original_owner_locator"],
            "first_consumer": f["first_consumer"],
            "successor": f["successor"],
            "signature": f["signature"],
            "current_signature": f["current_equivalent"].get("signature"),
            "unresolved_imports": f["compatibility"]["unresolved_imports"],
            "integration_steps": f["integration_steps"],
            "tests_positive_negative": f["tests_positive_negative"],
            "scientific_authority": f["scientific_authority"],
            "actor_permission_authority": f["actor_permission_authority"],
            "independent_reviewer": f["independent_reviewer"],
        })
    first_consumer = {
        "schema": "PYAT_S2_FIRST_CONSUMER_AND_SUCCESSOR_MAP@1",
        "generated_at": args.timestamp,
        "repository": "maidiu/rawlsing",
        "baseline_premain": args.current_premain,
        "current_premain_final_readback": args.current_premain,
        "roster_commit": "becf0bfb04705b8fe0927dd56e7290e1dcd180a8",
        "roster_blob": "879f1b400b0e1902bc2620c7f72b271a3c89f00b",
        "source_run_s0": 41137105778,
        "source_run_s1_s5": 41142495040,
        "s2_artifact_id": 13019246227,
        "counts": {
            "branches": len(branches),
            "source_branches": len(source_branches),
            "no_source_branches": len(no_source),
            "evidence_only_return_branches": len(return_branches),
            "no_code_no_return_branches": len(no_evidence),
            "function_rows": len(functions),
            "function_classes": dict(fclass),
            "functions_with_current_equivalent": len(functions) - len(no_current),
            "functions_without_current_equivalent": len(no_current),
            "multi_branch_function_variants": len(multi),
            "unresolved_import_function_rows": len(unresolved),
        },
        "branch_dispositions": dict(bdisp),
        "entries": entries,
        "unique_useful_held": [
            {
                "function_id": f["function_id"],
                "path": f["path"],
                "symbol": f["symbol"],
                "owner": f["owner"],
                "reason": " ".join(f["classification_reasons"]),
                "first_consumer": f["first_consumer"],
                "successor": f["successor"],
                "integration_steps": f["integration_steps"],
            }
            for f in held
        ],
        "unique_useful_needs_adaptation": [
            {
                "function_id": f["function_id"],
                "path": f["path"],
                "symbol": f["symbol"],
                "owner": f["owner"],
                "unresolved_imports": f["compatibility"]["unresolved_imports"],
                "first_consumer": f["first_consumer"],
                "successor": f["successor"],
                "integration_steps": f["integration_steps"],
            }
            for f in adapt
        ],
        "evidence_unknown": [
            {
                "function_id": f["function_id"],
                "path": f["path"],
                "symbol": f["symbol"],
                "reason": " ".join(f["classification_reasons"]),
                "owner": f["owner"],
                "successor": f["successor"],
            }
            for f in unknown
        ],
        "exact_or_superseded": [
            {
                "function_id": f["function_id"],
                "path": f["path"],
                "symbol": f["symbol"],
                "classification": f["classification"],
                "current_equivalent": f["current_equivalent"],
            }
            for f in exact + superseded
        ],
        "unclassified_roster_tip": {
            "branch": "agent/reviewer-d02zr-ee66e2b",
            "tip": "506381ac0fb68086e8028f916e935c04b9b5877d",
            "kind": "UNKNOWN_REQUIRES_CONTENT_TRIAGE",
            "branch_disposition": branch_by_name["agent/reviewer-d02zr-ee66e2b"]["branch_disposition"],
            "note": "Roster marks one tip unclassified; source-level disposition is EVIDENCE_ONLY_RETURN with no changed source/test paths.",
        },
    }
    (out / "FIRST_CONSUMER_AND_SUCCESSOR_MAP.json").write_text(json.dumps(first_consumer, indent=2) + "\n")

    # NEGATIVE_AND_UNVERIFIED.md
    def short_list(items, n=20):
        return "\n".join(f"- `{x}`" for x in items[:n])

    neg_lines = []
    for b in neg_branches[:30]:
        neg_lines.append(
            f"- `{b['branch']}` tip `{b['tip']}`; tokens {b['historical_review']['negative_tokens']}; "
            f"functions {b['classification_counts']}; purpose: {b['original_purpose_summary'][:160]}"
        )
    neg_branch_text = "\n".join(neg_lines) if neg_lines else "- None"
    no_code_text = short_list([b["branch"] for b in no_evidence], 20)
    no_source_text = short_list([b["branch"] for b in no_source_with_returns[:30]], 30)
    unresolved_modules = Counter(
        m for f in unresolved for m in f["compatibility"]["unresolved_imports"]
    ).most_common(30)
    unresolved_text = "\n".join(f"- `{m}`: {n} function rows" for m, n in unresolved_modules) or "- None"
    unknown_text = "\n".join(
        f"- `{f['function_id']}` `{f['path']}` `{f['symbol']}`: {' '.join(f['classification_reasons'])[:220]}"
        for f in unknown[:25]
    )
    held_text = "\n".join(
        f"- `{f['function_id']}` `{f['path']}` `{f['symbol']}`: {f['owner']}; {f['integration_steps'][:180]}"
        for f in held[:20]
    )
    adapt_text = "\n".join(
        f"- `{f['function_id']}` `{f['path']}` `{f['symbol']}`: unresolved {f['compatibility']['unresolved_imports']}"
        for f in adapt[:20]
    )
    neg_md = f"""# S2 negative and unverified record

**Baseline:** `{args.current_premain}`. **Generated:** {args.timestamp}.
This is a sourcefree Git/AST and original-return-text investigation. No branch executable, branch test, source-native survey/response, original scientific issuer, semantic authority or production consumer was run.

## Coverage

- 175 roster branches; 175 branch disposition rows; 175 distinct tips; 1 roster-unclassified tip (`agent/reviewer-d02zr-ee66e2b`, evidence-only return, no source/test changes).
- 59 branches change source; 116 do not. 165 branches have changed return roots; 10 have neither source nor return evidence.
- 178 changed source path occurrences; 206 changed test path occurrences; 378 changed return roots.
- 218 meaningful changed function variants after filtering unchanged/trivial/test-only helpers. The filter is documented in `FUNCTION_COURT.jsonl`; 910 branch-function references map to these rows.

## Function classifications

| Class | Count |
|---|---:|
| EXACT_ALREADY_IN_PREMAIN | {fclass.get('EXACT_ALREADY_IN_PREMAIN',0)} |
| INDEPENDENTLY_REBUILT_EQUIVALENT | {fclass.get('INDEPENDENTLY_REBUILT_EQUIVALENT',0)} |
| SUPERSEDED_BETTER | {fclass.get('SUPERSEDED_BETTER',0)} |
| UNIQUE_USEFUL_READY | {fclass.get('UNIQUE_USEFUL_READY',0)} |
| UNIQUE_USEFUL_NEEDS_ADAPTATION | {fclass.get('UNIQUE_USEFUL_NEEDS_ADAPTATION',0)} |
| UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY | {fclass.get('UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY',0)} |
| EVIDENCE_UNKNOWN | {fclass.get('EVIDENCE_UNKNOWN',0)} |
| INVALID/TRASH_WITH_GROUNDS | {fclass.get('INVALID/TRASH_WITH_GROUNDS',0)} |

No function was marked `INVALID/TRASH_WITH_GROUNDS` solely from branch-level negative tokens. The rule required symbol/path-specific negative text and no positive token; no row met that bar. No function was marked `UNIQUE_USEFUL_READY` because no unique function met the simultaneous current-import, current-consumer, positive-test and no-negative-condition requirement. `UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY` means useful-looking source with positive original-return/test evidence but no current equivalent, owner/authority decision or proven current consumer; it is not adoption.

## Branches with no source and no return evidence

{no_code_text}

## Branches with no changed source but return evidence

Count: {len(no_source_with_returns)}. Sample:

{no_source_text}

## Negative original evidence (source-bearing branches)

Count: {len(neg_branches)}. This table preserves negative tokens as evidence locators, not function-level convictions. A branch may contain positive and negative evidence for different functions.

{neg_branch_text}

## Functions with no current equivalent and positive/held evidence

{held_text}

## Functions needing adaptation

{adapt_text}

## Functions with unresolved imports

{unresolved_text}

## Functions still EVIDENCE_UNKNOWN

{unknown_text}

## Tests and execution NOT RUN

- All 206 changed test paths were indexed statically only. Test function names and fault-keyword counts are in branch rows; no branch test was executed.
- No original survey/response corpus, source-native data, actor/world execution, production consumer, branch executable or arbitrary branch code was run.
- Reported test counts in return text are attributed, not independently reproduced.
- No original scientific, CAN/ADP/Pyat/SCI05/FF/N9-N12 or actor permission was issued or verified.

## Currentness and origin limits

- Current PREMAIN readback: `{args.current_premain}`. If it moves after this return, re-run the comparison at the new head.
- Tip date is not branch creation date. Multi-branch repetition is marked `MULTI_BRANCH_REPETITION`; the earliest tip is only a candidate origin, not proven authorship.
- Textual current-reference search is not a callgraph or execution receipt.
- `SUPERSEDED_BETTER` is used only for current same-path/same-symbol implementation with a larger body; it does not prove semantic excellence.
- The one roster-unclassified tip is preserved as `UNKNOWN_REQUIRES_CONTENT_TRIAGE`; its return evidence is documentary only.

## Reviewer independence

This is an original-source/code investigation and disposition author return, not an independent hostile reviewer acceptance. A new I2/I3 hostile reviewer must review the exact pushed SHA. No adoption, merge, source grant or PRE-MAIN write is made here.
"""
    (out / "NEGATIVE_AND_UNVERIFIED.md").write_text(neg_md)

    # 00_RETURN.md
    counts = first_consumer["counts"]
    example_rows = "\n".join(
        f"- `{b['branch']}` — `{b['branch_disposition']}`; source={len(b['changed_paths']['source'])}, tests={len(b['changed_paths']['tests'])}, returns={len(b['changed_paths']['returns'])}, functions={b['meaningful_function_count']}"
        for b in branches[:12]
    )
    return_md = f"""# PREMAIN R4 / PYAT RABOCHII 845-S2 — source/function/merit/successor/integration investigation

**Status:** `SOURCEFREE_STATIC_INDEX_AND_DISPOSITION_COMPLETE__NO_ADOPTION__NO_BRANCH_EXECUTION__NEW_HOSTILE_REVIEW_REQUIRED`.
**Repository:** `maidiu/rawlsing` (PRIVATE)
**Output branch:** `agent/pyat-rabochii-845-s2-function-investigation-20261030-r1`
**Baseline and final current PREMAIN readback:** `{args.current_premain}`
**Roster:** `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_S2_HEAD_ONLY_ROSTER.json` at `becf0bfb04705b8fe0927dd56e7290e1dcd180a8`, blob `879f1b400b0e1902bc2620c7f72b271a3c89f00b`.
**S0 raw index:** GitHub Actions `41137105778`.
**S1/S5 machine index:** GitHub Actions `41142495040` (completed success); S2 artifact `13019246227`, branch index sha256 `b6c2af302632287738707b4f932ad55ec38d6038a5766483a610de8a3568ae30`, variant index sha256 `68db38a3a0bb995ca1512fc42aded1f96fe073e8ea43d1f5ed0774b35276d5d1`.

**Role:** original-source/code investigator and disposition author, not PRE-MAIN integrator, source/semantic issuer, original reviewer or own hostile reviewer.
**Session/device:** `mainMac` verified by `scutil --get ComputerName=mainMac`; OpenCode `1.18.34`; model `opencode-go/deepseek-v4.1-flash`, local session variant `max`; agent `build`; actual session title `F0R3 postseed authority bypass repairs`, ID `ses_e72807b76ffeufLz4gsp3C6yVQ`; worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-845-s2-20261030-r1`. This is a sourcefree static investigation; provider-side MAX effort is unverified.
**No active-worker collision:** isolated sparse worktree at the exact baseline; no other worktree, branch or process was modified.

## Method

1. Loaded the frozen 175-branch S2 roster and verified 175 unique names, 175 distinct tips, 1 unclassified tip.
2. Reused the completed S1/S5 machine index only as a candidate locator; independently read Git trees, merge-bases, changed paths, historical/current blobs, ASTs, source/test files and original return text.
3. Compared each changed source path at branch tip vs merge-base and vs current PRE-MAIN `{args.current_premain}`.
4. Built a current PREMAIN AST/symbol index over {len(list(Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/pyat845_s2_analysis/current').rglob('*.py')))} Python files and searched for exact, normalized, same-path and same-name current equivalents.
5. Classified 218 meaningful changed function variants, preserving multiple functions and contradictions per branch. Trivial dunders, test functions and unchanged helpers were excluded from function court but their branch/test evidence is retained.
6. Read original return/test evidence; did not execute any branch code or test.

## Counts

| Surface | Count |
|---|---:|
| Roster branches | 175 |
| Distinct tips | 175 |
| Roster-unclassified tips | 1 |
| Branches with changed source | 59 |
| Branches with no source | 116 |
| Branches with changed returns | 165 |
| Branches with no source and no return | 10 |
| Changed source path occurrences | 178 |
| Changed test path occurrences | 206 |
| Changed return roots | 378 |
| Meaningful function variants | 218 |
| Branch-function references | 910 |
| Functions with current equivalent | {counts['functions_with_current_equivalent']} |
| Functions without current equivalent | {counts['functions_without_current_equivalent']} |
| Multi-branch function variants | {counts['multi_branch_function_variants']} |

**Branch dispositions:** `{dict(bdisp)}`.
**Function classes:** `{dict(fclass)}`.

## Finding → interpretation → action → owner

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| 14 functions are exact current PREMAIN AST matches; 10 are current same-path larger implementations; 0 independently rebuilt equivalents were found by normalized AST. | A bounded subset is already present or superseded at the source level. Exact AST is not adoption. | Preserve current equivalents; do not recover duplicate bytes. | Current PRE-MAIN owners; original source owners for any semantic check. |
| 194 function variants have no current equivalent. 67 look useful with positive original-return/test evidence but are held by source/owner/consumer authority; 22 need import/interface adaptation; 105 remain evidence-unknown. | Missing current path is not value and not trash. Branch-level positive/negative tokens are not function-level acceptance. | Route held/adaptation functions to original source owners and a distinct hostile reviewer; keep unknown rows explicitly unknown. | Original Pyat/CAN/ADP/SCI05 owners; incumbent HQ; new reviewer. |
| 106 branches are return/evidence-only and 10 have neither source nor return evidence. | Most of the S2 roster is documentary or evidence-only, not recoverable production code. | Preserve evidence locators; do not infer code value from branch names or age. | Incumbent HQ and original return owners. |
| One roster tip is unclassified (`agent/reviewer-d02zr-ee66e2b`). | The roster itself marks content triage incomplete. | Keep `UNKNOWN_REQUIRES_CONTENT_TRIAGE`; no source disposition invented. | S2 roster owner / incumbent HQ. |
| No function met the strict `UNIQUE_USEFUL_READY` bar; no function met symbol-specific `INVALID/TRASH_WITH_GROUNDS`. | Readiness and trash require stronger evidence than branch-level tokens. | Do not integrate or discard; hold or keep unknown. | Original owners + new hostile reviewer. |

## Three courts

- **ENGINEERING:** `STATIC_SOURCEFUNCTION_INDEX_AND_DISPOSITION_ONLY`. 175/175 branches present; 218 meaningful function rows; actual source/test/return blobs read. No branch tests or executables run.
- **SCIENTIFIC:** `HOLD`. No native CAN/ADP/Pyat/SCI05 source, survey/response, actor/world, acquired practice or first consumer was executed or issued.
- **AUTHORITY:** `HOLD`. No source/semantic/actor grant, owner adoption, PRE-MAIN write or merge. All original owners retain their decisions.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** 175-branch roster verification; exact tips/merge-bases; changed source/test/return index; 218 function court rows; current AST equivalence search; original return/test evidence read; first-consumer/successor map; negative/unverified register.
- **REMAINING:** new I2/I3 hostile review of this exact SHA; original-owner review of the 67 held and 22 adaptation functions; source/actor/FF/N9-N12 compatibility where triggered; actual tests/fault negatives; current-consumer execution; any protected owner CAS.
- **CRITICAL BLOCKERS:** no branch execution; no source-native/science/actor authority; 105 evidence-unknown function variants; 22 import/interface adaptations; current PREMAIN may move; no independent reviewer acceptance.
- **LARGEST PRODUCTIVE MOVE:** a bounded original-owner review of the held/adaptation subsets against the current PREMAIN interfaces, followed by exact tests and a new hostile adjudication; not a new census.
- **FLIGHT:** only this S2 return tree was written. No source branch, PRE-MAIN, PR, other shard, active worker or production artifact was modified.
- **DELTA:** converts a 175-name frozen roster into a complete branch/function disposition ledger with exact source cuts and explicit unknowns, without adopting or trashing unproven code.

## Tests NOT RUN

- Every branch test and every branch executable: NOT RUN.
- Original survey/response, source-native, actor/world, CAN/ADP/Pyat/SCI05, FF/N9-N12 and production consumer: NOT RUN.
- All reported test counts are attributed from original return text, not independently reproduced.

## Exact artifacts

- `BRANCH_DISPOSITIONS.jsonl` — 175 rows.
- `FUNCTION_COURT.jsonl` — 218 meaningful function variants + evidence.
- `FIRST_CONSUMER_AND_SUCCESSOR_MAP.json` — current equivalents/successor/consumer map.
- `NEGATIVE_AND_UNVERIFIED.md` — negative, unknown, missing-source and test-not-run register.
- `analysis/` — the deterministic builder and current AST inputs where preserved.

**Push readback:** the exact final remote SHA is reported after `git push` and `git ls-remote`; it is not embedded in its own committed files. No self-adoption.

## Sample branch rows

{example_rows}
"""
    (out / "00_RETURN.md").write_text(return_md)
    print(json.dumps({"out": str(out), "branch_rows": len(branches), "function_rows": len(functions), "classes": dict(fclass), "dispositions": dict(bdisp)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
