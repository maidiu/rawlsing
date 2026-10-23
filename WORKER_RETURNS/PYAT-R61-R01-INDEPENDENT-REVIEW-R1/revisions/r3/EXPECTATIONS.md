# R61-R01V R3 frozen independent expectations

Frozen before inspecting R3 code (`89774b019...`), the R3 author return at
`9fbf1ec3b...`, or any R3 author conclusion. Read first: exact R01V R3
commission `ed6cb8675...`, R3 repair commission `3470da602...`, original R01
commission/NODE, R01V original and R2 commissions, R01/R01V INPUTS
(CONTRACTS/TESTS/OVERLAYS/USER_GRANT), and the complete R2 independent review
at `3ac1e498a...` (00_RETURN, EXPECTATIONS, defects, probes, native
conditional-joint/recursion evidence, proof witness/oracle results).

This file is the reviewer's own oracle. Candidate output, author counts,
author-selected cases and author conclusions never define the expected
universe. A partial callable pass is not full R01 qualification.

## 0. Exact review target, separation and grain

- Candidate/startup: `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`.
- R3 code commit: `89774b01990a7d18c10cf4f6e819895776a1a633`;
  parent/prior candidate `f0c602eddaee14a58d6f0935a587a46fcf96c6db`.
- Base: `a54893657ba65e44c1049f763208b0b4b6ed5eb9`.
- Prior independent review: `3ac1e498a08648950d31df0bf52750f9335d24fa`
  (R2 verdict REVISE; A1 blocking R03, A2/A3/A4 secondary).
- Reviewer branch `agent/opencode-pyat-r61-r01v-r3-independent-review-r1`;
  worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r3`.
- Author session `ses_e98c905cbffekusoHURfKyEUKG` is distinct from this
  reviewer session. Same provider account (`opencode-go/deepseek-v4.1-flash`,
  variant max, existing Global) is disclosed; this is role/session separation,
  not institutional scientific independence. Browser whole-native runtime
  remains unqualified.
- R01 owns a prospective symbolic frontier plus sound pre-execution native
  lowering. R03 owns total issuance/execution/Batch; R04 owns serialized
  custody/restore. A missing R03/R04 mechanism is not an R01 blocker by itself,
  but an R01 interface that cannot carry R03's required semantic fields is.
- Sourcefree TEST_ONLY only. No original source/science, adoption, production,
  CI, N11/N12, F6/F7/F8, Sorok or J52/W52 authority.

## A. A1 conditioned JOINT / CO_TRAVEL must bind exact ordered typed predicates

Inherited contract basis: `INPUTS/CONTRACTS.md` Revision 2 (receipt must verify
requested conditions **and values**, not only rule id/count/hash; a many-to-one
template needs an adequate coverage witness); R01V R3 commission A1; R01V R2
commission items 4-5; R01 NODE acceptance "semantic direction grants" and
"unique occurrence keys"; TESTS T05 ordered multi-target/value-conditioned
joint.

For every eligible `JOINT`/`CO_TRAVEL` operation with non-empty ordered
conditions, exactly one of these must hold:

1. `SUPPORTED` lowering whose executed semantic refs actually consume the exact
   ordered condition tuple: every condition occurrence, typed value and domain
   identity is represented by the joint baseline predicate **and** by each
   marginal/baseline query role required by the operation; or
2. a typed `NATIVE_UNSUPPORTED`/refusal that preserves the scientific operation
   as eligible/unsupported with an exact owner limitation and does not claim
   conditioned-joint support.

`SUPPORTED` with the condition atom merely stored in `record.atoms` or only
changing `rule_id` is a defect. Multiple conditioners are a conjunction over
the ordered tuple, not a disjunction, first-condition-only, or last-condition
override. Conditioner order remains semantic. Distinct typed values
(`true` vs `1`, `0` vs `"0"`, explicit null vs absent) must not collapse.

### Frozen A1 reference probes (independent of candidate output)

Use the inherited current native fixtures (synthetic TEST_ONLY C11/I03,
predicate/query catalogs) but derive expected candidate/query-role identities
by this reviewer's own exact join, never from returned receipts.

- **P1 two values:** ordered targets `(q_alpha,q_beta)`, one condition
  `q_gamma in {0,1}`, policy `J=2,K=1,D=0`. Independently locate all eligible
  `JOINT` and `CO_TRAVEL` operations for both values. Expected: for each
  operation either a typed unsupported record or a supported lowering whose
  joint and marginal semantic refs differ according to the exact condition
  value. `q_gamma=0` and `q_gamma=1` executions must not be semantically
  identical; an operation-hash-only difference fails.
- **P2 multiple conditioners:** ordered conditions over two conditioners, e.g.
  `(q_gamma=0,q_delta=1)` vs `(q_gamma=1,q_delta=1)` vs
  `(q_gamma=0,q_delta=0)`. Each ordered conjunction must be consumed; changing
  any component must change the executed predicate semantics or be refused.
  Order-swapped tuples must not silently alias unless the declared semantics
  prove order-insensitivity.
- **P3 data change:** with the same frozen operations/policy, change synthetic
  responses while keeping identities eligible. Membership/frontier and
  lowering semantic refs must not be derived from response values; actual I05
  candidates may legitimately change, but the condition refs must still bind
  the requested condition.
- **P4 bijective rename:** rename items/authority refs bijectively. Logical
  conditioned operations and typed values must be isomorphic; physical refs may
  change. Renaming must not drop or reroute condition semantics.
- **P5 same-rule-id mutation/refusal/restoration:** for the decisive native
  case, mutate a condition predicate/value while preserving `rule_id`, count
  and operation hash as far as possible. The reviewer-owned exact
  candidate/query-role join and the candidate receipt anti-join must fail;
  restoring the exact baseline must pass. A cold subprocess must reproduce the
  same baseline/mutation/restoration result.
- **P6 derived objects consumed:** any derived condition predicate must be an
  actual object/ref present in the lowering grammar and consumed by the native
  execution/query-role path. Presence in `LoweringRecord`/`atoms` alone is
  insufficient.

Acceptance for A1 requires positive supported evidence across both `JOINT` and
`CO_TRAVEL` (or an honest typed unsupported limitation that does not masquerade
as completion) plus the mutation/refusal/restoration/cold controls. A
signature/import crash is not a refusal proof.

## B. A2 canonical operation-ID recomputation and revalidation

Inherited basis: CONTRACTS Revision 2 exact identity K; R01V R3 commission A2;
R2 defect A2; R01 NODE unique occurrence keys; R01V R2 commission item 5.

- Lowering must recompute the canonical operation ID from the operation's
  semantic fields and require it to equal the supplied `op_id`, or typed-refuse.
  It may not trust a persisted `op_id`.
- A forged `op_id` with otherwise valid fields must not return `SUPPORTED`.
- A semantic field change while retaining the old `op_id` (same-rule-id or
  hash-preserving mutation, direction/condition/target/risk/clock/role/design
  or other identity-bearing field) must be detected and typed-refused or
  recomputed to the new canonical ID; it may not remain `SUPPORTED` under the
  stale ID.
- A valid recomputed/canonical operation must still lower positively and
  restore after the mutation. Revalidation must not be a blanket refusal.

## C. A3 truly empty complete frontier vs unsupported-only/PENDING

Inherited basis: CONTRACTS Revision 2 total states/conservation; R01V R3
commission A3; R2 defect A3; TESTS T01/T03; R01 commission "complete
disposition ledger ... lazy deterministic partition".

- `VALID_EMPTY`/`allow_empty_frontier=True` only for an independently complete
  frontier with zero considered operations (or zero eligible operations with
  the declared complete inventory and no pending/unsupported/held/unknown
  obligations), not merely zero *supported* operations.
- A nonempty scientific frontier whose operations are all currently
  `UNSUPPORTED_RUNTIME` must report `allow_empty_frontier=False`, retain the
  exact unsupported operation IDs and eligibility, and must not advertise a
  valid empty native grammar.
- Budget exhaustion yields exact `PENDING` IDs and is not empty/complete.
- Conserve disjoint partitions:
  considered scientific = eligible + prohibited + proven-inapplicable +
  held/unknown; eligible workload = supported/completed + pending +
  runtime-unsupported + errored. Unsupported/deferred cannot overwrite
  eligibility or disappear. Partition/flatten/cold recompilation preserve exact
  operation identities and counts.

Frozen probes: (i) a catalog with no supported claims over a nonempty eligible
frontier; (ii) a genuinely complete frontier with no considered operations;
(iii) a budget-limited eligible frontier with exact pending IDs; (iv) exact
set accounting across all partitions before/after partition/cold recompute. A
count-preserving substitution must fail an exact identity anti-join.

## D. A4 recurrence/baseline: honest preserved limitation vs generic failure

Inherited basis: CONTRACTS Revision 2 ("Apply issued class, arity J,
conditioning K and recursion D bounds; no hardcoded universal bounds";
operation identity binds "recursion/baseline"); R01 NODE acceptance;
R01V original/R3 commission item 2 "recursion/baseline/arity bounds"; R01V R2
commission item 6; R2 defect A4; R01V R3 commission A4.

The test is **not** whether R01 must invent original source science. The test
is whether an existing generic/synthetic recurrence, baseline or issuer
primitive/contract already suffices to represent and enumerate the required
policy semantics. Original-source scientific issuance is not automatically
necessary to represent generic recurrence/baseline policy.

`EXACT_CONTRACT_GAP` is an honest preserved limitation only if all hold:

1. The inherited contracts and current native/declared policy primitives do not
   already define a competent generic recurrence relation, baseline issuer or
   recurrence enumeration semantics sufficient for R01's generic scope. The gap
   is identified by exact primary refs, not missing implementation convenience.
2. R3 does not alias recursion/baseline to conditioner depth, does not relabel
   `K-1` as independent D recursion, and does not silently drop operations or
   bounds.
3. D and baseline are carried as explicit typed operation/policy fields or
   refs; D13 is explicitly **not** claimed PASS; any unsupported recurrence
   workload remains eligible and typed unsupported/pending.
4. If existing settled rules suffice, R3 must implement the independent
   enumeration. A missing *scientific issuer* is not accepted as the reason to
   omit a *generic policy representation* that the contracts already define.

Frozen probes: policy `J=1,K=3,D=3`, explicit recurrence/baseline refs where the
schema permits. Expected diagnostics must show whether `recursion_depth` is
independent of `len(conditions)`; whether a FORK can exist at recursion depth
independent of conditioner count; whether `baseline_policy_ref` is consumed
rather than ignored; and whether changing D changes exactly the declared
branching. If exact gap is claimed, enumerate the smallest competing
interpretations with exact primary refs and state which are generic software
vs original-source issuance. "Do not manufacture a scientific issuer blocker
where existing settled rules suffice."

## E. Process/identity/artifact checks

- Verify startup `9fbf1ec3b...` equals local HEAD and reviewer branch direct
  remote identity; candidate code `89774b019...` four blobs; author changed-path
  allowlist exactly the original four R01 paths plus the author's R3 return
  root; six R3 report artifact hashes; manifest explicit self-exclusion;
  immutable prior reports/INPUTS/commissions unchanged.
- Replay the focused prior 20 probes with reviewer-owned JUnit and actual
  imports, retaining prior demonstrated controls by exact identity except where
  changed code/schema requires a meaningful replay. Do not miscount deselected,
  import-crashed or stale path-derived failures as safety passes.
- Run own independent A1-A4 probes/outcomes/JUnit, exact frontier identities and
  native mutation/refusal/restoration/cold proof.
- Positive -> targeted assertion fault -> restored positive/cold is required.

## F. Frozen verdict rule

- `ACCEPT_SCOPED_LOCAL` at R01 grain only if all of A1, A2, A3 and A4 are
  resolved as above, the author suite/prior controls replay, independent
  identity/allowlist/manifest/immutable checks pass, three-axis conservation
  holds, and no remaining defect truly blocks R03 at R01's interface.
- Otherwise `REVISE` or `HOLD` with minimal exact primary evidence, demonstrated
  R3 capability delta, remaining defects, actual native consumer and
  NOT_REACHED edges.
- Return separate exact findings: (i) demonstrated R3 capability delta and
  remaining defects; (ii) full R01 contract qualification or HOLD/REVISE;
  (iii) whether R03's actual start prerequisite is met, with exact contract
  basis. A partial callable pass must not masquerade as full R01 qualification.
- A4 needing a concrete higher engineering/architecture decision gets the
  smallest competing interpretations and exact primary refs, not an unbounded
  audit.
- R03 start requires independently qualified R01 **and accepted R02**
  (`INPUTS/USER_GRANT.json` `r03_start_condition`; R61 FLIGHT). This reviewer
  supplies evidence only; no HQ wake authority.
- Preserve original35/1890/globalF6F7F8/Z UNRESOLVED16 and all source/science/
  CI/prod/N11/N12/Sorok/J52/W52 holds unchanged.
