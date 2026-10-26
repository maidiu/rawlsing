# R136 coverage and limits

## Scoped result

- Production transport code path: **PARTIAL**; synthetic transport executes,
  but actual native empirical support is absent.
- Production metadata: **FAIL**; descriptor source/country/population can be
  replaced while production execution succeeds.
- Authority binding: **FAIL**; foreign query-authority source and foreign
  source-authority snapshots are accepted.
- Admission/resolver boundary: **PASS for tested host/purpose/envelope/root/
  universe/role/grade refusals**; not sufficient because pre-decode permission
  ordering is not demonstrated.
- Bounded discovery: **NOT DEMONSTRATED**; only query path tested.
- Explicit test-only regression: **PASS** (4 listed nodes; author claimed 5).

## Demonstrated mechanics

- `execute_issued_workload(... allow_test_only=False)` is reached with an
  external resolver record in the synthetic harness.
- Value 0/1 changes output refs; restoring the original resolves the same refs.
- Wrong host/purpose/envelope/roots/native universe/authority role/TEST_ONLY
  grade/unbound descriptor refuse in focused tests.
- Cold replay of the synthetic output is deterministic.
- No source/respondent, learned/M2/B5, FF/V553, actor, M1-for-all, all35,
  R09/CI/prod/N11/N12/Sorok or production adoption is claimed.

## Production requirement gaps

1. The emitted fact is `UNAVAILABLE`/`MISSING_REQUIRED_AUTHORITY`, raw 0/0; no
   actual values-read empirical positive. The query authority lacks exact
   source-universe binding; with one added, the fixture still returns
   `UNRESOLVED`/`UNSUPPORTED_RESPONSE_TOPOLOGY`.
2. Query authority validation is ALLOW/string-role only; source/universe/role/
   scope/grammar/frontier/risk/measure exact agreement is absent.
3. Supplied source authority snapshots are validated by count/role/ALLOW only;
   foreign source scope is accepted.
4. Descriptor metadata is not compared with the actual projection/source.
5. Physical response decode occurs in the harness before current permission/
   admission; the production API accepts a prebuilt decoded bundle.
6. Discovery/frontier composition is accepted by types but not exercised.

## Parent/obligation holds

Original 35/1890/F1–F8/global F6/F7/F8/LongMemory, real source/science/access,
learned release, FF/V553, actor/person/dyad/V3, M1-for-all, protected R09/CI/
prod, N11/N12, Sorok and J52/W52 remain held. This review does not select
sources, issue permissions, open source products, or establish original-source
occupancy.
