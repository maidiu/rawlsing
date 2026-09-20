# Afrobarometer Round 9 — Weight Succession and Routing Authority

## Court rule

This file separates three things that must not be collapsed:

1. **physical carrier identity** — inherited from accepted Authority71/S35 source-native evidence;
2. **producer logical weight role** — established by official Afrobarometer documentation;
3. **exact short-carrier alias binding** — admitted only when the producer record binds the exact raw name.

No role in this return is inferred from numeric magnitude, correlations, or distributional similarity.

## Producer-authorized Round 9 succession

The Round 9 Survey Manual documents a substantive change in Afrobarometer weighting.

Earlier within-country weights adjusted selection probabilities using sampling structure through the enumeration-area level. Afrobarometer then expanded the weight to include household/adult-selection information through `ADULT_CT`.

The manual names:

- `withinwt_ea` — the **older** EA-level within-country weight;
- `withinwt_hh` — the **new** household-aware within-country weight.

It explicitly says the new `withinwt_hh` weight is the one that **must be used for analysis**, while the previous weight remains in the dataset under the `withinwt_ea` name.

This is producer-authorized succession, not numeric inference:

`withinwt_ea --superseded_for_R9_analysis_by--> withinwt_hh`

The old weight is retained for compatibility/comparison; retention is not co-equal analytical recommendation.

## Producer-authorized use domains

### National descriptive estimates

Afrobarometer's sampling guidance assigns within-country weights to national descriptive reporting.

For Round 9, the successor logical role is therefore:

`NATIONAL_DESCRIPTIVE -> withinwt_hh`

subject to exact raw-carrier realization authority.

### Multi-country descriptive estimates

The legacy weights protocol defines `COMBINWT` as the within-country weight adjusted so national samples contribute equally in merged analysis. The current producer sampling guidance retains the same cross-national descriptive purpose.

The Round 9 Survey Manual likewise instructs activation of COMBINWT for merged/AFROMEAN-style descriptive results.

Therefore:

`MERGED_MULTI_COUNTRY_DESCRIPTIVE -> COMBINED_WEIGHT_ROLE`

But this court does **not** infer which exact Round 9 short raw carrier represents the HH-based combined successor when the official Round 9 public documents do not name that alias.

### Inferential relationship analysis

The Round 9 Survey Manual cautions that WITHINWT/COMBINWT should be disabled when estimating inferential relationships rather than descriptive population summaries.

This is an analytical-use restriction. It does not permit deletion of any raw weight carrier.

## Exact canonical carrier map

| Canonical carrier | Accepted physical/native evidence | Producer documentary role | Exact alias status | Authorized disposition |
|---|---|---|---|---|
| `WITHINWT` | distinct carrier; source-native label says old EA-level within-country weight | legacy WITHINWT; old Round-9 weight renamed `withinwt_ea` | role closed through legacy protocol + R9 succession | preserve; old/EA role may be represented; do not make it the R9 default where new-HH analysis is authorized |
| `V397_A` | distinct carrier; source-native label points to new HH-level within-country weight | logical `withinwt_hh` is the producer-authorized R9 successor | **UNKNOWN exact public alias** | preserve carrier; do not select semantically until exact alias authority binds `V397_A -> withinwt_hh` |
| `COMBINWT` | distinct carrier | producer combined/cross-national descriptive weight role | generic role closed; exact EA-vs-HH variant of this short carrier not independently documented here | preserve; use only under exact later binding for the intended release variant |
| `V399_A` | distinct second/new combined-weight-like carrier in accepted source-native evidence | later Afrobarometer family documentation uses logical `combinwt_hh`, but exact R9 public alias is absent | **UNKNOWN exact alias and role** | preserve opaque; do not infer `V399_A = combinwt_hh` |

## Later family continuity — corroborative only

Later official Afrobarometer codebooks state that datasets use four logical weights:

- `withinwt_ea`
- `withinwt_hh`
- `combinwt_ea`
- `combinwt_hh`

This strongly explains the family shape represented by Round 9's parallel old/new carriers.

It is not, by itself, exact Round 9 authority that the canonical short names `V397_A` and `V399_A` are the latter logical names. Cross-release naming continuity cannot replace a missing exact alias table.

## Fail-closed rules for realization

A source-specific realization must:

- preserve all four canonical physical carriers;
- encode the producer's old-EA/new-HH succession as logical authority;
- keep selection of a logical role separate from short raw-name binding;
- refuse default selection of `V397_A` or `V399_A` until exact alias authority closes;
- never identify weights by numeric similarity;
- never silently normalize, combine, overwrite, or discard one carrier because another looks newer.

## Documentary sources

- Round 9 Survey Manual: https://www.afrobarometer.org/wp-content/uploads/2022/07/AB_R9.-Survey-Manual_eng_FINAL_20jul22.pdf
- Sampling guidance: https://www.afrobarometer.org/surveys-and-methods/sampling/
- Afrobarometer Weights Protocol: https://www.afrobarometer.org/wp-content/uploads/2022/04/Afrobarometer_Weights_Protocol.pdf
- Nigeria Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/05/NIG_R9.Codebook_15May24.final_.pdf
- Zambia Round 9 codebook: https://www.afrobarometer.org/wp-content/uploads/2024/06/ZAM_R9.Codebook_4Jun24.final_.pdf
- Later four-weight family documentation (corroborative only): https://www.afrobarometer.org/wp-content/uploads/2025/04/LES_R10.Codebook_22Mar25.final_.pdf
