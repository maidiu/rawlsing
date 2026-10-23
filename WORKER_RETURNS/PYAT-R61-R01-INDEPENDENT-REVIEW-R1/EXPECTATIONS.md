# R01V frozen independent expectations — written before candidate inspection

Frozen at 2026-10-23T05:39Z by reviewer session, before reading candidate
`rawlsing_next/universal_grammar/*` or author return. Candidate/startup
`fcf9fe9f8662c9e98801e670d0d4357072d8d453`; code commit
`d6f41177b16711ec721a9782c9797131295db2b5`; base `a54893657ba65e44c1049f763208b0b4b6ed5eb9`.
Reviewer branch `agent/opencode-pyat-r61-r01v-independent-review-r1`.

Sources of this oracle: `INPUTS/CONTRACTS.md` Revision 2 (K identity, axes,
occurrence/admin rules, conservation), `INPUTS/TESTS.md` T01-T03/T05,
`R01/00_COMMISSION.md`, inherited U53A11 R01 overlay. Candidate output is not
an oracle. Author counts and its seven native examples are not universal.

## A. Operation identity (must be conserved exactly)

An operation identity binds at minimum:

1. source/dataset/wave/edition/digest, instrument/grammar/model versions;
2. occurrence identity `(item, option, form, repeat)` — never bare column name;
3. sampled/reporting unit, lawful link, respondent/person/household role;
4. risk set, applicability/predicate identity;
5. **ordered** target occurrence tuple, preserving direction/role and
   target-vs-conditioner role; literal names `ID`/`Y` have no meaning;
6. **ordered** condition tuple of `(occurrence, typed value, domain/state
   version)`; typed bool/int/null/absent must not collide; explicit null is
   distinct from absent; order is semantic unless owner declares unordered;
7. operation class, arity, topology (scalar/MR/rank/repeat/form), recursion
   depth/baseline;
8. estimand/population, weight/design/strata/cluster/uncertainty method refs;
9. observation/reference/as-of/publication clocks and permitted comparisons;
10. custody/release/currentness refs where the declared contract requires them.

K is canonical: tagged scalar types, deterministic keys, no float/string
coercion, no accidental value-dependent membership. Unordered sets may sort;
ordered tuples must not.

## B. Exact hand-computed frontiers for independent tiny inventories

Fixtures below are declared literally; each expected identity set is computed
by hand under the stated policy, not by the candidate.

### E1 arbitrary labels, ordered targets

Inventory: targets `alpha`, `beta` (same unit/risk/form/clock); conditioners
`gamma` (bool domain `{true,false}`), `delta` (int domain `{0,1}`); policy
J=2, K=1, D=0. No item is named ID, Y, or q301.

Expected target tuples, ordered and distinct:
`(alpha)`, `(beta)`, `(alpha,beta)`, `(beta,alpha)` = **4**.
Expected conditioner tuples for K=1 plus empty: `()`,
`(gamma,true)`, `(gamma,false)`, `(delta,0)`, `(delta,1)` = **5**.
Expected frontier with independent Cartesian combination = **20**, with every
combination carrying identical non-target K fields. If the implementation
declares condition values outside the operation identity, the count may
legitimately be **4**; that design choice must be explicit and must still keep
ordered occurrence/role identity. A different non-declared count is a defect.

Falsifiers: any automatic `ID`/`Y` target, any reliance on literal name,
dropping `(beta,alpha)` as duplicate of `(alpha,beta)`, set-sorting the target
order, or pruning any tuple from observed values.

### E2 bijective rename

Rename E1 occurrences `alpha->zeta`, `beta->eta`, `gamma->theta`,
`delta->iota` and rewrite all authority refs. Expected logical frontier is
E1 under the bijection: exactly 20 (or 4 under the explicit condition-value
alternative) corresponding identities and identical typed values. Physical
row order and separate partition order must not change the logical set.
Falsifier: any count/identity difference or authority mismatch.

### E3 roles, direction, risk, unit, form, repeat

Inventory adds: same item measured on two units (person, household); one
target authorized only in direction `D1` and one only in `D2`; distinct forms
`F1`,`F2`; repeat occurrences `R0`,`R1`; risk sets `Rk1`,`Rk2`. Policy
restricts unit/risk/form/direction.

Expected: operations keyed by the full `(unit,risk,form,repeat,direction)`
qualified occurrence identity; `F1` and `F2` never alias; `R0` and `R1` never
alias; a person operation never becomes a household operation by string
concatenation. Only exact authorized combinations are eligible. Direction is
an explicit grant, not inferred from a value or a column suffix.
Falsifier: collapse across form/repeat/unit/risk/direction; manufacturing a
cross-unit joint; treating `R0`/`R1` or `F1`/`F2` as duplicates.

### E4 ordered multi-target and ordered typed conditions

Inventory: targets `t1`,`t2`,`t3`; conditioners `c_bool` bool,
`c_int` int `{0,1,2}`; J=3, K=2, D=0. Expected ordered target tuples are all
non-empty ordered selections without repetition of length 1..3 = 3+6+6=**15**
(if repeats are declared lawful, add them explicitly; the fixture declares
them unlawful). Ordered condition pairs over the two conditioners (with
repetition governed by declaration) and typed values are enumerated exactly
from the frozen domains. Collision tests: `(c_bool,true)` != `(c_int,1)`;
`(c_int,null)` != `(c_int,absent)` != `(c_int,0)`; `(c_bool,false)` !=
`(c_bool,absent)`. Condition component order is preserved:
`((c_bool,true),(c_int,1))` != `((c_int,1),(c_bool,true))`.
Falsifier: JSON-string/native-`bool`/int coercion collision, dropping either
order, flattening null/absent, or silently pruning a declared domain value.

### E5 recursion, baseline, arity bounds

Policy J=2, K=1, D=3 with declared baseline depth 0 and recursion relation.
Expected: depths 0..3 enumerated exactly, each depth carrying its own bound
identity; baseline is not invented and recursion does not exceed D. Changing
D to 2 must remove exactly depth-3 identities and nothing else (count delta
must be independently derived from branching). A runtime budget may mark
remaining exact IDs PENDING; it may never lower J/K/D, remove shapes, or
report a smaller complete frontier.
Falsifier: hardcoded universal J/K/D, silent truncation reported as complete,
or budget-linked disappearance of identities.

### E6 administration and inventory completeness

- `administered=false` occurrence: must be refused/held, never eligible and
  never executed; a structured reason bound to that occurrence is required.
- `administered=unknown`: must remain unknown/held, not excluded as false.
- `administered=true`, all response values missing: membership is frozen
  prospectively; all-missing data must not shrink the eligible frontier.
- absent inventory / absent original `U_Epre`: must be typed absent/unknown
  (no invented operations), never treated as a valid empty inventory.
- declared complete inventory with zero eligible operations: valid empty,
  distinct from absent, with a countable empty set and no filler.
- duplicate qualified occurrence keys: refused before dictionary
  construction/emission; ambiguous duplicates may not silently overwrite.
Falsifier: any value-dependent prune, admin-false eligible operation,
all-missing shrink, absent-as-empty, or duplicate overwrite.

### E7 multiplicity / no-drop

For any reference frontier F and candidate result R:
- `R` contains every `F` identity (no omission);
- no duplicate identity in `R` counts twice;
- a same-count substitution (drop one identity, add a different one) must fail
  identity anti-join even when counts agree;
- distinct eligible operations mapping to the same native template remain
  distinct scientific operations; many-to-one coverage needs an explicit
  witness.
Falsifier: count-only equality, dict overwrite, or selected-case-only proof.

### E8 partition / cold restore / permutation

Partitioning F by any deterministic stable key, concatenating partitions,
restoring from serialized state, and permuting physical source rows must
produce the same exact logical identity multiset and the same disjoint
disposition partition. Pending/held/unknown/unsupported sets must survive
restore with exact IDs. Falsifier: order-dependent frontier, partition loss,
or cold replay changing identities/states.

### E9 axes

Eligibility `{ELIGIBLE,PROHIBITED,INAPPLICABLE_PROVED,HELD,UNKNOWN}`,
execution `{NOT_STARTED,PENDING,COMPLETED,UNSUPPORTED_RUNTIME,ERROR}`, result
`{SUPPORTED,OBSERVED_ZERO,VALID_NULL,DIFFUSE,VALID_EMPTY,ZERO_SUPPORT,
UNSUPPORTED,UNKNOWN}` remain separate. Conservation:
considered = eligible + prohibited + proven-inapplicable + held/unknown;
eligible = adequate-completed + pending + unsupported-runtime + errored.
Falsifier: one conflated enum, dropped state, or runtime failure rewriting
eligibility.

### E10 native lowering against current installed contracts

Lowering must use the actual current installed C11/I03/I05/Batch/catalog
contracts, not infer capability absence from a historical/None `native_map`
branch. For each eligible supported shape (bool, int, null-typed condition,
ordered/n-ary target, directed/role-specific, conditioned) a LoweringRecord must
bind operation ref, exact predicate/query/DiscoveryAuthority refs, expected
candidate/query-role keys, unit refs, lowering version, typed refusal and
evidence-grade ceiling. Target must be target, conditioner must be
conditioner; query role and direction must match. Unsupported shapes stay
scientific obligations typed `UNSUPPORTED_RUNTIME`, never disappear.
Seven selected mapping proofs may establish those mappings only; they do not
establish full native R03 execution or original science.

## C. Commission-boundary expectations

- Write only `WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/`; candidate
  code/tests untouched; own fixtures/mutants below that root.
- Original data/credentials/external home/provider changes/extra sessions are
  out of bounds; TEST_ONLY synthetic fixtures only.
- Author report counts and its own JUnit are self-report until independently
  replayed with the actual imports.
- Verdict is finite `ACCEPT_SCOPED_LOCAL` (with explicit NOT_REACHED edges) or
  `REVISE` (with minimal reproducible exact inputs and contract links).
- No repair, adoption, source/science, production, N11/N12, J52/W52 claims.

## D. Verdict rule frozen in advance

`ACCEPT_SCOPED_LOCAL` only if: (i) exact startup/tree/allowlist/manifest
checks pass; (ii) author suite replays green under own JUnit with actual
imports; (iii) independent E1-E8 probes match the hand oracle (or any declared
deviation is contract-lawful and explicit); (iv) E9 conservation holds;
(v) E10 semantic lowering is correct for actual eligible supported shapes and
unsupported stays typed/held; (vi) no blocking defect for R03 start. Otherwise
`REVISE`. Native execution ceiling and NOT_REACHED edges must be stated.
