# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03 — LARGE THREE-TRUNK INTEGRATION JOIN — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq162-c1-03-large-join-r1`

Exact commission tip:
`PENDING_THIS_COMMIT`

## Governing accepted inputs

### C1-03A — adopted
Accepted branch:
`integration/pyat-hq162-c1-03a-source-free-accepted-r1 @ 26976201b3cf14f4cf89a45a909c780591f54bcb`

Accepted implementation:
`4f5555459e5ffdb240fc9e6e94178ec5e4b3eff1`

Critical accepted production blob:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- blob `3a5e3db8a0897900d0b2606813bda7c3f586d46e`

### AT17 / N10E — adopted
Accepted branch:
`integration/pyat-hq147-n10e-at17-source-free-accepted-r1 @ 52e41a41e8bc3b77390016a049095b5aea1721d0`

Critical accepted production blob:
- `rawlsing_next/pre553_empirical_possibility_provider.py`
- blob `23167aa25291fb148b1e3cf210ac33fe7769b783`

Accepted provider court:
- analytical composition: 13
- empirical query: 32
- positioned-subject consumer: 13
- empirical possibility provider: 30
- total: 88

### C1-03R — adopted
Accepted branch:
`integration/pyat-hq159-c1-03r-source-free-accepted-r1 @ 9ec7eaff2646c1effd5192002967407a5c66bbef`

Accepted implementation:
`c690bb0b1e6f071c9a640a6825769b96f30dd79a`

Critical accepted production blobs:
- `rawlsing_next/pre553_authority_maintenance.py`
  blob `547e6bf20354f38179a0e2600de64c7cb2260ea0`
- `rawlsing_next/pre553_analytical_replay_dependency.py`
  blob `47e65aad5e0a8df7af6fda72fc8807a002e556ce`

Accepted R court:
- analytical replay dependency: 43
- authority maintenance: 57
- replay audit: 54
- analytical composition: 13
- total: 167

## Lineage facts already established by HQ

- A and R diverge from accepted C1-02:
  `bc661188b51e995d9f5d74e55c4e37d2ba358a17`
- AT17/N10E diverges earlier from accepted C1-01:
  `5fafb499d53dddadaf8a7b4fd46506e91a09d270`
- A and R production terrains are complementary.
- AT17 provider terrain is also complementary.
- This is a real three-trunk integration, not a linear continuation.

## Mission

Construct one lawful C1-03 source-free integration tree in which:

- adopted C1-03A AT14–AT16 behavior,
- adopted AT17/N10E provider behavior,
- adopted C1-03R AT18–AT19 lifecycle/replay behavior

all coexist and are exercised together.

This is a **large integration commission**. Do not decompose it into branch-by-branch subreturns. Perform the lineage integration, add the necessary integration-specific courts, run the full union court, and return one integrated result.

A PASS here is still not adoption. Independent review follows.

---

# PHASE 0 — exact lineage lock

Before editing:

1. resolve all three accepted branch tips exactly;
2. verify the accepted implementation SHAs above are reachable from the accepted tips;
3. verify the critical production blobs above;
4. record merge bases;
5. record whether any accepted production file is modified on more than one accepted trunk.

Expected:
- no semantic production overlap among the A state/route owner, AT17 provider, and R lifecycle/replay owners;
- ordinary historical overlap in common baseline files is not a conflict.

If the remote tips or critical blobs differ, stop with:
`INTEGRATION_PROVENANCE_DRIFT__HQ_ADJUDICATION_REQUIRED`.

---

# PHASE 1 — build one accepted-trunk integration tree

Starting from the issued join branch, integrate the exact accepted AT17 and R branches into the adopted A branch.

Prefer ancestry-preserving merges of the exact accepted tips. Do not manually reconstruct accepted implementations from snippets.

The resulting tree must contain all three accepted implementation lines.

## Critical blob conservation

After integration, these four production files must remain byte-identical to their accepted blobs:

1. `pre553_analytical_state_and_route.py`
   -> `3a5e3db8a0897900d0b2606813bda7c3f586d46e`

2. `pre553_empirical_possibility_provider.py`
   -> `23167aa25291fb148b1e3cf210ac33fe7769b783`

3. `pre553_authority_maintenance.py`
   -> `547e6bf20354f38179a0e2600de64c7cb2260ea0`

4. `pre553_analytical_replay_dependency.py`
   -> `47e65aad5e0a8df7af6fda72fc8807a002e556ce`

Do not edit any of those accepted owner modules merely to make the join easier.

If one must change for lawful coexistence, do not silently patch it. Return:
`ACCEPTED_OWNER_INTEGRATION_CONFLICT__HQ_ADJUDICATION_REQUIRED`
with the exact conflict and smallest required owner question.

Acceptance/adoption documentary files may coexist. Do not let documentary merge conflicts drive source semantics.

---

# PHASE 2 — integration census and exact contract crosswalk

Produce one machine-readable crosswalk of the three accepted trunks.

For each accepted surface record:
- public entry point;
- exact input identity;
- exact output identity/ref/hash;
- authority owner;
- determinant refs;
- replay identity;
- negative/refusal states;
- consumer behavior;
- lifecycle/currentness behavior where applicable.

At minimum include:

### A
- `capture_empirical_integrity_refusal`
- `OwnerStateProjection`
- `build_state_route_result`
- AT15 learned/adjudicated route
- AT16 direct positive consumer route

### AT17
- `provide_empirical_possibility_slice`
- provider receipt/result
- generated `PossibilitySliceEvidence`
- positioned-subject consumer result
- determinant identity and replay path

### R
- `SemanticDeterminantGraph`
- `AuthorityMaintenanceExecutor`
- invalidation receipt
- current/noncurrent/not-governed lifecycle status
- replay/checkpoint path
- current-product resolver

The crosswalk must identify which identities are already lawful bridge points and which are merely adjacent.

Do not invent a bridge just to make the diagram prettier.

---

# PHASE 3 — positive-path coexistence

Use real accepted source-free fixtures and real public entry points.

Prove in one integrated tree that:

1. AT17's `provide_empirical_possibility_slice` still drives:
   empirical query -> accepted analytical composition -> generated evidence -> actual positioned-subject consumer.

2. A's AT16 positive path still drives:
   empirical query -> analytical composition -> actual positioned-subject consumer.

3. Where the A AT16 and AT17 paths overlap on the accepted 54/6 source-free grain, prove the shared underlying identities are coherent:
   - same intended source universe/release scope;
   - same producer fact when the same exact producer determinants are supplied;
   - generated evidence descends from that producer fact;
   - consumer query/model binding remains exact;
   - consumer result remains `EXACT_SUPPORTED`.

Do NOT require wrapper/receipt hashes from different owners to be equal merely because they wrap the same underlying event. Distinguish shared determinants from owner-specific identity.

4. Prove AT17 still rejects handwritten/precomputed slice geometry.

---

# PHASE 4 — negative-state and refusal coexistence

Run the accepted A negative-state machinery in the merged tree and prove all mandatory states remain distinct.

At minimum:
- observed zero;
- valid empty;
- underpowered;
- unresolved/unknown;
- unvisited;
- noncomparable;
- blocked required authority;
- integrity failure.

Prove:
- no A state is collapsed into an R lifecycle state;
- `EXPLICIT_NONCURRENT` is lifecycle status, not a synonym for A's empirical/analytical negative states;
- `NOT_GOVERNED` is lifecycle status, not `UNRESOLVED`, `VALID_EMPTY`, or `INTEGRITY_FAILURE`;
- AT17 typed refusal produces no geometry and is not silently mapped to a supported A route;
- A negative consumer non-invocation remains explicit.

Include hostile assertions against accidental string/state-name coercion across owners.

---

# PHASE 5 — real accepted identities under lifecycle control

This is the central join proof.

Use **real exact refs exposed by accepted A and AT17 outputs** wherever those contracts expose a governed exact ref.

Register real accepted output/receipt/dependent refs in the R determinant graph.

Do not fabricate a fake ExactRef merely to satisfy the lifecycle API.

At minimum prove a mixed set containing real accepted C1 artifacts can be classified under the R owner as:

- one affected dependent receiving a lawful replacement;
- one affected dependent receiving the generic explicit noncurrent outcome;
- one unaffected dependent remaining identity-stable CURRENT.

The changed determinants must be actual accepted determinant refs from the source-free A/AT17 paths.

Required distinctions:
- replacement is not noncurrent;
- explicit noncurrent is not an A negative analytical state;
- unaffected CURRENT retains exact identity;
- zero-release known dependent remains `NOT_GOVERNED / NO_GOVERNING_RELEASE`;
- unknown dependent remains `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT`.

If an accepted A/AT17 object has no lawful exact ref that can participate in the R graph, do not manufacture one. Use the nearest accepted receipt/ref only if its contract actually makes it the dependent identity. Otherwise return a typed integration gap naming the missing owner surface.

---

# PHASE 6 — mutation, reidentity and rollback across the joined tree

Use an exact determinant mutation that is already lawful under the accepted source-free contracts.

Prove:

1. all and only graph-declared dependents are affected;
2. unaffected accepted artifacts remain usable;
3. replacement refs are the actual sealed/released successors, not old refs or decoys;
4. explicit noncurrent dependents cannot be served as current;
5. rollback obeys the same A/U and R/N laws as promotion;
6. the accepted AT17 determinant-reidentity proof still holds in the joined tree;
7. A's route/consumer identities do not silently survive a determinant mutation that their own accepted identity preimage says should reidentify.

Do not infer a new causal or semantic relation merely because two objects coexist in the graph.

---

# PHASE 7 — replay and fresh-process integration

Preserve the accepted distinction among:
- serialization replay;
- explanatory replay;
- fresh empirical recomputation.

Run the existing accepted R fresh-process/replay courts and AT17 fresh-process provider replay in the merged tree.

In addition, add one join-specific fresh-process court that starts only from retained accepted determinants/receipts/checkpoint material and demonstrates as much of the combined path as the existing contracts lawfully permit.

Preferred joined proof:
- restore lifecycle/checkpoint material;
- resolve a CURRENT accepted provider/analytical dependent;
- replay/recompute the accepted producer/provider path from retained determinants;
- reach the named positioned-subject consumer again;
- compare exact governed identities at each owner boundary.

If the contracts do not expose a lawful single fresh-process bridge, do not fabricate one. Return the exact missing bridge as a typed integration finding while still executing both accepted fresh-process paths in the same merged tree.

---

# PHASE 8 — union court + join-specific court

Run the unique union of all accepted suites.

## Unique accepted baseline

A's ten suites = 229.

R contributes three additional unique suites:
- analytical replay dependency = 43
- authority maintenance = 57
- replay audit = 54

AT17 contributes one additional unique suite:
- empirical possibility provider = 30

Therefore the expected unique pre-join baseline is:

`229 + 43 + 57 + 54 + 30 = 413`

across these 14 unique test files:

1. `test_pre553_analytical_state_and_route.py`
2. `test_pre553_analytical_composition_higher_order.py`
3. `test_pre553_empirical_query.py`
4. `test_pre553_structural_admission.py`
5. `test_pre553_discovery_exact.py`
6. `test_pre553_analytical_composition.py`
7. `test_source_backed_positioned_subject_possibility.py`
8. `test_pre553_discovery_adaptive.py`
9. `test_pre553_discovery_adaptive_admission.py`
10. `test_pre553_recursive_handoff.py`
11. `test_pre553_analytical_replay_dependency.py`
12. `test_pre553_authority_maintenance.py`
13. `test_pre553_replay_audit.py`
14. `test_pre553_empirical_possibility_provider.py`

Before adding join-specific tests, reconcile whether the merged tree still collects exactly 413 across these files.

If not, explain every delta. Do not wave away collection changes.

## Join-specific tests

Add a substantial dedicated integration court, preferably:

`rawlsing_next/tests/test_pre553_c1_03_join.py`

and, if needed:

`rawlsing_next/tests/c1_03_join_fixture.py`
`rawlsing_next/tests/c1_03_join_fresh_process_runner.py`

The new court must cover PHASES 3–7.

A final PASS must run:
- all 14 accepted unique suites;
- all new join-specific tests;
- any new fresh-process runner.

No "targeted only" final proof.

---

# PHASE 9 — no semantic smuggling

The join may add minimal non-authoritative orchestration glue only if existing public APIs genuinely need one place to coordinate them.

Allowed new production file only if necessary:
`rawlsing_next/pre553_c1_03_join.py`

Any such module:
- may orchestrate existing accepted owners;
- may carry exact refs/receipts;
- may not invent new semantic authority;
- may not translate one owner's negative vocabulary into another's;
- may not manufacture currentness;
- may not synthesize provider geometry;
- may not create actor/person state;
- may not introduce C4/C7/raw-source behavior.

If no production glue is necessary, prefer test/fixture integration only.

---

# PHASE 10 — return package

Write:
`WORKER_RETURNS/PYAT-C1-03-LARGE-JOIN-R1/**`

Required:

- `00_RETURN.md`
- `01_LINEAGE_AND_BLOB_CONSERVATION.json`
- `02_THREE_TRUNK_CONTRACT_CROSSWALK.json`
- `03_POSITIVE_AND_NEGATIVE_COEXISTENCE.json`
- `04_LIFECYCLE_INTEGRATION_RECEIPT.json`
- `05_REPLAY_AND_FRESH_PROCESS_JOIN_RECEIPT.json`
- `06_HOSTILE_MATRIX.json`
- `07_EXECUTION_RECEIPT.json`
- `08_FINAL_DISPOSITION.json`

The execution receipt must include:
- exact final SHA tested;
- clean-tree status;
- exact interpreter/pytest;
- exact command;
- per-file counts for all 14 accepted suites;
- join-specific test counts;
- total counts;
- fresh-process commands and exit status.

## Allowed dispositions

- `PASS_C1_03_LARGE_JOIN__INDEPENDENT_REVIEW_REQUIRED`
- `INTEGRATION_CONTRACT_GAP__HQ_ADJUDICATION_REQUIRED`
- `ACCEPTED_OWNER_INTEGRATION_CONFLICT__HQ_ADJUDICATION_REQUIRED`
- `INTEGRATION_PROVENANCE_DRIFT__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No self-adoption.
No merge to control.
No C1-R.
No raw sources.
No C4/C7.
No V3 actor/person implementation.

Terminal:
`C1_03_LARGE_JOIN_RETURNED__HQ_ADJUDICATION_REQUIRED`
