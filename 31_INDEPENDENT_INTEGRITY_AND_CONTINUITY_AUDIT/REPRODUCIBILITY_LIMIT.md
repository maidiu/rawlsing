# Reproducibility boundary

The delivered final artifacts are fully inspectable, hashable, and structurally verifiable. The v2 source packages include catalogs, rulings, guards, review queues, structures, source references, correction ledgers, validation outputs, and provenance records.

The historical rebuild scripts are not a self-contained replay environment. They contain hard-coded transient paths (`/mnt/data/work_calibre`, `/mnt/data/handoff_v9_audit`, and `/mnt/data/audit_four`), and those pre-build working directories / original v1 sweep inputs are not delivered as a reconstructible working tree. Therefore:

- the final v2 artifacts can be audited and used as the governing restart state;
- the exact historical build process cannot be replayed from this package alone without reconstructing the missing transient input layout;
- claims that the historical rebuild scripts alone provide fully self-contained deterministic reconstruction are too strong;
- `verify_handoff_v11.py` provides self-contained read-only verification of the delivered state, not regeneration of the historical state.

This limitation does not erase or invalidate the completed source-local work. It limits provenance depth and replayability. Any later provenance-hardening pass should parameterize those scripts, include an input manifest with source hashes, and preserve the pre-build authority inputs or a deterministic acquisition recipe.
