# WSC002R — GT0 BOUNDED PARALLEL REPAIR PROGRAM R1

## Mission

Repair only the material defects established by the bounded hostile audit at exact audit evidence ref:

`252418c42722d0021273acc5bfe0fd3d852f2145`

Audited integration / repair working base:

`8028353c289875bb5d9993457362759932235535`

The audit evidence commit is evidence only. Every repair worker begins exactly at the working base above.

No worker may consume a sibling repair branch. No PRE-MAIN or `main` ref movement. No whole-spine redesign. No FIELD FORGE R2 reopen. No positive actor/PSEPF/render authority. No physical-architecture selection.

After A/B/C return, central Vozhd integrates only their bounded changes and reruns the exact existing audit.

---

# HANDOFF A — TYPED-NEGATIVE CONSERVATION FIX R1

Branch:
`agent/rabochii-wsc002r-a-typed-negative-fix-r1`

Repair only:
- `rawlsing_next/wsc_gt0_field_forge_ingress.py`
- one focused hostile regression under `rawlsing_next/tests/`

Exact defect:
The output envelope uses `status=source.status` but the enclosing `GT0StageReceipt` hard-codes `PASS`, so lawful non-PASS upstream typed states fail status consistency.

Required repair:
- change the receipt status to the exact preserved `source.status`;
- do not otherwise alter semantic behavior;
- add a hostile regression using at least one lawful non-PASS status and prove exact typed-state conservation without constructor failure or promotion;
- preferably cover more than one representative negative state if trivial, but do not broaden scope.

Terminal:
`PASS__WSC002R_A_TYPED_NEGATIVE_CONSERVATION_REPAIRED__READY_FOR_REINTEGRATION`

---

# HANDOFF B — AUTHORITATIVE V3 ZERO-POSITIVE GUARD BINDING R1

Branch:
`agent/rabochii-wsc002r-b-v3-authoritative-guard-binding-r1`

Repair only:
- `rawlsing_next/wsc_gt0_v3_runtime.py`
- focused tests under `rawlsing_next/tests/`

The current candidate shadows the expected zero effect locally. It must instead bind the accepted current V3 firewall in:

`rawlsing_next/v3_psepf_zero_positive_guard.py`

At the working base its accepted contract is:
- `GUARD_ID = IG_PSEPF_ZERO_POSITIVE_GUARD`
- `GUARD_VERSION = ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE@1`
- `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` is immutable and empty;
- `evaluate_psepf_zero_positive_guard(...)` returns a governed `GuardDecision`;
- denied decisions preserve actor state, causal ledger/cursor, RNG and scheduler exactly.

Required repair law:
1. GT0 must derive/validate its V3 zero-positive disposition against the authoritative guard, not merely reproduce the expected status locally.
2. Do not manufacture a positioned-subject possibility, comparator, PSEPF object, or positive authority that the GT0 baseline does not possess.
3. Use only a truth/provenance class already lawfully represented by the GT0 PRE-V3 evidence when binding the guard. Do not relabel F0 into a stronger source class.
4. Bind the guard identity/version and decision/reason into GT0 provenance/replay or receipt detail strongly enough that divergence in the authoritative guard makes focused tests fail.
5. Preserve exact zero mutation: actor state, causal ledger/cursor, RNG and scheduler unchanged.
6. Positive delegation remains impossible under the current empty production registry.
7. Add focused tests proving the authoritative guard was actually invoked/bound and that a local shadow implementation cannot silently substitute for it.

Terminal:
`PASS__WSC002R_B_V3_AUTHORITATIVE_ZERO_POSITIVE_GUARD_BOUND__READY_FOR_REINTEGRATION`

---

# HANDOFF C — AUTHORITATIVE M6 / RENDER NEGATIVE-SEAM BINDING R1

Branch:
`agent/rabochii-wsc002r-c-m6-render-authoritative-binding-r1`

Repair only:
- `rawlsing_next/wsc_gt0_v2_mediation.py`
- focused tests under `rawlsing_next/tests/`

The current candidate shadows the expected no-claim/no-render outcome locally. It must bind the accepted current negative authority surfaces in:

`rawlsing_next/m6_actor_safe_expression.py`
`rawlsing_next/render_bounded_expression.py`

Current accepted negative surfaces include:
- M6: `situated_expression_behavior_status() == BLOCKED_NAMED_AUTHORITY_REQUIRED`;
- M6: `require_situated_expression_owner()` fails closed absent separately accepted situated-expression authority;
- M6: upstream structural/empirical/audit material has no generic positive behavioral-source admission path;
- renderer: `current_positive_plan_authority_status() == BLOCKED_NAMED_AUTHORITY_REQUIRED`;
- bounded render makes no model call on nonpositive/missing-authority paths.

Required repair law:
1. GT0 must bind the current M6 negative semantic ceiling and current render-plan authority ceiling rather than locally minting equivalent booleans/status text.
2. Do not fabricate an `ActorSafeClaimEntry`, positive first-person permission, admitted semantic plan, renderer binding, wording variant, model call or causal return.
3. Do not fabricate an actor-safe positive envelope merely to exercise a positive API. Use the narrowest existing negative-only contract surfaces sufficient to establish that current M6 and render authority block the path.
4. Bind exact M6/render contract identity/status into GT0 provenance/replay or receipt detail strongly enough that authoritative-contract divergence makes focused tests fail.
5. Terminal must remain `BLOCKED_NAMED_AUTHORITY_REQUIRED`, actor claim absent, rendered artifact absent, model invocation count zero, V3 state unchanged.
6. Add focused tests proving both M6 and render negative surfaces are actually bound, not shadowed.

Terminal:
`PASS__WSC002R_C_M6_RENDER_AUTHORITATIVE_NEGATIVE_SEAMS_BOUND__READY_FOR_REINTEGRATION`

## Fan-in and rereview

Central integration must consume A/B/C only, preserve all other WSC002 integrated files unchanged except concrete API glue required by these bounded repairs, and produce a repaired candidate descendant of `8028353c289875bb5d9993457362759932235535`.

Then rerun the exact bounded hostile audit from `01_EXACT_BOUNDED_HOSTILE_AUDIT_HANDOFF.md`, explicitly retesting both prior material defects. No broader audit campaign is authorized.
