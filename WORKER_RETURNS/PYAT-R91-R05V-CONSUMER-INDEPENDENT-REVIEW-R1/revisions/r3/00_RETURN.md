# R91 R05V R3 independent review — return

Verdict: **REVISE.** R3 fixes the R2 false-exact status bug and duplicate
definition block, and its two-distinct-direct-composition graph is a real
positive. But graph validation still trusts internally consistent component
metadata: forged joint topology/count/order, forged discovery/recursive refs and
a real-type E41 object with a forged route are all accepted as
`LEARNED_CONSUMER_EXACT_SUPPORTED` and echoed. No actual discovery/recursive C1
linkage is exercised; the author states it is not present in the current learned
fixtures.

## Custody

- Stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-r3-consumer-review-r1`; startup/HEAD
  `737f1b143963352f201973140002d6f66dbabcaa`; clean at gate.
- R05V R3 commission `1a6ce552...`; R3 author contract
  `45cf09d55f80109114454d859aeb9b68ba6d2184`; code
  `0c416bed7fdae59cbb57a190d1ea215eae8de44a`.
- Frozen EXPECTATIONS `d6b4b3482fbc2863e3ddf4fb2ff1ff67b01c4fb1`,
  committed before R3 code.
- Code blobs match pins: learned-world `4e013062...`, test `b942370e...`.
  Only the two authorized code/test paths plus author r3 return changed.
- Accepted R08 `3ca860e4...`/`5832ce05...`; accepted C1/provider/evaluator/
  empirical owners `604c8d59/23167aa2/62e5eced/a61365b9` unchanged.
- Author R3 manifest independently recomputed: 7/7 artifacts match.

## What R3 establishes

- Author 37/37; R05V R1 exact probe replay 4/4; R2 exact probe replay 5/5;
  provider 43/43 with the exact AT07 fixture; analytical composition 13/13.
- Actual M01 → M1 → M2 → C1 → unchanged N10E positive; consumer hash
  `8e54f8b0...`.
- Two distinct actual DIRECT C1 compositions (`composition`, `composition_b`)
  produce a graph joint count 2 and same consumer assertion.
- R2 false-exact status disagreement is fixed: a producer-SUPPORTED /
  analytical-ZERO_SUPPORT composition returns typed `ZERO_SUPPORT`, not exact.
- Duplicate consumer definition block removed; one `__all__` and one active
  implementation remain.

## Remaining graph-provenance defect

`NativeProductGraph`/`_authoritative_graph` validates component metadata
self-consistency (topology arity/components, joint count/order, route labels,
duplicate hashes, E41 type/membership/consumer hash) but does not reconcile
those fields to actual native owner receipts/frontier/lineage/root-parent or
actual component results. Internally consistent invented labels still pass.

Independent probes (`probes/test_r05v_r3_actual_graph_gap.py`):

```text
forged_joint_topology:
  one actual composition with target topology arity=2, two copied components,
  joint_component_count=2 -> EXACT_SUPPORTED, joint=2;
  no second actual component result.

forged_discovery_route:
  actual direct composition relabelled I05 discovery with forged
  discovery_receipt_refs/frontier -> EXACT_SUPPORTED, forged ref echoed.

forged_recursive_route:
  actual direct composition relabelled MX01R2 recursive with forged
  handoff/lineage -> EXACT_SUPPORTED, forged refs echoed.

actual_type_e41_forged_route:
  real EmpiricalPossibilitySliceExtensionResult with producer_route changed to
  EXT_ROUTE_DISCOVERY -> EXACT_SUPPORTED, forged route echoed.
```

Two probes pass: the two-direct-component positive and the status-disagreement
typed result. Four graph-provenance probes fail. The author's two-component test
uses two direct compositions, not an actual joint/discovery/recursive product;
the author's own return admits no actual discovery/recursive C1 linkage was
exercised.

## Exact missing function/dependency

1. Reconcile component topology/joint count/order, discovery receipt/frontier,
   recursive parent/handoff/lineage/root-parent, source/operation and product
   currentness with the actual native owner objects/results. Do not trust
   internally consistent component metadata; a single actual composition with
   forged arity/components or a relabelled route must refuse.
2. Validate the E41 extension route against the actual component route and the
   actual discovery/recursive evidence it claims; a real-type extension object
   with a forged route must refuse, not echo.
3. If an actual discovery/recursive C1 composition cannot be linked to the same
   learned disposition using the existing five-path owners/fixtures, name the
   exact missing native fixture/caller dependency (for example a learned M1/M2/
   B5 disposition fixture linked to an actual I05/MX01R2 C1 composition). Do not
   fabricate labels or claim universal support. If the linkage requires a path
   outside the allowed five paths, return that exact caller/owner gap rather
   than another metadata patch.

No new authority, evaluator, provider or scientific method is required. The
two-direct positive and typed-status fix are retained partial capability.

## Limits

Full live J42/P41/E04 remains NOT_REACHED; R04 independent. No original
source/science, F6/F7/FieldForge, CI/prod, N11/N12, Sorok, J52/W52 or adoption.
The dead duplicate cleanup is not an acceptance gate and is already done.
No candidate edit, self-adoption or author wake.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_r3_observations.json`,
`probes/test_r05v_r3_actual_graph_gap.py`,
`probes/r05v_r1_immutable_probe.py`, `probes/r05v_r2_immutable_probe.py`,
`junit/*.xml`, `logs/stdout.jsonl`.
