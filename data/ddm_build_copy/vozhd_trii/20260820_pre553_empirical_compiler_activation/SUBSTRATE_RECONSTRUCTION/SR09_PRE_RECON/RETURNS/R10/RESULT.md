# SR09-PRE R10 — CROSS-CORPUS ADVERSARIAL RED TEAM RESULT

Status: `COMPLETE__NON_DISPOSITIVE__ADVERSARIAL`

Branch: `agent/vozhd-trii-sr09pre-r10-cross-corpus-red-team`

Exact starting HEAD: `491a2394e323c904128ca425ef9e793e33ca0d5d`

Required success token: `PRE553_SR09PRE_R10_CROSS_CORPUS_RED_TEAM_COMPLETE`

## Holding

The combined R01–R09 evidence does **not** disclose a new generic physical hazard class outside the frozen source constitution / decoder contract.

That does **not** mean CLOSED_35 can be certified by a small set of generic format fixtures. The red-team result is the opposite: the dangerous surface is concentrated in rare **subclasses and compound combinations of already-governed hazards**. Several sources can defeat a certifier that preserves the top-level taxonomy but collapses declaration/incidence, variable identity, label dictionaries, reader configuration, topology, or source-scope coordinates.

No R10 raw-source probe was necessary. The accepted SR03 census plus the completed nine family returns closed the physical classification burden. Reopening raw bytes without a named unresolved physical ambiguity would have duplicated the family scans.

## Corpus-level physical accounting

Accepted SR03 remains the physical census authority:

- 35 exact source snapshots
- 486,174,936 physical cells
- 326,652,033 ordinary cells
- 112,031,914 system-missing cells
- 47,490,989 SPSS user-missing cells
- 22 sources with observed SPSS user-missing cells
- 18 native SPSS multiple-response sets in exactly 3 sources
- 0 row-count failures

R10 normalizes the missingness census further: **32/35 sources exercise at least one observed physical missing state**. The three zero-incidence sources are Afro Barometer Round 1 and Asian Barometer Waves 4 and 5. Zero physical missingness is itself a hostile edge because ordinary values labeled “Missing,” DK, refusal, not-applicable, or module absence still occur.

## Highest-risk exception sources

### Probable label-dependent certification blockers

**EVS 1999** and **EVS 2008** remain the strongest blockers. Both require exact SHA-bound Latin-1 compatibility execution because default metadata decoding fails. That deterministic compatibility path establishes physical structure; it does not establish intended source text. EVS 2008 compounds that text-authority gap with 13 native MR sets, including alias/overlap structures.

### Reader/configuration exceptions

**LiTS IV** remains inside the existing `FORMAT_READER_COMPATIBILITY` class but adds a distinct reader-option interaction: pandas 2.2.3 fails with `convert_missing=True, convert_dates=True` and completes the raw-state scan with date conversion disabled. The same source also combines frozen Latin-1 compatibility execution, pandas-reported UTF-8 metadata, 134 explicit skip variables, ten visit blocks, and complementary base/top-up weight missingness.

### Structural metadata exceptions

**Latinobarometro 2024** has the strongest SAV header exception: header `nominal_case_size=174`, 332 parsed logical variables, `weight_index=332`, and successful 332-value case traversal. Certification must follow the parsed dictionary rather than silently trusting or “repairing” the nominal case-size field.

**WVS Wave 1** carries a different `OTHER_NAMED_PHYSICAL_HAZARD`: `S007` is stored as raw numeric values from 320,120,001 through 8,400,122,325 while SPSS display metadata says `F2.0`. Raw storage and display metadata must remain independent.

**Arab Barometer Waves 5 and 8** exercise a third `OTHER` subclass: logical string variables consume continuation storage slots. This is already covered by the generic SAV storage/type contract but needs a hostile ordinal/alignment fixture.

## Compound hazards that generic fixtures can miss

1. **True physical missing + ordinary absence-looking code in the same variable.** Arab Wave 2 `q2062` has both `SYSTEM_MISSING` and ordinary `0` labeled “missing.” LiTS III `q112_1` and LiTS IV `q1032` show the DTA analogue: true system missing alongside ordinary refusal-looking codes. A variable-level “missing policy” would destroy source state.

2. **Declaration without incidence.** Afro Round 9 `Q78F` declares `-1` as SPSS user-missing even though no row exercises the declaration. Declaration metadata cannot be reconstructed from observed values.

3. **Entire columns in one typed state.** WVS Wave 4 has variables user-missing on every row and another system-missing on every row; WVS Wave 1 and LiTS also contain all-system-missing variables. Column-elision is not lawful replay.

4. **Overlapping/alias native MR sets.** Asian Wave 5 has overlapping `Q112` / `SE15` membership; EVS 2008 has duplicate/alias MR declarations and overlapping set membership. Native set identity cannot be deduplicated merely because variable lists overlap.

5. **Raw-vector equality without metadata identity.** WVS Wave 4 `V220` and `Q223_LOCAL` are raw-identical across all rows but have different label dictionaries. WVS Wave 7 extends this to three parallel label views. Raw equality is not variable equivalence.

6. **Ordinary blank strings.** Arab Wave 8 `BLOCK_ID` is the ordinary empty string on 2,408 Iraq rows and has zero system-missing cells. Empty-string-to-null normalization would erase source information.

## Identity red team

No family-wide native respondent-key law survives the combined returns.

- South Asia Wave 1 exposes no evident native respondent/case identifier at all.
- Arab Wave 8 has 2,400 ordinary `ID=0` Jordan rows.
- WVS Wave 4 retains genuine `country+V3` collisions after typed-missing IDs are excluded.
- Afro Round 1, Arab Waves 1/5, Asian Wave 5, Latinobarometro 1995, South Asia Wave 2, LiTS II/III, and WVS Wave 7 each expose candidate-specific collision/scope problems even where another candidate may be injective.
- EVS has native candidates (`id_cocas`, `caseno`) but R04 did not measure their injectivity; R10 therefore refuses to invent a corpus-wide native-ID incidence claim.

The frozen source-snapshot + zero-based row ordinal identity remains the only safe universal replay identity.

## Country / scope red team

The strongest cross-wave failure mode is treating numeric country or regional codes as stable identifiers.

Examples include LiTS II versus IV assigning different numeric codes to decoded Albania, South Asia changing country meanings beginning at code 3, Latinobarometro year/country code drift, WVS parallel split-up coordinates, and unobserved dictionary-domain countries in Asian Wave 5 / South Asia Wave 2 / LiTS II.

Dictionary domain, observed support, raw numeric/string carriers, and canonical country semantics must remain separate until authority closes each mapping.

## Weight / design red team

There is no lawful default-weight rule derivable from raw files.

The source surface ranges from no obvious candidate, through one or two weights, through WVS Wave 1’s 13 weight-like variables and EVS 2017’s calibration/design/population weight family. Missingness can occur inside weight/design candidates themselves. LiTS IV’s base/top-up weights have complementary missing masks. Raw values, names, labels and distributions establish physical candidates only; role, estimand, normalization, combination and variance design remain documentary authority.

## Encoding / text red team

The six frozen compatibility-execution snapshots remain exactly bounded: EVS 1999/2008 and LiTS I–IV.

Other special text risks do **not** justify widening that compatibility allowlist:

- Asian Wave 1 explicitly reports BIG-5. That is source metadata, not an ad hoc compatibility guess.
- Arab Wave 1 explicitly reports UTF-8 but contains literal C1 controls in metadata. Exact text must be preserved; typography repair requires authority.
- LiTS III/IV demonstrate cross-reader encoding-report conflict under an already-frozen compatibility path.

No non-allowlisted source has been shown by the accepted evidence to require a new compatibility override.

## Taxonomy and output-schema attack

The frozen top-level hazard taxonomy remains sufficient, but three cross-worker reporting weaknesses must be fixed before HQ treats R01–R09 as a machine coverage ledger:

1. `OTHER_NAMED_PHYSICAL_HAZARD` is too coarse for fixture batching. Its four explicit sources represent three unrelated subclasses. Keep the top-level class, but freeze named subclasses in the G-SR09 exception layer.

2. `hazard_class_counts` is not unit-stable across workers. Some family results count sources, others findings/rows, and some count negative metadata-absence burdens. **Do not mechanically sum those fields.** R10 normalizes exact censusable classes and marks the rest as minimum explicit incidence or pair/family-unit drift.

3. `HOSTILE_SENTINELS.physical_state_expected` is being used for both cell physical states and metadata sentinel kinds (`METADATA_SENTINEL`, `RAW_BYTE_SEQUENCE`, `FORMAT_READER_COMPATIBILITY`, topology metadata, etc.). Downstream automation needs either a frozen mixed vocabulary or a separate sentinel-kind dimension.

These are output/governance gaps, not new raw-source physical classes.

## Likely family-worker overgeneralizations

- Afrobarometer: do not back-project Round 5’s `997` regime into R1/R9.
- Arab Barometer: do not assume country+ID becomes injective or that Q1/STRATUM equality is stable.
- Asian Barometer: do not import UTF-8 / zero-physical-missing / MR topology across waves.
- EVS: do not treat compatibility-decoded labels as source-text authority or transfer 2008 MR/weight topology to 2017.
- GSS: do not generalize the 2010/2016 structural subset into 2024.
- Latinobarometro: exact names are not semantic continuity; all 47 shared 2011/2024 names change labels.
- LiTS: country carriers/codes, missing density, reader text reports, weights and module topology are release-specific.
- South Asia: country codes and missing representation change between waves; neither wave supplies a reusable native-ID law.
- WVS: ID, weight, country and missing-code surfaces are wave-specific; raw-vector equality can coexist with metadata distinction.

## Disposition

- New top-level physical hazard class: **none observed**
- Raw R10 probe: **not required**
- Source certification performed: **no**
- Semantic authority decided: **no**
- Every CLOSED_35 source remains `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`
- EVS 1999 and EVS 2008 additionally remain `PROBABLE_CERTIFICATION_BLOCKER` for label-dependent certification until documentary text authority closes
- Cross-worker count/sentinel schema issues: `DOCUMENTARY_AUTHORITY_GAP`
- Pair/family drift classes without a frozen source denominator: `RECONNAISSANCE_INCOMPLETE` for exact source-count arithmetic only

See `CROSS_CORPUS_HAZARD_MATRIX.csv` for normalized rare/subclass coverage and `SR09_EXCEPTION_QUEUE.csv` for prioritized HQ action.
