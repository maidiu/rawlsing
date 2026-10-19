# Cross-Court Independence, Shared Substrate and Circularity Limits

## What the two courts actually share

Both courts execute the same sealed/upstream substrate:

* E04 generic world product (R10 `9c96f201f…` blobs staged into both packets).
* HQ297 N9C two-field reader + fixture (single upstream author, `9ab4a0192…`).
* Sealed M4 V557/V558 publication/repository and M5 RSC modules at each
  court's sealed startup.
* E03 progressive candidate (`0e0ed50db…`) for the empirical chain.
* The same synthetic 58-row TEST_ONLY source world (identical cell counts and
  balance in both courts).

## Where the courts are genuinely different

* **Adapter revision.** N9J delivers the R11 adapter `642381bc…`
  (`257dfaf41…`); T35 stages the R13 adapter `690790e8…` (`84485d32c…`).
  R13 differs materially: steps deep-copied (fixes N9J-F1), consumer
  envelopes recomputed and compared in full, native withdrawal overlay,
  `_fresh_native` re-reads, extra refusal codes.
* **Capability under test.** N9J: sourcefree progressive consumer over the
  N9-shaped selected-world interface with refused/typed empirical partials.
  T35: two-epoch institutional-rule world delta with revocation, mismatch and
  clock matrices over the same interface family.
* **Test programs.** N9J worker suite (20 events) vs T35 suites (183 events)
  are disjoint reviewer-visible programs; my two adversarial suites are also
  disjoint (a01–a14 vs t01–t13) and were written against each court's own
  frozen expectations.
* **Results.** A single zero-support probe reddens N9J (a14) and passes T35
  (t12) — direct evidence the courts exercise different seams, not one
  replayed capability.

## Shared-producer circularity limits (disclosed)

* The E04 product, N9C reader and both adapter revisions descend from the same
  upstream author lineage (R10/R11/R13). Producer-grain independence between
  the courts is therefore **limited**: a shared latent defect in E04/N9C would
  affect both courts identically. The cross-court value is at capability and
  adapter grain, plus the reviewer's arm's-length reimplementation.
* Sealed M4/M5 modules are common to both; their correctness is outside both
  returns' authority ceiling and is exercised, not re-derived, here.
* The reviewer's adversarial suites recompute all expected values from
  publisher records and hand-derived counts, but they still execute the same
  production functions to observe behavior; they cannot prove the production
  functions correct by construction, only that the delivered behavior matches
  the frozen and recomputed expectations on every probe attempted.

## Net independence statement

Accepted as two distinct consumer capabilities over one shared substrate. The
T35 result does not "rescue" the N9J finding (different adapter revisions), and
the N9J finding does not taint T35 (R13 is not the defect locus). Twelve of
thirteen T35 probes and thirteen of fourteen N9J probes could have failed
identically for a shared substrate fault; none did, so within the authority
ceiling both deliverables are behaviorally exact against their frozen
expectations.
