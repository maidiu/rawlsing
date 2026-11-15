# SOROK C05 — focused R2 rereceiving (same nonauthor)

**Verdict:** `ACCEPT_SCOPED_SOURCEFREE_C05_OPERATION_CUSTODY`
**Accepted source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Frozen final report:** `1cf1a37113cb7a48137734648b523a0a6deccd92`
**Frozen start / defect base:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Original implementation:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Original independent review:** `b5b810cdd7b51b20efcc42d4ce76960f9e410706`
**Reviewer session:** `ses_e2186e745ffecK1Ilg4cw26pVu` — same nonauthor; did
not write the repair.
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1038-custody-g5/Rawlsing`
**Branch:** `codex/sorok-c05-focused-g5-r2-20261115-r1`

This is the focused closure of the original `REVISE_EXACT_DEFECT`, not a new
duel, theory review, architecture review or general C05 acceptance.

## 1. Exact correction verified

From the frozen start to the final source, the only product change is one line
in `promote_relation`:

```diff
-    machine = _state_machine(state_changes)
+    machine = _state_machine(scope["changes"])
```

`state_changes` is still used for the promotion `history_hash` (state entries
only). `supporting_actor.py` is byte-unchanged at
`98cb4ceb3e5e201815c0ac46ba93f773601d818c`. No owner, transaction, schema,
ledger, actor or representation change was added. The post-code commits
`ea7c632b2` and `1cf1a3711` add return/evidence metadata only; the product and
test trees are unchanged after `5d771dd86`.

Pins: corrected module blob `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
(SHA-256 `72e213220ed2855a5bd303985a7a584cb14b1a3b2e704b26aa4b8161fef068d2`);
focused test blob `5df2c164bc4912a2ee13cbaf228969c2d4b96a90`; original C05 test
blob `4741264d5b23195731d7fe7f0f77e72ec847442e`.

## 2. Original defect closure

The byte-identical original reviewer defect probe (`blob
31a888cb9189686d321f29ab27e95aa8fe5f9d9e`, SHA-256
`1172fec4621c353bee5736423c42e5278dc3a1148112c676cd53f7b687105a70`) was copied
from `b5b810c` into `newprobes/` and run at the corrected source.

At the frozen base it reproduced the old defect: `RELATION_CUSTODY_SEVERED`,
write on refusal, permanent `HOLD_CUSTODY_SEVERED`, 49/2/2 → 51/3/3. The
immutable original RED is preserved at
`evidence/c05_defect_report_RED_original_b5b810c.json`; the author's RED receipt
is semantically identical (same probe bytes, counts and fields; report bytes
differ only by checkout-specific state root).

At the corrected source the same probe returns literal exit **2**, as expected,
because its unchanged oracle still asserts the old bug. The graded fields are
the closure:

| Field | Corrected |
|---|---|
| `second_call_refusal` | `RELATION_PROMOTION_NOT_DEEPER` |
| `wrote_episode_on_refusal` | `false` |
| `scope_severed_after_write` | `false` |
| `c12_verify_unchanged` | `true` |
| before/after episodes | 49 / 49 |
| before/after changes | 2 / 2 |
| before/after heads | 2 / 2 |
| world events / perceptions / checkpoints | 14/14, 42/42, 33/33 |
| relation status | `QUALIFIED` → `QUALIFIED` |
| first-operation retry | `UNCHANGED`, same primary ID |

Literal exit 2 is **not** a repair failure. The probe's static `defect` text is
its original immutable description, not a live finding; the live graded fields
above are corrected. Report: `evidence/c05_defect_report.json`, SHA-256
`d91901bfddb967b1dfdb891754c503996eb2e7d57527c0d4c15df44a4a36eeb8`.

The independent closure probe (`newprobes/c05_closure_probe.py`, 12/12 checks)
also verifies: first depth-2 promotion recorded; same-original-operation retry
`UNCHANGED`; different new depth-2 operation refuses before append; zero
episode/change/world-event/perception/checkpoint delta; relation episodes
unchanged; relation history and later-event context byte-exact and `QUALIFIED`;
`PERCEIVED` event access preserved; C12 verify ok; original retry after refusal
still `UNCHANGED`. Report `evidence/c05_closure_report.json`, SHA-256
`b815af9f4090c55dfceba5e68f187a64a49e31f3c8069374cd3e187e6212c1c3`.

## 3. Independent runs (final source)

Every command used
`TMPDIR=$PWD/.local-logs/sorok-c05-focused-r2/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`,
`-B`; pytest used `-q -p no:cacheprovider`; `/usr/bin/time -l` recorded RSS.

| Run | Result | Exit | Real s | Max RSS B |
|---|---:|---:|---:|---:|
| focused R2 test | 1 passed | 0 | 7.19 | 56,725,504 |
| original C05 suite | 5 passed | 0 | 42.18 | 61,513,728 |
| C01 supporting actor | 6 passed | 0 | 14.08 | 56,315,904 |
| C04 first-consumer identity | 6 passed | 0 | 26.23 | 64,487,424 |
| C04 custody | 12 passed | 0 | 54.90 | 68,943,872 |
| P2 owner | 5 passed | 0 | 14.83 | 58,519,552 |
| byte-identical 89-check normal/negative/cold probe | 89/89 passed | 0 | 160.63 | 57,630,720 |
| independent closure probe | 12/12 passed | 0 | 5.63 | 46,501,888 |
| byte-identical original defect probe | old bug not reproduced | **2 expected** | 2.91 | 37,203,968 |

The 89-check probe remains 89/89 with fresh-process cold exactness and cold
retry `UNCHANGED`; it preserves earlier event contexts, normal depth 1→2,
partial exposure, private boundaries, change/head sever-restore and the later
real P2 consumer. Logs and raw reports are under `evidence/`.

## 4. Explicit scope boundary

This verdict receives only **bounded mechanical operation/custody** of
caller-authorized sourcefree illustrative relations:

- caller-supplied relation value/change/exposure; both parties mandatory;
- dated append-only continuity/history, finite depth 1→2, qualified HOLDs and
  the existing later P2 event consumer;
- relation visibility remains `DATED_EXPOSURE_ONLY`, distinct from normal event
  `PERCEIVED`.

It does **not** receive or prove:

- an owner/source receipt for relation knowledge (none exists);
- relation `PERCEIVED` actor truth, native ADP-015/C4 authority, psychology,
  autonomy or independent actor awareness;
- the coherent public append of a change+head as owner authentication (it
  remains a disclosed caller-authorized sourcefree boundary; the self-hash is
  not an owner signature);
- G2 selection, generated language, complete J1/Nadia response, J2, D04/D05,
  protected merge, human/science/source rights, fork/concurrency uniqueness,
  depth >2, or whole C05 person life.

**Original full C05 actor qualification remains UNPROVED.** Caller exposure is
not independent perception or owner-qualified relation knowledge. The C04
parent-metadata/D03 residuals remain held. The author's late metadata discloses
a temporary symlink in its own checkout; this review did not use that adapter
and ran the byte-identical probes directly in its own authorized scratch. The
old published review/files and its claims are preserved.

## 5. G1–G5

| Gate | Status | Basis |
|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact final/implementation/start pins; one-line product delta; supporting actor unchanged; metadata-only post-code commits; product read-only |
| G2 build/actual first consumer | `PASS_FOCUSED_CLOSURE_AND_NORMAL` | focused 1, original 34, 89/89, closure 12/12; real P2 event and later consumer preserved; cold exact |
| G3 falsification | `PASS_DEFECT_CLOSED` | byte-identical original probe exit 2 expected; refusal before append; zero deltas; history/context exact; retry unchanged; base RED preserved |
| G4 preservation/restore/cold | `PASS_PRESERVATION_SCOPED` | C01/C04/P2 pass; earlier contexts, partial exposure, private, sever-restore and cold remain green; C12 verify ok |
| G5 independent receiving | `ACCEPT_SCOPED_SOURCEFREE_C05_OPERATION_CUSTODY` | one exact defect closed; no material regression; scoped mechanical custody only |

## 6. STOP

`ACCEPT_SCOPED_SOURCEFREE_C05_OPERATION_CUSTODY@5d771dd86767655534b23576075e5da2db4fba78`
is earned at the explicit caller-authorized fixture boundary above. No blanket
full C05, actor qualification, autonomy, native or protected acceptance. One
final verdict; no further author/duel/staging/protected merge.
