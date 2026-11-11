# RED at intake head c2f4737e

Exact probe at `c2f4737e27ee6e83ae6ac7bb721aa0a3b34aa681` using
`rawlsing_next.tests.test_pre553_source_backed_c11_facade._fixture` and an
`ExactPhysicalCellStream`, with an explicit private `NONRESPONDENT_SOURCEFREE`
policy file and no `RAWLSING_C11_ACCELERATOR_DIR`:

```text
default files 0 release a2f301007b449e18
coldfalse files 1 release a2f301007b449e18 equal True
```

The normal `build_source_backed_c11_repository` cold default returned the exact
release but wrote zero derived cache files.  `cold=False` wrote one.  This is
the combined W03/W04 governed-default RED: streaming cold construction bypassed
the existing policy/cache composition.

No source/science/original35/SAV/DTA/DB/actor/protected effect.
