# FIABC-LM2-R1J-A — ReadStat SAV Numeric Representation Law

## Holding

The upstream format/decoder representation propositions U01-U04 and U07 are **PROVED** for both exact stacks relevant to this court:

- pyreadstat `v1.3.2` @ `97a124bfebcdf225ffbec7430e81f2868238a115`, vendoring ReadStat `b2d5407d62caf3c33caadc0495c9f7684b6a0df7`;
- pyreadstat `v1.3.6` @ `ae4bfa5d84ed5da0a1b040be472703585bdfeefc`, vendoring ReadStat `634f40a80d27221848ba57e9fb633b41146bac36`.

This is representation mechanics only. It does **not** establish that any particular WVS Q291 physical value is any particular source-native response code.

## U01 — SAV distinguishes numeric and string storage

**Disposition: PROVED.**

### Format-level corroboration

IBM SPSS Statistics documents two basic variable types, string and numeric, and states that numeric values are stored internally as double-precision floating-point numbers:

- https://www.ibm.com/docs/en/spss-statistics/32.0.0?topic=universals-variable-types-formats

The independently documented SAV system-file structure also records variable type `0` for numeric variables and positive widths for string variables:

- https://www.gnu.org/software/pspp/pspp-dev/html_node/Variable-Record.html
- https://www.gnu.org/software/pspp/pspp-dev/html_node/System-File-Format.html

### Exact ReadStat implementation

At **both** exact ReadStat revisions, `src/spss/readstat_sav_read.c` parses the SAV variable record and maps a string declaration to `READSTAT_TYPE_STRING`; otherwise it assigns `READSTAT_TYPE_DOUBLE`.

- ReadStat `b2d540...`, `sav_read_variable_record`, lines 399-402:
  https://github.com/WizardMac/ReadStat/blob/b2d5407d62caf3c33caadc0495c9f7684b6a0df7/src/spss/readstat_sav_read.c#L399-L402
- ReadStat `634f40...`, same function and lines:
  https://github.com/WizardMac/ReadStat/blob/634f40a80d27221848ba57e9fb633b41146bac36/src/spss/readstat_sav_read.c#L399-L402

**What this proves:** SAV numeric-versus-string storage is a source-format distinction consumed by ReadStat.

**What this does not prove:** that Q291G5 or Q291P5 are numeric variables. That exact-variable premise belongs to R1J-B/fan-in.

## U02 — SAV numeric variables travel through ReadStat's double lane

**Disposition: PROVED.**

For a SAV variable already classified as numeric, ReadStat fixes the variable type to `READSTAT_TYPE_DOUBLE`. During row decoding, the parser copies the 8-byte numeric cell into a C `double`, places it in `readstat_value_t.v.double_value`, and sends that value to the registered callback.

- `b2d540...`, `sav_process_row`, lines 771-780:
  https://github.com/WizardMac/ReadStat/blob/b2d5407d62caf3c33caadc0495c9f7684b6a0df7/src/spss/readstat_sav_read.c#L771-L780
- `634f40...`, same function and lines:
  https://github.com/WizardMac/ReadStat/blob/634f40a80d27221848ba57e9fb633b41146bac36/src/spss/readstat_sav_read.c#L771-L780

No value-magnitude branch chooses an integer host lane for integral-valued numeric cells.

**What this proves:** a SAV numeric variable is exposed to ReadStat clients as `READSTAT_TYPE_DOUBLE` / `double_value`.

**What this does not prove:** response semantics, canonical mappings, or any WVS-specific code identity.

## U03 — integral numeric values remain in the numeric/double representation

**Disposition: PROVED as representation mechanics.**

The ReadStat SAV parser assigns type at the **variable** level, not by inspecting whether an individual numeric value has a fractional part. Every decoded cell for a SAV numeric variable takes the same `READSTAT_TYPE_DOUBLE` path. Therefore a numerically integral SAV value (for example a source numeric value represented as `1.0`) is delivered through the double lane; it does not become a ReadStat integer merely because it is integral.

pyreadstat then preserves that lane:

- pyreadstat 1.3.2, `convert_readstat_to_python_value`, `READSTAT_TYPE_DOUBLE` branch around lines 353-358:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/_readstat_parser.pyx#L353-L358
- pyreadstat 1.3.6, same branch around lines 342-347:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/_readstat_parser.pyx#L342-L347

The conversion calls `readstat_double_value(value)`, assigns it to a C/Python float path, and does not coerce integral doubles to Python integers.

**Narrow meaning of "without acquiring a different source-native meaning":** the decoder representation change is a host representation fact only; no integer semantic reinterpretation is introduced by the decoder. This court does not itself establish what the numeric value means in WVS.

## U04 — SAV numeric user-defined missings remain numeric representations

**Disposition: PROVED.**

ReadStat reads SAV numeric missing declarations into an array of C `double` values:

- `b2d540...`, `sav_read_variable_missing_double_values`, lines 278-307:
  https://github.com/WizardMac/ReadStat/blob/b2d5407d62caf3c33caadc0495c9f7684b6a0df7/src/spss/readstat_sav_read.c#L278-L307
- `634f40...`, same function and lines:
  https://github.com/WizardMac/ReadStat/blob/634f40a80d27221848ba57e9fb633b41146bac36/src/spss/readstat_sav_read.c#L278-L307

The common SPSS layer boxes numeric missing values as `READSTAT_TYPE_DOUBLE` and attaches those typed missing ranges to the ReadStat variable:

- exact identical blob at both endpoint revisions: `src/spss/readstat_spss.c` blob `4bc7cde0813d379d59526e488b07135eeb99bb58`;
- `spss_boxed_double_value`, `spss_boxed_missing_value`, and `spss_missingness_for_info`, lines 103-156:
  https://github.com/WizardMac/ReadStat/blob/b2d5407d62caf3c33caadc0495c9f7684b6a0df7/src/spss/readstat_spss.c#L103-L156

ReadStat's defined-missing check is also byte-identical between the two endpoint revisions (`src/readstat_value.c` blob `62aac39820184626df90451f0d999887d77ea884`) and dispatches numeric missing comparison through `readstat_double_value`:

- https://github.com/WizardMac/ReadStat/blob/b2d5407d62caf3c33caadc0495c9f7684b6a0df7/src/readstat_value.c#L70-L79

**What this proves:** source-declared numeric user-missing values remain numeric/double values in ReadStat representation.

**What this does not prove:** which WVS native special-state label corresponds to any particular value. That is layer-B semantics, not decoder mechanics.

## U07 — Python-facing representation is float/double for SAV numeric variables

**Disposition: PROVED for the pyreadstat path used by Rawlsing.**

At both exact pyreadstat tags, `READSTAT_TYPE_DOUBLE` maps to `np.float64` in the parser's NumPy type table:

- 1.3.2, lines 74-76:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/_readstat_parser.pyx#L74-L76
- 1.3.6, lines 80-82:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/_readstat_parser.pyx#L80-L82

The converter's `READSTAT_TYPE_DOUBLE` branch produces the float path rather than the integer path (U03 references above). pyreadstat also exposes `metadata.readstat_variable_types[var] = "double"` for that lane:

- 1.3.2 around line 1127:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/_readstat_parser.pyx#L1117-L1131
- 1.3.6 around line 1198:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/_readstat_parser.pyx#L1188-L1202

The accepted Rawlsing decoder calls `pyreadstat.read_file_in_chunks` with `read_sav`, `apply_value_formats=False`, and `user_missing=True`; pyreadstat's chunk wrapper forwards keyword arguments to the supplied read function. Rawlsing's `_jsonable` also converts scalar objects exposing `.item()` recursively, which preserves the numeric value while producing an ordinary Python float for a NumPy floating scalar.

## Critical boundary

The upstream law established here has the form:

`IF exact SAV variable is numeric -> ReadStat SAV numeric lane is DOUBLE -> pyreadstat value lane is float/np.float64`.

It does **not** have the form:

`float64 1.0 -> WVS native response code 1`.

The first statement is decoder law. The second requires the independent exact-variable/source-semantic premises reserved to R1J-B and HQ fan-in.
