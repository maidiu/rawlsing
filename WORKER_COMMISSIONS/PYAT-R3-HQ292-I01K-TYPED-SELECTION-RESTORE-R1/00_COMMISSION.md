# PYAT HQ292 I01K — smallest typed selection-key restore refusal

**STATUS:** SEALED_RESOURCE_GATED__NEW_NEEDS_LAUNCH (commission does not launch a worker).
**Repository:** maidiu/rawlsing PRIVATE.
**Role:** narrow integration owner error-contract repair, NOT HQ, NOT S00V3X reviewer or original I01R reviewer.
**Candidate owner exact base:** I01R accepted `473b7997d1b446c54a2d8688f94053b6c8670881`.
**Branch:** `agent/rabochii-pyat-r3-hq292-i01k-typed-selection-restore-r1`.
**Exact sealed startup:** HQ verified post-commission 40-hex remote HEAD, must match before edits.
**S00V3 accepted bounded seam:** `aba2f6a60d21b8daeeaf9eb3cfadef2620ac13f4`.
**S00V3X independent SOURCEFREE runtime review:** `ed34944e253b78714a28d72b8ca2a6521ce15930`.
**Frozen independent red case:** `WORKER_RETURNS/PYAT-R3-HQ291-S00V3X-INDEPENDENT-OFFLINE-EXECUTION-R1/repro/test_hq291_s00v3x_typed_index.py` at exact S00V3X tip, separately versioned strict typed-refusal test; preserve unchanged bytes.
**Canonical:** `integration/pre-main-reconciliation-r1` at `7f29aec36d24f16da52d84f17c00f08db3a55434` unchanged.

## Mission
Fix only the confirmed residual integrated-owner defect in `rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py::restore_product`. Existing code uses:
```python
key = next(k for k in life.export_checkpoint()['checkpoint_payload']['selection_keys'] if k['record_ref'] == index['selection_key_ref'])
```
When index selection_key_ref is forged, missing, foreign or incorrect shape, `next` may produce uncontrolled Python `StopIteration` rather than typed `I01Error`. Make the smallest fail-closed and exception-safe explicit identity validation that checks the required exact selected selection-key reference against lifecycle checkpoint, handles no match, invalid shape and optionally duplicate matches without silently choosing one; preserve legitimate existing key structure and selected receipt consistency. A forged missing key must NOT construct Product, advance B5 CURRENT, revive invalidated state or turn into `NO_CURRENT` false positive. Prefer fixed explicit I01Error reason like `SAVED_SELECTION_KEY_IDENTITY_MISMATCH` and document reason law.

Do not broaden to M2/B5 owner rewrite, alter valid wire identities, sourcefree numerical code, P01 callbacks or scientific semantics. If additional genuine malformed index paths cause other uncontrolled exceptions, log exact typed concern without scope expansion absent separately demonstrable minimal co-fix.

## Mandatory actual local tests
- Reproduce the **byte-original independent S00V3X test** `test_forged_selection_key_requires_typed_product_refusal` and record its expected historical FAIL on I01R original and required new PASS after repair. Do not edit original frozen test or expected exception.
- Add new tests `test_hq292_i01k_*.py` with missing, foreign, invalid-type, duplicate (where representable) selection key and positive correct saved key. Require typed reason and no successful Product on negative.
- Execute the original untouched I01R 26 test source `rawlsing_next/tests/test_hq288_i01r_independent_product.py` and I01 author 10, against actual isolated composite I01R owner patch with exactly S00V3 seam @aba2f6..., no unrelated owner imports from wrong namespace path.
- If independently feasible, exact S00V3R original independent 18-case offline court from `d4967c2f00b60d496a9c8a78714cf47fb0035953` using independently frozen candidate source selector and original P04 pins; at minimum retain the sourcefree accepted I01 byte artifact SHA256 `a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606` and release `582317a6731c43d84959f7d0e74604f30bba4d49f3fe114f1afb07f63108d22a` and run fresh product replay.
- Keep original S00C 27 historical 26/1, S00CR 16 historical 12/4 and S00E revised 27 historical 26/1 distinctly labeled RED under the already explicit S00M acceptance migration. Never rewrite them or assert they are green.
- Source-free only, no raw survey access. Confirm cold replay numerical output and after invalidation current refused/as-of replays; do not incorrectly assert full restore requires zero P04 *setup* calls.

## Write and resource controls
Change **ONLY** the I01 lifecycle module plus noncolliding new tests and own `WORKER_RETURNS/PYAT-R3-HQ292-I01K-TYPED-SELECTION-RESTORE-R1/` artifacts. No edits to S00V3 seam or independently frozen tests, P04, P01, S06G, M2/B5, canonical, protected CURRENT, actor, V3 or raw source. Resource choose eligible NON-CODEX local Python/low-cost code model with verified privacy and one shared Go allowance where possible; SECONDARY Mac Codex B GPT-6.1 Sol Low is allowable **only after fresh entitlement/quota, independent separate sparse worktree and no paid credits**. Primary Mac Codex A reserved for Astra. No clone/reset/broad fetch; exact object fetch and sparse root. If no qualified executor, return typed RESOURCE_HOLD not invented pytest.

## Return
Actual test commands/cwd/PYTHONPATH/exit/JUnit, exact Git blob/sha of frozen reviewer test and changed module, full unfiltered failures, exact saved product result, frozen original typed red become PASS, resource model/provider/account/quota/cost or UNKNOWN and exact pushed remote SHA. No self-adoption or scientific issuer. New independent post-repair qualification by separate reviewer if the change affects more than typed key restoration.
