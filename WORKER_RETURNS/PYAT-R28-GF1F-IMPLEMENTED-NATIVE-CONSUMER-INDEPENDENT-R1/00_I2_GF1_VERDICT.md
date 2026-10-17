# GF1F — independent computed pair-consumer verdict

**Verdict: `PASS_SOURCEFREE_BOUNDED_GENERIC_PAIR_CONSUMER_METHOD_ONLY`** — the
GF1E consumer genuinely computes the downstream pair-support signature from an
authentic `GenericNativePairRelation`, the original frozen44 is unchanged and
green, my independently frozen 81-relation universe and eight named cases all
match, the F2 non-copy falsifier binds, forged/mutated relations are refused,
the reverse X|Y operation is a distinct computed value, and a two-process cold
replay is bit-identical. No Field Forge S1–S9 semantic issuance, original
source35 grant, OC05, N11/N12 or actor activation is made.

**Candidate under review:** `agent/rabochii-pyat-r27-gf1e-actual-native-consumer-implementation-r1`
@ `eeb726357204653b22458dc267dd70ba0009bd77` (direct remote readback verified).
Consumer `gf1_pair_support_consumer.py` sha256
`06dd484b0e9b4b2c9fb0a1583453ac7ffa8c052135304eaaee167a34127cb402`.

## Independence disclosure

This reviewer is a **different model/agent** (DeepSeek V4 Flash) from the GF1E
implementer (DeepSeek V4 Pro), but **the same persisted session**: the prior
turns of this session authored the GF1E consumer. The session-continuity
limitation is real and is disclosed here rather than claimed away. The
scientific mitigations are: (a) a NEW 81-element 2x2 universe and eight named
cases were derived from first principles and frozen in
`01_INDEPENDENT_FROZEN_PAIR_ORACLE.json` **before** running the consumer on them;
(b) the reviewer wrote its own relation builder and did not reuse the author's
differential helpers; (c) the F2 non-copy falsifier, mutation attacks and cold
replay are independent constructions.

## Executed courts

| Court | PASS | FAIL | ERROR | SKIP | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| **GF1F independent court (81 universe + 8 named + F2 + 6 mutations + refusal + missing + reverse + cold)** | **100** | 0 | 0 | 0 | 0 |
| Original frozen44 (byte-unchanged) | 44 | 0 | 0 | 0 | 0 |
| GF1E author differential+cold (regression grade only) | 9 | 0 | 0 | 0 | 0 |
| Prior GF1I independent19 (where runnable) | 17 | 2 | 0 | 0 | 1 |

The GF1I two failures are its two **RED assertions that GF1E resolved**: "named
consumer module is absent" and "frozen44 cannot be collected". Both now fail
because the consumer exists and the frozen44 collects — that is the positive
closure of the prior RED, not a defect.

## What was independently established

* **All four separation classes** are computed, not copied: the first-principles
  81-relation universe splits into EXACT 8, NO_PAIR 56, UNDETERMINED_NO_ELIGIBLE
  16, UNDETERMINED_ZERO_SUPPORT 1, every one matching the frozen oracle.
* **Per-cell support, denominators and joint total** are recomputed from the
  profile and match the reviewer's own 2x2 derivation.
* **F2 non-copy binds**: none of `separation_class`, `separation_signature`,
  `support_vectors`, `zero_cell_semantics`, `joint_support_total`,
  `condition_states_with_positive_denominator`, `result_hash` appears in
  `relation.as_dict()`, and the consumer produces them.
* **Forged identity** (object_id, content_hash, one cell, risk denominator, role
  order changed) is rejected at relation construction without recompute.
* **Frozen bypass** (`object.__setattr__` mutation) is caught by the consumer's
  identity re-derivation and refused `CONSUMER_RELATION_IDENTITY_MISMATCH`.
* **Reverse X|Y vs Y|X** is produced by the real producer under its own
  `REVERSE_PAIR_GRANT_ID`; the consumer computes a distinct
  `separation_signature`/`result_hash` for the reverse, neither is a fixture echo.
* **Missing/suppressed** (`typed_state=MISSING_TARGET_STATE`, empty profile) is
  `RESPONSE_INPUTS_VALID_EMPTY` with `downstream_value_produced=False`.
* **Cold replay**: two fresh OS processes give bit-identical results with
  distinct PIDs and exercise all four classes.
* The real native baseline relation yields `EXACT_PAIR_SEPARATION` with the
  `1/0/0/1` cells.

## Limits (stated, not hidden)

* A **fully recomputed** forged relation (mutate a field AND recompute
  `content_hash`) is internally consistent and the consumer cannot distinguish
  it from a legitimate relation — the sourcefree fixture carries no issuer
  signature. The commission's attack ("without recomputing the original signed
  native relation") is the mutation-without-recompute case, which is refused.
* The consumer does not cross-check each `condition_denominator_support` against
  the sum of its `target_counts`; the real producer always makes them consistent,
  and an inconsistent recomputed relation is outside the commissioned attack.
* No original source, Field Forge S1–S9, OC05, N11/N12, actor, V3 or method
  adoption is granted or exercised.
