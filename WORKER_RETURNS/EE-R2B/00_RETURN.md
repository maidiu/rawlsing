# EE-R2B — LiTS EXACT CARRIER / RUNTIME CO-LOCATION — governed return

## Terminal

**PASS — one lawful immutable runtime-to-carrier co-location path is proved for the exact LiTS-I Library bytes and the accepted PRE553 decoder/runtime.**

`EE_R2B_PASS__EXACT_LITS_LIBRARY_CARRIER_AND_ACCEPTED_PRE553_PYREADSTAT_RUNTIME_COLOCATED_BY_RUNTIME_TO_CARRIER_TRANSPORT`

## Authority read

Current canonical HQ authority was read from `HQ_HANDOFF/LATEST.json` and followed to sealed checkpoint `20260916T0307-0400` at handoff commit `251a1d45c73cbe8d46bde1051a5f114c524ba837`; semantic PRE-MAIN remains `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

HQ explicitly held EE-W2/D03 on the absence of an authorized carrier/runtime co-location path and commissioned EE-R2B to repair only that local transport deficit.

The predecessor return read was EE-W2 commit `4523f1ea392abbd3a500e3459fef176607d790b4`.

## Exact source carrier

Library permission was used as `EXACT_ONLY` for only the commissioned carrier:

- file id `file_0000000036dc81f8b8b546e356590a03`;
- version `1`;
- filename `LITS-2006-data.dta`;
- materialized bytes `139531180`;
- SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

No public/mutable LiTS mirror, substitute source, LFS copy, release copy, or repository copy was created.

## Accepted decoder identity

The executed decoder was exactly:

- `rawlsing_next/pre553_physical_decoder.py`;
- required Git blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`;
- locally verified Git blob `13aa733b511dc23e00bfcdf288c5b920e3f09983`;
- LiTS encoding `latin1`;
- `apply_value_formats=False`;
- `user_missing=True`.

No decoder substitution or pandas/other-reader fallback occurred.

## Lawful co-location arrangement

The predecessor tried carrier-to-Actions and correctly found no authorized path for the 139,531,180-byte Library object. EE-R2B proves the inverse arrangement instead:

1. Keep the exact LiTS-I Library bytes on the worker-accessible file surface.
2. On the same commissioned branch, use `.github/workflows/ee-r2b-runtime-wheel.yml` to emit **only** the pinned public runtime dependency `pyreadstat==1.3.6` as a GitHub Actions artifact.
3. Download that artifact to the worker surface where the exact Library carrier already exists.
4. Independently hash the wheel, install it with `--no-deps`, and require import version `1.3.6`.
5. Obtain the accepted repository decoder and require its exact Git blob before import.
6. Execute the accepted decoder against the already-materialized Library file.

This is runtime-to-carrier transport. LiTS source authority never leaves the exact Library file/version.

## Runtime carrier qualification

The proving workflow execution was:

- producer commit `a2f3b7c8c0b600f408416bc35aa8926be45d65b5`;
- workflow run `35120057454` — **success**;
- artifact id `10456488840`;
- artifact name `ee-r2b-pyreadstat-1.3.6-35120057454`;
- artifact digest `sha256:ccf5a7236142f1c763fae5016adca5b662bf6a6550a150c50b44d02ff84b1225`;
- producer Python `3.13.15`;
- wheel `pyreadstat-1.3.6-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`;
- wheel SHA-256 `3ac231771dc038e0a42a4d14599af3112684f7eba680983b3ef9581db3e3b163`.

The downloaded artifact independently reproduced the same wheel SHA-256. It installed on the worker surface with `--no-deps`; the local runtime imported `pyreadstat 1.3.6` under CPython `3.13.5`.

The workflow is retained as an explicit `workflow_dispatch` reproduction mechanism rather than a push-triggered background producer.

## Bounded accepted-decoder proof

Using the exact carrier, exact decoder blob, and `pyreadstat==1.3.6`, `decode_dta(..., encoding="latin1")` returned:

- decoder-observed source SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- source format `DTA`;
- rows `29002`;
- variables `1198`;
- physical cell surface `34744396`;
- `q301_2` present, variable ordinal `194`;
- `q301_7` present, variable ordinal `199`;
- recorded reader `pyreadstat`;
- recorded reader version `1.3.6`;
- recorded encoding `latin1`;
- recorded `apply_value_formats=false`;
- recorded `user_missing=true`.

A bounded 16-cell probe through the accepted decoder object API also succeeded. No R2/R7/R27 root materialization, learned-result execution, or semantic interpretation was performed in EE-R2B.

## Governed artifacts

- `WORKER_RETURNS/EE-R2B/01_COLOCATION_RECEIPT.json` — machine-readable exact identities, transport proof, decode proof, guards, successor wake.
- `WORKER_RETURNS/EE-R2B/02_REPRO_RECIPE.md` — reproducible Library + runtime-artifact + decoder-hash procedure for an EE-W2/D03 rerun.
- `.github/workflows/ee-r2b-runtime-wheel.yml` — explicit-dispatch pinned runtime-wheel emitter; it transports no LiTS bytes.

## Scope guards preserved

EE-R2B did **not**:

- use any LiTS source other than the exact commissioned Library file/version;
- create a public or mutable LiTS mirror;
- substitute the decoder;
- use pandas or another reader as a decode fallback;
- freeze R2, R7, or R27 roots;
- run learned-result execution;
- widen semantics;
- rank A/B/C;
- modify MAIN;
- modify semantic PRE-MAIN;
- mutate HQ control state.

## Successor wake

**EE-W2/D03 is now rerunnable at its existing exact grain using the proved co-location path.**

D04 is not directly released by EE-R2B; it remains downstream of D03's own accepted root materialization/replay result.
