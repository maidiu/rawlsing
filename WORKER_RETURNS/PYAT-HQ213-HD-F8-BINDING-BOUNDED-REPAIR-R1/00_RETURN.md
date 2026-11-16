# HQ213 — H-D/F8 SOURCE-SCOPE BINDING BOUNDED REPAIR — RETURN

**LANE:** `PYAT-HQ213-HD-F8-BINDING-BOUNDED-REPAIR-R1`
**BRANCH:** `agent/rabochii-pyat-hq213-hd-f8-binding-repair-r1`
**STARTUP TIP (verified exact):** `a946d431f84dfe263c3508089b5c78422683fd03`
**EXACT REPAIR BASE:** `8d352f7d80983cbf49e7e57511f8cf6d5b80966d`
**HOSTILE REVIEW:** `33062ccfcca5c121bd699a98af11460440cd15ba`
**PUSHED SHA:** `17737c09194bffd7f8f2f7d135f79d5f8ebfa7fc`
**REMOTE VERIFIED EQUALS LOCAL:** yes
**DISPOSITION:** `HD_F8_BINDING_REPAIR_COMPLETE__READY_FOR_FINAL_HOSTILE_REREVIEW`

---

## 1. Plain answer to the commission

The two blocking defects are closed and the three low defects are closed. Nothing was
left unrepaired, nothing was widened, and no adopted owner was touched.

The review said `accept_for_hq_adoption = false` until Repairs 1 and 2 are made. Both
are made. This lane's own disposition is **COMPLETE / READY FOR REREVIEW**, which is
not acceptance: the commission requires an independent hostile rerereview, and that
rerereview has not happened.

## 2. The root cause was deeper than the review reported

The review described Repair 1 as "the requested source never has to be in the F8 rule
it is bound to" and "never uses it to constrain anything at evaluation time." Both are
correct, but the underlying reason is stronger and worth stating plainly:

**The constructed binding discarded `requested_source_universe_ref` entirely.** It was
recorded on the *binding request* — so it entered the request material — but the
`ServiceApplicabilityF8SourceScopeBinding` dataclass had no field to hold it. There was
nothing on the binding for evaluation to constrain against. Adding the field is what
makes the mode real; adding only a check in `assert_query_source_admitted` would have
had nothing to compare to.

The same investigation surfaced a residual gap in my own first pass, caught by the new
court rather than the existing one: after the enforcement was added, the binding
*material* still omitted the enforced requested source, so the refinement was enforced
at validation time but absent from the replay identity — meaning the replay verifier
could re-derive a binding enforcing a different source. That is now emitted in the
material, so the enforced refinement is part of the replay identity.

## 3. The five repairs

| Repair | Review finding | What changed | Witness |
|---|---|---|---|
| **1** | F1 blocking — single-source mode inert | Binding now carries `requested_source_universe_ref`. In single-source mode the query source must equal it (`F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE`). The requested source must be inside the bound rule's `source_universe_refs` (`REQUESTED_SOURCE_NOT_IN_F8_RULE_SOURCE_SCOPE`). Refinement is in the binding material, hence the replay identity. | A-bound/B-query refusal over a fixture where B is genuinely admitted |
| **2** | F2 blocking — "exactly two" false | Truthful enumeration: **six public callables, five of which return**. Two source-touching powers + constructor + delegating evaluator + replay verifier + a coverage guard that returns nothing. Delegating evaluator declared a non-power with the precise reason. | Exact exported-surface enumeration, pinned as literals |
| **3** | F3 low — dead fail-open release branch | `bound_to_requested_release: False` branch **removed and made fail closed** (`BINDING_OFF_RELEASE_POSITIVE_DECISION`). Owner's single-release invariant now pinned by test. | Forged-receipt witness that deliberately bypasses the owner |
| **4** | F4 low — four claim/evidence mismatches | Docstring count three→seven; "no third"→"no third power over sources"; AST scan widened from a chosen 8-name subset to the **complete pinned 57-name inventory**; currentness vocabulary closed against the adopted contract's own states; exact exported surface instead of `dir()`. | 11 witnesses, plus docstring checks |
| **5** | F5/G-3 low — silent guard skips | All **5** silent `pytest.skip` paths removed; guards now fail loudly with explicit NOT-CERTIFIED messaging. **0** remain. | Meta-guards that fail if a skip is reintroduced |

### Repair 1 ordering note

The new rule-scope check was initially inserted *before* the existing admission check,
which changed the refusal reason for a non-admitted requested source and broke a
pre-existing court test. The check was relocated to run after admission, keeping
`REQUESTED_SOURCE_NOT_ADMITTED` as the primary, more specific refusal. This is recorded
as a defect this lane introduced and caught.

### Repair 4 currentness vocabulary

Derived from the adopted contract's own `STATES`, not invented here:

- **accepted:** `CURRENT`
- **refused (adopted non-currency):** `STALE`, `REFRESH_REQUIRED`, `INVALID`
- **refused (legacy negatives):** `CONFLICTING`, `UNKNOWN`, `MISSING`, `UNRESOLVED`
- **new code:** `CURRENTNESS_RESULT_OUTSIDE_ADOPTED_VOCABULARY`

`FRESH`, `LOOKS_GOOD`, `ASSUMED_FINE`, `YES`, `OK`, `2026` now all refuse — the old
code accepted every one of them. `ACCEPTED_CURRENTNESS_RESULTS_ARE_ADOPTED` refuses at
import time if the pin ever drifts outside the adopted states, so the vocabulary cannot
silently diverge from its source. This binder still records a caller-supplied result
and never decides currency; `currentness_authority()` still refuses, a result without a
claim still refuses, and currentness is still never inferred from applicability.

## 4. Negative control — the court is genuine, not tautological

The review's own GAP-4 lesson is that re-running identical inputs proves nothing. So the
pre-repair binder was extracted from the exact repair base `8d352f7d` and swapped into
a shadow tree **outside the repository**, and the identical repair court was run
against it:

| Code under test | Result |
|---|---|
| Pre-repair binder | **19 failed**, 22 passed |
| Pre-repair binder + pre-repair binder court | Repair 5's witness fails as intended (5 skips exposed) |
| Repaired binder | **41 passed** |

Every one of the five repairs has at least one witness that **fails on the pre-repair
code and passes on the repaired code**. Nothing here is satisfied by re-running
identical inputs.

## 5. Courts and regression

**Commissioned + repair courts: 190 collected, 190 passed, 0 failed, 0 skipped.**

Deterministic across `PYTHONHASHSEED` 0, 0, and 12345.

| Court | Role | Result |
|---|---|---|
| `…service_f8_source_scope_binding_court.py` | existing binding court, extended | 74 passed |
| `…service_f8_source_scope_binding_repair_court.py` | **new** hostile repair court | 41 passed |
| `…pre553_service_source_applicability_court.py` | adopted owner, unmodified | 60 passed |
| `…source_backed_positioned_subject_possibility.py` | adopted F8 owner, unmodified | 13 passed |
| `…test_a05_z08_positioned_admission.py` | unmodified | 3 passed |

The HQ210 commissioned aggregate of **148** still reproduces (72+60+13+3); the binding
court now collects 74 because the widened AST scan split one test into two.

**Regression: 73 pre-existing slice files, compared as sorted failure-identity sets.**

| | baseline | repaired |
|---|---|---|
| failed | 91 | 91 |
| passed | 1406 | 1407 *(+1 = the split AST test)* |
| errors | 48 | 48 |
| skipped | 1 | 1 |
| **distinct failing/error IDs** | **139** | **139** |

**New failures introduced: 0. Failures removed or changed: 0. Delta is empty in both
directions.** None of the 139 pre-existing failures touch the binder, its courts, or the
three adopted owners — they are unrelated and spread over 16 files.

Slice membership was computed by parsing imports transitively, not by hand. One slice
test imports a materializer from `WORKER_RETURNS/EE-P2R6S`, which the sparse checkout
lacked; that path was added so the slice is complete rather than truncated. This
surfaced a pre-existing collection error and was **not** caused by the repair.

## 6. Write terrain — three owners byte-identical

Verified by `git hash-object` in the shell *and* inside both courts:

```
3e40caca29e8c96ee1f412f919cfc7dba63f96c4  rawlsing_next/pre553_service_source_applicability.py
62e5eced47b64512f47b004e3e13a6ef3fe21de7  rawlsing_next/source_backed_positioned_subject_possibility.py
f30fca20e7b56e00348e82765d95f974b4b6a195  rawlsing_next/objective_consumer_bounded_evidence.py
```

Exactly three files changed (239 insertions, 39 deletions, plus one new court). No
adopted owner was edited. No ranking, selection, priority, preference, weight, pooling,
composition, respondent linkage, source equivalence, currentness authority,
target-use permission grant, backfill, F8 conditioning or geometry/distribution
transformation, or actor/person inference was added. H-D/F8 was not reopened.

## 7. Environment, honestly classified

Interpreter: `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python`,
Python 3.11.3, with `PYTHONHASHSEED`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`PYTHONPATH=<worktree>`, `-p no:cacheprovider`.

Classification is **reconstructed-equivalent on this host**, unchanged as the commission
required. This is **not** governed certification and is not relabelled as such.

## 8. What the rerereviewer should attack first

1. **Repair 1 is the substantive change.** Attack whether the enforced single-source
   refinement can be bypassed through any path that does not go through
   `assert_query_source_admitted` — in particular whether the delegating evaluator can
   reach F8 for a non-requested source.
2. **The new read-only import** of `objective_non_event_currentness_contract` is a new
   dependency edge in the binder's import graph. The file is not modified, but judge the
   edge.
3. **Repair 5 changed failure semantics.** Paths that previously skipped now fail, so an
   environment without git will see failures rather than skips. That is the intent, but
   it is a behavioural change worth confirming.
4. **The currentness pin** derives from an adopted contract's `STATES`. Confirm that is
   the right source of vocabulary, and that refusing `STALE`/`REFRESH_REQUIRED`/
   `INVALID` is the intended semantics rather than over-tightening.
5. **Whether the pre-existing 91 failures / 48 errors** should now be triaged. They are
   out of this lane's scope and deliberately untouched.

## 9. Caveats

- COMPLETE / READY FOR REREVIEW is not acceptance.
- The 139 pre-existing failing identities remain in the tree, untouched by design.
- The negative control used a shadow tree outside the repository. It proves witness
  sensitivity; it does not replace independent reproduction.

## 10. Terminal

`HQ213_HD_F8_BINDING_REPAIR_RETURNED__FINAL_HOSTILE_REREVIEW_REQUIRED`