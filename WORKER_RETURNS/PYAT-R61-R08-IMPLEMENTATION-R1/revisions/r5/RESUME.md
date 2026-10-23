# R08 R5 resume

- Startup: `48a2eaf6d3c653e2efe40643c427f28c47cd744b`
- Amendment commit: `5cdbaaecdcd3a1ecfee62025e4a0ca7f99e9b469`
- R5 code commit: `cfe3297e8962b3a11a62e9e89d26d7de50fadba5`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- Reader/e04_step/cache export/import/replay now share one complete signed
  envelope projection; unsigned result/values substitutions are refused.
- Live execution requires a configured admitted-producer identity; missing pin is
  fail-closed before call. Verifier-only cold replay remains supported.
- Author suite: 34 passed, 0 failed/skipped, 9.70 s.
- R4 probe replay: 7 pass; 2 old defect probes expect forged 999 service and now
  correctly receive refusal. Successor R5 tests cover those field classes.
- Positive native 54/6/60, changed 54/16/70, observed zero, ZERO_SUPPORT,
  valid-product states, Z UNRESOLVED16 and cold replay preserved.
- Reach: J42/P41/E04 live adoption NOT_REACHED; archived returns unedited.
- Author validation only; independent R5 reviewer not launched/self-adopted.
- TEST_ONLY sourcefree; no original data, science/source, production/CI,
  N11/N12, F6/F7/F8, actor or Sorok authority.
