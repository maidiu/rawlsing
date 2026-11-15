# FIABC FINAL ORACLE + T3 FREEZE PRODUCERS — R1 RETURN

Terminal:

`FIABC_FINAL_ORACLE_T3_FREEZE_PRODUCERS_R1__PASS__B03_B05_B06_DETERMINISTIC_PRODUCER_CLIS_COMMITTED__NO_SOURCE_OR_CANDIDATE_EXECUTION`

## Exact lane

- base: `4c05a5289d0dd2fb6d475e90a039cce1360b38e3`
- commission head retained: `42ed6a56c1b2a6f8f3837639bab094a154e08b5e`
- implementation head before return packet: `e45ddd0231d574d91fde64956cbc14ff59e467c2`
- branch: `agent/rabochii-premain-fiabc-final-oracle-freeze-producers-r1`

## Delivered

One committed argparse/module producer:

`rawlsing_next.fiabc_final_oracle_freeze_producers`

with three deterministic subcommands:

1. `standardize-wvs` — B03.
2. `produce-lits` — B05.
3. `freeze-t3` — B06.

Source-free hostile/contract tests are committed at:

`rawlsing_next/tests/test_fiabc_final_oracle_freeze_producers.py`

They were authored but **not executed in this browser/GitHub-only worker lane**. No local runtime, raw survey bytes, Candidate A/B/C, measured P2X, or GitHub Actions were used.

## B03 closure

The WVS adapter accepts only the frozen R1M successor wrapper:

- wrapper identity `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`
- truth payload identity `eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405`
- successor DiscoveryAuthority `3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873`
- successor Lock2 `5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139`
- successor Lock2 replay `9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a`

It validates wrapper/truth semantic identities and zero-candidate provenance, converts R1M candidate rows into the exact live T5 observation shape, proves their constituent-I03 closure against the accepted 50-ref manifest, maps the successor court into the standard WVS materializer contract, calls `freeze_wvs7_oracle_from_common_material()`, and self-verifies with `verify_frozen_oracle()`.

This lane does not own B02. Therefore the adapter deliberately fails closed if the live standard-oracle constants have not yet been rebound to the accepted successor values. It does not weaken or bypass that live law.

## B05 closure

The LiTS CLI is a real local producer. When later invoked locally it:

- verifies exact LiTS SHA-256 before semantic work;
- rejects any source or producer output rooted under `WORK_ROOT/cells`;
- uses the current governed LiTS projection/runtime authority;
- builds the common source-backed C11 repository directly;
- runs the carrier-neutral I05 executor, not A/B/C;
- reruns the exact constituent I03 roles using the same T5 closure functions;
- requires exactly 50 candidates / 77 roles;
- requires the current product and semantic replay identities to equal the accepted ASTRA identities;
- emits the three previously missing current surfaces:
  - standardized constituent-I03 fact refs,
  - constituent-I03 closure identity,
  - observation-shaped exact-ref manifest;
- loads the immutable ASTRA-D04-R2 product/replay inputs from their accepted commit;
- calls `build_lits_i_oracle()` (which invokes the existing `freeze_oracle()` law);
- self-verifies the frozen standard oracle.

No candidate provider/composition API is called.

## B06 closure

The final T3 producer:

- accepts only two verified standard oracle documents, LiTS-I and WVS7;
- rejects oracle or freeze output paths under candidate-owned `WORK_ROOT/cells`;
- verifies each oracle through `verify_frozen_oracle()`;
- verifies exact source identities;
- lifts the already-frozen authority/workload identities directly from each standard oracle's court constitution;
- binds oracle document byte SHA and relative path;
- emits exactly `RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`;
- fixes freeze order at source=10, authority/workload=20, oracle=30;
- records zero candidate outputs/roots/state reuse;
- self-validates through `load_frozen_upstream_receipt()`;
- additionally exercises the live T5 `load_frozen_source_oracle()` resolver for both sources.

## Scope

No semantic authority, candidate truth, measurement, ranking, or selection was added. No raw WVS source is read by B03 or B06. The LiTS source-reading path exists only in the B05 CLI for later local execution and was not executed here.
