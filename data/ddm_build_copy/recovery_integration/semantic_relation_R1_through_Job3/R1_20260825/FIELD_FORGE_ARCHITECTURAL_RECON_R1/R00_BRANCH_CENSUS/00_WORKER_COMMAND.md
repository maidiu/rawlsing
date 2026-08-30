# R00 — TOTAL BRANCH-FAMILY CENSUS / ORPHAN DETECTOR

Read and obey `../00_MASTER_CAMPAIGN.md` first.

## Mission

Build the coverage skeleton for the entire `maidiu/rawlsing` repository across ALL branches. This is not deep conceptual excavation; it is a loss-prevention census that makes it difficult for later thematic workers or the central Vozhd to miss branch-stranded thought.

## Required work

1. Enumerate the full branch universe, including non-`agent/` branches if any.
2. Cluster branches into conceptual/implementation lineages using names, tip commits, ancestry, changed paths, and representative artifacts.
3. For each family, identify:
   - apparent purpose;
   - chronological span / ancestry where recoverable;
   - likely terminal / integration / control branches;
   - branches that appear to contain unique conceptual work rather than repeated implementation;
   - abandoned, temp, retry, repair, red-team, recovery, and supersession branches whose negative information may matter;
   - obvious cross-family seams.
4. Detect ORPHANS: branches or commits whose distinctive paths/commit messages are not clearly absorbed by later integration branches.
5. Produce an explicit coverage map assigning every branch family to R01–R08 where possible. Flag unassigned families.
6. Do not assume a branch is irrelevant because its name sounds implementation-only. Sample changed paths/commit messages sufficiently to justify exclusion.

## Special questions

- Which branch families are most likely to contain architecture that is NOT present on `main` or current FIELD FORGE?
- Which lineages contain repeated retries around a conceptual defect rather than mere coding defects?
- Where did branches fork into alternative conceptions rather than simple successive repairs?
- Which branches contain explicit `originary`, `wholevision`, `inheritance`, `genealogy`, `architecture`, `recalibration`, `correction`, `rejection`, `fracture`, `information-loss`, `positioned-subject`, `field`, `topology`, `phenomenology`, `development`, `authority`, or `conservation` work?

## Returns

Write the common three return artifacts required by the master command, plus:

`04_BRANCH_FAMILY_CENSUS.tsv`

Columns:
`family_id | branch | tip_sha | parent_or_base_if_known | purpose | likely_unique | likely_terminal | negative_result_value | assigned_lane | notes`

The central criterion is not elegance. It is repository coverage and orphan detection.