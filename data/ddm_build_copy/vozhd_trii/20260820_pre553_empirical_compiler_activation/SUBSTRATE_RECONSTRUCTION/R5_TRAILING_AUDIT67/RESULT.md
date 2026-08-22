# Authority 67 clean-rerun return

Starting commit: `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

Source: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Relevant R5 suite: `80 passed in 38.87s` (0 failed, 0 skipped).

The clean rerun completed only the authorized OA-250K and OA-2M V4 comparisons.
Carrier output byte, root, and inventory equality: PASS. Ordinary and trailing
`full_audit()` equality: PASS. No semantic difference, missed member/row,
duplicate, or reorder was observed.

OA-2M total-certification speedup: `1.202857x`
(raw: `1.2028573429833285`). OA-2M builder slowdown: `20.04%`
(raw fraction: `0.20044430368023747`). The preferred `>=1.25x` speedup gate
is MISS; the preferred `<=10%` builder-slowdown gate is MISS. Hard
queue/process/integrity gates: PASS.

Final disposition:

`R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

No further court was run, and no implementation or tuning change was made for
this persistence return.
