# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — TRUST-BOUNDARY CORRECTION — R2
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq152-c1-03a-trust-boundary-correction-r2`

Exact repair-return base:
`c4e37038add8fce1119db62b523f1529182547a9`

Prior independent review:
`agent/reviewer-pyat-hq149-c1-03a-r1 @ 6bc1cb8ecd5568d6e78e83916763f125e8b888c8`

Prior repair commission:
`2906f6a408f89c6af609e541304e90091fcf2eb5`

Prior repair disposition:
`PASS_C1_03A_REVIEW_REPAIR__INDEPENDENT_REREVIEW_REQUIRED`

HQ intake does **not** advance `c4e37038...` to rereview yet. The substantive repair is promising, but the original caller-authority problem remains statically reproducible at the new wrapper layer.

This is a narrow correction, not a reimplementation.

## HQ blocker A — projection trust moved outward

Current:
- `ProducerStateEvidence` requires `_PROJECTION_TOKEN`;
- but ordinary callers can directly construct `OwnerStateProjection(... retained_state=<chosen label> ...)`;
- `OwnerStateProjection.as_evidence()` then supplies the protected token and mints trusted evidence;
- `OwnerStateProjection.derive(... derive_fn=<caller function> ...)` is also public and lets a caller choose arbitrary projection logic.

Therefore the claim "retained state is always owner-derived" is not yet enforced.

### Required correction

Make `OwnerStateProjection` itself factory-only/fail-closed.

Direct public construction with arbitrary retained state must fail.

Only typed factories that actually read competent owner objects may mint a valid projection:
- empirical fact;
- exact discovery receipt;
- adaptive result;
- exact owner refusal;
- positive recursive handoff, if needed.

The generic `derive` helper must not remain a public authority-minting escape hatch. Make it private/internal and token-protected, or otherwise impossible for an external caller to provide arbitrary projection logic.

Add a hostile that exactly does:

`OwnerStateProjection(owner=..., producer_state="SUPPORTED", retained_state="VALID_EMPTY", ...).as_evidence()`

and prove it cannot mint trusted evidence.

Also remove fixture/test code that reconstructs an `OwnerStateProjection` directly merely to replace `supporting_refs`. If the adaptive owner's exact unvisited/visited/determinant refs are required, the typed adaptive factory must derive/carry them itself.

## HQ blocker B — owner-refusal projection is overbroad

Current `from_owner_refusal` accepts any `BaseException` and maps:
- exception class name containing `Integrity` -> `INTEGRITY_FAILURE`;
- everything else -> `BLOCKED_REQUIRED_AUTHORITY`.

That permits a caller-created `ValueError`, `RuntimeError`, etc. to mint a governed BLOCKED state.

### Required correction

Refusal projection must recognize only exact competent owner refusal classes/contracts for the state being claimed.

At minimum:
- integrity fixture must prove and require the exact accepted empirical integrity exception family (e.g. `Pre553IntegrityError` at the actual owner path);
- blocked-required-authority fixture must prove and require the exact current discovery/authority refusal type or exact typed owner refusal receipt/state produced by that path.

Do not classify by exception class-name substring.
Do not default arbitrary exceptions to BLOCKED.

If the two competent refusal paths have different exact exception families, use typed dedicated factories rather than one heuristic.

Add hostiles:
- arbitrary `ValueError` cannot mint BLOCKED;
- arbitrary exception whose name contains "Integrity" cannot mint INTEGRITY_FAILURE;
- correct real owner refusals still produce the two distinct mandatory states.

## HQ blocker C — route obligation can still be caller-forged or omitted

Current `RouteObligation` is an ordinary public dataclass. `assert_route_not_laundered` checks only `isinstance`, so a caller can directly construct a forged obligation.

Also `build_state_route_result(route_class=LEARNED_OR_ADJUDICATED_REQUIRED, route_obligation=None, ...)` remains accepted; the committed court `test_at15_route_label_alone_creates_no_authority` explicitly demonstrates this.

That does not satisfy the review law that learned/adjudicated route legitimacy be owner/use-derived.

### Required correction

Make `RouteObligation` factory-only/fail-closed. Direct construction must not establish legitimacy.

For this C1-03A contract:
- a `LEARNED_OR_ADJUDICATED_REQUIRED` envelope must carry a valid owner-derived route obligation;
- a competent `DIRECT_EMPIRICAL` route must not require one;
- changing only the route label must never create a lawful learned route.

The positive structural-admission factory must continue to bind:
- exact admission receipt;
- exact admission authority;
- exact empirical fact;
- exact rule hash when ADMITTED;
- receipt-declared target use;
- owner decision/reason and blocking refs.

For a positive ADMITTED route, validate any requested-use claim against the receipt-declared use rather than allowing contradictory caller metadata.

For a negative owner evaluation whose receipt truthfully says `UNRESOLVED_STRUCTURAL_USE`, preserve that exact receipt-declared value; do not invent the requested target use as granted authority.

Replace the current "learned label alone creates no authority" acceptance court with a hostile proving learned-without-obligation is refused.

## HQ blocker D — coverage custody can still be caller-forged

Current `RecursiveCoverageCustody` is an ordinary public dataclass. A caller may construct:

- a real handoff_ref;
- an arbitrary coverage_record_ref;
- an arbitrary completeness_state;

and `build_state_route_result` accepts it if no separate conflicting `coverage_record_ref` is supplied.

`from_handoff` also accepts caller-supplied `completeness_state`, even though `RecursiveBranchHandoff` itself does not own that completeness grade.

### Required correction

Make `RecursiveCoverageCustody` factory-only/fail-closed.

The owner-derived custody must bind at least:
- the exact real handoff ref;
- exactly `handoff.evaluated_frontier_ref`;
- the handoff's internally bound scope/frontier identity.

Do not permit a caller to substitute a different coverage ref.

Do not claim a completeness grade that is not carried by the owner object. Either:
- remove that field from the custody identity if it is not owner-owned; or
- require the exact competent discovery/adaptive result that owns the completeness grade and derive it from that object.

Add hostiles proving:
- direct forged custody construction cannot authorize a handoff;
- same handoff + wrong coverage ref fails;
- caller-chosen completeness label cannot alter authoritative custody;
- real positive handoff + exact frontier custody still passes.

Also add a typed `OwnerStateProjection.from_recursive_handoff(...)` (or equivalent) so positive handoff state is not itself created through direct `OwnerStateProjection(...)`.

## Preserve from c4e37038

Do not regress the valid work already established:
- AT16 54/6 is `SUPPORTED`, never OBSERVED_ZERO;
- all eight negative states stay distinct;
- real adaptive UNVISITED stays owner-derived;
- genuine ADMITTED learned route exists and binds rule/receipt/authority;
- failed/DENY structural routes do not launder to direct;
- positive recursive handoff requires exact coverage custody;
- producer -> accepted C1 composition -> named consumer path remains real;
- C1-02 remains untouched.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-TRUST-BOUNDARY-CORRECTION-R2/**`

Do not modify C1-02, AT17/N10E, C1-03R/lifecycle/replay, C5/C7, or V3 terrain.

## Required court

Re-run the same ten-file commissioned set from the prior repair, plus all new trust-boundary hostiles.

Record exact counts. Preserve the prior 175 as historical evidence; do not assume the new count.

## Return

Write only:
`WORKER_RETURNS/PYAT-C1-03A-TRUST-BOUNDARY-CORRECTION-R2/**`

Required:
- `00_RETURN.md`
- `01_HQ_BLOCKER_DISPOSITION.json`
- `02_TRUST_BOUNDARY_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_C1_03A_TRUST_BOUNDARY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No raw sources. No C4. No C1-03 join. No C1-R. No actor/V3 work.

Terminal:
`C1_03A_TRUST_BOUNDARY_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`
