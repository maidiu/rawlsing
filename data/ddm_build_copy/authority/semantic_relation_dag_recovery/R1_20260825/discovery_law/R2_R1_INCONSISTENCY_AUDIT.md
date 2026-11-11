# T06 Checkpoint R1 Internal Inconsistency Audit — R2

## Verdict

**FAIL for the saved T06 stated/intended narrowing claim; PASS for package byte integrity.**

Checkpoint R1 is preserved as immutable ancestry, but its narrative/status claim that the saved
`T06_NORM_STATED_CONDUCT_RECALL_PAIRS.csv` contains **44 same-wave review pairs** and recovers
**2 known R6 T06 canaries** is not substantiated by the saved CSV bytes.

## Direct byte/data findings

- R1 saved CSV SHA-256: `1d37082bb5dcd12051897ee5e4dea554922e586a01fd46a83fb075ee0e6bc2ab`
- Saved CSV data rows: **313**
- Saved CSV `known=True` rows: **0**
- Saved CSV `known=False` rows: **313**
- Occurrences of any of the four semantic-unit IDs participating in the two sealed R6 T06 canaries: **0**

The four sealed canary semantic units absent from the saved R1 CSV are:

- `p2xsafe__b78b1f88ee7fe5a2` — EVS 1999 `v278`, willingness to help elderly people
- `p2xsafe__4363881d3493db4a` — EVS 1999 `v281`, help elderly: moral duty
- `p2xsafe__7995f1c9863f16e7` — EVS 1999 `v279`, willingness to help immigrants
- `p2xsafe__c1c46e11bba5613d` — EVS 1999 `v286`, help immigrants: moral duty

R1 `CURRENT_STATUS.json`, by contrast, records:

- `T06_stated_intended_same_wave_review_pairs = 44`
- `T06_known_positive_canaries_recovered = 2`

Therefore the report/status and the saved T06 artifact diverge.

## Constitutional interpretation

This does **not** invalidate the sealed R6 relations or the broader S14 repair diagnosis.
It invalidates only the R1 checkpoint's claim that its saved T06 stated/intended recall CSV
demonstrates the reported 44/2 result.

The exact failure class is the same class R3 is designed to prevent:
a validator/report can be green with respect to package hashes while the payload does not
substantiate the semantic claim made about it.

## R2 correction

R2 reconstructs the stated/intended branch from the sealed canonical implementation registry
and R6 relation authority. The replacement artifact is:

`NARROWING/T06_STATED_INTENDED_RECONSTRUCTION_R2.csv`

It contains **11** fully dispositioned rows and explicitly recovers both sealed R6
T06 relations as `KNOWN_R6_ACCEPTED_T06_CANARY`. It does not claim that the R1 number 44 was
the correct denominator.

R1 remains immutable history; R2 supersedes the T06 narrowing claims for execution.
