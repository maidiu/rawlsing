# PYAT R3 — S2-E Agent B: adversarial descendant handoff

**Scope:** S2-E / P2-06 ONLY. Governing contract: [#919 S2-E](https://github.com/maidiu/rawlsing/issues/919) and [#909 R3C/R3S](https://github.com/maidiu/rawlsing/issues/909); exact first native reader is \`census_native_batch\` on real I03/I05/Batch output. No other R3 packet is recommissioned.

**Disposition:** \`B_CODE_REPAIRED__CI_NOT_EXECUTED__NOT_READY_FOR_G5\`. **Do not describe B's counterexamples as CI RED→GREEN.** They are complete, checkable test artifacts and source-control-flow defects, but the GitHub runner did not execute them.

## Exact lineage, changed artifacts, evidence

- Parent immutable **A frozen handoff**: \`4357675fc13cc933134bd3303e7efead7aeba4ea\`; actual A tested implementation: \`d7af5b8df922caa86bcd36a7baa0bbb55b43742d\`; [A PR #951](https://github.com/maidiu/rawlsing/pull/951).
- B separate descendant branch: \`agent/pyat-r3-s2e-b-followupper-20261112-r1\`; [B draft PR #963](https://github.com/maidiu/rawlsing/pull/963), targeting *same isolated integration base* as A, with no protected merge.
- **Test-only pre-repair attack cut:** \`5edc5091114e7bd99fb8e03384a404a8ccfa4ddf\`. Adds exactly two explicit B hostile native first-reader tests.
- **B repaired code/test cut:** \`56ce7299508d2d28d2eefb6a6a7f6fbe93360103\`. Two modified files and two additional tests, no evaluator/other-packet rewrites.
- Production: \`rawlsing_next/pre553_s2e_exact_conservation.py\`, source Git blob \`9dc02fb42377148875f097475128f886834d0888\` → \`7ca3cea24ffdcd2f7027033b1617d6fa50a2f552\`.
- Tests: \`rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py\`, B blob \`cbbe1bf04c6dfe32db53927429401f91e0bfbbab\`.
- Independent native source inspected: \`rawlsing_next/pre553_discovery_exact.py\` blob \`1b82b6df993bf14afa5e78782d988cba6e76b668\`. Its \`execute_exact_bounded_discovery\` computes \`valid_empty\` from all final candidate fates and the frontier replay as SHA256 of the contract, frontier ref, all receipt refs, all fact refs and that valid-empty boolean.

### What A genuinely accomplished and B preserved

A's tested native sourcefree five-unit Batch executes F1 marginal, both F2 directions with different denominator populations, F3 minority discovery, and true same-respondent three-way F4 with all eight cells, including observed zeros. Its own published exact-code CI [43275018294](https://github.com/maidiu/rawlsing/actions/runs/43275018294) reported 78 S2-E/native/regression tests plus 19 S2-F preservation tests passed. B preserved the complete existing query evaluator, discovery evaluator, grouped cache, Batch runner, issued workload, prior A tests, S2-F code and exact manuscript provenance. A correctly disclosed that tiny-batch group reuse had no demonstrated speedup and S2-D/original35/G5 remained open.

### B01 — FALSE EMPTY despite positive I05 fate (G1/G3)

At A's code, \`census_native_batch\` validates total candidate count, terminal receipt states and receipt identity, then **hashes \`output.valid_empty\` without checking its relation to the receipts**. The native \`ExactBoundedDiscoveryResult.__post_init__\` also does not check the empty-result semantic equation. A \`dataclasses.replace(native_result, valid_empty=True)\` therefore produces a structurally valid result despite its unchanged \`DISCOVERED_RESULT_SUPPORTED\` receipt, fact closure and Batch receipt. The exact A audit lacked \`S2E_I05_VALID_EMPTY_CLAIM_MISMATCH\`; a different digest is not a rejection. This is a source-level demonstrated missing check, with its native executable reproduction test committed but **not yet run**.

**Repair:** derive \`not receipts or all(receipt.typed_state == "VALID_EMPTY" for receipt in receipts)\`, require an actual \`bool\`, compare to the envelope; emit \`S2E_I05_VALID_EMPTY_CLAIM_MISMATCH\`. It uses precisely the existing native producer's predicate; it does not redefine discovery science.

### B02 — SUPPLIED REPLAY REF NOT AUTHENTICATED (G1/G2/G3)

At A's code, the audit includes \`output.replay_ref.as_dict()\` in its preimage digest without verifying that this hash and namespace commit to the actual native frontier's receipts, facts and empty-result state. A synthetic \`ExactRef("PRE553_I05_FRONTIER_REPLAY", "urn:rawlsing:pre553:i05:frontier-replay:sha256:ffff...", "ffff...")\` can replace the genuine result's replay ref while all actual native data and Batch receipt stay unchanged. \`ExactBoundedDiscoveryResult\` itself does not verify the equation. A's auditor hashes the false reference but has no source-derived check to refuse it.

**Repair:** recompute \`semantic_hash\` of the same **five** native replay material fields and native namespace used by \`execute_exact_bounded_discovery\`, construct the expected full \`ExactRef\` and require exact equality, emitting \`S2E_I05_FRONTIER_REPLAY_MISMATCH\`. Independent static readback confirmed equality of the original native and B field names, replay-namespace pattern and valid-empty rule. This is not a claim to authenticate original-source permission or to rerun I05 from scratch.

### Exact tests, status and self-attack

\`\`\`sh
PYTHONPATH=. python -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
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

New B test functions:
1. \`test_b_i05_valid_empty_false_absence_cannot_pass_native_output_census\`
2. \`test_b_i05_wrong_frontier_replay_is_not_an_accepted_complete_graph\`

Both use the **actual existing A native five-unit Batch**, assert rejection of one exact tamper, then restore and compare the complete original output census. The first tests a false negative/empty-fate declaration; the second tests false replay provenance.

**CI status must not be misrepresented:**
- [B pre-repair workflow 43282276800](https://github.com/maidiu/rawlsing/actions/runs/43282276800) and [B repaired workflow 43282556270](https://github.com/maidiu/rawlsing/actions/runs/43282556270) both reported failure, as did unrelated workflows triggered by these commits.
- GitHub Actions API exposed \`runner_id=0\`, empty \`steps=[]\` and completion within seconds for the affected jobs. Rerun requests succeeded at the API level, but the attempts also failed before any step.
- Therefore **no B RED/ GREEN tests or preservation regressions were executed**; both corrected runtime claims remain unverified. GitHub CI infrastructure availability/authorization needs independent attention, not a fabricated green receipt.

**Self-adversarial assessment:** The replay calculation was checked line-by-line against the actual native producer, not against A's description. A's eight-cell F4 test and denominator claims are independently supported by its code and prior CI and have not been overturned. B's patch adds only two additional checks to an existing read-only auditor; does not mutate F1–F4, fractions, risk sets, grouping, source build, Batch or S2-F closure. A legitimate producer with a different future replay schema would be refused by this versioned check (a **future-compatibility exposure**, not a demonstrated violation of the frozen contract). Complete original35 issuer/currentness and full saved-store/resume remain separate genuine holds. Process-tree RSS, larger economics and direct B performance have not been measured.

**Strongest next A attack:** execute the two B tests at the exact repaired code SHA; show both fail *for the specified reasons* on RED source and pass without changes to other native outputs on GREEN source. Then mutate I05 candidate-specific \`DiscoveryResultReceipt.replay_ref\` and \`winning_predicate_ref\` while preserving all relevant self-hashes to see whether the auditor continues to accept a fact/candidate closure whose *inner* replay or ancestry has been forged. Only promote a material discrepancy to repair if it reproduces against the already-frozen G1–G4 obligations and the real first consumer. Do not create a new generic hardening programme.

## G1–G5, authority and STOP

- **G1 PARTIAL:** complete bounded sourcefree keys/typed facts inherited from A; replay/empty cross-check added; no original35/full-operation census or B runtime proof.
- **G2 NOT_RUN at B code SHA:** A original code's five-unit native positive/parity was executed at A SHA, not the repaired B SHA.
- **G3 NOT_RUN at B code SHA:** two adversarial tests with restore assertions committed, but GitHub never started an executable test step.
- **G4 PARTIAL:** A's 12-respondent measurements, one reuse hit but no speedup; missing process-tree RSS/source/scratch/full saved-store demonstration is not green.
- **G5 NOT_RUN:** A and B cannot receive themselves. Independent nonauthor reproduction only after demonstrated applicable G1–G4.
- **Rights:** \`S2_SOURCEFREE\` engineering patch only, **not** original35 science, source-currentness, actor authorization or protected integration. \`HOLD_DEPENDENCY:S2-D\` still describes the full saved-store seam.
- **STOP:** \`AGENT_B_TURN_FROZEN__RETURN_TO_A_FOR_COUNTERATTACK_AND_NATIVE_EXECUTION_WHEN_AVAILABLE\`. No protected merge and no paused W03/W04 changes.

This is a stronger, exact descendant **in source code**, not yet a proven G1–G4-complete terminal result. B is not issuing G5 acceptance.
