# A04 — Typed issuer and production holds

Every hold below is **conserved and visible**, and none of it is executable work.
These are the exact states that must NOT be silently converted into jobs.

## 1. Holds declared and conserved in the measured run

Four non-runnable obligations are declared in the frozen universe, exported in
`BoundWorkload.held_frontier`, and proven never to appear as a constructed job.

| Item | State | Exact reason | Runnable |
|---|---|---|---|
| `O` (ordered sequence) | `HELD` | `ORDERED_SEQUENCE_COLLAPSE_NOT_YET_AUTHORIZED` | false |
| `R` (repeated event) | `HELD` | `REPEATED_EVENT_JOIN_NOT_YET_AUTHORIZED` | false |
| `V` | `DENIED` | `EXPLICIT_FAIL_CLOSED_SOURCE_GAP` | false |
| `U` | `SOURCE_NONAPPLICABLE` | `NO_COADMINISTERED_TARGET_IN_THIS_SLICE` | false |

Structural guarantees, each with a passing test:

- a non-RUNNABLE declaration **cannot carry executable owner refs** (`__post_init__` refuses);
- a HELD/DENIED/NA obligation **must carry** an exact reason (refused otherwise);
- removing the held export entirely is caught → `HELD_OR_DENIED_WORK_NOT_VISIBLE` (H13);
- a held obligation appearing as a job is caught → `HELD_OR_DENIED_WORK_EXECUTED`.

## 2. Issuer holds — the binder is NOT an issuer

| Hold | Status |
|---|---|
| Original-source read grant | **NOT HELD BY THIS WORK.** Never exercised; no SAV/DTA read. |
| Source-scoped expected-operation issuer | **ABSENT.** Declarations are caller INPUT; the binder creates none. |
| All-35 scientific eligibility | **NOT CLAIMED.** Out of scope; WGA 78,037 / WGD 81,179 are not workloads. |
| New model permission | **NOT CLAIMED.** |
| G0b / EE12 / operative publication | **NOT HELD, NOT EXERCISED.** |
| Competent adoption of this candidate | **NOT GRANTED.** HQ adjudicates. |

**Real issuer contract:** none was found in the accepted codebase for issuing
source-scoped expected-work frontiers. Consequently the binder's
source-free fixture competence **remains development-only**, exactly as the
commission requires. An unissued candidate row is refused: authority must
already exist in the issued `RuntimeObjectCatalog` (H16).

## 3. Production holds

| Hold | State |
|---|---|
| Canonical / semantic PRE-MAIN | **unmutated** — `1f47063c3205a45888b3c55e81e7485943ed1390` |
| Accepted production owners | **unmodified** — `git diff HEAD` empty; route_b blob `2385cd32…` == E18, discovery_exact blob `905f24d1…` == E19 |
| Branch | worker branch only; **no self-adoption, no merge** |
| Respondent lineage export | not performed, not required, not present |
| Consumer receipts in the positive run | modelled from **real produced `EmpiricalFact`/`DiscoveryResultReceipt` refs**; downstream *consumption* itself remains B02's licensed act |

## 4. Measurement limits (stated, not hidden)

1. **Source-free synthetic fixture only.** Four respondents, three physical rows, items X/Y/O/R, reused from the accepted Route B test corpus. **No real source, no all-35 scope.**
2. **Repository-wide suite: INCONCLUSIVE.** A partial run showed failures, but the baseline worktree was not demonstrably comparable. **I do not claim those failures are pre-existing, nor that this change caused them.** Proven locally: 118 targeted tests pass across the six directly-relevant suites.
3. **Consumer closure is modelled, not exercised end-to-end.** `REQUIRED_CONSUMER_OMITTED` is genuinely detected (H12), but no real analytical/Field-Forge/learned consumer was invoked — that is B02, and requires an A-03 grant.
4. **`EXPECTED_SET_OUTPUT_DERIVED` is currently coarse.** It fires whenever the recomputed frozen frontier diverges from the bound frontier. A refined check — proving the *derivation path* rather than the *hash* — is left as future work and is recorded as a known limit, not a pass.
5. **Discovery authority multiplicity is fixed at exactly one** in this candidate (`bind_expected_work` refuses zero or several). That is a deliberate simplification at development scope, **not** a claim that a real slice needs only one discovery authority.
6. **Typed-negative coverage is partial.** `_classify_result` maps the owners' own state vocabularies one-way; unrecognized states surface as `OWNER_TYPED_<state>` and are **never** promoted to measured. The mapping is not yet an exhaustive census of every owner state.

## 5. What a competent owner must still do

Before any real slice runs through this binder: issue a real expected-work
frontier with competent authority; bind a real issuer contract; replace the
synthetic fixture with an authorized source; exercise the real consumers; and
resolve item 4 above (derivation-path proof) so laundering detection does not
rely on hash comparison alone.

**Terminal:** `HQ280_PV3_A04_REAL_CURRENT_OWNER_BINDER_CANDIDATE_MEASURED__SOURCEFREE_ONLY__GITHUB_PUSHED`.