# Function, estimand, clock and source-ABI map

## Exact cuts

- Branch startup: `750548ddbb9b4392a16ce93097b856f349e16182`.
- Current PRE-MAIN recheck: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Current `rawlsing_next` tree: `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` (same as startup).
- Original P41 branch: `f27d1101048638bba395143a48efb7ef00bfcda4`.
- Original P41 service blob: `7d428106c79bcc56973f7c0044fc273a2b354554`.
- Original R08 binder blob: `3ca860e409f1d063da4cd03dd1691a89c67333f6`.
- Current E03 blob: `84d404147547767be8ecd4b6e1541f5fa3a8c8a2`.
- Current N10E/C1/F8 are the current sourcefree modules exercised by the 69-test court.
- Selected-world S3 exact tip: `ed34944e253b78714a28d72b8ca2a6521ce15930`; original S3 tip `208bca30471710d48124a6b69ba467f240d8834b`.
- PE owner-bound successor `a48c6acb...` is author-only TEST_ONLY; independent court pending; not used.

## P41 original consumer functions

| Original function/channel | Current status | Classification |
|---|---|---|
| `progressive(target, conditions)` over N10E→C1→F8→E03 | Current E03 `run_progressive_chain` exercises the same current N10E/C1/F8 providers; our `p41_current_service.py` wraps it with a versioned receipt | REPLACED/ADAPTABLE at sourcefree test scope |
| exact progressive denominators 32→16→8, 9/16→5/8→3/4 | Current E03 **18/18**; current P41-style adapter **5/5** | SAME geometry at fixture grade |
| historical receipt serving | Adapter-level `historical()` retains receipt with `archival_only=True`; no current native N9 lifecycle service | MISSING USEFUL / HOLD |
| `publish_rule_revision` | Current E03 has no structural rule owner; adapter records a `rule_revision` metadata clock only, explicitly `ADAPTER_TEST_ONLY_CLOCK__NO_SOURCE_RULE` | MISSING USEFUL / SOURCE-RULE HOLD |
| `revoke(scope)` | Adapter-level empirical/progressive revocation; historical receipt retained; no current N9 lifecycle owner | REPLACED at test scope / production missing |
| `current_clock_snapshot` | Adapter-level as-of/publication/reference/rule clock; no original N9 clock issuer | ADAPTED TEST-ONLY |
| `consumer_read` / learned-world read-through | Current learned-world composition tests **30/30**, but no P41 consumer import; historical P41 tests 19/19 use the staged E04L apparatus | CURRENT ALTERNATIVE NOT INTEGRATED |
| reverse/opposite conditioner and 3 severance witnesses | Historical P41 19/19 plus W1/W2/W3 **3/3** pass; current adapter only forward current E03 path | HISTORICAL PASS / CURRENT NOT CLAIMED |
| actor/person/route probability firewall | Historical P41 actor firewall and current E03 both declare no actor; no actor created | RETAINED / NO GRANT |

## Selected-world seam

| Function | Original | Current |
|---|---|---|
| selected contract | S3 `SelectedWorldContract` / 58-row P04 synthetic | absent from current `rawlsing_next` |
| selected-world 24-test court | 24 passed at `ed34944e` | NOT_RUN on current; S3 path absent |
| exact seam 27-test court | **26 passed / 1 failed** `KeyError exact_probabilities` at `ed34944e` | original failure preserved |
| source-owned numeric mutation | failed because changed channels/steps retained old contract; consumer returned `REFUSED PRODUCER_VALUE_IDENTITY_MISMATCH` | `selected_world_repair.py` rebinds contract to changed cells and proves 3/4→1/2; stale contract refused; cold restore; 5/5 |

The selected-world failure is a **contract rebind gap**, not a missing numerical
producer: the consumer reads exact channels, but producer identity validation
rebuilds the expected world from the changed cells and compares it with the old
selected-world contract. The old contract has the old source/risk identity. The
repair makes the value change a new selected-world contract, not a silent
mutation of the old one.

## R61-R08 evidence binder

| Function | Current status |
|---|---|
| `pre553_universal_evidence_binding.py` | **ABSENT** from current `rawlsing_next` |
| exact binder blob `3ca860e...` | 113/113 author tests pass against current `rawlsing_next` in an isolated tree |
| R8 targeted refusal probes | 8/8 pass (legacy binding pin, descriptor pin, stale cache, missing verifier, import/export limits, semantic adapters) |
| native source warrant | NOT CLAIMED; `TrustedAdmissionAuthority`/`TrustedCacheIssuer` are TEST_ONLY ephemeral HMAC authorities |
| production receiver | **GAP CARD**: no current import, no current native receiver |

## First genuinely integrated current consumer

**NONE at production scope.**

- Current E03 + the P41-style adapter is a **sourcefree test consumer**, not a
  production entrypoint.
- Current learned-world composition has tests but no P41 consumer.
- R08 binder has no current module import; exact binder is staged in a temp tree
  for tests only.
- PE owner-bound successor `a48c6acb...` remains author-only TEST_ONLY (33 tests),
  independent court pending; it is not a current PE/world receiver.
- Original PE strict remains **4/13**; V2K retirement and C11 item/namespace
  anti-join hold remain separate.

## Estimand and clock distinctions

| Axis | Status |
|---|---|
| synthetic empirical possibility | E03 current sourcefree exact fixture arithmetic; not real population |
| selected-world counterfactual geometry | bounded sourcefree 2x2 numeric repair; not operative N9 |
| learned/historical alternative | current learned-world composition is a separate current sourcefree test surface; not P41 integration |
| observation/publication/as-of/request clocks | adapter-level frozen clocks; no original N9 issuer |
| rule clock | adapter metadata only; no source rule revision authority |
| actor/person | none; firewall false |
| source rights | none |
| production adoption | none |

## Owner/consumer conclusion

The current N10E/C1/F8/E03 path is real and testable. The original P41 and R08
functions are **not current production receivers**. The selected-world seam is
repaired only as a bounded sourcefree alternative. Production acceptance remains
blocked on a named current adopter and original source/N9 authority.
