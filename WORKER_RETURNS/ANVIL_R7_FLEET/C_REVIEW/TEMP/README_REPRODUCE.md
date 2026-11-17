# Reproduction of the C-review witnesses

The review root commits only the scripts, result JSON and raw logs; it does not
commit a duplicate extraction of the candidate ZIP. To re-run any witness:

```bash
cd /Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW
mkdir -p WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP
unzip -q WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/REPAIRED_PACKAGE.zip \
  -d WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP/COLD_$(date -u +%Y%m%dT%H%M%SZ)
cd WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW
python3 WITNESS/w0_source_replay.py
python3 WITNESS/w1_req_f6_hollow.py
python3 WITNESS/w2_c_boundary_false_science.py
python3 WITNESS/w3_builder_receipt.py
python3 WITNESS/w4_source_negative_tamper.py
python3 WITNESS/w5_terminal_graph.py
python3 WITNESS/w6_projection_no_loss.py
python3 WITNESS/w7_joint_denominator.py
python3 WITNESS/w8_omission_controls.py
```

The witness scripts select the newest `TEMP/COLD_*` extraction for the candidate
tool modules. They read the candidate `INTEGRATION/` root but never write there.
The exact external pins are the shared Git store
`/Users/matthewsmith/s2b-work/rawlsing` and
`/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip`;
no author worktree or hidden checkout is used.

For the literal cold-handoff failure reproduction, see
`RAW_COMMANDS.md` §3 and `LOGS/handoff_clean_inventory.log` /
`LOGS/handoff_clean_13.log`.
