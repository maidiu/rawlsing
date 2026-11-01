#!/bin/sh
set -eu
TARGET=${1:?premain worktree}
PACKET=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DEST="$TARGET/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
[ -d "$DEST" ] || { echo "ROLLBACK_DEST_MISSING" >&2; exit 2; }
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
git -C "$TARGET" archive --format=tar 598d9e9eaba5143950c63317705fd09104fbf463 SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 | tar -x -C "$TMP"
rm -rf "$DEST"
mv "$TMP/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2" "$DEST"
python3 "$PACKET/verify_r2_base.py" --dest "$DEST" --repo "$TARGET" >/dev/null
echo "RRIF_E_ROLLBACK_RESTORED_EXACT_R2"
