# PR-ready receiving text — consolidate into the existing product PR

## Title

`P2 product receiving: final imported-source delta over accepted 25d40806`

## Body

This is a receiving-delta update for the existing product PR line, not a request for a second protected PR.

- Preserve the independent `ACCEPT_SCOPED_TEST_ONLY` for `25d40806d15516b7f7ffa04f47bc651022c6f2b0` at review `332e00cb3da51b859a408a31f820b1afd7fe8fc0`; it does not automatically extend to this newer head.
- Final product delta: `4b2fed81c3f513eb4262ad5de277ce519c74c614` over exact product `25d40806`; current guide PR699 source `b6d3f8d2b946a38f6336361c2b625c1260699100`.
- Protected base remains `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`.
- Selective composition: 665 product files + 9 guide files → final composite tree `f5debb10c53b8e9a735f6fe1e1696bfbf46412fc`; 674 changes vs protected base. Delta vs prior protected receiving composite `3894541e`: 80 files.
- Merge-tree compatibility is clean: product `07f32261`, guide `36b5341f`, combined `1e1bc686`; no product/guide path collision.
- Actual final cold first-consumer chain from snapshot: ACTUAL material `0`, later C9 ineligible, observation encounters `0`, explicit DO_HELP `0→1` and refused, outside cold action blocked, local return restores portal, UNKNOWN preserved, final verify `ok=true`.
- Imports originate from the receiving snapshot; public privacy clean; canonical guide verifier PASS.
- Reused focused custody: 7 fanin, 8 later author, 6 interval author tests; no full 7+8+6 or 55-suite rerun. One cold CLI chain executed for this final delta.

## Review / merge limit

Final head `4b2fed81` is **not independently accepted**; interval secondary and later public-boundary component closures remain pending. Later-event `76fdb624` original `REVISE` and public-CLI limits remain historical. No native/science/human/B grant. HQ should consolidate this delta into the existing product receiving PR rather than creating a duplicate protected PR; merge requires the competent PRE-MAIN owner and independent closure.
