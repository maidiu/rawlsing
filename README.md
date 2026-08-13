# Rawlsing V550+ Pipeline

This repository is a curated source transfer of the existing V550 through
V552J implementation. It contains runtime Python code, SQL/schema-adjacent
inputs, authority registries, manifests, CSV crosswalks, validation code, and
tests.

It intentionally excludes generated output trees, run logs, respondent-level
data, database files, archives, caches, virtual environments, and environment
files. The pipeline expects its runtime data and database connection to be
provided by the receiving environment.

## Layout

- `data/ddm_build_copy/`: V550 through V552J implementation and runtime manifests
- `section85/code/`: bounded diagnostic runners and authority builders
- `section85/authority/`: bounded authority registries and binding manifests
- `section85/validation/`: validation and reproduction utilities

This is a source transfer, not a claim that every included stage has passed a
full production run.
