# Rawlsing V550–V552J Repair — W06-B / G4 Launch

G3A and G3B are PASS. The integration branch now contains canonical V552 and V551J producer surfaces. W06-B is released to implement the V552J join. All work remains governed by `index.json`, `PROCEDURE.md`, `WORKER_PLAN.json`, and `GATE_STATUS.json` in this directory.

## W06-B — V552J

You are **W06-B**. Work only on branch `agent/v550-v552j-w06-v552j` and target your draft PR to `agent/v550-v552j-repair-integration`.

### Assigned mandatory issues

- `V552J-001` — remove fabricated/synthetic unknown primary-object behavior.
- `V552J-002` — missing/absent constraints must not become authoritative numeric zero aggregate scores.
- `V552J-003` — remove the duplicate `_first_nonempty` implementation from the effective V552J code path.
- `V552J-004` — structural matching must hard-filter exact producer/source/wave/country-or-shard identity before any semantic/fuzzy scoring; a score may never bridge a failed scope check.

Read the complete issue records and fingerprints from the canonical issue shards before editing. Read relevant `closed.json` and `deferred.json` entries so disproven behavior is not reintroduced.

### Write domain

Primary owned files:
- `data/ddm_build_copy/ddm_v552j_handoff.py`
- `data/ddm_build_copy/compile_v552j_structural_handoff.py`
- W06-namespaced V552J tests/fixtures only.

Do not edit V551/V551J/V552 semantic builders, W05 lineage/orchestration files, Section85, or issue-register governance.

### Frozen input contracts

Consume the **merged producer surfaces**, not legacy inferred readiness:

1. V552 is the canonical structural-pressure producer. Require its supported schema/compiler/shared boundary contract, producer `run_integrity_status=PASS`, exact producer run/scope identity, canonical manifest-declared Parquet artifacts, producer-declared post-serialization `artifact_file_sha256`, readability/schema validity, and exact row/count contract before semantic use.
2. V551J is the canonical joint-evidence producer. Require its supported schema/compiler/shared boundary contract, producer `run_integrity_status=PASS`, exact producer run/scope identity, manifest-declared canonical/compatibility artifacts as actually required by V552J, exact producer-declared serialized hashes, and typed evidence/downstream-permission state. Do not resurrect retired readiness booleans or nonempty-cardinality gates.
3. V552 and V551J must belong to one coherent inherited `run_id` and exact source/wave/country-or-shard scope before any join or structural match. Fail closed on disagreement.
4. Parquet remains mandatory canonical machine format for governed execution. CSV is diagnostic only.
5. Publication must be stale-safe/atomic. Reusing a run ID may not expose old V552J artifacts as current.

### Semantic rules

- Never fabricate an `UNKNOWN`, placeholder, or synthetic primary object merely because structural evidence is absent.
- Never map missing structural observations, absent constraints, no applicable joint evidence, unresolved upstream evidence, or missing scores to authoritative numeric `0`.
- Preserve the distinction among `OBSERVED_ZERO`, `NO_APPLICABLE_EVIDENCE`, and `APPLICABLE_BUT_UNRESOLVED`.
- A valid no-evidence/no-applicable V552J run may have `run_integrity_status=PASS`; evidence state and downstream permission are separate.
- Exact run/source/wave/country-or-shard identity is a prerequisite to structural matching. Only after exact scope identity passes may structural/semantic scoring rank candidates within that scope.
- If no exact-scope structural candidate exists, emit typed absence/unresolved state as appropriate; do not select a wrong-scope exact fact.
- Consume V552 pressure/status fields as produced; do not re-solve V551 scale geometry or V552 pressure formulas.
- Consume V551J neutral/low-support/repair-debt/no-joint-evidence semantics as produced; do not reinterpret packet certification from cardinality.
- Keep run integrity, evidence status, and downstream permission typed and separate using `rawlsing_pipeline_boundary_v1`.

### Cross-worker hooks

Implement the W06 stage-side hooks needed for `LIN-007`, `LIN-008`, `ORCH-007`, and `ORCH-008`, but do **not** edit W05-owned files. Record exact producer/consumer hook requirements in the worker report so W05 can close the end-to-end lineage/orchestration issues after G4.

### Required regression coverage

At minimum test:

- V552 + V551J correct producer manifests/hashes/versions/scope pass;
- tampered V552 or V551J artifact bytes fail before semantic use;
- wrong/unknown producer version or non-PASS integrity fails closed;
- cross-run, wrong-source, wrong-wave, wrong-country/shard joins fail closed;
- a wrong-scope candidate with a stronger semantic/exact-fact score can never beat an in-scope candidate or be selected when no in-scope candidate exists;
- no structural candidate yields typed absence, not a fabricated primary object;
- missing constraint observations do not become numeric zero;
- a true observed zero remains distinguishable from absence/unresolved;
- valid no-applicable/no-joint-evidence can remain integrity-PASS with the appropriate evidence/permission state;
- only one effective `_first_nonempty` definition remains;
- canonical output is Parquet and reused-run publication removes stale V552J outputs.

Run focused W06 tests plus syntax/import checks. If repository-wide execution is unavailable, state that truthfully and commit executable integration tests rather than claiming they ran.

### Return

Commit the completed W06-B work, open a **draft PR** against `agent/v550-v552j-repair-integration`, and return the exact `WORKER_PLAN.json` machine-readable worker report fields plus a concise terminal summary. All four assigned V552J issues must receive a terminal result; do not begin W06-C final regression work.
