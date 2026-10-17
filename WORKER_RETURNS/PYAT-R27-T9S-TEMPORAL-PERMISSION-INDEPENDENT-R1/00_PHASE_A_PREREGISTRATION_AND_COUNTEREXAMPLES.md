# T9S Phase A — independent preregistered temporal-permission counterexamples

**PHASE_A_PRECOMMITTED; PHASE_B_GATE_NOT_YET_OPENED.** Independent temporal
scientific reviewer; not the T9B/T9C/T9D author, HQ, source issuer or actor
issuer. Sealed startup `b6e6f64f01d339956d8140777eab7f0c4a45e1af` (the 01 HQ
OpenCode/DeepSeek-V4-Pro dispensation addendum) verified. Parent reviewer T9R
`299dbf0d3a54fa76e36e524c553662f60090fe72`.

No T9D candidate code or output has been inspected. T9R's public REDs are
inherited historic evidence, not blind preregistration; this court additionally
devises its own executable counterexample vectors and freezes them here.

## Inherited dispositions preserved until physically resolved

| Court | Disposition |
| --- | --- |
| Original native V553 | 8 PASS |
| Historical author 28 (vs T9C) | 27 PASS / 1 historical-compatibility FAIL (old unsafe open-route assertion must not be restored) |
| Independent T9I 48 (vs T9C) | 47 PASS / 1 historical-compatibility FAIL (two-time artifact disclosure diff) |
| T9R frozen delta 50 | 46 PASS / 4 unavailable-capability FAIL (D04, D16, D17, D17_WRONG_OWNER) |
| T9C author's own 52 | 52 PASS (author evidence only) |
| T9R post-inspection 7 | 0 PASS / 7 FAIL — these were NOT preregistered; **this court preregisters them** |

## What Phase A physically reproduced on the pinned T9C adapter

The pinned T9C adapter (`…/phase_b/pinned_candidate/t9b_temporal.py`, verified
byte-identical to T9C candidate `9a33c2dcaa7ac0d50606416ab965488c9782934b`)
reproduces all four current REDs, captured in
`observations/phase_a_reproduced_reds.json`:

1. **Unused future upgrade** — retrospective 1995 M0/M2: adding unused
   `W1=(2000,0.60)` leaves value `0.20` and basis `("W0",)` but upgrades
   `temporal_key` from `PROBE_ONLY_TEMPORAL_KEY` to
   `AUTHORIZED_SPARSE_TEMPORAL_KEY` and opens `ROUTE_DEFERRED_REVIEW`.
2. **Empty actor grants** — two anchors + `access_grants=()` still return
   `authorized_opportunity=True` and open both routes for all three methods.
3. **Lag parser** — `pub_lag_of` returns
   `DELAYED|POST_RUPTURE_CARRY_HYPOTHETICAL:R1995|IDENTIFIED_SET_UNBOUNDED:STABILITY_NOT_ASSUMED`
   as a single wave identity.
4. **Duplicate wave id** — a wrong-country duplicate rebinds provenance to
   `WRONG_SOURCE`/`WRONG_EDITION`.

The two capability gaps (archival known-at bound; source-edition/currentness/
owner grants) have no API representation and raise a typed
`CapabilityUnavailable` in the binding — a RED, not a skip.

## Frozen preregistered suite

`01_T9S_PRECOMMITTED_PERMISSION_ORACLE.json` freezes six falsifiers (F1–F6) and
six positive controls (P1–P6). `tests/test_t9s_permission_falsifiers.py`
preregisters 17 executable cases. Executed against the pinned T9C adapter:

| Phase A preregistered suite | PASS | FAIL | ERROR | SKIP | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| T9S permission falsifiers | 6 | 11 | 0 | 0 | 1 |

The 11 failures are exactly the six preregistered RED groups (F1×2 methods,
F2×3 methods, F3, F4, F5, F6×3), none skipped, none erroring. The 6 positive
controls (single-anchor PROBE, two-anchor endpoint AUTHORIZED, retrospective
interpolation PROBE/not-observed, missing-vs-zero, distinct-id provenance,
structural route removal) pass, proving the adapter's repaired arithmetic still
works and the falsifiers are narrowly about the unresolved permission defects.

## Source pins

`02_PHASE_A_SOURCE_MANIFEST.json` re-derives Git NUL-blob SHA-1s from local
bytes and matches each to the T9C candidate commit
`9a33c2dcaa7ac0d50606416ab965488c9782934b` (repair payload
`d6e062684ca34b99ee9713c8c0affa0ed5c27f25`). Seven files: `t9b_temporal.py`
(`fd492a970ba2`), `test_t9c_repair.py` (`26a258a8581b`), and five
`ddm_v553_*` native modules.

## Phase B gate

T9D is `FUTURE_NOT_YET_RETURNED`. After its exact remote push is verified, pin
its source under a separate `phase_b/` subtree (never overwriting Phase A) and
execute: original V553 8, historical author 28, unchanged T9I 48, T9R frozen
delta 50, T9C author 52, this preregistered 17, plus any new independent
controls — in fresh processes with pinned imports, JUnit and exit status. A
repaired safer contract may intentionally invalidate old positive assertions
that demanded the old unsafe open-route output; keep those historical assertions
intact and explain the difference rather than weakening them.

No real EE12, N9, OC05, N11/N12, Sorok actor, V3, source35 U/Epre or method
adoption is granted by Phase A or by any green author test.
