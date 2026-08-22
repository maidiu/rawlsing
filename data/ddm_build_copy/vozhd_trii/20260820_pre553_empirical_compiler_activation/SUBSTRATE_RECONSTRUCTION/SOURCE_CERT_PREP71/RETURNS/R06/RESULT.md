# PRE553 SOURCE CERT PREP71 — R06 LATINOBARÓMETRO PACKET RETURN

Status: `RETURN_READY__NON_DISPOSITIVE`  
Worker: `R06`  
Branch: `agent/vozhd-trii-srcprep71-r06-latam`  
Exact start: `0ac2a8c00ca5718f293e98f98be6685f67ea2445`

## Holding

Three source-certification packets are prepared. **No source is certified.** Exact Library source bytes remain primary physical evidence; official Latinobarómetro documents provide administered wording, released-code semantics, sampling/design claims, and supporting wave identity only where explicit.

| Source | Packet disposition | Fixtures |
|---|---|---:|
| Latinobarometro 1995.sav | `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION` | 8 |
| Latinobarometro 2011.sav | `PACKET_READY__NO_NAMED_AUTHORITY_BLOCKER` | 8 |
| Latinobarometro 2024.sav | `PACKET_READY__COMPOUND_HOSTILE_COURT_REQUIRED` | 10 |

Total hostile fixtures: **26**.

## Exact raw transport

`surveys.zip` = `158180333` bytes, SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`. Only the three assigned substantive members were extracted. Their hashes exactly match the frozen inventory. No WVS70 or local source file was accessed.

## 2024 P0 width court prepared and executed

The committed executable fixture reads raw SAV structure directly. It proves on the exact source:

- layout code `2`;
- raw `nominal_case_size=174`;
- compression `1`;
- `weight_index=332`;
- header cases `19214`;
- parsed dictionary variable records `332`;
- final dictionary variable `WT` at zero-based ordinal `331`;
- data offset `145498`;
- decoded values `6379048 = 19214 × 332`;
- zero partial-case remainder;
- stream terminates at exact file size `7886834`;
- the original abnormal 174 is preserved and never rewritten to 332.

Fixture: `latinobarometro_2024_width_hostile_fixture.py`  
Execution receipt: `LATINOBAROMETRO_2024_WIDTH_FIXTURE_RECEIPT.json`

## Documentary authority findings

### 1995

Official producer questionnaire/technical records and codebook are available. The exact SAV contains 8 countries and 9069 rows. Seven country counts match the official technical record exactly; **Brazil does not**: raw `PAIS=76` has `1200`, while the technical record says `1080`. This single 120-row discrepancy explains the technical-record sum `8949` versus raw `9069`. No row may be removed or reinterpreted to make the document fit.

The official released-data codebook also demonstrates why instrument codes and SAV storage codes are separate layers: source missing declarations and ordinary nonresponse-like values must be preserved exactly.

### 2011

Official questionnaire, codebook, and detailed methodological report are available. Raw 18-country sample counts match the methodology exactly and total `20204`. This is the clean middle-wave baseline, but it does **not** authorize family-wide schema reuse. `NUMENTRE` remains a native attribute; row ordinal remains the irreducible replay identity.

### 2024

The official technical record says `19214` face-to-face interviews in **17 countries**, and its country sample counts match the raw `IDENPA` counts exactly. The generic wave landing page says “18 countries/territories” while listing 17; the specific technical record plus exact raw source outrank that boilerplate.

No producer document found explains the SAV 174/332 header/dictionary mismatch. That absence does not permit repair.

A second documentary conflict is now named: official results identify `WT` / `PONDERADOR` with `Ponderación 0.01-10`, while the exact SAV contains raw `WT=19.7793` and a `-5..-1` user-missing declaration. Future certification must preserve the raw weight and resolve its documentary semantic/domain authority; clipping or normalization is forbidden.

## Longitudinal drift law

1995→2011 changes naming, sample universe and coordinates so radically that exact-name reuse is unavailable. 2011→2024 is more dangerous: **47 exact variable names recur, yet all 47 labels differ**, with widespread dictionary/missing/ordinal drift. `P2ST`, `P13ST`, and `P19ST` are hostile examples of exact names/question numbers being reused for different concepts. Family reuse is therefore limited to preservation laws, never semantic equality.

Questionnaire and released-storage layers also remain distinct: e.g. the 2011 instrument prints `Q1ST` DNK/DNA as `0`, while the official released-data codebook uses negative missing codes for `P1ST`. Future source certification must retain both layers rather than rewriting one from the other.

## Named blockers / future court gates

1. `LB95_GAP_BRAZIL_SAMPLE_120` — documentary sample-identity closure requires explicit treatment of raw Brazil `1200` vs official technical `1080`.
2. `LB24_GAP_HEADER_WIDTH_EXPLANATION` — P0 source-specific executable hostile court must pass; explanatory documentation is optional/supporting and cannot override raw bytes.
3. `LB24_GAP_WT_DOMAIN_CONFLICT` — weight semantic/domain authority must resolve raw `19.7793` vs official `0.01-10` description without altering raw values.

See `AUTHORITY_GAPS.csv` and `FUTURE_EXECUTION_ORDER.md` for exact fail-closed sequence.

Token:

`PRE553_SOURCE_CERT_PREP71_R06_RETURNED`
