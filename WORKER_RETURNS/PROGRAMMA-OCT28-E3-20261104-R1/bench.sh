#!/usr/bin/env bash
set -eu
packet=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$1" && pwd)
e1=$(cd "$2" && pwd)
e1_impl=$(cd "$3" && pwd)
profile="$e1/WORKER_RETURNS/PROGRAMMA-OCT28-E1-20261104-R1/profile_oct28.py"
fixture=$(dirname "$profile")
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
cd "$root"
mkdir -p "$root/evidence"
test "$(git -C "$root/base" rev-parse HEAD)" = ba165a6a073dfdac0cb2e993ab8111ebb5ef404c
test "$(git -C "$root/e3" rev-parse HEAD)" = 43d2b70ebae4d183aadbd9694624575857fd100f
test "$(git -C "$e1_impl" rev-parse HEAD)" = 4bd17accf0104ac05167c40a43076606e13c8448
test "$(git -C "$e1" rev-parse HEAD)" = cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8
shasum -a 256 "$fixture/same-source.sav" "$profile" >"$root/evidence/inputs.sha256"
printf '%s  %s\n' c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b "$fixture/same-source.sav" | shasum -a 256 -c -
run() {
    local cut="$1" output="$2"
    shift 2
    local checkout="$root/$cut"
    if [ "$cut" = e1 ]; then checkout="$e1_impl"; fi
    printf '%s\n' "$output"
    (cd "$checkout"; python3 "$profile" "$@" >"$root/evidence/$output.json" 2>"$root/evidence/$output.stderr")
}
# All joined processes start with no live I03 cache. Each contains reuse and
# the actual checkpoint capture, resume and P41 reader.
run base base-joined joined "$fixture" --instrument
run e3 candidate-joined joined "$fixture" --instrument
run e3 candidate-joined-repeat joined "$fixture" --instrument
run base base-joined-repeat joined "$fixture" --instrument

for rounds in 1 8; do
    run base "base-queries-$rounds" queries "$fixture" --instrument --rounds "$rounds"
    run e3 "candidate-queries-$rounds" queries "$fixture" --instrument --rounds "$rounds"
done
run base base-queries-150 queries "$fixture" --rounds 150
run e3 candidate-queries-150 queries "$fixture" --rounds 150

# E1 and E3 topology builds both equal six in the joined workload. Compare
# warm query overhead separately, reversing process order on the second pair.
run e1 e1-warm-a queries "$fixture" --rounds 150
run e3 e3-warm-a queries "$fixture" --rounds 150
run e3 e3-warm-b queries "$fixture" --rounds 150
run e1 e1-warm-b queries "$fixture" --rounds 150

(cd "$root/e3"; python3 "$packet/profile_attestation.py" "$profile" queries "$fixture" --instrument --rounds 150 >"$root/evidence/e3-attestation-queries.json")
