# RFA-06C2 owner-local successor execution — no automatic provider calls

Checkout assigned `agent/rabochii-sorok-r15-rfa06c2-quote-smoke-gate-repair-r1` and enter `SOROK_PRODUCT_CONTROL_ROOM/experiments/RENDERER_FEASIBILITY_R1/anthropic_cross_model_screen_r2`. Python 3.11+, locally pinned dependencies from `requirements.txt`.

**Preserve** `../anthropic_cross_model_screen_r1/EXPERIMENT_FREEZE_R1.json` and both existing `../anthropic_cross_model_screen_r1/results/raw/CM{SONNET,HAIKU}-SMOKE-A0001.json` files without changes. Also preserve all 60 R2 Opus results. Never copy these into Git. No assumption that private evidence is remotely available.

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest -v test_quote_and_smoke_r2
python3 validate_cross_model_court.py --expect-empty
python3 run_cross_model_court.py --freeze
python3 run_cross_model_court.py --reuse-existing-smokes
```

The last command performs an **offline two-phase receipt proof** (full original request and message SHA-256, frozen schema, fixture, model, effort, max tokens, API version, source packet hash/payload, unique provider response ID/raw content/original schema), then imports both JSON receipts append-only without modifying predecessor. `results/receipts/EXISTING_SMOKE_REUSE_PROOF_R2.json` contains the local disposition. If predecessor freeze/receipts are absent, mismatched, or ambiguous, it fails closed without calling Anthropic. Do **not** compensate by silently regenerating smoke.

A historically `STRUCTURAL_INVALID` smoke that is parsed, original-schema-valid, exact-model, exact-fixture and request-bound may pass transport eligibility; its historical status remains unchanged in the imported record and corrected issues are in the local reuse proof. Only owner-confirmed exact Haiku shape warrants `FALSE_POSITIVE__QUOTE_DELIMITER_STYLE_ONLY`.

After both reuse gates PASS and only by explicit owner decision, the already committed call schedule is:

```sh
python3 run_cross_model_court.py
```

This one command can make **up to 40 billed primary calls**; do not run it as part of this commission. No Sonnet/Haiku smoke re-generation is required when proof passes. It retains the exact existing run order, requests and case/condition allocations.

After authentic 40 new primaries and all 60 original Opus receipts are available:

```sh
python3 run_cross_model_court.py --build-blinded-bundle
python3 validate_cross_model_court.py --require-complete
python3 score_and_unblind.py --prepare
# After blind reviewers independently supply all 60 x 15 scores:
python3 score_and_unblind.py --seal
python3 score_and_unblind.py --verify-seal
# Separate authorized step ONLY:
python3 score_and_unblind.py --unblind
```

Never score the smoke as primary, never import older R1 diagnostic candidates, never repair generated candidates, never change historical Opus receipts, and never expose private blind mappings to scorers. Legacy RFA-06C status files remain unchanged.
