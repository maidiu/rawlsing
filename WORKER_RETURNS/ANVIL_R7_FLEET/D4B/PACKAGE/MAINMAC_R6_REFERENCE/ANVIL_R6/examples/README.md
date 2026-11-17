# Synthetic executable fixtures — NOT actual architectural results

`SYNTHETIC_PLAN.json`, `SYNTHETIC_MEASUREMENTS.json`, `SYNTHETIC_SPINE.json`, and `SYNTHETIC_COMPARISON_RESULT.json` are created solely to illustrate R6's typed document formats and exercise validation/rendering. They simulate 11 comparison cells with fabricated A/B advantages and fake independent-verification metadata; they do **not** establish ANY real source, hardware, review, economic, or science result.

The **actual campaign** must replace every source/runner/participant/receipt with immutable real refs, run actual qualified comparisons, and have C authenticate them independently. H1 requires real owner/CAS. These fixtures must not be submitted as ANVIL architectural evidence.

Run `python3 tools/r6.py check-plan examples/SYNTHETIC_PLAN.json` and `python3 tools/r6.py compare examples/SYNTHETIC_PLAN.json examples/SYNTHETIC_MEASUREMENTS.json` from the R6 root. Structural PASS only.
