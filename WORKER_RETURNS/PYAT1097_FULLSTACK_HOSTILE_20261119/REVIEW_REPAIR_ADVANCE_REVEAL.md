# PYAT #1097 cross-stack hostile review / bounded repair / next executable court
**Date:** 2026-11-19. **Lineage:** independent review branch from #1152 `2fe541d0773f0f0ccb761d5e99e4f216dd102ad9`; #1148 / #1149 / #1150 / #1151 author branches and protected PRE-MAIN untouched.
**Standing:** independent source-static review and corrective author, NOT independent G5 of my changes. No original source or host lease asserted. The user-supplied #1097 register itself is 2026-11-15 historical state, not protected Nov19 status.

## Whole-stack ten-module coverage (bounded source-static, not G5)

| Module | Source-static verdict and strongest remaining issue |
|---|---|
| `field_forge_generic_empirical_ingress.py` (1149) | REVISE_EXACT_DEFECT: valid top-level typed HELD can carry negative inner cell counts or nonmapping target topology; prior receiver silently produced held receipt. Bounded repair here; self-minted permission names remain nonissuance |
| `field_forge_observed_research.py` (1149) | HOLD_SCIENCE: exact conditional, context tables, small-cell candidates; no population/determinicity/rank metric or adaptive stopping, no causal/minority ontology |
| `field_forge_i05_role_ingress.py` (1149) | REVISE_EXACT_DEFECT: direct I05 path accepted receipt without checking per-candidate terminal evaluation, unlike S04. Bounded repair; retains VALID_EMPTY fact vs validation distinction |
| `field_forge_n10e_crossread.py` (1149) | ACCEPT_SOURCE_STATIC_CROSSCHECK_ONLY: compares an independent N10E provider's empirical cells with FF01 conditioned joint, checks direction/release/risk. Does NOT make N10E consume S04 value or eliminate second I03 execution |
| `pre553_s04_observed_research.py` (1150/1151) | REVISE_EXACT_DEFECT: repaired prior target-domain, resolved-target and multi-universe checks, but typed HELD nested cells were not validated. New guard preserves legal LOW_SUPPORT |
| `pre553_s04_i05_reception.py` (1150) | ACCEPT_SOURCE_STATIC_RECEPTION_ONLY: exact query role/fact ref/frontier + TERMINAL_COVERAGE_STATES, I05 VALID_EMPTY candidate not missing empirical fact; sampling/source authority separate |
| `pre553_s04_ff01_consumer.py` (1151) | HOLD_FIRST_CONSUMER_ISSUANCE: real S04 value-fed existing FF01 observed-joint ABI, yet relies on original in-memory I03 envelope or separate cold rehydration pin; remains explicit optional pathway, not adopted default |
| `pre553_s04_cold_custody.py` (1152) | HOLD_SOURCE_AUTHORITY_AND_PRIVACY: sourcefree caller assertion and caller-supplied query/fact/release pin establish equality, not independently issued original custody. Explicit original respondent preimage/retention permission absent. Directory fsync and hostile filesystem semantics need separate native qualification |
| `pre553_s04_research_batch.py` (1152) | ACCEPT_SOURCE_STATIC_SAMPLE_ONLY: caller-specified bounded 1/10/100 exact conditioned questions share original S04 joint without I03 requery, but max100 and 16,384-cell ceiling are unmeasured and not general high-width economics |
| `pre553_s04_first_consumer.py` (1152) | ACCEPT_SOURCE_STATIC_OPTIONAL_PATH_ONLY: existing I03 executes once then S04 then optional FF01+batch. It neither switches default FF01 route nor proves same-first-consumer N10E/N10W or joined S05 |

**These labels are review dispositions at source-inspection grade only. No module obtains independent G5 or scientific adoption from this text.**

## Exact established source defect and repair
1. Canonical `EmpiricalFact._validate_family` **already refuses** negative TOP-LEVEL integer supports (pre553_empirical_objects.py lines 709–721), wrong ZERO_SUPPORT/OBSERVED_ZERO states, and the family constructor rejects invalid producer state. Do not replicate these checks as claimed findings.
2. It does **not** recursively validate `target_topology.complete_cell_semantic_projection[*].raw_numerator_support`. In #1152 FF01 generic ingress around lines 365–384, a negative inner count is neither `>0` nor invalid type; S04 negative path around 289–300 never reads nested cell material. A hash-valid `UNRESOLVED` with legal top counts (raw0/eligible4) but nested -1 can therefore receive a benign-looking `PRODUCER_TYPED_HELD` / blocked FF01 receipt. A string `target_topology` similarly bypasses the old FF01 guard. Both source entries now refuse malformed held topology and negative/invalid nested counts. Legitimate LOW_SUPPORT with nonzero counts remains typed-held and unserved.
3. Direct `receive_i05_exact_joint_at_ff01` previously admitted selected receipt regardless of `coverage_state`. Upstream `receive_s04_i05_role` already checks `TERMINAL_COVERAGE_STATES`. The direct path now uses the exact original constant, preventing incomplete candidate coverage from being represented as completed fact-backed I05 role, while keeping VALID_EMPTY and DISCOVERED_RESULT_SUPPORTED distinct.

**New adversarial cases:** two malformed HELD topologies, genuine LOW_SUPPORT protected, hash-valid nonterminal I05 receipt refusing at BOTH S04 and direct FF01, and genuine terminal positive I05 role retained. All tests are authored, not executed in this environment.

## Operating register P0 / what changed since attached November 15 baseline

#1097's own current issue comments record independent scoped ANVIL production locality correction (review SHA `9ff290fd9d5eda87cb1541bd7b48b48897f6e099`, product blob d662fc…), a newer 10,000-respondent/5-question-role sourcefree run (ANVIL engineering scale author `19afff9758dcba1eb31dc47426bfca6c11ea6e9c`: build210.423s, retained31,163,472B, five operations130.864s, one index build12.618s, sampled query RSS568,688,640B), and 177/189 sourcefree S04 suites on earlier exact heads. These are not all independent certified original-source uses, nor a high-width 100k economic success. Earlier 100k writer3033.723s/5.26GB scratch and native per-session index1.30GB remain the closest measured cost failure but are earlier executable cuts; do not extrapolate linearly.

P0 C01–C17 MUST remain recognizable. C01–C04 original rights/selected alias/eligible/weights HELD. C05 saved 13-family sourcefree positive. C06 writer and journal double-handling cost unresolved. C07–C09 full hash validation and per-session SQLite O(events) prep, grouped saved I03 incompatibility / repeat 1/10/100 not yet economical. C10–C11 sourcefree F1–F4 genuine math and issued v2 scoped, original science held. C12–C13 score and cross-wave design unissued. C14–C15 joined #998 / N10E/N10W first consumer not complete. C16 current original two pilots/third family not issued. C17 retain original 52 T1R2 /24 paths/21 prospective/13 prongs without changing their acceptance grade. **This review adds exact negative protection; it does not solve the physical P0 cost.**

## Earliest decisive tests
- Exact clean sourcefree whole-stack negative court: `EXPECTED_PYAT_1097_REVIEW_HEAD=<EXACT_COMMIT_SHA> bash rawlsing_next/tests/run_pyat1097_fullstack_review_local.sh`, preserve JUnit/exit. Old malformed receipt is SOURCE-STATIC-ACCEPTED; corrected input should raise at both paths; before claiming RED→GREEN run original and repaired exact heads on qualified runner.
- Actual Codex b3dd original C11 vs accepted later routing-locator C11 must each run entire composed tests at exact real file-set and external true sourcefree permission; neither branch may be overwritten or passed by a two-module overlay alone. The original SRC04 witness `b3dd74d16…` contains no new original-source native reader acceptance.
- P0 high-width 1/10/100 different k-way/weighted operations on a single persisted estate, fresh and warm **same** release, row-group counts, process-tree RSS/disk/staging, query cost, exact member/fact/root/replay parity; no dummy 100x repeated same query. Decision-maker should use #1006 instrument as owner. No writer/physical-C11 modification here.

## Rights, adoption, complete review disposition
**CODE:** bounded three-module correction produced on separate review branch; tests NOT_RUN; no assertion of independent nonauthor accreditation for repair. **SOURCE:** no original35/SRC04 native rights or host lease and no protected C11 selection. **SCIENCE:** raw sample-only; estimand/design variance, relative predictor ranking, I05 adaptive stopping and LOW_SUPPORT method held. **CONSUMER:** FF01 optional, N10E independent C1 computation, #998 S05 unclosed, no N10W or actor promotion. **PERFORMANCE:** 100k high-width 6GiB and broad F1–F4 1/10/100 unproven. **PROTECTED:** PRE-MAIN rev11 unchanged; single PROGRAMMA #1148 candidate and paired progress unmodified because independent code review lacks current receiving/CAS authority.

**Next bounded owner action:** run this new exact review suite; if GREEN, compare against explicit previous source RED by checkout; then separately nonauthor hostile review of patched three modules + cold native sourcefree parity before eligible PROGRAMMA receiving. No second master plan or protected merge.

## P0 substantive extension — one authenticated physical session for 1/10/100 distinct saved I03 queries

The exact saved executor at `pre553_carrier_execution.py::CarrierNeutralResearchExecutor.execute_i03` lines 442–483 creates `with DirectEstateI03Session(self.repository)` **inside every invocation**. In S2-D physical `DirectEstateI03Session.__enter__` the native constructor verifies all event/posting positional identities and materializes its temporary SQLite index. Thus 100 successive original I03 requests through the old public method can perform up to **100** full posting preparations, even when the release and CURRENT remain unchanged. This is a source-code cost property, **not a measured 100x timing claim**.

New additive `rawlsing_next/pre553_distinct_cold_i03_batch.py` supplies `execute_distinct_native_cold_i03(executor, operations)`: exactly one independently pinned already-existing `VerifiedDirectEstate`, existing catalog-selected query/predicate exact preflight, one native `DirectEstateI03Session` lifetime, unchanged original `execute_empirical_query` for each of 1–100 distinct actual semantic query refs. Same risk/universe/replay/negative/I03 semantics, no grouped evaluator, no second C11, no permanent cache/index, no new grant. CURRENT is checked before/after each operation, existing per-yield guards remain, and failure cleans the temporary postings without yielding a partial bundle. Output is an in-memory tuple and must itself be measured for RSS at realistic width.

New `rawlsing_next/tests/test_pre553_distinct_cold_i03_batch.py` uses 1/10/100 distinct native question refs on actual accepted sourcefree C11→Parquet→cold executor (not 100 renamed identical operations), compares original in-memory I03 exact fact refs at first/last positions, instruments number of native session enters (expect ONE), rejects duplicate request preflight and invokes actual revocation after first existing-I03 execution (expect refused and no orphan postings). These tests are **AUTHORED_NOT_EXECUTED**, and the high-width real-source/CURRENT/6GiB economic threshold remains HELD. If the small suite fails, repair it before any performance/correctness claim.

This extension implements a *bounded economical scheduling primitive*, not a replacement saved I03 API. Resource owner can now time same 1/10/100 query sets old independent method vs this one-session path on an existing retained 10k/high-width estate with process-tree RSS and scratch, exact parities, then accept/reject its actual benefit. Do not report speedup from code structure alone.

## Further high-severity source-law correction: LEGITIMATE partial-positive UNRESOLVED

Native `_pre553_query_eval.py` ~lines 547–550 and 820–823 explicitly emits
`typed_state="UNRESOLVED"` whenever `raw_resolved != raw_denominator`,
even when **some** real eligible respondents have fully resolved positive
joint cells. The older #1149 and #1150 receptions rejected all positive
`UNRESOLVED` supports as "unexplained" and erased this legitimate state from
the available research receipt. Simply whitelisting it would have broken
the inherited hostile guard `test_negative_state_cannot_hide_positive_cell_evidence`
and let a top-level zero mask nested positive cells.

The independent branch now admits only the exact source-typed
`UNRESOLVED` **HELD** state where `0<raw_resolved<raw_eligible` and,
when full original nested cell material is present, validates
`sum(raw_cell_counts)==raw_resolved`. It never publishes a supported
conditional distribution for partially observed respondents; it carries
the positive count and remaining eligibility gap as evidence only. It
also conserves `LOW_SUPPORT`/unquantified uncertainty as held, refuses
self-rehashed inconsistent positive nested counts with a contradictory
header, and keeps canonical zero/negative types distinct. Three new
adversarial tests challenge the 3/4 partial support and 2-vs-3 forged
header; the full inherited FF suite's top-0/positive-cell RED is retained.
**These are author code and NOT_RUN, and the 3/4 fixture is a semantically
coherent mutation of native I03 fact material rather than an independently
executed original-source incomplete-response query.**

## Whole-consumer partial-negative repair

Follow-up self-attack found the optional actual `pre553_s04_ff01_consumer.py`
rejected the newly conserved genuine positive-partial `UNRESOLVED` fact
under its own old `LOW_SUPPORT`-only held predicate; this would have
stranded the repaired S04 data before FF01 first consumption. The adapter
now admits `UNRESOLVED` only **as already independently validated
S04 HELD knowledge** without re-execution or cell publication. Test checks
that S04→FF01 output exactly equals direct FF01 held output and
`ask_s04_exact_condition` yields typed HELD (no denominator or cells).
Additional negative branch preserves the **literal** inherited test's
`contradictory positive cell` refusal for top resolved0 with positive
nested cells; malformed 2-vs-3 partial remains a distinct refusal.
No real original-source incomplete-case runtime claimed. Tests NOT_RUN.
