# ZAK02S Round 5 — Corrections the predecessor missed, with exact counterevidence

**Immutable inputs:** historical `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e`; prior documentary candidate `9eac116260c009c3ec4acc63b6313130fc3a0e1b`. **S1 source-only.** No historical-function tests, engineering, CI dispatch, independent scientific authority, protected merge, or program execution.

## Refuted: R4's “two missing V551J packet filenames”

Selected `compile_v551j_joint_evidence_packets.py` emits `v551j_certified_joint_packet_index.parquet` in frame_targets **and subsequently** emits the old-name `v551j_certified_packet_index.parquet` with `compatibility_certified_packet_index` at L1538–1551 (EV0124). R4 only inspected frame_targets. Hence the assertion that the legacy certified index is absent is wrong, even though the old resolver requires nonempty certified rows. The previous EV0121/0122 remain present with R5 corrective notes, and EDGE0048/GAP0036 are revised.

## What is genuinely still unproved

`resolve_pipeline_lineage_impl.py` L479–499 requires both nonempty certified and `v551j_reviewable_evidence_sidecar.parquet`, plus `v551j_certification_readiness_report.json` and `v551j_review_readiness_report.json`. The selected compiler imports the older sidecar builder but does not invoke it on its selected path and writes newer `v551j_review_surface.parquet` and consolidated `v551j_readiness_report.json` (EV0125/0126/0128). The older sidecar independently filters *evidence-backed* review-only observations; equivalence to the modern review surface is unproved. The 20-variable smoke summary at `run_20var_allwaves_v550_552j_smoke_impl.py` L1049–1107 explicitly accepts old/new paths and readiness fallback (EV0127); it is a **real alternate static reader**, not an observed selected production execution. Separate older report paths are GAP0037.

## Challenge we deliberately refuted

A V551J component-denominator disagreement may be present in a candidate before final certification, but `certify_v551j_v2_2_3` explicitly gates `component_denominator_contract_gate` on `denominator_separation_status == PASS` and denies certification/permissions otherwise. `ddm_v551j_validation.py` also refuses non-PASS (EV0129/0130). **No unchecked certification defect established.** This is negative counterevidence, not another invented bug.

## Separate, bounded V550 source-authority caveats

`ddm_v550_clouds._question_cloud_meta` uses Python `bool(value)` for authorization/status flags: a string `"false"` would be truthy; Boolean `False` would not. The current QUC builder generally supplies typed role-use Booleans; a wrongful selected native source is **unproved** (EV0131/0133, GAP0038). Separately, generic `build_co_signature_rows` defaults a missing/blank allow field to allowed and examines nonexcluded columns if no feature allowlist is supplied. This narrows R4's blanket “specifically allowlisted” characterization; it does not prove a science bypass because the V551 bridge treats the artifact as disabled diagnostic (EV0132/0133, GAP0039).

## Explicit truth grades and future utility

19 **provisional** historical T (OPEN DISCOVERY), 228 unchanged T×domain cells (45 located source locators; 15 unresolved; 168 uninspected); 54 distinct mechanism records, 133 evidence IDs, 35 reverse readers, 56 bounded searches, 39 unresolved cases. Original nine obligations 9/9 accounted and 0/9 newly discharged. No native original operation, scientific issuer, qualified first consumer, or integration acceptance granted. Future read-only priority: trace selected legacy report/sidecar producer and native issuer, then actual V550 field types and source feature qualifications. Engineering remains a separate commission.

## R5 final R1 link closure

Two independently grounded current operations now have explicit records: `ZAK02:OP:N0014_COMPAT_WRITER` → `ZAK02:SHAPE:V551J_CERTIFIED_COMPAT_ALIAS` → `ZAK02:REVERSE:034`, and `ZAK02:OP:N0014_SMOKE_READ` → `ZAK02:SHAPE:V551J_SMOKE_SUMMARY` → `ZAK02:REVERSE:035`. Both are **static implementation traces**, not executed first-consumer proof. Their four corresponding DATA_SHAPES and AUTHORITY_USE:T0014 updates prevent orphaned references.
