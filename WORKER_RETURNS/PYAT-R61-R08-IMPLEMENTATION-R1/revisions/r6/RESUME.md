# R08 R6 resume

- Startup: `6abd49ffd9bb61925084036f2f1275841b3b5c83`
- Amendment commit: `b9076985ec3be2ead1c47a2f754a52f774dfca59`
- R6 code commit: `7450b4f389e4a95a85066065dec7acafe83da84d`
- Branch: `agent/opencode-pyat-r61-r08-evidence-binding-r1`
- Signed original execution provenance/mode added to envelope; served output no
  longer derives trust from unsigned result provenance.
- Export validates evidence/query/rule objects and refuses mutated payloads;
  verifier-only re-export preserves signed envelope and works.
- Author suite: 38 passed, 0 failed/skipped, 9.64 s.
- R5 probe replay: 6 pass; 2 old expectations superseded (removed unsigned grade;
  export-refusal assertion shape). Successor R6 tests cover both.
- Positive native 54/6/60, changed 54/16/70, observed zero, status partitions,
  Z UNRESOLVED16, fail-closed live pin and cold/re-export round-trip preserved.
- Reach: J42/P41/E04 live adoption NOT_REACHED; archived returns unedited.
- Author validation only; independent R6 reviewer not launched/self-adopted.
- TEST_ONLY sourcefree; no original data, science/source, production/CI,
  N11/N12, F6/F7/F8, actor or Sorok authority.
