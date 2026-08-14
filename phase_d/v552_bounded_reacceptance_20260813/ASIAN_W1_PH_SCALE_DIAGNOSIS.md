# Asian Barometer W1/PH Scale Diagnosis

## Classification

All four frozen distributions are `V552_TRANSFORM_DEFECT`.

The governed codebook records, for q065, q072, q122, and q148, source codes `1 = Strongly agree` through `4 = Strongly disagree`, with source-scale metadata `scale_min=1`, `scale_max=4`, and `scale_direction=descending`. The frozen atoms also carry supplied `response_intensity` coordinates: code 1 is `1.0`, code 4 is `0.0`, with intermediate coordinates as applicable. Those values are coherent source-scale coordinates after the descending source ordering is applied. The source labels and current semantic directions agree.

The defect was precedence: `_source_response_intensity()` reconstructed from `ordinal_rank` before consulting supplied `response_intensity`. Because these inherited atoms carried `ordinal_rank` on a normalized `0..1` scale while their source scale metadata was `1..4`, the fallback reconstructed code 1 as zero. That produced a positive response with canonical signed value `-1` and correctly triggered `direction_scale_inconsistency`.

The repair now uses supplied `response_intensity` first and only uses ordinal reconstruction when the supplied coordinate is absent. Relation projection and item reversal remain separate and untouched.

For compatibility with inherited v2.1 atoms, the repair retains one explicit exception: a neutral row carrying legacy `response_intensity=0` falls back to its ordinal midpoint when available. This prevents a legacy magnitude zero from becoming canonical `-1`; it does not affect Asian Barometer W1/PH, which has no neutral selected categories.

## Results

- Asian-only rerun: `READY_V552_STRUCTURAL_PRESSURE_CONTRACT`
- candidates: 4
- observed pressure: 4
- noncomputable pressure: 0
- invalid output rows: 0
- all-nine V552 rerun: 9/9 ready, 0 invalid rows
- focused transform and existing contract regressions: 14 passed

## V552J boundary

V552J was not accepted because the existing V551J handoff tree does not satisfy the current required artifact contract. For example, the Asian run has `v551j_readiness_report.json` and `v551j_review_surface.parquet`, while the current V552J court requires certification/readiness reports and `v551j_reviewable_evidence_sidecar.parquet`. It also reports `BLOCKED_PACKET_CONTRACT` with 25 review packets and 50 denominator issues. No aliases or synthetic certification artifacts were created.

`V553 WAS NOT EXECUTED.`
