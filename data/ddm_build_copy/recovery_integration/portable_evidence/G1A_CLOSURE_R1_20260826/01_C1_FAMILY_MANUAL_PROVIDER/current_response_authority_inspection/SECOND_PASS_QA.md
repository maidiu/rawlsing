# Second-pass QA — SAV-derived R2

This QA was performed after extracting the previous package from scratch and independently recomputing its invariants.

## Defects found in R1 and fixed in R2

### 1. Misleading context/admin court diagnostics

R1's court table recorded `runtime_rows=0` for context/admin contracts even when unsigned runtime rows existed, and labeled their generic `validation_status` as `FAIL` while the final court status correctly passed them.

R2 reports the real counts. Of 464 no-signed-scale contracts, 354 have 7,445 runtime rows total and 110 have zero rows. All 7,445 rows are unsigned. `validation_status` is PASS for all 700 contracts.

### 2. Alias replicas duplicated into the runtime map

R1 copied 2,468 raw-SAV alias response rows into the runtime map. Although semantically equivalent to their canonical targets, that blurred the identifier-authority boundary and could allow a raw identifier to match response semantics without first traversing the governed alias crosswalk.

R2 removes all alias replica rows. The canonical response map now contains 392,572 rows: 350,066 current manual rows + 42,506 quarantined legacy rows. Raw identifiers must resolve through the explicit alias/family authority before QSM and response-option joins.

## Independent checks performed

- ZIP/source file hashes verified.
- All manifest-listed files verified by SHA-256 and byte count.
- Raw SAV hashes match the recorded 1995/2011/2024 hashes.
- Current nine manual packet hashes match the recorded hashes.
- Historical 700-contract inventory hash matches the recorded hash.
- Canonical 350,066 runtime rows equal the union of the nine current manual packets over the established 71-column runtime schema.
- 42,506 quarantined legacy rows contain no direction, intensity, or polarity.
- zero raw alias replica rows in R2 runtime map.
- zero exact duplicate runtime rows.
- 359/359 direct aliases exist in the appropriate SAV dictionary, resolve through first-pass to the same governed question ID, target a current manual authority variable, and target runtime rows identical to the current packet rows.
- 110/110 one-to-many family member rows exist in the SAV dictionary and are excluded from direct alias handling.
- no raw identifier maps to multiple authority variables within wave.
- 236/236 certified active response-scale contracts pass.
- 464/464 context/admin contracts have zero signed rows.
- 700/700 historical court rows pass.

## Explicit non-claim

This package does not certify the new fresh 35×20 selection until that selection is frozen and run through the same response-semantics coverage court.
