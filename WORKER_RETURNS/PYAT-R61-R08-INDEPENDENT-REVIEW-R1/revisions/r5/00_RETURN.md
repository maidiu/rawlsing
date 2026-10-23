# R61-R08V R5 independent review — return

Verdict: **REVISE.** R5 closes the two exact R4 defects at the tested scalar/
field level: the SAME reader now refuses the former unsigned `consumer_values_read`
and metadata mutations, and a live resolver without `admitted_producer` refuses
before invoking a substituted callable. Genuine native positives, changed case,
cold replay and the main refusal controls remain live.

The complete signed/served projection is still not complete on two public paths:

1. **Unsigned provenance/grade is served.** `_result_matches_envelope` does not
   compare `EvidenceResult.provenance`, and `read()` derives
   `cache_trust_grade` from that unsigned field. A canonical result mutated to
   `AUTHENTICATED_CACHE` is accepted by the SAME reader and served with
   `cache_trust_grade=FULL_K_PRODUCER_ASSOCIATION_SHA256`; a cold cache result
   mutated to `CANONICAL_PRODUCER` is accepted and served with no cache grade.
   The signed envelope contains no provenance/execution-mode field to compare.
2. **Cache export emits unsigned evidence/query/rule content.** `export_cache`
   checks the scalar result fields but not `result.evidence_object`,
   `consumer_query_object` or `model_rule_object` against the signed envelope.
   A public in-place mutation of `evidence_object.geometry` (999) is refused by
   the SAME reader, yet `export_cache` emits an entry with that forged evidence
   under the valid envelope signature (downstream import then refuses).

## Custody actually checked

- Exact root/worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`
  (folder suffix historical; no alternate worktree).
- Branch: `agent/opencode-pyat-r61-r08v-r5-independent-review-r1`; preflight
  `pwd`/toplevel/branch/status matched and the tree was clean.
- Candidate/startup: `6abd49ffd9bb61925084036f2f1275841b3b5c83`.
- R5 code commit: `cfe3297e8962b3a11a62e9e89d26d7de50fadba5`.
- Module blob `f3835b4add2f42d81a0f4b64f8df49398537edc9`; test blob
  `c0740589967d68dd29cfacf8d55490c5b4776f71` (working tree matches).
- Precode amendment: `5cdbaaecdcd3a1ecfee62025e4a0ca7f99e9b469`;
  amendment blob `f83cdeef41ca40d81259241e923c74a313765963`.
- Frozen R5 EXPECTATIONS: `732404d1bdb53d6eb25618bf806aa9fd68800291`,
  committed before reading R5 candidate code or author conclusions.
- Prior R4 review: `d1baa92cb457c30bf6dffb91f23f8cee351de4f6`; preserved on the
  old branch/logs. The R4 probe was replayed from its exact blob
  `80b89a714da02a670c96a69f40706dd8d80df0b5`, unchanged.
- Candidate delta from `48a2eaf6d` is exactly the two allowlisted code/test paths
  plus the seven author R5 artifacts; the amendment commit adds only
  `REPAIR_AMENDMENT.md`. No native owner/evaluator/archived/HQ/workflow path
  changed.
- Author R5 manifest independently recomputed: all six listed artifacts match
  byte-for-byte; `manifest.json` is explicitly self-excluded.
- Native owner blobs independently re-hashed and unchanged:
  provider `23167aa2...`, composition `604c8d59...`, positioned evaluator
  `62e5eced...`, empirical objects `a61365b9...`, AT07/n10e fixture
  `0e384f72...`.
- Direct remote readback at start: `origin` R5 branch was at candidate
  `6abd49ffd9bb61925084036f2f1275841b3b5c83`.

## What R5 actually fixes

- R4 scalar/value mutation route: a `dataclasses.replace` of
  `consumer_values_read` denominator 999/cells/state/evidence ref and the former
  producer/uncertainty metadata mutations now raise `EvidenceAssociationError`
  at `reader.read()` and `e04_step()`; restoring the original signed result passes
  54/6/60.
- Missing live producer pin: `EvidenceResolver(admission_verifier=...,
  executor=...)` with no `admitted_producer` now binds but resolves
  `UNKNOWN/OWNER_ADMISSION_UNRESOLVED` with substituted-callable call count 0.
- Positive native controls: independent fixture-table counts 54/6/60 and changed
  54/16/70 are served by the SAME configured consumer with the actual unchanged
  provider/evaluator; cold fresh process reproduces `AUTHENTICATED_CACHE` 60 and
  the same consumer hash.
- No-config, wrong-root, attacker-issuer and cache forged-evidence/missing-
  envelope controls refuse; author suite replay is 34/34.
- R4 immutable probe replay: 7 passed, 2 failed; both failures are lawful
  `EvidenceAssociationError` refusals from the repaired path (the old probes
  expected the defective served 999 values). No TypeError/import/setup failure
  was counted as safety.

## Remaining defects and exact missing function

### R5-D3/D4-01 — provenance/grade is not in the signed served projection

Location: `_result_matches_envelope` (`pre553_universal_evidence_binding.py:2273`)
does not compare `result.provenance`; `read()` (`:2519`, `:2539`) adds
`cache_trust_grade` when `result.provenance == AUTHENTICATED_CACHE`. The envelope
has `trust_grade` but no execution provenance/mode field.

Reproducer: canonical `SUPPORTED` result -> `replace(result,
provenance="AUTHENTICATED_CACHE")` -> `reader.read()` succeeds and returns
`cache_trust_grade=FULL_K_PRODUCER_ASSOCIATION_SHA256`. Cold cache result ->
`replace(result, provenance="CANONICAL_PRODUCER")` -> `reader.read()` succeeds
and drops the cache grade. Observation:
`outcomes/r5_observations.json` key `provenance_grade_mutation`.

Minimal missing function: sign the execution provenance/grade (or a canonical
execution-mode/grade projection) in the envelope and compare it in
`_result_matches_envelope`; never derive a served trust label from unsigned
`result.provenance`.

### R5-D3-02 — cache export does not authenticate evidence/query/rule objects

Location: `export_cache` (`:1978`) checks `_result_matches_envelope` and the
envelope signature, but writes `_evidence_material(result.evidence_object)`,
`result.consumer_query_object.material()` and `result.model_rule_object.material()`
without checking their content/ref against the signed envelope. The reader
already performs those checks at `:2477` onward.

Reproducer: after a legitimate positive, mutate
`result.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999`
(public nested mapping); the SAME reader raises `EvidenceAssociationError`, but
`resolver.export_cache()` returns an entry whose `evidence` shows 999 under the
original envelope signature. A fresh configured resolver refuses the emitted
cache with `EvidenceCacheIntegrityError` ("envelope/evidence/query/rule
association mismatch"). Observation: `outcomes/r5_observations.json` key
`export_mutated_evidence_object`.

Minimal missing function: reuse the reader's evidence/query/rule content checks
in `export_cache` and refuse before emitting any entry (or export only canonical
objects derived from the signed/retained execution).

### Partial obligation — verifier-only re-export

A verifier-only resolver can import and replay an authenticated cold cache
(positive 60), but `export_cache()` on that imported resolver raises
`EvidenceCacheIntegrityError: cache entry lacks its admitted owner binding`.
This is not a served-value bypass, but the claimed resolver
import/export/replay path is incomplete. If re-export is required, retain the
imported binding in `_bindings` or build the export payload from
`_binding_materials` plus the signed envelope. Observation:
`outcomes/r5_observations.json` key `cold_process_positive` (`reexport`).

## Verdict boundary

The scoped callable grain is **not** fully qualified: the SAME configured
reader still serves a false provenance/grade, and the public export path emits
unsigned object content under a signed envelope. Reject
`ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING` until the
two missing functions above are repaired and re-reviewed.

Full live J42 `E41ProviderAdapter.step`, P41 progressive and repaired live E04
terminal remain NOT_REACHED. No original source/science, original-35/1890,
global F6/F7/F8, production/CI, N11/N12, Sorok, J52/W52, actor or protected-
capture authority is claimed. No candidate code/test, native owner, archived
return or HQ file was edited; no self-adoption or author wake.

Artifacts: `EXPECTATIONS.md` (frozen), `defects.md`, `limits.md`, `RESUME.md`,
`FACILITY_HISTORY.md`, `proof_witness.json`, `SHA256manifest.json`,
`outcomes/r5_observations.json`, `outcomes/r4_probe_replay_observations.json`,
`probes/test_r08v_r5_independent_boundary.py`, `probes/r4_immutable_probe.py`,
`junit/*.xml`, `logs/stdout.jsonl`. The harness log path `.r61/r5/stdout.jsonl`
is outside the reviewer edit root and was not written by this session.
