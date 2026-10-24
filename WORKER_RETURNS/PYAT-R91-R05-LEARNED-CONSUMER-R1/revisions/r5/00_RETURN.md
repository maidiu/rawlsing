# R91 R05 R5 actual linkage completion return

**Verdict: CANDIDATE_FOR_INDEPENDENT_REVIEW. The R4 named discovery/recursive linkage gap is completed with actual native AT10/AT11 owner objects plus a real joint query; R4 custody and typed axes are preserved. Full live J42/P41/E04 remains NOT_REACHED.**

## Identity

- Startup `d966b019b24ad0882ddf6964fe5dc11409ec4947`; same OpenCode author.
- Contract commit `ee999a4aada1d779364dd4734d6d4763e99d3e4b`.
- Code commit `70d1d87417bad215234145ac1b587cbeec8f98d0`.
- Prior High decision/review read and preserved.

## Delivered actual linkage

- M1 input is built directly from actual AT10/AT11 native discovery receipts,
  facts, executed queries/predicates, discovery authority and source authorities
  using `build_m1_adjudication_input_bundle`; existing explicit synthetic family
  binding/validator then adjudicates and I4 composes M1/M2/B5.
- AT10 actual `ExactBoundedDiscoveryResult` + exact receipt feeds C1
  `I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT`; same learned disposition reaches
  unchanged N10E `EXACT_SUPPORTED`.
- AT11 actual `RecursiveBranchHandoff` feeds C1
  `MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT`; handoff/parent lineage is preserved
  and the same learned consumer reaches `EXACT_SUPPORTED`.
- Actual joint query on the same AT10 native source/predicate/learned disposition
  has native target arity 2, distinct from two scalar graph slots; consumer
  reports joint count 2 and same exact N10E assertion.
- R4 retained-original coordinator/custody, E41 route reconciliation, duplicate/
  forged view refusal and typed status/Z16 axes are unchanged.

## Evidence

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05-LEARNED-CONSUMER-R1/revisions/r5/junit.xml
```

`40 passed`, 0 failed/errors/skipped, `7.64s`.

Exact R05V R1/R2/R3 probe replay: `15 passed`, 0 failed/skipped, `1.23s`.

Sever/restore: actual AT10 discovery route and AT11 recursive route each refuse
with a wrong producer predicate and restore to `EXACT_SUPPORTED`; direct/JOINT
positives and retained-original view mutation controls remain.

## Blobs / scope

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_learned_world_composition.py` | `1095f491b8867f592cd32c22fb43b25d6d41f805` (unchanged from R4) |
| `rawlsing_next/tests/test_universal_learned_consumer.py` | `9c04f789655dcf36406c3784d68372fb98562f6a` |

Only authorized paths plus own r5 return changed. Prior R4 evidence immutable.

## Limits

Full live J42/P41/E04, original science/source, F6/F7, CI/prod, N11/N12, Sorok,
J52/W52 and R04.joined remain NOT_REACHED/HOLD. Same-UID private replacement is
outside the local coordinator assumption. Distinct review follows; no
self-adoption.
