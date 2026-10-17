# SOROK VOZHD-2 HQ322 OUT14 — Bounded implementation candidate / typed HOLD

## Identity, custody and governing law

- Repository: private `maidiu/rawlsing`.
- Sealed startup and exact branch HEAD at launch: `ddf7f1550d76c8b94661f089631ba67432c37ee1`.
- Worker branch: `agent/rabochii-sorok-v2-hq322-out14-multiwriter-integrity-repair-r1`.
- Governing docs: complete sealed OUT14 commission; `SOROK_PRODUCT_CONTROL_ROOM/00C_*`, `00D_*`.
- Source provenance: original OUT12 candidate blob `99217d390a452f22fc1a470abc411c6ca84b86ba`; original OUT9 accepted baseline `331840768ce0b5f6f73e5e93094ca0d217ddaebf`; OUT13 review `9b4392f86d942ba12eddc31c5b9ae33ba309597c`.
- Writes restricted to the original OUT12 **candidate** Python module and the new OUT14 return directory; no OUT9 source, frozen author or independent tests, shared control, ADP019, PRE-MAIN, CURRENT or canonical history modified.

## Implemented but NOT qualified

The OUT12 candidate now seals `schema/state/writer_version` together into a deterministic `version_state_digest`, in addition to the accepted state digest; refuses missing/corrupt/unknown/noncanonical version fields with typed `VERSION_STATE_UNREADABLE`; permits genesis version zero **only** when the journal file is absent; enforces an unchanged acknowledged-ledger prefix on replacement; and separates `os._exit(79)` from actual `SIGKILL_BEFORE_RENAME` and `SIGKILL_AFTER_COMMIT` hooks.

New independent-of-OUT13 *author* tests cover malformed/deleted version, unversioned legacy overwrite, noncanonical metadata, stale CAS, prefix preservation, 2/3/5 process barrier races, lock timeout, pre-/post-rename exit and signal boundaries, and unkeyed forged-version counterexample. These tests are **UNEXECUTED**; do not treat them as verification.

## Real runtime and acquisition receipts

- Actual Browser Python: 3.13.5; pytest 9.0.2; git 2.47.3; subprocess and `fcntl.flock` verified.
- Browser-generated identical files were byte-checked against the GitHub blob SHA-1, including the NUL byte in `blob <size>\0<contents>`.
- `python -m py_compile multiwriter_journal.py test_out14_integrity.py`: **PASS**, syntax only, two exact SHA-verified sources.
- `pytest -q --disable-warnings test_out14_integrity.py`: **exit 2 / collection ERROR** `ModuleNotFoundError: No module named 'outbox_prototype'` (NOT_RUN, 0 tests executed). Consult `out14_collection.log` in this return.
- `python -c 'import os,signal,subprocess,sys;...'` delivered real `SIGKILL` to a child: **-9**. Separate `os._exit(79)` child: **79**. This is a runtime capability preflight, NOT proof a journal write survived a signal.
- The GitHub connector read the exact private source, but it did not mount the checkout or inherited imports into Browser Python. Direct GitHub `git ls-remote` failed `Could not resolve host: github.com`. Missing pinned closure is `MISSING_SOURCE_STAGING`, not missing Python/pytest.
- Original inherited 272: **NOT_RUN**; historically OUT13 reported 270 PASS / 2 historical RED. OUT12 nine: **NOT_RUN** (historically 9 PASS). OUT13 frozen 23: **NOT_RUN** (historically 23 PASS). OUT14 new court: **NOT_RUN / collection ERROR**. No JUnit created; no artificial green counts.

## Binding authorization and scientific HOLD

**Disposition: `SOURCEFREE_AUTHORIZATION_BYPASS_UNCLOSED`; `OWNER_REQUIRED`; `EXECUTABLE_BASELINE_NOT_STAGED`.**

1. Original accepted `Journal.commit` remains directly callable and can overwrite the journal without version enforcement or locking. The new wrapper detects that older writer's unversioned receipt **after** the bypass, but cannot prevent already-erased data or withdraw the old writer's permission. Only an accepted owner can close every legally callable writer path and grant the facade exclusivity.
2. The seal is an **unkeyed hash**, not keyed writer authentication. Any actor allowed to rewrite the file can recompute the digest; replacing it with an entire old valid receipt can roll back the version. A trusted external anchor or owner-managed capability is necessary for anti-rollback and writer authenticity. This candidate expressly includes a falsifying test exposing recomputation.
3. Because the required genuine pinned test closure was not staged, no operating integrity verdict or independent I2 acceptance follows from the syntax checks.

No claims of power-loss durability, exactly-once client delivery, real actors, ADP019 event issuance, product V3, or semantic adoption. Independent I2 review must be separately commissioned by HQ after a qualified executable court and authorization-owner adjudication.

## Return and next authorized work

Reconstruct only missing **pinned source-free** module closure with verified Git blob SHA-1 and actual imported path; rerun unchanged 272 + 9 + 23 and added author court; preserve 2 historical REDs. Obtain formal old-writer restriction from competent owner. Do not green multiwriter security while the bypass is a legal path. The branch records an unaccepted candidate plus concrete HOLD, not HQ adoption.
