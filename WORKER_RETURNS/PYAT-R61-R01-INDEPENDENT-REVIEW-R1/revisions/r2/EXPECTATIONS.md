# R61-R01V R2 frozen independent expectations

Frozen before inspecting R2 candidate code (`d56e53301`), the R2 author return,
or any author R2 conclusion. Read first: R01V R2 commission
`b04278d1...:R01V/revisions/r2/00_COMMISSION.md`, original R01 commission,
R01/R01V INPUTS/CONTRACTS/TESTS/OVERLAYS, R01 R2 repair commission, and prior
independent review `b310c5469` (EXPECTATIONS/00_RETURN/defects/probes/results).
This file is the reviewer's own oracle. Candidate output, author counts and
author-selected fixtures are never the expected universe.

Exact candidate/startup: `f0c602eddaee14a58d6f0935a587a46fcf96c6db`; code
`d56e53301aaa0203e83fc1b60a0bcafb86b17892`; prior code `d6f41177b`; base
`a54893657ba65e44c1049f763208b0b4b6ed5eb9`. Reviewer branch
`agent/opencode-pyat-r61-r01v-r2-independent-review-r1`; worktree
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r2`. Same provider
account disclosed; not institutional scientific independence. Browser
whole-native runtime unqualified.

## A. R01 grain and later-owner boundary (frozen)

R01 owns a *prospective symbolic frontier plus sound pre-execution native
mapping*. It must be sufficient for R03 to start. R01 does not own:

- R03 total issuance, native execution of every operation, U43
  `IssuedWorkloadRecord`, Batch unit binding or duplicate-discovery proof;
- R04 authenticated byte custody, serialized cold restore/resume, revocation;
- R05 five proof grades/canonical values-read; R06 world/F6/F7/F8; original
  E_pre/science; N11/N12; production/CI.

Therefore: deterministic cold *recompilation* from the same frozen inputs must
conserve exact identities; serialized cold *restore* remains NOT_REACHED for R04
and must not be claimed. A missing R03/R04 mechanism is not by itself an R01
blocker. An R01 interface that cannot carry the needed R03 fields *is* an R01
blocker. The final verdict must state precisely which remaining issue (if any)
truly blocks R03 at R01 grain.

## B. Exact operation identity K (must be conserved, independently derived)

For each operation, identity binds at minimum:

1. source id/dataset/wave/edition/byte digest; instrument/grammar/model/policy
   version; grade;
2. occurrence identity `(item, option, form, repeat)`; never bare names; no
   reserved `ID`/`Y`/`q301` semantics;
3. unit, lawful link, respondent/person/household/reporting role;
4. applicability/risk identity and predicate identity; common-risk semantics
   explicit (unknown is not silently "unconstrained");
5. ordered target occurrence tuple with exact direction/role; target vs
   conditioner role preserved; ordered semantics not sorted into sets;
6. ordered condition tuple `(occurrence, typed value, domain/state version)`;
   tags for bool/int/string/explicit-null/absent; absent distinct from null;
   `(c_bool,true)` != `(c_int,1)`; `(c_int,0)` != `(c_int,null)` != absent;
   order of condition components semantic;
7. operation class/arity/topology; declared recursion depth and baseline
   identity separate from conditioner depth K; finite issued bounds J/K/D;
8. estimand/population, weight/design/strata/cluster/uncertainty method refs;
9. observation/reference/as-of/publication clocks, permitted comparisons,
   current-selection ref;
10. custody/release refs where the contract requires them.

Logical frontier identity and physical provenance identity are distinct:
changed response bytes may change provenance-bound identity but must not change
prospective membership; a legitimate bijective label rename changes physical
refs while producing isomorphic logical operations/typed values. Hashing a
frontier alone does not substitute for per-operation K binding. Response
observations never determine membership.

## C. Independent tiny reference frontiers

Fixtures are declared literally; expected identities are hand-derived, not
read from candidate output.

- **X1 arbitrary/ordered targets:** targets `alpha`,`beta`; conditioners
  `gamma` bool `{true,false}`, `delta` int `{0,1}`; J=2 K=1 D=0, no reserved
  names. Ordered nonempty target selections = `(alpha)`,`(beta)`,
  `(alpha,beta)`,`(beta,alpha)` = 4. Condition choices = `()`,`(gamma,true)`,
  `(gamma,false)`,`(delta,0)`,`(delta,1)` = 5. If condition values are declared
  part of operation identity, independent Cartesian frontier = 20 exact
  `(ordered targets, ordered conditions)` identities; a different declared
  lawful grain must be explicit and still conserve ordered roles.
- **X2 bijective rename:** rename to `zeta/eta/theta/iota` plus rewritten
  authority refs; expected logical frontier is X1 under the bijection with
  identical typed values; physical row and partition order changes nothing.
- **X3 typed collisions:** condition values `true` vs `1`, `0` vs `"0"`, `None`
  vs absent vs `0`, `False` vs absent; native target cells `1` vs `"1"` and
  `True` vs `"True"` must not collide. A typed codec may either preserve actual
  native semantics injectively or typed-refuse with exact reason; silent
  stringification is forbidden. Catalog-declared support alone is not proof
  the actual engine executes the shape.
- **X4 roles/forms/repeats/units/risk:** F1/F2, R0/R1, person/household, Rk1/Rk2
  and direction D1/D2 stay distinct; no cross-unit joint; only exact authorized
  combinations eligible; reverse direction prohibited until granted.
- **X5 administration/inventory:** duplicate qualified occurrence keys refused
  before construction; `administered=false` never eligible/executed and carries
  a structured owner reason bound to the occurrence/operation; admin unknown
  stays unknown; admin true with all response values missing does not shrink
  the prospectively frozen frontier; absent inventory/U_Epre is typed
  absent/unknown, never valid empty; declared complete inventory with zero
  eligible operations is `VALID_EMPTY` with a countable empty set and no filler.
- **X6 bounds/recursion:** J/K/D are finite issued values; D is recursion depth
  distinct from conditioner depth; baseline identity carried; changing D
  removes/retains exactly the identities implied by the declared branching.
  Budget exhaustion yields exact pending IDs; it cannot lower J/K/D, drop
  shapes or report smaller complete frontier.
- **X7 multiplicity/no-drop:** every expected identity present; no duplicate
  counted twice; same-count substitution (drop one expected, add another) must
  fail an exact identity anti-join even when counts agree; many-to-one native
  templates need an explicit adequate coverage witness.
- **X8 partition/cold:** deterministic partition flattening and cold
  subprocess recompilation conserve exact op IDs, content root, disposition
  counts, held/unknown/unsupported/pending sets; physical row permutation does
  not change logical identities. Serialized restore is NOT_REACHED.

## D. Three axes, conservation, native receipts

- Eligibility `{ELIGIBLE,PROHIBITED,INAPPLICABLE_PROVED,HELD,UNKNOWN}`,
  execution `{NOT_STARTED,PENDING,COMPLETED,UNSUPPORTED_RUNTIME,ERROR}`, result
  `{SUPPORTED,OBSERVED_ZERO,VALID_NULL,DIFFUSE,VALID_EMPTY,ZERO_SUPPORT,
  UNSUPPORTED,UNKNOWN}` are separate; one conflated enum is a defect.
- Conservation: considered = eligible + prohibited + proven-inapplicable +
  held/unknown; eligible = adequately completed + pending + runtime-unsupported
  + errored. Runtime failure cannot rewrite eligibility; unsupported/deferred
  cannot disappear.
- `LoweringRecord` carries: operation_ref; lowering_version; exact
  predicate/query/DiscoveryAuthority refs; expected candidate/query-role keys;
  planned Batch-unit refs; typed refusal; evidence-grade ceiling. Refusal must
  be typed, not free text.
- Native receipt anti-join must bind exact requested/returned **targets,
  conditions and typed values**, predicate/query/authority/candidate/query-role
  objects, not only `rule_id`/count. Decisive probe: run real current I05 with
  synthetic C11/I03 inputs; baseline positive; semantically change one
  condition atom (same rule_id/count); the same anti-join/consumer assertion
  must fail; restore the condition and the same assertion must pass in a cold
  process. Actual receipts/native owners read-only.
- Forged direction/policy/frontier dispositions must not be silently trusted;
  lowering revalidates or typed-refuses. Missing-map branch must not precede
  current catalog capability lookup. Unsupported shapes remain scientific
  obligations typed `UNSUPPORTED_RUNTIME`, never pruned.

## E. Required artifacts/process checks

- Remote/startup exact; changed paths only the original four R01 allowlist code
  paths plus the author's own R2 return root; six author report hashes valid;
  immutable v1 reports/commission/INPUTS unchanged; manifest self-excluded.
- Author suite replay with reviewer JUnit/actual imports; own hostile probes
  independent of author counts; versioned probes acceptable for schema change,
  but import/signature crash is not a passing refusal.
- Positive -> targeted assertion fault/refusal -> restored positive and cold
  required for the decisive native proof.
- No candidate code/test edit; probes/mutant copies only under this return
  root. No originals/private home/credentials/models/providers/accounts/
  subagents/sessions. 45 min budget, bank by 35; non-force push own branch and
  direct-verify SHA.

## F. Frozen verdict rule

`ACCEPT_SCOPED_LOCAL` only if all hold: (i) identity/allowlist/manifest/immutable
checks pass; (ii) author suite replays green under reviewer JUnit with actual
imports; (iii) independent X1-X8 and D1-D8 hostile replays match this oracle,
including actual I05 same-ruleid semantic mutation refusal and restored cold
positive; (iv) three-axis conservation holds; (v) `LoweringRecord` and typed
codec/refusal are sound for R03 at R01 grain; (vi) no remaining defect truly
blocks R03 start. D9-D16 are judged at their correct R01 owner grain; later
R03/R04 gaps are NOT_REACHED, not verdict drivers unless the R01 interface
fails. Otherwise `REVISE` or `HOLD` with minimal reproducible primary evidence,
actual capability delta, exact native consumer and NOT_REACHED. If core function
is still unmet after R2, state the exact missing function/primitive and finite
engineering options; no third minor audit.
