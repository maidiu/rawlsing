# Court B — T35 Independent Reproduction and Adversarial Review

Target: `8bfb145f7da8a2d5e6c0913919721ad4085b5d85`
(worker return `WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1`)
Pinned read-only worktree: `R38-N9TI-T35-pin-8bfb145f7`.
Declared sealed startup: `5064d76b3c58a8225693055a8ec6bb07e216d9b1`.
Verdict: **ACCEPT**. See `00_INDEPENDENT_REVIEW_VERDICTS.md`.

## Custody

* T35 does not contain the review base commit; its line is
  `7b1dcb82e → 5064d76b3 (commission/sealed startup) → 71a4df6d5 → 8bfb145f7`.
  The brief's base is therefore not an ancestor of this court; the sealed
  startup hash is recorded instead (`product["sealed_startup"]`).
* Custody diff `71a4df6d5..8bfb145f7` is documentation-only:
  add `publication_verification.json`, update `artifact_manifest.json`.

## Reproduction (cold, reviewer's own runs)

| Artifact | Tests | Result | Time |
|---|---|---|---|
| `our_suite.xml` | 41 | 0F/0E/0S | 81.278 s |
| `original_m4_m5.xml` | 30 | 0F/0E/0S | 0.417 s |
| `original_empirical_chain.xml` | 75 | 0F/0E/0S | 16.653 s |
| `original_e04_author.xml` | 37 | 0F/0E/0S | 16.041 s |

Total 183 events, all green (cold JUnit files in `evidence/`).

* Driver `two_epoch_world.py` redriven from the pinned runtime: product
  byte-identical to the pinned `03_WORLD_TWO_EPOCH_CONSUMER_DELTA.json`
  (SHA-256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`,
  1,099,273 bytes); `cold_a.json`/`cold_b.json` also byte-identical to it.

## Reviewer adversarial suite (`evidence/test_i2_adversarial_t35.py`)

Values in the suite are recomputed from the publisher catalog records, the
hand-derived 58-row cell counts and reviewer-owned preimage math; the worker's
tests are not imported.

Result: **13 passed, 0 failed** (87.698 s;
`evidence/t35-adversarial-i2.xml`, timestamp `2026-10-18T21:14:08-04:00`).

- t01 rule-revision identity recomputed from catalog records: fee 2 rev-1
  (pub `2026-03-01`, eff `2026-01-01`), fee 6 / exit 8 rev-2 (pub
  `2027-06-01`, eff `2027-01-01`), access/civil frozen at rev-1; both epochs
  select the expected revisions; selection clocks exact.
- t02 empirical steps recomputed from the documented cell counts
  ((6,2)(4,4)(5,3)(3,5)(4,2)(2,4)(3,3)(2,6)): (32,{14,18}), (16,{6,10}),
  (8,{2,6}), exact fractions consistent, source balance [4,4,4], identical
  across epochs.
- t03 affordability ladder: budget 5 → training blocked / exit constrained;
  6,7 → training eligible / exit constrained; 8 → eligible / within budget;
  proposals feasible under both routes; access stays TRUE.
- t04 clock matrix at both boundaries plus the day before, and the explicit
  `AS_OF` control vs `TEST_CURRENT`: identical values/routes/scenarios.
- t05 both served receipts equal the pinned `epoch_receipts` (complete dict
  equality after canonical JSON round-trip); receipt/snapshot hashes equal the
  pinned views; re-serve in the same adapter is hash-stable; historical receipt
  is `archival_only = True`, `fresh_use_authorized = False`.
- t06 revocation matrix: civil revocation → `TYPED_PARTIAL_SELECTED_WORLD`,
  civil route `UNAVAILABLE_AUTHORITY_OR_CLOCK`, training still eligible, old
  receipt invalidated for fresh use; fee revocation → civil-only receipt still
  served, full receipt training unavailable; GSS revocation → native state
  `PARTIAL_TEST_ONLY_NOT_POSITIVE` with remaining role
  `NCA_NATIONAL_MOBILE_DATA` and a typed refusal for GSS.
- t07 four refinements: `UNREGISTERED_SELECTED_SNAPSHOT` (foreign accept),
  `ACCEPTANCE_BINDING_MISMATCH` (foreign serve),
  `ACCEPTED_SNAPSHOT_SUBSTITUTION` (cross-epoch acceptance),
  `UNREGISTERED_SELECTED_SNAPSHOT` (rehashed tampered snapshot).
- t08 forbidden-token scan (N8E, N8E_GHA, GHA_R5, GHA_R9, Q43, Q31, Sorok)
  clean over full receipt strings and keys; required authority flags all
  false/zero; claim ceiling
  `SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL`.
- t09 every pinned-closure preimage matches its own recorded blob+sha256, and
  every pin's blob is additionally verified to exist at its claimed commit via
  `git ls-tree`. Notably `rawlsing_next/pre553_hq297_n9c_two_field_reader.py`
  (`03eb46ef…`) exists at `9ab4a0192…` and is absent at the sealed startup,
  justifying staged loading; the progressive candidate (`84d404147…`) exists
  at `0e0ed50db…`. T35's R13 adapter blob `690790e8…` ≠ N9J's R11 adapter blob
  `642381bc…`.
- t10 driver end-to-end byte-identity (see reproduction table); assertions all
  true, `failed_assertions = []`, terminal
  `TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_CONSUMER_POSITIVE__N8E_ABSENT_HOLD`;
  N8E input remains `ABSENT_HOLD` with null numerics; V553 candidate verdict
  and empty-readiness count (45) match; import preimages carry commit
  `84485d32…` and blob `690790e8…`.
- t11 transport runtime modules contain no wall-clock, PID, socket, urllib,
  requests or http(s) tokens.
- t12 **cross-court probe**: the identical zero-support path that reddens
  N9J-F1 is typed under the R13 seam — `TYPED_PARTIAL_SELECTED_WORLD`,
  `PARTIAL_TYPED_EMPIRICAL_SUPPORT`, last step denominator 0, empty cells —
  no `KeyError`. The upstream fix for N9J-F1 is present in this revision.
- t13 R13-specific hardening: serving a tampered consumer envelope raises
  `CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT`; a trimmed consumer set raises
  `TWO_ORIGINAL_CONSUMERS_REQUIRED`. The R11 adapter lacks this envelope
  enforcement entirely.

## Documented limitations (not defects)

* The freeze claim `frozen_before_executable_comparator_or_driver_code: true`
  is not Git-order verifiable: freeze, runtime, tests and product land in one
  commit (`71a4df6d5`). Content-level consistency (frozen values vs delivered
  values vs my independent recomputation) was verified instead, and no
  contradiction was found.
* Worker JUnit artifacts carry a sanitized hostname; test counts/status are
  unchanged. My own evidence retains authentic host metadata.

## N8E / Ghana envelope

`n8e_input` remains `ABSENT_HOLD` with `numeric_delta = null`,
`measured_no_change = null`, `world_input = false`, `consumer_input = false`;
the Ghana EE12 owner record stays `HOLD_…` with all numerics null. The
hypothetical N8E arithmetic in the freeze (p_A 0.5, p_B 0.7, delta 0.2,
variance 0.0061, interval [0.04692, 0.35308]) is method illustration only and
is never executed by the driver.
