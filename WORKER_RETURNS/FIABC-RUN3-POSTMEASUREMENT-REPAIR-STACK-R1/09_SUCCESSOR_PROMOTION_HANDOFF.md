# Successor handoff to HQ

The source-free RUN3 repair stack and current-head succession provenance closure are ready for HQ review on `agent/codex-fiabc-run3-postmeasurement-repair-stack-r1`.

- PRE-MAIN base: `36dbab16e8a82083de54dfc1e1e8228b50fe5b63`.
- Exact source-free-qualified implementation head: `3d8f2ad62600b6777dcb23a28404a067502e77a0` (parent `a0e20d561310ed9f9fedeb4996eb733316a8bd80`).
- New provenance requirement: the generated succession manifest carries all four repaired direct execution dependencies under `current_head_bindings.required_files`; the current preflight resolves each ref at the exact generated head and checks Git blob/content identity.
- Complete prior repair suite: 115/115 passed. Succession producer/preflight regressions: 24 tests and 28 subtests passed.
- Actual source-free producer and preflight on a fresh clean checkout of `3d8f2ad62600b6777dcb23a28404a067502e77a0`: PASS, 11/11 preflight checks, no failure codes, candidate processes/outputs 0/0, no candidate-owned roots.
- Frozen A/B owner blobs, C policy blob, T2/T3/T5, stop, source/oracle identities, metrics, cell order, representation authority, and accepted C11 release/replay identities remain unchanged; see `07_NO_GOVERNED_DRIFT.json`.
- PRE-MAIN remains `36dbab16e8a82083de54dfc1e1e8228b50fe5b63`. Protected measured execution remains `bc832181b4284ac110d2be44fc83504e04de081e`.

HQ should review and, if adopted, promote through the normal succession/preflight path. This return does not authorize a new measured run, RUN4, P2 synthesis, or P3. Preserved RUN3 evidence remains immutable.
