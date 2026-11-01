#!/bin/sh
set -eu
TARGET=${1:?premain worktree}
CANDIDATE=${2:?candidate root containing receiving_packet}
DEST="$TARGET/SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2"
test -f "$DEST/joined/session.py" || {
  echo "RRIF_E_BASE_R2_MISSING: install exact R2 candidate first" >&2
  exit 2
}
patch -p1 -d "$DEST" < "$CANDIDATE/receiving_packet/RRIF_E_ADDITIVE.patch"
echo "RRIF_E_ADDITIVE_APPLIED_NOT_MERGED"
