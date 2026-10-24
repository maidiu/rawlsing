# R91 R05V R2 independent review — return

Verdict: **REVISE / HOLD full R05 acceptance.** R2 adds a useful
`NativeProductGraph` wrapper, consistent-status axes and the actual M01/C1
positive, but it still accepts copied joint/discovery/recursive labels, a fake
E41 extension route and duplicate graph components, and can return
`EXACT_SUPPORTED` when `producer_fact_state` is supported but
`analytical_state` is not. The author explicitly demonstrated only a
single-component graph plus direct E41; mixed/joint/recursive/discovery status
and real graph validation remain missing.

## Custody

- Stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-r2-consumer-review-r1`; startup/HEAD
  `d9e809094a2398d20273605afada8ad9b81a3dda`; clean at gate.
- R05V R2 commission `f57b932ed1bd66f8648a6d65f46e0127e6294a55`.
- R2 contract `cde351f734143da2c1b3eab076ff35c080a60438`; code
  `09a0232f7bd6eac45ab835e62e6e4f55f8a06b44`.
- Frozen R2 EXPECTATIONS
  `21f37e783277721c5c5dbb6bc53a45e3409a4bfa`, committed before code.
- Code blobs match pins: learned-world `32631d17...`, test `3ae5e674...`.
  Only those two authorized code/test paths plus author r2 return changed.
- Accepted R08 bodies `3ca860e4...`/`5832ce05...` and accepted C1/provider/
  evaluator/empirical owners `604c8d59/23167aa2/62e5eced/a61365b9` unchanged.
- Author R2 manifest independently recomputed: 7/7 artifacts match; explicit
  self-exclusion.

## Already-qualified partial capability

- Author 36/36; independent R05V R1 probe replay 4/4; provider 43/43 with the
  exact previously materialized AT07 fixture; analytical composition 13/13.
- Actual M01 → discovery/facts → M1 RULE_SATISFIED → M2 release → C1 evidence →
  unchanged N10E `EXACT_SUPPORTED`; consumer hash `8e54f8b0...`.
- Consistent typed-status cases (`producer_fact_state == analytical_state` for
  ZERO_SUPPORT/VALID_EMPTY/UNRESOLVED16) now return typed states and z16.
- E41 direct extension actual/delegating; direct graph route accepted.

## Missing graph/status function (prioritized)

### P1 — Copied graph labels and fake E41 routes are trusted/echoed

`NativeProductGraph` only validates that components are `AnalyticalCompositionResult`
values; the consumer's `_graph_refs` concatenates/sums joint, discovery,
frontier and recursive fields and returns them. It does not validate them
against actual native owner receipts/frontier/lineage/root-parent, component
order/count/morphology, or the E41 extension's actual type/route/consumer
identity.

Independent probes (`probes/test_r05v_r2_graph_gap.py`):

- copied forged discovery/recursive refs + `joint_component_count=2` on the
  single actual composition → `LEARNED_CONSUMER_EXACT_SUPPORTED`, forged refs
  echoed in values; actual component joint count is 1.
- `NativeProductGraph((composition, composition))` → exact supported; no
  duplicate/order/count refusal; graph count 2.
- a fake object with `composition_result` and `producer_route="FAKE_ROUTE"` →
  exact supported and `extension_route="FAKE_ROUTE"` echoed.
- The author's only graph test uses one actual composition plus direct E41; no
  actual materially different multi-component/joint/recursive/discovery route.

Exact missing function: validate each component and E41 extension against actual
native owner evidence/receipts/frontier/lineage/root-parent and component
order/count/morphology; reject copied labels, duplicates and fake extension
objects; derive graph fields from authenticated native objects, not caller
metadata. Exercise a real multi-component/joint/recursive/discovery route using
existing owners.

### P2 — False exact-supported when producer and analytical state disagree

The success path checks `producer_fact_state == "SUPPORTED"` and evidence, then
returns exact support/hardcoded supported, ignoring `analytical_state`. A
composition with `producer_fact_state="SUPPORTED"`,
`analytical_state="ZERO_SUPPORT"`, denominator 0 returns
`LEARNED_CONSUMER_EXACT_SUPPORTED` / `SUPPORTED` in probe
`::test_non_supported_analytical_state_cannot_be_false_exact`.

The R2 typed-status test only sets producer and analytical state to the same
value, so it misses this inconsistency. Exact missing function: check the
complete native axes/evidence jointly before exact support, and preserve
ZERO_SUPPORT/VALID_EMPTY/UNKNOWN/HELD/Z16 without false exact or generic
refusal.

### P3 — Duplicate definition block

`rawlsing_next/pre553_learned_world_composition.py` contains two `__all__`
blocks and two copies of `NativeProductGraph`, `LearnedWorldConsumerResult` and
`evaluate_learned_world_consumer` (around lines 1413/1952, 1452/1991,
1719/... of the candidate). The later definitions win; the earlier block is
dead duplicate code. This is unrequested duplication and a maintenance hazard;
remove the duplicate while preserving the single implementation.

## Exact scoped boundary

No new authority, provider, evaluator or scientific method is needed. Full live
J42/P41/E04 remains NOT_REACHED; R04 independent; no original source/science,
F6/F7/FieldForge, CI/prod, N11/N12, Sorok, J52/W52 or adoption. The already
qualified narrow M01/C1/E41-direct positive is preserved.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_r2_observations.json`,
`probes/test_r05v_r2_graph_gap.py`, `probes/r05v_r1_immutable_probe.py`,
`junit/*.xml`, `logs/stdout.jsonl`.
