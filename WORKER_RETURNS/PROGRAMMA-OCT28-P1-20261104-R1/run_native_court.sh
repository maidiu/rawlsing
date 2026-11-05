#!/usr/bin/env bash
set -euo pipefail
root=$1
fixture=$2
e3_suite=$3
e4_capture=$4
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
for cut in base p1; do
    destination="$root/evidence/native-$cut"
    mkdir -p "$destination"
    (
        cd "$root/$cut"
        export RAWLSING_C11_ACCELERATOR_DIR=""
        if [ "$cut" = p1 ]; then
            export RAWLSING_C11_ACCELERATOR_DIR="$root/pair-cache-final"
        fi
        python3 "$e4_capture" "$fixture/same-source.sav" "$destination"
    ) >"$root/evidence/native-$cut.log" 2>&1
done
cmp "$root/evidence/native-base/native.json" "$root/evidence/native-p1/native.json"
cmp "$root/evidence/native-base/checkpoint-0.json" "$root/evidence/native-p1/checkpoint-0.json"
(cd "$root/evidence"; shasum -a 256 native-*/{native,checkpoint-0}.json)
(
    cd "$root/p1"
    unset RAWLSING_C11_ACCELERATOR_DIR
    bash "$e3_suite"
    python3 -m pytest \
        rawlsing_next/tests/test_pre553_c11_execution_view.py \
        rawlsing_next/tests/test_pre553_route_b_production.py \
        rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
        rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py \
        rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py \
        -q -o addopts= -p no:cacheprovider
    RAWLSING_C11_ACCELERATOR_DIR="$root/pair-cache-final" python3 -m pytest \
        rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 \
        -q -o addopts= -p no:cacheprovider
) >"$root/evidence/regression.log" 2>&1
