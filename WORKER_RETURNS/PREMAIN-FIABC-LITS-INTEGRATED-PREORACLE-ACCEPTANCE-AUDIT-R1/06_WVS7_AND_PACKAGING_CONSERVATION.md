# Courts 9–10 — WVS7 Current Successor and Packaging Conservation

## Result

**PASS**

## Exact current WVS7 successor truth

Accepted oracle:

`WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`

Exact observed values:

- candidate count = **46**
- query-role count = **58**
- terminal counts = `{"COVERAGE_LIMITED":46}`
- family counts:
  - UNARY_SOCIAL_FORK = 10
  - PAIR_RESPONSE_COTRAVEL = 1
  - BRANCH_CONDITIONED_DISTRIBUTION = 10
  - BOUNDED_K_WAY_RESPONSE_CONFIGURATION = 25
- Lock2 =
  `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`
- DiscoveryAuthority =
  `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`
- oracle identity =
  `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`
- truth payload identity =
  `eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405`
- candidate processes = 0
- candidate outputs = 0
- candidate-owned roots = []
- candidate-owned state reused = false

The zero-candidate provenance is present both in the oracle wrapper and its freeze receipt.

## LiTS noncontamination

The current packaging regression test imports the LiTS I03 successor authority hash and explicitly asserts that it is absent from serialized WVS accepted oracle material.

Therefore the LiTS jurisdiction repair cannot silently contaminate WVS expected truth through this path.

## Stale packaging repair

File:

`rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py`

Exact qualified blob:

`205d22f38588b40688a0738129f4bf25e1e689f3`

It now pins exact current runtime assets:

- LiTS current materializer =
  `e0bbbc03d0e7160edef5e91b15a20666f3b34f7b`
- WVS runtime package =
  `f016cdfdfd51e7973ab10b2196fe27ba5c90b3cd`
- WVS projection materializer =
  `ec685803a7416032037ee415e8faf7bf60db8f1b`

It also pins exact current Lock2, replay identity, DiscoveryAuthority, oracle identity, truth payload identity, counts and families.

The test was not deleted, skipped, xfailed, weakened or replaced by generic assertions.

It is explicitly present in both focused and broad qualification court specs.

Worker C's additional stale-packaging qualification defect is therefore closed.
