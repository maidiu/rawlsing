# Upstream decoder/version evidence

## Exact versions

| stack | exact pyreadstat tag / commit | bundled ReadStat revision |
|---|---|---|
| persisted R1G | `v1.3.2` / `97a124bfebcdf225ffbec7430e81f2868238a115` | `b2d5407d62caf3c33caadc0495c9f7684b6a0df7` |
| Lock1 runtime | `v1.3.6` / `ae4bfa5d84ed5da0a1b040be472703585bdfeefc` | `634f40a80d27221848ba57e9fb633b41146bac36` |

The 1.3.2 changelog records the ReadStat update at `change_log.md:10-12`; the 1.3.6 changelog records its exact ReadStat revision at `change_log.md:1-4`.

Relevant tagged blob identities:

- 1.3.2: `src/readstat_value.c` `62aac39820184626df90451f0d999887d77ea884`; `src/spss/readstat_sav.c` `62188bba9d26b73ff03ede34e50d936432f8bc82`; `src/spss/readstat_sav_read.c` `731d8addb14379cc7a9700f17cf217cd0c927e01`; `pyreadstat/_readstat_parser.pyx` `b9733bcf4112fed59271007533e7f5398d0ba5e6`.
- 1.3.6: `src/readstat_value.c` same blob `62aac39820184626df90451f0d999887d77ea884`; `src/spss/readstat_sav.c` same blob `62188bba9d26b73ff03ede34e50d936432f8bc82`; `src/spss/readstat_sav_read.c` `5810f1ff8a92d010d8ad86d05ddd64aa227c0b92`; `pyreadstat/_readstat_parser.pyx` `bd43be1928139e343469cbad456f8773c41131bf`.

## Burden 1 holdings

1. **SAV variables are ReadStat string or double — PROVED.** In both exact tags, `src/spss/readstat_sav_read.c:399-403` assigns A/string variables `READSTAT_TYPE_STRING`; otherwise `READSTAT_TYPE_DOUBLE`.

2. **Numeric SAV cells enter the double lane — PROVED.** In both exact tags, the row reader at `src/spss/readstat_sav_read.c:771-780` copies eight bytes into `fp_value`, byte-swaps if needed, assigns `value.v.double_value = fp_value` (line 777), tags missingness, then calls the value handler.

3. **Numeric SAV user-defined missings are doubles — PROVED.** Both tags use `sav_read_variable_missing_double_values` at lines 278ff/338ff; defined-missing numeric material is read and normalized as C `double` before being attached to the variable metadata. The same double-valued cell is tagged against that metadata.

4. **`read_sav(..., user_missing=True)` preserves defined-missing numeric values — PROVED.** In both tagged `_readstat_parser.pyx`, the missing-value handler at 1.3.2 lines ~698-718 / 1.3.6 lines ~695-715 first converts to NaN when user missings are not requested or the value is system missing; for `readstat_value_is_defined_missing`, it calls `convert_readstat_to_python_value` and stores the original numeric value. The public `read_sav` documentation states user-defined missings are delivered as-is when `user_missing=True`.

5. **`apply_value_formats=False` leaves values unlabelled — PROVED.** The public `read_sav` wrappers default this flag to false; label substitution is guarded by `if apply_value_formats:` (1.3.2 `pyreadstat.pyx:396`; 1.3.6 `pyreadstat.py:708`).

6. **Python-facing double representation is deterministic for this lane — PROVED.** Both exact parser tags map `READSTAT_TYPE_DOUBLE: np.float64` (1.3.2 line 76; 1.3.6 line 82). Both conversion switches obtain `readstat_double_value(value)`, cast/store it through the float path (1.3.2 lines 351-356; 1.3.6 lines 340-345). Q291 is `F3.0`, not a date/time format. The accepted R1G physical carrier independently records the resulting nine relevant values as exact `float64_finite` R5 bit patterns.

7. **Relevant behavior is stable between 1.3.2 and 1.3.6 — PROVED.** The bundled ReadStat comparison shows `readstat_value.c` and `readstat_sav.c` are blob-identical. The only relevant-file delta in `readstat_sav_read.c` is multiple-response-set parser context plumbing; the variable type decision, missing-double reader, and row double lane are unchanged. The pyreadstat parser retains the same `READSTAT_TYPE_DOUBLE -> np.float64`, C-double conversion, and defined-missing handling.

## Source links

- https://github.com/Roche/pyreadstat/tree/v1.3.2
- https://github.com/Roche/pyreadstat/tree/v1.3.6
- https://github.com/WizardMac/ReadStat/compare/b2d5407d62caf3c33caadc0495c9f7684b6a0df7...634f40a80d27221848ba57e9fb633b41146bac36

## Holding

`REPRESENTATION_EQUIVALENCE_PROVED__R1G_CARRIER_ADMISSIBLE`

No 1.3.6 source reread is required for this representation premise.
