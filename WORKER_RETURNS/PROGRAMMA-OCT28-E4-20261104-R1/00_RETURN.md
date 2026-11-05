# PROGRAMMA OCT28-E4 independent S2 review

**`ACCEPT_SCOPED_WITH_PROTECTED_RECEIVING_RECOMMENDATION`**

Accept the sourcefree I03 shared-index implementation plus the E3 integrity repair at `43d2b70ebae4d183aadbd9694624575857fd100f` for qualified protected PRE-MAIN receiving. The original E1 payload fault reproduced independently. E3 rebuilt from the sealed C11 release and returned the original exact fact. Joined output remained byte-identical across the three implementation cuts. On this fixture, E3 retained the shared-index savings against protected PRE-MAIN.

| Input | Immutable identity |
| --- | --- |
| Private repository | `maidiu/rawlsing` |
| Protected `integration/pre-main-reconciliation-r1` | `ba165a6a073dfdac0cb2e993ab8111ebb5ef404c` |
| E1 implementation | `4bd17accf0104ac05167c40a43076606e13c8448` |
| E1 frozen fixture and profile | `cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8` |
| E2 independent review and probe | `59eceb6917f2bb8fb0038bf7a036a0cdedac5069` |
| E3 repair | `43d2b70ebae4d183aadbd9694624575857fd100f` |
| E3 terminal return and E4 branch parent | `3de9db3f0632c23c3a5817d0526c2f42caf5ebd1` |
| P41 runtime | `f27d1101048638bba395143a48efb7ef00bfcda4` |
| E1 synthetic SAV | 12 rows, 911 bytes, SHA-256 `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b` |

Local S2 runner `mainMac.lan`, x86_64 Darwin 22.3.0, macOS 13.2.1 build 22D68, Python 3.11.3. Detached baseline, E1 and E3 worktrees used a separate repository under `/private/tmp/rawlsing-oct28-e4.idwtRm` with the canonical object store as a read-only alternate. The initial authenticated SSH readback found the protected and E3 heads at their pins and the E4 branch absent. Substantive review ran in separate GPT-6.1 Sol High session `01a1a8ff-3b8e-7c01-8c74-caf307a8e237`, independent of E1, E2, the E3 code author and the E3 evidence author. [Provenance](PROVENANCE.log) · [Initial remote refs](remote-before.log)

## Hostile court

| Original E2 injection | Before | Warm poisoned read | After explicit deletion |
| --- | --- | --- | --- |
| E1 typed state | SUPPORTED | SUPPORTED | SUPPORTED |
| E1 raw denominator and resolved support | 3 / 3 | 2 / 2 | 3 / 3 |
| E1 exact fact hash | `7dc14856de18670198b20039d90c94cc93cab19d1029128dfec41447b6ce2690` | `496db04ff0167f35ae59a8d5abbaac7605f36bfd607a6567242888ed642634ea` | `7dc14856de18670198b20039d90c94cc93cab19d1029128dfec41447b6ce2690` |
| E3 typed state and support | SUPPORTED, 3 / 3 | SUPPORTED, 3 / 3 | SUPPORTED, 3 / 3 |
| E3 exact fact hash | Original | Original | Original |

The original E2 probe removed R1 from a read-only respondent map while retaining the exact release and universe. E3 restored the full fact body, reference and replay reference before any explicit deletion. [E1 full facts](e1-e2-facts.json) · [E3 full facts](e3-e2-facts.json)

A separate injection tested same-key respondent replacement, in-place truncation of a two-event repeated occurrence and routing map replacement under a different risk set. Each rebuilt and replayed exactly. The two legitimate risk queries had denominators 12 and 2 and distinct member sets. A test-only change to the check that admitted the truncated occurrence produced `INTEGRITY_FAILURE` instead of the exact supported result. Restoring the check rebuilt the original occurrence and fact. The probe also rejected a false exact release hash and a foreign query universe, recovered from foreign release and universe objects placed in the warmed slot, enforced revoked and changed exact authority, and preserved both observed zero in a supported denominator and `ZERO_SUPPORT`. [Probe](probe_cache.py) · [Exact outputs](e4-cache.json)

## Active caller, provenance and lifetime

On all three cuts `CarrierNeutralResearchExecutor.execute_i03` resolves the exact query and predicate and calls the imported owning `pre553_empirical_query.execute_empirical_query`. Its semantic identity, public authority, exact I03 fitness and target plan checks precede lookup. Exact sealed release and universe resolution encloses cache lookup, and evaluation still checks current routing, risk, predicate, weight and authority determinants. The runtime binding is attached to evaluation-local copies of the index. [Actual imports](imports.log)

In E3, `pre553_empirical_query.py` lines 70–122 compare the warmed index object and every dataclass field by identity against separately retained originals under the repository lock. The builder creates read-only maps from private dictionaries and tuple values from sealed C11 records. A copied slot with the same release and universe fails the object check, and in-place replacement of a field fails the separate field check. Reconstruction uses the sealed release. The append-only repository owns the cache and the attestations and retains them for its lifetime. Runtime authority and query decisions have their existing per-call checks. The fault model covers cache-slot substitution or top-level field replacement before lookup, with sealed C11 and the separate originals intact. Concurrent or coordinated arbitrary memory tampering falls outside this model.

The production repair from E1 to E3 changes only `pre553_c11_repository.py` and `pre553_empirical_query.py`, plus the focused test file. The baseline-to-E3 increment also includes E1's existing topology extraction and immutable index construction changes. The E3 terminal commit and this review add evidence only. No persistent cache, authority decision, carrier format, checkpoint schema or protected ref is part of the change.

## Native parity and regression

The joined runs exercised synthetic physical decoding, Route B I02/C11, native I03/I05 and Batch, partial R04 checkpoint capture and restoration, R05, and the actual pinned P41 reader. Independently captured canonical byte streams matched across PRE-MAIN, E1 and E3. The capture includes complete source and occurrence objects, I03 queries, predicates, every fact body and ref, I05 receipts, projection and route replay, and P41 consumer values. It contains 53,463,055 bytes with SHA-256 `8048dee503f5d42079bae0b4cd43e944b4de60114b3efdd19b7929e70077254b`. The checkpoint matched byte for byte at 28,017 bytes with SHA-256 `bbc9a626f1045a22e3f4b0f95b44ef62bc434dd593c55cfd818986978d850f9c`. [Canonical native material](native.json.gz) · [Exact checkpoint](checkpoint-0.json)

Changing the checkpoint source digest and recomputing its internal hashes produced `JOINED_CHECKPOINT_PIN_MISMATCH` against the original external pin. Restoring the original bytes resumed to view `c6aaef3c9816cdd63601703f4de52adf58d86ef0382adccb7cb6764f53812cf5`. Revoked issuance and wrong source refused with `WorkloadAdmissionError`. A substituted R05 upstream evidence binding refused with `R05_N10E_EVIDENCE_BINDING_MISMATCH`, and restoring the binding reproduced the view. [Capture and determinant falsifier](capture_native.py)

The related suite passed on protected PRE-MAIN (200), E1 (201) and E3 (209), each with one installed Stata extended-missing capability skip. The separate fresh-process P41 test passed on all three cuts. The initial baseline suite attempt exposed two omitted tracked documentary files in the sparse checkout. The final runs materialized those exact blobs from each cut and reran the complete suite. [PRE-MAIN log](base-final-suite.log) · [E1 log](e1-final-suite.log) · [E3 log](e3-final-suite.log)

## Same-host paired performance

The comparison used fresh processes in baseline/E3/E3/baseline order, with ordinary filesystem cache behavior and no concurrent review workloads during timing. Joined wall excludes P41 runtime extraction. Peak RSS covers the entire process. Both process orders ran the same synthetic input, instrumentation and complete semantic workload.

| Observation | Protected PRE-MAIN | E3 |
| --- | ---: | ---: |
| Joined wall, forward pair | 26.345 s | 24.621 s |
| Joined wall, reverse pair | 26.072 s | 24.484 s |
| Index builds per joined run | 1,328 | 6 |
| Index build time across the two runs | 1,467–1,522 ms | 6.35–6.65 ms |
| Native fact construction across the two runs | 2,511–2,540 ms | 2,474–2,492 ms |
| Native replay materialization across the two runs | 288–295 ms | 281 ms |
| Peak RSS, forward pair | 247,623,680 B | 251,654,144 B |
| Peak RSS, reverse pair | 247,836,672 B | 253,235,200 B |

Joined wall fell 6.54% and 6.09%. The sample comprises two pairs on this host and fixture. The roughly 1.46–1.52 seconds of eliminated index-build time is the main measured gain. Peak RSS rose 4.03 MB and 5.40 MB on these pairs. In the seven query scenarios, one round built 13 baseline indexes and 8 on E1/E3. At eight rounds the count was 104 versus 8, and E3's summed wall was 0.420 s versus 0.474 s baseline. Complete fact and replay envelopes matched across cuts and round counts.

In the uninstrumented E1/E3 warm comparison, summed case wall was 6.666/6.636 s forward and 6.858/6.901 s in reverse. The E3 delta changed sign, from −0.46% to +0.61%. The paired runs did not resolve a consistent warm wall penalty. Separately, 1,950 attestation checks averaged 4.47 μs each and eight creations averaged 3.82 μs each, including probe overhead. These values characterize the bounded workload. [Measurements and phase data](MEASUREMENTS.json.gz) · [Raw timing outputs](timing-raw.tar.gz)

## Receiving boundary

- `W05/P03` engineering passes for the repository-local I03 topology and the tested corruption model. `P04/P10` sourcefree output parity and the bounded performance claim pass.
- The qualified current PRE-MAIN importer must re-resolve the protected head and authority, verify this E4 commit and its E3 parent and production delta, and carry the required E1 implementation with the E3 repair as one scoped receiving increment. The importer must exercise the active receiving caller, rerun the relevant hostile and native replay checks against the actual protected cut, and obtain the incumbent owner's protected CAS decision before integration.
- Compact or lazy C11 realization, the compatible grouped calculator, and persistent Parquet/Zstd cross-session acceleration remain open. Original35, native S3, FF/N9/N11, Sorok, scientific issuance and all other PROGRAMMA and protected receiving holds continue. The verdict covers sourcefree engineering and semantic parity at the observed scope.

## Reproduce

Use the three detached worktrees and review parent above. Extract `profile_oct28.py` and `same-source.sav` from the E1 frozen return into `inputs/e1`, the original `probe_same_identity_cache.py` from E2 into `inputs/e2`, and `related-suite-command.sh` and `profile_attestation.py` from the E3 terminal return into `inputs/e3`. The input blob paths and checksums are in the provenance log. Use a writable `evidence` directory and the actual pinned P41 runtime object in the independent Git store.

```sh
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
bash "$packet/run_comparisons.sh" "$root"
for cut in base e1 e3; do
    bash "$packet/run_suites.sh" "$root" "$cut"
done
for cut in e1 e3; do
    (cd "$root/$cut" && python3 "$packet/read_e2_facts.py" "$root/inputs/e2/probe_same_identity_cache.py" "$cut")
done
bash "$packet/run_hostile_and_native.sh" "$root"
```
