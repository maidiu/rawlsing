# R61-R08V R8 independent review — resume

State: complete; verdict
**ACCEPT_SCOPED_LOCAL_TRUSTED_HOST_ADMISSION_AND_CONSUMER_BINDING** for the
bounded R8 correction and retained R7/R61AF scoped grain. Full J42/P41/E04 is
NOT_REACHED. No adoption, candidate edit or author wake.

## Custody

- Branch: `agent/opencode-pyat-r61-r08v-r8-independent-review-r1`.
- Candidate/startup: `be1133391d91b5c2bf69299188e6f011162f269b`; code
  `80bb8c182`; module blob `3ca860e4...`; test blob `5832ce05...`.
- Frozen EXPECTATIONS: `cb018e1011fca433c9a8132fbbe3a75879429fe9`.
- Precode correction contract `3f45fc9bc`.
- Prior R7 review preserved: `fc4597fb8398b8012367d8d9d1fa36502b3d798e`.
- Return root:
  `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/`.

## Established

- R7-AF-01 closed: legacy pin cache hit exact
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`; descriptor pin cache hit exact
  `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; missing verifier
  `NO_CONFIGURED_TRUST_ROOT`; genuine stale remains
  `STALE_OR_UNAUTHENTICATED_CACHE`; no support on refusal.
- R8 targeted 5/5; author 126/126; R7 successor 76/76; adapters 3/3.
- R6 9/2 removed-transport, R5 6/2 old grade/import, R4 7/2 lawful; all
  accounted.
- Native 54/6/60, changed 54/16/70, zero/status/typed/currentness/Z16,
  descriptor normal form/13 classes, verifier-only replay/re-export, cold chain
  retained.

## Commands

```text
PYTHONPATH=<inherited r7 harness> /usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/junit/author_suite_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/probes/test_r08v_r8_targeted_refusal_codes.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/junit/targeted_probes.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/probes/test_r08v_r7_independent_boundary.py \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r8/junit/r7_successor_probe_replay.xml
```

## Boundaries

No source/science/prod/CI/N11/N12/Sorok/J52/W52/R03/R09, no adoption, no
candidate edit, no new session/provider/account.
