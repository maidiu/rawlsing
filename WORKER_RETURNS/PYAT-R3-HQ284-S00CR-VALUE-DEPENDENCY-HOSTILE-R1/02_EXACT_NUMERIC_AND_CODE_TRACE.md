# Exact S00CR producer→read→calculation→receipt code trace

## References

Frozen author candidate `54f145538ed0880f8257368f838baa5b0e12e2d3`, `rawlsing_next/r3_s02_seam_witness.py` Git blob `408c4700aee7a63db43f1e01c22ab6e1371e3568`, reviewer branch starts at candidate plus exact commission. P04 source `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` and `pre553_selected_world_progressive_contract.py`; canonical Afro R5 `wave1_r5_q86_c11_projection.py` and `field_forge_conditional_support.py`.

### Positive numeric dependency: actual code, NOT hypothetical receipt-only

1. `build_sociological_bundle` (lines ~173–276) calls `select_world()`, `run_progressive_chain(world)` and `verify_chain_preserves_contract(contract, chain)`. Every P04 step gives two raw numerator supports, denominator and owner-produced `evidence_ref`. S00C serializes these into `ChannelValue.value["raw_numerator_support"]` and `["producer_evidence_ref"]`, synthetic `test_origin=True`.
2. `ContractOnlySeamConsumer._validate_bundle` (~425–460) verifies self-excluded SHA256 of serialized bundle, `SOURCE_FREE_SYNTHETIC`, local contract/replay relation, exact synthetic risk_set_ref across conditions, channel expected scope/test flag, and absence of permission/current claims. It does **not** independently resolve `producer_evidence_ref` against an owner-held store or verify counts against that evidence.
3. `compute_scenario` (~479–578) takes exact P04 step IDs or exactly one synthetic Q86 native step; does not use substring channel selection. For each step and target cell 0/1, calls `self.read_value("CH_"+step_id+"_"+cell)` and obtains `val["raw_numerator_support"]` (lines ~510–525). Recomputes `denom=sum(cell_numerators)` (line ~527), checks it equals declared condition and channel denominator (lines ~528–531), and sets a typed zero-denominator outcome.
4. Only when both actual cell reads are closed are the corresponding `ValueReadReceipt` objects upgraded to `VALUE_USED_IN_EXACT_CONDITIONAL` (~536–541). The progress trace records exact fraction `Fraction(numerator,denom)` (~550–555), used input hashes and actual numeric values (~542–560). The final result uses the last selected nested predicate's risk only (`total_support=last["raw_denominator_support"]`), avoiding old 112/48 overlap.
5. `get_receipt` (~585–590) hashes its semantic projection after clearing its `output_hash` field; repeated reads with no new effects yield same output hash, as designed. This hash remains *self-authored*, not independent source trust. `result["distributions"]` is still copied directly from `self._bundle.channels` after numerical computation, not by a second instrumented per-value read. Its contents include producer-advertised fractions which may be inconsistent with recalculated fractions; numerical `exact_probabilities` do use read data.

### Hand-derived P04 truth

P04's 58 synthetic responses are a known categorical test law. For full A/B/C Y1/Y0 cells:
- A=1 across 4 strata: (6+4+5+3 = **18** successes, 2+4+3+5 = **14** failures) → **18/32 = 9/16**.
- A=1 and B=1 across C=0/1: **10** successes, **6** failures → **10/16 = 5/8**.
- A=B=C=1: **6** successes, **2** failures → **6/8 = 3/4**.
- S00C progressive trace `A→AB` final **16** and `AB→ABC` final **8**; no observational reason to add 32+32+16+16+8+8=112 or 16+16+8+8=48.

### Native Q86B/Q86A original meaning and synthetic discriminator

Canonical `wave1_r5_q86_c11_projection.py` native code states: 0 No, 1 Yes, 9 DK, 997 NOT_ASKED, 998 REFUSAL, -1 MISSING. `field_forge_conditional_support.py` freezes `CONDITIONER_SOURCE_NATIVE_VARIABLE=Q86B` and `TARGET_SOURCE_NATIVE_VARIABLE=Q86A`, identity-only / no ordinal or metric meaning. Q86B asks citizenship opinion on country-born persons with TWO noncitizen parents, Q86A on ONE citizen/one noncitizen parent. These are response-attitudes, not actual citizenship law, democracy or institution trust. S00C's new native 2×2 path is **hand-authored** with distinct `SYNTHETIC_...` release/risk identities and no source rows.

Both tables below have X=(Q86B) row marginals 4,4 and Y=(Q86A) column marginals 4,4; rows X=0,1 and columns Y=0,1:

| Native TEST joint | X=0 | X=1 | P(Y=1 | X=1) |
|---|---|---|---|
| First | (3,1) | (1,3) | **3/4** |
| Opposite | (1,3) | (3,1) | **1/4** |
| Numerical change to first | (3,1) | (2,2) | **1/2** |

These are **invented** counts for identity/function hostiles. They are not retained GT2 numerators and grant no 19,210 substantive denominator.

### Replay and output-hash claim limits

- `build_sociological_bundle` content hash includes local displayed channel values and `selected_world_contract_hash`. Local consumer rehash check detects naïve tampering; anyone able to rewrite bundle can recalculate consistent hash. There is no independent issuer or immutable versioned producer read.
- Native synthetic builder `SelectedWorldContract` is hash-addressed from its hand-authored joint material; independently built different tables have separate local refs. But editing downstream `ChannelValue` values and recomputing bundle hash without updating contract/source refs is accepted if 2-cell row sum closes. This is the exact stale-origin adversary.
- The new source `build_retained_gt2_bundle` unconditionally raises `SOURCE_VALUE_UNAVAILABLE__ISSUED_GT2_AGGREGATE_AND_USE_AUTHORITY_HOLD`, even if caller passes a purported source dict/token; this scientific refusal is appropriate.
