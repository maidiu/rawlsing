# FIABC-LM2-R1I — Special States and System Missing Court

## Physical side

For each Q291 variable the real frozen carrier contains four distinct physical keys classified by the physical decoder as:

`FORMAT_USER_MISSING_RANGE`

under the exact source missing declaration:

`{"kind":"range","lo":-5,"hi":-1}`.

Their R5 witness lane is `float64_finite`.

This is a **physical missingness statement only**. R1I does not infer which native special state each physical float represents.

## Governed rule side

The current R6S projection separately contains four native special-code rules constructed from Python `int` constants:

- native -5 → response state `MISSING`;
- native -4 → `NOT_ASKED`;
- native -2 → `SOURCE_SPECIFIC_SPECIAL`;
- native -1 → `DK`.

For all four:

- `canonical_value = None`;
- `transform_authority_ref = None`;
- FIABC-LM2-R1E native→canonical mapping authority is absent;
- the source-semantics/topology authority remains the extra semantic authority.

Thus the established special-state ceiling is preserved. The R1E mapping authority does not leak onto specials.

## Exact mismatch holding

The four realized physical user-missing keys and the four native-special rule keys are disjoint because the physical witnesses are R5 floats while the rules were built from R5 ints.

The court does **not** pair an individual float witness to an individual semantic special state. That would be the very A→B authority currently missing.

## System missing

Current R6S also contains one separate system-missing rule:

- physical material: `None`;
- physical state: `SYSTEM_MISSING`;
- response state: `MISSING`;
- canonical value: `None`;
- transform authority: `None`.

The real Q291 carrier contains **zero realized system-missing cells** for either Q291G5 or Q291P5. Therefore:

- there is no realized physical system-missing key that fails lookup;
- the system-missing rule appears only in `RULE_KEYS - PHYSICAL_KEYS`;
- its presence is not the R15 failure cause;
- it must remain distinct from the four format-user-missing physical states and from source-native semantic missing/special states.
