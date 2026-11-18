# CUT2 R2 — FIRST BOUNDED HIGH-WIDTH PAIR

**Verdict:** `MEASURED_FIRST_BOUNDED_HIGHWIDTH_PAIR`  
**Grade:** sourcefree TEST_ONLY geometry/mechanics. Not native/original35/100k/science/actoreconomics.  
**Product candidate:** `347baec696c8b395d750ac3b9e74417a6490c223`  
**Executable code/test:** `a13d69cf5636de5541660cd60115f8b61d66261b`  
**Cut1 G5:** `ACCEPT_SCOPED_PREPARED_SAVED_BATCH_CUT1` at review `092bf29ffa6724d477abb4ccfc770e3bc492250d`  
**Harness SHA-256:** `4fbbd48fd49d330efac0aeb8c41e2f08011cd00f550557a8377430a32b3491c6`  
**Width generator SHA-256:** `8d9efbb779a1596530c89226b37b4950be6b80e067f2e2425ec78029de5334f1`  
**Fixture contract SHA-256:** `e928ebd17016c005efd1c8fee19a19b27e35fb360c6b8f85dd489cc9371b8f28`  
**Machine result SHA-256:** `9def4b08cfd9e937c42625d5d07d5a80e375fe4b425a814d225c7f8cc56f5f42`

## 1. One paired comparison only

Three fresh producer/consumer processes, each product-exited:

1. producer `prepare`: build the exact 16R/600Q estate once, outside the timed query pair, then exit;
2. fresh `baseline`: plain `SavedC11Admission`, five operations, then exit;
3. fresh `prepared`: one `PreparedI03Session`, the same five operations, one fixed revocation/restore check, then exit.

No fresh Batch, no 1/10/100, no repeated matrix, no automatic worker, no product edit.

Exact commands are in `FIRST_PAIR_RESULT.json` under `commands`; raw supervision samples and exits are in `samples_build.json`, `samples_baseline.json`, `samples_prepared.json`.

## 2. Geometry actually built and audited

| Field | Actual |
|---|---:|
| Respondents | 16 |
| Native question bindings | 600 |
| Added question slots | 595 |
| Added response cells | 9,520 |
| Added valid substantive | 7,616 (80%) |
| Added typed MISSING | 952 (10%) |
| Added typed NOT_ASKED/routing | 952 (10%) |
| Added events | 8,568 |
| Base events | 54 |
| Total RespondentEvent | 8,622 |
| Total RoutingEligibilityFact | 9,600 |
| WeightMeasureFact | 16 |
| AuthoritySnapshot | 6 |
| QuestionVariableBinding | 600 |
| Events/respondent min / mean / max | 538 / 538.875 / 542 |
| Base repeated MR occurrences | 4 |
| Retained estate | 7,099,520 B |
| Estate manifest SHA-256 | `c209d3a198b25e5392dd422878fcc9111ada5c72aeb146d5d2a07388586bbc8b` |

The added 595 slots are a deterministic `(respondent*595 + q_index) % 10` pattern: 0–7 valid, 8 typed MISSING, 9 typed NOT_ASKED. This is a controlled sourcefree geometry population, **not** original eligible QUERY issuance, and 600 columns are **not** treated as 600 events/respondent.

The five query operations target the accepted base A/B/C/MR roles, not all 600 added items. The added width loads the actual writer, cold admission, index build and selected reads; it does not add a scientific query catalog or issuer.

## 3. Cost / phase boundaries

| Phase | Wall s | CPU user+sys s | H s | S s | Q s (timed ops) | O s | RSS peak sampled | Retained B | Scratch peak B | Output B | Row reads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| producer build | 33.18 | not instrumented | — | — | — | — | 193,429,504 | — | 99,941,972 | — | — |
| fresh baseline | 80.62 | 78.11 + 5.08 | 0.273 | 14.378 | 65.404 | 0.019 | 185,323,520 | 7,099,520 | 23,269,376 | 166,175 | 20,101 |
| fresh prepared | 78.05 | 78.32 + 2.60 | 0.287 | 5.498 | 60.176 | 0.017 | 200,810,496 | 7,099,520 | 23,269,376 | 166,175 | 23,898 |

- **H** = admission/member validation, including exact manifest/member hashes.
- **S** = existing `DirectEstateI03Session._build`; prepared total has 2 index builds (one timed context + one negative/restore), `index_builds_measured_operations = 1`; baseline has 5 timed builds.
- **Q** = existing native evaluator, including fact construction/hash.
- **O** = separate export serialization of full fact/semantic/identity/replay/refs/member payload; **not** added to Q.

The one pair is not a speedup claim: baseline Q 65.404 s vs prepared Q 60.176 s; baseline wall 80.62 s vs prepared 78.05 s; prepared RSS is slightly higher (200.8 vs 185.3 MB). The structural difference is index-build reuse (5 vs 1 measured builds).

## 4. Full payload correction and parity

The old 82d14 smoke measured `canonical_json(result.facts)`. `pre553_empirical_objects.canonicalize` returns `CanonicalSemanticObject.ref.as_dict()` for a semantic object, so that old 1,885-byte number was **refs only**, not full fact/risk/denominator payload. R2 fixes the measurement, not the product:
- full `f.semantic_projection()` and `f.as_dict()` are serialized separately;
- exact fact refs, replay refs, `risk_set_member_refs`, `denominator_member_refs`, provenance refs and wrapper ABI bytes are measured;
- the old ref-only path is kept as an explicit witness.

For the first selected operation: ref-only 234 B vs full semantic 35,256 B vs identity 35,458 B; risk member refs 16, denominator member refs 8, provenance refs 51. Across five operations: full semantic 148,727 B vs ref-only 1,170 B; serialized output components 166,175 B.

Parity exact for all five operations on:
`identity_sha256`, `semantic_sha256`, `refs_sha256`, `member_refs_sha256`, `replay_sha256`.

Wrapper ABI: binding receipt 6,923 B for both; prepared receipt 550 B.

Revocation/restoration: revoked CURRENT refused with `DirectEstateError: current source/operation authority refused`; restored identity SHA `435262ba...` exactly equals the baseline selected identity. Negative/restore is separate from the timed five operations and records 1 index build / 1 evaluator call / ~14.8 s.

## 5. Abort/supervision and limitations

- Build cap 300 s; each query mode 180 s; combined physical run cap 720 s; process-tree RSS cap 2 GiB; scratch cap 2 GiB.
- External child supervision: 0.25 s `ps` process-tree/RSS/scratch sampling, child process group SIGTERM/SIGKILL on timeout/limit; no admin service/global kill.
- Observed: build 33.18 s / 193 MB / 100 MB; baseline 80.62 s / 185 MB; prepared 78.05 s / 201 MB; combined 194.6 s; no abort.
- Process-tree peak is sampled max plus child `ru_maxrss`, not continuous; OS file cache is uncontrolled. One fresh read is legitimate but is not a warm-cache claim.
- No native/original35/source/science/actor/100k/6 GiB/economic acceptance.

## 6. Choice-changing next decision

The pair is exact and within fixed caps. The evidence selects a **qualification decision**, not a predetermined speedup:

1. qualify the measured H/S/Q/O and retained/scratch/RSS shape;
2. because Q dominates and S reuse saves only ~8.9 s while prepared RSS is higher, choose the next repair from measured evidence: evaluator/read-path cost, index geometry/durability, or Batch-forward wiring;
3. do not run 1/10/100 or fresh Batch until that choice is recorded; do not infer native/100k economics from this sourcefree pair.
