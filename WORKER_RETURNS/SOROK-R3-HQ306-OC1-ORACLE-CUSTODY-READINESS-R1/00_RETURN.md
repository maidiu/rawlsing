# SOROK HQ306 OC1 — Independent Oracle Custody and Experimental Readiness

**STATUS: SOURCEFREE_DUMMY_CUSTODY_PROTOCOL_EXECUTED** · REAL_INDEPENDENT_ORACLE_ISSUANCE=HOLD · LIVE_MODEL_USE=NOT_GRANTED

**Branch:** `agent/rabochii-sorok-r3-hq306-oc1-custody-readiness-r1`  
**Sealed startup:** `3b0680c3b342137d334d55f6051b762715a63dd9`  
**Model:** Muse Spark (owner-configured) · **Editor:** Muse code editor (existing authorized)  
**Network/model calls:** 0 · **Provider requests:** 0 · **Survey data reads:** 0

---

## 1. Deliverable summary

Built and executed a sourcefree custody-readiness protocol that separates scenario authors, semantic adjudicators, oracle custodians, experiment runners, blind response coders and competent grant issuers. All content is fictional/test-only. No real model calls, real oracle issuance, production owner changes, provider permissions, V3 actors or adoption occurred.

### Role separation and conflict graph

| Role | Conflicts with | Purpose |
|---|---|---|
| SCENARIO_AUTHOR | CUSTODIAN, EXPERIMENT_RUNNER, BLIND_CODER, SEMANTIC_ADJUDICATOR | Constructs fictional scenarios |
| SEMANTIC_ADJUDICATOR | SCENARIO_AUTHOR | Resolves contested lawful choices |
| CUSTODIAN | SCENARIO_AUTHOR, EXPERIMENT_RUNNER, BLIND_CODER, GRANT_ISSUER | Unblinds and releases holdout capsules |
| EXPERIMENT_RUNNER | SCENARIO_AUTHOR, CUSTODIAN, BLIND_CODER, GRANT_ISSUER | Runs experiments |
| BLIND_CODER | SCENARIO_AUTHOR, CUSTODIAN, EXPERIMENT_RUNNER | Codes responses without arm/answer labels |
| GRANT_ISSUER | CUSTODIAN, EXPERIMENT_RUNNER | Issues model-use grants (all fields NOT_ISSUED) |
| ACCEPTANCE_REVIEWER | (independent of all above) | Final acceptance review |

**Second-signature requirement:** Two distinct persons with non-conflicting roles must sign the same content. Same-person signatures and conflicting-role signatures are refused.

### Mock signer disclaimer

All signatures use ephemeral TEST_ONLY fixture credentials with a transparent verification root (`TEST_ONLY_EPHEMERAL_ROOT`). A mock signer does NOT create real independent custody. Hash equality is NOT independent semantic agreement. The `custody_status` is `HOLD` even when fields look complete, because no real organizational custodian or external signature registry exists.

---

## 2. Dummy corpus and escrow

12 fictional test-only scenarios across 4 families (FAM-00 through FAM-03), 3 cases per family. Each case carries:
- `case_id`, `family_id`, `blind_id` (opaque UUID), `k_label` (K1–K6)
- `facts_digest`, `lawful_answers` (always includes `OTHER_UNSCORABLE`)
- `hidden_origin_digest` (sealed, never in model-visible packets)
- `public_projection_digest` (visible to model)

**Escrow lifecycle:** `commit` → `unblind` → `release` with full ledger integrity. Post-freeze edits are refused. Exposure logging records every unblinding. Premature release without unblinding is refused.

**Leakage detection:** `assert_no_leakage()` checks every model-visible packet and coder input against a token set covering `answer_key`, `hidden_origin`, `oracle_digest`, `arm`, `contrast`, `expected_answer`, `expected_result`, `provider`, `desired_result`, `case_id`, `family_id`, `blind_id`, `k_label`. Any leak is a hard `LeakageError`.

---

## 3. Hostile validation (22 negative tests)

| ID | Attack | Result |
|---|---|---|
| h01 | Forged custodian signature | REFUSED |
| h02 | Same-person conflicting roles | REFUSED |
| h02b | Same-person second signature | REFUSED |
| h02c | Conflicting-role joint signature | REFUSED |
| h03 | Scenario/oracle identity mismatch | REFUSED |
| h04 | Wrong purpose | REFUSED |
| h05 | Stale/revoked capsule | REFUSED |
| h06 | Revised answer after freeze | REFUSED |
| h07 | Clone family detection | REFUSED |
| h08 | Blind-ID pairing break | REFUSED |
| h09 | Hidden-origin leak | REFUSED |
| h10 | Answer-key leak | REFUSED |
| h11 | Premature reveal | REFUSED |
| h12 | Null signature | REFUSED |
| h13 | Ledger rollback | REFUSED |
| h14 | Response-coding leak | REFUSED |
| h15 | Missing signature | REFUSED |
| h16 | Capsule wrong purpose | REFUSED |
| h17 | Model-visible packet leak | TEST_ONLY_PASS |
| h18 | Exposure logging | TEST_ONLY_PASS |
| h19 | Non-test-only signature | REFUSED |
| h20 | Family graph digest | TEST_ONLY_PASS |

**22/22 PASS** (20 REFUSED + 2 TEST_ONLY_PASS)

## 4. Positive lifecycle tests (9)

Full role-separated escrow round-trip, no-leakage model packets, coder input without arm/answer labels, role separation enforcement, `OTHER_UNSCORABLE` in all lawful sets, deterministic capsule digests, verifiable mock signatures, purpose gate, blind-ID pairing.

**9/9 PASS**

---

## 5. Lawful-set and coding governance (proposed, NOT issued)

- **Multi-valued lawful answers:** A choice between lawful options is NOT automatically a quality improvement. `OTHER_UNSCORABLE` is always present.
- **Contested lawful choices:** A disputed key goes to the competent semantic owner with blinded alternatives and provenance. Confirmatory analyses stay HOLD for unresolved keys.
- **K3 origin secrecy:** Hidden origin content NEVER appears in model-visible packets or coder inputs.
- **K5 public vs private:** Public standing and private belief are separate typed fields. A public position change does NOT overwrite private belief.
- **K6 position/capacity:** K6 requires actual position/capacity evidence. POLICING_CANDIDATE and NO_SANCTION are both lawful when practiced+capacity is present.
- **Blind prose coding:** Deterministic typed coding. Ambiguous output is `OTHER_UNSCORABLE`. Arbitrary prose requires a separately reviewed key-blind rubric.
- **Appeal mechanism:** Any player may appeal a coding decision to the ACCEPTANCE_REVIEWER (distinct from BLIND_CODER and EXPERIMENT_RUNNER). Resolution timeline: 30 days. Decision is binding and versioned.
- **Semantic owner nonnegotiable rights:** Semantic owner alone may approve/reject lawful sets and resolve contested choices. Custodian alone may unblind/release holdout capsules. Experiment runner may not edit capsule content after freeze. Blind coder may not see arm/provider/expected answer/desired result.

**This worker constructs examples and tests. It does NOT issue accepted law, independent scenario validity, or a protected real test corpus.**

---

## 6. Prospective statistics and grant frontier

### Formula verification (independently recomputed)

| Bound | Formula | Inputs | Computed n | BL3 claim | Verified |
|---|---|---|---|---|---|
| 5pp half-width | `n ≥ ceil(2·log(2m/α)/ε²)` | α=.05, m=12, ε=.05 | 4,940 | 4,940 | ✓ |
| 10pp superiority 80% | `n ≥ ceil(2·(√log(2m/α)+√log(1/β))²/g²)` | α=.05, m=12, β=.2, g=.10 | 2,818 | 2,818 | ✓ |
| 5pp equivalence 80% | `n ≥ ceil(2·(√log(2m/α)+√log(2/β))²/ε²)` | α=.05, m=12, β=.2, ε=.05 | 12,814 | 12,814 | ✓ |

All three figures are **conditional worst-case sufficient bounds** under independent-family sampling and range-2 concentration assumptions. They are NOT approved sample sizes, NOT achieved power, NOT spending recommendations.

### Family-unit crisis

6 convenience families + 28 template clones do NOT establish independent sampling. The independent unit is the family, not the trial. Families from the same template/author/causal structure are correlated. **Population inference remains HOLD.**

### Per-provider cost: UNKNOWN (no live provider call made)

### Proposed economical pilot (owner consent required)

~50 independently sourced families for ICC/variance estimation. Needs ICC model, cost model, and separate owner consent.

### Model-use grant frontier: ALL 8 REQUIRED FIELDS NOT_ISSUED

`named_provider_exact_endpoint`, `exact_model_and_version_pin`, `privacy_permission_for_synthetic_lab_packets`, `experiment_use_grant_behavioral_actor_trials`, `explicit_monetary_cap`, `price_class_and_quota_observed`, `raw_request_response_retention_permission`, `per_trial_call_budget` — all NOT_ISSUED. Provider adapter NOT_IMPLEMENTED.

---

## 7. Frozen negative expectations

Frozen before code execution: `frozen_negative_expectations.json` (22 negative + 9 positive = 31 total). All 31 executed tests matched expected results.

---

## 8. Source/identity/hash manifest

| File | SHA-256 (first 16 hex) |
|---|---|
| `repro/custody_protocol.py` | computed at return |
| `repro/dummy_corpus.py` | computed at return |
| `repro/test_custody_hostiles.py` | computed at return |
| `repro/test_positive_lifecycle.py` | computed at return |
| `repro/stats_critique.json` | computed at return |
| `repro/lawful_set_governance.json` | computed at return |
| `frozen_negative_expectations.json` | computed at return |

Prior freeze SHA256s preserved and never mutated: R3 v1 `b0d44f663e2392a4207c28a331e5a7627cfef81bdc8b47e9240642161977f465`, R2 v6 `9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823`, R1 `880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330`.

---

## 9. Owner actions remaining for HQ

1. **Appoint a real independent semantic custodian** — distinct from scenario author and implementer. Not a mock signer.
2. **Issue competent lawful-set approval** — semantic owner must approve event admission, access rules, K3/K5/K6 constructs.
3. **Implement external signature verification** — trusted registry of externally controlled public keys (e.g. Ed25519) with context-bound signatures.
4. **Establish truly protected sealed holdout custody** — separate access-controlled environment. Commitments alone do not hide a JSON file readable by the implementer.
5. **Adopt prospective sampling/power design** — independent statistician verification; ICC/variance pilot; cost model.
6. **Issue all 8 model-use/privacy/spend/retention grant fields** — competent issuer must actually authorize exact purpose, packet disclosure, retention, max attempts/retries and cost under a current pin/expiry/revocation policy.
7. **Commission provider-adapter validation** — separate commission for named immutable endpoint/model, privacy/retention behavior, serialization, stateless isolation, raw capture, cost reservation/attempt limits, retry discipline and fail-closed ledger.
8. **Commission independent acceptance review** — after this complete return, distinct from this OC1 implementer.

---

## 10. Scientific limitations (explicit)

- **No real independent oracle custody exists.** A mock signer does not create organizational independence. Hash equality is not semantic agreement.
- **No real model calls were made.** Zero experimental model calls, zero provider requests.
- **No population inference.** 6 convenience families + 28 clones are not independent draws. Intervals are descriptive only.
- **No approved sample sizes.** Hoeffding/Bonferroni bounds are planning tools, not targets.
- **No V3/N12 wake, no production owner changes, no real survey data, no real signer keys, no adoption.**
- **This worker does not self-issue accepted law, independent scenario validity, or a protected real test corpus.**

---

## 11. Changed-path manifest

All writes confined to `WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/`:

- `00_RETURN.md`
- `frozen_negative_expectations.json`
- `environment_passport_delta.json`
- `repro/custody_protocol.py`
- `repro/dummy_corpus.py`
- `repro/test_custody_hostiles.py`
- `repro/test_positive_lifecycle.py`
- `repro/stats_critique.json`
- `repro/lawful_set_governance.json`

---

## 12. Remote SHA verification

Verified by direct `git ls-remote` after push. SHA reported in the completion message (a commit cannot self-reference its own future SHA).
