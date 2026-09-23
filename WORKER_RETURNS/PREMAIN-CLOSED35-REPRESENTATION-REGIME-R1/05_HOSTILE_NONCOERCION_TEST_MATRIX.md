# Hostile Noncoercion Test Matrix

This file freezes the minimum hostile law for any implementation that later consumes this registry.

| ID | Hostile | Required result |
|---|---|---|
| H01 | native int rule `1` presented with float64 physical `1.0` and no authority | FAIL CLOSED |
| H02 | float64 `1.0` presented as Decimal `1.0` by convenience conversion | FAIL CLOSED |
| H03 | Decimal `1` and Decimal `1.0` treated as the same physical token | FAIL CLOSED |
| H04 | same displayed value but different physical missing state | FAIL CLOSED |
| H05 | same value and state but different source-missing declaration | FAIL CLOSED |
| H06 | exact regime replayed under a different source SHA | FAIL CLOSED |
| H07 | exact source under a different decoder/version/config | FAIL CLOSED |
| H08 | LiTS-I q301 bridge attempted on another LiTS wave or another variable | FAIL CLOSED |
| H09 | WVS7 Q291 authority attempted on WVS1/WVS4 or another WVS7 variable | FAIL CLOSED |
| H10 | one of the nine SAV int-rule/float-physical gaps admitted because magnitudes match | FAIL CLOSED |
| H11 | missing exact value-key owner replaced with label/display semantics | FAIL CLOSED |
| H12 | source 03 or 05 missing governed variable silently ignored | FAIL CLOSED |
| H13 | declared BIG5/WINDOWS-1252 source admitted generically without exact decoder/config evidence | FAIL CLOSED |
| H14 | EVS-2008 decoder date/time object stringified or semantically interpreted by R5 | FAIL CLOSED |
| H15 | Latinobarometro-2024 raw header width forced to equal decoded dictionary/data width | FAIL CLOSED |
| H16 | historical file loaded with changed current key/hash dependency but no provenance/successor authority | FAIL CLOSED |
| H17 | historical dependency is called hermetic merely because `spec_from_file_location` was used | FAIL CLOSED |
| H18 | byte-identical ambient dependency accepted without proving byte identity | FAIL CLOSED |
| H19 | 35-source measurement input has filename match but canonical SHA mismatch | FAIL CLOSED |
| H20 | carrier/archive provenance differs but all user-authorized canonical payload SHA+size identities are exact | REPRESENTATION RESULT MAY REMAIN ADMISSIBLE; record acquisition provenance, do not weaken payload identity |
