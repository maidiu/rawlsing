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
→ 55003 proved strict tip-containment relations
→ 0 unresolved topology
```

The complete frozen branch census is `BRANCH_CENSUS.tsv`. Exact-tip aliases are in `EXACT_TIP_ALIASES.tsv`; all 581 unique tips and their maximal containers are in `UNIQUE_TIPS.tsv`; the irreducible head universe is `MAXIMAL_TIPS.tsv`; the complete strict containment relation is `CONTAINMENT_EDGES.tsv`; all pairwise relations among maximal tips are recorded as incomparable in `MAXIMAL_INCOMPARABLE_PAIRS.tsv`.

### Frozen-census integrity

The live repository had advanced Wave-1 worker refs. This court rewound only the ten exact Wave-1 branches to their common launch SHA and asserted the prior frozen invariants: 638 refs, 581 unique tips, 57 alias surplus. All invariants passed or this return could not have been written.

### Governing non-conclusion

`MAXIMAL_TIPS.tsv` is **not** a pre-main admission list. A maximal tip may later prove to be superseded, experimental, command-only, exploratory, or otherwise nonbinding. W01 establishes only that Git topology cannot collapse it into another frozen tip. Authority valuation remains outside this worker.
