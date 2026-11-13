# PYAT R3 S1-C — Independent G5 receiving

**Role:** independent nonauthor G5 receiver (`G5_INDEPENDENT_NONAUTHOR_RECEIVER`).
This receiver did not author any S1-C A/B round, the B2 repair, or the local runner
correction. Scope is the original #918 S1-C / P1-04 packet under #909 R3C/R3S and
adopted MCR-lite.

- **Verdict:** `ACCEPT_SCOPED@TEST_ONLY_SOURCEFREE`
- **Terminal freeze:** `S1C_TERMINAL_CLOSED@dae66cdf9f3846d237e0b1c3069cc17eb05b7746__SOURCEFREE`
- **Phase:** `CLOSURE_ONLY`
- **Integration:** `UNMERGED` (no protected merge, no source/science/original35 authority)
- **Review branch:** `agent/pyat918-s1c-g5-r1`
- **Return directory:** `WORKER_RETURNS/PYAT_R3_S1C_G5/`

## 0. Prior-G5 search

No genuinely independent G5 for this S1-C implementation was found. The Q2 S1-E
independent G5 receipt records S1-C `dae66cdf...` as a **distinct nonauthor G5 still
pending** and does not accept it. The Q2 provisional composition marks the same S1-C
blobs `PINNED_PROVISIONAL_READONLY_UPSTREAM_G5_PENDING`. The combined scoped-G5 branch
covers S1-B/S1-D/S2-F, not S1-C. Remote refs contain no S1-C G5 branch. See
`evidence/prior_g5_search.txt`; therefore this receiving is performed directly.

## 1. Exact artifact and ancestry (G1)

- Actual tested code/test commit: `dae66cdf9f3846d237e0b1c3069cc17eb05b7746`
- Agent A documentary HEAD / PR #975 head: `779fea665829aae641a3f3d6b463f456c78f8316`
- Local runner evidence head: `53adb6702b7e6c82652689df6a1a06f8698ac5c2`
- PR #975 remote head / merge: `779fea665...` / `644dd199104bb8fbbedb9f51e95184b71c48fe82`
- Census blob: `dd5bf3940083679612d73f98e6a7b7711c223fd5`
- Tests blob: `a19b0db5ea800af80aff86816e77e666f4acc72f`
- Runner blob: `63656522497dd6f7760872b692b46bf0e8b7580e`
- Workflow blob: `901e2e6ce54bf5fda7b016d39524aac32f2862a8`
- Protected PRE-MAIN reference `6a5c12f04323d74001f9632063ec907f4fc4468e` remains an
  ancestor; no merge or protected-path change occurred.

`779fea` adds only the Agent A handoff/receipt documents over `dae66cdf`; the runner
adds only `WORKER_RETURNS/PYAT_R3_S1C_RUNNER_A_COUNTER/`. Relative to the unmerged
#948 base `7064daa14d93109211629e72d08f3a6e705a0d57`, S1-C adds exactly four files:
the adapter, its test, the RSS runner and the workflow. Existing
`ScientificFrontier`, `compile_governed_frontier`, `execute_governed_frontier`, the
I05 issued reader, Batch/C11 builder, R61 enumerator/policy and shared owners are
untouched. The adapter imports and calls the existing owners; it adds no second
enumerator, issuer, parser, carrier, C11 engine, universal graph or persistence.

The qualified declared census was conserved: 309 source candidates / 309 scientific
fates / 309 frontier operations; `ELIGIBLE=150`, `HELD=159`; 150 candidate receipts
and 330 native facts; 3 unsupported-runtime rows; 6 deferred records; 3 inventory
ledger rows. UNKNOWN and EXCLUDED can be zero in the all-eligible/held fixture and
are nonzero in the independent negative-axis variant (279 UNKNOWN, 16
INAPPLICABLE_PROVED). The test census is an explicitly labelled sourcefree
test-double, not an original35 issuer; input completeness remains external.

## 2. Actual issued-reader path (G2)

Executed locally from a clean detached worktree at `dae66cdf`, with the existing
issued path `compile_governed_frontier -> execute_governed_frontier ->
execute_test_only_discovery_workload -> build_source_backed_c11_repository ->
CarrierNeutralResearchExecutor.execute_i05 -> BatchExecutionRunner`.

- Positive: 309 declared / 309 compiled / 309 receipt rows, 150 issued candidates,
  330 native facts, one source-factory call, one bounded C11 build; 147 operations
  carry receipts, the other 159 are `HELD` and 3 are `UNSUPPORTED_RUNTIME`, all with
  no receipts/facts. Candidate and operation anti-joins are green.
- Changed value: changing observed `A` response cells changed the actual fact
  identity of all 147 fact-bearing operations while counts stayed 150/330; the
  checkpoint changed and restored exactly.
- Changed eligible operation and restoration are covered by the focused suite and
  passed. No original35 source or scientific issuance was used.

## 3. Independent attacks on the two historical defects (G3)

**B2 false-HELD.** Co-forging an eligible valid SAMPLE/RAW operation to `HELD`,
rehashing the science census and adjusting the histograms leaves the source census
equal and makes the direct native R03 path lose two real receipts (150 -> 148) while
both native anti-joins remain green. The corrected adapter refuses with
`SOURCEFREE_ROLE_FATE_DRIFT` with **0 source-factory calls**. A reason-only forge on
a genuine HELD operation is refused identically. Exact restoration passed.

**Pending-budget overissuance.** Honest `budget=5` R61 frontier: `PARTIAL`, 145
pending IDs, execution counts `NOT_STARTED=164/PENDING=145`, exactly 5 receipts and
11 native facts, 0 pending receipts/facts. Removing only `pending_operation_ids`
leaves rows PENDING and source/science/UNKNOWN/EXCLUDED/inventory censuses equal;
direct native R03 then issues **150 receipts, +145 over budget**, with 142 of 145
pending IDs receiving receipts and both native anti-joins green. The corrected
adapter refuses with `PENDING_FATE_CENSUS_DRIFT` with **0 source-factory calls**.
False `COMPLETE` with 145 pending IDs refuses with `BUDGET_STATE_FATE_DRIFT`.
Independent variants (partial list loss, duplicate pending ID, unmarked PENDING row)
refuse before source. Restoration of checkpoint, frozen census, operation fates,
receipts and facts is exact. The native overissue is retained only as the historical
counterexample; the S1-C adapter is the guarded contract path.

**Other negative axes.** The genuine R61 risk-set negative variant conserves 279
UNKNOWN and 16 INAPPLICABLE_PROVED operations with zero receipts/facts; the disjoint
administration-form variant conserves 272 INAPPLICABLE_PROVED operations with no
receipts/facts; routing-UNKNOWN remains typed HELD with no administered positive.
Dropping the frozen UNKNOWN/EXCLUDED axes or tampering the frontier deferred records
refuses before source. A caller that co-forges both the frozen census and the
frontier can omit deferred records (and operations); this is the acknowledged
declared-input completeness boundary, not a bypass of the repaired pending/HELD
guards.

**Optional-weight RAW.** 150 eligible unweighted SAMPLE/RAW operations: 147 execute,
3 are typed `UNSUPPORTED_RUNTIME`; 147 population/weighted operations without
weight/design remain `HELD` with no receipts, and no operation was invented
eligible. This preserves valid optional-weight RAW without promoting weighted
science.

## 4. Independent local execution (G4)

Clean pinned worktree, detached at `dae66cdf`; macOS 13.7.8 x86_64, Python 3.11.3,
isolated venv (pytest 9.2.0, pandas 3.1.1, pyreadstat 1.3.7, pyarrow 26.0.1,
duckdb 2.0.0, psutil 7.2.2, numpy 2.4.6). Hosted CI was not claimed.

| Suite | Result |
|---|---|
| Focused S1-C + process-tree RSS wrapper | **18 passed** (152.00s) |
| Inherited R03/R61 + custody | **22 passed** (150.99s) |
| Combined S1-B | **46 passed** (222.32s) |
| Combined S1-D | **59 passed** (157.61s) |
| Combined S2-F | **19 passed** (20.79s) |
| Combined shared C11/universal/empirical | **58 passed** (137.17s) |

Combined total 182; grand total 222 passed, 0 failed, 0 skipped.
Focused run: inner elapsed `10.257499s`, wall `152.709s`, sampled process-tree peak
RSS `200,646,656 bytes` over 5,136 samples. Resource counts repeated exactly
(309/309/309, 150/159, 150 receipts, 330 facts, 6 deferred, 3 unsupported, 1 source
open, 1 bounded C11 build). Zero/unknown result counts in the 309 case:
`SUPPORTED=123`, `VALID_EMPTY=24`, `HELD=159`, `UNSUPPORTED=3`, `ZERO_SUPPORT=0`,
`UNKNOWN=0`, `DIFFUSE=0`. The 309/150/330 case is synthetic sourcefree evidence and
is **not** promoted to original35 execution.

## 5. Decision and holds (G5)

`ACCEPT_SCOPED@TEST_ONLY_SOURCEFREE` at
`dae66cdf9f3846d237e0b1c3069cc17eb05b7746`; frozen terminal
`S1C_TERMINAL_CLOSED@dae66cdf9f3846d237e0b1c3069cc17eb05b7746__SOURCEFREE`.

Preserved holds: original35 source/science/respondent entitlement; native-host
CURRENT permission; production S1-D issuer; protected merge; 100k/6GiB and original
N9/N10W claims; #980 combined receiving; upstream S2-B G5. No new authority or
optional hardening is granted. The admitted evidence is TEST_ONLY_SOURCEFREE only.

**STOP:** No further S1-C author contest, speculative hardening or duplicate G5
commission after this terminal receiving verdict. One bounded correction is not
requested; no material in-scope defect at the declared sourcefree grade was found.

## 6. Operational note

The available repository credential can push branches but lacks GitHub Issues
permission (REST returns 403 `Resource not accessible by personal access token`).
The exact notification text for #918, #909 and #960 is preserved in
`evidence/issue_notification.md`; it could not be posted by this receiver. The
durable branch return is the authoritative delivery.

Evidence: `WORKER_RETURNS/PYAT_R3_S1C_G5/evidence/` (refs, environment, command
logs, focused collection, independent attack and negative-axis probes, pip freeze).
