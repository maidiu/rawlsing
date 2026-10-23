# R61-R08V R6 independent review — resume

State: review complete; verdict **REVISE**. Frozen R6 EXPECTATIONS is unchanged.
No candidate repair, self-adoption or author wake has occurred. R01 High
adjudication was not inspected or decided.

## Exact custody

- Branch: `agent/opencode-pyat-r61-r08v-r6-independent-review-r1`.
- Candidate/startup: `d8a7b4005d23a1e39b35360ca96bf2aef5b9e591`.
- Code commit: `7450b4f389e4a95a85066065dec7acafe83da84d`; module blob
  `ad165eba9d04644f4b5ab34cd9e52ea1cf9b0ebe`; test blob
  `576142c525e140fdfcd34af3949b5bf68ff2386f`.
- Precode amendment: `b9076985ec3be2ead1c47a2f754a52f774dfca59`.
- Frozen R6 EXPECTATIONS: `57ce687fefca959fa736abeb822a87c3060521d9`.
- Prior R5 review preserved: `4a5d9a9f8d700cbc5e692401220623df1122e22b`;
  R4 review preserved: `d1baa92cb457c30bf6dffb91f23f8cee351de4f6`.
- Reviewer return root:
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/`.

## Established

- Independent positive 54/6/60, changed 54/16/70, cold same-hash replay.
- Signed original provenance/mode served; no unsigned `cache_trust_grade`.
- Export refuses mutated evidence/query/rule objects; restoring each restores
  export/read at 60.
- Verifier-only re-export round-trip: live export -> import/read -> re-export ->
  second import/read, same envelope signature and 60.
- Missing live producer pin call count 0; no-config/wrong-root/attacker-issuer/
  cache-forgery/old-schema/old-envelope refusals.
- Author suite 38/38; R4 probe 7/2 lawful old-defect failures; R5 probe 6/2
  superseded old expectations.
- Remaining defect: cache `producer_binding` top-level metadata and producer
  admission token are not authenticated against the signed owner identity
  material; altered producer query/admission survives import and verifier-only
  re-export at 60.

## Next exact bounded task (author/owner, not this reviewer)

Repair only the two allowlisted paths: at cache import, cross-check the
duplicated producer-binding fields against the signed `owner_identity_material`
(or reconstruct them) and verify/drop the producer admission; at export, rebuild
the binding payload from authenticated owner material and refuse inconsistent
retained records. Keep the signed envelope/owner material as sole authority.
Then return a new candidate and request a distinct hostile review.

## Commands to replay

```text
/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/probes/test_r08v_r6_independent_boundary.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/junit/reviewer_probes.xml

/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/junit/author_suite_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/probes/r4_immutable_probe.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/junit/r4_immutable_probe_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/probes/r5_immutable_probe.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r6/junit/r5_immutable_probe_replay.xml
```

Expected reviewer-probe result until the remaining function is repaired:
10 passed / 1 failed; the failure is the recorded cache binding metadata defect.

## Boundaries

No candidate/self-repair, no author wake, no old product test assumption, no
J42/P41/E04 live integration claim, no source/science/prod/CI/N11/N12/Sorok/
J52/W52/R03/R09 authority, no R01 inspection, no subagent/session/provider/model/
account change.
