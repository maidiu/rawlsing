# S02 runtime-dataflow and numerical court

## 1. Source input trace is synthetic-only

At candidate `rawlsing_next/r3_s02_seam_witness.py` lines 163–170:
- `build_sociological_bundle` invokes `select_world()` from `pre553_selected_world_progressive_contract.py`.
- The P04 `select_world()` calls `synthetic_world_rows()` with **58** fully synthetic A/B/C/Y responses, then `build_synthetic_world(tag)` using a test-source factory; its selection metadata includes `SOURCE_FREE_SYNTHETIC` and hard-codes `real_current=False`.
- `run_progressive_chain(world)` invokes actual N10E (single-conditioner), C1 (multi), and F8 over that synthetic test-source world. This is genuine P04 owner arithmetic on a synthetic population, not a retained Afro source execution.

Candidate seam lines 171–188 append channel values **only** from `chain.steps`. Every channel is explicitly `source_scope="P04_SYNTHETIC_58_RESPONDENT_FIXTURE"`, `test_origin=True`. The top-level `world_scope` (lines 227–232) advertises eleven-country R5; this is not the source of its values. The seam imports **no** GT2 Q86A/Q86B empirical fact, GT2 complete count profile, retained release resolver or original source binding; no GT2 actual numeric cell is read in its call graph. `s00_target_contract.json` refers to `N=19210` as scope and `retained_N01_N02_GT2_Q86B_Q86A` as a documentary release label, not a resolved measured release or the channel numerators.

### Observed saved example (author-provided evidence, not a fresh runtime test)

`WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/repro/s02_evidence.json` (blob `3a3269446114ebfd045b9867c3545c5f777918c5`) records channels:
- `P_Y_given_A`: Y=1 **18**, Y=0 **14**, denominator **32**, probability Y=1 **9/16**.
- `P_Y_given_A_B`: Y=1 **10**, Y=0 **6**, denominator **16**, probability **5/8**.
- `P_Y_given_A_B_C`: Y=1 **6**, Y=0 **2**, denominator **8**, probability **3/4**.

These are the exact P04 authored fixture counts, not 19,210-survey counts. For source scientific grade, expected GT2 per-cell native count data would require resolved actual source-owned Q86B×Q86A joint fact with exact release/query/risk, native state topology, provenance and model-use ceiling; NONE of the saved seam channels meets that requirement.

## 2. S02 does not itself compute cumulative probabilities

At seam lines 297–321:

    relevant = [
        ch for ch in self._bundle.channels
        if any(c in ch.channel_id for c in conditioning)
    ]
    total_support = sum(ch.support for ch in relevant)

- `conditioning` is an arbitrary sequence of substrings **of channel IDs**, not an exact ordered predicate on respondents/events with risk/response-state logic.
- Since `P_Y_given_A` is a prefix of `P_Y_given_A_B` and `P_Y_given_A_B_C`, selecting it matches all three steps.
- There are two channel rows per step (one for Y=0, one for Y=1) and BOTH carry the full step denominator as `support`, so summing counts duplicates the same cohort.
- There is no response-set intersection, no target-cell sum over a chosen native semantic denominator, no new calculation of `P(Y=y|A=a,B=b,...)`, no explicit conditioning-world selection, and no source/risk consistency check.
- The result's `distributions` are a bag of channel objects copied intact from precomputed synthetic owner outputs.

**Author's saved scenario A** `["P_Y_given_A","P_Y_given_A_B"]` selects six channels: `32+32+16+16+8+8 = 112`. **Scenario B** `["P_Y_given_A_B","P_Y_given_A_B_C"]` selects four: `16+16+8+8 = 48`. Both are mathematically irrelevant to the denominators 32/16/8 and to true R5 GT2 sample risk. A "high democracy" vs "low democracy" scenario string changes NO condition value in the underlying P04 fixture. Labels do not produce different source-scientific worlds.

**Important separation:** The **P04 owners DO** calculate the three fixture probabilities. S02 is a serialization and synthetic read adapter which **does not calculate** its advertised scenario-conditioned distributions.

## 3. Consumer receipts do not prove semantic dependence

At seam lines 279–290, `read_value(channel_id)` walks the bundle, hashes the channel and unconditionally stamps `semantic_effect="VALUE_READ_AND_USED"` when found. At lines 337–345, `run_seam_witness` calls `read_value` on six channels, then calls `compute_scenario`. But `compute_scenario` directly iterates `self._bundle.channels`, bypassing the read path. Hence changing, omitting or refusing these prior reads does not change how scenario values are collected; their supposed semantic effect is a user-authored label, not a verified computation dependency. The `query_ref` is the fabricated string `read_{channel_id}`, not the exact GT2 empirical query or a consumer operation ref.

The `same_marginals_different_joints` test at `rawlsing_next/tests/test_r3_s02_seam_witness.py` compares **channel IDs after requesting different substrings** and checks one existing support 32; it constructs **no pair of equal-marginal/different-joint datasets** and proves no sensitivity to joint dependence. The "irrelevant input" test reads another channel but leaves the bundle untouched, so it cannot establish invariance to changing irrelevant input values. The "zero support" case uses a **nonexistent matching substring**, not a qualified actual predicate whose risk count is zero. The "scope mismatch" uses an unknown channel ID, not an actual wrong source/release/risk. Tests of \`VALUE_READ_AND_USED\` assert the hard-coded label, not that a modeled output was computed from that value.

`get_receipt()` (lines 322–324) computes an `output_hash` over `self._receipt.as_dict()` **including its then-current output_hash**; first computation reads the empty-string hash slot, subsequent calls rehash the prior output. It is deterministic in the author's fixed call sequence but not a canonical self-excluding receipt hash. Similarly the bundle content hash is built from `bundle.as_dict()` while content_hash is still blank and returned with the digest subsequently filled. A defined self-excluded hash projection and exact dependency roots must replace the present self-reference for an independently verifiable stable receipt. A changed hash is integrity evidence only, not semantic use.

## 4. Exact first positive source-value demand

To qualify a *retained* GT2 seam, the production/input stage must resolve immutable source-owned `EmpiricalQuerySpec@1.0.0` and `EmpiricalFact@1.0.0` for the accepted ordered Q86B×Q86A RAW joint, or the exact authorized `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0` with complete source-native cell domain; preserve its 11-country/source-release/risk/provenance/authority/replay, including native non-substantive states and fully typed counts. Use an authorized read of **already retained** aggregate objects if allowed; this request does not grant new source-rows access. The consumer must compute at least two legitimate conditional outputs by keyed native Q86B states and preserve Q86A alternatives. If original joint table is not available/authorized at this time, the correct state is `SOURCE_VALUE_UNAVAILABLE__HOLD` and the synthetic mode remains correctly labeled. No pseudo-real numbers from the fixture or coexposure count.
