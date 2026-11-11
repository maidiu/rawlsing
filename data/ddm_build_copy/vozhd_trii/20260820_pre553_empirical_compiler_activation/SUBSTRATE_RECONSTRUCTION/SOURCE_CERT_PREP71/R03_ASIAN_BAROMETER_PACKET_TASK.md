# PREP71 R03 — ASIAN BAROMETER CERTIFICATION PACKETS

Assigned sources:

- `Asian Barometer Wave 1.sav` — `ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2`
- `Asian Barometer Wave 4.sav` — `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200`
- `Asian Barometer Wave 5.sav` — `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63`

Raw transport: `surveys.zip` under frozen Library law.

Read accepted `SR09_PRE_RECON/RETURNS/R03/` before raw probing.

Priority hostile burden:

- Wave 1: explicit BIG-5 source encoding must remain exact and source-specific; later-family UTF-8 behavior cannot overwrite it;
- Wave 5: native multiple-response sets `Q112` and `SE15` overlap on `SE15A..M`; certify future fixtures for exact set identity, membership, counted values, and overlap without deduplicating one set into the other;
- preserve any other native MR metadata declared by the source even where labels/semantics remain authority-limited;
- characterize Wave 4 without inheriting W1/W5 special rules by convenience;
- bound family reuse for encoding, missingness, respondent identity, geography, weights, and MR topology.

Prepare all three packets under `SOURCE_CERT_PREP71/RETURNS/R03/` using the common packet contract.

Do not certify.

Token: `PRE553_SOURCE_CERT_PREP71_R03_RETURNED`
