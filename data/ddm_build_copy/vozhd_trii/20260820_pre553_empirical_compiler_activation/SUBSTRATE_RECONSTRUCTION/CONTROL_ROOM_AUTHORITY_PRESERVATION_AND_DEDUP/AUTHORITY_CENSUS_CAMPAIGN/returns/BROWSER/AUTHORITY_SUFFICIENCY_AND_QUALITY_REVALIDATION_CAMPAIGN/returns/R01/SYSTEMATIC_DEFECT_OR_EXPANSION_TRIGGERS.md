# R01 Systematic Defect / Expansion Trigger Result

R01 performed a full requirement-level coverage census. It did not perform semantic source-quality sampling and therefore does not report a semantic defect rate or Wilson interval.

## Common trigger results

- Systematic rate trigger: `NOT_APPLICABLE` — no semantic sample.
- Severe semantic trigger: `NOT_APPLICABLE`.
- Cluster trigger: `NOT_APPLICABLE`.
- Downstream consequence trigger: `NO_NEW_DEFECT_TRIGGER` — R00 already explicitly carried the high-consequence orphan/frontier states.
- Provenance trigger: `DEFER_TO_R08`.
- Hidden-coverage trigger: `NOT_FIRED_AS_A_SURPRISE` — R01 did not discover a class previously certified complete whose lawful consumer denominator unexpectedly exceeded coverage. Instead it confirmed several R00-known partial/provider-unproved classes.
- False-unresolved trigger: `NOT_FIRED` — R01 located no source-backed evidence that resolves a nontrivial unresolved class; source-hostile proof belongs to R05/R07.
- False-certainty trigger: `NOT_FIRED_BY_R01` — quality courts may still do so.

## Task-specific expansion frontier

R01 does propose bounded provider/scope expansion for the classes in `COVERAGE_EXPANSION_CANDIDATES.csv`. These are not automatic new-authority orders. They are proof obligations for HQ/R02-R08/Chetiri before a missing-authority or schema-gate ruling.

Highest-priority T4 coverage frontiers:

- `TIR-014` semantic event-occurrence / slot identity;
- `TIR-047` production adaptive-discovery authority instance;
- `TIR-048` branch/cohort predicate membership provider;
- `TIR-049` advanced discovery provider mapping;
- `TIR-050` general post-discovery validation/admission law;
- `TIR-051` positive comparator rule coverage;
- `TIR-053` production PSEPF provider;
- `TIR-065` learned-product lifecycle owner law.

No class reaches `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED_CANDIDATE` because exhaustive successor/provider search and derivability proof are not complete at the exact required grains.
