# CUSTODY INCIDENT — C_REVIEW witness output paths

**Incident:** During the R2 repair, this author copied five independent-C witness scripts into its own `R2_C_WITNESS/` directory but initially left the copies' `ROOT`/`OUT` paths pointing at the read-only C_REVIEW worktree. Running them caused writes to C_REVIEW witness output paths (result JSONs and temporary `w*_*` directories).

**Files/paths affected by the commands:** `C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W1_REQ_AND_F6_HOLLOW/`, `W2_C_BOUNDARY_FALSE_SCIENCE/`, `W4_SOURCE_NEGATIVE_TAMPER/`, `W5_TERMINAL_GRAPH/`, `W6_PROJECTION_NO_LOSS/` (result files and untracked temp dirs).

**What this author did NOT do:** no repair, restore, stage, commit, reset or deletion in C_REVIEW; no protected/reviewer branch write; no claim that the original review was legitimately altered. At the last read, tracked C_REVIEW witness files matched frozen HEAD `6c70839a6a1ed4dd4dd15cd709c92a379e589178`; untracked `w1_*`, `w2_*`, `w4_*` temp dirs remained. HQ must inspect/restore its own root.

**Exact raw commands (abridged, run from INTEGRATION return root):**

```
# copied C witness scripts to R2_C_WITNESS/, replaced INT and COLD with absolute paths,
# but initially left ROOT/OUT pointing at C_REVIEW:
python3 R2_C_WITNESS/w1_req_f6_hollow.py
python3 R2_C_WITNESS/w2_c_boundary_false_science.py
python3 R2_C_WITNESS/w4_source_negative_tamper.py
python3 R2_C_WITNESS/w5_terminal_graph.py
python3 R2_C_WITNESS/w6_projection_no_loss.py
```

**Correction:** all copies were edited so `ROOT`/`OUT` resolve under `INTEGRATION/R2_C_WITNESS_OUTPUT/`; `grep -R "ROOT/'WORKER_RETURNS" R2_C_WITNESS/*.py` returns no match. Rerun outputs are under `R2_C_WITNESS_OUTPUT/` only. W1/W2/W4/W5 now return `WITNESS_REFUTED`; W6 returns `REVIEW` with 43/58 graph and full projection fields. No peer root was written after the correction.

**Preserved:** original integration `0f0c673f…`; frozen review `6c70839a…`.
