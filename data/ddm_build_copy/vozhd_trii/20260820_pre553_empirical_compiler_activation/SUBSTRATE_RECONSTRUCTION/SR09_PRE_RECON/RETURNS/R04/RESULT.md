# SR09-PRE R04 — EVS adversarial raw-source reconnaissance

Status: `PRE553_SR09PRE_R04_EVS_RECON_COMPLETE`
Branch/start: `agent/vozhd-trii-sr09pre-r04-evs` @ `491a2394e323c904128ca425ef9e793e33ca0d5d`

This return is **non-dispositive**. It measures source-physical/reader facts and names later authority burdens; it does not certify any EVS release.

## Frozen inputs verified

- `surveys.zip`: 158180333 bytes; SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`.
- Only the five assigned EVS members were extracted. Every extracted member matched its frozen R04/SOURCE_BYTE_INVENTORY SHA-256 before probing.
- Accepted SR03 return evidence was independently re-hash-verified: checkout ZIP `e58fd7cdd6e8587573e8cb94ca1df4cd8949cee5fdbc39042b739df6add1c232`; deterministic manifest ZIP `8d06a436b7148d86273e5ae35a887252198ce8ae984902a4a38f05ad11a0e9cc`.

## Measured family facts

| source | rows | cols | reader/config encoding | missing-decl vars | observed user-missing vars | user-missing cells | system-missing | MR sets |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| EVS 1981.sav | 19378 | 370 | WINDOWS-1252 | 363 | 260 | 585266 | 0 | 0 |
| EVS 1990.sav | 38213 | 390 | WINDOWS-1252 | 380 | 314 | 1587207 | 0 | 0 |
| EVS 1999.sav | 41125 | 513 | latin1 (compatibility only) | 506 | 462 | 7117691 | 0 | 0 |
| EVS 2008.sav | 66280 | 477 | latin1 (compatibility only) | 450 | 443 | 4169635 | 0 | 13 |
| EVS 2017.sav | 59438 | 474 | UTF-8 | 451 | 449 | 6975675 | 11 | 2 |

### Missingness and hostile physical states

- EVS 1981 `v308` declares both the range `-5..-1` **and ordinary numeric value `3`** as SPSS user-missing. A sign-based missing rule would destroy this fact.
- EVS 1990 `q745` is physically present on all 38,213 rows yet every cell is the user-missing code `-5`; dropping “all-missing” variables would lose source structure.
- EVS 2008 `v372` declares the date `1582-10-13` as a user-missing value; missing preservation must be type-aware, not numeric-only.
- EVS 2017 has 11 actual system-missing cells (`v228b_r=1`, `v231b_r=3`, `v233b_r=3`, `v251b_r=4`) in addition to extensive SPSS user-missing incidence.
- Missing-declaration shapes broaden sharply by 2017 (`-10..-1`, narrower flag ranges, positive discrete declarations, string-code declarations, and `dweight=-4`). No EVS-wide “negative code” shortcut is lawful.

### Reader compatibility: EVS 1999 / EVS 2008

Authority status is exactly `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`. The override is an execution rule, not a ruling that Latin-1 is the intended source text encoding.

- Frozen accepted SR03 evidence states that the default pyreadstat metadata decode fails on an invalid byte sequence for both exact source SHAs; the explicit compatibility path produces full physical manifests. This worker environment lacks pyreadstat, so the default exception was **not re-executed** here; no substitute reader or guessed encoding was used.
- New raw-byte scans localized the hazard without decoding repair:
  - EVS 1999 contains the Hungarian note path with literal single-byte `e1/e9` accents at six exact offsets, while value-label regions also contain UTF-8-shaped `c3 xx` sequences (for example `AT: SP...` at offsets 130597/146529 and the Hungarian party label at 135973/151905).
  - EVS 2008 contains the same single-byte Hungarian note pattern 90 times, while other value-label regions contain UTF-8-shaped punctuation (`e2 80 93`) and Cyrillic (`d0 xx`) sequences.
- Compatibility-decoded metadata surfaces are correspondingly heterogeneous: EVS 1999 has 236 non-ASCII string fields, 42 containing C1 code points; EVS 2008 has 9,025 non-ASCII string fields, 3,910 containing C1 code points. These counts describe reader output, **not corrected text**.
- Safe physical authority under the frozen compatibility execution includes exact bytes/SHA, counts, raw storage incidence, physical missing declarations/counts, replay variable identity/order, and MR member topology. Human-language labels, notes, MR labels, and semantic claims remain documentary/text-authority gaps.

### Multiple-response topology

- EVS 1981/1990/1999 expose no source-declared MR sets in accepted SR03 metadata.
- EVS 2008 exposes 13 dichotomy sets. Four pairs are exact duplicate-member aliases (`evs_q14/q14`, `evs_q52/q52`, `evs_q5a/q5a`, `evs_q5b/q5b`); `vv25` overlaps `q5a` but omits `v25`, and `vv43` overlaps `q5b` but omits `v43`. Set identity therefore cannot be reconstructed from member variables alone.
- EVS 2017 exposes only two sets (`Q4`, `Q11`), a large topology contraction from 2008.

### Identity, coordinates, weights/design, rank/routing

- `id_cocas` and `caseno` are present in all five releases and physically populated on all rows in the accepted census, but injectivity and intended identity scope are not proved by presence or label wording. `(source snapshot, source row ordinal)` remains the replay identity.
- Coordinate systems drift: 1990/1999/2008 add split-up companions (`country1`, `c_abrv1`, `cntry1_y`); 2017 removes those and labels `country`/`c_abrv` explicitly as ISO 3166 numeric/alpha. Mapping meaning still needs documentary authority.
- Weight topology changes from `weight_g` (1981), to `weight_g + weight_s` (1990/1999/2008), to `gweight`, `gweight_no_edu`, `dweight`, `pweight` plus matrix/mixed-mode/responsive-design coordinates in 2017. No physical variable is automatically the lawful primary weight.
- Ranked first/second-choice structures recur but their variable names/ordinals change substantially. EVS 2017 also contains explicit matrix-design/mixed-mode/responsive-design variables whose eligibility/risk-set meaning cannot be inferred from missingness.
- EVS 2008 has a metadata inconsistency worth replaying: `f201` says “aims of respondent”/Q55-Q56 while adjacent `v201`/`v202` say “aims of this country”/Q60-Q61. This is a documentary authority burden, not permission to repair a label.

## Cross-wave schema drift

- 1981→1990: 11 same-name variables; 359 prior-only; 379 later-only; Jaccard 0.0147.
- 1990→1999: 16 same-name variables; 374 prior-only; 497 later-only; Jaccard 0.0180.
- 1999→2008: 321 same-name variables; 192 prior-only; 156 later-only; Jaccard 0.4798.
- 2008→2017: 269 same-name variables; 208 prior-only; 205 later-only; Jaccard 0.3944.

The early releases are not ordinal-compatible bags of the same variables; even 1999→2008 and 2008→2017 retain only partial same-name overlap. Later certification must use release-specific fixtures with narrowly reusable family laws.

## Authority gaps / disposition

- No novel hazard class beyond the frozen taxonomy was required. The important new **source-specific manifestations** are EVS 2008 MR alias/overlap topology, typed date missingness, EVS 2017 mixed physical missingness/design topology, and exact mixed-byte loci in the two compatibility sources.
- EVS 1999 and EVS 2008 remain `PROBABLE_CERTIFICATION_BLOCKER` candidates for text-bearing semantics until intended text encoding/documentary authority is closed; their physical manifests remain valid compatibility-execution evidence.
- Weight estimands, native-ID semantics, filter/routing meaning, and 2017 matrix/design applicability remain documentary authority gaps.

Overall reconnaissance disposition: `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`.

Token: `PRE553_SR09PRE_R04_EVS_RECON_COMPLETE`
