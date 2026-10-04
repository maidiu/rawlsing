# HQ204 — accepted R9 runtime surgical fan-in — R1

**Disposition: `ACCEPTED_R9_DEPENDENCY_CLOSURE_INCOMPLETE`**
**Terminal: `HQ204_R9_ACCEPTED_RUNTIME_FANIN_RETURNED__HQ_REVIEW_REQUIRED`**

The accepted source-free R9 runtime **was** placed onto the current-control lineage,
byte-for-byte, with no collision and no invented semantics. The commission's R7
six-file gate, however, is **structurally unreachable** on this lineage, so the
candidate is not declared ready. A second, independent material finding is also
reported. Nothing here is self-adopted.

## Identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq204-r9-integration-r1` |
| Commissioned startup SHA | `26e92e6d1fac4b5bc9bfa755ced6e7038e4f959d` (verified exact) |
| Implementation base | `ff4f06954824a3a5699bc5c1c9bd68cb3c5b4146` |
| Blob source of truth | `0deb64784829661780ee3957f8070ccc2c241722` |
| Checkout mode | `SPARSE_REQUIRED` |

### Store-law deviation (disclosed)

`$HOME/Desktop/Rawlsing` is **not a git repository** — it has no `.git`. Per the
store law's own verification step, that path failed and no second copy was cloned.
The existing `maidiu/rawlsing` clone that owns the commissioned
`$HOME/Desktop/Rawlsing_Worktrees` root was used instead:

- store: `/Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository`
- remote: `https://github.com/maidiu/rawlsing.git` (blob:none partial clone)
- worktree: `$HOME/Desktop/Rawlsing_Worktrees/pyat-hq204-r9-fanin-r1`
- fetch: the single exact commissioned ref, no tags

## What was placed

Six adds and two forward-evolution overwrites. Every placed blob is byte-identical
to the accepted commits, verified after placement.

| Path | Control | Accepted blob | Relation |
|---|---|---|---|
| `pre553_source_access_broker.py` | ABSENT | `090d978b` | ADD |
| `pre553_source_session.py` | ABSENT | `ac1390b8` | ADD |
| `pre553_execution_binding.py` | ABSENT | `0e11af22` | ADD |
| `tests/test_pre553_execution_binding_court.py` | ABSENT | `67492110` | ADD |
| `tests/test_pre553_source_access_broker_court.py` | ABSENT | `c1bc8273` | ADD |
| `tests/test_pre553_source_session_court.py` | ABSENT | `8b45e3f9` | ADD |
| `pre553_physical_decoder.py` | `d2a074a4` | `b406d45f` | OVERWRITE |
| `pre553_r5_codec.py` | `72f8f3c0` | `6000a170` | OVERWRITE |

The final independent acceptance agrees with the hardened candidate on all six R9
blobs, so the accepted blob set is unambiguous. The broker is the later hardened
`090d978b`, not the earlier HQ199 `67fac8a3`; the session blob is unchanged from the
accepted GovernedSourceSession owner.

### No collision

The accepted lineage is **not** merged into control (merge-base `87029d34`), so
every placement needed adjudication. The two overwrites are **forward evolutions,
not nonancestor forks**:

- decoder: control blob introduced by `11d86982b`, which **is** an ancestor of the
  accepted introducer `90ccbd54`
- r5_codec: control blob introduced by `43c5c937e`, which **is** an ancestor of the
  accepted introducer `30686b185`

Both control versions sit on the shared chain, so no
`ACCEPTED_R9_FANIN_COLLISION` stop was triggered and no semantic resolution was
improvised. The decoder overwrite is unavoidable: the control decoder has no
`decode_in_session` symbol, which the accepted source-session court imports
directly, and it predates brokering entirely. `pre553_r5_codec` is required
transitively by the accepted decoder. The closure terminates there (stdlib only).

## Results

The three commissioned courts reproduce the accepted HQ201 counts **exactly**:

| Court | Result |
|---|---|
| hardened execution-binding | **34 passed** |
| source-session | **15 passed** |
| broker | **20 passed** |
| aggregate | **69/69** |
| import/compile smoke | PASS |

No failure was retried away.

## Why this is not `READY`

### 1. The R7 six-file 55-test gate is unreachable (blocking)

The authoritative court requires **55 collected, then 55/55, then 55/55**. On this
lineage only 25 of those tests exist:

| Court file | Expected | Present |
|---|---|---|
| `test_closed35_g01_sav_numeric_representation_authority.py` | 9 | **ABSENT** |
| `test_closed35_d01_declared_encoding_admission.py` | 8 | **ABSENT** |
| `test_closed35_d02_opaque_datetime_carrier.py` | 13 | **ABSENT** |
| `test_fiabc_lm2_r1j_sav_representation_authority.py` | 9 | 9 ✅ |
| `test_r35_i01_physical_metadata.py` | 6 | 6 ✅ |
| `test_pre553_source_backed_c11_facade.py` | 10 | 10 ✅ |

The three missing files came from the separate **accepted C3 source-free repair**
lineage (`fe9ec0361`, `105246b33`, `5fbf9cc56` — siblings of `1f9990fec` and
`30686b185`). None of those commits is an ancestor of control `ff4f0695`, and the
files are equally absent from the commissioned startup SHA `26e92e6`. They are C3/C4
`closed35` court content, **not** R9 runtime and **not** R9 courts.

They were deliberately **not** imported: that is precisely the "unrelated historical
side-branch content" the commission forbids, and choosing to pull them in would be
improvising a resolution. The gap is reported instead.

The reachable 25 pass **twice** (45.84s, 46.18s), deterministically, with per-file
counts matching the accepted expectations. This is a real positive: all three
reachable files import the overwritten decoder, so **the decoder and r5_codec
forward-evolution regresses nothing in the reachable R7 court.**

**HQ decision required:** authorise the three `closed35` files as an explicitly
scoped additional dependency, or re-specify the R7 gate against the court files this
lineage actually carries.

### 2. The fan-in is not purely additive (material new counterexample)

An identical 12-file control set was run twice on one interpreter — at pure control
base and on the candidate:

| Tree | failed | passed | skipped | total |
|---|---|---|---|---|
| control `ff4f0695` | 14 | 94 | 1 | 109 |
| fan-in candidate | 16 | 92 | 1 | 109 |

Exactly **2** tests moved from passed to failed; the 14 pre-existing failures are
unchanged. Both are in `test_pre553_sr06_decoder_carrier.py`:

1. `test_expected_source_identity_is_hashed_once_before_reader_decode` — the control
   court requires the identity gate to hash via `decoder._sha` once; the accepted
   decoder reaches the same fail-closed `DecoderError` via the broker-governed
   `_governed_source_sha` instead, so `hash_calls == []`.
2. `test_normal_decode_uses_chunk_path_and_compatibility_uses_full_read` — the
   control court requires the chunked reader route; the accepted decoder's
   restructured declaration-aware route no longer issues that call, so
   `chunk_calls == []`.

Neither is in the commissioned R7 court nor in the three R9 courts. Neither was
suppressed, retried, or worked around.

**HQ decision required:** adjudicate whether the accepted decoder supersedes these
control-lineage assertions (retiring the two control tests by that adjudication), or
whether the decoder needs a compatibility repair. This worker did not choose.

### 3. Environment insufficiency (disclosed, not silent)

The governed R7 interpreter
(`Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv`) and the C4C3 base
interpreter (`LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none`) **no
longer exist on this machine**.

The ambient reader `pyreadstat 1.3.2` is rejected closed by the accepted broker's
`1.3.6` pin — 23 of 34 binding-court tests failed on that ground alone. The pin was
**not** relaxed and no accepted code was bent to accommodate it.

Qualification therefore ran on a **disclosed reconstruction**
(`/var/folders/.../T/opencode/hq204-r9-env`) whose 13-package freeze matches the
governed `01_ENVIRONMENT_LOCK.json` **exactly**, on CPython **3.11.3**, matching the
governed base version, with `PYTHONHASHSEED=0`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-p no:cacheprovider`. This is strong evidence,
**not** a governed-environment certification. `duckdb` is absent from the governed
freeze too, which is why two direct-duckdb tests fail in both arms.

## Holds preserved

Route-pass applicability; attempts / retries / completions separation; pre-operation
retry ceiling; completion-after-postconditions; pyreadstat dependency injection;
seven warrant plan shapes; no source-specific production policy; source-dependent
byte budgets still unbound.

No raw source access, no locator discovery, no warrant issuance, no invented numeric
reader-byte ceilings, no live C4, no C7, no actor/person work, **no self-adoption**.

## Terminal

`HQ204_R9_ACCEPTED_RUNTIME_FANIN_RETURNED__HQ_REVIEW_REQUIRED`
