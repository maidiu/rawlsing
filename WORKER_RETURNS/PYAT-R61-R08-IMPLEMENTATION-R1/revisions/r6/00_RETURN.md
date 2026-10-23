# R61-R08 R6 implementation return

**Verdict: REVISE for full-progressive reach only. R6 closes the R5 provenance/grade and export-object bypasses at the shared authenticated projection, and completes verifier-only re-export. Positive native/evaluator/status/cold controls remain.**

## Custody

- Startup: `6abd49ffd9bb61925084036f2f1275841b3b5c83`
- R6 amendment commit (banked before code): `b9076985ec3be2ead1c47a2f754a52f774dfca59`
- R6 code commit: `7450b4f389e4a95a85066065dec7acafe83da84d`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- R5 review preserved: `4a5d9a9f8d700cbc5e692401220623df1122e22b`
- Writes only the two allowlisted code/test paths plus this `revisions/r6/` root.

## Repairs

### Signed provenance / delivery mode

`ExecutedEvidenceEnvelope@2` signs `execution_provenance=CANONICAL_PRODUCER` and
`execution_mode=LIVE_TRUSTED_EXECUTION`. Reader/e04 output now takes
`original_execution_provenance` and `original_execution_mode` from the signed
envelope. The only delivery label is explicitly
`local_delivery_context_unsigned` (`LIVE_TRUSTED_EXECUTION` or
`VERIFIED_REPLAY`). No served `cache_trust_grade` is derived from unsigned
`EvidenceResult.provenance`; cache transit cannot assert a new original
execution.

### Export completeness and verifier-only re-export

`export_cache` now applies the same evidence/query/rule content validation as
the reader (`_objects_match_envelope`) and refuses before emitting any entry with
mutated nested evidence/query/model content. It exports only the signed result
projection plus validated canonical objects. Verifier-only resolvers retain
imported owner/binding material and can re-export an imported authenticated cache
without live producer authority; the original envelope/signature is preserved
and the re-exported cache re-imports/reads at another verifier-only resolver.

Live producer pin remains mandatory; missing pin is fail-closed before call.
Cache/result/envelope versions advanced to `@4`/`@4`/`@2`; legacy records refuse.

## Preserved

Actual AT07 54/6/60, changed native 54/16/70, observed zero, ZERO_SUPPORT,
VALID_NULL/DIFFUSE/VALID_EMPTY/OBSERVED_ZERO states, Z UNRESOLVED16,
condition/typed/currentness identities, no-config/wrong-root/attacker-issuer/
forged-context/cache-forgery refusal and fresh-process cold replay remain.

## Tests

Command (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r6/junit.xml
```

**38 passed, 0 failed, 0 errors, 0 skipped, 9.64 s** (25 R08 tests + 13
unchanged C1 composition regressions).

Immutable R5 review probes: **6 passed, 2 failed as superseded old expectations**:
the provenance probe requires the now-removed unsigned `cache_trust_grade` key;
the export probe asserts `import_refused` even when export already refused.
Successor R6 tests assert signed original provenance, no unsigned grade, export
refusal for mutated evidence/query/rule, and verifier-only re-export/cold
round-trip. No archived probe was edited.

## Reach and limits

Covered: signed trusted-host admission, actual provider/evaluator/consumer,
complete signed projection, export/import/replay, verifier-only re-export,
fail-closed live pin, status reduction. NOT_REACHED: live J42/P41/E04; archived
returns unedited.

No original data/source/science, production/CI, N11/N12, F6/F7/F8, actor, Sorok,
J52/W52 or protected-capture authority is issued. Same-UID host/key compromise,
ptrace/root and dishonest competent issuer remain outside the scoped threat
model. Author validation only; distinct R6 hostile reviewer not launched or
self-adopted.
