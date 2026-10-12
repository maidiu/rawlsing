# PYAT HQ282 P04 — Product or Hold

## Product: source-free selected-world → progressive-consumer contract

**Status:** `PASS__BOUNDED_PRODUCT`

The smallest genuinely executable contract that binds an explicitly synthetic selected world to the E03 progressive owner chain (N10E → C1 → F8) has been built and executed.

### Contract structure

```
SelectedWorldContract (frozen dataclass)
├── contract_id: PYAT_HQ282_P04_SELECTED_WORLD_PROGRESSIVE_CONTRACT@1.0.0
├── world_tag: p04-selected-world
├── source_universe_ref: ExactRef (synthetic universe)
├── release_ref: ExactRef (synthetic release)
├── risk_set_ref: ExactRef (shared risk set)
├── selection_metadata: MappingProxyType (synthetic, with HOLDs)
└── real_current: False (hard-coded)
```

### Execution path

1. `select_world()` — builds synthetic 58-respondent fixture, emits contract
2. `run_selected_world_progressive_chain(contract)` — verifies bindings, runs E03 chain
3. `verify_chain_preserves_contract(contract, chain)` — checks conservation

### What attaches later (typed HOLDs)

| missing owner | E01 status | how it would attach |
|---|---|---|
| N9 (publication/resolution/lifecycle world-serving) | `implemented: false` | Real N9 would replace `select_world()` with actual publication/resolution/lifecycle world-serving; the contract's `selection_metadata` would carry real N9 receipts |
| N10W (progressive multi-condition world binding) | `implemented: false` | Real N10W would own the progressive world binding; the C1 multi-conditioner calls would route through N10W instead of directly |
| G0b (model-use grant) | UNISSUED | Real G0b would be issued by EE14 competent issuer; the contract's `effects()` would flip `model_use_grant` to True |
| B5 CURRENT selection | not selected | Real B5 would select a CURRENT; the contract's `real_current` would become True only through B5 |

### Conservation properties verified

- Same `release_ref` across all 3 steps
- Same `risk_set_ref` across all 3 steps
- Minority cells present at every depth (min count 2 at depth 3)
- `UNCERTAINTY_UNQUANTIFIED` preserved
- `real_current` is False
- Oracle match: 9/16, 5/8, 3/4
