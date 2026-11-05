#!/usr/bin/env bash
set -euo pipefail
root=$1
fixture=$2
packet=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
test "$(git -C "$root/base" rev-parse HEAD)" = f58c8400a024d108a8ab9fa814c87967d336ea47
test "$(git -C "$root/p1" rev-parse HEAD)" = 0a63e7c90cabcfd01dbb169d477f2d0ead5be22c
git -C "$root/base" diff --quiet HEAD -- rawlsing_next
git -C "$root/p1" diff --quiet HEAD -- rawlsing_next
cache="$root/pair-cache-final"
mkdir -p "$root/evidence"
test ! -e "$cache"
printf '%s  %s\n' c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b "$fixture/same-source.sav" | shasum -a 256 -c -
run() {
    local cut=$1 label=$2 storage=$3
    printf '%s %s\n' "$cut" "$label"
    (
        cd "$root/$cut"
        RAWLSING_C11_ACCELERATOR_DIR="$storage" python3 "$packet/profile_p1.py" \
            "$fixture/profile_oct28.py" "$fixture"
    ) >"$root/evidence/$label.json" 2>"$root/evidence/$label.stderr"
}
run base base-a ""
run p1 compact-cold "$cache"
run p1 compact-warm "$cache"
run base base-b ""
for member in "$cache"/c11-events-*.parquet; do
    printf 'torn Parquet member' >"$member"
done
run p1 compact-corrupt "$cache"
for member in "$cache"/c11-events-*.parquet; do
    unlink "$member"
done
run p1 compact-deleted "$cache"
