# Source-semantic court — S00 versus canonical Afrobarometer R5

## Exact evidence identities

Author candidate commit `208bca30471710d48124a6b69ba467f240d8834b` contains:
- `WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json` (Git blob `9be28b2e2df93d1b9c207a207866be1595f22aeb`).
- `rawlsing_next/r3_s02_seam_witness.py` (Git blob `60bdaee9fc4dae2d0e98b33d26309ef229554fe3`).
- `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` (Git blob `84d404147547767be8ecd4b6e1541f5fa3a8c8a2`).
- `rawlsing_next/pre553_selected_world_progressive_contract.py` (Git blob `e9caea543bcc4e1418905f1442d2c7c97eef04b2`).

Canonical commit `7f29aec36d24f16da52d84f17c00f08db3a55434`:
- `rawlsing_next/wave1_r5_q86_c11_projection.py` blob `d96933180d310b4078f23127bb5a97a3677728d1` (native Q86 states lines 58–65; Q86 refs, routing, risk).
- `rawlsing_next/wave1_gt12_i03_positive_facts.py` blob `067628dc6605f28be68bdcd86ef57b02a0db4348` (GT1 unary and GT2 two-target RAW joint, first 10 lines and lines 50–60).
- `rawlsing_next/field_forge_conditional_support.py` blob `a70decb20747d84cbcbe27d1280babc6de88ef33` (line 34 Q86B conditioner, 35 Q86A target; nominal full joint count closure, lines 130–185 and 290–342).
- `rawlsing_next/gt12_c_to_d_relation_bridge.py` blob `ea04ec079e8d60e6e5c7236ec5b54898876be4b3` (source-specific role refs and rejection of wrong role; lines 78–79).
- `rawlsing_next/wave1_ff_prev3_relation_admission.py` blob `c5fb675fd6f95cb7dc9e0ad505224803839cc645` (GT2 source/risk/role and bounded admission lines 33–43).

Prior original-document cross-check (not new issuance): `WORKER_RETURNS/PYAT-HQ273-S01-AFRO-R5-Q86A-Q8A-Q97-HETEROGENEOUS-SCIENTIFIC-SOURCE-WARRANT-R1/00_OFFICIAL_ORIGINAL_Q8A_Q97_Q86A_MEANINGS_AND_ADMINISTRATION.md` at `47755ddba44cd5f79c3fc4817c990e5d4ad9bb01`; original Ghana 2012 source https://www.afrobarometer.org/wp-content/uploads/2022/02/gha_r5_questionnaire.pdf and merged R5 codebook https://www.afrobarometer.org/wp-content/uploads/2022/02/merged_r5_codebook_2.pdf. Ghana original validates Q86A as citizenship inclusion opinion but Ghana is OUTSIDE the frozen GT2 eleven-country scope. These primary document links are inherited from S01, not fresh original-page scans in this review.

## Contradiction matrix

| S00 frozen claim | Exact source/owner reality | Required scientific ruling |
|---|---|---|
| `CH_01_DEMOCRACY_SUPPORT` = R5 `Q86B`, "ordinal Likert 1–4", strongly disagree→strongly agree | Frozen GT12 Q86B is citizenship inclusion for *country-born person with two noncitizen parents*, scalar native **No=0 / Yes=1**; other codes represent DK/routing/refusal/missing | **FALSE SEMANTIC ATTRIBUTION**. Cannot label democracy support, construct 4-step Likert or infer agreement scale |
| `CH_02_INSTITUTIONAL_TRUST` = R5 `Q86A`, same 1–4 Likert | Frozen GT12 Q86A is inclusion for country-born person with *one citizen, one noncitizen parent*: native No=0 / Yes=1 | **FALSE SEMANTIC ATTRIBUTION**. No institutional trust measurement |
| `CH_03_DEMOCRATIC_ATTITUDES` derived joint | GT2 source semantics: ordered **Q86B CONDITIONER → Q86A TARGET** nominal co-response profile | **WRONG DERIVATION LABEL**. May only be a citizenship-attitude joint/count profile under frozen scope |
| `eligibility=complete Q86A/Q86B responses` and `N=19,210` | Frozen common source **coexposure** risk count is 19,210; this does NOT by itself establish a complete substantive-answer denominator or national weighted estimand | **DENOMINATOR/POPULATION HOLD**. Subject to exact typed eligibility/response and source design |
| `STRUCTURAL_POSITION=democracy support / institutional trust` | GT2 is reported normative responses; not objective institutional trust/structure, or material pressure | **STRUCTURAL INTERPRETATION REFUSED** |
| Scenario "high/high" vs "low/low" | Source supports binary No/Yes response at exact native state, without ordinal high/low | **REQUIRES NEW SCENARIO SPEC**, e.g. Q86B Yes vs No, target Q86A Yes under same eligible risk, explicitly respondent attitudes |

### Native code table (not optional)

| Code | Q86A, Q86B native response meaning | Response class |
|---|---|---|
| `0` | No | substantive |
| `1` | Yes | substantive |
| `9` | Don't know | DK |
| `997` | Not asked | NOT_ASKED |
| `998` | Refused | REFUSAL |
| `-1` | Missing | MISSING |

Code values are **identifiers**; no ordinal distance, institutional meaning, generalized class/psychic score or democracy rating. For either conditioning value `0` or `1`, exclude or separately type DK/refusal/not-asked/missing according to the source-issued risk and estimand. "No" is a real response category, not a zero-support numerical result. "Zero support" must mean zero **actual observed cell count** under a qualified denominator.

## Source population and permission ceiling

Frozen source sha256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`, original 51,587 physical source rows, a previously frozen **19,210** common-coexposure carrier and selected countries `BFO, BOT, CVE, KEN, LES, MAU, MLW, MOZ, NAM, SAF, UGA`. Those are inherited frozen GT12 contract metadata, not numerical Q86B×Q86A cells delivered through S02. Accepted GT2 operation is RAW two-target Q86B×Q86A, within source/risk and target-use; GT2 does not authorize all Afro variables, democracy/trust semantics, national representative proportions, official citizenship rules, causal institutional effects or actor-level psychology. Original multilingual administered-form completeness and any use extension remain with qualified source/operation issuer.

**Source-scientific resolution:** replace the S00 labels with an actually defensible, source-scoped **citizenship inclusion opinion** contrast, or choose different genuinely source-authenticated democracy/trust variables and secure separate original question/routing/operation/target-use grants. Do NOT relabel Q86A/B to save the target.
