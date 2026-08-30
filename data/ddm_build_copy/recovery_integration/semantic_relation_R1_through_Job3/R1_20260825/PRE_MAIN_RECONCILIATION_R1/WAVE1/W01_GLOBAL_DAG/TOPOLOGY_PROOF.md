# W01 GLOBAL DAG — EXHAUSTIVE TOPOLOGY PROOF R1

## Jurisdiction

Topology only. No branch is classified as worthy, canonical, superseded, garbage, exploratory, binding, or suitable for pre-main. No Wave 2 work is performed.

## Frozen-census reconstruction

The prior frozen observation established the invariant sequence:

- `638` branch refs
- `581` unique tip SHAs
- `57` exact-tip alias surplus

The ten Wave-1 workers were all launched from exact SHA `0777a34e50221bde6801dbaca26c058a7350c9e8`. The live repository necessarily moved those worker refs after the snapshot. This reduction therefore rewinds **only those ten exact Wave-1 refs** to the common launch SHA and leaves every other observed ref unchanged. The reconstructed census reproduces all three frozen invariants exactly; failure of any invariant aborts the court.

## Exhaustive ancestry method

1. Collapse the 638 frozen refs by exact SHA to 581 unique tips.
2. Materialize the union commit graph reachable from all 581 tips in one `git rev-list --topo-order --parents` pass.
3. Assign one bit to each unique frozen tip.
4. Propagate descendant-tip bitsets from every commit to its parents in topological order.
5. For frozen tip `A`, any other frozen-tip bit present at `A` is a mathematical proof that `A` is a strict ancestor of that tip.
6. A frozen tip is topologically maximal iff no other frozen-tip bit reaches it.
7. Every non-maximal tip is mapped to every maximal tip that contains it.
8. `CONTAINMENT_EDGES.tsv` emits the complete strict ancestry relation among frozen unique tips; `MAXIMAL_TIPS.tsv` emits the irreducible independent tip set.

## Sibling blindness

The reducer reads ref names, commit SHAs, commit parent edges, and tip commit metadata only. It does **not** read sibling worker return files, diffs, source files, semantic claims, or branch payloads. Later Wave-1 sibling tips are explicitly excluded from the frozen census by rewind.

## Semantic non-conclusion

Topological maximality says only that Git cannot collapse a tip into another frozen tip. It says nothing about whether that tip contains living project capital or should be admitted to pre-main. Those questions remain for later authority courts.
