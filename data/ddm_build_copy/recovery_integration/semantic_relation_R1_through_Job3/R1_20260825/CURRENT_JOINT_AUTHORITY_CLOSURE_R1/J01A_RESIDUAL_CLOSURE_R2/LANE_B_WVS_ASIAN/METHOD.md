# METHOD — J01-A R2 WVS / ASIAN BAROMETER LANE

## Scope and blindness

Only WVS W1/W4/W7 and Asian Barometer W1/W4/W5 were touched. The worker started from `bb2d350d34b188db5bee9e4ac3b36919af264e16`, read the lane command and shared residual authority, and used only the frozen J01-A R1 metadata/authorized carriers plus current governed source materials. No C07/C08/C09/C10 historical carrier, historical J membership, J01-B, executable-J authority, or sibling R2 branch was consumed.

## Baseline integrity gate

Before lineage, the R1 carrier manifest SHA/bytes/rows were compared with the current Library objects. Both aliases had changed. The original manifest-bound file IDs were not materializable from the current Library surface. The mutated payloads were excluded from discovery and lineage; they were used only to establish byte-integrity mismatch.

This gate is decisive because the R2 contract requires exact one-for-one R1 lineage. A later mutable payload cannot substitute for the frozen baseline even if many rows appear plausible.

## Current-source recovery

WVS: exact current W1/W4/W7 questionnaires and codebooks were materialized and SHA-256 bound. All questionnaire pages were rendered to images; full questionnaire and codebook text was extracted. The command-authorized WVS deep catalog was hash-verified at `cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0`. The current WVS longitudinal documentation was independently searched for an explicit W1 crosswalk and found to list the variables/equivalences workbook.

Asian Barometer: the current locator ledger was searched for W1/W5 native questionnaire, codebook, data, normalized codebook, and deep-catalog names. W4 native PDF was materialized, hash-bound, rendered over all 44 pages, and fully text-extracted. The official current Asian Barometer core-questionnaire page and current data-release page were checked; the official W5 `CoreQ_W5.pdf` was reached as a 44-page PDF. Exact-title and locator-ledger searches were run independently for the current Asian deep catalog.

## WVS W1 hostile crosswalk test

The worker tested a concrete same-number counterexample rather than assuming the conflict. Native W1 `V111` and current W1 `V111` have different meanings. The current deep catalog agrees with the current codebook, not the native questionnaire numbering. Therefore `native V-number -> current same V-number` is positively rejected.

No row position, ordinal proximity, wording resemblance alone, W4/W7 analogy, or historical membership was promoted to identity.

## Source-structure review method

For materialized questionnaires, every page was rendered and every text page was extracted. Relation-language scans (`for each`, `all that apply`, rankings, repeated item blocks, explicit range headings, matrix instructions) were used only as navigation; they were not treated as exhaustive proof by themselves. Asian W4 explicit range blocks were checked directly in the full extracted source. WVS W4/W7 relation blocks were sampled and navigated across the complete text, but because exact R1 lineage was already impossible and a full semantic recourt was not finished, no exhaustive-completeness claim is made.

## Emission law

Because the exact R1 lineage substrate is unavailable, no uncertified row is written to either R2 carrier. Schema-only carrier files are emitted to satisfy the return interface without asserting an empty substantive universe. Certified counts are `null`, not zero.
