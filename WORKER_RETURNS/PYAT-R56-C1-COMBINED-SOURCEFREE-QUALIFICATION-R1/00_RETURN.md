# R56-C1 — combined-candidate source-free compatibility return

Disposition: **ACCEPT_SCOPED_LOCAL_COMPOSITION_COMPATIBILITY__NATIVE_PROMOTION_HOLD**.

The exact accepted R00 gate and R02 adapter compose with the accepted R04
read-only decoder on one isolated tree. The actual decoder -> R02
`materialize_native_preimages` -> unchanged facade/C11 -> unchanged I03 path
produces the exact frozen tuples/domains/facts on generated SAV and DTA, the
R04 custody attacks preserve/refuse correctly, and the actual accepted R00
evaluator returns positive POLICY_ONLY consistency plus the expected
refusal/HOLD ceilings. No native promotion is claimed: R08/R09 authenticated
association/enforcement remain NOT_IMPLEMENTED/NOT_REACHED.

- Engineering: ACCEPT_SCOPED_LOCAL composition compatibility on the tested
  local interfaces.
- Science: no new science, no original data, no original35/N11 measurement.
- Authority: no production/CI/adoption, no universal-machine, no R03/R04.joined,
  no joined issued workload, no partial Batch/revocation/dedup lifecycle.

## Session, startup and assembly

- Same independent `R56-R04BYTEV` reviewer, fresh context; R00/R02/R04
  production was authored by other sessions and installed only as exact pinned
  blobs. R1/R2/R3 reviewer branches/returns preserved; author worktrees not
  reused. Session details in `00_STARTUP_SESSION_RECORD.md`: OpenCode,
  `opencode-go/deepseek-v4.1-flash`, effort/provider/session ID
  `UNKNOWN_NOT_EXPOSED`, host `MacBook-Pro.lan`, macOS 13.2.1, Python 3.11.3,
  pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1.
- Startup `625f24a28ed8c567ca3d7bb330ddb91d6c7b2ce7`. C1 branch/worktree were
  verified absent before creation; no duplicate C1 job.
- Production assembly commit (the actual combined candidate SHA):
  **`a2aeb53b0a1e6abb93d4bb3d173007002fd7cf44`**. Production diff vs startup is
  exactly:
  - `CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py`,
    `git hash-object e31ed7565b3dd59fcd65e2c865f55d48ae786dfa` (R00
    `3d4d77e9`, reviewed `d02ef322`);
  - `rawlsing_next/pre553_source_native_preimage_adapter.py`,
    `git hash-object a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` (R02
    `6f4be338`, reviewed `e1f0aeb6`);
  - R04 decoder unchanged `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd`
    (startup).
- Accepted tests copied with pinned blobs from the review refs (R00
  `d02ef322`: `conftest` `662d3b3f`, `dependency_probe` `be536964`,
  `r00v_r2_dependency_probe` `ecff8bd1`, `test_r00e_r2_reviewer_regressions`
  `54f44f2e`, `test_r00v_r2_requalification` `98dbd60b`, `test_r56_gate`
  `5d433783`, `.gitignore` `7a60b85e`; R02 `e1f0aeb6`: projection test
  `ff9aea0f`, proof `7e4294d4`). R04 byte tests preserved at startup blob
  `76a2a17a`. Added focused C1 test blob `6f59bb38` and proof sibling
  `886ceae0`. The final test-tree commit SHA is recorded in
  `evidence/final_remote_readback.json` after the qualification commit.

## Actual combined native path (claim a)

Evidence `evidence/probe_combined_path.json` and the C1 tests:

- SAV 4×2 and DTA 4×2 generated through `pyreadstat`; decoded with
  `decode_sav`/`decode_dta` and the expected digest.
- Source identity: `source_sha256 == sha256(file bytes) ==
  snapshot_sha256`; `reader_access_mode == "O_RDONLY"`; reader binding
  `OPEN_FD_VIA_POSIX_DEV_FD`; pathname unlinked.
- Adapter output routed through the unchanged facade/C11; release
  `source_artifact_ref.content_hash` equals the source sha.
- Exact event tuples (8): `("R56R02:P0",0,SUBSTANTIVE,"0")`,
  `("R56R02:P0",1,...,"1")`, `("R56R02:P1",0,...,"2")`,
  `("R56R02:P1",1,...,"3")`, repeated for P2/P3. Prospective I03 domains are
  the exact per-respondent occasion-ordered event lists returned by the
  source-derived oracle.
- I03 fact: `SUPPORTED`, denominator 4, numerator 4, 4 cells with support 1,
  deterministic same fact ref on repeat. DTA gives the same.
- Composition variation: reversed SAV rows conserve tuples and the
  respondent/occasion/value domain projection (event ids rebind to the new
  source sha); 5 respondents conserve the denominator/cardinality shape.
- DTA separate-unit household/person fixture refuses
  `CROSS_UNIT_POOLING_UNAUTHORIZED` before any C11.

## Custody and interaction attacks (claim a)

`evidence/probe_combined_path.json` and the C1 test:

| attack | result |
|---|---|
| original path replaced after acquisition | same bound tuples/fact ref |
| foreign file at old private snapshot path | not consumed; same fact; foreign survives close |
| `write` / `pwrite` / `ftruncate` through supplied fd | denied `OSError` (9/9/22); digest and fact unchanged |
| shared writable `mmap` through supplied fd | denied `EACCES` 13; fact unchanged |
| `/dev/fd` reopen `O_RDWR` | denied `EACCES` 13; fact unchanged |
| normalized source-key collision `{0.0:"P0","0":"P1",1:"P2"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY` before C11 |
| duplicate destination `{0.0:"1",1:1}` | `DUPLICATE_RESPONDENT_KEY_MAPPING` before C11 |
| permitted value fault on the same query | changed/refused fact |
| exact original bytes restored | same fact id/payload; fresh-process fingerprint identical |

Producer-dependency witness: `evidence/c1_proof_witness.json` — adapter
`canonical` substitution makes the same source→fact tuples assertion RED
(`TARGET_ASSERTION_FAILED`), and normalized source-key guard removal makes the
collision assertion RED; adapter restored byte-exact
`a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c`. Fresh positive nodes pass after
restore (`evidence/fresh_positive_after_witness.txt`).

## R00 policy/claim ceiling on the same tree (claim b)

`evidence/probe_r00_gate.json`; policy `6d95a78b...` variant CANONICAL_V1,
freeze blobs verified (`CONTRACT` `01ccb464`, `policy` `5f5d0253`,
`synthetic_universes` `66fdf81f`, `decision_cases` `5608e9c3`, `freeze`
`dfc1c375`):

- complete POLICY_ONLY claim -> `ALLOW_LOCAL_POLICY_CONSISTENT`, ceiling
  `LOCAL_ONLY_POLICY_CONSISTENT`;
- missing/altered frontier -> `REFUSE_FRONTIER`, ceiling NONE;
- EXECUTED_NATIVE without R09 -> `HOLD_TRUSTED_NATIVE`, ceiling local-only;
- GENERIC_SOURCEFREE -> `HOLD_GENERIC_R09`;
- supported status without native evidence -> HOLD/refuse;
- `K_mutation` marker -> `REFUSE_IDENTITY`; this is the gate's policy conflict
  marker, **not** native producer-consumer association verification;
- policy substitution changes the same claim's GateDecision to
  `REFUSE_FRONTIER`; restore returns `ALLOW_LOCAL_POLICY_CONSISTENT`.
- No verified-evidence handle was constructed; local run logs are not R09
  attestation; no native-positive gate verdict was issued.

The two claims are distinct: (a) actual native projection/custody
compatibility, (b) R00 policy/claim-ceiling enforcement on the combined tree.
R08 serving association and R09 authenticated enforcement are
`NOT_IMPLEMENTED`/`NOT_REACHED` at their actual boundary.

## Suites run once on the combined tree

`evidence/combined_suites_receipt.txt`:

```
tests/universal_execution_oracle (R00 accepted + C1 focused)
rawlsing_next/tests/test_universal_source_projection.py (R02 accepted)
rawlsing_next/tests/test_universal_source_byte_custody.py + R04 core modules
169 passed, 1 skipped in 68.89s
```

The skip remains `test_pre553_sr06_decoder_carrier.py:268` (installed
pyreadstat writer/readback does not expose `missing_user_values`; DTA
extended-missing unexercised/unqualified). No broad historical archaeology.

## Missing capability / next owner

- R08 serving association (actual producer-consumer identity binding) and R09
  authenticated enforcement: NOT_IMPLEMENTED/NOT_REACHED; later separately
  gated. The gate's `K_mutation` marker is not a substitute.
- R01/R03 prospective grammar/lowering, R05/R06 learned/world integration,
  joined replay and original science/R07 are outside C1.
- Preserved limits: POSIX `/dev/fd`; read-only trusted-runtime assumptions and
  fail-closed raw OS exception paths; DTA full-frame O(rows×cols) memory; SAV
  streaming with one hash per pass; transformed R02 stream limited to the
  admitted facade path; synthetic encoding authority only; no all35/N11 scale
  or original-source claim.
- No module repair is needed for the tested composition; this return is not HQ
  adoption or native promotion.

## Disposition

**ACCEPT_SCOPED_LOCAL_COMPOSITION_COMPATIBILITY__NATIVE_PROMOTION_HOLD.**
No production/CI/adoption, no universal machine, no original35/N11, no
authenticated native-promotion claim. After this finite job, stop; do not
launch R01/R03/R08/R09 or renamed J52/W52.
