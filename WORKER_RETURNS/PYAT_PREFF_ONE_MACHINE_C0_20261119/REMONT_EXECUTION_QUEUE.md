# REMONT — Growing sourcefree execution queue (OPEN)

**Queue identity:** `PYAT_REMONT_EXECUTION_QUEUE@1` · **Test custodian:** REMONT · **Runner/diagnostician:** OpenCode · **Major repair reviewer:** REMONT Browser · **Forward architecture:** PYAT HQ. This is one continuing commission, not a succession of isolated agents or a replacement PROGRAMMA.

**Repository/branch:** `maidiu/rawlsing` · PR #1164 · `review/pyat1158-mulch-physical-dhikr-20261119-r1`.

**Immutable evidence chronology:** User Mac first-fault at `a0b95cb7231601bbc228cf13b644851dd22c449d`, `PREFF_COURT=C4_FF_V3`: **19 tests / 9 PASS / 10 FAIL**, nine from DHIKR float identity, one mistaken I05 source identity collapse. Later Mac sourcefree full queue at **frozen `8c4e70ef0a3bc1a146f84504bd1ac5ff548f0fb0`**: **194 test executions / 177 PASS / 17 failure instances (16 unique nodes)**. Q001 13/13 PASS, Q002 8/8 PASS, Q003 7/8, Q004 66/78, Q005 83/87, Q006 HELD. Q004 12 share one supported FF01 null-field/ABI identity defect; Q003 one stale cold pin error regex; Q005 coordinate owner miscount and frozen mapping `.key` (plus repeated C4 red). These are **user/worker Mac local reports, not independent G5**, with unpublished JUnit under `.pyat-preff-remont-proof/8c4e70ef.../`. The repairs are code-committed at descendants of C5 and **NOT_EXECUTED at repaired HEAD**. Never transfer test results across SHAs.

## Single repeatable worker operation

**Executor:** `rawlsing_next/tests/run_preff_remont_batch.sh`. It checks a frozen `EXPECTED_PREFF_C0_HEAD`, rejects dirty tracked trees, runs every QID even after a preceding red, preserves each `junit.xml`, `pytest.log`, `exitcode.txt` and per-case exact SHA. Batch `index.csv` records each exit. No git writes or original wave operations.

At a clean worktree pinned to the current, explicitly recorded #1164 commit:

```bash
EXPECTED_PREFF_C0_HEAD="$SHA" \
bash rawlsing_next/tests/run_preff_remont_batch.sh \
  RMT-Q001 RMT-Q002 RMT-Q003 RMT-Q004 RMT-Q005 RMT-Q007 RMT-Q008
```

Without arguments the runner defaults to Q001–Q004, Q007 and Q008; Q005 remains the separately requested broad original regression sweep. Run specific QIDs as script arguments. Evidence lands at `.pyat-preff-remont-proof/$SHA/` by default; override with `REMONT_PROOF_ROOT` for a low-disk host.

**Growing rule:** Add a fresh numbered QID and its purpose, exact file(s), producer/consumer, positive/negative proof and triage owner here, and append one bounded suite to the launcher. Do **not** modify existing QID meanings or erase red/held evidence; supersede old IDs explicitly. OpenCode receives the same commission on every run, reads its latest queue and executes all eligible new QIDs against one frozen HEAD.

## Eligible pending first-fault tests

### RMT-Q001 — DHIKR sample numerics and exact identity
**Priority P0 · RUN_PENDING**
- **Actual test:** `rawlsing_next/tests/test_preff_c3_dhikr_comparative.py`
- **Producer:** `rawlsing_next/pre553_s04_dhikr_comparative.py`. **Upstream exact identity owner:** `rawlsing_next/pre553_empirical_objects.py` (must remain unchanged).
- **Positive:** real sourcefree I03→S04→DHIKR XOR; same-case n and contextual n conserved; pair synergy; bootstrap interaction rank, finite typed decimal output and explicit `read_dhikr_sample_estimate` Decimal consumer roundtrip; canonical hashes stable without a global source-identity rule change.
- **Falsifiers:** forbidden binary floats in receipt/source; NaN/Inf/uncanonical estimate acceptance; disabled low-N hold, false interaction, incorrect target count, sampling-right promotion.
- **Triage:** OpenCode for local codec mechanics; REMONT Browser if the numerical ABI or source identity ownership changes.

### RMT-Q002 — I05 distinct identity, same source-observed joint
**Priority P0 · RUN_PENDING**
- **Tests:** `rawlsing_next/tests/test_preff_c0_dhikr_first_consumer.py`; `rawlsing_next/tests/test_pyat1009_ff01_i05_role_ingress.py`; `rawlsing_next/tests/test_pre553_s04_i05_reception.py`.
- **Owner route:** `rawlsing_next/pre553_discovery_exact.py` → `pre553_s04_i05_reception.py` → `pre553_s04_ff01_consumer.py`, and alternate `field_forge_i05_role_ingress.py`.
- **Positive:** eight I05 candidate query/fact/role identities survive; four `VALID_EMPTY`, four `DISCOVERED_RESULT_SUPPORTED`; each carries the same observed full XOR joint cells, target roles, sample n=4, release and risk-set identity.
- **Falsifiers:** collapsing separate legitimate provenance, false equality for unlike underlying source evidence, lost I05 negative classification, role/fact misbinding.
- **Triage:** OpenCode for isolated assertion error; REMONT Browser for provenance/owner changes.

### RMT-Q003 — complete C4 first consumer through PRE-V3
**Priority P0 · RUN_PENDING**
- **Test:** `rawlsing_next/tests/test_preff_c4_ff_v3_empirical_handoff.py`.
- **Producer:** `rawlsing_next/pre553_s04_field_forge_v3_bridge.py`. **Inherited consumers:** `pre553_s04_first_consumer.py`, `pre553_s04_general_joint_algebra.py`, `field_forge_observed_research.py`.
- **Positive:** one genuine existing I03 fixture; S04 and FF01 receive exactly that source; DHIKR context n cross-checked to FF01; deterministic count-weighted complete-joint sourcefree hypothetical configurations; no independent marginal invention; low-N/zero/unknown abstention; independent-pin private cold replay without opening C11/I03.
- **Falsifiers:** forged/rehashed FF01/DHIKR, substituted source root, count mismatch, fabricated state combination, unauthorized V3 actor or FF02 structural promotion.
- **Triage:** REMONT Browser for source/actor/structural or cross-owner failures; OpenCode for bounded one-owner code bug.

### RMT-Q004 — upstream and downstream regression ring
**Priority P1 · RUN_PENDING**
- **Tests** (all under `rawlsing_next/tests/`): `test_pre553_empirical_objects_authority.py`, `test_pre553_s04_first_consumer.py`, `test_pyat1009_ff01_s04_consumer.py`, `test_pyat1009_ff01_generic_ingress.py`, `test_pyat1009_ff01_observed_research.py`, `test_pyat1009_ff01_cold_direct_estate.py`.
- **Positive:** strict original PRE553 no-float identity; unchanged upstream I03→S04 and FF01 first consumers; source risk and fact closure; positive/zero/negative exact counts; cold read and independently issued root controls preserved.
- **Falsifiers:** any historical negative assertion unexpectedly becomes positive; loss of source identity or issuer rights; alternative estimator or silent response-state reinterpretation.
- **Triage:** REMONT Browser if historical functionality/conservation involved.

### RMT-Q005 — existing C0_ALL_SMALL broad integrated sweep
**Priority P1 · ELIGIBLE_EXTENDED_RUN**
- **Existing executable:** `rawlsing_next/tests/run_preff_c0_first_fault_local.sh`, `PREFF_COURT=C0_ALL_SMALL`; batch runner calls this directly. Includes C3/C4, C11 physical/raw preservation, I05, saved-batch and interpretation checks. **Do not duplicate or replace its authority.**
- **Positive:** no regression in inherited C0 scientific/engineering machine. **Falsifier:** changed upstream behavior or new red, preserving old known reds at their historical SHAs.
- **Triage:** REMONT Browser for cross-cutting, OpenCode for isolated bug.

### RMT-Q006 — original-wave/scientific qualification
**Priority P2 · NOT EXECUTABLE HERE / AUTHORITY_HOLD**
- **No runnable test path authorized.** Needs explicit original-source entitlement, mapping edition, actual ARABBAR1/GSS material, survey design method and secure execution host. Do not turn this sourcefree commission into original wave runs. Separate owner issuance required.

### RMT-Q007 — C5 live contextual possibility service, history, contradictions and case offer
**Priority P0 · RUN_PENDING · NEW CONTINUING PRODUCT**
- **Actual tests:** `rawlsing_next/tests/test_preff_c5_continuing_contextual_prev3.py` (14 tests). **New implementation:** `rawlsing_next/pre553_ff_prev3_possibility_navigation.py`. **Upstream actual owners:** I03 `_pre553_query_common.QueryExecutionResult` → `pre553_s04_first_consumer.py`, `pre553_s04_dhikr_comparative.py`, `pre553_s04_field_forge_v3_bridge.py`, `field_forge_observed_research.py`. **Downstream:** PRE-V3 whole-case conditional offer; no Sorok actor mutation or structural admission.
- **Expected positive:** one actual native synthetic I03 multi-target joint and separately an I05 `VALID_EMPTY` candidate's still-supported I03 fact; exact pinned C4 FF01/DHIKR input; map all unconditioned source axes' values into conserved raw complete-case branch partitions; show source-observed target alternatives including ties/nonmodals (actual 5-to-1 minority vs separate ties); zero is NOT impossibility, low-N is held, continuing steps stop at held; reproduce whole observed joint configuration with deterministic seed, exact replay after cold private archive restore, never reread C11/I03.
- **Negative falsifiers:** independently invented marginal combinations, duplicate/foreign/mapped-by-guess axes, NaN/float source conditions, context escalation after low-N, missing external pin, counterfeit rehashed replay, incompatible source risk or state, falsely declaring minority a trait/cohort, fabricating world/actor permission.
- **Triage:** REMONT Browser for source/semantics/privacy/actor and cross-owner defects; OpenCode separately authorized for one-module bounded code mistakes. **No fake person.** All 14 tests and inherited Q001–Q005 remain NOT EXECUTED at the new C5 commit. Historical user Mac 10 fail/9 pass remains old head only.

### RMT-Q008 — repair-bound held-source/raw provenance ring (PF-038–041)
**Priority P0 · NEW / SOURCEFREE / RUN_PENDING**
- **Tests:** `rawlsing_next/tests/test_preff_c1_typed_condition_uncertainty.py` (native I03→S04→FF01 actual source-unknown roster, 1/4 unknowns and forged rehashed membership); `rawlsing_next/tests/test_preff_c0_raw_preservation.py` (original SAV/DTA raw physical witness, unmapped preservation, correct independent coordinate owners, frozen saved respondent identity).
- **Boundary:** Q008 covers the historical negative controls often missed by the Q004 FF01 parity test and Q005 broad C0; **does not replace** Q003/C4, Q004/FF01 or Q005 full prior-source regressions. For source fix PF-038, require source exact positive `test_pyat1009_ff01_s04_consumer.py` as Q004; assert supported `held_condition_membership_uncertainty` key fully absent, not serialized null.
- **Positive:** supported S04→FF01 exact historical generic receipt ref; HELD authentic source-unknown provenance remains restricted to S04 knowledge ref (count/denominator/source knowledge, NO roster exports/digest); no false joint support; all saved source cells retain own raw physical identity/typed missingness across mapping changes; owner authority applies to both emitted coordinate slots; frozen respondent mapping rehydrates with existing `exact_ref`.
- **Falsifiers:** C1 held state loses knowledge or exports member refs; Q004 parity still differs despite missing null; 5/10 coordinate false count; SAV/DTA `.key` failure; unbound response cells absent; counterfeit release or physical witness accepted; protected scientific authority inferred.
- **Routing:** REMONT Browser judges PF-038 original FF01 ABI/provenance; OpenCode bounded test corrections for PF-039–041; distinct independent G5 only after exact-SHA executed proof.
- **Exact state:** repaired source/test commits `826a500`, `a05c705`, `c98141d`, `212713a`; all `CODE_COMMITTED_NOT_EXECUTED` until rerun at one current frozen HEAD.


### RMT-Q009 — immutable historical RED/GREEN proof and macOS batch preflight
**Priority P0 · TEST_INFRASTRUCTURE · RUN_PENDING**
- **Test:** `rawlsing_next/tests/test_preff_remont_batch_guard.py`, registered in the SAME `rawlsing_next/tests/run_preff_remont_batch.sh` batch.
- **Producer:** current exact-head REMONT Q001–Q008 batch runner. **Consumer:** cumulative JUnit/log/exit/index evidence and old historical RED proof.
- **Positive:** the default queue includes Q005 and Q008; exact clean 40-hex HEAD; no previous proof directory overwritten; Bash 3.2/macOS nounset-safe execution.
- **Negative falsifiers:** stale HEAD, duplicate QID, original-wave Q006, unknown QID, existing immutable proof archive must refuse before executing a test or truncating any log. A prior RED sentinel survives byte-exact.
- **Routing:** REMONT Browser for proof custody/QID authority; separately user-authorized OpenCode BUG worker for a narrow shell syntax error only. Q009 pass is sourcefree, not G5 or original-wave rights.
- **Grade:** CODE/TEST_AUTHORED_NOT_EXECUTED; historical RMT-Q008 ownership and Q001–Q007 preserved.

## Required execution comment (PR #1164, linked to #1097)

One **version-pinned** report, including: exact tested SHA and git tree cleanliness; host OS, Python and pytest version; each QID with test files, exact command, summary, exit code and JUnit/log paths; first failure stack and minimal source trace; whether a failure is old/new/test-misstatement/owner contract; proposed smallest repair; affected upstream and downstream owners; historical negative controls to conserve; recommended **REMONT Browser vs OpenCode** with reason. Mark unrun items `NOT_EXECUTED`; do not call author runs independent G5 or protected acceptance.

**Repair boundary:** OpenCode executes and *suggests*, does not commit code in this standing commission; the REMONT Browser repair author has issued bounded fixes separately. A later separately user-authorized OpenCode bug flight may repair a narrow one-owner, no-new-ABI defect (approximately two implementation/test files maximum), with a fresh exact-head regression. Cross-owner, historical source/provenance, scientific/actor authority or substantive method changes go to REMONT Browser; architectural forward construction stays with PYAT HQ. REMONT keeps test execution history beside PF001–PF036 without making HQ wait for the queue.
