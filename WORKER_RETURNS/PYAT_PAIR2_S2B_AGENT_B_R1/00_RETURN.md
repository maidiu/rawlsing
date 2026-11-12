# PYAT R3 / Pair 2 / S2-B — Agent B adversarial construction return

**Status: `REVISE_EXACT_DEFECT__DERIVED_CERTIFICATE_IMPROVED__FULL_S2B_INCOMPLETE__G5_NOT_RUN`.**

**Controlling packet:** [#919 S2-B/P2-02](https://github.com/maidiu/rawlsing/issues/919), [#909 R3/R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), [PROGRAMMA PYAT](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md), and [adopted MCR-lite](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md). The user's top-level pasted commission says **S1-C / P1-04 / #918** while the provided adversarial Agent A artifact is **S2-B / P2-02 / #919**. We acted only as **S2-B Agent B** on the explicit supplied code artifact. This return is not an S1-C fate-conservation receipt.

## 1. Immutable lineage and preservation

- Opponent: [draft PR #952](https://github.com/maidiu/rawlsing/pull/952), Agent A frozen `d5d6577b557fa8ced2dbb42d190ab254ab983b19`; tested source `2d217c63653f98a56ac23182f766a059460e8d68`.
- Antecedent: S2-A [PR #944](https://github.com/maidiu/rawlsing/pull/944) at `d3814d08dbe03b8464ac6fff4164765179869213`, G5 still pending; nothing here changes that grade.
- B descendant: [draft PR #954](https://github.com/maidiu/rawlsing/pull/954), `agent/pyat-pair2-s2b-b-certificate-forgery-20261112-r1`; exact **tested code commit `96877c0c8315d06033371a622dc306419340fc57`**.
- Original protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` was not merged into or edited. No W03/W04, source/native rights, authority, Sorok, original35 or S2-C work.
- Changed production file `rawlsing_next/_pre553_external_i02_certificate.py` at tested blob `ca25d777204d194daa7159100f7f8e17cc534094`. Test file `rawlsing_next/tests/test_pre553_external_i02_certificate.py` blob `4111dafa978bdac6bd5f47ab4b8222837250ee9f`; workflow blob `513f02b83ad3d73068378cc11dbf35e60cebf040`. The other inherited query evaluator, scientific compiler, and native semantics are unchanged by B.
- Evidence commits: first failing-three tests `7eb268b5a614626d51cad2b80e364d820888525b`; initial B fix `c84914692791ab4fda14c96d57e0aec134e64769`; self-attacking fourth case `82b15d51d26b7d16123d1f75fe4952c6a97a3a26`; sealed-state fix `96877c0c8315d06033371a622dc306419340fc57`.

## 2. Predecessor strengths verified, not destroyed

A implemented a real, deterministic SQLite-backed **DERIVED** whole-I02 corpus/semantic-selector certificate from a preexisting genuinely I02-sealed `C11LogicalRelease`, with separate logical and physical roots, complete indexed object/closure/selector comparison, native I03 event selection, sourcefree changed-value/restoration and crash/orphan negatives. We retained its original 84 tests unchanged and reproduced them passing as part of the final 88-test suite. The 2,048-respondent probe reproduces the original logical root `025e17afa43b083a1aa557cab257f63d06716761da25e8575efb431996a88277` and physical root `15be249f8da207d63c45e2999e9238c879b367d809b738bcb97cc8c99da16575`. The proof remains **sourcefree and derived**, not original-source or full source-direct I02.

## 3. Four reproduced hostile failures, two causal correction groups

**Group F01 — fake installation accepts a false selector:** In A code, `install_sourcefree_external_i02_i03` checked `repository` exact type but accepted arbitrary `certificate.roots`, `respondent_refs()`, `selector_refs()`. The native adapter wrapped a crafted object with the authentic roots and respondent census but omitted selector results. Likewise a `VerifiedExternalI02` subclass could override selector retrieval. The expected-RED tests proved both were accepted by the pre-repair installer, not refused. Source [RED run 43276452169](https://github.com/maidiu/rawlsing/actions/runs/43276452169): **84 passed, 3 failed** (two forgery acceptance plus a closed-reader negative). **Repair:** require `type(certificate) is VerifiedExternalI02` before native cache installation, and use slots to exclude per-instance selector monkeypatching.

**Group F02 — lifecycle and post-validation state replacement:** A retained a native disk index after certificate close; a later native selector raised uncontrolled `sqlite3.ProgrammingError` rather than a typed integrity refusal. The first fix installed `_ensure_open` checks in verifier and disk-backed sequence reads. Hostile review of B's own fix then showed the exact verified object still permitted replacing `reader.db` *after* hash/root verification with an unanchored copy stripped of native postings. The real native I03 result differed from the oracle. [Second RED run 43277256665](https://github.com/maidiu/rawlsing/actions/runs/43277256665): **87 passed, one new test failed specifically because a post-verification connection swap corrupted real I03 facts**. **Repair:** once cold validation completes, seal certificate path/database/roots/closed-state assignment; only `close()` can transition to typed closed state. Readers refuse attempts to use a closed certificate before issuing selected facts.

## 4. Execution proof and resource honesty

- [Initial RED](https://github.com/maidiu/rawlsing/actions/runs/43276452169): 84 PASS / 3 FAIL on counterfeit Protocol, counterfeit subclass and closed witness.
- [First repair GREEN](https://github.com/maidiu/rawlsing/actions/runs/43276551713): 87/87 PASS.
- [Self-attack RED](https://github.com/maidiu/rawlsing/actions/runs/43277256665): 87 PASS / 1 FAIL, with an actual native I03 fact discrepancy under post-verification DB reassignment.
- [Final tested GREEN](https://github.com/maidiu/rawlsing/actions/runs/43277344553): **88/88 PASS**, native query and I02/S2-A + repository regression suites; separate 2,048-respondent sourcefree probe PASS.
- Final isolated probe: 24,801,280 retained certificate bytes, 5.94 s construction, 0.153 s fresh full verification; 2,112,161 peak Python allocation bytes during builder-only tracing; process test peak RSS 101,400 KB. The 88-test suite process peak RSS 193,804 KB. These runner-specific values are measurements, not guaranteed performance improvement. Logical and physical roots preserved.
- Peak scratch/process-tree aggregate, 100k integrated original source/build, source-direct semantics from source packets, and 6 GiB full pipeline: **NOT_MEASURED / NOT_RUN**, not PASS. No new real original35 eligibility, competent scientific/root issuer or S2-C physical cold reader.

## 5. Original contract G1–G5 disposition

| Gate | B result | What remains |
| --- | --- | --- |
| G1 | **PARTIAL** | Inherited M01–M18 v1 coverage and exact closure preserved; no independent source-direct validation, and external source-equivalence/current issuer separate |
| G2 | **PARTIAL** | Actual native I03 positive and changed/restored facts preserved, forged and closed verifier refusal repaired; source-direct S2-B full certificate missing |
| G3 | **PARTIAL** | Four genuine adversarial breaches repaired; original 84 tests conserved; independent exhaustive source-direct no-drop/negative proof remains |
| G4 | **PARTIAL** | Derived disk certificate and 2,048 sourcefree benchmark measured; upstream full in-memory `ReplayManifest.closure_refs`, `C11LogicalRelease` and 100k/process-tree/scratch not repaired |
| G5 | **NOT_RUN** | Independent G5 belongs to neither A nor B and requires completed G1–G4 at the frozen packet scope |

**No entire S2-B completion or acceptance claimed.** The decisive inherited engineering defect remains: `build_sourcefree_external_i02` still starts from a fully materialized v1 I02 release, including heap-sized `ReplayManifest.closure_refs`. Its I03 bridge also uses `_build_release_index` and the in-memory repository; full cold saved physical release belongs separately to S2-C, but bounded source-direct **I02 validation itself** belongs to S2-B and is genuinely unfinished. This is not a permission HOLD disguised as engineering success.

## 6. Refuted attacks, admitted weaknesses and next attack

- **Refuted:** A's real external logical/physical roots and sourcefree native I03 parity were not mere fake receipts; 84 inherited cases survived. A 2,048 fixture cannot be retroactively declared 100k/native proof.
- **Refuted:** a missing original35 issuer does not forbid implementing S2-B's independent sourcefree validation; conversely, an author-created manifest is not an external root issuer. S2-C disk-native event bodies and W03/W04 must not be smuggled into this packet's code ownership.
- **New B limitation:** `__slots__` plus post-init immutability protect ordinary Python assignment at this API boundary; they do not provide tamperproof security against arbitrary co-resident Python execution using `object.__setattr__`, direct private repository mutation or malicious underlying file systems. Full TOCTOU across independently hostile filesystem actors/platforms is unproved. S2-B must not claim cryptographic process isolation.
- **New B limitation:** the corrected installer still retains upstream legacy I02 materialization and the already-sealed in-memory repository, so memory scalability does not improve. The new checks address *integrity*, not physical construction economy.
- **Next Agent A attack:** (i) produce a genuinely bounded direct-source I02 validator using actual S1-B/S1-E candidate semantics and M01–M18, no complete legacy `closure_refs` array; (ii) test 100k or a resource-scaled sourcefree equivalent with full scratch/RSS, genuine native I03 positive/negative/restoration, and fixed independently held roots; (iii) falsify B's assignment seal under a *permitted* caller, or demonstrate a legitimate certified reader class rejected wrongly; (iv) ensure no loss of original alias, occurrence, typed UNKNOWN/zero, routing, weights, authority, replay and test cases. Do not rename S2-C's cold physical body store into S2-B.
- **Decision:** retain the real B trust-boundary repair; return `REVISE_EXACT_DEFECT` for still-incomplete full S2-B. No extra speculative review committee or protected merge. Agent A may take its next substantive adversarial construction turn, and only a distinct nonauthor reviewer may grant G5 at an actually complete scope.
