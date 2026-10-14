# HQ298 S-M-LAB2 — independent reviewer boundary

**Discipline:** implementer cannot serve as independent reviewer. A distinct **blind independent I2 behavioral reviewer** is required before any scientific/semantic acceptance (commission "Acceptance, stop and independent review"; 00C §8).

## What the reviewer adjudicates

1. **Freeze integrity** — `01_PREREGISTRATION_FROZEN.json` sha256 `880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330` recorded in `outputs/preregistration_freeze.json` before any trial; confirm no behavioral capture predates the freeze.
2. **Verdict preservation** — confirm the LAB1 machine-level verdict is preserved verbatim (A passed all K; B ranking REJECT via K2 1.0→0.0 and +33.5% tokens; C DERIVED_CACHE) and that nothing in this return relabels synthetic results as behavioral proof.
3. **Replication honesty** — re-run `python3 lab/run_lab.py` from the blob-verified vendored closure (`lab2/predecessor_lab1/PROVENANCE.json`) and confirm 576/576, identical scores and identical preregistration hash `f36d2d31…`.
4. **Model-gate strictness** — confirm zero model calls were issued, that `run_granted()` is unreachable without a complete grant, and that no local credential was used as a substitute for a grant.
5. **Matched-comparison validity** — confirm `matched_content_across_arms_ok: true` for all 576 trial packets and that the only cross-arm variation is the arm machinery label (absent from actor-visible packets).
6. **Blind scoring integrity** — confirm the scorer API structurally excludes prose; dual-scorer agreement enforced; counterbalance codes hide arm/contrast labels; expected codes match the frozen preregistration.
7. **Firewalls** — re-run the N5 trace-firewall and K5 standing-separation probes; confirm hidden origins never reach actor-visible packets and standing effects never appear in actor-info packets.
8. **Dry-run labelling** — confirm the harness dry-run is labelled `HARNESS_DRY_RUN__NOT_BEHAVIORAL_EVIDENCE` everywhere and its trivial all-1.0 comparison is not presented as a result.

## Out of scope for this reviewer

- The behavioral answer itself (untested; the reviewer cannot supply it by opinion).
- Any adoption decision (CAN/ADP rules, B/C promotion) — owner acts, not reviewer acts.
- Any grant issuance (provider/model/privacy/cap are owner decisions).

## Requested reviewer terminal

`REVIEW_PASS | REVIEW_REVISE | REVIEW_REJECT | REVIEW_HOLD` with exact failed predicates. Even `REVIEW_PASS` adopts nothing.

## Reviewer qualification

I2-high experimental-validity reasoning; familiarity with S-M-LAB1 (`d7cc7ebf…`), SM (`7777a06d…`) and HQ297 K35 (`12c65e0e…`); able to re-run the python/pytest closure independently; must not be the implementer.
