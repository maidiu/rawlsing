# FIABC-W3-I08 — Final Terminal Verifier Contract

Contract input schema:

`RAWLSING_FIABC_P2_FINAL_TERMINAL_INPUT@1.0.0`

Verifier output schema:

`RAWLSING_FIABC_P2_FINAL_TERMINAL_VERIFICATION@1.0.0`

Terminal:

`GOVERNED_I05_LEARNED_EMPIRICAL_PRODUCT__EXACT_SEMANTIC_REPLAY_OUTPUT_IDENTITY__COMPLETE_COVERAGE__CONSTITUENT_I03_FACT_CLOSURE`

## Inputs are receipts, not new truth

The verifier requires already-produced governed material. It does not materialize, infer or repair any missing item.

Required top-level inputs:

- `admitted_cells`: exact source×candidate court membership;
- `succession_preflight`: `PASS`, exact receipt identity, exact frozen manifest identity;
- `independent_parity_oracle`: `PASS`, exact receipt identity, candidate-neutral/pre-output-freeze assertions, one source-local oracle per admitted source;
- `cells`: one terminal bundle per admitted source×candidate cell.

Each source-local oracle supplies:

- `expected_c11_identity`;
- `expected_i03_identity` including exact typed fact manifest;
- `expected_terminal_identity` for full I05;
- independent `candidate_matches` covering every admitted candidate for that source.

The expected I05 identity binds:

- exact source identity;
- exact workload identity;
- exact authority-closure identity;
- exact frontier identity;
- exact coverage-receipt identity;
- learned empirical product identity;
- semantic identity;
- replay identity;
- output identity;
- `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`;
- candidate and covered-candidate counts;
- exact constituent I03 fact refs and typed states via the fact manifest.

## PASS law

Overall PASS requires all of the following simultaneously:

1. succession preflight PASS;
2. independent parity oracle PASS and explicit independence/freeze conditions;
3. terminal cell set exactly equals admitted cell set;
4. every admitted candidate has independent PASS against the same source-local oracle;
5. C11 PASS and exact oracle identity match;
6. I03 PASS and exact oracle fact/state/replay match;
7. I05 PASS with complete coverage;
8. I05 constituent refs exactly equal the I03 fact set;
9. full I05 terminal identity exactly equals the oracle expectation;
10. every cell-required later lifecycle phase has a PASS reproduction receipt with the identical terminal identity.

There is no partial/warning PASS. C11-only, I03-only, partial-frontier I05, missing admitted cells, self/pairwise agreement without independent oracle closure, or typed nonqualification all BLOCK the full court.

## Lifecycle law

The first full I05 product establishes the logical comparison terminal. Later cold/warm/delete/regenerate/invalidate/replay/audit work may remain in the wider measurement envelope. For every lifecycle phase declared required by the integrated cell contract, the verifier requires reproduction of the exact same source/workload/authority/frontier/product/semantic/replay/output/coverage/fact identity.

The verifier does not decide which lifecycle phases the measurement constitution requires. That remains owned by the equal-work/court composition. It only verifies exact reproduction for the phases explicitly supplied as required.

## Integration seam

HQ should bind `verify_final_p2_terminal(...)` into the integrated final P2 stage only after I05 and I07 fan-in can supply real independent-oracle and succession-preflight receipts. This verifier must not synthesize defaults when either sibling receipt is unavailable.
