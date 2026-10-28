# Exact demonstrated defect — repair only

V2candidate6ffd821df custody verified;8artifacthashes and terrain match. REVISE before actual decoded source use.

HQ reproduction using your existing nonrespondent test_numeric_domain_binding._cells():
- apply_observed_domain(BASE,_cells()) -> added q715:2,q716:2
- apply_observed_domain(BASE,iter(_cells())) -> added q715:2 ONLY

PhysicalSourceIncidence.iter_cells is a generator. apply_observed_domain currently loops slots outside one shared cells iterator; first slot exhausts it, second is silently skipped. Fix with one pass over cells routed to prepared exact slot lookup, or equivalent stream-safe approach. Do not materialize the whole source to work around it. Preserve exact original numeric tokens/missing states, config/source checks, country-specific currency provenance and old13repairs. Add the discriminating iterator regression covering BOTH fields; run actual native factory on a clearly NONRESPONDENT iterator-backed stream so tuple-onlytest cannot hide this. No originalsource I/O; grant stillpending. No extra scope or tests unrelated to this bug. PreserveV1/V2returns ashistory and emitversionedsuccessor. Same allowlist/session/model; commit/push/directremoteverify.
