# HQ305 BR3 — Independent R3 Synthetic Sensitivity Court

**Verdict: REVIEW_PASS_SCOPED_R3_SYNTHETIC_SENSITIVITY**

The BL3 R3 assay correctly detects a deliberately scripted arm-aware synthetic
response change under controlled read budgets, and correctly holds representation-blind,
position-only, metadata-only, menu-first, and ablation policies at zero. K3/K5/K6
adversary detections work. This is sourcefree measurement/plumbing sensitivity
evidence. It is NOT a behavioral treatment effect, LLM behavioral finding,
psychological truth, model-use permission, oracle custody, or adoption.

## Custody and independence

- Repository: `maidiu/rawlsing` (private)
- Branch: `agent/reviewer-sorok-r3-hq305-br3-synthetic-sensitivity-independent-r1`
- Sealed startup: `4085cb26be27977c0ec9afc5fc1b7ef96f400029`
- Candidate BL3: `10b507af06973657f2d772b636fb6fbd2d6aff36`
- This reviewer is distinct from BL3 author (Codex GPT-6.1 High) and RBA author
  (Muse Spark). This reviewer (Muse Spark) has no channel correlation with either.
- Runtime staged from pinned Git objects via independent staging script. All
  70 staged entries verified by Git blob SHA-1 (NUL preimage). No author
  staging code executed.

## Freeze verification

- R3 v1 SHA256: `b0d44f663e2392a4207c28a331e5a7627cfef81bdc8b47e9240642161977f465`
  verified byte-identical at first read.
- R2 v6 SHA256: `9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823`
- R1 prereg: `880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330`
- No frozen oracles modified.

## Exact execution

| Suite | Result | Source |
|---|---|---|
| R3 tests | 33/33 PASS | BL3 `tests/test_r3.py` |
| R2 suite | 51/51 PASS | RBA `exec/r2/test_r2.py` |
| RBA hostiles | 19/19 PASS | RBA `hostile/test_hostile_rba.py` |
| LAB1 | 20/20 PASS | RBA `exec/lab1/lab/test_lab.py` |
| LAB2 | 25/25 PASS | RBA `exec/lab2/lab2/test_lab2.py` |
| RMB | 13 PASS / 23 RED | RBA `exec/rmb/test_independent.py` (original split preserved) |
| BR3 independent attacks | 15/15 PASS | `repro/test_br3_attacks.py` |
| Schedule | 9432 trials, 3144 blocks, all 6 orders = 524 | Verified |
| Capture integrity | No unplanned IDs | Verified |

## Independent attacks (reviewer-origin)

| ID | Attack | Result |
|---|---|---|
| i01 | Representation actually read (aware reads, blind does not) | PASS |
| i02 | Aware positive contrast present in sampled blocks | PASS |
| i03 | Blind null exactly zero across all blocks | PASS |
| i04 | No answer key in decoded representation | PASS |
| i05 | Facts/menu/trial-id alone insufficient (zero contrast) | PASS |
| i06 | K3 origin attack detected | PASS |
| i07 | K5 standing attack detected | PASS |
| i08 | K6 capacity attack detected | PASS |
| i09 | Position-only no systematic positive | PASS |
| i10 | Schedule order balance (6 orders x 524) | PASS |
| i11 | Full-information ablation kills contrast | PASS |
| i12 | Metadata-only no positive | PASS |
| i13 | Menu-first no positive | PASS |
| i14 | Capture integrity (no unplanned IDs) | PASS |
| i15 | Two lawful response alternatives (menu-consistent) | PASS |

## Scientific assessment

The representation-sensitive synthetic policy demonstrates that changing the
representation alone changes the typed output under a one-record read budget.
When the representation is ablated (empty entries), contrast vanishes. The
blind policy is exactly null. Position, metadata, and menu-first policies show
zero contrast. This is genuine plumbing/measurement sensitivity for the assay
infrastructure.

**Not established:** real LLM behavioral effect, treatment superiority,
psychological ontology, population inference, model-use permission, scenario
independence, actual human experience, V3 readiness. The scripted responder is
a test instrument, not a model of empirical LLM attention.

## Statistical design critique

The proposed conditional planning estimates (alpha=.05, m=12, beta=.2) are
recalculated as consistent with standard formulas:
- 5pp simultaneous half-width: ~4,940 independent families
- 10pp superiority 80% power: ~2,818 families
- 5pp equivalence 80% power: ~12,814 families

These are correct under stated assumptions (independent families, known
variance). However: 6 convenience families + 28 template clones do NOT
establish independent family sampling. No ICC, no variance estimates from
pilot data, no cost model. These numbers are model assumptions, NOT authorized
targets, budget recommendations, or achieved power. Multiplicity (12 contrasts)
is correctly Bonferroni-adjusted.

## Oracle/scenario custody review

BL3's proposed custody protocol is well-specified in structure (independent
semantic custodian, signed/hash-grant boundaries, contribution graph, blind
response coding) but NONE was actually issued. `custody_status()` correctly
returns HOLD with reasons. Same-author dual code paths are not independent
oracle science. A distinct semantic custodian and prospective sampling owner
remain named future actions.

## Owner actions required

1. Independent oracle/scenario custodian appointment (separate from BL3 author)
2. Prospective sampling/power owner adoption (separate statistician verification)
3. Real behavioral experiment requires: provider adapter, model/config pin,
   eight-field use/privacy/retention/spend grant, revocation, budget ledger
4. Independent reviewer for any SC0F2 repair (distinct from both SC0F and SC0I)

## Acceptance ceiling

`REVIEW_PASS_SCOPED_R3_SYNTHETIC_SENSITIVITY` — the sourcefree R3 assay
correctly detects arm-aware synthetic sensitivity and false controls. This
ceiling does NOT extend to behavioral, psychological, causal, or model-use
claims.

## Terminal

`BR3_REVIEW_PASS_SCOPED_R3_SYNTHETIC_SENSITIVITY__NO_BEHAVIORAL_CLAIM__NO_ADOPTION`
