# R61-R08V R7 independent review — resume

State: review complete; verdict **REVISE** for one bounded legacy-pin refusal
code. Frozen R7 EXPECTATIONS unchanged. No candidate repair, adoption, author
wake or new session.

## Custody

- Branch: `agent/opencode-pyat-r61-r08v-r7-independent-review-r1`.
- Candidate/startup: `ea39bd324d297a93bb9e87ede9b9da75dfa8750a`; code
  `992236d245e165dcf5842411ad0a4733433fd7de`.
- Module blob `00312f84...`; test blob `0dae1230...`; frozen EXPECTATIONS
  `17484296abb50e2f24775db53d7765cdbe10dab1`.
- Prior R6 review `c42b4abee...`; R5/R4 preserved.
- Reviewer return root:
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/`.

## Established

- R61AF normal form, 13 owner classes, no admission/duplicate transport,
  descriptor pins, legacy schema refusal, unknown-field refusal.
- Independent positive 54/6/60, changed 54/16/70, observed-zero/ZERO_SUPPORT,
  typed/currentness/Z UNRESOLVED16.
- Verifier-only import/read/re-export/second import and cold process 60, same
  envelope signature/provenance, no producer invocation.
- Missing live pin counter 0; wrong root/no config/attacker issuer/cache forgery
  refusal.
- Author 126/126 with verified fixtures/harness; R6 9/2 removed-transport;
  adapters 3/3; R5 6/2 superseded; R4 7/2 lawful.
- One failing assertion: legacy `trusted_binding_hashes` cache-hit `resolve`
  returns `STALE_OR_UNAUTHENTICATED_CACHE` instead of the explicit
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION` (import/export are explicit).

## Next bounded task (author/owner)

Preserve the explicit legacy-pin migration refusal in
`EvidenceResolver._replay_cache` instead of collapsing it to generic stale
cache; add a resolve-path assertion. Optionally mirror the explicit
`CACHE_OWNER_DESCRIPTOR_NOT_PINNED` code on replay for the distinct descriptor
pin. Re-run the full author and independent chains; request a distinct review.
No candidate repair by this reviewer.

## Commands

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/junit/author_suite_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/probes/test_r08v_r7_independent_boundary.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/junit/reviewer_probes.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/probes/test_r08v_r7_semantic_adapters.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r7/junit/semantic_adapters.xml
```

Expected reviewer result until repaired: 75 passed / 1 failed; the failure is
the recorded legacy-pin replay code.

## Boundaries

Full live J42/P41/E04 NOT_REACHED. No original source/science, production/CI,
N11/N12, Sorok, J52/W52, R03/R09 or adoption/authority change.
