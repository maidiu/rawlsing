# PYAT R27 GF1E — actual native pair-support consumer implementation

**OUTCOME:** `GF1E_CONSUMER_IMPLEMENTED__FROZEN44_GREEN__DIFFERENTIAL_AND_COLD_REPLAY_COMPLETE`
**TERMINAL:** `PYAT_R27_GF1E_CONSUMER_IMPLEMENTED__GITHUB_PUSHED`

**Role:** original GF1/GF1C/GF1D implementation continuation. **Not** an
independent reviewer, issuer, HQ or installer.

**Branch:** `agent/rabochii-pyat-r27-gf1e-actual-native-consumer-implementation-r1`
**Sealed startup:** `e9867879a0f0b3ac8d8afe21fced9e18a8a0a1fb`
**Parent:** GF1D `b9f3fbefe8ec0c873d47745688bffe1c21e9d940`; original GF1
`9f4a23cef1482e0a81afb1e7a65df90879931465`; independent GF1I RED
`c6a55f0dd5b327c40d64f96e0705ab5485559e90`.

## What was delivered (not a diagnosis, not a stub)

`gf1_pair_support_consumer.py` — a real, computing consumer placed at its
frozen import site `court/runtime_root/` (next to the sibling candidate
`generic_native_pair_relation.py`, exactly where `gf1_native.py:45` and
`test_gf1_generic_pair.py:33` import it). It exposes
`compute_pair_support_signature(relation) -> dict` and genuinely derives every
downstream field from the immutable `GenericNativePairRelation`:

| field | how it is computed |
| --- | --- |
| `separation_class` | decoded from the ordered `conditional_count_profile` 2x2 + `eligible_joint_risk_total` |
| `separation_signature` | role order + operation order + class + ordered cell counts |
| `support_vectors` | `{condition_state: {target_state: joint_support_count}}` recomputed from the profile |
| `zero_cell_semantics` | per-cell `joint_cell_state`, preserving `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` vs `ZERO_SUPPORT` |
| `joint_support_total` | sum of every cell count (never copied from the relation) |
| `condition_states_with_positive_denominator` | condition states whose denominator > 0 |
| `result_hash` | sha256 over the canonical result content (excluding itself) |
| `decision_state` | `PAIR_SUPPORT_SIGNATURE_COMPUTED` / `CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION` / `RESPONSE_INPUTS_VALID_EMPTY` |
| `generic_native_semantics_hold` | `RETAINED` |

The consumer verifies the relation `object_id`/`content_hash` before computing,
rejects non-relation input, and emits no personhood or causal claim.

## Separation classification (all four classes, genuinely computed)

| pattern (cell key `[conditioner, target]`) | eligible risk | class |
| --- | --- | --- |
| `00=1, 01=0, 10=0, 11=1` | 2 | `EXACT_PAIR_SEPARATION` |
| `00=0, 01=1, 10=0, 11=1` (target collapsed) | 2 | `NO_PAIR_SEPARATION` |
| `00=0, 01=0, 10=0, 11=1` (one condition empty) | 1 | `UNDETERMINED_NO_ELIGIBLE_RISK` |
| `00=0, 01=0, 10=0, 11=0` (zero support) | 0 | `UNDETERMINED_ZERO_SUPPORT_RISK` |

Baseline native `1/0/0/1` reproduces `EXACT_PAIR_SEPARATION`; the two live
interventions collapse to `NO_PAIR_SEPARATION`; the discovery / reverse slots
produce `UNDETERMINED_NO_ELIGIBLE_RISK`; a zero-support risk set produces
`UNDETERMINED_ZERO_SUPPORT_RISK`. Reversed X|Y remains a separate operation
under `REVERSE_PAIR_GRANT_ID` (unchanged producer behaviour).

## Court results

| suite | PASS | FAIL | ERROR | SKIP | exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| Frozen 44 (original, unchanged) | 44 | 0 | 0 | 0 | 0 |
| GF1E differential + cold (new) | 9 | 0 | 0 | 0 | 0 |

The frozen 44 test file and `01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json`
are byte-unchanged (SHA256 `2bbb54aa…` and `c5bdc14a…`). The baseline
`ModuleNotFoundError` is preserved in this lane's history and recorded in
`observations/baseline_collection_failure.log`.

## New evidence

* `tests/test_gf1e_consumer_differential.py` — four live differential patterns,
  the F2 non-copy falsifier, identity/anti-claim checks, a real native-chain
  baseline relation, and a two-process cold replay.
* `observations/frozen44.xml`, `observations/gf1e_differential.xml` — raw JUnit.
* `observations/gf1e_cold_consumer_{0,1}.json` — two fresh OS processes,
  bit-identical results, distinct PIDs.
* `02_EXECUTED_CONSUMER_EVIDENCE.json` — executed consumer outputs + import
  identities (`gf1_pair_support_consumer.py` blob `75670c69dc58…`,
  SHA256 `06dd484b…`).

## Authority boundaries (unchanged)

No self-acceptance. No Field Forge semantic or model authority, no S1–S9
relation issuance, no original source rights, no OC05, no N11/N12, no actor, no
V3. No frozen oracle, reviewer freeze or historical author SHA modified. The
accepted specialized GT2 owner and its two HELD ORDERED operations remain
untouched. Independent corrected-delta review is still required.
