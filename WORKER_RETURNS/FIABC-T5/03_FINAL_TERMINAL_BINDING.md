# FIABC-T5 — Final Full-I05 Terminal Binding

## Accepted I08 owner

T5 transposes the accepted Wave-3 terminal verifier byte-exact:

`rawlsing_next/fiabc_p2_terminal_verifier.py`

Blob:

`c9d31ae48f4ab338a29f3054f866cd5ae51e7142`.

The only successful comparison terminal remains:

`GOVERNED_I05_LEARNED_EMPIRICAL_PRODUCT__EXACT_SEMANTIC_REPLAY_OUTPUT_IDENTITY__COMPLETE_COVERAGE__CONSTITUENT_I03_FACT_CLOSURE`.

C11 is intermediate.

I03 is intermediate.

Partial I05 is nonterminal.

Self replay is nonterminal.

## S16 cell seal

T5 seals a cell only after all of the following are explicit real receipts/material:

- candidate independent-oracle PASS;
- current C11 identity;
- current I03 exact fact/state closure;
- complete current I05 output;
- complete fixed frontier and coverage;
- exact semantic/replay/output/product identities;
- T4 S16 live accounting receipt;
- T4 write-once telemetry receipt path + exact file SHA;
- T4 S15 actually executed fresh-process replay;
- complete fresh-process C11/I03/I05 terminal projection.

The fresh replay projection must equal the original projection field-for-field.

A single equal output hash is not enough to hide drift in source/workload/authority/frontier/coverage/facts.

## S17 final composition

S17 no longer invokes the historical final-court verifier as current authority.

It constructs the accepted I08 input from:

- exact T5/I07 succession PASS;
- exact two source-local frozen oracle identities;
- source-level A/B/C same-oracle PASS receipts;
- all six current T5 cell terminal bundles;
- C11 intermediate closure;
- I03 intermediate closure;
- I05 complete coverage;
- constituent-I03 fact closure;
- T4 accounting/lifecycle evidence.

Then it invokes:

`verify_final_p2_terminal(...)`.

The verifier consumes evidence; it does not manufacture missing receipts.

## Required failure cases

The accepted I08 + T5 live seal blocks:

- C11-only terminal;
- I03-only terminal;
- partial I05 coverage;
- omitted admitted cell;
- non-PASS I07;
- missing/invalid independent oracle;
- pairwise-only agreement;
- constituent-I03 drift;
- semantic/replay/output drift;
- collapsed typed state;
- lifecycle terminal drift;
- missing/drifted T4 accounting receipt.

## R35 claim boundary

A T5 PASS is claim-scoped to the declared LiTS-I + WVS7 RAW/source-local P2 court.

It does not certify:

- whole-source physical equivalence;
- CLOSED_35 universality;
- whole files;
- 105 source×candidate cells;
- population validity;
- weighted validity.

The accepted R35 generic parentage/physical-equivalence fan-in remains unmerged here and must converge in the separate bounded post-T5 step before final qualification.
