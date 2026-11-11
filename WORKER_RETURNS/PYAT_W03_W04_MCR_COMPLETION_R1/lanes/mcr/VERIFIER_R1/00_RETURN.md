# CC-F05 verifier repair return

**Status:** `DELIVERED_PENDING_RECEIVING`

**Branch:** `agent/pyat-w03-w04-mcr-verifier-repair-r1`
**Initial clean HEAD:** `26f70635e8493c7759fa087b17da269104bd8922`
**Repair scope:** CC-F05 only: executable MCR launch presentation and external
postcommit evidence boundary through the existing validator. This is not whole
MCR acceptance.

## Finding and repair

The frozen `PYAT_W03_W04_MCR_C_Commission.md` is preserved byte-for-byte:
SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`.
It has no single fenced launch block, so the exact original validator command
returns `RED_INVALID_FOR_DISPATCH: REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK`.
That RED is historical and is not relabeled as PASS.

A faithful external presentation was added at:

`WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md`

It contains the exact frozen MCR contract block (1 scope, 12 obligations, 1
receiving record), the complete launch header, and a runtime-selection addendum
recording the already-qualified `opencode-go/deepseek-v4.1-flash#max` session.
It passes the existing checker:

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Result: `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH`, 12 obligations,
contract SHA-256 `1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583`.

The original `no_drop_check` remains inside the frozen contract as historical
text. Its corrected executable presentation/invocation is documented in the
addendum and below; the original file is not claimed to have passed.

## External evidence boundary

`verify_copy_paste_commission_r1.py --verify-return` now receives the actual
evidence path and rejects a path that is tracked at the candidate SHA. This
enforces a repository-tracking exclusion: evidence must be outside the candidate
commit, or untracked at that candidate. It does not invent timestamp or stronger
provenance; the result is explicitly marked
`REPOSITORY_TRACKING_ONLY__NO_TIMESTAMP_OR_STRONGER_PROVENANCE`.

Corrected final invocation:

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md \
  --verify-return RECEIVING_EVIDENCE.md \
  --candidate-sha "$(git rev-parse HEAD)" --evidence-root .
```

The validator still checks exact candidate HEAD, source tuple blobs, 12 exact
identities, committed output/evidence paths and digests, grades, statuses and
missing/extra/duplicate records. It returns
`READY_FOR_INDEPENDENT_RECEIVING` only; it never issues authoritative completion.

No final `RECEIVING_EVIDENCE.md` block, delivered IDs or 12 same-head PASS
package is created or claimed here.

## Verification

- New validator tests: **4 passed**.
- Existing validator self-test: **PASS_SELF_TEST**, 5 positive kinds, 32 negative
  mutations rejected.
- Launch artifact: **PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH**, 12 obligations.
- Frozen contract baseline: **RED_INVALID_FOR_DISPATCH** (preserved).
- External positive evidence: accepted.
- Tracked self-contained evidence: rejected (`MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE`).
- Wrong candidate and forged output hash: rejected; valid external evidence
  restored to `READY_FOR_INDEPENDENT_RECEIVING`.

## Remaining

CC-F01/F02/F03/F04 and economics are not reworked here; CC-F03/F04 remain with the
exclusive bench owner after its return. Final same-SHA 12-ID evidence, external
postcommit receiving block, independent code/economic review and protected
receiving remain open. No whole-MCR, source/science/native/actor or protected
acceptance is claimed.
