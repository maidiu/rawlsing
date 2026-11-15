# EE-P2XD — DARWIN MECHANICAL COURT DRIVER PREPARATION — GOVERNED RETURN

Status: **PASS**

Terminal:

`EE_P2X_DARWIN_MECHANICAL_COURT_DRIVER_READY__NO_EMPIRICAL_MEASUREMENT_PERFORMED`

Branch:

`agent/rabochii-prev3-ee-p2xd-darwin-mechanical-court-driver-preparation-r1`

Commission lineage:

- exact base: `a954e2d6676843da8427ef2439b5d1ef33478359`
- commission tip: `8f2b5fec8808824a43e119789adecb4dc4bba127`
- sealed HQ checkpoint: `20260918T0317-0400`
- immutable HQ handoff: `ac722a9952b792e0fd43b5fbf28ca98b6d0c1e87`
- HQ decision: `HQD-2026-09-18-036`

## Holding

PASS. The browser-side deterministic Darwin orchestration layer is implemented and governed-browser-qualified.

Implementation:

`rawlsing_next/ee_p2x_darwin_court_driver.py`

Git blob:

`c3a368270f6f7a6f613efb78e31972e64a092c88`

The driver consumes the exact adopted continuation map:

- schema `RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0`
- reducer return `eb7595f1030d1861c262dbdb6bb4d7c12d1abd43`
- Git blob `e06e95dd370a4fd44235932088308c3372522ed4`
- exact-byte SHA-256 `ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`

It does not reconstruct the court from conversational history.

## Mechanical execution law implemented

The driver now mechanically enforces:

- exact source order `LITS_I -> WVS7`;
- exact candidate order `A -> B -> C`;
- reducer-local stage sequencing, including cell-local next-stage expansion;
- first unfinished entry at `LITS_I/A/S02_C11_REACHABILITY`;
- non-execution of `DONE__PRESERVE` stages;
- non-execution of frozen-law skips;
- preservation of the completed LiTS-A qualifying first build;
- preservation of the completed LiTS-B standalone cacheless-C11 preparation;
- exact source SHA verification before fresh empirical source use;
- explicit Darwin x86_64 / CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1 gate;
- R8B Darwin `ru_maxrss` byte law;
- isolated scratch/durable/log/receipt roots per source×candidate;
- single-driver locking without process-name idleness heuristics;
- exact-byte Candidate-A/B/C owner deployment from accepted owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`;
- P2R1 `RuntimeObjectCatalog -> governed projection -> accepted owner -> bind_repository_builder -> CarrierNeutralResearchExecutor` composition;
- fixed backend contract for measured stage bodies rather than candidate/source semantic branching in the orchestrator;
- candidate-local failure propagation without suppressing later lawful candidates;
- common-source and common-court blocker scope;
- atomic durable stage ledger;
- `RUNNING != COMPLETE`;
- resume-time revalidation of terminal receipt and output hashes;
- WVS-C preserved `WVS7_C__CURRENT_PORTABILITY_FAILURE` with no executable fallback;
- explicit `S17_FINAL_COMPLETENESS_AND_VERIFICATION` dispatch;
- local-supervisor action tokens after measured host stages without inventing automatic Git commit/push behavior.

## Governed browser qualification

Commission-required hostile suite:

`tests/test_ee_p2x_darwin_court_driver.py`

Git blob:

`53ab07f00f23b6d5d8d8b67d8974de7bebc61488`

Result:

**19/19 PASS**

The repository-governed court was bound through:

`rawlsing_next/tests/test_ee_p2xd_governed_browser_court.py`

and:

`.rabochii/court_spec.json`

Transient qualification PR:

**#387**, closed without merge.

Governed workflow:

- workflow: `Rabochii Governed Bounded Court`
- run: `35321826151`
- run number: `474`
- job: `105525800028`
- semantic candidate: `d69ebc3767461b110721d6acfcf3b9b373c92bab`
- evidence execution SHA: `10d9920d7ec69d86231acb02a4391155b1da288e`
- protocol self-tests: **20/20 PASS**
- governed outer court: **1/1 PASS**
- court receipt: `RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0`, result `PASS`
- court spec SHA-256: `6c7d294bb5f464db1342424c20b78aabe88936358ca81891d695c4f937c67bb4`
- receipt artifact ID: `10537033071`
- artifact ZIP SHA-256: `f8573fa73c1a656e5e0f04aec5416d4dffe07bfba3048e6732253f6597e67e57`

Full qualification receipt:

`WORKER_RETURNS/EE-P2XD/01_BROWSER_QUALIFICATION_RECEIPT.json`

## Scope audit

Not performed:

- empirical carrier access;
- Library carrier access;
- real LiTS or WVS source open/decode;
- measured P2X execution;
- benchmark execution;
- wall/CPU/RSS/I/O/throughput measurement;
- surrogate timing or performance generation;
- fake receipt or fake measurement generation;
- Lock1 mutation;
- Lock2 mutation;
- candidate or workload redesign;
- WVS accelerator creation;
- third CACC creation;
- ranking or selection;
- P2X ref movement;
- MAIN mutation;
- semantic PRE-MAIN mutation;
- rebase;
- replacement branch.

This PASS prepares the mechanical court driver only. It does **not** authorize local measured continuation. HQ must adjudicate this return and selectively bind qualified preparation into the existing EE-P2X branch before the coordination hold is lifted.

Successor wake:

`HQ_ADJUDICATE_EE_P2XD__SELECTIVE_QUALIFIED_FANIN_TO_EXISTING_EE_P2X`

Terminal:

`EE_P2X_DARWIN_MECHANICAL_COURT_DRIVER_READY__NO_EMPIRICAL_MEASUREMENT_PERFORMED`
