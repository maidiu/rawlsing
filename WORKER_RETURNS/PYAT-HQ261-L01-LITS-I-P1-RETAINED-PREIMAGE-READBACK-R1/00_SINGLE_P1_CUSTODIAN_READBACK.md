# HQ261 L01 — single-P1 custodian readback

**RESULT: `CUSTODY_BLOCKER__AUTHORIZED_ARTIFACT_ABSENT_ON_THIS_HOST`**
**TERMINAL:** `HQ261_L01_RETURNED__NO_SELF_ADOPTION`

**Agent:** existing DeepSeek-Harness/OpenCode retained-evidence custodian worker
**Branch:** `agent/deepseek-harness-pyat-hq261-lits-i-p1-retained-preimage-inspection-r1`
**HEAD at inspection:** `ebc39373e83b2fcf9831e16d8a469d1f69f7fb98` (frozen base `788b2bf7…`)
**Live control:** `integration/pre-main-reconciliation-r1 @ 1ff7c74f6bef580ba3ce0738b7a9ac6b560ca2d7`
**Sealed HQ261 checkpoint:** `20261009-PYAT-HQ261-G1-TRUST-G3-LOCAL-LITS-P1-GHANA-R1 @ 91545f05…`
**Warrant read in full:** `PYAT_CONTROL_ROOM/HQ261_LITS_I_RETAINED_CANONICAL_P1_READ_ONLY_CUSTODY_INSPECTION_R1.md`
**Preceding S01 report read:** `465c87d218fdbb9892a5e0d712392d3a60a6b283`
**Runtime:** governed CPython 3.11.3, macOS 13.7.8 x86_64, isolated sparse shared-store worktree,
clean, read-only inspection (no production/test/control mutation).

## 1. Outcome

The warrant grants exactly **one-file / one-pointer** read-only access:

- file `court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json`,
  document sha256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`;
- pointer `/material/canonical_empirical_object_closure`,
  closure sha256 `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`.

**That file is not present on this host, and neither is its containing governed persistent store.**
The exact warranted path is

```
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/
  payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/
  court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json
```

and its **first existing ancestor is the repository root itself** —
`/Users/matthewsmith/Desktop/Rawlsing`. The whole `LOCAL_CUSTODY/…` chain is absent. A bounded
search of the home directory (depth 12, excluding `Library`) found **no** file named
`current_i05_materialization_checkpoint_v3.json` anywhere, and **no** directory named
`LOCAL_CUSTODY`.

Per the warrant — *"Report if too large or bytes not found without trying raw data fallback"* — and
per the commission — *"If local artifact absent … STOP explicitly; no raw DTA or Library fallback"* —
**I stopped.** No ordered-target, category, risk-set, response-configuration or joint/marginal
semantic readback is possible, and **none is asserted**.

## 2. Why this is a hard blocker and not an access-size problem

The custody manifest for this artifact records it exactly:

| field | value |
|---|---|
| `git_disposition` | `PERSISTENT_LOCAL_HEAVYWEIGHT_PAYLOAD` |
| `bytes` | **3 404 445 161** (3.4 GB) |
| `sha256` | `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` |
| `git_path` | `null` — *"explicitly excluded from ordinary Git and bound by SHA-256 in custody_manifest.json"* |
| `persistent_path` | the absent `LOCAL_CUSTODY/…` path above |

So the artifact was deliberately never committed to Git, and the only host that could have served it
is this one, whose `LOCAL_CUSTODY` store root no longer exists. There is no alternate authorized
copy: the retention command that produced it (`…/07_ONE_PASS_SOURCE_BACKED_EXECUTION_COMMAND.md`)
writes checkpoint v3 into a `FIABC_LITS_WORK_ROOT` from `LITS_SOURCE_PATH`, i.e. from a **raw**
LiTS-I source — regenerating it would require exactly the raw-survey access this warrant forbids.

## 3. What I explicitly did NOT do

- **No raw `.dta`/`.sav`.** `Data/LiTS_I.dta` (S01-recorded sha256 `7cac43e2…`) was not opened,
  decoded or hashed.
- **No Library fallback**, no public re-download, no source re-read.
- **No substitute object.** The Git-banked `current_i05_precheck.json`
  (83 613 bytes, sha256 `1ffbcb0f02e0c6b89a09cb255ce9342cbcb162ab2a1302de0ca8ade24990eed6`) exists in
  the repository, but it is **not** the warranted 3.4 GB checkpoint; the warrant's one-file
  permission does not extend to it, so it was not used as evidence.
- **No respondent-level, person-level, row-level or raw-variable output** of any kind; the analysis
  never reached any data rows.
- **No FF02 execution**, no admission rule/permission issued, no GT2 retarget, no N7/N9 or
  world/actor claim, no EE14 model use, no EE12 pair authority, no V3, no AT07 issuer/root.
- **No repository mutation** outside this return directory; no source/test/control/HQ edit.

## 4. Consequence for the S01 provisional claim

S01's provisional identification — that this candidate P1 query represents **`q301_2 × q301_7`** —
recorded `exact_pair_is_q301_2_q301_7_verified: false` and `complete_query_preimages_git_available:
false`. With the authorized preimage absent, that claim is, on this host:

**`UNPROVABLE`** — neither confirmed nor retractable. The warrant's instruction to *retract* the
claim "if actual ordered targets disagree" cannot be executed, because the actual ordered targets
cannot be read. The claim must stay provisional and **must not be adopted** in either direction.

## 5. Exact custodian request

Restore (or re-authorize access to) the single heavyweight payload at its recorded persistent path,
or issue a new warrant naming a verifiable current location, then re-run this L01 lane. Required for
a positive readback: the file must hash to
`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726` and expose pointer
`/material/canonical_empirical_object_closure` hashing to
`f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`.

See `03_NEXT_FF_SOURCE_PERMISSION_OR_HOLD.md` for the full request and the condition on which the
lane resumes.

**Terminal:** `HQ261_L01_RETURNED__NO_SELF_ADOPTION`.
