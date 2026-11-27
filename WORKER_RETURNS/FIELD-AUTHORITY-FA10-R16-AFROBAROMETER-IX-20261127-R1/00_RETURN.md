# FA10 R16 — Afrobarometer IX execution return

**Disposition:** `EXECUTED_SOURCEFREE_CANDIDATE / STRUCTURAL RECEIVING ONLY / SCIENTIFIC AND FULL-FACTORIAL ACCEPTANCE HELD`.

This return contains Afrobarometer Round 9 source-metadata work only. It contains no respondent-level observations, no WVS7 analysis, and no WVS7 transfer. The original controller-side return and frozen assets were not modified.

## Implementation and execution

`implementation/` carries the FA10 R16 extension patch, implementation module, and the sequential Afro worker/provider entrypoints. The actual source-bound stage packets, provider inputs/outputs, receipts, rejections, accepted responses, and projections are retained under `afro/core/`. Each accepted stage response was revalidated against its exact saved packet; all A/B/C/D projection artifacts are present. These are structural receipts, not scientific acceptance or a complete matched factorial verdict.

`afro/lineages/` preserves the scoped A–D source corrections, failed and successful repairs, exact scoped receiving artifacts, and integrated candidate projections. The four receiving notes state the source and authority limits for each arm.

`afro/experiments/P1_exact_reveal/` contains the bounded exact-retrieval comparison. `afro/experiments/P2_subtle/` contains the matched six-field Afro comparison, source-first and blind review, both original responses, the post-review exact-source audit, and a separately received two-path neutral correction. P2 found a modest reviewed coverage advantage for the directed response, not a decisive accuracy winner. The post-review audit found and repaired a nonliteral Q28 quote and imprecise Q22B code-3 description; the original comparison remains unchanged.

## Method findings

- Ask the first reader which exact scope, alternative, or denominator would change before revising an upstream reading.
- Keep a revised source reading versioned as a sidecar, and reconsider only dependent inquiries.
- Treat source literal accuracy and reviewer adequacy as separate checks: the P2 blind review missed two defects caught by the later exact-source readback.
- Preserve agency, respondent/interviewer role, answer grain, routing and eligibility as separate questions; the codebook alone does not establish local administration or observed respondent relations.

## Limits and next use

There is no complete four-arm baseline comparison, no overall R16 scientific verdict, no respondent-level finding, and no native form/routing/rights issuance. The scoped reviewer receipts do not confer those authorities. No protected/common progress record was changed. The repository receiving PR is a durable worker-return surface only; it is not protected adoption.

The local publication copy substitutes `$HOME` for machine-specific home-directory prefixes in copied artifacts. `PATH_REDACTIONS.json` records each original and published hash; exact originals remain unchanged in the local controller archive.
