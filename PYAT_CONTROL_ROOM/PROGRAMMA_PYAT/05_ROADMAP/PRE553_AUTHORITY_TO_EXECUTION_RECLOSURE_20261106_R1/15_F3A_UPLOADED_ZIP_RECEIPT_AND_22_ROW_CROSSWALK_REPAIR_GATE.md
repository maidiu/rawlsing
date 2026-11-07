# PROGRAMMA PYAT #716 — F3-A ZIP UPLOADED AND MECHANICALLY VERIFIED; 22-ROW CROSSWALK REPAIR REQUIRED

**Intake grade:** `F3A_ZIP_INTEGRITY_PASS__HASH_LEDGER_INTERNALLY_COHERENT__58_ROW_CROSSWALK_REPAIR_REQUIRED__MAC_ORIGINAL_INDEPENDENT_REREAD_NOT_RUN__DURABILITY_HOLD__NO_LIVE_PROMOTION`. **This is incumbent HQ deterministic ZIP/ledger receiving, NOT the independent nonauthor #744 source review or Mac source byte reread.**

## ZIP actual measured identity

- User uploaded `F3A_LOCAL_CUSTODY_RETURN_20261107.zip` into ChatGPT, exact **29,931 bytes** and **SHA-256 `760d09117e515509227b8429d2a6c042f957f534aa4b58e936df8d047f981239`** — independently recomputed exact PASS.
- 10 safe-named regular-file ZIP members, 9 required `00–08` documentary files plus `F3A_SHA256SUMS.txt`; ZIP CRC validation passes, **9/9 documented individual file SHA-256s match**. Transfer report contains **no original 333 MB of authority content**; reporter's original Mac direct hashes cannot be independently rerun by Browser.
- `01_ORIGINAL_SHA256_COLD_REHASH.tsv`: **207** rows = **14** unique physical selected content classes + **12** conflict-candidate versions + **181** bounded dynamic-overlay files. **26/26** selected/conflict rows print `sha_match=YES` and `size_match=YES`, with **0** mismatch/unknown. The 181 overlay rows carry original measured SHA but **NO predeclared expected SHA for comparison**; do not inflate to 207/207 expected-match claims.
- Selected 14 unique class bytes total **333,076,858**; each maps to the corresponding F2 printed SHA for all **18** selected AR rows (AR-0014–18 share one 13,380-byte U01–U06 ledger). Four overlay families: 44 first_pass / 44 semantic / 44 position_conditioning / 49 directionality = **181**; total **41,391,479** bytes, **148** unique SHA values overall (within-family 36/36/36/40). This is observed within the REPORT, not asserted current operative selection.
- `02` retains 58 unique F2 AR IDs with 100% exact `function_ids` and `selection_disposition` field agreement. `03` contains 5 concrete conflict groups including cross-cut AR-0048 and 4 overlay holds. `05`: 14 proposed content-address receipts + one cold-restore placeholder **ALL NOT_RUN**. No approved store, physical copy, cold restore, source runtime install, native proof, Git PR or protected change.

## Material defect: 22 wrong/absent asset-to-hash/hold join dispositions in F3-A 02

**File:** `02_F2_58_ASSET_AND_18_TO_14_CUSTODY_CROSSWALK.tsv`.

1. **All 18 F2 original physically selected local AR rows** `AR-0011, AR-0014–0018, AR-0033–0038, AR-0041–0045, AR-0052` have complete measured SHA, sizes and correct `F3A-C01...C14` mapping in F3-A `01`. But `02` maps **all 18** to `ISSUER-HOLD-AR-xxxx`, blanks the SHA, and grades `ISSUER_OR_NO_BYTE_HOLD`. This falsely conflates **confirmed local byte custody** with absent bytes/issuer uncertainty. Fix with exact 01 class foreign key and printed SHA; retain separate issuer+durability HOLD. No new source read necessary.
2. **Four overlay group AR IDs `AR-0054..0057`**: F3-A `01` lists individually hashed 181 members and `03` contains four correct `F3A-OV-*` group IDs/aggregations, but `02` gives `ISSUER_OR_NO_BYTE_HOLD` and no hold foreign key. Update to the correct group ID and `COLD_SHA_HASHED__DYNAMIC_SELECTION_HOLD` **without inventing one operative release SHA**; preserve family/scope/runtime-selection unproved.
3. All **five concrete conflict groups** (`AR-0009`, `0039`, `0040`, `0048`, `0049`) correctly link to `F3A-X01…X05`; their scientific winner remains HELD. The fifteen prior Git present rows should remain present/issuer held, with AR-0048's physical presence and shadow conflict explicitly coexisting.

**Required bounded action:** assign the EXISTING F3-A worker a **22-row repair of table 02 ONLY**, regenerate output-file checksums and sanitized ZIP under a new versioned name/SHA, preserve the original ZIP as a frozen record, and provide it to independent #744 receiving. No new archaeology, Mac originals mutation, science issuance, storage transfer or second compiler. If installer needs provenance now, use authoritative `01`+`03` as evidence and explicitly mark file `02` incorrect for those 22 rows.

## Receiving limits, custody, currentness

Stored ZIP source and extracted diagnostics were analyzed in the user conversation; actual ZIP is NOT uploaded into GitHub in this action. Independent nonauthor [#744](https://github.com/maidiu/rawlsing/issues/744) must receive the exact ZIP via its own authorized channel and rerun receiving; HQ can only report mechanical checks. Source and rights evidence is still F3-A's investigator testimony until authorized local cold reread by independent custodian.

**Durable store still unapproved.** Free ~16 GiB Mac space is no substitute for an authorized different failure domain. `DURABILITY_HOLD`, `LIVE_INSTALL_HOLD`, original science `NOT_RUN` and #716 authority-dependent STOP remain; current F3-B issuer lane #743 can independently continue for Git-resident AR-0007/conditional AR-0046. Protected PRE-MAIN must not be altered based on this report.