# P04-S0 — Exact native provenance and replay audit

Current code cut: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`. Owner: Browser Architecture HQ. Design only; no code, raw source or benchmark.

The current `_pre553_query_eval.py` retains full visited objects in `_UsedObjectAccumulator`; `_build_fact` later uses them for exact `.ref` provenance. The full C11 ReplayManifest is added to that list even though native I03 fact/replay uses its exact ref. Exact member refs, complete zero-inclusive cells, used authorities, and native negative detail are public identity material and cannot be dropped. Native source object validation stays unchanged. Sourcefree limited ref accumulator/evidence identity probes are local, not complete I03 parity. P04-S1 will require an I02-verified view-provided replay ref, exact used-ref ledger, once-only cell projection, unchanged native fact builders and independent old/new tests. No semantic rights are transferred.
