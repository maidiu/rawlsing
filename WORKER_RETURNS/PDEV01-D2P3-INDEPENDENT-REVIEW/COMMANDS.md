# Exact PDEV01 commands

All candidate execution used a disposable snapshot, never the candidate worktree.

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-hq-bounded-independent-review-20261103
SNAP=$(mktemp -d /private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pdev01.XXXXXX)
git archive cfe7dc6111afcb8eda26eb9a54f6cad43b6d1584 | tar -x -C "$SNAP"
R="$SNAP/WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-PRODUCER-READER-LINEAGE-R1"
O="WORKER_RETURNS/PDEV01-D2P3-INDEPENDENT-REVIEW"

# New full suite
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R:$SNAP" python3 -m pytest \
  "$R/new/tests/test_d2p3_single_registry.py" -q -p no:cacheprovider -o addopts='' \
  > "$O/new13.log" 2>&1

# Adapted seven selected node IDs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R:$SNAP" python3 -m pytest \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_01_exact_producer_refs_are_dereferenced_and_native_numbers_read" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_02_reader_dependency_readset_is_exact_produced_refs_only" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_03_mutated_exported_field_ref_is_denied_not_self_rehashed" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_04_forged_issuer_signature_cannot_pass_producer_or_reader" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_05_wind_cannot_be_renamed_hydro_turbine_at_same_totals" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_06_producer_refuses_wrong_person_mobile_unit_before_emission" \
  "$R/new/tests/test_d2p3_single_registry.py::test_new_07_publisher_and_source_family_identity_are_verified" \
  -q -p no:cacheprovider -o addopts='' > "$O/adapted7.log" 2>&1

# Preserved original seven negative oracles (expected 7 failed RED)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R/repro" python3 -m pytest \
  "$R/repro/d2r_original/test_d2r_required_integrity_red.py" -q -p no:cacheprovider -o addopts='' \
  > "$O/original7_red.log" 2>&1

# Actual direct transport
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R:$SNAP" python3 \
  "$R/new/d2p/direct_trace.py" "$R/repro/n9c_fields.json" \
  > "$O/direct_trace.stdout.json" 2> "$O/direct_trace.stderr.log"

# Producer/reader witness
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R:$SNAP" python3 - "$R/repro/n9c_fields.json" \
  ... > "$O/PRODUCER_READER_WITNESS.json"
```

The witness script is recorded in the review transcript; `PRODUCER_READER_WITNESS.json` contains its measured output.
