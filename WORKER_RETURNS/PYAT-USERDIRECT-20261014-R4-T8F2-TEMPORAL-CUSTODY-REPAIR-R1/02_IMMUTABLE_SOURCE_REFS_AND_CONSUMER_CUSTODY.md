# Immutable Source Refs and Consumer Custody

## content_hash scope (all 18 WaveFact fields)

year, field_start/end, publication, question, version, refusal_code,
category_weights, special_weights, eligible/asked weights,
native_category_codes, national_weight, country_selector, population,
variance, variance_method, sample_identity.

A variance-only change yields a distinct hash and distinct ref_id; the old
ref still retrieves exactly its old fact (no overwrite: FACT_IDENTITY_COLLISION
on conflicting content under one ref_id).

## Registry guarantees

- Tuple-normalized at __post_init__ and registration: caller list mutation
  cannot corrupt stored facts.
- retrieve() verifies: schema, known ref, stored hash == ref hash,
  registry hash == ref hash, stored.year == ref.year, not revoked.
- revoke() marks ref_id; reads check revocation at consumer time.
- wave_refs carry source/version; registry authority is
  TEST_ONLY_TRUSTED_REGISTRY@1, never EE12.

## Consumer custody

consume_registered() takes (registry, product). It dereferences both refs
from the supplied registry, recomputes every primitive from retrieved facts
(categories, specials, weights, shares, delta, variance sum), checks the
authoritative publication clock, asof, revocation, category-0 presence, and
the caller digest. No positive rests on a caller digest alone.
