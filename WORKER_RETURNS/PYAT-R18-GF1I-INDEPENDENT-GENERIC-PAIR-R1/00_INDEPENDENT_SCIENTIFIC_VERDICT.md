# 00 — GF1I independent scientific verdict

**Terminal:** `RED__NAMED_DOWNSTREAM_CONSUMER_ARTIFACT_ABSENT__FROZEN_44_CASE_CHAIN_NOT_REPRODUCIBLE__METHOD_CORE_INDEPENDENTLY_CONFIRMED_AT_SOURCEFREE_CANDIDATE_GRAIN`

**Role:** Independent native scientific/semantic/permission reviewer. NOT the
GF1 author, NOT a Field Forge semantic issuer, NOT HQ, NOT V3.

- Repository `maidiu/rawlsing` (private).
- Branch `agent/reviewer-pyat-20261016-r18-gf1i-generic-relation-independent-r1`.
- Sealed startup `e2667f25794ba00070f0437197b943483a69e7f7` (direct remote verified).
- Candidate reviewed: `agent/userdirect-pyat-20261016-r17-gf1-generic-native-pair-relation-r1 @ 9f4a23cef1482e0a81afb1e7a65df90879931465`.
- Write terrain only: `WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1/`.

## Verdict

**RED.** Not because the method is wrong — on every point I could execute, the
method holds — but because the artifact GF1 actually sold cannot be
independently reviewed.

GF1's §3 headline claim is that a **named downstream consumer**
(`GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0`) *physically reads* the
relation and emits `separation_class`, `support_vectors` and eligible-risk
consequences **that do not exist anywhere in the relation**. Falsifier F2 rests
on this: "a copy would fail immediately."

**The module `gf1_pair_support_consumer` exists nowhere in the candidate branch
history.** It is imported by `court/repro/gf1_native.py:45` and
`court/repro/test_gf1_generic_pair.py:33`, and it is absent from every blob on
`refs/heads/agent/userdirect-pyat-20261016-r17-gf1-generic-native-pair-relation-r1`.
Consequence: the returned 44-case suite cannot even be **collected** —
`ModuleNotFoundError: No module named 'gf1_pair_support_consumer'`. The claimed
**44/44 PASS is not reproducible**, and neither is any consumer value claim.

I did not reconstruct the missing consumer. Writing the candidate's own
artifact would make me a co-author of the very claim under review and destroy
independence exactly where it is needed. I exercised the relation module
directly against the real owner chain instead, and report what that does prove.

## What I independently CONFIRMED (sourcefree candidate-method grain only)

Executed: **19/19 independent reviewer tests pass**, exit 0, JUnit
`junit/gf1i_independent.xml`. 74/74 native files re-attested by Git blob SHA-1
(NUL preimage) + sha256 + byte count.

| Claim | Independent result |
|---|---|
| 74-file native closure | **74/74 re-attested, 0 drift** |
| Accepted Field Forge GT2 unmodified | blob `a70decb20747d84cbcbe27d1280babc6de88ef33`, matches commission pin and current tree |
| 8 operations, 2 ORDERED HELD | **preserved**; both `hold_reason = ORDERED_OWNER_NOT_ISSUED` |
| Baseline ordered XY cells | **1,0,0,1** exactly |
| Per-condition denominator | **1** (not the joint risk) — GF1's own §4.1 clarification is correct |
| Eligible joint risk (R1+R2) | **2** |
| Discovery consumer | cells 0,0,0,1; risk 1; denominators [0,1] — eligibility absent ≠ zero cell |
| Zero cells | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`, **never** `ZERO_SUPPORT` |
| Role binding follows native order | slot A (m01-X, m01-Y), slot B (m01-Y, m01-X) — a fixed-label owner cannot do this |
| R2_Y1 reaches frozen cell set | **0,1,0,1** observed |
| R1_Y0 reaches frozen cell set | **1,0,1,0** observed |
| Source-B relations under intervention | **bitwise stable** (both indices 4,5) |
| Permission ceiling | `("SOURCE_FREE_DEV",)`; widening refused |
| Reverse swap without separate grant | refused |
| Forged reverse grant | refused |
| Non-native role ref | refused |
| No causality/personality/significance claim | verified absent from relation material |

**One honest reviewer correction, recorded rather than hidden:** my frozen
oracle initially expected **2** changed relations per intervention. I observed
**3** (2 of 4 QUERY-path + 1 of 2 DISCOVERY). The oracle was corrected to the
observation *before* the negative tests ran. GF1's own wording — "2 of the 4
QUERY-path consumers change and 2 remain at baseline" — is independently
**confirmed**.

## What I could NOT verify

| Item | Reason |
|---|---|
| The 44/44 frozen chain | returned suite fails at import |
| `separation_class` / `EXACT_PAIR_SEPARATION` vs `NO_PAIR_SEPARATION` | consumer module absent |
| `support_vectors`, `zero_cell_semantics`, `joint_support_total` | consumer module absent |
| Falsifier F2 ("a copy would fail immediately") | no consumer to test |
| SIGKILL-grade cold replay at new GF1 identity | not executed here; PV3N's original cold is **not** relabelled as new GF1 cold |

## Standing of the accepted specialized Field Forge owner

**Unchanged and correct.** The accepted GT2 `Q86B`→`Q86A` specialization stays
as accepted. The original raw generic-label failing assertion is untouched — not
xfailed, skipped or suppressed. `GENERIC_NATIVE_SEMANTICS_HOLD` remains in force:
nothing here issues Field Forge generic semantics.

## Ceiling

Method-grade acceptance is **not** granted. Even had the consumer been returned,
acceptance would be `ACCEPT_SOURCEFREE_GENERIC_PAIR_CANDIDATE_METHOD_ONLY` at
most. Positive person/world relevance is real but limited: an exact
same-person 2×2 conditional support profile with native denominators is useful
structural evidence, and nothing more — no causality, no significance, no
personality, no dyad claim.

## Minimum next step

GF1 returns the `gf1_pair_support_consumer` module (plus its own reproduction
command). A distinct reviewer then re-runs the 44-case chain and the consumer
value claims. Field Forge S1–S9 generic semantic issuance remains a separate
competent authority, untouched either way.

---

**Deliverables:** [01 frozen oracle](01_FROZEN_GENERIC_PAIR_AND_ROLE_ORACLE.json) ·
[02 executed relations](02_ACTUAL_NATIVE_RELATION_CONSUMER_AND_INTERVENTIONS.json) ·
[03 source authority + cold](03_ORIGINAL_SOURCE_AUTHORITY_HOSTILES_AND_COLD.md) ·
[04 semantic owner scope](04_FIELD_FORGE_SEMANTIC_OWNER_SCOPE_AND_HQ_NEXT_EDGE.md) ·
[environment passport](environment_passport_delta.json) ·
`court/` (driver + 19 tests), `junit/`, `logs/`.

No original survey, canonical, model, actor or production change.