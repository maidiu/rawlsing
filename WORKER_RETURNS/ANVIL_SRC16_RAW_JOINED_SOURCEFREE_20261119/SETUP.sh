#!/bin/sh
set -eu
A=/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117
S=${1:?isolated scratch path}
rm -rf "$S"
mkdir -m 700 -p "$S"
cp -a "$A/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree/rawlsing_next" "$S/rawlsing_next"
cd "$S"
patch -p0 < "$A/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC16_RAW_JOINED_SOURCEFREE_20261119/patches/01_handoff_raw_lane.patch"
patch -p0 < "$A/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC16_RAW_JOINED_SOURCEFREE_20261119/patches/02_query_predicate_guard.patch"
patch -p1 < "$A/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC16_RAW_JOINED_SOURCEFREE_20261119/patches/03_i05_unresolved_repair.patch"
patch -p1 < "$A/IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC16_RAW_JOINED_SOURCEFREE_20261119/patches/04_saved_batch_prior_cache.patch"
python3 -m py_compile rawlsing_next/pre553_source_i02_handoff.py rawlsing_next/_pre553_query_predicate.py rawlsing_next/pre553_discovery_exact.py rawlsing_next/pre553_saved_workload_integration.py
