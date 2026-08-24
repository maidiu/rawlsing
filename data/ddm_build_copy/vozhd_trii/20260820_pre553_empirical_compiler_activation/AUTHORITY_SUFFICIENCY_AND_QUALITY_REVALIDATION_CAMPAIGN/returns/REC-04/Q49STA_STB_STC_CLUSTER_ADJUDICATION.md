# Latinobarómetro 2024 Q49STA / Q49STB / Q49STC — Source-Native Cluster Adjudication

## Source-native cluster

The governed source-object accounting binds the following as one Q49 source-native cluster:

- `Q49STA` — increase/decrease in the last twelve months of **crime in general**
- `Q49STB` — increase/decrease in the last twelve months of **drug addiction**
- `Q49STC` — increase/decrease in the last twelve months of **corruption**

All three carry the same source response geometry:

1. Increased a lot
2. Increased a little
3. Remained the same
4. Decreased a little
5. Decreased a lot
8. Don't know
0. No response

`Don't know` and `No response` are non-substantive and cannot be signed anchors.

## Geometry ruling

The scale has a textual directional-change structure: **increased ↔ remained the same ↔ decreased**. This statement does not derive semantic polarity from numeric code order. The words themselves establish the ordered change topology; the semantic sign for any target still depends on the governed relation axis/reversal.

## QRA700 jurisdiction

Only `Q49STA` is inside the 700-row QRA denominator.

For `Q49STA`:
- current QRA directionality is source-supported;
- current QRA anchors `Increased a lot` / `Decreased a lot` with `Remained the same` neutral are supported under its governed reversed sign;
- current O07 class `NOMINAL` is defective at this row;
- O07 successor class candidate: `SIGNED_SCALAR`;
- REC-04 classification: `CONFLICT__O07_RECONCILIATION_REQUIRED`.

`Q49STB` and `Q49STC` are outside QRA700. Their identical source response geometry is recorded as cluster evidence only. REC-04 does **not** create QRA rows for them. Their current O07 row classes were not recovered from an accessible row-level carrier in this Browser/Library court, so no O07 correction is counted for either.

`REC04_Q49_CLUSTER_QRA_MUTATION = NONE`

`REC04_Q49STA_O07_CORRECTION_COUNTED = YES`

`REC04_Q49STB_STC_O07_CORRECTION_COUNTED = NO__CURRENT_ROW_CLASS_NOT_RECOVERED`
