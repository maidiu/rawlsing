# DDM Build Copy Runtime Transfer

This directory is the source-only transfer of the current `ddm_build_copy`
V550 through V552J implementation from the local Rawlsing working tree.

Included:

- Python implementation modules at this directory level;
- `authority/` runtime authority inputs;
- `bindings/` wave/source binding manifests;
- `manifests/` pipeline contracts and registries.

Excluded deliberately:

- respondent-level outputs and Parquet files;
- `reports/` generated response maps and run outputs;
- PostgreSQL data, caches, bytecode, backups, ZIP archives, and credentials.

The excluded response-option maps are large generated/runtime inputs and must
be transferred separately with their SHA-256 recorded before execution. This
branch is therefore the implementation and manifest transfer, not a claim
that it contains the respondent runtime substrate.
