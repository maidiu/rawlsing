# R56-R04BYTEV — independent native review return

Verdict: **REVISE** — one minimal reproducible engineering defect at the claimed
consumed-byte custody boundary. The old source identity CAN be attached to
native C11/I03 facts built from replacement bytes through the
content-verification-to-reader window.

- Engineering: REVISE (defect reproduced with actual generated SAV and DTA,
  actual C11 `RespondentEvent`/I03 `EmpiricalFact` values, on the exact
  candidate).
- Science: no acceptance and no new science claim. Synthetic generated data
  only; no original source, original35 or N11 measurement.
- Authority: no production promotion, no R03/R04.joined, no joined issued
  workload, no partial Batch/revocation/dedup lifecycle, no protected R09 CI.
  Local byte custody only, and locally that boundary is not yet enforced in
  the window below.

## Session, startup and candidate verification

- Reviewer role: fresh independent OpenCode session for `R56-R04BYTEV`; no
  author context and no authoring writes in this session. Session ID not
  exposed by the harness (`UNKNOWN_NOT_EXPOSED`); independence basis and
  allowlist recorded in `00_STARTUP_SESSION_RECORD.md`.
- Model `opencode-go/deepseek-v4.1-flash`; effort `UNKNOWN_NOT_EXPOSED` (MAX
  not claimed); harness OpenCode; host `MacBook-Pro.lan`, macOS 13.2.1;
  Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1.
- Candidate `c1b0abec563a91940ae2f505b53a4c7e16f8685a`; parent/startup
  `6d95a78bf6b7bcf70022e303a151255e65edc38a`; startup is an ancestor; remote
  author branch equals the candidate. Dispatch custody matches (9 files,
  scope verified, no production edit permitted).
- Reviewer branch `agent/rabochii-pyat-r56-r04bytev-independent-custody-review-r1`
  did not exist remotely or as a worktree before creation; author worktree was
  not reset or reused. Fresh sparse worktree created from the candidate.
- Governing files read from Git objects at the commissioned refs (director
  `485f31e52`, R57 `953eb07a...`, direction `6cdde972...`, shared contract
  `eb28fdcc...`, frozen R00P R2 at `6d95a78...`).
- Author manifest hashes independently verified against actual Git objects:
  decoder blob `b04c5e6397...`/sha256 `d51f23e3...`, test blob `c5e1091a...`/
  sha256 `d398ec88...`, proof blob `e9e8121b...`/sha256 `1019fd93...`, return
  files all match.

## Author claims independently reproduced

- Author test module at candidate state: **16 passed** (run before any
  independent addition).
- Author core command: **80 passed, 1 skipped** — reproduced exactly.
- Skipped capability identified honestly: `test_pre553_sr06_decoder_carrier.py:268`
  `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation`
  skips because the installed pyreadstat writer/readback does not expose
  `missing_user_values` in metadata; the DTA extended-missing path of the
  decoder is therefore not exercisable in this environment. The test file is
  unchanged by the candidate.
- Author proof witness independently re-run through
  `CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness`: both the author
  claim and an added independent claim show baseline PASS and exact lazy-reader
  mutation `TARGET_ASSERTION_FAILED`; decoder restored byte-exact
  (`d51f23e3...`).
- Positive mechanism verified independently (my own test, actual facts):
  original-path replacement after acquisition is not consumed; facts stay
  identical; snapshot/source digest equality holds; changed same-path bytes
  acquired anew get a new identity; altered/closed snapshots refuse; fresh
  process old-digest cold replay refuses changed bytes and restores the exact
  same fact payload.

## Defect (minimal reproducible, engineering)

**Verification is by open file descriptor, consumption is by mutable path.**
`_SourceSnapshot.verify()` rehashes the snapshot through `os.pread(self.fd, ...)`
(decoder lines 210–214), but every reader call passes
`self._source_snapshot.reader_path` — a plain path string — to pyreadstat:
metadataonly read (lines 611–613), compatibility full read (lines 615–619),
and lazy `read_file_in_chunks` (lines 175–178). Between the `verify()` call and
the reader's own `open()`, the private snapshot path can be replaced
(`os.replace`) by a same-uid actor. The fd still points at the original inode,
so `verify()` and `verify_source_identity()` keep reporting the original
digest, while the reader consumes the replacement bytes. The snapshot is
created in a 0700 temp directory as a 0400 file; that defends against other
users only, not against the owning user/process the tests model.

Reproduced on both formats with actual generated SAV/DTA and the unchanged
facade/I03 consumer (`evidence/probe_toctou_sav.json`,
`evidence/probe_toctou_dta.json`):

| quantity | baseline (original bytes) | after private snapshot-path replacement |
|---|---|---|
| `source_sha256` / `snapshot_sha256` | original digest | original digest (unchanged) |
| `verify_source_identity()` | original digest | original digest (passes) |
| I03 `i03_y_cells` | `{"0": 1, "1": 1}` | `{"0": 0, "1": 2}` |
| I03 `i03_fact_ref` | `94f1d05c...` (SAV) | `248ae3e3...` |
| release content hash | baseline | changed |

So differently sourced native facts carry the old source/release identity.
Same root cause residuals (probe evidence in
`evidence/probe_metadata_and_batch_windows.json`):
- metadata-phase replacement: `decode_*` returns original `source_sha256`
  while variable identity comes from the replacement file (observed `W`→`Z`);
  the raw header prefix still comes from the fd, so metadata is internally
  inconsistent under this window;
- between-batch in-place same-size alteration after the first lazy batch: rows
  2–3 were served from the altered bytes while `source_sha256` stayed
  original; only a later `verify()` (if called) raises;
- between-batch truncation stops with an untyped `ReadstatError` (no silent
  misbinding observed there), and in-place writes need a chmod because the
  snapshot file is 0400.

Affected file: `rawlsing_next/pre553_physical_decoder.py` (candidate lines
171–178, 607–619; `_SourceSnapshot` lines 192–236). No production code was
edited by this review; the defect goes back to the same author.

## Independent tests added (author tests preserved verbatim)

`rawlsing_next/tests/test_universal_source_byte_custody.py`:
- `test_independent_snapshot_bound_c11_i03_facts_survive_original_path_replacement`
  (positive, SAV+DTA, real generated bytes → facade → C11 → I03; PASS);
- `test_private_snapshot_path_replacement_after_verify_cannot_rebind_old_identity_to_new_bytes[sav|dta]`
  (minimal defect demonstration; FAIL on candidate exactly at
  `assert observed == baseline`).
Diff vs candidate is additions only (+56 lines). Proof sidecar
`...py.proof.json` gained one independent claim (+11 lines).

Post-addition module: `2 failed, 17 passed` (16 author + 1 independent positive
pass; 2 are the defect demonstration). Post-addition core command:
`2 failed, 81 passed, 1 skipped` (the 2 are the same defect demonstration).
`proof_integrity_gate_r1.py lint` passes.

## Inherited older failures — independent classification

Exact nodes re-run at startup `6d95a78` and candidate `c1b0abec` under the same
fixtures/runtime (fixture and test files are byte-identical between the two
commits; only the candidate decoder diff differs, and it touches neither
`classify_physical_value` nor `physical_value_binding_key`). Both runs:
**10 failed, 24 passed**, with identical failure messages per node
(`evidence/candidate_r1e_r1i_r1j.xml`, `evidence/baseline_r1e_r1i_r1j.xml`).
Classification: **baseline-identical / reproduced inherited**, not candidate
regressions.

| node | message | artifact dependency |
|---|---|---|
| `test_fiabc_lm2_r1e_bounded_mapping_recovery.py::test_r03/r04/r05/r06/r07/r09/r17_*` (7) | `ValueError: representation authority variable identity/ordinal mismatch` | `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` → `rawlsing_next/fiabc_lm2_r1j_wvs7_representation_authority.py:176` (`Q291_VARIABLES` vs materializer variable identity/ordinal) |
| `test_fiabc_lm2_r1e_bounded_mapping_recovery.py::test_r11_lock2_and_complete_46_candidate_frontier_are_conserved` | `AssertionError: 8e5842eb... != 5e2a53f0...` | frozen LOCK2 predecessor vs `WVS7_LOCK2_IDENTITY` successor (`rawlsing_next/pre553_independent_parity_oracle.py`) |
| `test_fiabc_lm2_r1i_physical_native_hostile.py::test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation` | `AssertionError: physical_key 47f141e4... != b9b72033...` | frozen carrier projection (`WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json`) vs current binding key |
| `test_fiabc_lm2_r1i_physical_native_hostile.py::test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak` | `StopIteration` | frozen carrier lacks keys for `SPECIALS = (-5, -4, -2, -1)` |

## Attack matrix (actual facts/identities, not decoder flags)

| attack window | consumed bytes | old identity attached to new facts? |
|---|---|---|
| replace original path right after acquisition/before metadata | snapshot (original) | NO — facts equal baseline (author test + my positive test) |
| replace original path between metadata and lazy value | snapshot (original) | NO (author test) |
| replace original path between prehash and acquisition | refused before reader | NO (author test) |
| alter/truncate snapshot before lazy pass | refused (`DecoderError`) | NO (author test) |
| close snapshot then read | refused (`DecoderError`) | NO (author test; cleanup verified) |
| fresh-process old-digest cold replay, changed bytes | refused, no stdout | NO; restore reproduces identical fact payload (my probe) |
| genuinely changed same-path bytes acquired anew | new digest/new facts | NO; old incidence keeps old facts (author test) |
| **replace private snapshot path after verify, before reader open** | **replacement bytes** | **YES — reproduced SAV+DTA (defect)** |
| **replace private snapshot path before metadata pass** | **replacement metadata** | **YES — reproduced (residual, same root cause)** |
| **in-place same-size alter snapshot between lazy batches** | **altered later rows** | **YES — reproduced (residual, same root cause)** |

Private snapshot/runtime trust assumptions: the implementation trusts the
private snapshot path against replacement between verification and the reader
open, and trusts the reader to consume the same inode it verified. It does not
open the reader source with `O_NOFOLLOW`, does not re-verify after the reader
open, does not pass the verified descriptor/bytes to the reader, and does not
re-verify per batch. `source_custody["content_bound"] = True` therefore
describes the acquired snapshot, not provably the consumed bytes.

## Proof witness

`python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint <test>` →
`AST_LINT_PASS`. Witness over author + independent claim → both
`baseline PASS`, `fault_probe TARGET_ASSERTION_FAILED`,
`grade BOUNDED_MUTATION_DETECTED`; decoder restored exact
(`evidence/independent_proof_witness.json`). Fresh-process positive re-run
after restore: PASS.

## Limits

- No production/science/N11/original-source acceptance; no R03/R04.joined,
  joined issued workload, partial Batch/revocation/dedup lifecycle claim.
- Defect is reported, not repaired (reviewer cannot silently fix production
  code). Re-qualification is needed after the owner's repair.
- Uncovered by this pass: compatibility full-read window (needs an
  allowlisted encoding SHA not generatable here), between-batch path
  replacement as opposed to in-place alteration (same root cause), and
  generated-bytes determinism (SAV/DTA writer output differs per run, so
  identity must be checked within a run; author probe hashes are run-specific).
