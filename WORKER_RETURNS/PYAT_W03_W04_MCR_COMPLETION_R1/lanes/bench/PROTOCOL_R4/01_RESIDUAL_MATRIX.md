# Residual receipt matrix

| Group | Required measured fields / identity | Current status |
|---|---|---|
| M1 env isolation | inherited policy/legacy absent before actual call; no foreign cache file; cold status truthful; full own qualified policy | GREEN `env_isolation_probe.json`, cold foreign count 0, `test_cold_clears...` |
| M3 cap | `cap_bytes`, `cap_enforced`, `cap_monitor_active`, `cap_peak_sampled_bytes <= cap_bytes`, sampled-kill method, no blocked pass | GREEN `cap_probe.json`; tiny pair `cap_pass=true`; synthetic missing-cap fails |
| M4 regressions | all >10% records; explicit status+justification+correction; unresolved fails; thresholds retained | GREEN tests; 20% other-profile report with resolution; independent receiving still required |
| M4 clock | parent launch-to-firstconsumer marker in both arms; canonical reopen excluded; total parent wall retained separately | GREEN tiny pair ratio 0.790474; parent wall still in receipts |
| M4 identity | protected 4f source, method hash, command params, external baseline SHA256, host/rows/profiles/reps, event counts, fingerprints | GREEN tiny pair all identity fields true; 6 parity comparisons |
| M5 cost | derived write wall/CPU/bytes; canonical separate; amortization actual savings | GREEN tiny pair; break-even derived-only |
| M5 hit | actual read validation result; envelope/body content; no size/mtime hit; fresh PIDs and typed parity | GREEN body-corruption miss; valid warm hits; non-body byte caveat recorded |
