# R61-R08V R5 independent review — resume

State: review complete; verdict **REVISE**. Frozen R5 EXPECTATIONS is unchanged.
No candidate repair, self-adoption or author wake has occurred.

## Exact custody

- Branch: `agent/opencode-pyat-r61-r08v-r5-independent-review-r1`.
- Candidate/startup: `6abd49ffd9bb61925084036f2f1275841b3b5c83`.
- Code commit: `cfe3297e8962b3a11a62e9e89d26d7de50fadba5`; module blob
  `f3835b4add2f42d81a0f4b64f8df49398537edc9`; test blob
  `c0740589967d68dd29cfacf8d55490c5b4776f71`.
- Precode amendment: `5cdbaaecdcd3a1ecfee62025e4a0ca7f99e9b469`.
- Frozen R5 EXPECTATIONS commit: `732404d1bdb53d6eb25618bf806aa9fd68800291`.
- Prior R4 review preserved: `d1baa92cb457c30bf6dffb91f23f8cee351de4f6`.
- Reviewer return root:
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/`.

## Established

- Independent positive 54/6/60, changed 54/16/70, cold same-hash replay.
- R4 scalar/value and metadata mutations now typed-refuse; missing live producer
  pin is fail-closed (call count 0).
- Author suite 34/34; R4 immutable probe replay 7/8 passing controls plus two
  lawful `EvidenceAssociationError` old-defect failures.
- Remaining defect 1: the SAME reader derives `cache_trust_grade` from unsigned
  `result.provenance`; a public provenance mutation is accepted and served.
- Remaining defect 2: `export_cache` emits mutated evidence/query/rule object
  content under a valid envelope signature; the reader refuses the same object.
- Partial: verifier-only import/replay works, but re-export refuses with
  `cache entry lacks its admitted owner binding`.

## Next exact bounded task (author/owner, not this reviewer)

Repair only the two allowlisted paths: (1) sign the execution provenance/grade
or canonical execution mode in the envelope and compare it in the served
projection; (2) apply the reader's evidence/query/rule content checks in
`export_cache` or export only canonical objects. Complete the verifier-only
re-export path if the claimed import/export path requires it. Return a new
candidate and request a distinct hostile review.

## Commands to replay

```text
/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/probes/test_r08v_r5_independent_boundary.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/junit/reviewer_probes.xml

/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/junit/author_suite_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/probes/r4_immutable_probe.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r5/junit/r4_immutable_probe_replay.xml
```

Expected reviewer-probe result until the two missing functions are repaired:
6 passed / 2 failed; the failures are evidence, not harness errors.

## Boundaries

No candidate/self-repair, no author wake, no old product test assumption, no
J42/P41/E04 live integration claim, no source/science/prod/CI/N11/N12/Sorok/
J52/W52 authority, no subagent/session/provider/model/account change.
