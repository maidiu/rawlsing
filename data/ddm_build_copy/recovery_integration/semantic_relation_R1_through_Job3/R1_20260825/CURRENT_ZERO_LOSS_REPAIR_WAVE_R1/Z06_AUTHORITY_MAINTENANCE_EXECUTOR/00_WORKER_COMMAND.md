# Z06 — FUTURE SEMANTIC-AUTHORITY MAINTENANCE EXECUTOR R1

Role: VOZHD CHETIRI
Repository: `maidiu/rawlsing`
Worker branch: `agent/verkhovod-z06-authority-maintenance-executor-r1`
Exact starting HEAD: `c649d57c14ca6c0f84571beab4610c007c2484f2`

Read Authority 40 and D05 exact return `b7dd1bce667651c88ddd71c17c065f2b33ec38ec`.

Target: close inherited `LMQ-006 / LMX-004` at same-or-stronger function grain. Current immutable `AuthoritySnapshot` consumption/replay is strong but is not an authority-production/correction lifecycle.

C5R2 prototype `b4dae70ee524c7a3297f7b48bdfd0d0c927eac21` is nonauthoritative prototype evidence only. Do not inherit/promote its owner IDs.

Implement/prove the minimum current governed lifecycle capable of:
`candidate/evidence -> adjudication -> collision/split/exclusion correction -> immutable revision -> seal/promotion/release/current-selection -> rollback/supersession -> affected-dependency invalidation/recompilation -> deterministic replay/audit`.

Requirements:
- immutable historical revisions remain replayable; later authority cannot silently reinterpret old runs;
- same id/version + conflicting content fails closed;
- no latest/default/fuzzy authority selection;
- every mutation has exact parent/supersession/genealogy and evidence/adjudication refs;
- rollback selects a prior lawful release without mutating history;
- changed authority deterministically invalidates only affected dependents under the semantic determinant graph;
- future source onboarding can create needed semantic authority rather than requiring prebuilt snapshots from nowhere;
- positive promotion requires explicit governed adjudication; unresolved/rejected candidates remain typed states;
- promotion/current-selection must be atomic/restartable.

Do not rebuild the historical P2/P3/P3A/P3C physical topology unless a function cannot be preserved more directly. Historical algorithms/numeric heuristics are not binding absent function-law proof.

Add executable hostile lifecycle tests and a complete function ledger against the eleven D05-required lifecycle functions. Return exact test/receipt refs and negative ceiling.

No architecture selection or V3 work.
