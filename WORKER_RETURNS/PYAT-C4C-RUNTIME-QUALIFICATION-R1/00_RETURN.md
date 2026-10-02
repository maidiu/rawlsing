# PYAT C4C — Non-Mac execution runtime qualification — R1

**Disposition: `C4_RUNTIME_EXECUTION_SURFACE_QUALIFICATION_REQUIRED`**

Terminal: `C4C_RUNTIME_QUALIFICATION_RETURNED__HQ_FANIN_REQUIRED`

Branch `agent/opencode-pyat-hq170-c4c-runtime-qualification-r1` at commissioned tip `b2ff3b0d89d32c41430cf50c3c785d64d8fd5f55` (base `149c3d2636160d8de9b5a8be0c8b87195158077d`, governing Omega-1 `01762d7379be4e423dad3e21bcdcee47c536902d`). No self-adoption.

## The finding

**There is no non-Mac execution environment to qualify, and the current tree would refuse one if it existed.**

Three facts, each independently sufficient:

1. **Zero non-Mac surfaces are reachable.** `docker`, `podman`, `colima`, `lima`, `limactl`, `nerdctl`, `orb` are all absent; `~/.colima`, `~/.lima` and the Docker state directory are absent; no Linux kernel is reachable. The GitHub/browser surface was already recorded — in the accepted C3 review receipt — as having no lawful general-purpose runtime.

2. **The only decoder-capable surface is the user's Mac, which is also the anchor.** macOS 13.7.8 / Darwin 22.6.0 / **x86_64**, CPython 3.11.3, pyreadstat 1.3.6, pyarrow 25.0.1 — an exact match for the retained physical reproducibility anchor. Commission item 6 forbids using the user's Mac as a fallback, and the surface is in any case a machine-local, git-**untracked** path, so it could never serve as a reproducible frozen surface identifier. It is the anchor, not an alternative to it.

3. **The repository's own hard gate rejects every non-Mac surface.** Probe **P05** called the real gate at `rawlsing_next/ee_p2x_darwin_court_driver.py:46-49` with synthetic hosts:

   | synthetic host | outcome |
   |---|---|
   | Darwin / x86_64 | **ACCEPTED** |
   | Linux / x86_64 | `REJECTED(RuntimeGateError)` |
   | Darwin / arm64 | `REJECTED(RuntimeGateError)` |
   | Linux / aarch64 | `REJECTED(RuntimeGateError)` |

   Five tests pin that refusal (`test_ee_p2x_darwin_court_driver.py:191-208`, `test_ee_p2x_local_court_receipts.py:22-28`), and a second independent gate — `FROZEN_PYREADSTAT_VERSION` at `ee_p2x_darwin_stage_backend.py:61,896-901` — sits on the WVS7 `.sav` read path.

This is why the disposition is not "insufficient evidence." The Darwin/x86_64 dependency is not merely historical. **It is a live equality check in the code C4 would execute.** Admitting a non-Mac surface is an HQ contract decision, not a worker finding.

## What the 14 source-free probes did establish

They are recorded in full in `03_SOURCE_FREE_COMPATIBILITY_PROBES.json`; 14 ran, 0 errored.

**Proved portable — may lawfully be inherited by any competent surface:**
- **P01** — the G01 float64 bit-token layer is host-endianness independent. All nine authorised tokens reproduced exactly (`3ff0000000000000`-style big-endian) and round-tripped, on a little-endian host. `struct.pack(">d")` removes the dependence.
- **P02** — `semantic_hash` is stable under reserialisation and structurally refuses binary float.
- **P04** — R5 exact-type semantics hold: `type(x) is int` correctly rejects `np.int64` and `bool`.

**Proved not inheritable:**
- **P14 (critical)** — pyreadstat 1.3.6 leaves **ten** reader options that materially govern C4 read behaviour **unpinned**, including `formats_as_category` which **defaults to `True`**, and the two date-carrier controls `dates_as_pandas_datetime` and `disable_datetime_conversion` which default to `False`. The repository passes only `metadataonly`, `apply_value_formats`, `user_missing`, `encoding`. **C4 read behaviour currently follows whatever pyreadstat build happens to be installed.** O1-C05's "exact reader options" is not currently met by the repository.
- **P03** — with no opaque D02 carrier in this tree, every date/time collapses to a *string*. Measured: `datetime(2008,4,5,6,7,8)` → `'2008-04-05 06:07:08'` (space, not ISO `T`); the tz-aware form → `'...08+00:00'`, a **different string and therefore a different identity**; and `np.datetime64` unit `'D'` → `'2008-04-05'` versus unit `'s'` → `'2008-04-05 06:07:08'`. **The numpy datetime64 unit changes the D02 rendering, and numpy is pinned by no gate.**
- **P06** — `reader_version` enters the **physical-metadata SHA-256 digest**. Any pyreadstat version change invalidates every frozen digest in the repository. Widest blast radius here.
- **P07** — `ru_maxrss` is **bytes on Darwin, kibibytes on Linux** — a 1024× difference. O1-C07 budgets do not port, and the retained R8B Darwin law cannot be inherited by name.

**A probe I corrected rather than banked:** P10's first run reported `changed=false` because my input had already been NFC-normalised. Re-run with an explicitly decomposed `U+0065 U+0301`, it returns `[0x65,0x301] → [0xe9]`, `changed=true`. The corrected reading is what the packet carries; the superseded one is relied on nowhere.

## The blocker I did not work around

**P13** measured that pandas and pytest are **absent**, and that `pyreadstat.write_sav/write_dta` annotate their first parameter as a pandas `DataFrame` (`TypeError: Unsupported dataframe type, got: <class 'list'>`). So **no synthetic SAV/DTA reader fixture can be built here at all.**

That means the reader-behaviour half of the probe layer — D01 declared-encoding resolution under `encoding=None`, D02 arrival typing from a real reader, the DTA extended-missing token shape — **could not be probed**, only characterised from code and reader-API signatures. The strongest available evidence is signature-level, not behavioural.

I did not install pandas or pytest to fix this. Doing so would mutate the substrate under qualification and silently change the very runtime facts being frozen, against commission lines 20-21. The absence is recorded as a blocker. **The probe layer is therefore incomplete, and this return does not pretend otherwise.**

## Three things HQ should know that the packet records but the summary cannot

**The tree I was asked to qualify is not the tree C4 will run.** Omega-1 O1-C01 already said this; I confirmed it at code-identity level. `closed35_g01_sav_numeric_representation_authority.py` and the three `test_closed35_*` files are **absent**; `DECLARED_ENCODING_ALLOWLIST`, `normalize_decoder_physical_value`, `opaque_decoder_value` are **not found**. The blobs here are `pre553_physical_decoder.py d2a074a4…` and `pre553_r5_codec.py 72f8f3c0…` — the pre-successor values. So the two most runtime-sensitive C4 operations, D01 and D02, have **no contract in the tree under qualification**. That is C4A's obligation to fix; I record it as a blocking dependency of O1-C05.

**O1-C05's pinned dependency inventory cannot be derived from this repository — it must be authored.** There is no `requirements*.txt`, `constraints*.txt`, `uv.lock`, `poetry.lock`, `Pipfile`, `*.lock`, `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `tox.ini` or `conftest.py`. All six CI workflows install `pytest` and `pandas` **unpinned** on `ubuntu-latest` with `python-version: "3.11"`. And the accepted material self-conflicts: numpy is recorded as **both** 2.3.1 and 2.3.2; pandas as **both** 2.3.1 (checkpoint) and 2.3.3 (C3 receipt). I did not choose between them.

**`duckdb` is a hard requirement with no accepted version anywhere.** `run_as2b_lits1_mechanical_certification.py` imports it at module scope and is `exec_module`'d onto the live LiTS path. It is absent here and no anchor records a version for it.

## The anchors, kept distinct

As O1-C05 requires, the two runtime anchors are preserved as separate grades and **neither is used to bridge the other**:

- **Retained physical anchor** — CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1 / Darwin / x86_64. Physical, inherited from actual survey decodes.
- **Accepted C3 source-free anchor** — CPython 3.11.3 / pytest 9.1.1 / pandas 2.3.3, `pip_freeze_sha256 9cde8e5a…`, raw survey reads **0**. It records **no OS, no architecture, and no reader-library version** — correctly, because that court never read a survey file. It therefore cannot serve as reader-side physical evidence, and I did not try to make it.

## Smallest exact missing qualification / wake condition

**Wake (any one of these is HQ's call alone; no worker may waive them):**
- **WC-1** — provision/designate one concrete, reachable, reproducible **non-Mac** surface: exact OS, exact architecture, durable locator, not the user's Mac.
- **WC-2** — HQ rules on `EXPECTED_RUNTIME` (`ee_p2x_darwin_court_driver.py:46-49`), which P05 measured to refuse every non-Mac and non-x86_64 host. Either amend the gate for the chosen surface, or bind C4 to Darwin/x86_64 and abandon the non-Mac route.
- **WC-3** — HQ rules on `FROZEN_PYREADSTAT_VERSION` (`ee_p2x_darwin_stage_backend.py:61,896-901`).

**Then, to qualify:** QQ-1 exact 3.11.3/1.3.6/25.0.1 with a frozen hash inventory · QQ-2 an **authored** lock file · QQ-3 HQ resolves the numpy/pandas version conflict · QQ-4 the ten unpinned reader options explicitly frozen · QQ-5 the surface-native `ru_maxrss` unit law and its own budget · QQ-6 the reader-behaviour probes re-run **on the chosen surface** · QQ-7 the matrix and probes re-run against the **combined C1+C3 tree** · QQ-8 the **actual** current date/time subclass recorded for O1-C04 (never inferred from the retained rendering `1582-10-13`) · QQ-9 confirmation that the chosen pyreadstat version does not invalidate any retained physical-metadata digest.

Full listing in `04_QUALIFIED_EXECUTION_ENVIRONMENT.json` and `06_FINAL_DISPOSITION.json`.

## What I did not do

Did not use the user's Mac as a fallback. Did not open, hash, read metadata from, or decode any survey file — **0 raw survey reads**. Did not install or upgrade anything. Did not merge C3 or own the combined tree. Did not self-adopt. Did not waive the Darwin/x86_64 anchor. Did not fabricate a single metric: **no test pass/fail/skip counts are claimed, because pytest is absent and none were run.** Did not reinterpret the PYAT-C1-01-R7 failure on CPython 3.12.14 — it is cited as recorded, cause not established either way.

I also found and reported a local environment defect, deliberately not repaired: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11` is a **zero-byte file** that exits 0 emitting nothing; only the `python3.11-intel64` alternate runs. Worth knowing, because it means "CPython 3.11.3 is on PATH" is not a sufficient identity check for any future surface.

## One judgement, stated plainly

The honest answer to the mission is that **no non-Mac environment is competent for this claim at any grade, because none was available to test and the code currently refuses all of them.** I could have produced a packet claiming partial qualification of the Mac surface — the versions happen to match the anchor exactly, and P01 does prove some layers are portable. That would have looked like progress. It would have been the anchor re-observed, on a forbidden host, against a tree missing the two contracts that matter most, with the reader layer never probed. Returning the blocker is the more useful result.
