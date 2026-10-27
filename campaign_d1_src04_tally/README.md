# D1 — SRC04 observed-sample tally

This bounded campaign consumes the accepted local original SRC04 C11 release
`fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec` and emits a
source-native descriptive tally over the exact 42 accepted response fields.

## Product

Counts are aggregate only. For each field the product records:

- source-variable / question / response-slot identity;
- exact native-value counts and state-specific native-value counts;
- source-record denominator (7,337);
- observed-response denominator (recorded `SUBSTANTIVE_RESPONSE`, `DK`, `REFUSAL`
  or `SOURCE_SPECIFIC_SPECIAL` states);
- answered-substantive denominator;
- missing / non-observed accounting;
- exact response topology and single-component identity.

Event presence is **not** treated as an answered question. Counts are conditional
on recorded response availability, not eligibility or population.

The product preserves `ROUTING_UNKNOWN` and the original `DEFER` canonical
authority. A narrow negative exercises the existing authority gate against one
`DEFER` snapshot from the same release, then restores the exact descriptive tally.
It contains no weights, canonical scale, signed direction, eligibility,
population, causal or downstream scientific claims.

## Commands

```sh
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode primary
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode tests
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode replay
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode return \
  --artifact-commit <code-commit>
```

`primary` reads only the accepted local C11 bundle and committed Campaign A
metadata; it never opens the original SAV. The exact TRUE-HQ grant and governing
program are committed as pinned evidence copies under
`campaign_d1_src04_tally/evidence/`, so the portable primary/replay path has no
author-private `.r61` dependency. `replay` rebuilds the product in a fresh process
and compares every field count. `return` assembles `RETURN.json`.

Local respondent-bearing objects remain outside Git. Only aggregate counts,
exact refs, negatives and replay evidence are committed.
