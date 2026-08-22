# PREP71 R09 — WVS-OTHER CERTIFICATION PACKETS

Assigned sources:

- `WVS Wave 1.sav` — `051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824`
- `WVS Wave 4.sav` — `c6757ed187655c8b9af88ae4c23c00f066696a641af2f316b4343272ea1d4a0a`

WVS Wave 7 is EXCLUDED. It is under independent Authority-70 full-source execution and may not be probed under Authority 71.

Raw transport: `surveys.zip` only.

Read accepted `SR09_PRE_RECON/RETURNS/R09/` before raw probing.

Priority hostile burden:

- Wave 1: `S007` carries 9–10 digit raw IDs despite `F2.0` display metadata; future fixture must prove raw numeric magnitude survives independently of display/print width and that display metadata cannot truncate or redefine storage;
- Wave 4: candidate respondent identity remains unsafe (`country+V3` collisions and typed-missing identity values); row ordinal remains irreducible replay identity;
- Wave 4: preserve all-row typed-missing columns rather than eliding them;
- Wave 4: `V220` / `Q223_LOCAL` raw vectors can be identical while label dictionaries differ; variable/dictionary identity must survive raw-vector equality;
- do not import WVS7 source-specific hostile facts as if they were W1/W4 law; reuse only generic frozen SAV/source-native rules and explicitly supported family drift facts.

Prepare both packets under `SOURCE_CERT_PREP71/RETURNS/R09/` using the common packet contract.

Do not certify.

Token: `PRE553_SOURCE_CERT_PREP71_R09_RETURNED`
