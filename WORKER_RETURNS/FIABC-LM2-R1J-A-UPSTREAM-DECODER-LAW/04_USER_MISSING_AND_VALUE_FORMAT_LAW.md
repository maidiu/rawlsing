# FIABC-LM2-R1J-A — User-Missing and Value-Format Law

## Holding

U05 and U06 are **PROVED** at both pyreadstat 1.3.2 and 1.3.6. The exact Rawlsing reader call uses those settings through `read_file_in_chunks`, so their behavior is relevant to the physical lane under review.

## U05 — `user_missing=True` preserves SPSS user-defined numeric missing values

**Disposition: PROVED.**

### Official pyreadstat API contract

At pyreadstat 1.3.2, the exact tagged `read_sav` documentation says that when `user_missing=False`, user-defined missing values are delivered as NaN; when `user_missing=True`, missing values are delivered as-is and missing metadata is supplied.

- exact tag commit `97a124bfebcdf225ffbec7430e81f2868238a115`
- `pyreadstat/pyreadstat.pyx`, `read_sav`, lines 308-399; `user_missing` documentation around 339-343:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/pyreadstat.pyx#L308-L399

At pyreadstat 1.3.6, the same contract remains in the exact tagged `read_sav` documentation:

- exact tag commit `ae4bfa5d84ed5da0a1b040be472703585bdfeefc`
- `pyreadstat/pyreadstat.py`, implementation beginning line 607; `user_missing` documentation around 652-656:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/pyreadstat.py#L607-L714

### Implementation

At both versions, `user_missing=True` becomes the parser's user-missing flag. In `handle_value`, when a value is missing:

1. system missing remains the NaN/system-missing path;
2. if the value is a ReadStat-defined missing and user-missing preservation is enabled, pyreadstat calls `convert_readstat_to_python_value` and stores that source value;
3. for a SAV numeric variable, U02-U04 establish that this converter is the double/float path.

Exact implementation:

- 1.3.2, `pyreadstat/_readstat_parser.pyx`, `handle_value`, lines 650-722; defined-missing branch around 715:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/_readstat_parser.pyx#L650-L722
- 1.3.6, same function, lines 647-719; defined-missing branch around 712:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/_readstat_parser.pyx#L647-L719

The `handle_value` function body is byte-for-byte text-identical between the two exact tags for this court's relevant block.

**What U05 proves:** with `user_missing=True`, SAV user-defined numeric missings are not silently replaced by system missing/NaN; they remain values in the same numeric representation lane.

**What U05 does not prove:** the WVS semantic names of those numeric source states.

## U06 — `apply_value_formats=False` retains underlying values

**Disposition: PROVED.**

At both exact pyreadstat tags, `read_sav` defaults `apply_value_formats=False`. Value-label substitution is performed only inside an explicit `if apply_value_formats:` branch that calls `set_value_labels`.

- 1.3.2: `pyreadstat/pyreadstat.pyx`, `read_sav`, lines 308-399, with the label-application branch at 396:
  https://github.com/Roche/pyreadstat/blob/97a124bfebcdf225ffbec7430e81f2868238a115/pyreadstat/pyreadstat.pyx#L308-L399
- 1.3.6: `pyreadstat/pyreadstat.py`, `read_sav`, lines 607-714, with the label-application branch at 708:
  https://github.com/Roche/pyreadstat/blob/ae4bfa5d84ed5da0a1b040be472703585bdfeefc/pyreadstat/pyreadstat.py#L607-L714

Therefore `apply_value_formats=False` leaves the decoded numeric values in the data frame rather than replacing them with their display/value-label strings.

**What U06 does not prove:** that a decoded numeric value has any particular WVS response semantics.

## Chunked reader propagation

Rawlsing does not call `read_sav` directly for the full physical scan. It calls:

`pyreadstat.read_file_in_chunks(reader, ..., apply_value_formats=False, user_missing=True)`

with `reader = pyreadstat.read_sav` for SAV.

At both exact pyreadstat versions, `read_file_in_chunks` documents `**kwargs` as keyword arguments passed to the read function, removes only chunk-control keys such as `row_limit`/`row_offset`, and invokes the supplied read function with the remaining `**kwargs`.

- 1.3.2: `pyreadstat/pyreadstat.pyx`, `read_file_in_chunks` implementation on exact tag `v1.3.2`.
- 1.3.6: `pyreadstat/pyreadstat.py`, `read_file_in_chunks` implementation on exact tag `v1.3.6`.

Thus the Rawlsing reader flags are not lost at the chunking wrapper.

## System missing remains separate

The implementation separately tests `readstat_value_is_system_missing(value)`. Even with `user_missing=True`, a system-missing value follows the system-missing/NaN path rather than being treated as a source user-defined missing value. This is consistent with R1I's requirement that system missing remain outside any future source-native representation authority.

## Authority ceiling

This file establishes exact reader behavior only:

- user-defined missing preservation;
- system-missing separation;
- suppression of value-label substitution;
- propagation of these flags through the chunked reader.

It creates no response-code semantics and no physical-to-native WVS authority by itself.
