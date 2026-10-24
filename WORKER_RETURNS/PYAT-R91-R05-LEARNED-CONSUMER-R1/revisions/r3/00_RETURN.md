# R91 R05 R3 actual graph consumer return

**Verdict: CANDIDATE_FOR_INDEPENDENT_REVIEW. The R05V R2 P1/P2/P3 defects are repaired at the callable grain; full live J42/P41/E04 remains NOT_REACHED.**

## Identity

- Startup `d9e809094a2398d20273605afada8ad9b81a3dda`; same OpenCode DeepSeek
  V4.1-Flash MAX/Global author/branch.
- Contract commit `45cf09d55f80109114454d859aeb9b68ba6d2184` (before code).
- Code commit `0c416bed7fdae59cbb57a190d1ea215eae8de44a`.
- R05V R2 review read/preserved: `01d59c7ca8335c5d1f38041f4d76624b38c5c7fd`.

## Repairs

### P1 actual graph validation

`NativeProductGraph` components are now reconciled with native component
topology/route fields:

- joint component count/order must equal target topology arity, component count
  and declared order semantics;
- direct route must not carry discovery/recursive labels;
- discovery route must carry actual receipt/frontier and no recursive labels;
- recursive route must carry handoff/lineage;
- duplicate component identities refuse;
- returned graph values come from the authoritative component projection, not
  copied caller metadata.

E41 extension must be the actual `EmpiricalPossibilitySliceExtensionResult`, its
composition must be in the graph, its route must be an accepted E41 route, and its
consumer hash must equal the component consumer hash. Fake objects/routes refuse.

### P2 joint state validation

Exact support requires `producer_fact_state == SUPPORTED`, `analytical_state ==
SUPPORTED`, and denominator equal to evidence raw support. Disagreement returns
typed `ZERO_SUPPORT`/`VALID_EMPTY`/`UNKNOWN` etc. with denominator/cells/Z16
preserved; false exact support is impossible.

### P3 duplicate definitions

Removed the duplicate/shadowed consumer definition block. One active
`NativeProductGraph`, `LearnedWorldConsumerResult`, helpers and
`evaluate_learned_world_consumer` remain.

## Actual evidence

- Actual M01 -> discovery/facts -> M1 `RULE_SATISFIED` -> M2 release -> C1
  conditional evidence (denominator 1, cells 0=0/1=1) -> unchanged N10E
  `EXACT_SUPPORTED`; E41 direct extension reaches same consumer hash.
- Actual two-component graph test uses two distinct actual C1 composition
  executions on the same native source/predicate/consumer; graph joint count 2,
  two distinct component hashes, same consumer assertion.
- Duplicate component, copied graph labels, fake E41 route, producer/analytical
  disagreement, typed ZERO_SUPPORT/VALID_EMPTY/UNRESOLVED16 all refuse/typed as
  required.

## Tests

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05-LEARNED-CONSUMER-R1/revisions/r3/junit.xml
```

`37 passed`, `0 failed/errors/skipped`, `10.02s` (7 R05 tests + 30 learned-world
regressions).

Exact R05V R1+R2 probes replay, exit 0:

`9 passed`, `0 failed/skipped`, `1.31s` — R05V R1 4/4 and R05V R2 5/5
(`r05v_probes_replay.xml`).

## Blobs / scope

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_learned_world_composition.py` | `4e013062c433659a94f63995ba1b8179096bca9d` |
| `rawlsing_next/tests/test_universal_learned_consumer.py` | `b942370e83cb901fc1a6b1b31ad98c345afda039` |

Only the authorized two code/test paths plus own r3 return changed. Accepted
C1/provider/evaluator/R03/R08 bodies remain unchanged.

## Limits

Actual discovery/recursive C1 routes are validated by route/ref consistency but
the materially exercised graph is two direct-route compositions; a real
discovery/recursive C1 composition linked to the same learned disposition is not
available in the current fixtures without inventing linkage. It is named here as
the remaining test-coverage limit, not hidden. Full live J42/P41/E04 service,
original science/source, F6/F7, CI/prod, N11/N12, Sorok, J52/W52 and R04.joined
remain NOT_REACHED/HOLD. Distinct review follows; no self-adoption.
