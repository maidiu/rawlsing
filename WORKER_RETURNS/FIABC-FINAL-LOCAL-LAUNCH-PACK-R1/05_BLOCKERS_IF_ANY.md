# FIABC FINAL LOCAL LAUNCH PACK — R1
## Exact blockers and smallest deterministic repairs

Measured P2X MUST NOT start from integrated head `858b3b52674044e020b85f8697c5f2c61ce15371`.

### B01 — S16/S17 metric constitution is 29/35

**Defect:** `fiabc_terminal_completeness.py` omits six telemetry metrics now frozen by the 35-field registry.

**Smallest repair:** add exactly the six fields listed in `01_INTEGRATED_STATIC_AUDIT.md` to `FROZEN_DISPOSITIVE_METRICS`; add the S10/S11/S15 stage bindings for lifecycle-grain fields; leave Candidate-A `delete_rebuild_wall_ns` typed-N/A law unchanged. Add a hostile assertion:

`set(FROZEN_DISPOSITIVE_METRICS) == set(METRIC_DEFINITIONS)`

Do not change any metric definition.

### B02 — WVS successor Lock2 has not succeeded the live parity-oracle constitution

**Defect:** current runtime and manifests use successor `5e2a53... / 9b5ac1... / 3aee360...`; `pre553_independent_parity_oracle.py` and T5 `_court_constitution()` still use predecessor `8e5842... / b1aa43... / 245916...`.

**Smallest repair:** succeed only those frozen WVS constitution identities in the live oracle module to the already-adopted successor values. Candidate grammar, 46-candidate hash stream, family shape, risk set, measure basis, workload semantics and source identity remain unchanged. Re-run source-free oracle/T5 tests.

### B03 — accepted R1M WVS oracle is not in the schema the live T3/T5 loader consumes

**Defect:** accepted document:
`WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json`
has schema `FIABC_LM2_R1M_FRESH_WVS_ORACLE@1.0.0`. The live court requires `RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`.

**Smallest repair:** add one source-free deterministic adapter/launcher that consumes only the accepted R1M truth payload and already-frozen successor authority, maps it to the existing `WVS_MATERIALIZER_CONTRACT` shape, and calls the existing `freeze_wvs7_oracle_from_common_material()`. It must not reopen WVS bytes or inspect candidate output. Bind the resulting standard oracle identity/document SHA into the final T3 freeze and current launch control artifacts. Do not silently treat the R1M wrapper as the standard T5 oracle.

### B04 — current failure receipt still serializes predecessor WVS authority

**Defect:** active backend `_cell()` reads `WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json`; its Lock2 is `8e5842...` and DiscoveryAuthority `245916...`.

**Smallest repair:** make current failure serialization derive the authority identity from the current six-cell manifest/current court contract (or refresh one exact successor-bound expectation object consumed by `_cell()`). A WVS successor-court failure must name successor Lock2 `5e2a53...` and must not emit predecessor authority metadata. Keep manifest-derived six-cell sequence indexing intact.

### B05 — LiTS exact current T5 oracle has no committed local producer CLI

HQ already proved source-free 50/77 frontier shape and accepted product/replay. It explicitly records three missing current pieces:

- `CURRENT_STANDARDIZED_CONSTITUENT_I03_FACT_REFS`
- `CURRENT_CONSTITUENT_I03_CLOSURE_IDENTITY`
- `CURRENT_OBSERVATION_SHAPED_EXACT_REF_MANIFEST`

**Smallest repair:** add one candidate-neutral local producer that uses the exact LiTS source plus accepted common semantic/runtime authority to materialize those current I03/I05 observation surfaces, then calls existing `build_lits_i_oracle()` / `freeze_oracle()`. It must start zero A/B/C processes and consult zero candidate-owned roots. The existing source-free frontier probe is not this producer.

### B06 — final two-source T3 freeze receipt has validator but no producer

**Defect:** `ee_p2x_candidate_process_envelope.load_frozen_upstream_receipt()` consumes `RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`; no final CLI builds it.

**Smallest repair:** deterministic pre-candidate producer that seals, in order:
1. exact LiTS/WVS source roots;
2. accepted authority/workload identities;
3. exact standard LiTS and WVS oracle identity + document path + document SHA;
4. `candidate_outputs_seen = 0`;
5. `candidate_owned_roots_consulted = []`;
6. `state = FROZEN_READ_ONLY`.

Self-validate with `load_frozen_upstream_receipt()` before returning.

### B07 — current-head I07 manifest and P10 lifecycle context have evaluator but no real producer

**Defect:** `fiabc_succession_preflight.py` can evaluate a manifest/context, and driver `--preflight` can seal the T5 receipt, but no committed final producer emits the real current-head manifest and lifecycle context.

**Smallest repair:** deterministic pre-candidate producer using the existing succession schema/governing profile and current accepted evidence. It must set `manifest_identity.generated_from_commit_sha` to the exact final launch head and `frozen_before_candidate_execution = true`; emit the governed P10 lifecycle/failure-scope context; then run the existing evaluator. No candidate process.

### B08 — execution branch must be lawfully advanced to the final launch head

Driver/current manifest require:
`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`.

Its remote tip `617c9c9426db12a3c0f7fea6b68a582c10759553` is an ancestor of integrated `858b3b5...` (224 commits behind, zero ahead). This is therefore a branch-pointer/control-plane issue, not a required rebase.

After B01-B07 are repaired and a final launch head is sealed, **fast-forward the existing execution branch** to that head. Do not rebase and do not create a substitute execution branch. Then regenerate this launch pack against that exact head.

## Non-blocker

Variable-width/projection narrowing is expressly non-blocking. Full-width decode is accepted for this court.

## Required order after repair

1. final source-free qualification at the repaired exact head;
2. fast-forward existing P2X execution branch to that exact head;
3. exact host/runtime and source SHA preflight;
4. candidate-neutral LiTS + standard WVS oracle freeze;
5. two-source T3 freeze receipt;
6. current-head succession manifest + P10 context;
7. driver `--preflight`;
8. one serialized driver `--run`;
9. no P3/final architecture selection until the six-cell court terminal is recorded.
