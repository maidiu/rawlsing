# VMC-T2 R7 — fourth hostile review, reproducible validator defects, bounded repair

**R6 reviewed disposition: `REVISE_EXACT_DEFECT` — validation/provenance only.** R6's source-graded I07, R08, Batch, V552J/V553, original V554, modern M1 and experimental F6M findings are retained at their **existing** S0–S1 ceilings. No row-level historical or current semantics is being newly accepted, and no P0/P1/P2 duel or 160-module census was resumed.

## Immutable chain / issue custody

- Original owner: VMC-T2 #870, existing draft PR #1085, same `research/vmestye-vmc-t2-programma-transform-seams-r1` branch.
- Preserved R3 `5a73ee31e7dd5af26474f35bbe280dd3bb3b0bac`, R4 `edfe7bb9fab1fd295621e9447745ddab4bb67bfb`, R5 `355b49217087159a0ed93ae2c076f4a4c23b287b`, R6 `3d7ed2c23354decee6f75b0a3ddfdb805de58795`. Current R7 authoritative HEAD is the new frozen PR SHA after append-only publication.
- Protected `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e` externally rechecked unchanged before this repair. Historical code `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`; experimental prior R29 `1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa`. T1 R6 author `bb83248e6e7140122d0f01171409954fc9d0cf70` still needs independent #815 receiving.

## Hostile defects found

### R7-D01 — missing duplicate-ID proof in R6 transition primitive

**Reproducer.** Against the published R6 `diff` semantics, start with two records IDs `X01`, `X02`, and append an identical third record with ID `X01`. The algorithm builds a `Set` of IDs, retrieves the **first** matching record via `get`, compares only that first original prefix, and counts appended records only if their ID was *not* in the prior set. It therefore returns **zero violations, zero field modifications and zero appended IDs** for this duplication. This exact controlled test was executed in the GitHub tool JS runtime.

**Severity:** a genuine defect in the R6 change-detection *primitive* and its advertised hostile controls. It is **not proof** that the already pinned R6 tables contain a duplicate: their ID uniqueness and Git blob pins had been separately verified. In particular, a mutated R6 file would also fail its expected SHA check in ordinary strict execution. The correction makes the transition invariant itself fail closed instead of relying on that separate safeguard.

**Repair:** `validate_vmc_t2_r7.mjs` independently requires non-empty unique IDs and fixed row counts at **each** frozen R3/R4/R5/R6/candidate source, maintains original order, and attacks same-content duplicate insertion with a dedicated rejected negative control. It then invokes the preserved R6 strict validator, rather than representing a new snapshot-only check as complete whole-mission conservation.

### R7-D02 — a pinned historical commit is not a current protected or author ref

**Finding:** R6's strict `rev-parse SHA^{commit}` showed that protected and author source commits exist, but did not check that the **named protected PRE-MAIN branch** still points to the reported protected SHA. Similarly it had no independent candidate HEAD versus owner-ref comparison. A detached/stale source checkout could pass some historical checks without proving current authoritative reference identity.

**Repair:** R7 strict mode requires `--repo-root` and explicit `--candidate-ref <40-hex-sha>`, independently reads the configured `--owner-ref` (default T2 original owner branch) and `--protected-ref` (default protected PRE-MAIN branch), and **requires exact equality** to the candidate and protected SHAs. Missing/unfetched refs fail closed. The running R7 script bytes must equal the blob in that exact candidate Git commit, and the inherited R6 validator bytes must equal its frozen R6 source. This does not confer source/issuer authority; it only establishes source identity at checkout.

### R7-D03 — original code blob and T1 overlay provenance insufficiently cross-checked

**Finding:** R6 verified only selected source lines while many new current/historical source anchors were not checked as exact Git blob identities by its standalone validator. It also accepted four T1 R6 source overlay rows by author-SHA and known T2 IDs without proving the IDs actually exist in the frozen T1 R6 historical return.

**Repair:** R7 pins **eleven** exact current, historical and experimental source file blobs (I07, early/late R08, Batch, M1, original numeric V554, V552J resolver, selected-only compatibility adapter, canonical V553 validator, V553 temporal resolver, and prior sourcefree F6M). At author review, all eleven were retrieved **directly from GitHub at their committed cuts**, with **11/11 matching** source blobs. Strict mode independently checks the frozen T1 R6 `HISTORICAL_TRANSFORM_CONTRACTS.tsv` for all four overlay IDs and verifies each one was an original R3 map ID. The exact R08 effect assignments L1224–1225 and V553 temporal call L2048 remain pinned.

## Exact R7 conservation

- R7 introduces **NO changes** to `INTENDED_ACTUAL_TRANSFORMATION_MAP.tsv`, `DISCREPANCY_AND_OWNER_ACTIONS.tsv`, `REVERSE_CONSUMER_TRACES.tsv`, `R4_T1_T2_CROSS_REFERENCES.tsv`, original 235-fate crosswalk, R4/R5/R6 reversible delta ledgers, or T1 source overlays.
- Counts remain **52 historical contracts**, **68 owner actions**, **542 reverse consumers**, **235 inherited fates**, **seven T1/T2 crosslinks**, **four T1 R6 source overlays**. All previous R3–R6 SHAs and evidence IDs retained, with no new canonical atlas.
- New `validate_vmc_t2_r7.mjs` is an **additive strict reviewer preflight** that executes the prior `validate_vmc_t2_r6.mjs` and demands its five negative-control rejections and `PASS_STRICT_DOCUMENTARY`, plus new unique-ID, branch identity, source-blob and ledger constraints.
- The new JS module body was **syntactically parsed in the GitHub tool JavaScript runtime after stripping module imports and replacing `import.meta`**, which is a syntax-only sanity check, **not** execution of Node/Git full strict mode. A live GitHub 11-file source-blob audit **PASS**. The previously executed GitHub-backed R3→R4→R5→R6 whole-row/delta audit remains the prior author-side result, not fresh independent receiving.

## Independent reader / smallest remaining tests

1. #816 ZL-17: in a qualified local clone, fetch the exact candidate and protected named refs and all historical commits, run `node validate_vmc_t2_r7.mjs --repo-root PATH --candidate-ref <R7 HEAD>`. Any missing refs or source blobs should produce HOLD rather than an invented PASS. Inspect distinct reader definition versus consumer for I07, real conditional R08 step field mutation and negatives, historical V553 canonical/temporal code first readers, and the preserved issuer/native gaps.
2. #815 ZL-16: cross-check the four unchanged source overlays and T1 R6 historical return as an unaccepted author candidate. Avoid read-in of wave-exclusive V549b denominators, alternate V552J fact lists or native scientific acceptance absent actual source proof.
3. #814 ZL-15: take only independently accepted, source-specific historical-to-current deltas into the **single existing** canonical atlas. Neither R7 nor R6 author return accepts itself. The HQ-designated custodian alone may maintain the common SHARED index.

No production engineering, original35/native, experiments, respondent replay, source science/actor/consent issuance, S2/S3, protected merge, or broad reconnaissance was performed.

**Terminal author scope:** `T2_TARGETED_DOCUMENTARY_REPAIR_READY_FOR_INDEPENDENT_RECEIVING`; standalone strict R7 Node execution **NOT_RUN** in this GitHub connector environment and independently accepted status **NOT CLAIMED**.
