# EE-P2X local Darwin executor — proposed receipt/verifier surface

Status: `PROPOSED_FOR_HQ_ADOPTION__NOT_OPERATIVE_AUTHORITY`

This surface exists to make the remaining local court mechanical. It performs no source access itself and contains no candidate outcome or performance value.

## Executor loop

For each lawful cell in exact order:

`LITS_I/A -> LITS_I/B -> LITS_I/C -> WVS7/A -> WVS7/B`

WVS7/C is not executed. It is covered by the preserved
`WVS7_C__CURRENT_PORTABILITY_FAILURE`.

The local executor should:

1. append the cell to `attempted_cells` before candidate work;
2. run the already-authorized stage through the adopted P2R1 carrier-neutral seam;
3. have the driver fill the cell receipt directly from raw counters/results;
4. emit the source-local learned receipt when I05/learned production succeeds;
5. emit B/C deletion-regeneration or A persistence-information receipt as applicable;
6. point the canonical coverage row at the qualifying receipt or authorized stop receipt;
7. run `12_verify_ee_p2x_local_court.py`;
8. commit only after the verifier returns the expected terminal for the evidence state.

No prose ledger is required.

## Repetition-forbidden stages

Do not execute stage IDs:

- `LITS_I_A_FIRST_BUILD`
- `LITS_I_B_CACHELESS_C11`

Consume their exact already-banked receipts. The verifier recomputes their SHA-256 and fails on drift.

A metric that genuinely was not captured by one of those preserved stages is represented as
`NOT_CAPTURED_PRESERVED_STAGE` with null value plus reason. It is never filled with zero,
estimated, inferred, or repeated merely to make the vector rectangular.

## Pre-outcome identities vs measured values

The following are exact deterministic identities and must be written before candidate outcome/performance admission:

- physical host identity token/hash;
- governed projection identity;
- exact RuntimeObjectCatalog identity;
- accepted candidate-provider identity;
- candidate-neutral oracle identity.

The current sealed HQ/P2R1 packet does not publish a single expected WVS governed-projection
binding identity, runtime-catalog identity, provider-composition identity, or oracle hash.
Therefore this proposal does not invent them. The local driver must materialize them from the
accepted frozen objects before candidate output; the verifier enforces source-local equality
where candidate-neutrality requires it.

The following are local Darwin evidence and may only be supplied by actual execution:

- source open/decode/reread counts;
- bytes read/written/rewritten;
- wall/CPU/RSS/scratch measurements;
- durable authoritative/regenerable bytes;
- cold/warm I03;
- I05/learned wall time and throughput;
- repeated-research reread/redecode;
- delete/rebuild;
- invalidation recomputation units;
- stale/corrupt cache behavior receipts;
- interruption/session recovery;
- fresh-process replay;
- audit time;
- removable-with-zero-loss bytes;
- moving-parts count;
- current execution output/product/semantic/replay identities;
- WVS learned-product identities.

## LiTS learned product

For every qualifying LiTS cell, fresh execution must produce exactly:

- 50 candidates;
- 77 independently executed roles;
- 49 `EVALUATED_SUPPORTED` + 1 `EVALUATED_VALID_EMPTY`;
- product SHA-256 `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`.

The historical D04 artifact is oracle/reference evidence only. `historic_product_substitution`
must be false.

## WVS learned product

The verifier pre-binds Lock2, DiscoveryAuthority, all 46 canonical candidate hashes, 11 exact
predicate hashes, 3 query hashes, and family shape 10/1/10/25. It requires the frontier to have
been frozen before outcome access and unchanged afterward. No synthetic fallback is admitted.

If both WVS A and B qualify, their governed product/semantic/replay identities must match.
No expected WVS outcome identity is invented in advance.

## Deletion / regeneration

For a qualifying B or C cell:

- delete P4 optional cache;
- delete P5 transient compiler state;
- retain only P1/P2/P3;
- prove C11/I03/I05 remain reachable;
- regenerate in a fresh process;
- require exact equality of before/after product, semantic and replay identities.

## Candidate A persistence classification

The A receipt separately records irrecoverable information, information-authority status,
operational persistence value and rebuild cost. The verifier rejects any receipt where
`expensive_to_rebuild_used_as_authority_basis` is true.

## Stops

Typed stops are exactly:

- `CANDIDATE_LOCAL_CORRECTNESS_FAILURE`
- `SOURCE_SPECIFIC_CANDIDATE_FAILURE`
- `COMMON_SOURCE_AUTHORITY_FAILURE`
- `WVS7_C_CURRENT_PORTABILITY_FAILURE`
- `INTERRUPTED_PARTIAL_EXECUTION`
- `PARITY_ORACLE_FAILURE`

Candidate-local/source-specific failures do not suppress later lawful cells. A failure receipt supplements, rather than replaces, the source-candidate receipt for any cell actually attempted. Common-source/interruption blockers may cover later unattempted cells explicitly; they prevent PASS and the earliest canonical disposition becomes the verifier terminal.

## Final verifier

The verifier never opens `LITS-2006-data.dta` or `WVS Wave 7.sav`.
It prints one terminal line only:

`PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE`

or the exact smallest blocker/failure disposition.

It separately writes
`WORKER_RETURNS/EE-P2X/LOCAL_COURT/90_FINAL_VERIFICATION_RECEIPT.json`.

No score, ranking, winner, candidate selection, recommendation, or cross-universe metric pool
is permitted.

## Driver-preparation fan-in note

At sealed HQ checkpoint `20260918T0210-0400`, no separate continuation-reducer or Darwin
court-driver preparation branch/return is present in the repository, and the active P2X branch
is still exactly `a954e2d6676843da8427ef2439b5d1ef33478359`. This proposal therefore binds to the
adopted P2R1 seam and frozen court directly and does not pretend to integrate an unavailable
driver artifact. If HQ later adopts a driver-prep return, HQ should bind its exact blob identities
into the expectation file before commissioning this preparation packet.
