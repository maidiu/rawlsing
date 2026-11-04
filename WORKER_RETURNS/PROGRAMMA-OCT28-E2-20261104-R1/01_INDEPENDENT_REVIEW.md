# PROGRAMMA OCT28-E2 independent implementation review

**Verdict `REVISE_EXACT_MATERIAL_DEFECTS`.** This return supersedes the runner hold in [00_RETURN.md](00_RETURN.md). The user selected this nonauthor reviewer. Desktop turn `01a1a8ba-cae8-79c1-9d9e-5d7d022ad035` in chat `01a1a88d-ae9d-7f91-b62f-4a08f7bf9591` records GPT‑6.1 Sol High. E1 was implemented in separate chat `01a1a867-3437-7560-9122-77ffa965dbe4`. The reviewer controlled both detached worktrees and ran Python directly on the local S2 runner.

| Reviewed object | Exact cut |
| --- | --- |
| Protected PRE-MAIN and measured baseline | `ba165a6a073dfdac0cb2e993ab8111ebb5ef404c` |
| E1 implementation | `4bd17accf0104ac05167c40a43076606e13c8448` |
| E1 final return and packaged harness | `cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8` |
| P41 runtime exercised | `f27d1101048638bba395143a48efb7ef00bfcda4` |
| Synthetic 12-row SAV SHA-256 | `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b` |

## Material defect

`rawlsing_next/pre553_empirical_query.py::_release_index_for` checks the cached index's sealed release instance and exact universe reference. It admits a replacement payload carrying those same two identities.

The independent [probe](probe_same_identity_cache.py) warms the cache through ordinary I03, replaces its respondent map with a read-only map omitting R1, then repeats the identical query against the same untouched sealed repository. Both results are `SUPPORTED`, with different exact fact bodies and refs. The original and restored fact hash is `7dc14856de18670198b20039d90c94cc93cab19d1029128dfec41447b6ce2690`. The damaged entry yields `496db04ff0167f35ae59a8d5abbaac7605f36bfd607a6567242888ed642634ea`. Deleting the entry and running the same query reconstructs the exact original result and fact body. The injection replaces the private in-process cache entry directly. The reviewer observed this failure under deliberate fault injection, with the normal immutable entry performing correctly. [Exact probe output](cache-fault.json)

The next implementation cut must ensure that same-release, same-universe payload corruption either refuses before fact publication or rebuilds from sealed topology and returns the exact original output. Keep this fault in the review court alongside the existing foreign-index, risk and current-authority tests. Remeasure the joined improvement after the repair.

## Independent bounded results

The existing carrier-neutral executor imports `rawlsing_next.pre553_empirical_query.execute_empirical_query` in both worktrees. [Import readback](imports.log) records separate file digests from each cut. This confirms the actual caller and places the changed code on the candidate branch. PRE-MAIN still selects its baseline implementation.

Route B, I02, the I03/I05 owners, Batch and the resumed R04→R05/P41 consumer ran on the synthetic fixture. The native release, query, predicate, fact bodies, replay and discovery refs, authority and projection roots, checkpoint bytes, and P41 consumer values and view hash matched within both baseline/candidate pairs. All seven I03 workload scenarios matched their complete result envelopes at 1, 8 and 150 rounds. On both cuts P41 refused a foreign upstream learned-evidence binding with `R05_N10E_EVIDENCE_BINDING_MISMATCH`. Restoring the determinant reproduced the original view hash. The joined path also refused revoked issuance and wrong source with `WorkloadAdmissionError`.

| Paired joined observation | Baseline | Candidate |
| --- | ---: | ---: |
| First pair wall | 31.456 s | 24.246 s |
| Reverse-order pair wall | 25.288 s | 23.697 s |
| Index builds, both pairs | 1,328 | 6 |
| Index time, reverse-order pair | 1,457.96 ms | 7.42 ms |
| Peak RSS, reverse-order pair | 249,626,624 B | 247,664,640 B |
| Serialized checkpoint | 28,017 B | 28,017 B |

The reverse-order pair showed a 6.3% reduction in end-to-end wall time. Pair-to-pair wall variation limits the precision of the estimate. [Independent comparison](independent-comparison.json) records the host, phase timings, cold and warm query counts, memory and storage, and content digests. The cache is in process. The joined test independently exercises the existing exact logical checkpoint and a fresh-process replay. Power-loss or persisted cache recovery remains outside this result.

The [candidate related suite](candidate-suite.log) passed 201 tests with one skip for the installed Stata extended-missing capability. The existing index-reuse [proof witness](candidate-proof.log) caught the bypass at its target assertion and restored the positive result. The joined fresh-process pytest passed independently in the [baseline](base-cold-joined.log) and [candidate](candidate-cold-joined.log) worktrees.

The historical HQ282 candidate at `73d45f3ac6a50fbee6666ad3a5023840f01ef196` durably commits individual work units and replans from a separate journal. E1 reuses the native index builder and current Route B/Batch/custody path. The current fixture exercised restoration from an exact joined checkpoint through the actual P41 consumer. The historical journal serves a separate persistence contract. The existing R4/R5/Parquet code serves physical normalization and carrier persistence. The measured gain comes from reuse of in-process I03 topology.

## Separate dispositions

| Dimension | Disposition |
| --- | --- |
| Engineering | Measured benefit independently reproduced. Revise same-identity cache admission. |
| Scientific semantic parity | Exact on the intact synthetic paths observed. Failed under same-identity corruption, which issued a changed supported fact. |
| Source and original-native permission | S2 synthetic fixture only. S3 and original35 science and issuance remain held. |
| Protected receiving | Hold the exact candidate. The qualified PRE-MAIN owner can consider a repaired and independently accepted diff through protected CAS. |

The defect affects `W05/P03` topology reuse and `P04/P10` evidence and performance claims. `W01/W06/P05` exact logical resume is verified at the joined fixture scope. `W03/P01` compact realization and `W04/P02` cross-session acceleration remain open. This review is an input to incumbent Pyat HQ's existing PROGRAMMA records.

## Reproduce

Use the E1 [pinned harness](../PROGRAMMA-OCT28-E1-20261104-R1/profile_oct28.py) and SAV at the hashes above. In each detached worktree set `PYTHONPATH=.`, `PYTHONHASHSEED=0`, and `PYTHONDONTWRITEBYTECODE=1`. Run the joined measurements sequentially in baseline/candidate/candidate/baseline order. Run the other commands under the candidate unless specified.

```sh
python3 "$profile" joined "$scratch" --instrument
python3 "$profile" queries "$scratch" --instrument --rounds 1
python3 "$profile" queries "$scratch" --instrument --rounds 8
python3 "$profile" queries "$scratch" --rounds 150
python3 "$review/probe_same_identity_cache.py"
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py.proof.json --root .
python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 -q -o addopts= -p no:cacheprovider
```

The pytest first-consumer command runs from both cuts. The candidate related-suite command is the first line of E1's [green.log](../PROGRAMMA-OCT28-E1-20261104-R1/green.log).
