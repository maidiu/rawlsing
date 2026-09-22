# FIABC Cloud Source-Backed Pre-Candidate Reproduction — R1

## Disposition

This court is **BLOCKED before real production invocation**.

Remote state was verified rather than trusted:

- governed execution branch = `7b38c22dd469735eed0b0c01c304a028dd3046cf`
- repair branch = `7b38c22dd469735eed0b0c01c304a028dd3046cf`
- qualified production code head `ea0baa4d87244a548ba9a6a46a883d307c65e3e4` is an ancestor of dispatch head
- source-free qualification closure `4c1641d1f1ec51a4116d0664dbf149e915465bdb` is an ancestor of dispatch head

The isolated worker branch was created from exact dispatch head. The governed execution branch was not moved or modified.

## Exact sources

Both source carriers were located in the user's connected Library estate and materialized only into the worker cloud runtime.

LiTS-I:

- Library transport: `LITS-2006-data.dta`
- size: 139,531,180 bytes
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- **PASS**

WVS7:

- Library transport: `WVS Wave 7.sav.zip`
- archive SHA-256: `ce92993a022edbe39823f4a95d3f33522179ce4f388e2de2c1778c4ae6f1059a`
- archive contains canonical `WVS Wave 7.sav`, 185,163,494 bytes, plus a 312-byte macOS metadata sidecar
- extracted SAV SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- **PASS**

No source bytes were committed.

## Why the real current production call graph did not run

The cloud host is CPython 3.13.5 on Linux/x86_64 with pyreadstat and pyarrow absent.

The exact diagnostic runtime requested by the court could not be materialized:

- `uv python install 3.11.3` failed after three retries because the runtime could not resolve the GitHub release host;
- `pip install pyreadstat==1.3.6 pyarrow==25.0.1` failed because the runtime could not resolve PyPI.

Separately, the only recent Library checkout located, `FIABC-QF1-qualification-checkout.zip`, is not raw-materializable in this Project context; Files returned `This Project file does not have an authorized raw-byte materialization path.`

The GitHub connector permitted exact source inspection and branch writes, but it does not provide an executable repository filesystem to the cloud shell. Stale August repo archives were not substituted.

Therefore the underlying current `standardize-wvs`, `produce-lits`, `freeze-t3`, succession, and driver-preflight commands were not invoked. Claiming the desired pre-candidate terminal would be false.

## Historical dependency audit

The audit found the exact non-hermetic loading pattern the commission asked to hostile-test: historical files are deployed individually and executed via `spec_from_file_location`, while their absolute `rawlsing_next.*` imports are not dependency-pinned as a private historical package.

Two distinct cases matter:

1. **Accepted legacy facade** — historical blob `7c509c...`. Its critical legacy key dependency `pre553_empirical_objects.py` is byte-identical at owner and current heads; the relevant missing-state enum declaration is text-identical. Static archaeology therefore found no changed primitive underneath `semantic_hash(canonicalize(...))`.
2. **Banked LiTS projection builder** — historical blob `c51b567...`. Most imported PRE553 files differ from its banked commit. The current successor intentionally relies on that hybrid for current typed projection keys, then explicitly rebinds only the exact authorized q301_2/q301_7 current keys into the pinned legacy owner namespace.

Because runtime import provenance could not be captured in the required executable environment, dependency closure is **not proved**.

## Representation repair static check

The exact current algorithms reproduce the documented split:

- raw decoder float64 keys differ from current Decimal keys;
- transport Decimal `x.0` keys differ from current Decimal integer-exponent rule keys under R5;
- the legacy owner canonicalizes both Decimal forms to one legacy physical key;
- current code head `ea0baa4d...` rebinds only the exact current Decimal rule keys to those legacy keys;
- system-missing is rebound separately;
- coordinate rule rebound accepts system-missing only;
- weights are rejected.

This is a static exact-key audit, **not** a real-source PASS. See `04_TYPED_KEY_JOIN_TRACE.json`.

## Stop boundary

Candidate A/B/C: 0 processes started.

Measured P2X: not run.

P3: not run.

Architecture selection: not run.

## Terminal

`FIABC_CLOUD_SOURCEBACKED_PREFLIGHT_R1__BLOCKED__QUALIFIED_RUNTIME_AND_CURRENT_CHECKOUT_UNAVAILABLE__STOPPED_BEFORE_CANDIDATES`
