# SR09-PRE R06 — Latinobarometro raw-source reconnaissance

**Status:** `AUTHORIZED__NON_DISPOSITIVE` — COMPLETE  
**Branch:** `agent/vozhd-trii-sr09pre-r06-latinobarometro`  
**Exact starting HEAD:** `491a2394e323c904128ca425ef9e793e33ca0d5d`  
**Completion token:** `PRE553_SR09PRE_R06_LATINOBAROMETRO_RECON_COMPLETE`

## Input gates

- `surveys.zip`: 158,180,333 bytes; SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`.
- Extracted only the three assigned substantive members; `__MACOSX/**` / AppleDouble entries were ignored.
- Exact source hashes all matched the frozen R06 inventory before probing.
- No source compatibility/encoding override was used. All three sources carry an explicit SPSS subtype-20 `UTF-8` encoding record.

## Measured certification burden

| source | rows | dictionary vars | countries observed | physical missing | respondent-identity evidence | disposition |
|---|---:|---:|---:|---|---|---|
| 1995 | 9,069 | 203 | 8 | 202 vars declare user missing; 267,448 user-missing cells; 0 system missing | `enc` 2,589 unique; `(pais,enc)` 8,629/9,069 unique, so 440 duplicate excess rows | `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED` |
| 2011 | 20,204 | 414 | 18 | 372 vars declare user missing; 730,387 user-missing cells; 0 system missing | `NUMENTRE` repeats globally; `(IDENPA,NUMENTRE)` 20,204/20,204 unique | `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED` |
| 2024 | 19,214 | 332 | 17 | 306 vars declare user missing; 313,064 user-missing cells; 0 system missing | `NUMENTRE` repeats globally; `(IDENPA,NUMENTRE)` 19,214/19,214 unique | `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED` |

Observed injectivity is not respondent-identity authority. Physical row ordinal remains the only universally governed replay identity absent separate source documentation.

## Country / year / sample drift

- 1995 contains 8 observed country codes; 2011 expands to 18; 2024 has 17. Raw country code `558` / Nicaragua is present in 2011 and absent in 2024.
- The year coordinate is not stable in raw coding: 1995 uses `numero=1995`; 2011 uses `NUMINVES=16` with value label `2011`; 2024 uses `NUMINVES=24` with value label `2024`.
- Lower-geography domains move sharply: 2011 `REG` has 173 observed codes versus 148 in 2024; 2024 also mixes raw `REG` values `1,3,5` with country-prefixed codes. No numeric-pattern normalization is authorized.

## Recurrent-variable drift: name equality fails

2011 and 2024 share **47 exact variable names**. Across those 47:

- **47/47** have different variable labels;
- **38/47** have different value-label dictionaries;
- **25/47** have different missing declarations;
- **32/47** move ordinal position.

Hostile examples are decisive: `P2ST` changes from “In your opinion, which is the most important problem in the country?” (2011) to “Imagen de progreso del país” (2024); `P19ST` changes from a powerful-groups/governance item to a 1–10 democracy scale. Conversely, 1995 and 2011 have zero exact names after native long-name expansion despite analogous-looking fields such as `pais`/`IDENPA`, `enc`/`NUMENTRE`, `region`/`REG`, and `wt`/`WT`. **Neither exact-name equality nor similar Spanish/English labels is canonical-equivalence authority.**

## Missingness and ordinary-code hazards

- 1995 is dominated by declared `-9..-1` user-missing ranges; 2011 retains that regime; 2024 shifts predominantly to `-5..-1`.
- 1995 `p33b=98`, labeled `Don´t know`, is observed 1,757 times but lies outside its declared `-9..-1` user-missing range.
- 2024 `P56N.1=96`, labeled `Don't know him`, is observed 10,490 times outside its declared `-5..-1` missing range; several recodes use ordinary `0` labeled `No data`. These are **semantic-code candidates only**, not inferred missing values.
- Routing/applicability cannot be reconstructed merely from negative missing values or labels such as `Not asked` / `Not applicable`.

## Weight / design drift

The SAV header points to the final weight variable in every release, but the physical distributions change substantially:

- 1995 `wt`: 19 values, min `0.16216216`, median `1`, max `2.30769231`.
- 2011 `WT`: 307 values, min `0.07150674806593951`, median `1`, max `7.424112681330718`.
- 2024 `WT`: 90 values, min `0.4208`, median `1`, max `19.7793`; label changes to `Ponderación` and the variable itself gains a `-5..-1` missing declaration.

No raw name/label establishes strata/PSU semantics or the weight estimand. Those remain documentary authority gaps.

## Topology / hostile physical metadata

- No assigned source contains an SPSS multiple-response-set extension record.
- Repeated/ranked structures remain physically explicit in names/order, including 2024 `P23STM.1/.2/.3`, `P4NINT.1..10`, and `S13P1STINT.1..3`; their slot order is preserved without promoting them to canonical ontology.
- 2024 contains a hostile header mismatch: `nominal_case_size=174`, while the dictionary has 332 distinct numeric variable records and `weight_index=332` resolves to `WT`. The full 19,214-row data stream decodes at 332 values per case. The raw creation-date bytes are also nonstandard: `17 031 25`. Reader fixtures must not “repair” either field or trust nominal case size over the dictionary.

## Authority gaps / non-dispositive boundary

Raw bytes establish physical values, labels, missing declarations, observed injectivity, and topology. They do **not** establish respondent-key semantics, intended sample universe, weighting estimand/design, questionnaire routing, or cross-wave canonical equivalence. Those gaps are enumerated in `AUTHORITY_GAPS.csv`; exact fixtures are frozen in `HOSTILE_SENTINELS.csv`.

No Library/raw bytes, database, production runtime, governance file, or non-R06 repository path was modified.
