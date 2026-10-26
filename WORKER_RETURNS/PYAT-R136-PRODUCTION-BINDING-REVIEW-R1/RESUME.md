# R136 review resume

- Verdict: **REVISE**. Production transport code path executes synthetically,
  but the required production positive and metadata/authority binding are not
  qualified.
- Branch: `agent/opencode-pyat-r136-production-binding-review-r1`.
- Candidate: `bda89324a85ce06d44a19e6b19994e5543c065de` vs baseline
  `d933411889dbcbcafc8d3a2c596e44fc69820f63`.
- Code blobs: source adapter `f21e01b1…`, workload binding `a166d687…`,
  production binding `a34252a8…`, focused test `4e3158cf…`.
- Oracle frozen at `86e73a1f3`; initial review branch was at prior R118 tip, so
  candidate was merged nonforce (`985dcd712`); `rawlsing_next` tree exactly
  candidate. See `evidence/branch_reconciliation.txt`.
- Author focused 5/5; listed existing regression actual 4/4 (author claimed 5);
  independent probes 1 pass/4 fail; cold replay deterministic but output facts
  non-positive.
- Blocking findings: no supported empirical fact (UNAVAILABLE, raw 0/0);
  query authority accepts foreign source/scope; source authority snapshots
  accept foreign source; descriptor metadata accepts foreign source/ZZ;
  physical decode occurs before admission; discovery path not demonstrated.
- Preserved: synthetic transport reaches allow_test_only=False, value/refusal/
  restore mechanics, explicit test-only path, wrong host/purpose/envelope/roots/
  universe/role/grade controls.
- Limits: sourcefree synthetic harness only; no original 35/1890/F1–F8/global
  F6/F7/F8/source/science/learned/FF/actor/M1forall/R09/CI/prod/N11/N12/Sorok/
  J52/W52/production. No source/permission issuance or candidate edit.
- Next: author repairs exact authority/metadata/predecode/positive seams or HQ
  disposition; this branch is evidence only. Push nonforce; direct remote
  readback in `evidence/remote_readback.txt`.
