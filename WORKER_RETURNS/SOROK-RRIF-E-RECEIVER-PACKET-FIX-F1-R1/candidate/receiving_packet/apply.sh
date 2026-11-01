#!/bin/sh
set -eu
TARGET=${1:?premain worktree}
PACKET=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
COMMIT=8d9585296ff264b947559f4a78f49f73ca45e53a
CPATH=WORKER_RETURNS/SOROK-RRIF-FINAL-E-REPAIR-AND-FIRST-CONSUMER-R1/candidate/rrif_r2
DEST="$TARGET/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null
[ -d "$DEST" ] || { echo "RRIF_E_BASE_R2_MISSING: install exact R2 candidate first" >&2; exit 2; }
python3 "$PACKET/verify_r2_base.py" --dest "$DEST" --repo "$TARGET" >/dev/null || { echo "RRIF_E_BASE_R2_IDENTITY_MISMATCH: STOP before write" >&2; exit 3; }
git -C "$TARGET" cat-file -e "$COMMIT^{commit}" || { echo "RRIF_E_CANDIDATE_COMMIT_MISSING: $COMMIT" >&2; exit 4; }
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
git -C "$TARGET" archive --format=tar "$COMMIT" "$CPATH" | tar -x -C "$TMP"
SRC="$TMP/$CPATH"
[ -d "$SRC" ] || { echo "RRIF_E_ARCHIVE_PATH_MISSING" >&2; exit 5; }
cp "$PACKET/overlay/joined/source_identity.py" "$SRC/joined/source_identity.py"
cp "$PACKET/overlay/tests/test_rrif_e_repair.py" "$SRC/tests/test_rrif_e_repair.py"
cp "$PACKET/RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json" "$SRC/RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json"
python3 "$PACKET/verify_packet.py" --root "$SRC" >/dev/null || { echo "RRIF_E_PACKET_SELF_CHECK_FAILED: STOP before write" >&2; exit 6; }
cp -a "$SRC/." "$DEST/"
python3 "$PACKET/verify_packet.py" --root "$DEST" >/dev/null || { echo "RRIF_E_INSTALL_VERIFY_FAILED" >&2; exit 7; }
echo "RRIF_E_PACKET_APPLIED_NOT_MERGED"
