# PROGRAMMA OCT28-E3 — I03 cached-index integrity repair

**Disposition `AUTHOR_SIDE_GREEN_READY_FOR_E4`.** The exact E2 cache fault reproduced on E1 and recovered automatically on E3. The selected suite and the synthetic joined checkpoint and actual P41 reader passed on the repaired cut. Independent review remains pending.

| Object | Exact identity |
| --- | --- |
| Repository and branch | `maidiu/rawlsing`, `agent/programma-oct28-e3-cache-integrity-repair-20261104-r1` |
| Protected baseline | `ba165a6a073dfdac0cb2e993ab8111ebb5ef404c` on `integration/pre-main-reconciliation-r1` |
| E1 implementation and unpatched RED | `4bd17accf0104ac05167c40a43076606e13c8448` |
| E1 fixture and profiling harness | `cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8` |
| Binding E2 review and probe | `59eceb6917f2bb8fb0038bf7a036a0cdedac5069` |
| E3 code and tests | `43d2b70ebae4d183aadbd9694624575857fd100f`, direct child of E1 implementation |
| P41 runtime exercised | `f27d1101048638bba395143a48efb7ef00bfcda4` |

The duplicate Browser commission supplied the existing E3 code commit. Its model and effort are unverified. After the user clarified custody, the single local return operator reused that exact code and ran the S2 proof, measurements and publication. Codex Desktop session `01a1a8de-8f37-7962-aff6-46dd8aa5b261`, agent `/root/oct28_e3`, ran as GPT-6.1 Sol High and was distinct from the E2 reviewer. The immutable return appends evidence to the original code commit, preserving its authorship and ancestry.

## Repair and fault model

- `rawlsing_next/pre553_c11_repository.py` holds repository-local strong references to each built index and its original fields, separately from the cache slot and under the existing lock.
- `rawlsing_next/pre553_empirical_query.py` checks those identities plus the sealed release instance and exact universe. A mismatch causes a rebuild from the sealed C11 release before evaluation. The check compares a fixed set of fields, including immutable mapping proxies and tuple payloads. The hit check has constant cost in the size of the respondent graph.
- `rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py` adds the original respondent-map fault, top-level map replacements for respondent/event/coordinate/routing/weight fields, missing attestation, and 32 requests across eight threads verifying a single cold build. The existing reuse test exercises foreign release/universe, denied authority, wrong risk, and restoration. The related suite also exercises exact zero, domains, occurrence and weighted cases.

The fault model is a substituted private index slot or replaced top-level cached payload field before a query checks the cache, with sealed C11 and the separately held originals intact. Arbitrary interpreter or process-memory mutation, coordinated tampering with the attestation or sealed release, and malicious writes during use are outside this check. All source and authority decisions still pass through the current release and per-query validation. The existing authority and public carrier contracts govern every query.

[Import readback](imports.log) verifies the callable identity on all three cuts. `CarrierNeutralResearchExecutor.execute_i03` resolves its exact query and predicate and calls the owning `pre553_empirical_query.execute_empirical_query`. I03 resolves the exact release/universe, looks up or builds the topology through `_release_index_for`, checks current authority and evaluates. The first-reader module is byte-identical across the cuts. The joined harness runs Route B and native I02/I03/I05 through Batch, captures and resumes the R04 checkpoint, and reaches the actual R05/P41 consumer.

## Exact RED and recovery

The [original E2 probe on E1](e1-original-probe.json) obtained a `SUPPORTED` fact at `496db04ff0167f35ae59a8d5abbaac7605f36bfd607a6567242888ed642634ea` after removing R1 from the replacement read-only map. Its untouched and deletion-restored fact was `7dc14856de18670198b20039d90c94cc93cab19d1029128dfec41447b6ce2690`. The [same probe with assertions before deletion](probe_exact_auto_rebuild.py) failed at exact result equality on [E1](e1-exact-auto-rebuild-red.log). On [E3](e3-exact-auto-rebuild.json) it passed exact envelope, fact body, fact ref and replay ref equality, and verified the poisoned entry had already been replaced. The subsequent delete/rebuild also returned the same exact fact.

- [Focused repair file](e3-focused.log) passed 16 tests.
- [Related suite](e3-related-suite.log) passed 209 tests with one skip for the installed Stata extended-missing capability.
- The fresh-process checkpoint/resume test reached P41 on [protected baseline](base-cold-joined.log) and [E3](e3-cold-joined.log). The joined fixture refused the foreign upstream evidence binding with `R05_N10E_EVIDENCE_BINDING_MISMATCH`, restored its exact view, and refused revoked issuance and wrong source with `WorkloadAdmissionError`.

## S2 cost and output parity

Sequential baseline/E3/E3/baseline runs used the same exact 911-byte, 12-row synthetic SAV with SHA-256 `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b`. Each process began with empty in-process cache and then exercised reuse within the workload. The elapsed time is the instrumented joined operation, excluding P41 runtime archive extraction. Peak RSS covers the process. The operating system managed its ordinary filesystem cache.

| Measurement | Baseline | E3 |
| --- | ---: | ---: |
| Joined wall, forward pair | 29.484 s | 27.089 s |
| Joined wall, reverse-order pair | 25.802 s | 25.371 s |
| Index builds, each run | 1,328 | 6 |
| Index build time, reverse-order pair | 1,462.02 ms | 7.24 ms |
| Peak RSS, forward pair | 243,867,648 B | 247,910,400 B |
| Peak RSS, reverse-order pair | 249,503,744 B | 243,974,144 B |
| Serialized checkpoint | 28,017 B | 28,017 B |

Joined wall reductions were 8.1% and 1.7%. The difference across orderings limits the precision of the improvement. In two uninstrumented E1/E3 warm-query pairs at 150 rounds, summed case wall was 6.695/6.681 s and 6.715/6.684 s. The observed differences were 0.2% and 0.5%, so no wall penalty was resolved at this scale. Separately instrumenting E3 measured 1,950 attestation checks in 9.41 ms (4.83 μs per call) and eight attestation creations in 30.3 μs total, including probe overhead.

[Measurements](MEASUREMENTS.json) retain host and dependency pins, phase timings and parity digests for full fact, reference and replay material, release and authority roots, checkpoint and P41 values. All seven complete query result envelopes matched at 1, 8 and 150 rounds. [Native identities](NATIVE_IDENTITIES.json) records joined fact-body roots, sampled exact refs and replay refs, workload replay identity and complete P41 consumer values. The exact view hash was `c6aaef3c9816cdd63601703f4de52adf58d86ef0382adccb7cb6764f53812cf5`. [Timing assertions](timing.log) record both paired parity checks, warm cost and attestation probe output.

## Reproduce

Use detached baseline and E3 worktrees named `base` and `e3` under a writable scratch directory. Set `e1_code` and `e1_return` to detached worktrees at their exact cuts above, and `packet` to the absolute directory holding this return. The benchmark script checks all four heads and the fixture digest before running the [pinned E1 harness](https://github.com/maidiu/rawlsing/blob/cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8/WORKER_RETURNS/PROGRAMMA-OCT28-E1-20261104-R1/profile_oct28.py). Run benchmarks sequentially. The local [input checksums](inputs.sha256) identify the exact SAV and harness used.

```sh
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
(cd "$e1_code" && python3 "$packet/probe_exact_auto_rebuild.py") # expected assertion RED
(cd "$scratch/e3" && python3 "$packet/probe_exact_auto_rebuild.py")
(cd "$scratch/e3" && bash "$packet/related-suite-command.sh")
for cut in base e3; do
  (cd "$scratch/$cut" && python3 -m pytest \
    rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 \
    -q -o addopts= -p no:cacheprovider)
done
bash "$packet/bench.sh" "$scratch" "$e1_return" "$e1_code"
python3 "$packet/compare.py" "$scratch/evidence" >"$scratch/evidence/comparison.json"
python3 "$packet/summarize.py" "$scratch/evidence"
```

## Receiving boundary

The author-side evidence addresses `W05/P03` cache admission and the bounded `P04/P10` evidence and performance claim. E4 requires a qualified independent high-reasoning reviewer, separate from both code and return authors, to replay the exact E2 RED and E3 recovery, review the stated fault model and current source/authority refusal paths, and reproduce the joined parity and cost measurements on the pinned S2 fixture. Carry forward E2's open compact realization and cross-session acceleration boundaries. S3, original35, FF/N9/N11, Sorok, scientific issuance, and protected receiving remain held. Protected merge and CAS require the competent receiving owner.
