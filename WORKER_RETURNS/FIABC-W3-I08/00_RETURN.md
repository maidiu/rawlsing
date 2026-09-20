# FIABC-W3-I08 — Final I05 Terminal Verifier

Worker: `FIABC-W3-I08`  
Repository: `maidiu/rawlsing`  
Branch: `agent/rabochii-premain-fiabc-w3-i08-terminal-verifier-r1`  
Base SHA: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`  
Return path: `WORKER_RETURNS/FIABC-W3-I08/`

## Holding

IMP13 is implemented as a fail-closed current verifier contract.

The verifier accepts the Wave-2 terminal literally:

`GOVERNED I05 LEARNED EMPIRICAL PRODUCT + EXACT SEMANTIC / REPLAY / OUTPUT IDENTITY + COMPLETE COVERAGE + CONSTITUENT I03 FACT CLOSURE`.

Validated C11 and exact I03 are mandatory intermediate invariants. Neither is accepted as the final court terminal. Every admitted `source × candidate` cell must reach the full I05 terminal and independently match the same source-local candidate-neutral oracle expectation.

The verifier also consumes, rather than fabricates, explicit PASS receipts for the mechanized succession preflight and independent parity oracle.

## Exact present owner / call surface inspected

The audited P2X execution tip is `617c9c9426db12a3c0f7fea6b68a582c10759553` on `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`.

Its current final call surface is `rawlsing_next/ee_p2x_darwin_court_driver.py`:

- `_final_ready(...)` requires terminalized stage receipts and rejects unresolved common blockers;
- final stage `S17_FINAL_COMPLETENESS_AND_VERIFICATION` is then delegated to the runtime backend;
- a backend result with `verifier_complete=True` can yield `COURT_SEQUENCE_COMPLETE__S17_VERIFIED`.

That final gate predates the Wave-2 L01/B02/B05 adjudications. It does not itself prove the complete I05 terminal, independent-oracle PASS, succession-preflight PASS, constituent-I03 closure, or lifecycle identity reproduction.

The P2X driver is not present on this worker's exact Wave-2 HQ base. Copying that whole historical execution carrier onto this branch would exceed I08's burden and would collide with sibling Candidate-C/accounting/preflight/oracle work. The bounded delta therefore adds a current composition-friendly verifier module for HQ to bind into the integrated P2 S17 surface.

## Implemented verifier

Production module:

`rawlsing_next/fiabc_p2_terminal_verifier.py`

Primary API:

`verify_final_p2_terminal(document) -> deterministic PASS/BLOCK receipt`

The verifier requires:

1. exact admitted source×candidate cell set;
2. explicit succession-preflight `PASS` receipt identity + frozen manifest identity;
3. explicit independent-parity-oracle `PASS`, candidate-neutrality and pre-output freeze assertions;
4. exact source-local oracle expectation for C11 identity, I03 fact/state/replay identity, and full I05 terminal identity;
5. independent oracle-match `PASS` for every admitted candidate;
6. C11 `PASS` + exact logical-release/replay identity;
7. I03 `PASS` + exact replay identity + noncollapsed typed fact-state manifest;
8. I05 `PASS`, `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`, equal candidate/covered counts, exact source/workload/authority/frontier/coverage/product/semantic/replay/output identity;
9. exact closure of I05 constituent fact refs over the I03 fact set;
10. exact full terminal identity equality to the candidate-neutral oracle;
11. any cell-declared post-terminal lifecycle phase to reproduce the identical full terminal identity.

A typed nonqualification or failure state is retained in the BLOCK detail. It is never converted to a successful scalar/ordinary terminal and never silently omitted from the admitted cell set.

## No second semantic owner

This module is deliberately verification-only:

- it creates no `EmpiricalFact`;
- it mutates no `EmpiricalFact`;
- it creates no source semantics or discovery authority;
- it cannot choose or prune the I05 frontier;
- it cannot mint an oracle or preflight receipt;
- it compares exact identities and typed states supplied by governed owners.

Its output explicitly records `semantic_authority_created=false` and `empirical_fact_created_or_mutated=false`.

## Negative-case coverage

Focused tests prove that PASS is rejected when:

- the court stops at C11;
- the court stops at I03;
- I05 frontier coverage is partial;
- an admitted cell disappears;
- succession preflight is not PASS;
- oracle independence/pre-output freeze is false;
- pairwise candidate agreement is presented without complete independent oracle matches;
- I05 constituent fact refs do not close over I03 facts;
- semantic/replay/output identity drifts from the oracle;
- a typed fact state collapses to `None`;
- later deletion/regeneration-style lifecycle work reproduces a different terminal identity;
- an admitted cell retains a typed nonqualification instead of a complete I05 terminal.

## Execution status

No local or measured P2X execution was performed. This commission is GitHub/browser-only, and the available repository connector does not execute Python. The focused unit suite is deterministic and source-byte independent; exact commands are recorded in `02_TESTS_AND_COMMANDS.md` for the integrated/local execution surface.

The verifier intentionally cannot claim an integrated court PASS until sibling Wave-3 outputs supply real succession-preflight and independent-oracle receipts and HQ wires this verifier into the final P2 S17 composition.

## Terminal

`FIABC_W3_I08_FINAL_TERMINAL_VERIFIER_IMPLEMENTED__READY_FOR_FANIN`
