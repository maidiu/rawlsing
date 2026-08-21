# SR09-PRE R05 — GSS Longitudinal Raw-Source Reconnaissance Return

Status: `AUTHORIZED__NON_DISPOSITIVE__LONGITUDINAL_PRIORITY`  
Worker: `R05`  
Family: `GSS`  
Branch: `agent/vozhd-trii-sr09pre-r05-gss`  
Starting HEAD: `491a2394e323c904128ca425ef9e793e33ca0d5d`  
Non-dispositive: `true`

Success token: `PRE553_SR09PRE_R05_GSS_RECON_COMPLETE`

## 1. Input / execution boundary

The branch was verified identical to the exact starting HEAD before work. `surveys.zip` was materialized into worker-private scratch and matched the frozen `158180333`-byte bundle identity and SHA-256 `f68d2b33ec0eeb973699963e4c7122d624b99a541b40277e4daed8b87dc9d05f`. Only the eight assigned substantive GSS members were extracted. Every extracted member matched the exact R05/SOURCE_BYTE_INVENTORY SHA-256 before probing. No database connection was used; no production/runtime or raw source was modified.

The accepted SR03 census and source constitution were used as prior authority. A bounded read-only full data-body pass was then performed on only the eight assigned sources because the R05 burdens require exact within-file ID injectivity, exact coordinate incidence, physical missing-state counts, and zero-based row-ordinal hostile sentinels. The scratch probe does not harmonize variables or assign semantic states.

## 2. Measured source facts

| source | rows | vars | ordinary cells | user-missing cells | system-missing cells | sentinels |
|---|---:|---:|---:|---:|---:|---:|
| `GSS1972.sav` | 1613 | 216 | 289155 | 59253 | 0 | 3 |
| `GSS1973.sav` | 1504 | 339 | 435930 | 73926 | 0 | 3 |
| `GSS1984.sav` | 1473 | 675 | 705372 | 288903 | 0 | 4 |
| `GSS1993.sav` | 1606 | 752 | 783905 | 423807 | 0 | 3 |
| `GSS2002.sav` | 2765 | 1119 | 1463287 | 1630748 | 0 | 4 |
| `GSS2010.sav` | 2044 | 922 | 1039687 | 844881 | 0 | 3 |
| `GSS2016.sav` | 2867 | 1018 | 1363274 | 1555332 | 0 | 3 |
| `GSS2024.sav` | 3986 | 980 | 1911284 | 1994996 | 0 | 4 |

### Common 2026 export envelope

All eight files are SPSS SAVs produced by `IBM SPSS STATISTICS 64-bit MS Windows 30.0.0.0`, carry SAV header creation date `06 Mar 26`, declare `UTF-8`, and expose `fileversion=7224.3` with label `GSS 1972-2024 Release 3 (March 2026)`. Thus the physical corpus is a set of historical-year slices inside a common March-2026 release/export envelope, not eight original historical SAV containers.

Every variable in every selected file declares the same SPSS user-missing range `[-100,-10]`. No system-missing cell was observed in any of the eight full scans. Common labels inside the declared range include `-100 iap`, `-99 no answer`, `-98 don't know`, `-90 refused`, `-80 not available in this release`, `-70 not available in this year`, and the explicitly composite `-40 dk, na, iap`. These are physical/label facts only. R05 does **not** turn them into semantic states.

No source-native SPSS multiple-response set is declared in any selected GSS file, consistent with the accepted SR03 holding that the corpus's 18 MR sets occur only in Asian Barometer Wave 5 and EVS 2008/2017. This does not erase repeated/ranked slot topology encoded in ordinary variable names/labels.

### Respondent identity

`id` is ordinal 2 in every selected release, is complete and injective within every file, and runs exactly `1..N`. But it restarts at `1` in every source. Therefore the raw bytes prove useful within-file ID behavior and simultaneously prove that `id` alone is not an injective cross-release key. No longitudinal person equivalence is inferred. `(source snapshot, source row ordinal)` remains the irreducible replay identity.

`intid` appears in 2010/2016/2024 and is labeled interviewer ID; it is highly non-injective and is not a respondent identity candidate.

### Scope, ballot/form/module/subsample evolution

- **1972:** `sample=1` for all rows: `1960 sample frame, block quota`; no `form`, `ballot`, `VPSU`, or `VSTRAT` variable.
- **1973:** `form` appears with X/Y split `753/751`; `sample=2`: `1970 sample frame, block quota`.
- **1984:** `form` expands to X/Y/Z; `formwt` appears; `sample=6`: `1980 sample frame, full probability`; `VPSU/VSTRAT` appear.
- **1993:** `ballot` A/B/C appears (`549/531/526`); `issp` appears; `sample` is mixed code 6 (`810`) and code 8 (`796`).
- **2002:** `ballotformwt`, explicit `saqissp`/`saqsex` module coordinates, and six-valued `version` appear; `sample=8` throughout.
- **2010:** `phase`, `mode`, and `subsamprate` appear with a two-phase design; `subsamprate` is physically `-100` for 1,658 rows and `0.5` for 386; expanded nonresponse/post-stratification weights appear.
- **2016:** the 2010 structural family persists; `phase=1/2` is `2294/573`, `subsamprate` is `-100/0.5`, and `random` contains both ordinary and user-missing states.
- **2024:** `mode` expands to in-person/phone/multimode/web; `modesequence` appears; `sample` bifurcates into 3,309 code-13 baseline rows and 677 code-14 AmeriSpeak rows; the latter share `phase=-100`, `modesequence=-100`, `baselinestatus=0`, `amerstatus=1`.

These coordinate facts are not routing authority. In particular, empirical missingness or co-variation is not used to infer eligibility/risk sets.

### Weight/design evolution

The family moves from `wtssall/wtssps` (1972/1973), through `formwt` and `VPSU/VSTRAT` (1984), ballot/form weights (2002), and the large 2010/2016 family (`wtss`, `wtssall`, `wtssnr`, `wtssnrps`, `wtssps`, ballot/form weights, `VPSU/VSTRAT`). 2024 breaks that surface: generic `wtss/wtssall/wtssnr` and ballot/form weights are absent from this slice; `*_next` and `*_as` candidates appear.

The 2024 domains are hostile: `wtssps_as=-70` (`not available in this year`) on all 3,986 rows, while `wtssnrps_as` is ordinary on all rows; baseline `wtssnrps/wtssps` are `-100` on exactly the 677 AmeriSpeak rows; `*_next` weights are `-100` on 2,921 rows. No candidate is selected as a default weight and no estimand is inferred.

### Repeated/ranked topology

Starting by 1984, household-person data physically expose 14 numbered slots. The March-2026 export orders those variables lexicographically, not numerically: e.g. in 1984 `where1@636, where10@637 ... where14@641, where2@642 ... where9@649`. The same pattern persists in later selected legacy/middle releases. In 1993, `mostimp1..mostimp4` explicitly encode first/second/third/fourth ordered event slots. In 2024, person-numbered families such as `talkto1..talkto5` and `race1..race5` are present.

A fixture that derives semantic slot sequence from physical ordinal adjacency would therefore be lossy even while preserving every scalar cell.

## 3. Cross-wave drift findings

The selected schema changes are large at every checkpoint: adjacent common-variable counts are `193, 298, 464, 429, 601, 649, 398`; corresponding one-sided additions/removals are recorded exactly in `CROSS_WAVE_DRIFT.csv`.

Two drift modes matter especially:

1. **Same name, changed observed topology.** `form` moves from two observed codes to three and back; `mode` changes from in-person/phone in 2016 to in-person/phone/multimode/web in 2024; `subsamprate` changes from `0.5 + IAP` to `1/.4/.3/.2 + IAP`; `VPSU` expands from `1/2` to `1/2/4/6` in 2024. A stable name/dictionary does not prove stable incidence/topology.
2. **Renamed apparent continuity without authority.** Exact same-label candidates exist across income vintages (`income72 -> income -> income82/income91 -> income98 -> income06 -> income16`, likewise `rincom*`), but names and labeled bins change. These are drift observations only. No equivalence/harmonization is inferred.

No adjacent common variable in the targeted March-2026 metadata comparison showed a changed variable label/value-label dictionary under the *same* name. That absence itself is not semantic continuity authority because observed topology and source scope still change.

## 4. Fixture-law partition indicated by the evidence

This is a reconnaissance observation, not an architecture ruling.

A **common physical-envelope fixture law** can cover all eight for: exact byte identity; UTF-8 reader path; common March-2026 Release-3 provenance; `fileversion/year/id` at ordinals `0/1/2`; SPSS user-missing range `[-100,-10]`; preservation of physically present special-code cells; and zero source-native MR sets.

A **shared structural fixture family** is plausible for **2010 + 2016** because both expose ballot/form, ballot/form weights, mode, phase, subsampling rate, questionnaire version, `VPSU/VSTRAT`, and the same named `wtss*` weight family. Expected values, ordinals, and exact schema remain release-bound.

The selected **1972, 1973, 1984, 1993, and 2002** checkpoints each cross a material structural breakpoint and therefore need release-specific structural extensions/sentinels rather than one undifferentiated early/middle fixture. **2024 requires its own special fixture** because its mode, dual-frame sample structure, and weight domains are not the 2010/2016 topology.

## 5. Documentary authority gaps

Raw bytes cannot close: cross-release semantics of `id`; weight estimands/default/combination rules; routing/eligibility meaning of form/ballot/module/phase/subsample coordinates; positive equivalence of renamed income vintages; or provenance from original historical materials into the March-2026 re-export.

A 2024-specific label gap is also present: `baselinestatus` and `amerstatus` labels literally say `... for gss 2022` while the source `year` is 2024. R05 preserves both facts and does not let one silently overwrite the other.

All gaps are enumerated in `AUTHORITY_GAPS.csv`. No novel hazard class was required.

## 6. Disposition

Every assigned source returns `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`. This is non-dispositive and is **not** source certification. No source is labeled certified/failed/blocked.

`DATABASE_URL_used=false`  
`legacy_postgres_used_as_truth=false`  
`production_runtime_modified=false`

Token: `PRE553_SR09PRE_R05_GSS_RECON_COMPLETE`
