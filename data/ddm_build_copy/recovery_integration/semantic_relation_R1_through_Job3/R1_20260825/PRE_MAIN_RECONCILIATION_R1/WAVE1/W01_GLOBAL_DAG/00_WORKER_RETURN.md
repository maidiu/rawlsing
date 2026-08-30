# PRE-MAIN RECONCILIATION R1 — W01 GLOBAL DAG

## FINAL WORKER RETURN — TOPOLOGY CLOSED

**Jurisdiction:** topology only.  
**Semantic authority adjudication:** not performed.  
**Wave 2:** not started.  
**Frozen launch SHA for all Wave-1 refs:** `0777a34e50221bde6801dbaca26c058a7350c9e8`.

### Exact reduction

```text
638 frozen refs
→ 581 unique tip SHAs
→ 22 exact-tip alias groups / 57 alias-ref surplus
→ exhaustive strict-ancestry reduction
→ 367 topologically maximal independent tips
→ 55,003 proved strict tip-containment relations
→ 0 unresolved Git-topology relations
```

The complete reconstructed frozen branch census is `BRANCH_CENSUS.tsv`. Exact-tip aliases are in `EXACT_TIP_ALIASES.tsv`; all 581 unique tips and their maximal containers are in `UNIQUE_TIPS.tsv`; the irreducible head universe is `MAXIMAL_TIPS.tsv`; the complete strict containment relation is `CONTAINMENT_EDGES.tsv`; all pairwise relations among maximal tips are recorded as incomparable in `MAXIMAL_INCOMPARABLE_PAIRS.tsv`.

### Frozen-census reconstruction proof

The original frozen observation was banked before exhaustive reduction as three invariants: **638 refs / 581 unique tips / 57 alias surplus**. The transient raw API response is no longer readable, so the final court does not pretend to possess a byte-for-byte copy of that response.

The repository-level reconstruction audit in `FREEZE_RECONSTRUCTION_AUDIT.json` establishes:

- current live refs, excluding the synthetic execution-trigger ref: **638 refs / 591 unique tips / 47 alias surplus**;
- exactly **10** Wave-1 refs have moved from the common launch SHA;
- every one of those ten current tips is a descendant of `0777a34e50221bde6801dbaca26c058a7350c9e8`;
- rewinding exactly those ten refs, and no others, reproduces the frozen invariants exactly: **638 / 581 / 57**;
- the live-minus-reconstructed delta is therefore exactly **+10 unique tips / -10 alias surplus**;
- the first post-launch Wave-1 commit is timestamped `2026-08-30T12:08:38-04:00`;
- **0 non-Wave-1 refs** currently point to tips with committer timestamps at or after that first Wave-1 execution commit.

That makes the reconstructed frozen mapping **high-confidence and fully consistent with the banked snapshot invariants under normal append-only branch evolution**. The audit explicitly preserves one theoretical limit: GitHub's present ref state cannot disprove an unobserved force-update of a non-Wave-1 ref to an older pre-existing commit. No evidence of such a movement was found, and no such assumption is converted into semantic authority.

### Sibling blindness

The exhaustive reducer consumed ref names, commit SHAs, commit-parent topology, and tip commit metadata only. It did not read sibling worker return files, diffs, source payloads, or semantic claims. The later sibling returns were excluded from the frozen court by the exact ten-ref rewind.

### Governing non-conclusion

`MAXIMAL_TIPS.tsv` is **not** a pre-main admission list. A maximal tip may later prove to be superseded, experimental, command-only, exploratory, or otherwise nonbinding. W01 establishes only that Git topology cannot collapse it into another frozen tip. Authority valuation remains outside this worker.
