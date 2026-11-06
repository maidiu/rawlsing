# UNIVERSAL35 A remaining-mapping R2 independent review

**VERDICT: REVISE** at A head `7f3931607d1309e84ad068c353946831248184b3`, delta `ef43bbbbb16ac8925056f7c5bed522d6b1200ea5`.

- **Mechanism/provenance: ACCEPT_SCOPED_ENGINEERING.**
- **Source metadata/denominators: ACCEPT_SCOPED_ENGINEERING.**
- **Factual response-state authority: REVISE.**
- **Consumer: ACCEPT_SCOPED_ENGINEERING** for the checked projection path; full C11/native remains NOT_RUN.
- **Overall: REVISE** for the composite-label state mappings and the latent fail-open correction default.

## FINDING

The trusted base-commit/exact-path enforcement works. Independent probes passed for no provenance, wrong source SHA, wrong base hash, wrong provider commit, wrong loaded path, wrong registry path/commit, refusal and exact restore. The R157/SRC31 entry is unchanged; fixtures and unrelated sources are unaffected; the 35/18,276/18,413/18,250/26 denominators are preserved. All eight correction entries match actual source-declared missing declarations and labels, all 46 targeted tests pass, and **no substantive response value was added**.

However, 362 correction changes map composite/ambiguous source labels to a single precise `DK`, `NOT_ASKED`, or `REFUSAL` state without an exact state-authority receipt. Examples:

- SRC16 label `dk, na, iap` -> `DK` (154 changes).
- SRC24 label `No answer/Refused` -> `REFUSAL` (182 changes).
- SRC25 labels `No answer/Don't know`, `Don't know/No answer`, `DK/NA`, etc. -> `DK` (24 changes).
- SRC26 labels `Don't know / No answer`, `Don't know/Don't remember` -> `DK` (2 changes).

A composite label is not an exact single-state codebook contract. The correct conservative result without authority is `SOURCE_SPECIFIC_SPECIAL` or `INVALID_UNRESOLVED`, not a precise DK/NOT_ASKED/REFUSAL. This is the same label-alone boundary the commission flags; no substantive promotion occurred, but precise non-substantive states were inferred from labels.

The current correction application also defaults `response_state` to `SUBSTANTIVE_RESPONSE` for an `add_if_absent` change when the field is omitted. All current registry entries are explicit, so no current substantive promotion exists, but the default is fail-open for future data and should become a required field or `INVALID_UNRESOLVED`.

The review also observed 95 existing substantive base values in remaining-seven configs being overwritten to non-substantive states based on declared missing ranges/labels. This is not substantive promotion; where the source missing range is exact it is plausible, but A should explicitly account for these state transitions rather than treating the corrections as unbound-only additions.

## EVIDENCE

- Targeted suite: **46 passed** (`results/pytest_46.log`).
- Provenance probe: `results/provenance_probe.json`.
  - no provenance: 0 applied; wrong SHA/base hash: 0; wrong provider commit/loaded path/registry path/commit: refused; exact restore: 31 SRC31 / 86 SRC32.
  - SRC31 entry unchanged; fixture and SRC09 corrections empty; index baseline exact.
- State/metadata probe: `results/state_probe.json`.
  - all 8 entries match source declared missing state/declaration/label; zero substantive additions; all mismatch-free.
  - SRC16 and SRC31 actual factory projection carried every corrected physical key with the declared state (2,538 and 31 values; zero projection misses).
- Composite-state findings: `results/state_authority_findings.json`.
  - 362 composite-label precise-state changes; 95 existing-substantive overwrites (remaining seven; not a substantive promotion).

## REQUIRED REPAIR

1. For composite/ambiguous labels, replace precise `DK`/`NOT_ASKED`/`REFUSAL` with `SOURCE_SPECIFIC_SPECIAL` or `INVALID_UNRESOLVED`, or supply an exact accepted response-state/codebook authority for each mapping. Add tests that reject composite-label precise states.
2. Make the add-if-absent default fail closed (require explicit `response_state`, or default to `INVALID_UNRESOLVED`), never substantive.
3. Document/review the 95 existing substantive-to-missing state transitions; preserve or explicitly justify each with exact source metadata/authority.
4. Keep provenance enforcement, R157/SRC31 freeze, fixture identity and denominators unchanged; rerun zero-unbound and projection-state checks.

## LIMITS

No full C11/native/empirical execution, no full 600s scan, no all35 fixture floor, no original DTA/native acceptance. SRC31 factual authority remains F-scoped; no new science or permission is granted. This review is nonauthor and bounded; no A/D/E/guide/progress/protected changes are made.

## PROGRAMMA_DELTA

`MAPPING_R2_REVIEW = REVISE`: provenance/source metadata/denominators accepted scoped; composite-label precise states and fail-open default require A revision; consumer projection accepted scoped for SRC16/SRC31; full native remains NOT_RUN.
