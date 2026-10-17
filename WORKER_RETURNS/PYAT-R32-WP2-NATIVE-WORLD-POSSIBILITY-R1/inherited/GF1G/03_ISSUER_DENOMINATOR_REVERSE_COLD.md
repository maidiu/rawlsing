# GF1G — ISSUER, DENOMINATOR, REVERSE, AND COLD EVIDENCE

Bounded source-free computed-consumer level. No original35, no Field Forge S1–S9, no
OC05/N11/N12/V3, no HQ acceptance, no method adoption.

## 1. Inconsistent per-condition denominator — the decisive hostile

**Constructed relation (TEST_ONLY, fully rehashed):** a valid baseline relation whose
`conditional_count_profile` is replaced by

| condition | denominator | target 0 | target 1 |
|---|---|---|---|
| `"0"` | **2** | 1 | 0 |
| `"1"` | 1 | 0 | 1 |

The counts sum to `1` in condition `"0"` but the row declares `2`. The object constructor
accepts it because the content hash is recomputed over the new projection; only the consumer
can refuse it.

**GF1E observed behaviour:** `decision_state = PAIR_SUPPORT_SIGNATURE_COMPUTED`,
`separation_class = EXACT_PAIR_SEPARATION`, `downstream_value_produced = True`,
`joint_support_total = 2`, `condition_states_with_positive_denominator = ["0","1"]`,
`result_hash` computed. The contradictory denominator is never compared with the counts.

**Why this is scientifically wrong:** the relation is internally contradictory. A downstream
"exact separation" claim computed from an impossible denominator is not an exact pair
separation; it is a data-integrity failure. The commission requires typed rejection before the
consumer, or a HOLD if unexpressible. The check is expressible in one line and absent. This is a
**substantive RED**, not a style issue.

**Related bound:** a relation with `joint_support_total = 2` and
`eligible_joint_risk_total = 1` is likewise consumed as `EXACT_PAIR_SEPARATION`; observed joint
support cannot exceed eligible risk.

**Negative count:** a rehashed cell `-1` plus `2` is coerced with `int()` into
`joint_support_total = 1` and `UNDETERMINED_NO_ELIGIBLE_RISK`; no exact-nonnegative-integer
validation exists. A zero/positive cell-state contradiction is similarly not refused by the
consumer.

**Missing / unresolved / nonresponse / zero-support:** a validly constructed blocking relation
(`typed_state` in `{MISSING_TARGET_STATE, UNRESOLVED_TARGET_STATE, NONRESPONSE, ZERO_SUPPORT}`,
`producer_state_blocking=True`, empty profile) is returned as
`RESPONSE_INPUTS_VALID_EMPTY`. That is a valid-empty response state, not a typed HOLD, and it
conflates missing/suppressed risk with genuine emptiness. The empty-profile branch is checked
before the producer typed state.

**Boundary class inversion:** GF1E maps `eligible_joint_risk_total <= 0` →
`UNDETERMINED_ZERO_SUPPORT_RISK`, and all-zero support with eligible risk `2` →
`UNDETERMINED_NO_ELIGIBLE_RISK`. The independent reading is the reverse. This is declared in
GF1E's own differential evidence (its zero-support pattern has `eligible_joint_risk_total=0`).

## 2. Issuer authority — not expressible, and correctly not claimed

The relation schema contains:

- `producer_authority_refs` / `producer_provenance_refs` — **self-declared references**;
- `content_hash` / `object_id` — a **self-hash** over the projection;
- no external signature, certificate, key identifier, issuer attestation, or verification
  material.

A fully rehashed relation with fabricated `producer_provenance_refs` and
`producer_authority_refs` is structurally indistinguishable from an authentic one. GF1E consumes
it as `EXACT_PAIR_SEPARATION`; it retains `production_owner_commit=False` and
`GENERIC_NATIVE_SEMANTICS_HOLD=RETAINED`, and grants no real-source privilege (precommitted
`test_g17` passes; forged relation content hash is frozen in `01_FROZEN_ORACLE.json`).

**Conclusion:** qualified issuer authority is **not expressible** in the current relation or
consumer schema. Self-hash is not a signed issuer. Any future issuer gate would need, at minimum,
an external signature over the semantic projection by an independently pinned issuer key, a
consumer-side verification step, and a key/authority lifecycle; none of that exists and none is
granted here. GF1E does not pretend otherwise, which is correct; the consequence is that HQ
acceptance cannot exceed `SOURCEFREE…TEST_ONLY` computed evidence on the strength of this
consumer alone.

## 3. Reverse X|Y vs Y|X

- Forward operation is `FORWARD_NATIVE_ORDER`; roles come from the actual native query
  (`m01-X` conditioner / `m01-Y` target in the PAIR slot, reversed in the B slot).
- A swap without authority raises `REVERSE_PAIR_GRANT_REQUIRED`; an unknown grant raises
  `REVERSE_PAIR_GRANT_UNKNOWN`.
- Under `REVERSE_PAIR_GRANT_ID`, GF1E's producer emits `REVERSE_GRANTED`, swaps the role variables
  and produces a **different relation object identity**
  (`…:sha256:652052461e95c276f27764f58aa6311e6cd3f3a9c357e08f7ce4941dc1a91d38` for the reviewed
  baseline orientation), with the same 2×2 counts and the same `EXACT_PAIR_SEPARATION` class.
- The independent oracle froze both forward and reverse identities; GF1E reproduced the exact
  producer hashes (precommitted tests g02/g03/g04 passed).

## 4. Cold-process evidence (real OS processes, distinct PIDs)

Two separate `python3` invocations of `cold/cold_child.py` against the verified staged GF1E court:

| process | PID | imported consumer file | SHA-256 | relation `content_hash` | `result_hash` |
|---|---|---|---|---|---|
| 0 | 18527 | `…/court/runtime_root/gf1_pair_support_consumer.py` | `06dd484b…` | `74d3aaac…` | `0b8ee8a6…` |
| 1 | 18528 | same | same | same | same |

- imported module resolves **inside the verified staged court**, not to any cached or external
  copy;
- 74 native blobs reattested in each process;
- relation identity `74d3aaaca35aaacc4491c7e472ac38a6e69fcf0d51736b86b853ea48d10b2236` exactly
  matches the independent oracle's forward m01-X relation;
- roles `m01-X | m01-Y`, cells `1/0/0/1`, denominators `1/1`, total `2`, class
  `EXACT_PAIR_SEPARATION`, zero cells preserved as `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`;
- `production_owner_commit=False`, `GENERIC_NATIVE_SEMANTICS_HOLD=RETAINED`.

## 5. Reproduction

```sh
# Phase A freeze (already pushed at ecd975ad5)
git archive 9f4a23cef \
  WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1 \
  WORKER_COMMISSIONS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1 \
  | tar -x -C /tmp/gf1g_pre
cp phase_a/reference_consumer/gf1_pair_support_consumer.py \
  /tmp/gf1g_pre/WORKER_RETURNS/…/court/runtime_root/
python3 phase_a/derive_oracle.py --court /tmp/gf1g_pre --out 01_FROZEN_ORACLE.json

# Phase B — original 44 (unchanged)
git archive eeb726357… WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1 \
  | tar -x -C /tmp/gf1g_stage_gf1e
cd /tmp/gf1g_stage_gf1e/WORKER_RETURNS/…/court/repro
python3 -m pytest test_gf1_generic_pair.py -q

# Phase B — precommitted independent suite
GF1G_COURT=/tmp/gf1g_stage_gf1e/WORKER_RETURNS/… \
GF1G_ORACLE=$PWD/WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1/01_FROZEN_ORACLE.json \
python3 -m pytest phase_a/test_gf1g_precommitted.py -q

# Phase B — cold processes
python3 cold/cold_child.py /tmp/gf1g_stage_gf1e/WORKER_RETURNS/…
```

## 6. Bottom line

The genuine 2×2 computed core, role derivation, reverse grant, F2 non-copy and cold determinism
are independently reproduced. The boundary is not safe: internally contradictory or forged
self-authenticated relations are computed as exact science instead of being typed-rejected or
held, and blocking typed states are mislabelled as valid empty. Because qualified issuer
authority is not expressible, the correct disposition is **HOLD** with a narrow author patch,
not acceptance.
