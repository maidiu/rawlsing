# PYAT R29 GF1G — TRULY INDEPENDENT PAIR-CONSUMER COURT — VERDICT

**Verdict: HOLD — bounded scientific RED at the consumer's inconsistent-input and
typed-state boundary; the genuine 2×2 computed core is independently reproduced and
sound. Not HQ-accepted. A narrow author patch is required before any acceptance.**

Reviewer: fresh independent session (DeepSeek V4.1 Flash in DSH), **not** the GF1E author,
**not** the GF1F prior reviewer (which was the same persisted session as GF1E), **not** HQ.

---

## 0. Independence attestation

- This is a new, separate model session. I have not read the GF1E author's conversation,
  the GF1F observed results, or any same-session history from those workers before my freeze.
- I read only the GF1G commission, Pyat 00D and Sorok 00C, the pre-GF1E R17 commission and
  precommitted contract, the R23 GF1C recovered consumer contract, the unchanged original 44
  specification, and the pre-GF1E producer owner at `9f4a23cef`.
- I verified the GF1E consumer blob identity (`git blob 75670c69…`, SHA-256 `06dd484b…`,
  matching the declared hash) **without reading its content**, then committed and pushed my
  own oracle and precommitted tests (Phase A freeze `ecd975ad5`, remote-verified) before
  Phase B.
- I did not mutate GF1E code, the frozen 44, the GF1F suite, or any accepted production module.

## 1. Phase A — independent freeze (pushed before GF1E inspection)

`01_FROZEN_ORACLE.json` was derived from the pre-GF1E court with an independently written
reference consumer (`phase_a/reference_consumer/`), not from GF1E:

- genuine 2×2 baseline `(00,01,10,11)=(1,0,0,1)`, `R2_Y0→1` and `R1_Y1→0` interventions in both
  native orientations, and BOUNDED_DISCOVERY;
- reverse `X|Y` vs `Y|X` under its own grant (roles swapped, distinct object identity, same counts);
- four separation classes with explicit definitions;
- positive / zero / missing / suppressed risk, observed-zero vs `ZERO_SUPPORT`;
- source-role identity, counts, per-condition denominators, eligible risk, nontrivial
  distributions (`(2,1,1,2)→NO`, `(2,0,0,2)→EXACT`);
- exact relation identity hashes and reference-relative consumer result hashes;
- inconsistent `condition_denominator_support` vs `sum(target_counts)` → typed rejection;
- support exceeding eligible risk → typed rejection;
- fully rehashed, internally consistent, externally unauthenticated relation.

The unchanged original 44 passed against the reference consumer (44/44), and the precommitted
independent suite passed against it (26/26) — the oracle and tests are internally valid before
GF1E is seen.

## 2. Phase B — physical results (GF1E at verified identity)

| suite | command domain | result |
|---|---|---|
| unchanged original 44 | staged GF1E court, no edits | **44 passed** |
| GF1G precommitted independent suite | staged GF1E consumer | **17 passed, 9 failed** |
| inherited GF1I 19 | closure extracted, GF1E consumer seated | **17 passed, 2 failed** — the two historical "consumer absent" tests, correct new behaviour, **never green** |
| GF1F 100 (regression only) | GF1F return, consumer SHA `06dd484b…` | **100 passed**, but same-session as GF1E → regression, not independent evidence |
| real cold processes | two OS processes, PIDs 18527 / 18528 | distinct PIDs, identical imported consumer SHA `06dd484b…`, identical relation identity and result hash |

Genuine-relation reproduction (passed): exact producer `content_hash`/`object_id` for baseline,
both interventions, discovery and reverse; classes, denominators, totals, zero-cell semantics,
role order, reverse grant gating, F2 non-copy, result-hash determinism, and forged-identity
TEST_ONLY retention.

## 3. Independent findings

### F1 — inconsistent denominator is silently accepted (**substantive RED**)
A fully rehashed relation with `condition_denominator_support = 2` for a condition whose target
counts sum to `1` is consumed as `EXACT_PAIR_SEPARATION`, `downstream_value_produced=True`, with
`joint_support_total=2`. The relation object constructor admits the contradiction; GF1E performs
no `denominator == sum(target_counts)` check. This is exactly the hostile the commission requires
to be typed-rejected before the consumer (or HELD if unexpressible). It is expressible and not
rejected.

### F2 — support exceeding eligible risk is silently accepted (**substantive RED**)
A relation with `joint_support_total=2` and `eligible_joint_risk_total=1` is consumed as
`EXACT_PAIR_SEPARATION`. No risk-bound check exists.

### F3 — negative support accepted, totals silently corrupted (**substantive RED**)
A rehashed cell with `raw`/`joint` count `-1` and another `+2` yields
`joint_support_total=1` and `UNDETERMINED_NO_ELIGIBLE_RISK`; counts are coerced with `int()`
without exact-nonnegative-integer validation. A zero/positive cell-state contradiction on a
rehashed profile is likewise not rejected by the consumer.

### F4 — missing / unresolved / nonresponse / zero-support states are mislabelled as valid empty (**HOLD-level RED**)
For a validly constructed blocking relation (`typed_state=MISSING_TARGET_STATE`,
`UNRESOLVED_TARGET_STATE`, `NONRESPONSE`, or `ZERO_SUPPORT`; `producer_state_blocking=True`;
empty profile) GF1E returns `RESPONSE_INPUTS_VALID_EMPTY` with no separation class. That
conflates missing/suppressed risk with a genuinely valid empty response. The empty-profile
branch is checked before the producer typed state.
- Note: the generic producer itself cannot emit a blocking relation with a profile (its
  constructor raises), so this is reachable only through the admissible object constructor and
  rehash — i.e. the same self-authenticated boundary as F1/F2/F3.

### F5 — the two UNDETERMINED classes are inverted at the boundary (**semantic HOLD**)
GF1E maps `eligible_joint_risk_total <= 0` → `UNDETERMINED_ZERO_SUPPORT_RISK`, and
all-zero support with eligible risk `2` → `UNDETERMINED_NO_ELIGIBLE_RISK`. The independent
definition is the reverse: no eligible risk members → `NO_ELIGIBLE_RISK`; eligible risk exists
but observed support is zero → `ZERO_SUPPORT_RISK`. This is a declared behaviour in GF1E's own
differential evidence, not an accident. It is unreachable from a genuine SUPPORTED producer fact
with positive denominator, so severity is lower than F1–F3, but it must be corrected or
explicitly owner-adjudicated.

### F6 — one precommitted failure is shape-only
`test_g13` (invalid input) confirms the contract state
`CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION`; it fails only because GF1E's refusal dict omits the
`separation_class` key. This is **not** a scientific RED.

## 4. Issuer authority — not expressible, and not claimed

The generic relation carries self-declared provenance/authority references and a recomputable
content hash; there is **no external signature or issuer-authentication field**. A fully rehashed
relation with fabricated provenance and authority is processed as a valid EXACT relation
(precommitted `test_g17` passes, relation content hash committed in the oracle). GF1E correctly
retains `production_owner_commit=False` and `GENERIC_NATIVE_SEMANTICS_HOLD=RETAINED` and grants no
real-source privilege — but it cannot distinguish a forged self-authenticated relation from an
authentic one. **Self-hash is not a signed issuer.** Qualified issuer authority is therefore not
expressible in the current relation/consumer schema; any acceptance is bounded to
`SOURCEFREE…TEST_ONLY` computed evidence, never semantic/Field Forge adoption.

## 5. What is independently established

- GF1E is a genuine **computed** consumer: it reads the relation object identity, derives
  vectors/totals/classes and a deterministic result hash; F2 non-copy holds; the seven
  downstream fields are absent from the relation material.
- The genuine 2×2 computation is correct and exactly reproducible: producer identities, classes,
  denominators, zero semantics, roles, reverse-grant operation and cold determinism all match
  the independent oracle.
- The reverse `X|Y` vs `Y|X` operation is correctly gated and role-derived from the native query.
- The unchanged original 44 is green; GF1I's substantive 17 are green; the two stale absence
  tests fail as correct new behaviour; GF1F 100 is a regression pass only.

## 6. Recommendation

**HOLD. Do not HQ-accept the consumer as-is.** The genuine computed core may be retained as
bounded `TEST_ONLY` evidence. Require a narrow GF1E-follow-up patch that:

1. rejects any row where `condition_denominator_support != sum(target_counts)`;
2. rejects `joint_support_total > eligible_joint_risk_total`;
3. validates exact nonnegative integers (no bool/float/negative/coercion) for counts and
   denominators, and cell-state consistency;
4. checks `producer_state_blocking` / `typed_state != SUPPORTED` **before** the empty-profile
   branch and returns a typed HOLD, reserving `RESPONSE_INPUTS_VALID_EMPTY` for non-blocking
   SUPPORTED empty profiles;
5. corrects or explicitly owner-adjudicates the `NO_ELIGIBLE_RISK` vs `ZERO_SUPPORT_RISK`
   mapping for the eligible-empty and zero-support boundary.

After the patch, re-run: unchanged 44, this precommitted 26, GF1I 19, and GF1F 100. Only then
consider bounded computed-consumer acceptance — still with no issuer, no original35, no
Field Forge S1–S9, no OC05/N11/N12/V3, no method adoption, and no HQ acceptance.

## 7. Non-grants

No original35, no Field Forge S1–S9, no OC05/N11/N12/V3, no HQ acceptance, no method adoption,
no U/E_pre issuance, no source permission. This review is bounded to the source-free computed
pair consumer.
