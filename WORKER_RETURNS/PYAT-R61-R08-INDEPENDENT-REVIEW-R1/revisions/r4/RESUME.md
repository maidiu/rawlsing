# R61-R08V R4 independent review — resume

State: review complete, verdict **REVISE**. Frozen EXPECTATIONS is unchanged.
No candidate repair, self-adoption or author wake has occurred.

## Exact custody

- Branch: `agent/opencode-pyat-r61-r08v-r4-independent-review-r1`.
- Candidate/startup: `48a2eaf6d3c653e2efe40643c427f28c47cd744b`.
- Frozen EXPECTATIONS: `4cf30eee34891f269bed95294e3f31ef80c0b2d5`.
- Code commit: `3c69a13e64dd2bca65858906a367347e895f9d82`; code blob
  `c3b039fd908c20b6494a2bcf37b89d878dfaf6c6`; test blob
  `1f72a428283eb35d7bcedf5391528dbcbd22a489`.
- Reviewer return root:
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r4/`.

## What is already established

- Independent positive 54/6/60, changed native case 54/16/70, cold same-hash
  replay, no-config/wrong-root/attacker-issuer/cache-forgery refusals.
- Author suite replay 31/31.
- Decisive defect: the SAME reader accepts a publicly replaced
  `consumer_values_read` and result metadata after signing; it serves forged
  999 denominator/cells/evidence ref/state while the signed envelope says 60.
- Secondary defect: `admitted_producer` is optional and fails open; a copied
  admission plus a substituted callable executes when it is omitted.

## Next exact bounded task (author/owner, not this reviewer)

Repair only the two allowlisted paths: bind every served result field and the
complete `consumer_values_read` to the signed `ExecutedEvidenceEnvelope` (or
reconstruct output only from the envelope), and make the admitted producer
callable pin mandatory/fail-closed. Then return a new candidate and request a
distinct hostile review. Do not treat this review as a repair or adoption.

## Commands to replay this review

```text
/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r4/probes/test_r08v_r4_independent_boundary.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r4/junit/reviewer_probes.xml

/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r4/junit/author_suite_replay.xml
```

The reviewer probe suite is expected to show 6 passed / 3 failed until the two
missing functions above are repaired. The failures are evidence, not harness
errors.

## Non-negotiable boundaries

No candidate/self-repair, no author wake, no old product test assumption, no
J42/P41/E04 live integration claim, no source/science/prod/CI/N11/N12/Sorok/
J52/W52 authority, no subagent/session/provider/model/account change.
