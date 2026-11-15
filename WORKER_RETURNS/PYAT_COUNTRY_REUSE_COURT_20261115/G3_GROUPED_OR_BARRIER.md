# G3 — Existing grouped parity and the exact cold qualification barrier

**Disposition:** `EXACT_COLD_QUALIFICATION_BARRIER` for the cold saved estate; `EXACT_PARITY` for the existing in-memory grouped path. **No cold grouped positive was manufactured.** The existing grouped path was exercised only through its lawful public interface on a sealed `C11Repository`, not as a cold saved consumer.

**Receiving status:** the independent review `c5a71fcc59a45aa470720159a334ae57f365de11` reproduced the exact facts, counters, guards and receipts at the sourcefree measurement scope (`ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED`), while returning `REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS` for the handoff narrative. This corrected G3 is documentary; it is not a new measurement and not self-acceptance.

## 1. What was measured

Same fixture, same 100 distinct query operations, same predicates/targets/measures/authorities/native evaluator.

| Path | Substrate | Wall | Core builds | Core hits | Capacity fallbacks | Exact parity |
|---|---|---:|---:|---:|---:|---|
| Ungrouped | in-memory `C11Repository` | 4.304 s (author one pass) | n/a | n/a | n/a | reference |
| Grouped, `max_groups=256` | in-memory `C11Repository` | 4.216 s (author one pass; review 1.199× vs its ungrouped) | 80 | 20 | 0 | **100/100** |
| Grouped, default `max_groups=64` | in-memory `C11Repository` | 3.927 s (author one pass) | 64 | 20 | **16** | **100/100** |
| Cold saved, `group_scope=None` | `DirectEstateI03Session` per operation | **51.929 s author; 65.661 s independent** | n/a | n/a | n/a | **100/100 vs native** |
| Cold saved, `group_scope` supplied | `DirectEstateI03Session` | **REFUSED** | 0 | 0 | 0 | no result |

The in-memory grouped wall difference is **not a clean performance claim**: the author's single frozen pass was 1.021× and the independent review's single pass was 1.199×, with identical receipts under ambient load. The exact evidence is the receipt: **80 core builds + 20 core hits** at `max_groups=256`, and **64 builds + 20 hits + 16 capacity fallbacks** at the default 64. The 20 hits are precisely the 20 governed-weighted variants of 20 raw cores; the other 80 distinct cores do not share. No narrow stable wall range is claimed.

## 2. Existing grouped path does amortize repeat invocations

A separate 1,000-repeat invocation probe on the **in-memory** grouped path, one operation (`marginal_A`), measured:

| Path | 1,000 invocations (author / review) | Receipt |
|---|---:|---|
| Ungrouped | 52.035 s / 56.238 s | 1,000 full evaluations |
| Grouped | **15.683 s / 15.925 s** | 1 core build, **999 core hits**, 0 fallbacks |
| Wall speedup | **3.32× / 3.53×** | p50 grouped invocation 15.2 ms |

This is `REPEAT_INVOCATIONS_NOT_DISTINCT_OPERATIONS`. It proves the existing scope is a useful repeat cache; it does **not** prove a 1,000-distinct-operation contract, and it is not a cold saved measurement. The 1,000-distinct cold projection is **519.29 s author / 656.61 s independent review**, both over the 300 s budget (`EXTRAPOLATION_NOT_MEASURED`).

## 3. Cold grouped refusal: exact messages, no bypass

Both lawful public entry points refused before publishing any grouped core:

| Entry point | Exception | Exact message | Receipt after refusal |
|---|---|---|---|
| `CarrierNeutralResearchExecutor.execute_i03(..., group_scope=...)` on `VerifiedDirectEstate` | `CarrierExecutionBindingError` | `grouped saved I03 scope awaits distinct S2-D qualification` | 0 builds, 0 hits, 0 open groups |
| `execute_empirical_query(repository=DirectEstateI03Session, ..., group_scope=...)` | `EmpiricalQueryExecutionError` | `grouped native I03 cache not yet qualified for cold sourcefree estate` | no fact served |

The grouped scope receipt for the carrier refusal is all zeros; the evaluator refusal occurred before any grouped core materialization. No guard was removed, monkeypatched away, or bypassed.

## 4. Exact missing contract (read-only diagnosis)

The refusal is not merely a policy flag. The cold saved estate does not yet expose the exact identity/stable index contract the grouped key requires:

1. **Release identity fields absent.** `DirectEstateI03Session` uses `_DirectReleaseIdentity(release_ref, replay_manifest)`. `I03GroupedExecutionScope._index_identity` (`pre553_empirical_query.py:562-582`) requires:
   - `release.semantic_release_hash`
   - `release.source_release_manifest_hash`
   
   Measured: both absent (`release_fields = ["release_ref", "replay_manifest"]`).

2. **Transient index object.** `DirectEstateI03Session.indices_for` builds a **new** `_ReleaseIndex` on every call (`pre553_direct_estate_i03.py:401-414`), while `_index_identity` includes `id(index)`. Measured: `same_index_object_across_two_calls = false`; two calls returned different index ids.

3. **Saved admission hard-codes unshared.** `SavedC11Admission.execute_i03` passes `group_scope=None` (`pre553_saved_c11_admission.py:440`); there is no lawful cold grouped call surface.

4. **Core key is not a generic substrate cache.** Even with a repaired identity, `_core_key` includes predicate identity and target plan. It would share only exact same-core measure variants, not the 80 distinct condition/target operations. A many-distinct-operation contract needs a broader prepared respondent substrate, not merely unguarding this cache.

The missing contract is therefore: **a versioned exact cold release/index identity plus a stable per-execution prepared index/session, with explicit S2-D owner qualification and exact current/revocation/body-truth preservation**. Renaming fields or removing the guard is not sufficient and is not authorized.

## 5. Parity evidence

`evidence/parity.json`:

| Comparison | Result |
|---|---|
| cold saved vs native ungrouped | **100/100 exact, 0 mismatches** |
| grouped max256 vs native ungrouped | **100/100 exact, 0 mismatches** |
| grouped default64 vs native ungrouped | **100/100 exact, 0 mismatches** |
| grouped max256 vs cold saved | **100/100 exact, 0 mismatches** |

Exactness covers fact ref, replay ref, release refs, typed state, raw/weighted support fields, target-domain identity and complete cell projection. The grouped in-memory parity is real; it is not evidence that the cold saved path is grouped-qualified.

## 6. G3 conclusion

- **Qualified existing grouped parity:** yes, at the narrow in-memory sealed-`C11Repository` scope; 100/100 exact, 20 measure-variant hits, 80 distinct core builds.
- **Qualified cold saved grouped parity:** **NO**. Both public guards refuse; the release/index identity contract is missing and the index is transient.
- **Amortization:** the existing scope amortizes repeated invocations (3.32× author / 3.53× review on 1,000 repeats) and measure variants (20/100), but not 100 distinct condition/target cores. No 1,000-distinct-operation positive exists.
- **B is not measured:** no prepared-session/iterator implementation or B A/B run exists in this return. B remains a source-grounded hypothesis with a measured cold-cost target; a bounded owner-approved measurement is required before any gain claim.
- **No production behavior changed; no guard removed.**
