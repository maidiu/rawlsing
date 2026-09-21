# FIABC-LM2-R1J-A — Upstream SAV / pyreadstat / ReadStat Representation Law

Terminal:

`FIABC_LM2_R1J_A_UPSTREAM_DECODER_LAW_PASS__EXACT_SAV_NUMERIC_REPRESENTATION_LAW_PROVED__VERSION_PARITY_DISPOSITION_FROZEN`

Parity disposition:

`REPRESENTATION_STACK_PARITY_PROVED__1_3_2_AND_1_3_6_EQUIVALENT_FOR_RELEVANT_SAV_NUMERIC_LANE`

## Exact commission state

- repository: `maidiu/rawlsing`
- exact base: `74205b23f546d78fed449c2f351a714be184ed8c`
- branch: `agent/rabochii-premain-fiabc-lm2-r1j-a-upstream-decoder-law-r1`
- return: `WORKER_RETURNS/FIABC-LM2-R1J-A-UPSTREAM-DECODER-LAW/`
- worker scope: upstream SAV / ReadStat / pyreadstat representation mechanics only

No WVS7 SAV or ZIP bytes were opened or materialized. No Rawlsing candidate, I03, I05, R15, or measured P2X execution occurred.

## Court holding

The exact upstream representation law needed by the R1J fan-in is proved.

For a SAV variable independently established to be **numeric**:

1. ReadStat's SAV parser classifies it as `READSTAT_TYPE_DOUBLE`, distinct from SAV string variables.
2. Its row cells are emitted through `readstat_value_t.v.double_value`, regardless of whether a particular numeric value is mathematically integral.
3. Numeric SAV user-defined missing declarations remain double-valued numeric missing definitions.
4. pyreadstat maps ReadStat DOUBLE values through its floating path (`np.float64` for the pandas/NumPy storage lane and Python floating values through conversion), not through an integer path.
5. With `user_missing=True`, SPSS defined numeric missing values are retained as their numeric values while system missing stays separate.
6. With `apply_value_formats=False`, value-label substitution is not performed and the underlying decoded numeric values remain.
7. The representation behavior relevant to points 1-6 is materially identical between exact pyreadstat 1.3.2 and 1.3.6.

This court therefore closes U01-U09 at the upstream representation layer.

It does **not** close R1I by itself, because this worker was forbidden to and did not establish the separate premise that the exact WVS7 variables Q291G5/Q291P5 are numeric source variables.

## Exact version graphs

### pyreadstat 1.3.2

- tag: `v1.3.2`
- tag commit: `97a124bfebcdf225ffbec7430e81f2868238a115`
- exact ReadStat revision in the vendored source lineage: `b2d5407d62caf3c33caadc0495c9f7684b6a0df7`
- pyreadstat parser blob: `b9733bcf4112fed59271007533e7f5398d0ba5e6`
- vendored SAV reader blob: `731d8addb14379cc7a9700f17cf217cd0c927e01`
- vendored common SPSS representation blob: `4bc7cde0813d379d59526e488b07135eeb99bb58`
- vendored ReadStat value blob: `62aac39820184626df90451f0d999887d77ea884`

pyreadstat's tagged changelog records the ReadStat update to `b2d5407...` at pyreadstat 1.3.0; 1.3.1 and 1.3.2 record no later ReadStat update.

### pyreadstat 1.3.6

- tag: `v1.3.6`
- tag commit: `ae4bfa5d84ed5da0a1b040be472703585bdfeefc`
- exact ReadStat revision recorded by the tagged changelog: `634f40a80d27221848ba57e9fb633b41146bac36`
- pyreadstat parser blob: `bd43be1928139e343469cbad456f8773c41131bf`
- vendored SAV reader blob: `5810f1ff8a92d010d8ad86d05ddd64aa227c0b92`
- vendored common SPSS representation blob: `4bc7cde0813d379d59526e488b07135eeb99bb58`
- vendored ReadStat value blob: `62aac39820184626df90451f0d999887d77ea884`

## U01-U09 dispositions

| Proposition | Disposition | Holding |
|---|---|---|
| U01 | **PROVED** | SAV numeric/string distinction is explicit; ReadStat maps SAV numeric to DOUBLE and SAV string to STRING. |
| U02 | **PROVED** | SAV numeric cells are exposed through ReadStat's double/numeric lane, not an integer host-type lane. |
| U03 | **PROVED** | Integral-valued numeric cells remain on the double/float lane; no magnitude-based integer retyping occurs. |
| U04 | **PROVED** | SAV numeric user-defined missing values remain numeric/double representations. |
| U05 | **PROVED** | `read_sav(..., user_missing=True)` retains user-defined missing numeric values rather than replacing them with system missing/NaN; system missing remains separate. |
| U06 | **PROVED** | `apply_value_formats=False` prevents value-label substitution and retains the underlying decoded values. |
| U07 | **PROVED** | The Python-facing lane relevant to this pipeline is float/`np.float64` for numeric SAV variables. |
| U08 | **PROVED** | U01-U07 representation behavior is materially identical between exact pyreadstat 1.3.2 and 1.3.6. |
| U09 | **PROVED_NO_MATERIAL_CHANGE** | The different bundled ReadStat revisions do not change the relevant SAV numeric/user-missing representation lane. |

## U08/U09 parity court

pyreadstat 1.3.2 and 1.3.6 do bundle different ReadStat revisions. Parity was therefore not inferred from the shared project name.

The exact ReadStat comparison `b2d5407... -> 634f40a...` spans 21 commits.

For the relevant lane:

- `src/spss/readstat_spss.c` is exact-blob identical at both endpoints;
- `src/readstat_value.c` is exact-blob identical at both endpoints;
- `src/spss/readstat_sav_read.c` has only one endpoint source-line difference, in a multiple-response-name parser call (`parse_mr_string` gains the parser context); the numeric variable classification, double row decoder, and numeric user-missing reader blocks are unchanged;
- pyreadstat's exact parser still maps `READSTAT_TYPE_DOUBLE` to `np.float64` and the float converter path at both tags;
- the pyreadstat public API refactor between these versions leaves the relevant `read_sav` flags and parser behavior intact;
- the relevant `handle_value` user-missing block is text-identical.

Therefore the required parity disposition is positively proved for this exact scope.

## Evidence-quality distinction

### Official/project documentation

- exact tagged pyreadstat `read_sav` API docstrings for `user_missing` and `apply_value_formats`;
- exact tagged pyreadstat changelog for bundled ReadStat lineage;
- IBM SPSS documentation as format-level corroboration of numeric/string types and double-precision numeric storage.

### Exact implementation source

- exact tagged/vendored pyreadstat sources;
- exact upstream ReadStat commits;
- exact SAV reader and common ReadStat value/missingness implementation.

### Inference from implementation

- an integral-valued numeric cell cannot switch to an integer host lane because the decoder branch is controlled by the variable type;
- the exact endpoint change set does not alter the relevant lane because its operative blocks are identical, with the only SAV-reader diff confined to MR-name parsing.

## Authority boundary preserved

This result is deliberately conditional:

`IF exact source variable is independently proven SAV-numeric`
→
`exact pyreadstat/ReadStat stack returns it through the DOUBLE/float lane`.

It does **not** assert:

`float64 1.0 means WVS native response code 1`.

That second relation still requires the independent exact Q291 variable/source premise and the source-native semantic premise at fan-in.

Accordingly this worker did not:

- issue a Rawlsing authority ref;
- broaden `SOURCE_SEMANTICS_TOPOLOGY`;
- modify R6S;
- modify R5 typed equality;
- add int/float coercion;
- weaken C11;
- infer WVS meanings from numeric resemblance;
- perform any WVS source read.

## Return artifacts

- `00_RETURN.md`
- `01_PYREADSTAT_132_VERSION_GRAPH.json`
- `02_PYREADSTAT_136_VERSION_GRAPH.json`
- `03_READSTAT_SAV_NUMERIC_LAW.md`
- `04_USER_MISSING_AND_VALUE_FORMAT_LAW.md`
- `05_132_VS_136_PARITY_MATRIX.csv`
- `06_AUTHORITY_USABILITY_BOUNDARY.md`
- `RETURN.json`

## Execution boundary

- user Mac/local runtime used: **0**
- WVS7 SAV/ZIP opened/materialized: **0**
- new WVS source read: **0**
- Candidate A/B/C: **0**
- I03: **0**
- I05: **0**
- measured P2X: **0**
- R15 retries: **0**
- WVS raw-value semantic inference: **0**
- Rawlsing production-code changes: **0**

## Terminal

`FIABC_LM2_R1J_A_UPSTREAM_DECODER_LAW_PASS__EXACT_SAV_NUMERIC_REPRESENTATION_LAW_PROVED__VERSION_PARITY_DISPOSITION_FROZEN`
