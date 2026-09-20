# CLOSED35-R1-GSS1973 — GSS 1973 Split-Form Governed Source-Specific Realization

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-closed35-l2-documentary-fanin-r1@5c582e2325ecc2b37377cd518fe4c456331c81d8`  
Worker branch: `agent/rabochii-closed35-r1-gss1973-realization-r1`  
Source: `GSS1973.sav`  
Canonical SHA-256: `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2`

## Terminal

`CLOSED35_R1_GSS1973_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`

## Holding

The GSS 1973 source-specific realization contract is implemented at the documentary/semantic-owner layer without opening or executing the raw source.

This realization does not claim realized X/Y counts, physical missing-code incidence, or any measured output. It defines the governed source-specific surface that a later exact-carrier execution must populate and that all A/B/C candidates must consume identically.

The owner surface is:

`GSS1973_SEMANTIC_OWNER_V1`

A/B/C may differ in physical implementation only. They may not independently reinterpret FORM, CLASS/CLASSY, routing, weights, design, income history, or Q105 Card X/Y.

## Implemented law

1. `FORM=1` means standard Questionnaire X.
2. `FORM=2` means Questionnaire Y.
3. Form assignment was randomized within quota type.
4. Form-specific membership comes from the producer's 1973 Appendix P registry, not from missingness.
5. `CLASS` belongs to X / FORM=1.
6. `CLASSY` belongs to Y / FORM=2.
7. `CLASS` and `CLASSY` are distinct variables with distinct response dictionaries.
8. Ineligibility is classified before response missingness:
   `FORM_NOT_ADMINISTERED -> ROUTED_SKIP -> SUBSTANTIVE_NONRESPONSE -> PHYSICAL_MISSING_UNCLASSIFIED`.
9. Q105 Card X/Y is a separate coordinate from Questionnaire FORM X/Y unless later authority proves a join.
10. No 1973 form weight is authorized.
11. `WTSSPS` is the current producer-authorized general 1973 weight, but it may be bound only if the exact carrier exposes it.
12. `WTSSNRPS`, `FORMWT`, and `BALLOTFORMWT` are not authorized for 1973.
13. 1973 uses the 1970-frame block-quota design; later survey-estimation strata/clustering assumptions are not imported.
14. `INCOME72@1972` and `INCOME@1973` are not source-semantic equivalents.
15. Unknown physical realized form counts remain an exact-carrier observation for the later execution court and do not reopen documentary authority.

## Candidate-neutrality

Future A/B/C qualification must bind the exact source SHA and materialize the same semantic-owner contract before candidate-specific processing begins.

No candidate may:

- infer form from missingness;
- derive form membership by suffix/name heuristics;
- alias `CLASS` with `CLASSY`;
- merge `INCOME72` with `INCOME`;
- invent or stack a form weight;
- use `WTSSNRPS` for 1973;
- use Q105 Card X/Y as the FORM coordinate;
- translate physical missingness directly into routing semantics.

## Outputs

- `01_REALIZATION_CONTRACT.md` — normative semantic-owner contract.
- `02_SPLIT_FORM_PROJECTION_MAP.csv` — governed source-specific projection map.
- `03_PHYSICAL_EDGE_BINDING.json` — exact source / edge-class / owner binding.
- `04_TEST_PROTOCOL.md` — future qualification rejection protocol.
- `RETURN.json` — machine-readable return.

## Execution boundary

- raw source carrier opened: **no**
- source executed: **no**
- source decoding run: **no**
- measured P2X run: **no**
- physical form counts asserted: **no**
- physical missing-code mapping asserted: **no**

This worker implements the source-specific contract; it does not perform source realization by observing raw bytes.
