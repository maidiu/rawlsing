# PYAT C4C3 — Darwin/x86_64 anchor runtime qualification + C3 55/55 — R1

**Disposition: `PASS_C4C3_DARWIN_ANCHOR_RUNTIME_QUALIFIED__C3_55_OF_55__FANIN_READY`**

Terminal: `C4C3_DARWIN_ANCHOR_RUNTIME_RETURNED__HQ_FANIN_REQUIRED`

Branch `agent/opencode-pyat-hq174-c4c3-darwin-anchor-runtime-r1`, commissioned tip `eba2f4249fb7cd315851ff687269bc43ade19ce8`. Tree qualified: `8f7efe690a161902e79358eb31650c238a4c0be8`. No self-adoption.

## Result

| Phase | Result |
|---|---|
| 0 — tree + host | **12/12 pinned blobs EXACT**; Darwin 22.6.0 / x86_64 / CPython 3.11.3 all met |
| 1 — isolated environment | **Historical C3 seed reproduced byte-for-byte**, zero transitive differences |
| 2 — C4 call path | `P2X_DARWIN_GATES_NOT_ON_C4_PATH` **independently confirmed** |
| 3 — reader option freeze | 5 explicit + **11 inherited defaults frozen**; no unidentified default governs C4 |
| 4 — synthetic probes | **21/21 completed**, 18 PASS, 2 OBSERVED, **0 errors, 0 failures** |
| 5 — authoritative C3 court | **`55 passed / 0 failed / 0 errors / 0 skipped`** — twice |
| 6 — resource/identity law | Frozen; execution-surface identifier issued |
| 7 — C1 preservation | 5/5 blobs exact; **0 anchor-runtime incompatibilities** |

## The three findings that matter most

**1. The historical C3 freeze hash is not just comparable — it is reproducible, and I now know its normalisation.** I reconstructed the 13-line seed from the commission, tested four normalisation variants, and matched `9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb` exactly: it is the SHA-256 of the LF-terminated, alphabetically-sorted `Name==Version` freeze **including pip and setuptools**. My fresh venv's 13-package subset hashes to the same value with **0 differences**.

So commission line 127's conditional ("if current resolution requires transitive-version differences, record and prove them harmless") was satisfied *trivially* — there was nothing to prove away. The only additions are `pyreadstat 1.3.6`, `pyarrow 25.0.1`, and `narwhals 2.26.0` (pulled by pyarrow). narwhals is off the C4 closure and absent from the court, so it cannot affect the result. A bonus datum: the freshly installed `_readstat_parser`, `_readstat_writer` and `_parquet` Darwin extensions are **byte-identical** to those in a separately provisioned local environment — the decoder-relevant wheel content is reproducible, not merely version-equal.

**2. O1-C04 now has its answer, recorded rather than inferred.** Probe D02-5 read a synthetic SAV DATE variable through the real reader on this anchor. It arrives as **built-in `datetime.date`** (pandas dtype `object`, *not* a `datetime64` column), and the accepted decoder converts it to `R5OpaqueValue('python.datetime.date@1', payload b'\x06.\n\x0e')` — i.e. 1582-10-14, confirming the SPSS epoch. That is the "actual current subclass" Omega-1 demanded, obtained without inferring anything from the retained `1582-10-13` rendering.

The decisive control here is `dates_as_pandas_datetime`, which **defaults to `False`** and which the repository never passes. Had it been `True`, the carrier would have been a pandas datetime64 column and the `date@1` identity would not have held. It is now frozen.

**3. A new fact for O1-C06: the physical-metadata digest is reader-lane bound, not source-only.** Two decodes of the *same* synthetic DTA produce **different** digests:

```
encoding="latin1" lane → 5f58388491b1e41424b177f966c5d61032f5f88f344f0403cfad203ca19f315a
encoding=None  lane    → f9148f36ba2b58a8a6386c4a7f8fff796dfb6a0a4a4fc7418043ae8849f727e6
```

`file_metadata` was **identical** across lanes (0 differing keys). The difference is entirely `reader_configuration` — `encoding` and `authority_status` sit inside the digest payload. Decode *is* repeatable within a lane (two runs, bit-identical). **Therefore a frozen digest is valid only for (source, reader lane), and the source warrant must bind both.**

## What I did not dress up

**RES-1 — the Stata extended-missing branch is still unprobed.** pyreadstat 1.3.6's `write_dta(missing_user_values={'x':['a']})` does **not** round-trip: the reader reports empty `missing_user_values` *and* empty `missing_ranges`. So the accepted decoder's dual-shape branch (`pre553_physical_decoder.py:315-320`, accepting both bare `a` and dotted `.a`) cannot be exercised by a synthetic round-trip. The repository **independently acknowledges this** — `test_pre553_sr06_decoder_carrier.py:268` skips with *"installed pyreadstat writer/readback does not expose missing_user_values in metadata"*. That branch is exercisable only against the real LiTS source, which I am not authorised to open.

**RES-2 — `pandas.Timestamp` is outside the D02 carrier.** The accepted contract uses exact type identity, and `Timestamp` subclasses `datetime.datetime`, so it is missed and collapses to `str`. Naive and tz-aware Timestamps render *differently*, so tz-awareness changes identity on that lane. This is a property of the accepted decoder as merged — **not repaired here, not this lane's to change.**

**RES-3 —** numpy `datetime64` unit changes D02 arrival typing. Bounded by the `numpy 2.4.6` pin.

## Two things HQ should act on

**C4A's pandas collection-blocker is retired — and it was hiding an authoritative court file.** C4A excluded five files for `ModuleNotFoundError: pandas`, among them `test_pre553_source_backed_c11_facade.py`, which is **one of the six authoritative court files**. With pandas 2.3.3 installed it collects and passes 10/10. All five now collect: **48 passed / 11 failed / 1 skipped**, 0 collection errors.

Of those 11: eight are a banked content-hash mismatch (`8e5842eb…` vs recomputed `5e2a53f0…`), one is a banked projection identity/ordinal mismatch at `fiabc_lm2_r1j_wvs7_representation_authority.py:176`, and two are `ModuleNotFoundError: duckdb`. **None is an anchor-runtime incompatibility.** That is why commission line 242's condition for re-running the 454 was not met, and I did not re-run it. I have not relabelled them — they are HQ's to triage, they are simply no longer hidden behind a collection error.

**No dependency lock exists in the repository.** `01_ENVIRONMENT_LOCK.json` supplies the freeze for this surface and the historical hash is now reproducible, but a durable repo lock is still absent.

## Two corrections I made to my own work

My first probe run reported four failures. Three were my bugs (`write_sav(1.3.6)` has no `missing_user_values` kwarg; `datetime.date` has no `tzinfo`; `PhysicalSourceIncidence` exposes `iter_cells()`, not `.cells`; `physical_metadata_digest` is a property). I fixed and re-ran rather than reporting them as findings.

The fourth was **not my bug and I reported it as a first-class result**: my probe expected an `encoding="latin1"` override to work on a synthetic file and it was **correctly refused** — `_compatibility_config` admits an encoding only for a SHA carrying an exact authority, and a synthetic SHA never will. That is the admission law working. To exercise the compatibility *read* lane I then extended the allowlist **in memory only**, recorded as six disclosed harness injections, reverted after each probe, with the unmodified fail-closed behaviour measured first and kept as its own probe.

## Honest scope

This is a **source-free** runtime qualification. **Zero** survey files were opened, stat'ed, hashed or decoded; nothing under `data/` was opened. The accepted C1 fresh-process bridge limitation, the C2 epistemic-origin residual, and the C5/C7 holds are untouched. No equivalence to any non-Darwin surface is claimed — none was involved.

**0 raw survey reads · 0 C4 live production · 0 measured P2X · 0 tracked production changes · 0 fabricated metrics · no self-adoption.**
