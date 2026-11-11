# PREP71 R06 — LATINOBARÓMETRO CERTIFICATION PACKETS

Assigned sources:

- `Latinobarometro 1995.sav` — `4b7fc6da17dfddafd6a835717e8dc06981208eb4120fa33bdd16e12ae95926f7`
- `Latinobarometro 2011.sav` — `a44e89e08e564e4e175199eeeabfa6163f32f4ba0a19a6c3f5b4752de6cca22e`
- `Latinobarometro 2024.sav` — `ff5cef18c87969026e7f993d09f10c38a547bf81d5d398784fb59b960b7b0a40`

Raw transport: `surveys.zip` under frozen Library law.

Read accepted `SR09_PRE_RECON/RETURNS/R06/` before raw probing.

Priority hostile burden:

- Latinobarometro 2024 has the unique CLOSED_35 SAV header/dictionary-width inconsistency: nominal case size `174` conflicts with `332` parsed variables and `weight_index=332`;
- future fixtures must prove exact 332-value traversal and preservation of relevant nonstandard header/dictionary facts without silently trusting or repairing nominal width;
- inspect source documentation for any official explanation of 2024 export structure, but do not let documentation overwrite exact raw physical layout;
- map which identity/geography/weight/missing/value-label laws from 1995/2011 survive into 2024 and which do not.

Prepare all three packets under `SOURCE_CERT_PREP71/RETURNS/R06/` using the common packet contract.

Do not certify.

Token: `PRE553_SOURCE_CERT_PREP71_R06_RETURNED`
