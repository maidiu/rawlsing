# FIABC-T6 — R35 to Live-T5 Transposition Diff

## Governing bases

Live base:

`agent/vozhd-premain-fiabc-live-t5-fanin-r1@a8f913dfafd13a15cc56c6b7df4773331c1f61df`

R35 source:

`agent/vozhd-premain-fiabc-r35-fanin-r1@c3c83908fb0083c575ab1b5ea2a3a6d84f14b5ff`

No branch merge was performed.

## Byte-exact accepted additions

| R35 owner | Path | Live T6 blob |
|---|---|---|
| I01 | `rawlsing_next/pre553_physical_decoder.py` | `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78` |
| I02 | `rawlsing_next/fiabc_derivative_parentage.py` | `95d806a709ef4f4a0f33a8bf15b122a721a72e68` |
| I03 | `rawlsing_next/fiabc_whole_source_physical_equivalence.py` | `acdbc3f99f38d228d20d6a27ab7e89558af354af` |
| Q01 | `tests/test_r35_generic_guard_court.py` | `8fb4fb7f011d2789e5cc6164976ab2011e2bdeb3` |
| Q01 | `WORKER_RETURNS/FIABC-R35-Q01/01_HOSTILE_FIXTURES.json` | `df144726d48737dbca873ebcb367cd86c16ce61f` |

Focused R35 tests were likewise transposed at their accepted blobs.

## Adapted live surfaces

### Stage backend

Starting live-T5 blob:

`ec987c75d3053c452647cc3940e0b61b050d2175`

T6 blob:

`f8e02d6911c1abe45a543f025d17ddf10dc46f00`

Changed top-level functions:

- `_new_state`;
- `_wvs_structural_path`;
- `_wvs_parentage_path`;
- `_root_lineage_identity`;
- `_wvs_reader_config`;
- `_wvs_parentage_material`;
- `_wvs_projection`;
- `_assert_r5_canonical_source_root`;
- `_compose_lits` at the Candidate-A parentage branch only;
- `_compose_wvs`.

The current Candidate-C branch inside `_compose_lits` was retained explicitly from the live T2/T5 body.

No T5 S05/S15/S16/S17 replacement occurred.

### Live T4 accounting bridge

Starting blob:

`3ca3a1ce90f18fbcb2d7b5c7e3a25d41dd4b0c4e`

T6 blob:

`db5966f9c1e075f5aa255c46c5f587d7f5eddccd`

Changed functions:

- `require_derivative_parentage`;
- `preserved_stage_adjudication`.

The former T4 parentage schema is removed as an ownership law. The function is now an adapter over the generic R35-I02 verifier.

### Live driver

No T6 change.

Blob remains:

`4500cbb149fa187a766aca71568dc1f205a4c367`.

## Added live convergence surface

`rawlsing_next/fiabc_live_r35_guard.py`

Blob:

`707d1daa692bdaed23dbbdf073c594f180452bab`.

It composes R35-I03 for the current two-source edge-class declarations without entering the I05/I08 semantic chain.

## Intentionally untouched

- T1 package/runtime assets;
- T2 manifest and Candidate-C module;
- T3 process-isolation modules;
- T4 telemetry and lifecycle modules;
- T5 terminal-control module;
- T5 succession preflight;
- T5 I08 verifier;
- historical continuation reducer;
- historical LiTS-C/WVS-C failure receipts;
- raw source carriers.
