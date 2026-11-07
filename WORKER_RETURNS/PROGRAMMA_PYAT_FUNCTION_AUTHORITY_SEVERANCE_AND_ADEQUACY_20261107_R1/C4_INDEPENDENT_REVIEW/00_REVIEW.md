# Independent nonauthor review — issue #777 C4 J-role first consumer

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-j-role-independent-review`  
**Review branch:** `review/pyat777-j-role-20261107-r1`  
**Reviewed author cut:** `8986f3d4936edb1bda68f9eda55bf4be710e8642`  
**Author session:** `ses_1b9742b6c02745d8a69d062011` (distinct from this reviewer)  
**Verdict:** **ACCEPT_WITH_REPORTING_CORRECTIONS**

This review covers only C4_J_ROLE_FIRST_CONSUMER and its actual O14/historical
first-reader claims. It does not accept a current native J issuer, historical J
equivalence, structural/science/actor authority, or any protected merge.

## Independently reproduced

- The seven named O14 mechanism tests pass: **7 passed in 2.69s**
  (`02_FOCUSED_TEST_LOG.txt`).
- Current source hashes match the author receipt:
  `pre553_j_role_certification.py` `838e123c…`,
  `pre553_component_authority_vector.py` `9cbe0200…`,
  `pre553_learned_empirical_adjudication.py` `40ce648e…`.
- The six cited historical source pins at
  `9ba4764bef551b1ce498e5772d60b73d69337d4b` match the author receipt
  (`04_SOURCE_PINS.txt`), including the F17/F19/F20/F21 modules and shared
  respondent substrate.
- The actual M1 registration path is present in non-test source:
  `build_j_validator_registry` (`pre553_j_role_certification.py:1018-1027`)
  constructs an exact `M1ValidatorRegistry` with
  `FamilyValidatorRegistration.from_binding(binding,
  j_component_certification_validator)`. `M1ValidatorRegistry` is exact,
  immutable, and explicitly has no aliases/latest/default/fallback
  (`pre553_learned_empirical_adjudication.py:1112-1140`).
- `compose_learned_world` accepts a caller-supplied exact
  `M1ValidatorRegistry` on the M01_M1_M2_B5 route and passes it to
  `adjudicate_learned_empirical`; no J-specific registry is assigned internally.
- No non-test invocation of `build_j_validator_registry`, the J role
  constructors/channel, or `j_component_certification_validator` was found in
  static source. This is **NONE_FOUND_IN_STATIC_SOURCE**, not proof that no
  external/dynamic caller exists. The author's narrow grep of literal
  constructors omitted the registration builder and bare callable reference.

## Required reporting corrections

### C4-R1 — Narrow constructor grep is not sufficient for the “no non-test caller” claim

The author search
`grep -RIn 'JFamilyRoleAssignment(\|...j_component_certification_validator(' ...`
does not cover `build_j_validator_registry`, which is an actual non-test M1
registration builder at `pre553_j_role_certification.py:1018-1027`, nor does it
cover bare callable references. The disclosed result should be:

- exact M1 registration builder exists in non-test source and wires the J
  validator into an exact `M1ValidatorRegistry`;
- no non-test **invocation/call-through** was found statically;
- therefore `NONE_FOUND_IN_STATIC_SOURCE`, not proved absence and not a general
  “no producer” finding.

This is an evidence/reporting correction, not a demonstrated runtime defect.

### C4-R2 — Fixed six-token roles are a different responsibility, not automatically a narrower full pipeline

Current O14 uses `ROLE_VOCABULARY` six tokens
(`exception_case`, `elective_case`, `social_condition`, `family_size_condition`,
`economic_condition`, `target_case`) and M1 role certification. Historical F17
uses dynamic `family_cfg.item_role_groups`/order, `target_resolution_rules`,
`boundary_rules`, `response_role_rules`; F19 compiles family tables; F20 handles
packet/readiness/typed stops; F21 performs structural handoff. These are
different responsibilities. The source/test evidence does not prove historical
equivalence and does not establish that current O14 must reproduce the dynamic
full-J family/order/target/boundary/measurement surface for an actual current
operation. The report should say “different responsibility; historical
equivalence UNPROVED; no actual current J demand established,” not imply a
global “narrower” inadequacy of the whole pipeline.

### C4-R3 — Preserve the precise historical-selection gap

The evidence supports **STATIC_CALLSITE_ONLY / HISTORICAL_SELECTION_UNPROVED**,
not historical absence and not a proved severance or equivalence. F1 callsite
records and source pins identify static historical code routes; they do not
prove a selected original J release/row was executed. AR-0051 draft,
AR-0052/0053 rules and AR-0058 conceptual are candidate inputs, not universal
proof of absence. Missing current native J release or S3 grant does not prove
historical selection absent; it limits current proof. Retain the exact
UNPROVED/NOT_RUN gaps and do not invent an issuer or a new gate.

### C4-R4 — Keep shadow/old-version/revocation NOT_RUN explicit

C4-J01/C4-J02 already record
`old_version_shadow_revoked=NOT_RUN__NO_SELECTED_J_RELEASE`; this is correct.
The concise return/limits should retain that explicit NOT_RUN, not convert it
into an absence claim or a new authority requirement.

## Bounded historical J scope

Historical `F17_J_REGISTRY`, `F19_J_PATTERN`, `F20_J_PACKET` and
`F21_J_STRUCT` are preserved as **static historical callsite/source-pin
candidates** at the cited 9ba cut. No selected original J release/row/version
reaches O14. The current O14 mechanism is caller-supplied/sourcefree and its
seven tests are mechanism tests, not historical parity or original-issuer
evidence. F21/M3 remains a separate potential C3 handoff; no overlap or merge
was performed. No old private cache/compiler restoration, no J installation, no
whole-pipeline absence claim, and no mandatory historical-J demand gate is
authorized.

## Source/test proof limits

- Seven named O14 tests pass; no full suite was repeated.
- Sourcefree synthetic mechanism only; no original respondent/SAV/DTA/DB read.
- No selected original J release, historical first-reader execution, historical
  effect/negative, or actual non-test current operation is established.
- The six historical 9ba source hashes are verified as static source pins, not
  selected runtime use.
- No native/science/actor/current grant, structural admission, FF/post-FF
  effect, or protected receiving is claimed.

## Minimal indispensable next action

Reporting/evidence correction only: disclose the actual M1 registration builder
and state `NONE_FOUND_IN_STATIC_SOURCE` (not proved absence); describe the fixed
six-token mechanism as a different responsibility with historical equivalence
UNPROVED; retain the exact static-callsite/UNPROVED gap and shadow/revocation
NOT_RUN. If a future actual selected non-test O14 operation demands historical
dynamic J family/order/target/boundary/measurement semantics, route the exact
selected release through the existing O14/M1 ABI; otherwise keep the current
sourcefree mechanism and unmatched historical IDs. No new authority, compiler,
cache restore, production patch, or implementation grant is warranted.

## Artifacts

`00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`,
`02_FOCUSED_TEST_LOG.txt`, `03_CALLER_AND_REGISTRATION_SEARCH.txt`,
`04_SOURCE_PINS.txt`, `05_M1_REGISTRATION_AND_CALLTHROUGH.txt`.

All writes were confined to this review lease. No author/production/test/HQ/
peer/protected writes; quota UNKNOWN; STOP after commit/push.
