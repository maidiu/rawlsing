# FFP012 — CORE-C DIRECT CONDITIONAL REDISTRIBUTION PRODUCER R1 — WORKER RETURN

Status: \`PASS__EXE004_CLOSED__CORE_C_PRODUCER_IMPLEMENTED\`

Repository: \`maidiu/rawlsing\`

Worker branch: \`agent/rabochii-field-forge-r2-ffp012-core-c-direct-redistribution-r1\`

Exact starting HEAD: \`9611a9067ab28e17eb45b565398c7e604a24e77b\`

Jurisdiction: close \`EXE004\` only. No production canary, authority restoration, TTAR/PRA minting, sibling import, experiment integration, or closure of EXE001/EXE002/EXE003/EXE005.

## Result

Implemented a respondent-level \`DIRECT_CONDITIONAL_REDISTRIBUTION\` producer for one exact frozen common semantic input. The producer computes exact or explicitly bounded-backoff \`P(D|C)\` distributions and fails closed when the representation would silently change semantic states, risk-set membership, estimand identity, or analytic roles.

This implementation is explicitly non-equivalent to and does not import or relabel \`data/ddm_build_copy/ddm_v551_conditional.py\`. V551 remains a derived-determinicity bridge index; Core C is a respondent-level redistribution producer.

## Executable surface

- \`data/ddm_build_copy/ddm_ffx002_r2_direct_conditional.py\`
- \`data/ddm_build_copy/compile_ffx002_r2_direct_conditional.py\`

CLI:

\`\`\`bash
python data/ddm_build_copy/compile_ffx002_r2_direct_conditional.py \
  --input-json <bundle.json> \
  --output-json <result.json> \
  --pretty
\`\`\`

The input bundle contains:
- exact \`COMMON_SEMANTIC_INPUT_MANIFEST\`;
- frozen post-transform state registry;
- exact manifest-bound respondent risk set;
- respondent x measurement state rows with explicit positive coexposure;
- exact condition identity;
- exact outcome identity plus complete frozen destination-state list;
- support/backoff/abstention contract;
- estimand/weight-design binding;
- analytic-role binding.

## Contract coverage

### Exact condition/outcome identity
Condition predicates and outcome states must resolve to exact frozen state IDs. Unknown states fail closed. The outcome destination list must exactly equal the complete frozen outcome-state list, in frozen order; omission, pooling, merging, or rebinning is rejected.

### Exact common risk set and coexposure
The risk-set ref must exactly equal the common manifest's \`exposure_risk_set_ref\`. Every risk-set respondent must have exactly one explicitly \`exposed: true\` row for every required condition and outcome measurement. Missing response rows are never interpreted as exposure authority.

### Support, backoff and abstention
Support law is explicit. Exact condition support is tried first. Any backoff must be preregistered and may only remove exact condition predicates in a strict nested subset chain. It cannot replace a state, rebin, reorder, merge, or re-role semantics. If no admitted condition meets support, the producer emits \`ABSTAINED__INSUFFICIENT_SUPPORT\`, preserves exact support counts, and withholds probabilities.

### Full destination distribution
Every frozen destination state is always emitted, including zero-count and minority alternatives. Nonmodal/counterpattern mass is therefore not silently erased.

### Estimand / weight-design consumption
\`estimand_ref\` and \`weight_design_refs\` must exactly match the common manifest. Governed respondent weights are required when a weight design exists and forbidden when the manifest declares governed NONE. Weighted probabilities use those exact supplied weights.

### Uncertainty
The R1 numeric contract provides Kish effective-sample-size plus Wilson score intervals with explicit confidence level. The output labels this as an approximation and does not silently claim complex-survey variance support.

### Common-manifest attestation
The producer independently recomputes the SHA-256 common-manifest hash using the FFX002-R2 canonical boundary and refuses execution on post-fork hash divergence.

### Typed loss and replay receipts
Each result emits:
- \`TYPED_LOSS_RECEIPT\` with invariant statuses and explicit view/backoff/abstention loss;
- \`TYPED_REPLAY_RECEIPT\` with versioned numeric contract, input hashes, deterministic ordering/summation/rounding rules, output hash, and receipt hash.

## Synthetic hostile coverage

Synthetic-only tests cover:
1. exact \`P(D|C)\` and complete destination support including zero/minority states;
2. governed weight consumption;
3. negative coexposure rejection;
4. missing-row / missingness-as-exposure rejection;
5. lawful strict-subset backoff with explicit specificity loss;
6. honest insufficient-support abstention;
7. post-fork common-manifest tamper rejection;
8. outcome-state pooling/omission rejection;
9. backoff replacement/rebin semantic-change rejection;
10. estimand-switch rejection;
11. deterministic numeric replay under respondent-row reordering;
12. explicit non-equivalence to V551 conditional determinicity;
13. unknown-state rejection rather than rebinning;
14. post-fork analytic-role change rejection.

Validation commands:

\`\`\`bash
python -m py_compile \
  data/ddm_build_copy/ddm_ffx002_r2_direct_conditional.py \
  data/ddm_build_copy/compile_ffx002_r2_direct_conditional.py

pytest -q data/ddm_build_copy/tests/test_ffx002_r2_direct_conditional.py
\`\`\`

No production respondent data are used by these tests.

## Blocker disposition

Closed:

\`EXE004__CORE_C_DIRECT_CONDITIONAL_REDISTRIBUTION_PRODUCER_ABSENT\`

Still outside this worker's jurisdiction:
- \`EXE001__FFX002_R2_EXECUTION_HARNESS_ABSENT\`
- \`EXE002__CORE_A_CONTRACT_COMPLETE_PRODUCER_ABSENT\`
- \`EXE003__CORE_B_LOCAL_GEOMETRY_PRODUCER_ABSENT\`
- \`EXE005__FFX_HOSTILE_QUERY_ABLATION_REPLAY_RUNNERS_ABSENT\`

Terminal return:

\`PASS__EXE004_CLOSED__CORE_C_PRODUCER_IMPLEMENTED\`
