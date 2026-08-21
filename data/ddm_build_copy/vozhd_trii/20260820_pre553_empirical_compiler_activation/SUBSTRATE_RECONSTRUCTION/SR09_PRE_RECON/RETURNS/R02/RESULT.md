# SR09-PRE R02 — Arab Barometer raw-source reconnaissance

Status: `COMPLETE__NON_DISPOSITIVE_RECONNAISSANCE`  
Worker: `R02`  
Family: `Arab Barometer`  
Branch: `agent/vozhd-trii-sr09pre-r02-arab-barometer`  
Starting authority HEAD: `491a2394e323c904128ca425ef9e793e33ca0d5d`

Required token: `PRE553_SR09PRE_R02_ARAB_BAROMETER_RECON_COMPLETE`

## Scope and disposition

All four assigned source members were obtained **only** from the frozen ChatGPT Library `surveys.zip`, after the bundle passed its frozen size/SHA check and each extracted member passed its exact R02 source SHA check. No local source copy was substituted.

Every assigned source disposition is:

`KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`

No new generic hazard class was observed. The family requires source-specific hostile fixtures and documentary authority before later certification; this return does **not** certify any source, semantic state, mapping, routing rule, identity rule, or weight.

## Measured physical source surface

| Source | Rows | Logical vars | SPSS storage slots | System missing | Ordinary present | SPSS user-missing declarations | Non-ASCII metadata vars | MR sets |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Arab Barometer Wave 1.sav | 7,337 | 181 | 181 | 42,461 | 1,285,536 | 0 | 11 | 0 |
| Arab Barometer Wave 2.sav | 12,782 | 468 | 468 | 2,781,161 | 3,200,815 | 0 | 94 | 0 |
| Arab Barometer Wave 5.sav | 27,850 | 359 | 361 | 4,426,794 | 5,571,356 | 0 | 7 | 0 |
| Arab Barometer Wave 8.sav | 15,627 | 690 | 692 | 4,798,210 | 5,984,420 | 0 | 418 | 0 |

All four files physically declare character code `65001`; Wave 1 also carries an explicit `utf-8` encoding extension. SPSS header `weight_index=0` in every assigned snapshot. Zero SPSS user-missing declarations were found in the assigned four files; therefore DK/refusal/missing-like labels remain ordinary storage-value candidates unless later authority says otherwise.

## Measured source facts

### Wave 1

- `ser` is noninjective: 1,885 distinct values over 7,337 rows; max multiplicity 7. Adding `country` still leaves **six duplicate pairs**. Example: rows 3021 and 3450 both store `country=3`, `ser=972`.
- `country` has seven observed codes; critically, code `1` is **Jordan**, a coding that changes in later waves.
- Physical missingness and ordinary semantic-candidate codes coexist. `q227` has 5,093 system-missing rows; `q206` row 5 is ordinary `98` with label “can't choose/don't know”.
- Parallel income fields `q715withoutmorocco` and `V715onlymorocco` coexist with different missing incidence. Their names and missingness are routing clues only.
- Metadata is declared UTF-8 but contains **17 literal C1-control-bearing strings** (`U+0092`/`U+0093`). This is an exact source-text preservation burden, not permission to repair typography.
- `q2131..q2135` are physically separate adjacent battery/member variables. No SPSS MR-set metadata is present.

### Wave 2

- `qid` is noninjective alone (1,841 distinct / 12,782 rows; max multiplicity 10), but `(country,qid)` is empirically injective in this snapshot. That measurement is not identity authority.
- `q101` stores ordinary `0`, `8`, `9` even though their labels include “missing”, “i don't know”, and “declined to answer”. More hostile still, `q2062` has both true system-missing rows and ordinary `0` labeled “missing”.
- Country/local systems are layered: `country`, `a1`, `v1`, and `q1` coexist; `q1` exposes 150 observed local province/governorate/state codes.
- Country-module alignment is exact but non-dispositive: `eg2041` is nonmissing on exactly 1,219 rows, all `country=5`; `sa2013` exactly 1,404 rows, all `country=17`; `ir2035` exactly 1,234 rows, all `country=7`.
- `wt` is complete at logical ordinal 467, but header active-weight index remains 0 and raw values do not establish estimand or lawful use.
- `q2061/q2062` physically encode first/second challenge slots with different missing incidence; no MR-set metadata is present.

### Wave 5

- `id` is noninjective and `(country,id)` still leaves **three duplicate pairs**. Rows 19404/19405 both store `country=15`, `id=15165`.
- Physical scope/design expands: `wave=5`, `splita`, `splitb`, `sample`, `mode`, `wt`, `psu`, `stratum` are all present. `wt` has 32 system-missing rows; `psu` has 1,070.
- `Q101` dictionary contains observed `98/99` plus unobserved `-8/-9` missing-like labels and `97`; none is declared SPSS user-missing. Dictionary membership, observation incidence, and semantic state must stay separate.
- `q1` and `stratum` are **not** aliases here: they match on only 842 of 27,850 rows.
- UTF-8 metadata/cells include `Saïda` and Arabic string `ظريف`. `E2001B` is a 21-character logical variable spanning three SPSS storage slots.
- `Q2061A/Q2061B` are separate ranked slots with different missing incidence. No SPSS MR-set metadata is present.

### Wave 8

- Native `ID` is unusable as a hard replay key: ordinary `ID=0` occurs **2,400 times**, exactly all Jordan (`COUNTRY=8`) rows, and adding country does not disambiguate them.
- `BLOCK_ID` has **zero** system-missing cells yet stores an ordinary empty string on exactly **2,408 Iraq (`COUNTRY=7`) rows**. A blank string is not a system missing value.
- Country-specific physical surfaces are dense: `Q1A_PAL` is nonmissing exactly 1,189 rows, all Palestine; `Q2061A_KUW`, `Q1012C_MOR_*`, `Q201A_41_GAZA`, `Q622C_IRQ_*` likewise expose country-linked incidence. These are routing clues, not route authority.
- `WT`, `PSU`, `STRATUM` are complete. Unlike Wave 5, `Q1 == STRATUM` on **all 15,627 rows**. Raw equality does not establish semantic identity or design role.
- 418 logical variables carry non-ASCII metadata. `DATE` contains “TODAY’S”; `Q1` includes `Ma’an`.
- `Q622C_IRQ_*` and similar prefixed blocks are separate variables with heavy/hybrid missingness but no SPSS MR-set metadata; topology requires questionnaire authority.
- 690 logical variables occupy 692 storage slots because `DATE` and `BLOCK_ID` are 10-character strings spanning continuation slots.

## Cross-wave fault lines

1. **COUNTRY code drift is hard, not cosmetic.** Wave 1 code `1=Jordan`; Waves 2/5 code `1=Algeria`. Country codes must be wave-scoped.
2. **Q101 coding drifts.** Wave 1 uses ordinary `98/99`; Wave 2 uses ordinary `0/8/9`; Wave 5 returns to `98/99` while carrying extra unobserved `-8/-9`; Wave 8 again uses `98/99`. Shared variable name does not license semantic equivalence.
3. **Identity law drifts.** Wave 2 happens to become injective under `(country,qid)`; Waves 1 and 5 still collide under country+ID; Wave 8 contains a 2,400-row zero-ID block. Source row ordinal remains irreducible.
4. **Weight/design representation drifts.** No obvious Wave-1 weight surface; Wave 2 adds `wt`; Wave 5 adds `wt/psu/stratum` with physical missingness; Wave 8 has complete `WT/PSU/STRATUM` and exact `Q1==STRATUM`.
5. **Routing/module representation drifts.** Wave 5 foregrounds split/sample/mode controls; Wave 8 foregrounds extensive country-suffixed modules and ordinary blank `BLOCK_ID` incidence.
6. **Text burden expands and changes form.** Wave 1 has C1 control payloads under UTF-8; Wave 2 has proper curly punctuation; Wave 5 includes Arabic cell text; Wave 8 has 418 variables with non-ASCII metadata.

The pairwise recurrent-name audit is recorded in `CROSS_WAVE_DRIFT.csv`; among Waves 5/8 alone, 88 case-insensitive names recur, but 87 shift ordinal, 86 shift label, and 84 shift value-label dictionary.

## Authority gaps

The raw bytes close physical facts but do not close:

- native respondent-ID semantics/scope;
- semantic response-state meaning of DK/refusal/missing-like ordinary codes;
- routing/universe/applicability for split/country/module surfaces;
- weight purpose, estimand, normalization and design law;
- multiple-response/battery/rank/member topology;
- country/local-region canonical mappings;
- recurrent-variable semantic equivalence across waves;
- Wave-1 typography intent for C1-bearing source metadata.

See `AUTHORITY_GAPS.csv` for the source-specific burden.

## Full-scan reason

A full sequential case-stream scan was performed for each assigned source. Metadata-first probing established the dictionary/encoding/schema surface, but exact row-level missing-state, ID-injectivity, routing-alignment and hostile-cell evidence still required traversing the compressed sequential SAV case stream. The worker runtime did not provide `pyreadstat`; no network substitution or guessed encoding was used. The private scratch reader decoded only classic compressed SAV behavior needed for these exact snapshots and required source-declared UTF-8/character-code `65001` before decoding text. Additional full-stream replays were limited to named joint/duplicate/sentinel measurements and are enumerated in `PROBE_RECEIPT.json`.

## Non-dispositive holding

No generic SAV decoder-contract extension is demanded by these observations. Every burden maps to an existing frozen hazard class. Later certification nevertheless requires exact source-specific hostile fixtures, especially Wave-1 text controls, Wave-2 physical-vs-labeled missing coexistence, Wave-5 duplicate IDs/design missingness, and Wave-8 zero IDs/blank block IDs/country modules.
