#!/usr/bin/env bash
set -eu
root=$1
evidence=$root/evidence
profile=$root/inputs/e1/profile_oct28.py
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
printf '%s  %s\n' c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b "$root/inputs/e1/same-source.sav" | shasum -a 256 -c -
for pair in base:ba165a6a073dfdac0cb2e993ab8111ebb5ef404c e1:4bd17accf0104ac05167c40a43076606e13c8448 e3:43d2b70ebae4d183aadbd9694624575857fd100f; do
    cut=${pair%:*}
    test "$(git -C "$root/$cut" rev-parse HEAD)" = "${pair#*:}"
    test -z "$(git -C "$root/$cut" status --porcelain --untracked-files=no)"
done
run() {
    local cut=$1 label=$2
    shift 2
    printf '%s %s\n' "$cut" "$label"
    (cd "$root/$cut"; python3 "$profile" "$@" "$root/inputs/e1") >"$evidence/$label.json" 2>"$evidence/$label.stderr"
}
run base joined-base-a joined --instrument
run e3 joined-e3-a joined --instrument
run e3 joined-e3-b joined --instrument
run base joined-base-b joined --instrument
for rounds in 1 8; do
    for cut in base e1 e3; do
        run "$cut" "queries-$cut-$rounds" queries --instrument --rounds "$rounds"
    done
done
run e1 warm-e1-a queries --rounds 150
run e3 warm-e3-a queries --rounds 150
run e3 warm-e3-b queries --rounds 150
run e1 warm-e1-b queries --rounds 150
(cd "$root/e3"; python3 "$root/inputs/e3/profile_attestation.py" "$profile" queries "$root/inputs/e1" --instrument --rounds 150) >"$evidence/attestation.json" 2>"$evidence/attestation.stderr"
