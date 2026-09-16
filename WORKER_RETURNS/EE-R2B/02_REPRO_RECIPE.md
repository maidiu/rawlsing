# EE-R2B reproducible co-location recipe

This recipe preserves the commission's `EXACT_ONLY` source rule. It does **not** copy LiTS-I to GitHub, a public mirror, LFS, a release, or any other substitute carrier.

## 1. Materialize only the authorized Library carrier

Materialize Library file id `file_0000000036dc81f8b8b546e356590a03`, version `1`, as `LITS-2006-data.dta` on the worker file surface.

Before any decode, require:

- byte size `139531180`;
- SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.

Abort on any mismatch.

## 2. Emit only the exact runtime dependency

Use `.github/workflows/ee-r2b-runtime-wheel.yml` by explicit `workflow_dispatch`. The workflow downloads only the binary wheel for `pyreadstat==1.3.6` with `--no-deps`, writes `SHA256SUMS.txt`, and uploads the result as a GitHub Actions artifact.

The qualification run for this return was:

- producer commit `a2f3b7c8c0b600f408416bc35aa8926be45d65b5`;
- workflow run `35120057454`;
- artifact id `10456488840`;
- artifact digest `sha256:ccf5a7236142f1c763fae5016adca5b662bf6a6550a150c50b44d02ff84b1225`;
- producer Python `3.13.15`;
- wheel `pyreadstat-1.3.6-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`;
- wheel SHA-256 `3ac231771dc038e0a42a4d14599af3112684f7eba680983b3ef9581db3e3b163`.

The artifact is a convenience carrier, not enduring source authority. Future reruns may emit a fresh artifact from the frozen workflow, but must require `pyreadstat==1.3.6` and independently hash the emitted wheel before use.

## 3. Co-locate runtime with carrier

Download the runtime-wheel artifact to the same worker surface as the exact LiTS-I file. Install the wheel into an isolated target/venv with `--no-deps`. Require runtime import version exactly `1.3.6`.

No pandas/Stata/other-reader fallback is permitted.

## 4. Use only the accepted decoder

Obtain `rawlsing_next/pre553_physical_decoder.py` from repository authority and require Git blob:

`13aa733b511dc23e00bfcdf288c5b920e3f09983`

The qualification execution verified that exact blob before import.

Execute only:

```python
incidence = decode_dta(EXACT_LITS_PATH, encoding="latin1")
```

The accepted decoder itself fixes `apply_value_formats=False` and `user_missing=True`.

## 5. Required pre-D03 decode checks

The co-location qualification must reproduce:

- decoder-observed source SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- source format `DTA`;
- `29002` rows;
- `1198` variables;
- `34744396` physical cells;
- `q301_2` present (qualification ordinal `194`);
- `q301_7` present (qualification ordinal `199`);
- reader version `1.3.6`;
- `encoding=latin1`;
- `apply_value_formats=false`;
- `user_missing=true`.

Only after those checks may EE-W2/D03 resume its existing exact R2/R7/R27 root materialization/replay grain. EE-R2B does not itself freeze those roots or publish learned results.

## Governing distinction

The solved transport is **runtime-to-carrier**, not carrier-to-runtime. Exact LiTS-I bytes remain on the Library-derived worker surface. The transported object is the pinned public decoder dependency, whose identity is independently hash-checked. This eliminates the predecessor's GitHub-Actions-ingress blocker without creating a second LiTS source authority.
