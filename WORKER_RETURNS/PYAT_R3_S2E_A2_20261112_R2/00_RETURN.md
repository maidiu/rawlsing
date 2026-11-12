# PYAT R3 S2-E — Agent A return on B's adversarial descendant

**Disposition:** \`A2_SOURCE_GROUNDED_REPAIR_COMMITTED__CI_DID_NOT_START__NOT_G5_ACCEPTED\`.
This is the **same** A→B→A implementation lineage, not a replacement statistics engine or a parallel campaign. Everything below distinguishes a source-derived code correction from a successfully executed native proof.

## 1. Exact immutable artifact and provenance

- Governing scope: original P2-06, [#919 S2-E G1–G5](https://github.com/maidiu/rawlsing/issues/919), [#909 R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), protected PROGRAMMA Pyat, MCR-lite.
- A's frozen previous code: \`d7af5b8df922caa86bcd36a7baa0bbb55b43742d\`, [prior executed A CI](https://github.com/maidiu/rawlsing/actions/runs/43275018294): 78 native/hostile/inherited and 19 S2-F preservation tests PASS **at that code cut only**.
- B's frozen source: [PR #963](https://github.com/maidiu/rawlsing/pull/963), HEAD \`529444b6126256fd803e90a758fa4d0be3f4d541\`; B's actual repair commit \`56ce7299508d2d28d2eefb6a6a7f6fbe93360103\`; pre-repair attack \`5edc5091114e7bd99fb8e03384a404a8ccfa4ddf\`.
- **Frozen A2 code and test cut:** \`75d4a24bddcfdc5bd1553bd48f130d64f5d5b1e3\`. Subsequent return files are documentary only, not a new code cut.
- Separate A2 writer branch: \`agent/pyat-r3-s2e-a-counterattack-20261112-r2\`. [Draft PR #966](https://github.com/maidiu/rawlsing/pull/966), explicitly based on the **B frozen branch**, not protected PRE-MAIN. Compare B→A2: **three file paths only**:
  1. \`rawlsing_next/pre553_s2e_exact_conservation.py\` — native output auditor only;
  2. \`rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py\` — five new fully rehashed native-Batch attack/restoration tests;
  3. \`.github/workflows/pyat-r3-s2e-a.yml\` — include those tests.
- No changes to native I03/F1–F4 arithmetic, I05 original evaluator, grouped-core optimization, Batch execution, saved-store S2-D, accepted S2-F, original35 authorizations, actor systems, paused W03/W04, or protected branches.

## 2. B's actual victories and what is preserved

**B01 genuinely found a false I05 empty-claim hole**: A's earlier auditor hashed \`ExactBoundedDiscoveryResult.valid_empty\` without deriving it from all terminal receipts. B's exact source-derived boolean check is sound at the pinned native I05 contract. Kept.

**B02 genuinely found a frontier replay hole**: A hashed the supplied top-level I05 replay ref without independently deriving the commitment to frontier, candidate receipts, facts and valid-empty state. B correctly derives the native replay namespace and SHA256 preimage. Kept.

**No materially false B accusations were established.** B itself checked and retained A's actual same-respondent three-way F4, separate bidirectional F2 denominators, and the functioning first-consumer Batch. B's careful refusal to claim CI RED→GREEN was correct. Its two new tests remain preserved without modification.

**Incomplete victory:** a correct *outer* replay still accepts a self-consistent but forged *inner* candidate receipt unless candidate identity, role/fact closure, native candidate replay and exact authority frontier are independently checked.

## 3. A2's new, causally targeted corrections

The source comparison is directly against \`pre553_discovery_exact.py\`: native \`_candidate()\`, \`_compile_frontier()\`, \`_verify_discovery_authority()\`, \`execute_exact_bounded_discovery()\` and \`_derived_ref()\`. Neither author-side assertions nor re-hashing an attacker-controlled object are treated as sufficient.

**A2-01 candidate replay and producer root**: derive per-candidate replay ref from native contract, issued discovery authority, evaluated frontier, candidate ID/hash, terminal coverage, all candidate fact refs, exact release refs and I03 contract. Require exact match to both \`receipt.replay_ref\` and \`producer_replay_locator_or_reference_root\`. Attack changes a candidate replay, rehashes the full public receipt, rebuilds the outer I05 replay and updates the completed Batch receipt. Test: \`test_a2_rehashed_candidate_replay_and_rehashed_outer_frontier_refused\`.

**A2-02 winner and actual role/fact closure**: derive candidate SHA256 identity from declared family, rule ID, winning predicate, ordered query roles, validation rule and exact ancestry refs. Verify role names unique, referenced I03 fact preimages exist and belong to the correct exact role query, union equals candidate fact refs, and validation fact refs close without loss. Attack replaces the winning predicate with another *actual executed* native predicate and rehashes all affected public objects. Test: \`test_a2_rehashed_wrong_winning_predicate_and_outer_refused\`.

**A2-03 whole issued frontier rather than claimed totals**: with the original \`RuntimeObjectCatalog\`, re-run **only the native pre-search authority grammar compiler**, **not I03 computation**, to reconstruct all declared candidates, the real frontier ref, candidate hashes, winners, roles, ancestry and exact grammar ref. Compare all expected candidate IDs with all actual receipts. Attack supplies a coherent claimed zero-candidate result and correctly rehashed top-level replay with a completed Batch receipt, despite the real issued grammar being nonempty. Test: \`test_a2_declared_grammar_refuses_coordinated_missing_candidate_and_outer\`. This is a substantial G1 completeness improvement; it is not independent validation of the compiler's scientific theory.

**A2-04 coordinated forged ancestry**: inject fake branch ancestry *and rederive candidate hash, ID, inner replay, outer replay and Batch references*. All attacker-controlled hashes are valid; native authority grammar still rejects the substitution. Test: \`test_a2_coordinated_rehashed_ancestry_and_candidate_replay_refused_by_issuer_grammar\`.

**A2-05 typed terminal fate mismatch**: enforce frozen I05 terminal coverage→result-type pairs. Attack changes \`EVALUATED_SUPPORTED\` to \`EVALUATED_VALID_EMPTY\` but retains a supported typed receipt, updates candidate replay, receipt hash, outer replay and Batch refs. All outer B checks would still agree; the new check detects \`S2E_I05_CANDIDATE_TERMINAL_FATE_MISMATCH\`. Test: \`test_a2_rehashed_candidate_coverage_cannot_contradict_typed_fate\`.

**Self-attack/repair:** moved authority frontier reconstruction **after** cheap candidate-level checks to avoid unnecessary compiler work on already invalid public receipt material. Exact B positive/negative tests and A inherited tests are still included in the CI command.

## 4. Executable proof and exact CI boundary

Run from the repository root with Python 3.11 and \`pytest pandas pyreadstat pyarrow duckdb\`:

\`\`\`sh
PYTHONPATH=. python -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py

PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
\`\`\`

**Do not report RED→GREEN:** [A2 exact-head workflow 43287533659](https://github.com/maidiu/rawlsing/actions/runs/43287533659), at **\`75d4a24b...\`**, reported failed within four seconds, with **no executable job steps**. Earlier [A2 workflow 43286588528](https://github.com/maidiu/rawlsing/actions/runs/43286588528) failed the same way; a requested failed-job rerun did not execute. B's [RED](https://github.com/maidiu/rawlsing/actions/runs/43282276800) and [GREEN](https://github.com/maidiu/rawlsing/actions/runs/43282556270) also did not run a test. The inaccessible GitHub runner is an operational blocker **for verification**, not evidence of a Python regression or a code PASS.

**What was verified:** independent GitHub code readback, exact B→A2 fast-forward/3-file diff, source-derived formulas and issuer compiler invocation, immutable frozen code cut, complete executable tests committed, actual CI behavior. **What was not verified:** execution of B's two tests or A2's five tests against this SHA, baseline regression preservation at this SHA, measured output graph/elapsed/memory on this SHA, and independent G5. A's older 97 passing tests belong solely to A's older SHA.

## 5. G1–G5 and scientific/authority grades

| Gate | Actual current result |
|---|---|
| G1 full exact science and output | **PARTIAL**: corrected code covers original sourcefree candidate/fate/role/frontier obligations; no original35 full operation universe/issuer evidence |
| G2 whole output graph parity | A old code **PASS scoped**; **NOT EXECUTED** on B/A2 head |
| G3 mandated adversarial controls | A old controls passed; B two and A2 five native tests **COMMITTED, NOT EXECUTED** |
| G4 economics/recovery | **PARTIAL**: A tiny 12-respondent sourcefree case measured one core hit but no speedup; added grammar recomputation's cost unmeasured; S2-D saved store pending |
| G5 independent nonauthor receiving | **NOT RUN**, no authorization to self-accept |

Engineering: \`S2_E_SOURCEFREE_PATCH_PREPARED__RUNTIME_UNVERIFIED\`. Science: \`NO_ORIGINAL35_NATIVE_SCIENCE_LICENSE\`. Source: \`NO_NEW_ISSUER_OR_SOURCE_RIGHTS\`. Authority: \`NO_ACTOR_OR_HUMAN_CONSENT_GRANT\`. Integration: \`DRAFT_PR_ONLY__NO_PROTECTED_MERGE\`.

## 6. Strongest legitimate remaining attacks and rejected alternatives

- **Immediately execute** B's two and A2's five hostile tests, plus real F1/F2/F3/F4/I03/I05/Batch parity, changed upstream value, restoration and S2-F regressions at this actual frozen code SHA. The CI runner blocker must not be converted to a green claim.
- If any failure reproduces, inspect the native producer's exact receipt semantics and repair causally in **one bounded** exchange, not another general review chain.
- Test larger, mixed weighted/RAW and repeated-occurrence/routing UNKNOWN/unsupported-topology cases, including exact \`Fraction\` and separate authority/design/estimand key guards; initial A five-unit Batch was a limited synthetic workload.
- Whole-frontier recompilation adds computation and memory overhead. Quantify it with actual source opens, cold/repeat cost, process-tree RSS, output/scratch bytes and a typed cap when the applicable full workload is made available. The current SHA does **not** demonstrate scale/100k cap.
- Incomplete saved-store/partial-resume output preimages belong to the pending **S2-D** seam, not a permission to fabricate complete Batch evidence.
- Source issuer and revocation currentness, source facts and independent scientific qualifications are not authenticated by a self-hashed receipt or a repeated native grammar compiler. G5 remains an independent **third reviewer**, neither A nor B.

**Alternatives rejected:** discarding B's valid repairs, rewriting F1–F4 as a second statistics engine, treating a valid global replay ref as proof of actual declared candidate coverage, claiming an unrun CI as a regression PASS, forbidding bounded sourcefree work because S2-D remains open, or adding another administrative acceptance court.

**STOP state:** \`AGENT_A_RETURN_FROZEN__NO_MORE_GENERAL_DUEL_ROUNDS__EXECUTED_TEST_RECEIVING_PENDING\`. Preserved B's enhancements; no competing implementation, protected merge, external rights promotion or side commission.
