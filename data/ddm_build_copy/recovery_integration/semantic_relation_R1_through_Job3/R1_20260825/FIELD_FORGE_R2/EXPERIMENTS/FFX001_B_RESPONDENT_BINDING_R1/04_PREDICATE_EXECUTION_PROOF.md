# FFX001-B — PREDICATE EXECUTION PROOF

## Exact current predicate objects

The C04 full-current court archive was replayed and the six Q86 predicate objects were recovered from `C04_POSITIVE_ROUTING_PREDICATES.jsonl` (SHA256 `78af4494282dbabc6b331e4f12dcf7df4c3c47a9cb2b5e154b9b801dcbad5576`).

All six use the same compiled predicate:

`COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}`

with AST:

`{"all":[{"field":"COUNTRY_ALPHA3","op":"not_in","values":["ALG","EGY","MRC","SUD","TUN"]}]}`

Exact mapping:

| member | predicate_id | evidence_ref |
|---|---|---|
| Q86A | `C04P.9c3bd54f111f068a22f8` | `SEP.U1.NATIVE.9c63ebbd5ad1126a9d88ba07` |
| Q86B | `C04P.34fb5970fdb1af3cbaec` | `SEP.U1.NATIVE.b67bc175b86139b78d81f118` |
| Q86C | `C04P.40fdf23da878e2774e48` | `SEP.U1.NATIVE.4236462666e913b0f36f4196` |
| Q86D | `C04P.b75dfbead8f71621ac5f` | `SEP.U1.NATIVE.c3ff715d3830f3c01f49c3fb` |
| Q86E | `C04P.a93e49ae75ebbe415686` | `SEP.U1.NATIVE.a18cdf46693c2ff716ce0c31` |
| Q86F | `C04P.153aaa6fa7f3c82c4230` | `SEP.U1.NATIVE.965fe312a83fed515af1e2b8` |

## Native-primary provenance

Each evidence reference resolves in `C04_CLOSURE_EVIDENCE_INDEX.jsonl` (SHA256 `6042f4f8927b6b959f4391b1ed3b7456ff70bfbe4ede0c600d98a600b9218423`) to:

- artifact: `merged_r5_codebook_2.pdf`
- artifact SHA256: `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`
- authority grade: `NATIVE_PRIMARY`
- fact summary: `* Not asked in ALG, EGY, MRC, SUD, TUN`
- origin: `W07_U1`

Source locators by member:

- Q86A: extracted text lines `3201-3210`
- Q86B: `3211-3220`
- Q86C: `3221-3235`
- Q86D: `3236-3245`
- Q86E: `3246-3256`
- Q86F: `3257-3267`

## Determinism

The predicate semantics themselves are executable and deterministic given a governed respondent-level input `COUNTRY_ALPHA3`:

- if respondent `COUNTRY_ALPHA3` is one of `ALG, EGY, MRC, SUD, TUN`, the Q86 member is not administered by the native country restriction;
- otherwise the named-country restriction does not bar administration.

This statement does **not** by itself establish full respondent exposure. Other source mechanics would still have to be preserved if they existed at respondent grain.

## Execution blocker

No CURRENT governed respondent carrier/key relation was established that supplies `COUNTRY_ALPHA3` for a specific respondent and binds that same respondent to the current Q86 question implementations.

Therefore the predicate is **semantically executable but not executable at respondent grain within the currently established binding chain**.

Typed status:

- `predicate_semantics_status = ESTABLISHED_CURRENT_AUTHORITY`
- `predicate_input_required = COUNTRY_ALPHA3`
- `respondent_input_binding_status = NOT_CANONICALLY_REACHABLE`
- `respondent_predicate_execution_status = NOT_EXECUTED`
- `exposure_rows_emitted = 0`

## Prohibited substitute executions

The worker did not execute any of the following substitutes:

1. `response nonmissing -> exposed`;
2. `response missing -> not exposed`;
3. source/wave co-membership -> exposed;
4. Contract@2 routing positivity -> respondent exposed;
5. historical row alignment -> respondent binding;
6. guessed/fuzzy country-variable matching -> predicate input.

## Holding

`QUESTION_LEVEL_ROUTING_AUTHORITY != RESPONDENT_LEVEL_PREDICATE_EXECUTION`

The missing seam is not the Q86 predicate definition. It is the canonical CURRENT respondent binding needed to feed that predicate lawfully.
