# R91 R05 R5 native linkage completion contract

Startup `d966b019b24ad0882ddf6964fe5dc11409ec4947`; same OpenCode author.
Implements the R4 unfinished actual discovery/recursive linkage, no new trust
decision.

## Native linkage

- Build the M1 bundle directly from the actual AT10/AT11 native discovery
  receipts/facts/queries/predicates and source authorities via
  `build_m1_adjudication_input_bundle`; adjudicate with the existing explicit
  synthetic family binding/validator; compose M1/M2/B5 via the existing I4 owner.
- Compose the C1 route from the same actual discovery/recursive owner objects:
  AT10 `discovery_result` + exact receipt for I05 discovery, AT11
  `RecursiveBranchHandoff` for MX01R2 recursion.
- Feed the resulting graph through the retained-original coordinator/compat
  consumer to unchanged N10E; no copied labels or invented geometry.
- Add an actual joint query on the same AT10 native source and learned
  disposition; two scalar slots remain distinct from native target arity 2.

## Required tests

Actual discovery, recursive, joint and direct positives; learned/source/query/
predicate severance and restore; retained-original coordinator view mutation;
all prior R05V probes. Full status/Z16 and E41 route rules remain from R4.

## Limits

Full live J42/P41/E04 NOT_REACHED; no source/science/CI/prod/N11/N12/F6/F7/
Sorok/J52/W52/R04 dependency. Author candidate only; distinct review follows.
