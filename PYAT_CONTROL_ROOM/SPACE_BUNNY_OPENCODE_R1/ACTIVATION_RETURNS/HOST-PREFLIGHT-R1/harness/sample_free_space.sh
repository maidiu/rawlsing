#!/bin/bash
# HQ192 — repeated free-space sampling for HOST-PREFLIGHT-F3-DISK-CAPACITY-VOLATILITY.
# Read-only. Samples one volume at an interval and reports min/max/spread and the
# largest observed single-interval delta, which is the quantity that actually
# breaks a live run: not the average level but the rate of change.
set -u
VOL="${1:-/System/Volumes/Data}"
N="${2:-24}"
INTERVAL="${3:-5}"
prev=""; min=""; max=""; maxdelta=0; i=0
samples=""
while [ "$i" -lt "$N" ]; do
  k=$(df -k "$VOL" | awk 'NR==2{print $4}')
  [ -z "$k" ] && { i=$((i+1)); sleep "$INTERVAL"; continue; }
  [ -z "$min" ] && { min=$k; max=$k; }
  [ "$k" -lt "$min" ] && min=$k
  [ "$k" -gt "$max" ] && max=$k
  if [ -n "$prev" ]; then
    d=$((k-prev)); [ "${d#-}" -gt "${maxdelta#-}" ] && maxdelta=$d
  fi
  samples="${samples}${k}\n"
  prev=$k
  i=$((i+1))
  [ "$i" -lt "$N" ] && sleep "$INTERVAL"
done
gib() { awk -v k="$1" 'BEGIN{printf "%.2f", k/1048576}'; }
echo "volume            : $VOL"
echo "samples           : $N every ${INTERVAL}s"
echo "min free          : ${min} KiB ($(gib "$min") GiB)"
echo "max free          : ${max} KiB ($(gib "$max") GiB)"
echo "total spread      : $((max-min)) KiB ($(gib $((max-min))) GiB)"
echo "largest 1-interval delta: ${maxdelta} KiB ($(gib ${maxdelta#-}) GiB)"
echo
echo "series (KiB):"
printf "$samples"
