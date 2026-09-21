# FIABC-LM2-R1L-A RETURN

Status: **PASS**

Exact base: `89bfde652eb8a983e51ff51f5258e5fdfbb2433b`

Branch: `agent/rabochii-premain-fiabc-lm2-r1l-a-validation-authority-provenance-r1`

## Court holding

All three WVS validation kinds have independent pre-outcome authority:

- `TARGET_CELL_SUPPORTED`
- `JOINT_NOT_PRODUCT_OF_MARGINALS`
- `DISTRIBUTION_DIFFERS_FROM_BASELINE`

The authority is **not** derived merely from the fact that the frozen grammar uses the tokens. The independent chain is accepted generic I05 validator/constructor law + HQ Lock1 family/frontier governance + adopted EE-P2F1 R12 classification + the P2F2 zero-new-semantics issuer mandate and exact DISCOVERY_FRONTIER operation authority.

P2F2 then froze the exact three names in the WVS grammar/candidate identities before outcomes, while omitting those same names from `DiscoveryAuthority.validation_rules.kinds`.

Therefore:

`INCOMPLETE_SERIALIZATION_OF_ALREADY_FROZEN_AUTHORITY`

and **not**:

`NEW_AUTHORITY_PREMISE_REQUIRED`

No repair was performed.

## Key evidence

- Generic I05 initial validation law: `8a3382d9de7ce38591f92e3a09481b38198a106c` (2026-08-20), introducing `DISTRIBUTION_DIFFERS_FROM_BASELINE` and `JOINT_NOT_PRODUCT_OF_MARGINALS` plus the fail-closed validation-kind authority guard.
- Generic I05 completion: `6a75433b9a12b66e75f1def97f69163587970fd1` (2026-08-20), blob `b2b99460cc5991bc26aa2ffe5bda129b408fc197`, adding `TARGET_CELL_SUPPORTED`. P2F2 used this exact blob.
- EE-P2F1 R12: `B__SEMANTIC_AUTHORITY_EXISTS__PRE553_ISSUANCE_OR_BINDING_ONLY`; parent inventory `I01_LOCK1_WVS_SOURCE_AND_PROGRAM_FREEZE` + `I08_PRE553_I05_EXACT_BOUNDED_CONTRACT`.
- HQ P2F1 adoption: 14 B rows, 0 new authority; deficit classified as authority-form/exact-binding.
- EE-P2F2 commission: R12 exact support/validation-rule bindings; zero new semantic proposition; no invented validation semantics.
- Exact P2F2 DISCOVERY_FRONTIER authority: `EE-P2F2-WVS7-LOCK1-DISCOVERY-FRONTIER@1.0.0` / `f0f5634d42c61cc34878c8ab005bcfad98261d4fd147f76b5413c2fac5f9d6c7`.
- Frozen DiscoveryAuthority: `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`.
- Frozen grammar: `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`.
- R1K blocker correctly exposed the missing local `validation_rules.kinds` envelope.

## Scope / prohibitions observed

No WVS SAV/ZIP opened. No I05 execution. No candidate outcomes inspected. Candidate A/B/C not run. No source repair or authority repair performed.

## Return files

- `01_VALIDATION_KIND_LINEAGE.csv`
- `02_AUTHORITY_PARENT_GRAPH.json`
- `03_PREOUTCOME_PROVENANCE_COURT.md`
- `04_OMISSION_VS_NEW_PREMISE_HOLDING.json`
- `RETURN.json`

Terminal:

`FIABC_LM2_R1L_A_PASS__THREE_VALIDATION_KINDS_HAVE_PREOUTCOME_AUTHORITY__DISCOVERY_ENVELOPE_OMISSION_IS_REPAIRABLE`
