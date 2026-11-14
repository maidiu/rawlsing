# Locality candidate — risk, exactness and potential REDs

## What the candidate changes

`locality_probe.py` patches only the module-global `sorted` lookup in
`rawlsing_next._pre553_query_eval`.  When it sees the native
`sorted(index.respondents.values(), key=lambda item: item.ref.key)` call, it
returns the same immutable `RespondentIdentity` objects in the session mapping's
physical insertion order.  Every other sort falls back to builtins.  There are
three respondent-sort call sites in the module (lines ~364, ~448, ~697); all
become physical-order.  No production file, predicate, risk, denominator,
occurrence, authority, root, CURRENT or replay owner is edited.

## Exactness observed

- 1k: selected, reverse F2 and 3-way F4 -> fact ref, full semantic projection
  SHA-256, replay ref and release refs all equal baseline.
- 10k: selected, reverse F2 and 3-way F4 -> all equal baseline.
- 100k: selected -> all equal baseline.  `SUPPORTED`, denominator 50,000.
- 64-respondent representative oracle and changed/restore:
  `test_locality_candidate.py` 2 passed; candidate facts equal native oracle,
  changed C changes the fact, old root restores exact old fact.
- Candidate hostiles: denied CURRENT, wrong direct-I02 source and missing
  locator refuse under the same override; the 1k retained estate also refused
  denied CURRENT and wrong source root (`evidence/candidate_hostile_1k.json`).
- No fallback, no full C11 graph, no whole-table read, no new persistent cache
  or index was introduced.

## Potential REDs and exact status

1. **100k F2/F4 order sensitivity** — `NOT_RUN`.  10k F2/F4 exact parity is the
   scale proxy; the original 100k F2/F4 remain `NOT_INDEPENDENTLY_REPRODUCED`.
   This is the main unproven candidate axis.
2. **Candidate I05 / grouped execution** — `NOT_RUN`.  The patch changes the
   same eval module; no candidate I05 or grouped-scope fact comparison was run.
   Do not claim those readers for the candidate.
3. **Other `RespondentIdentity` sorts** — audited by source grep: the three
   respondent traversals are the only such sorts in the eval module.  A future
   production change that adds another respondent sort would need re-audit.
4. **Physical insertion order dependence** — the candidate assumes the session
   `respondents` mapping follows the physical RespondentIdentity Parquet order.
   `DirectEstateI03Session._build` builds it from `iter_family`, which is
   row-group order.  The reviewer estates confirm this; a future reader that
   reorders that mapping would need re-qualification.
5. **Fact/replay canonical order** — no RED observed; exact refs/projections
   equal at all executed scopes.  This does not prove arbitrary new evaluator
   branches are order-independent.
6. **Known #999 native body-truth RED** — external and still open.  This
   candidate does not repair native coherent-body poison and must not be
   presented as blanket native correctness.
7. **Resource cap** — 100k candidate selected tree RSS 2.81 GiB, below 6 GiB;
   temp SQLite 1.301 GB unchanged; no candidate run was killed.

## Handoff condition

The candidate is a measured, exact-at-executed-scope runtime experiment, not a
production patch.  A production implementation needs an explicit narrow S2-C/D
owner handoff, coordination with the qualified S2-A native body-truth
descendant, an owner-approved traversal-order hook or equivalent, and
independent G5 including 100k F2/F4, I05/grouped and the preserved hostiles.
