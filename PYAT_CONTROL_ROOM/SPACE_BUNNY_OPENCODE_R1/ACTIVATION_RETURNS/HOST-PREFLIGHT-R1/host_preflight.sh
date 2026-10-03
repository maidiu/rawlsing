#!/usr/bin/env bash
# HQ192 — SHA-pinned, source-free host execution preflight.
#
# Verifies the pinned execution identities and the adopted disk policy BEFORE any
# live run. Fails closed. Executes NOTHING: no live C4, no source access, no
# locator discovery, no warrant issuance.
#
# The disk threshold is a REQUIRED POLICY INPUT, not a value chosen here.
# Governed repository evidence declares no source size, output size, peak disk
# footprint or execution write volume, so no defensible number can be derived
# (see WORKER_RETURNS/.../02_DISK_EVIDENCE_AND_THRESHOLD.json). This script
# therefore REFUSES to proceed unless HQ has adopted a threshold and supplied it
# via HQ_DISK_MIN_FREE_GIB. Inventing a default here would be exactly the
# failure this preflight exists to prevent.
#
# Usage:
#   HQ_DISK_MIN_FREE_GIB=8 ./host_preflight.sh            # KiB/MiB/GiB accepted
#   HQ_DISK_MIN_FREE_GIB=8 ./host_preflight.sh --json
#
# Exit codes: 0 all checks passed | 2 identity mismatch | 3 policy threshold
# not adopted | 4 insufficient free space | 5 environment unusable
set -u

REPO="${HQ192_REPO:-/Users/matthewsmith/Desktop/Rawlsing}"
PY_REL="LOCAL_COURTS/tooling/python"
FREEZE_COMMIT="8ff40d37de69db2d8a6053a7c2242f481677f1a4"
NEXT_TREE="b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0"
INTERP_SHA="11d6f541a870a141249ce98d45834a6789e29c07031e85ce17f3e67f24c535f6"
INTERP_REL="$PY_REL/cpython-3.11.3-macos-x86_64-none/bin/python3.11"
SHORT_REL="$PY_REL/cpython-3.11-macos-x86_64-none/bin/python3.11"

AS_JSON=0; [ "${1:-}" = "--json" ] && AS_JSON=1
FAIL=0; declare -a LINES

rec() { LINES+=("$1"); [ $AS_JSON -eq 1 ] || printf '%s\n' "$1"; }
ok()  { rec "  PASS  $1"; }
bad() { rec "  FAIL  $1"; FAIL=1; }

rec "HQ192 source-free host execution preflight"
rec "repo: $REPO"
rec "NOTE: this preflight performs NO live execution and opens NO source data."

# ---- 1. executable freeze commit -------------------------------------------
rec "[1] executable freeze commit"
if git -C "$REPO" cat-file -e "${FREEZE_COMMIT}^{commit}" 2>/dev/null; then
  ok "freeze commit present: $FREEZE_COMMIT"
  SUBJ=$(git -C "$REPO" log -1 --format=%s "$FREEZE_COMMIT" 2>/dev/null)
  rec "        subject: $SUBJ"
else
  bad "freeze commit absent: $FREEZE_COMMIT"
fi

# ---- 2. rawlsing_next tree at the freeze commit ----------------------------
rec "[2] rawlsing_next tree identity"
GOTTREE=$(git -C "$REPO" rev-parse "${FREEZE_COMMIT}^{tree}:rawlsing_next" 2>/dev/null || echo "")
if [ -z "$GOTTREE" ]; then
  gotraw=$(git -C "$REPO" rev-parse "${FREEZE_COMMIT}:rawlsing_next" 2>/dev/null)
  GOTTREE=$(git -C "$REPO" rev-parse "${gotraw}^{tree}" 2>/dev/null || echo "$gotraw")
fi
if [ "$GOTTREE" = "$NEXT_TREE" ]; then
  ok "rawlsing_next tree matches: $NEXT_TREE"
else
  bad "rawlsing_next tree mismatch: got '${GOTTREE:-<none>}' expected $NEXT_TREE"
fi

# ---- 3. R7 interpreter identity -------------------------------------------
rec "[3] R7 interpreter / environment identity"
INTERP="$REPO/$INTERP_REL"
SHORT="$REPO/$SHORT_REL"
if [ ! -f "$INTERP" ]; then
  bad "R7 interpreter missing at $INTERP_REL"
else
  GOT=$(shasum -a 256 "$INTERP" 2>/dev/null | cut -d' ' -f1)
  if [ "$GOT" = "$INTERP_SHA" ]; then
    ok "interpreter sha256 matches: $INTERP_SHA"
  else
    bad "interpreter sha256 mismatch: got '$GOT' expected $INTERP_SHA"
  fi
  # the repaired short-name symlink must resolve to the same bytes
  if [ -e "$SHORT" ]; then
    S=$(shasum -a 256 "$SHORT" 2>/dev/null | cut -d' ' -f1)
    [ "$S" = "$INTERP_SHA" ] && ok "short-name symlink resolves to identical bytes" \
                             || bad "short-name symlink resolves to different bytes ('$S')"
  else
    bad "short-name interpreter path does not resolve (dangling symlink regression)"
  fi
  # interpreter must actually execute
  if "$INTERP" -c 'import sys; sys.exit(0 if sys.version_info[:2]==(3,11) else 1)' 2>/dev/null; then
    ok "interpreter executes and reports CPython 3.11"
  else
    bad "interpreter did not execute as CPython 3.11"
  fi
fi

# ---- 4. disk policy threshold (REQUIRED POLICY INPUT) ----------------------
rec "[4] disk capacity policy"
THRESH="${HQ_DISK_MIN_FREE_GIB:-}"
if [ -z "$THRESH" ]; then
  rec "  BLOCK  no adopted disk threshold. Governed evidence declares no source/output"
  rec "         size or execution write volume, so no number can be derived here."
  rec "         HQ must adopt a threshold and export HQ_DISK_MIN_FREE_GIB."
  rec "         required_disposition: HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED"
  THRESH_BLOCK=1
else
  THRESH_BLOCK=0
fi
AVAIL_KIB=$(df -k /System/Volumes/Data 2>/dev/null | awk 'NR==2{print $4}')
if [ -z "$AVAIL_KIB" ]; then
  bad "could not read free space for /System/Volumes/Data"
  THRESH_BLOCK=1
else
  rec "        measured free: ${AVAIL_KIB} KiB ($(awk -v k="$AVAIL_KIB" 'BEGIN{printf "%.2f", k/1048576}') GiB)"
  # measure three times: the blocker under repair is volatility, not a single number
  MIN_KIB=$AVAIL_KIB; MAX_KIB=$AVAIL_KIB
  for _ in 1 2 3; do
    s=$(df -k /System/Volumes/Data 2>/dev/null | awk 'NR==2{print $4}')
    [ -n "$s" ] || continue
    [ "$s" -lt "$MIN_KIB" ] && MIN_KIB=$s
    [ "$s" -gt "$MAX_KIB" ] && MAX_KIB=$s
  done
  rec "        sampled range: ${MIN_KIB}..${MAX_KIB} KiB (spread $((MAX_KIB-MIN_KIB)) KiB)"
  if [ "$THRESH_BLOCK" -eq 0 ]; then
    NEED_KIB=$(awk -v g="$THRESH" 'BEGIN{printf "%d", g*1048576}')
    rec "        adopted threshold: ${THRESH} GiB (${NEED_KIB} KiB)"
    # fail closed against the WORST sample, not the most favourable one
    if [ "$MIN_KIB" -ge "$NEED_KIB" ]; then
      ok "free space satisfies the adopted threshold on every sample"
    else
      bad "free space below adopted threshold on at least one sample: min ${MIN_KIB} KiB < required ${NEED_KIB} KiB"
    fi
  fi
fi

# ---- verdict ---------------------------------------------------------------
if [ "$FAIL" -eq 0 ] && [ "$THRESH_BLOCK" -eq 0 ]; then
  rec ""; rec "PREFLIGHT RESULT: PASS — all pinned identities verified and disk policy satisfied."
  rec "This authorises nothing by itself. It is a precondition check, not a warrant."
  RC=0
elif [ "$THRESH_BLOCK" -eq 1 ]; then
  rec ""; rec "PREFLIGHT RESULT: BLOCKED — HOST_PREFLIGHT_POLICY_THRESHOLD_REQUIRED"
  RC=3
else
  rec ""; rec "PREFLIGHT RESULT: BLOCKED — identity or capacity check failed."
  RC=2
fi

if [ $AS_JSON -eq 1 ]; then
  printf '{"schema":"HQ192_HOST_PREFLIGHT@1.0.0","result":"%s","exit":%s,"threshold_blocked":%s,"checks":[' \
    "$([ $RC -eq 0 ] && echo PASS || echo BLOCKED)" "$RC" "$THRESH_BLOCK"
  first=1
  for l in "${LINES[@]}"; do
    [ $first -eq 0 ] && printf ','; first=0
    printf '"%s"' "$(printf '%s' "$l" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  done
  printf ']}\n'
fi
exit $RC
