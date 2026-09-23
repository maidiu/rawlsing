# WVS7 Noninterference Requirements

## Accepted terminal truth

The accepted WVS7 successor oracle records:

`{"COVERAGE_LIMITED": 46}`

with:
- candidate_count = 46
- query_role_count = 58
- successor Lock2 = `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`
- successor DiscoveryAuthority = `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`
- accepted fresh R1M oracle identity = `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`
- truth payload identity = `eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405`
- zero candidate processes/outputs at freeze.

## Effect of A — generic I03 successor jurisdiction

A is generic, so it has theoretical WVS reach. Its minimum noninterference contract is:

1. no LiTS successor authority may become visible to a WVS query;
2. a WVS I03 call that succeeds under its existing authority path must produce the same result without needing LiTS-specific catalog metadata;
3. successor fallback, if invoked anywhere, must consume the catalog identity of the exact catalog executing that call;
4. no default/ambient catalog fallback is allowed;
5. accepted WVS7 constituent facts, candidate order, family counts, terminal states, and oracle material remain unchanged.

The clean implementation pattern is to pass catalog identity from the generic `CarrierNeutralResearchExecutor.runtime_catalog`; do not hard-code LiTS catalog identity in the generic resolver.

## Effect of B — LiTS ↔ ASTRA parity closure

B should be source-local to LiTS normalization/oracle production. It must not alter:
- WVS7 materialization;
- WVS7 candidate-neutral oracle schema;
- WVS Lock2 / replay / DiscoveryAuthority;
- WVS expected fact manifest;
- WVS terminal classification;
- WVS candidate process law.

## Exact post-merge noninterference regression

A/B merged source-free qualification must include a WVS regression that proves all of the following from accepted candidate-neutral material:

1. candidate count remains exactly **46**;
2. query-role count remains exactly **58**;
3. typed terminal counts remain exactly **`{"COVERAGE_LIMITED":46}`**;
4. all 46 expected candidate facts remain in the exact accepted ordered Lock2 frontier;
5. family counts remain exact `10 / 1 / 10 / 25`;
6. successor Lock2 remains `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`;
7. successor DiscoveryAuthority remains `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`;
8. accepted source-free standardization of the R1M artifact still yields the same semantic truth payload; if byte-level output is designed to remain stable, assert the exact standard oracle identity too;
9. candidate-neutral provenance remains zero-candidate: no candidate processes, outputs, roots, or state reuse;
10. no I03 successor record bound to LiTS runtime catalog `5983d7d5...` is consumed by WVS7.

At minimum, the terminal assertion must be exact dictionary equality:
`{"COVERAGE_LIMITED": 46}`,
not “46 candidates” or “all terminal.”

## Stale qualification test that must not be mistaken for WVS truth

`rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py` currently expects old:

`WVS_LOCK2 = 8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`

while the current backend and accepted successor oracle use:

`5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`.

The test also pins an older materializer blob. This is a stale qualification surface, not evidence that WVS should be rolled back. Reconcile the test to accepted current successor truth; do not weaken exact identity checking.
