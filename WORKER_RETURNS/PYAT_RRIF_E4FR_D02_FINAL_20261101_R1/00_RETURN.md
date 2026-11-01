# PYAT RRIF-E4FR — FINAL INDEPENDENT REVIEW OF E4F'S CORRECTED D02 SAV/DTA DATETIME RECEIVER — RETURN R1

Status: `APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN__ENGINEERING_PASS__SCIENTIFIC_AND_AUTHORITY_HELD__NESTED_ITEM_BOUNDARY_NONBLOCKING`

One-line result: At exact E4F head `f2c0af3273d612bff0a7bd2407532b52caf4348b`, real pyreadstat-written SAV and DTA `DATETIME` cells reach `PhysicalSourceIncidence.iter_cells` and the pinned historical first R5 seam as `R5OpaqueValue` / `python.datetime.datetime@1` / codec tag `opaque`, never `str`; direct and one-level item-wrapped aware, `NaT`, sub-microsecond, and hostile date-like subclasses refuse with typed `R5CodecError`; opaque date/time versus a numeric missing range raises typed `DecoderError`, not `TypeError`; D01 exact pairs, PR526 O_RDONLY `/dev/fd` custody, SAV finite-float bits, E1's 33, E4F's 12, and the selected 194-pass/1-skip suite reproduce green, and G01's same two hostile failures reproduce on PREMAIN and E4F. A two-or-more-level `.item()` chain containing an aware date still stringifies through the unchanged recursive `_jsonable` fallback; that is outside the bounded one-level D02 promise, is not reachable from the current pyreadstat SAV/DTA cell route, and is recorded as a non-blocking residual hostile-input boundary rather than timezone-aware carrier authority.

## 1. Identity and execution envelope

- Role: independent I3 hostile physical decoder / R5 post-correction reviewer. Not E1/E4F author, original C3 issuer, protected integrator, HQ, or own reviewer. This is an exact correction court, not an adoption or merge authority.
- Reviewer branch: `review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1`.
- Reviewer branch start / PREMAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Live reference check at review time (`git ls-remote origin`):
  - `refs/heads/integration/pre-main-reconciliation-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29`.
  - `refs/heads/agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1` = `f2c0af3273d612bff0a7bd2407532b52caf4348b`.
  - `refs/heads/review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29`.
  - `refs/heads/main` = `25830fe7462bb9e29bc4087e6ae14f3f84cec377`.
- Reviewed candidate: E4F `f2c0af3273d612bff0a7bd2407532b52caf4348b`, parent E1 `ffd03934d0a86c98ed095d973e45587bd5751013`.
- Original E4 hostile return: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`.
- Host: `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Harness/model: OpenCode `1.18.34`, agent `build`, read-only session DB evidence for the live review session `ses_e67ce6138ffe4GaCdkjtL5CYvr`: `modelID=deepseek-v4.1-flash`, `providerID=opencode-go`, `variant=max`, `mode=build`. The proposed OpenCode / DeepSeek V4.1-Flash MAX pair was actually active; no model/provider/account/host/editor/effort switch occurred.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- Execution surface: three fresh, detached, sparse Git worktrees outside the author/E4/PREMAIN worktrees, plus the reviewer return worktree:
  - E4F: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-e4f-f2c0af3273d612bff0a7bd2407532b52caf4348b` (HEAD `f2c0af32…`, clean).
  - E1 replay: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-e1-ffd03934d0a86c98ed095d973e45587bd5751013` (HEAD `ffd03934d…`, clean).
  - PREMAIN baseline: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-premain-8e44ca9c751049d65e6def47600b5c073ee04b29` (HEAD `8e44ca9c7…`, clean).
  - Return branch: `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-return`.
- Sparse set: `rawlsing_next/`, `tests/`, `WORKER_RETURNS/EE-P2R6S/`, `WORKER_RETURNS/FIABC-LM2/`, `WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/`, `WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/`. Fixtures were read from the exact commit's own tree; no foreign-worktree symlink or copy was used. No raw/native survey source, Sorok, PROGRAMMA, R9, actor, or production route was opened or executed.

## 2. Exact reviewed correction

Changed files against E1 (`git diff --name-only ffd03934 f2c0af32`), exactly:

- Production: `rawlsing_next/pre553_physical_decoder.py`, `rawlsing_next/pre553_r5_codec.py`.
- Test: `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py`.
- Return documents: the five files under `WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/`.

No other production or test file changed. Exact identities:

| Path | Git blob | sha256 |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |
| `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` |

The two production files are the only production deltas: `+22/−6` for the decoder, `+71/−13` for the codec. The test is `+314/−0`. The five return documents are documentary only.

D01, PR526, and float-bit blocks were independently compared at E1 and E4F and are byte-identical as source segments:

- `DECLARED_ENCODING_ALLOWLIST` block `051ea39a048d93ebef123429a47df326e4ef69044374ce4919060b41daf44eab` at both cuts.
- `COMPATIBILITY_ALLOWLIST` block `64131d172918dad450517a5b0c34962951aaa2450c6ff5602fd37d1d29062878` at both cuts.
- `_compatibility_config` `6e6aeca563e39b9c4d57e521edb166f57c624dcfdcd5f4f3f9c73562f973bcff` at both cuts.
- `_SourceSnapshot` `7a4d0ea4e7d3428a60893333f58d625a90b6b94d3400d1033544cee42bcdc5e2` and `_acquire_source_snapshot` `1e267242fd39ead8365f711bc67b09a9e6e841d5c84f3f6a86f6f2259c7e5511` at both cuts.
- `_float64_bits` `326b8def532424b709bf7ce21fd32751d14eb03619c677ec6db0231b023f6d1c` and `_bits_float64` `842f27333da07b839cb9fb3eab6450e2fd5fcb52988a564b36c7302bee94c30f` at both cuts.

D01 exact three declared SHA/config pairs are live and exactly the expected three:

```
ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2  BIG5
5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2  WINDOWS-1252
66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec  WINDOWS-1252
```

All three return `{"encoding": <pinned>, "authority_status": "SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY"}`; the declared and compatibility lanes remain disjoint. PR526 source custody remains content-bound `O_RDONLY` `/dev/fd` as inspected in `_SourceSnapshot` / `_acquire_source_snapshot`; SAV finite floats remain Python `float` with exact `float64` bits (observed `1.5 -> 3ff8000000000000`, `-2.25 -> c002000000000000`). No R9 broker, G01 numeric-coercion bridge, native-source grant, aware-carrier authority, or source-use authority was added.

## 3. Mandate results

| Area | Result |
|---|---|
| Real SAV `DATETIME` at `iter_cells` | PASS. Source-free pyreadstat fixture; `R5OpaqueValue`, `python.datetime.datetime@1`, exact civil payload. |
| Real DTA `DATETIME` at `iter_cells` | PASS. Same. |
| Pinned historical first R5 seam | PASS. Exact blob `cef326ebbc40468428378f7fdbe76e4756179f39` executed test-only; `dtm` rows have `t == "opaque"`, `type_id == "python.datetime.datetime@1"`, never `"str"`. |
| Naive `Timestamp` / other naive subclasses | PASS. Canonicalized by exact built-in civil fields; fold and microseconds preserved (`2008-04-05 06:07:08.901234`, fold 1). |
| Aware `Timestamp` / plain `datetime` / `time` subclasses, direct and one-level wrapper | PASS. Explicit `R5CodecError` carrier-authority refusal; no string. |
| `pandas.NaT`, sub-microsecond `Timestamp`, hostile `tzinfo`/civil-field subclasses | PASS. Typed `R5CodecError`; no string fallback on the direct/one-level route. |
| Opaque date/time carrier versus numeric missing range | PASS. Typed `DecoderError` naming `R5OpaqueValue`, not `TypeError`. |
| Recursive item chain ≥2 levels containing an aware date | NON-BLOCKING BOUNDARY. Still stringifies through unchanged recursive `_jsonable`; outside the explicitly bounded one-level D02 promise and not reachable from the real pyreadstat cell path. See §5. |
| E1 original 33 tests | PASS. 33 passed, exit 0. |
| E4F new 12 tests | PASS. 12 passed, exit 0. |
| Selected PR526/SAV/C11/EE-P2X suite | PASS. 194 passed, 1 skipped, exit 0; the skip is the known pyreadstat writer limitation. |
| G01 two hostile failures | UNCHANGED/HELD. PREMAIN full pair `2 failed, 7 passed`; E4F full pair `2 failed, 7 passed`; same node ids and assertion values. |
| D01 exact pairs and custody | PASS/UNCHANGED. Three pairs exact; custody and float blocks byte-identical; selected custody/float tests green. |
| Wrong-source tamper | PASS. Post-acquisition tamper does not change the content-bound snapshot or cells; pre-decode tamper refuses. |
| Reviewer branch discipline | PASS. Only the four documentary artifacts are added; no production patch. |

## 4. Test receipts

All runs were on the clean detached E4F worktree unless stated. Exact commands and observed exits are in `REPRODUCIBLE_RECEIVER_AND_HOSTILE_NEGATIVES.md`.

- E4F new D02 test: `12 passed in 0.79s`, exit `0`.
- E1 original 33: `33 passed in 0.86s`, exit `0`.
- Selected PR526/SAV/C11/EE-P2X: `194 passed, 1 skipped in 144.12s`, exit `0`.
- G01 PREMAIN full pair: `2 failed, 7 passed in 278.00s`, exit `1`; failures:
  - `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`: `47f141e43fb2…` vs `b9b720335f37…`.
  - `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`: `StopIteration`.
- G01 E4F full pair: `2 failed, 7 passed in 278.76s`, exit `1`; the same two node ids and assertion values.
- E1 detached RED replay (same source-free real SAV/DTA fixtures): both `dtm` cells `str '2008-04-05 06:07:08'`; aware `dt`, `Timestamp`, one-level wrapper, and aware `time` all `str`; `NaT`/sub-microsecond/hostile fields `str`; opaque-range classification `TypeError`.
- E4F corrected replay: both real formats `R5OpaqueValue python.datetime.datetime@1 opaque`; direct/one-level aware `R5CodecError`; `NaT`/sub-microsecond/hostile fields `R5CodecError`; opaque-range `DecoderError`; float bits exact.

## 5. Nested item-chain boundary (hostile decision)

The mandate's critical question is answered directly:

- A two-level `_ItemWrapper(_ItemWrapper(aware_datetime))` passed to `decoder._physical_value` returns the string `"2008-04-05 06:07:08+00:00"`.
- A two-level wrapper around an aware `pandas.Timestamp` does the same.
- A two-level wrapper around a hostile civil-field subclass returns its string.
- The path is `_physical_value` → `_jsonable` → recursive `_jsonable(value.item())` → `_jsonable(aware datetime)` → `str(value)`.
- The E4F test deliberately codifies only the naive two-level fallback (`_ChainWrapper(_ChainWrapper(dt.date(...)))` → `"2008-04-05"`); it does not test an aware two-level wrapper.

Decision at this exact scope: **not a true fail-closed blocker** for the accepted E4F D02 correction.

- It is not reachable from the current source/consumer route: `iter_batches` obtains values from pyreadstat frames via `frame.itertuples(index=False, name=None)`; real SAV/DTA `DATETIME` arrives as a direct pandas `Timestamp` (or direct built-in/`datetime.date` for date variables), and real numeric scalars unwrap in one level. No current decoder or seam consumer constructs a two-or-more-level custom `.item()` wrapper. The real cells and pinned seam are opaque, as re-run here.
- It is outside the accepted D02 promise: the defect E4 found was the direct real `Timestamp` and the direct/one-level aware subclass/wrapper. E4F explicitly disclaims recursive item chasing in `_physical_value` and `FANIN_SCOPE.md`, preserving the E1 non-carrier fallback.
- It is a disclosed residual hostile-input limitation, not an authority to stringify aware values and not an installed-current vulnerability. It must not be cited as timezone-aware carrier support.
- No new representation is invented. A future hardening (for example, rejecting any date-like value reached through recursive item normalization or capping item unwrapping) would be a new bounded change with its own tests and review; it is not required for this exact fan-in and does not need a new historical court.

An additional non-scope observation, recorded for honesty: `numpy.datetime64` is not a subclass of the built-in date/time types. For most units its one-level `.item()` returns a built-in date/datetime and E4F carries it; for `datetime64[ns]` it returns an integer (observed `1207375628123456789`) and for `datetime64('NaT')` it returns `None`. Those are not produced by the current pyreadstat SAV/DTA `DATETIME` cell route (observed direct `Timestamp`), are outside the accepted `pandas.Timestamp`/subclass D02 scope, and do not change this verdict. They are noted so no one extrapolates the one-level promise to arbitrary numpy scalars.

## 6. Test-only pinned seam honesty

- At E4F `f2c0af32`, `rawlsing_next/pre553_r5_seam.py` is not in the tree. Independently: `import rawlsing_next.pre553_r5_seam` raises `ModuleNotFoundError: rawlsing_next.pre553_r5_seam`; the test's `_pinned_seam()` therefore falls through to the pinned historical blob path.
- The test loads `cef326ebbc40468428378f7fdbe76e4756179f39` (seam, sha256 `626f74200a11dd8f749bead1ebd904eae22b65246636395a16df60d33d2b052f`) and `62ce608829c3d9c2fb7c999aefe40188637edf80` (model, sha256 `cdb8a2581aeed7f24acd668f3b93ca23244f64820266e5d282fb65915c17ac3a`) from the local Git object database, verifies Git blob and SHA-256 identity, and executes them in-memory. The loaded module has no `__file__`; it is test-only.
- This is honestly described in E4F's `00_RETURN.md`, `REAL_SAV_DTA_AND_SUBCLASS_FAULT_TESTS.md`, and `FANIN_SCOPE.md`. It is a historical/test-pinned first-consumer execution, not a claim that the current production package installs `pre553_r5_seam.py`. It adds no production file and no network/survey read. If a future tree adds a production seam, the test's first-choice import would silently prefer it over the pinned blob; that is a future test-maintenance caveat, not a current false claim, because the seam is absent at this cut and the pinned blob was actually executed.
- The return documents and test contain no unreviewed native/private survey data and no unrelated code. The test uses only synthetic source-free pyreadstat files, temporary directories, local Git objects, and the reviewed production modules. No raw source bytes or survey files are embedded.

## 7. Grades

- ENGINEERING: `PASS__D01_D02_SOURCEFREE_FANIN_ACCEPTED_AT_EXACT_BOUNDED_SCOPE__NESTED_ITEM_BOUNDARY_DOCUMENTED_NONBLOCKING`. The real SAV/DTA `DATETIME` receiver, direct and one-level aware/NaT/lossy refusals, typed opaque-range refusal, D01/pairs, PR526 custody, SAV float bits, E1 33, E4F 12, selected 194/1, and G01 severance all reproduce at the exact corrected SHA. No production patch is proposed by this reviewer.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. No raw source, encoding text semantics, survey meaning, estimand, response state, G01 numerical representation, or result is issued. The date/time carrier is physical representation only.
- AUTHORITY: `HELD__NO_SOURCE_RIGHTS_NO_AWARE_CARRIER_AUTHORITY_NO_MERGE_ADOPTION`. This review does not grant source-use/license/rights, timezone-aware carrier authority, G01 authority, issuer/use, protected PRE-MAIN merge, or adoption. Aware values remain refused on the accepted route.

## 8. Holds and NOT_RUN

- HOLD: Pyat HQ adjudication of this exact returned review SHA. This reviewer does not self-adopt, self-merge, or implement.
- HOLD: scientific/source meaning, source rights, issuer/use, G01, R9/Sorok/native, actor, PROGRAMMA, and protected PRE-MAIN merge.
- HOLD: timezone-aware carrier authority. Aware direct/one-level values refuse; no aware representation was invented.
- NOT_RUN: actual raw survey-source decode under any declared encoding. All fixtures are synthetic source-free pyreadstat files.
- NOT_RUN: full repository test suite. Only the mandated 12, 33, selected 194/1, G01 pairs, and bounded hostile probes were executed.
- NOT_RUN: G01 repair or integration. The two known failures remain baseline; they are not claimed as repaired.
- NOT_RUN: any production patch, merge, PR, force push, or worktree mutation of E1/E4/E4F/F0/PREMAIN.

## 9. Return discipline

Only these four documentary artifacts are added on the reviewer branch:

- `WORKER_RETURNS/PYAT_RRIF_E4FR_D02_FINAL_20261101_R1/00_RETURN.md`
- `WORKER_RETURNS/PYAT_RRIF_E4FR_D02_FINAL_20261101_R1/EXACT_REVIEWED_HUNKS_AND_BLOBS.md`
- `WORKER_RETURNS/PYAT_RRIF_E4FR_D02_FINAL_20261101_R1/REPRODUCIBLE_RECEIVER_AND_HOSTILE_NEGATIVES.md`
- `WORKER_RETURNS/PYAT_RRIF_E4FR_D02_FINAL_20261101_R1/FINAL_ALLOWLIST_OR_MINIMAL_BLOCK.md`

No production patch is on the reviewer branch. The exact final 40-hex review commit is read back from `origin` with `git ls-remote` after push and reported in the reviewer terminal response; it is not embedded here because embedding it would change the commit it identifies.

Terminal: `RRIF_E4FR_D02__APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN__NESTED_ITEM_BOUNDARY_NONBLOCKING__SCIENCE_AND_AUTHORITY_HELD`
