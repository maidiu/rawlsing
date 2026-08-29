# C06 — CURRENT 18,276 ROUTING LEDGER COMPILER / COVERAGE VALIDATOR R1

BECOME VOZHD VERKHOVOD.

Repository: `maidiu/rawlsing`
Worker branch: `agent/verkhovod-c06-routing-ledger-compiler-r1`
Governing authority: Authority 45 at `16a212b7343206c81634b26f2546ad8b60a77475`.
Remain sibling-blind.

## Mission

Implement the deterministic current routing/applicability ledger compiler and coverage validator. This lane decides **no source authority**.

## Required work

1. Bind to the exact governed 18,276-row active implementation catalog and its identity hashes.
2. Define/implement the Authority-45 routing disposition schema and exact scope fields.
3. Accept future per-family adjudication ledgers and validate:
   - exact current implementation identity;
   - no duplicate or extra IDs;
   - exact total coverage 18,276 when all nine families are joined;
   - family counts 6,021 GSS; 4,434 LiTS; 2,224 EVS; 1,698 Arab; 1,219 WVS; 913 Afro; 814 Asian; 812 Latin; 141 South Asia;
   - evidence authority type and scope are preserved;
   - executable predicate serialization/replay contract;
   - scoped nonapplicability cannot be widened;
   - unresolved stays typed unresolved.
4. Add hostile tests rejecting any ledger whose membership is selected from the historical 700/99/600/699 trial partitions, aggregate counts, source-column presence or inferred completion.
5. Produce deterministic joined-ledger and unresolved-summary hashes from fixture inputs without inventing dispositions.

## Forbidden

- deciding whether any real row is routed/unconditional/nonapplicable;
- converting missing evidence into a semantic disposition;
- consuming C02-C05 results;
- V550J/architecture/V3 work.

Success token: `C06_CURRENT_ROUTING_LEDGER_COMPILER_R1_COMPLETE`
