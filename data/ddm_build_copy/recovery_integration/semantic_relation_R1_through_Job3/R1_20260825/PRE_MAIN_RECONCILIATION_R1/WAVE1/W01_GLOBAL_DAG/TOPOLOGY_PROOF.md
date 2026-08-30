# W01 GLOBAL DAG — EXHAUSTIVE TOPOLOGY PROOF R1

## Jurisdiction

Topology only. No branch is classified as worthy, canonical, superseded, garbage, exploratory, binding, or suitable for pre-main. No Wave 2 work is performed.

## Frozen-census reconstruction

The banked frozen observation established the invariant sequence:

- `638` branch refs
- `581` unique tip SHAs
- `57` exact-tip alias surplus

The ten Wave-1 workers were launched from exact SHA `0777a34e50221bde6801dbaca26c058a7350c9e8`. The transient raw ref response from the original snapshot is no longer readable, so the final reducer reconstructs that frozen mapping rather than claiming a byte-for-byte replay.

`FREEZE_RECONSTRUCTION_AUDIT.json` independently tests the reconstruction against the later repository state. Excluding the synthetic trigger branch, the live repository contains `638` refs, `591` unique tips, and `47` alias surplus. Exactly ten refs—the ten Wave-1 branches—have moved from the common launch SHA. Rewinding exactly those ten refs produces `638 / 581 / 57`, exactly the banked frozen invariants. The live-minus-reconstructed delta is exactly `+10` unique tips and `-10` alias surplus.

The earliest post-launch Wave-1 tip commit is timestamped `2026-08-30T12:08:38-04:00`. The audit finds zero non-Wave-1 refs whose current tip committer timestamp is at or after that boundary. This is high-confidence evidence that the observed post-snapshot ref movement is exhausted by the ten launched workers under normal append-only branch evolution.

Residual epistemic limit: present Git state cannot disprove an unobserved force-update of a non-Wave-1 ref to an older pre-existing commit. That theoretical possibility is recorded rather than laundered into certainty; no evidence of such a movement was found.

## Exhaustive ancestry method

1. Collapse the 638 reconstructed frozen refs by exact SHA to 581 unique tips.
2. Materialize the union commit graph reachable from all 581 tips in one `git rev-list --topo-order --parents` pass.
3. Assign one bit to each unique frozen tip.
4. Propagate descendant-tip bitsets from every commit to its parents in topological order.
5. For frozen tip `A`, any other frozen-tip bit present at `A` proves that `A` is a strict ancestor of that tip.
6. A frozen tip is topologically maximal iff no other frozen-tip bit reaches it.
7. Every non-maximal tip is mapped to every maximal tip that contains it.
8. `CONTAINMENT_EDGES.tsv` emits the complete strict ancestry relation among frozen unique tips; `MAXIMAL_TIPS.tsv` emits the irreducible independent tip set.

The exhaustive reduction yields:

- `22` exact-tip alias groups;
- `57` alias-ref surplus;
- `55,003` strict containment relations among frozen unique tips;
- `367` topologically maximal tips;
- `67,161` pairwise incomparable maximal-tip pairs (`367 choose 2`);
- `0` unresolved relations **within the reconstructed frozen Git graph**.

## Sibling blindness

The reducer reads ref names, commit SHAs, commit parent edges, and tip commit metadata only. It does **not** read sibling worker return files, diffs, source files, semantic claims, or branch payloads. Later Wave-1 sibling tips are excluded from the frozen census by the exact ten-ref rewind.

## Semantic non-conclusion

Topological maximality says only that Git cannot collapse a tip into another frozen tip. It says nothing about whether that tip contains living project capital or should be admitted to pre-main. Those questions remain for later authority courts.
