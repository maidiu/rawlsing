# Reproducing the N10W sourcefree court

**Do not mistake a test harness for a model or actor issuer.** All files are under the authorized reviewer return prefix; original inherited client code is copied byte-identically *only* as scientific evidence. No production module was edited.

## In exact reviewer branch checkout

```sh
cd WORKER_RETURNS/USERDIRECT-N10W-LAYERED-POSSIBILITY-TO-ACTOR-ARCHITECTURE-R1/repro
python -m pytest -q test_n10w_hostiles.py test_exact_native_consumers.py
python cold_replay.py
```

The reference+native court is **36 tests** total (22 research-only negative/structural tests and 14 exact original E04 client tests). Requires Python 3.13 and pytest 9; Git 2.47 was used to assert each native file's original blob. Original E04 files are **exact copies** inside `repro/native/`: `nonparent.py` `2181b832d3c4376d4b9428e13f4354f273be8f32`, `scenario.py` `b7e568166cd277c1ba127374ea1a350d1b3841a2`; original source at WP2 commit `f7824794bc6674c662734c9a8b110dd3df224be7`. In this reviewer branch the sourcefree test files are also bit-identical to actually executed local source: `n10w_reference.py` blob `2febdb26bd6a29f82f621b38a885de2e0d8996fd`, `test_n10w_hostiles.py` blob `3515eec342a24913a975f29ac74faaca22ce4fa2`, `test_exact_native_consumers.py` blob `806b4ab0e46d3b6720d8ff2d9057a021efaf481b`, `cold_replay.py` blob `eef91d4a0c9074a254f43e9b871c0ed219cfbad0`.

The synthetic `Service` adapter in `test_exact_native_consumers.py` is NOT accepted upstream source, original35, real E05R selected-world or C1/N10E. It never issues actor awareness.

## In the supplied executable evidence ZIP

`N10W_Layered_Architecture_Court_Evidence_R1.zip`, SHA256 `180debae440775fae6985c2a1efe8689ec9b1365b40430c2767cffd7134c238d`, contains **all 17** manifest/source/test/JUnit/cold artifacts, including user-provided legacy snapshots under `legacy_sources/` and a third independent test `test_legacy_driver_adversarials.py`. After extracting:

```sh
python -m pytest -q test_n10w_hostiles.py test_exact_native_consumers.py test_legacy_driver_adversarials.py --junitxml=all_reproduced.junit.xml
python cold_replay.py
```

Observed independently **39 passed, zero failed**: 36 + separate legacy 3. Node.js 22.16 was used for the legacy exact-function cases via a read-only JS VM; `csv-parser` not required. Bundle generated/tested in an isolated Python 3.13.5 filesystem. Run-time JUnit, log, manifest and both child-hash matches are included.

## Interpret the proofs narrowly

What a PASS validates: internal reference refusal/bounds, public formal vs budget practical grades from original two clients, null actor-route probabilities, distinct source inputs and two-interpreter deterministic output. It does **not** validate a generated personal history, actual CAN008 meaning/attempt, durable development or external world effect; T04–T20 actor-positive outcomes remain NOT_REACHED. No current source/use, installed N9/N10W, original35, N11/N12, OC05 or model issue follows. Exact scientific and HQ owner motions: `00_VERDICT.md`, `03_HOSTILE_DIFFERENTIAL_COURT.md`, `04_PYAT_SDTF_SOROK_OWNER_MOTIONS.md`, `05_INDEPENDENT_REVIEW_HANDOFF.md`.
