# Version-parity holding

Decision:

`REPRESENTATION_EQUIVALENCE_PROVED__R1G_CARRIER_ADMISSIBLE`

R1G persisted the Q291 carrier with pyreadstat 1.3.2. Lock1 requires pyreadstat 1.3.6. The relevant representation lane is proved equivalent between the two exact tagged stacks.

- 1.3.2 exact commit: `97a124bfebcdf225ffbec7430e81f2868238a115`; bundled ReadStat `b2d5407d62caf3c33caadc0495c9f7684b6a0df7`.
- 1.3.6 exact commit: `ae4bfa5d84ed5da0a1b040be472703585bdfeefc`; bundled ReadStat `634f40a80d27221848ba57e9fb633b41146bac36`.
- SAV non-string variables remain `READSTAT_TYPE_DOUBLE`.
- SAV numeric cell values remain `value.v.double_value`.
- numeric user-defined missing definitions and cells remain on the double lane.
- pyreadstat remains `READSTAT_TYPE_DOUBLE -> np.float64`.
- `user_missing=True` preserves SPSS defined-missing values through the ordinary numeric converter while system missing remains NaN/separate.
- `apply_value_formats=False` continues to skip label substitution.
- the relevant ReadStat C files are identical except for unrelated multiple-response-set parser-context plumbing.

Accepted Rawlsing metadata independently proves Q291G5 and Q291P5 are declared `double` variables, and the frozen R1G carrier records the expected exact float64 bit patterns. Therefore no respondent-value reread and no metadata-only local operation is required.

This holding is source/variable/configuration scoped. It is not a general promise of pyreadstat version equivalence.
