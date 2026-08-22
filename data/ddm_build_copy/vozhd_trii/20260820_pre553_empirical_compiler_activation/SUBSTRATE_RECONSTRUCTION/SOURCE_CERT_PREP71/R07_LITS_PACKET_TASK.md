# PREP71 R07 — LITS CERTIFICATION PACKETS

Assigned sources:

- `LiTS_I.dta` — `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- `LiTS_II.dta` — `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9`
- `LiTS_III.dta` — `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8`
- `LiTS_IV.dta` — `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c`

Raw transport:

- `LiTS_I.dta.zip` for LiTS I;
- `surveys.zip` for LiTS II/III/IV.

All four use the frozen compatibility execution path `decode_dta(..., encoding="latin1")` with status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

Read accepted `SR09_PRE_RECON/RETURNS/R07/` before raw probing.

Priority hostile burden:

- LiTS I is the designated DTA proving source for later G-SR08; prepare its packet completely but DO NOT execute or claim G-SR08 certification under Authority 71;
- preserve ordinary DTA values as ordinary even when labels imply DK/refusal/not-applicable; do not map them to physical missingness without authority;
- LiTS I accepted SR03 fact: `weight_0`, `weight_1`, `weight_2` each have 29,000 ordinary values + 2 Stata system-missing values;
- LiTS III: preserve distinct PR/SR module namespaces/topology; sparse/noninjective `hhid` cannot replace row ordinal; reader/text authority conflict remains explicit;
- LiTS IV: preserve exact reader-option interaction as a negative compatibility fixture; map 134 skip variables and top-up weight candidates without inferring routing/estimand semantics; seek source-text authority and name any remaining blocker;
- compare LiTS I-IV only under exact snapshot/config law; no family-wide encoding or semantic shortcut.

Prepare all four packets under `SOURCE_CERT_PREP71/RETURNS/R07/` using the common packet contract.

Do not certify.

Token: `PRE553_SOURCE_CERT_PREP71_R07_RETURNED`
