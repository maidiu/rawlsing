# PYAT HQ273 C01 — Actual native I03 call graph and source-free fixture grain

**Commission:** `PYAT-HQ273-C01-TRUE-I03-CONDITIONED-DENOMINATORS-SOURCE-FREE-EXECUTABLE-COURT-R1`
**Commission file:** `WORKER_COMMISSIONS/PYAT-HQ273-C01-.../00_COMMISSION.md`
**EXACT COMMISSION TIP:** `6e9e1ddb766861da273aa75c7b692547506acc25` (= exact working HEAD used)
**EXACT CONTROL BASE:** `e82508091214d2543cfd1a2d8f7ff5ea4b5fe48f`
**BRANCH:** `agent/step5-pyat-hq273-c01-source-free-true-conditional-owner-court-r1`
**MODEL / INTELLIGENCE:** **Step 5 Preview** (as commissioned). No mid-task switch occurred in this
execution; no earlier model identity is claimed. Model identity remains uncertifiable from
repository state and must not be quoted from this document as a certified fact.
**MACHINE:** MacBookPro15,1 (Intel Core i9-9880H), macOS 13.2.1 build 22D68.
**WORKTREE:** `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hq273/c01`
(git worktree of `/Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository`).
**INTERPRETER:** `/usr/local/bin/python3`, CPython 3.11.3, pytest 9.0.2, pluggy 1.6.0.
**No original SAV/DTA, no LiTS checkpoint, no source file of any kind was opened, read or hashed.**

## 0. Sealed HQ273 resolved

Worktree detached HEAD `6e9e1ddb7` == the exact commission tip. Frozen control base
`e82508091` present as HEAD~1. Sealed adjudication read on
`origin/integration/staging-pyat-hq273-r01-f02-intake-conditional-and-structural-science-r1`
(`df4e28b1`, decision `HQD-2026-10-09-273`), plus the HQ272 R01 hostile review it rests on
(`agent/reviewer-pyat-hq272-r01-afro-gt3-true-conditional-hostile-r1 @ 0c2730d5…`, documents
`01_TRUE_CONDITIONAL_RISK_SET_AND_OWNER_OPERATOR_COURT.md` and
`02_HETEROGENEOUS_ALTERNATIVE_AND_MINIMUM_EXECUTABLE_AUTHORITY.md`).

The sealed finding this court answers, verbatim in substance:

> the frozen `wave1_gt12_i03_positive_facts.py` `_predicate_for_members` is **only**
> `DERIVED_BRANCH_COHORT`, not value equality; the arity-polymorphic target tuple is **only a
> joint cell tensor**. Existing same-respondent target-tuple *capacity* is affirmative, but
> `q(Y|A) → q(Y|A,B)` source-backed positive product is **NOT DEMONSTRATED**.

This court demonstrates, source-free, that the **generic engine underneath that wrapper does
support genuine conditioned denominators**, and it names the exact missing edge.

---

## 1. The actual call graph (no parallel API, no counting stub)

```
two_nested_true_conditional_facts(source, qauth)          [tests/hq273_c01_true_conditional_fixture.py]
  ├─ common_case_base_ast(source)                -> AND(routing(ELIGIBLE){Y,A,B},
  │                                                  typed-response(SUBSTANTIVE){Y,A,B})
  ├─ p1_ast = AND(base, SURVEY_RESPONSE_EVENT(A EQ "0"))
  ├─ p2_ast = AND(base, SURVEY_RESPONSE_EVENT(A EQ "0"), SURVEY_RESPONSE_EVENT(B EQ "0"))
  ├─ true_conditional_predicate(...)             -> make_empirical_predicate(...)   [owner-native]
  ├─ true_conditional_query(...)                 -> EmpiricalQuerySpec@1.0.0        [owner-native]
  └─ run_true_conditional(source, pred, query)
        └─ pre553_empirical_query.execute_empirical_query(...)      <-- THE ACCEPTED PUBLIC EXECUTOR
              ├─ _verify_public_identity(query) / (predicate)
              ├─ _require_exact_i03_authority_fitness(...)
              │     ├─ grammar_ref ∈ query_authority_refs
              │     ├─ PREDICATE_GRAMMAR / operation / 3 families / universe scope
              │     └─ TARGET_USE_PERMISSION ref + authority + operation bonded together
              ├─ _parse_target_plan(query, registry)                [_pre553_query_common.py]
              ├─ _resolve_release_indices(repository, ...)
              └─ _evaluate_index_group(indices, ...)                [_pre553_query_eval.py:318]
                    ├─ _build_release_index(release, universe)      [_pre553_query_predicate.py:19]
                    ├─ per respondent: _routing_fact_for(...) -> per-target routing state
                    ├─ _risk_membership(per_target_states, profile) -> risk_members
                    ├─ _eval_predicate(predicate.predicate_ast, ...) [_pre553_query_predicate.py:366]
                    │     └─ _leaf_match(...)  [same file:119]
                    │           ├─ SURVEY_RESPONSE_EVENT EQ      (line 225)
                    │           ├─ TYPED_RESPONSE_STATE          (line 273)
                    │           ├─ ROUTING_APPLICABILITY_STATE   (line 253)
                    │           └─ EMPIRICAL_POSITION_COORDINATE (line 137)
                    ├─ if predicate passes  -> denominator_members.append(respondent.ref)   <-- line 417
                    ├─ _target_configuration(...) -> raw_cells
                    └─ returns _Evaluation(fact_state, denominator_members, raw_cells, ...)
              └─ _build_fact(...) -> EmpiricalFact@1.0.0            [_pre553_query_eval.py:552]
```

Two calls to the accepted executor with two different predicates produce **two different
`EmpiricalFact` objects**. There is no independent counting code anywhere; the only "oracle"
in the return is a separate set-logic function used purely to check the engine's answer, and
it is asserted to share no engine code (`test_independent_oracle_shares_no_engine_code`).

### The decisive existing code, cited

| Behavior | Location |
|---|---|
| Only predicate-passing respondents enter the denominator | `rawlsing_next/_pre553_query_eval.py:417` (`denominator_members.append(respondent.ref)` after `if not condition: continue`) |
| `raw_denominator = len(denominator_members)` — condition-specific, not collection size | `rawlsing_next/_pre553_query_eval.py:452-453` |
| Per-scoped-respondent respondent-wise `AND` evaluation | `rawlsing_next/_pre553_query_predicate.py:393-403` |
| Native `SURVEY_RESPONSE_EVENT` EQ leaf | `rawlsing_next/_pre553_query_predicate.py:225-251` |
| Native `TYPED_RESPONSE_STATE` leaf | `rawlsing_next/_pre553_query_predicate.py:273-292` |
| Native `ROUTING_APPLICABILITY_STATE` leaf | `rawlsing_next/_pre553_query_predicate.py:253-271` |
| `EmpiricalPredicate@1.0.0` required fields | `rawlsing_next/pre553_empirical_objects.py:631-640` |
| `EmpiricalQuerySpec@1.0.0` required fields (arity-polymorphic) | `rawlsing_next/pre553_empirical_objects.py:677-685` |
| `EmpiricalFact@1.0.0` required fields + numerator≤denominator invariant | `rawlsing_next/pre553_empirical_objects.py:696-719` |
| ZERO_SUPPORT / OBSERVED_ZERO / VALID_EMPTY / UNRESOLVED typing | `rawlsing_next/_pre553_query_eval.py:455-476` |
| Deterministic replay identity | `rawlsing_next/pre553_empirical_query.py:542-565` |

---

## 2. The source-free fixture grain

**Ten respondents**, one synthetic sealed C11 release, three **distinct** scalar questions with
generic labels `Y`, `A`, `B`. Every authority snapshot and every exact ref is fixture-intrinsic
under `urn:test:hq273-c01:...`; every authority id is prefixed `HQ273-C01-AUTH-`; the universe
declares `raw_source_identity=HQ273-C01-RAW-…`, `country_geography=FIXTURE-ONLY`,
`sampling_design_regime=SYNTHETIC-FIXTURE-NO-INFERENCE`, and the query grain carries
`fixture_marker=DEVELOPMENT_FIXTURE_ONLY`. **No real Afrobarometer item, question
implementation, risk set or target-use permission is named, bound or forged.**

Each respondent has exactly one `RespondentEvent` per question, with **typed state and stored
native code kept independent**:

| Id | Y | A | B | role in the court |
|---|---|---|---|---|
| P01 | 1 | 0 | 0 | in S, R1, R2, Y=1 |
| P02 | 0 | 0 | 0 | in S, R1, R2, Y=0 |
| P03 | 1 | 0 | 1 | in S, R1 only |
| P04 | 1 | 0 | 1 | in S, R1 only |
| P05 | 0 | 0 | 0 | in S, R1, R2, Y=0 |
| P06 | 1 | 1 | 0 | in S only (A=1) |
| P07 | 0 | 1 | 1 | in S only (A=1) |
| P08 | 1 | 0 | DK (9) | **excluded**: B non-substantive |
| P09 | DK (9) | 0 | 0 | **excluded**: Y non-substantive |
| P10 | 1 | REFUSAL, stored value "0" | 0 | **excluded**: A non-substantive — and a real coercion hazard |

P10 is the deliberate hazard: its `A` event is typed `REFUSAL` but its stored native value is
the substantive bucket `"0"`, exactly what a naive recode of a refusal code into a "No" column
produces. It must not enter either denominator.

### Predicates (owner-native grammar only)

`S` (declared complete-case scope) =
`AND( ROUTING_APPLICABILITY_STATE(Y, ELIGIBLE_APPLICABLE), …(A…), …(B…),
      TYPED_RESPONSE_STATE(Y, SUBSTANTIVE_RESPONSE), …(A…), …(B…) )`

```
P1 = AND( S, SURVEY_RESPONSE_EVENT(A, EQ, "0") )                       -> q(Y | A=0)
P2 = AND( S, SURVEY_RESPONSE_EVENT(A, EQ, "0"),
             SURVEY_RESPONSE_EVENT(B, EQ, "0") )                       -> q(Y | A=0, B=0)
```

Both predicates carry `same_respondent_binding_semantics = "EXACT_SCOPED_RESPONDENT"`,
`grammar_authority_ref` = the fixture `PREDICATE_GRAMMAR` snapshot, and
`typed_state = "PREDICATE_RESOLVED_AUTHORIZED"`. Each query is **unary** on `Y` with
`risk_set_type = "WHOLE_QUESTION_RISK_SET"`, `measure_kind = "RAW"`, unweighted,
`UNCERTAINTY_UNQUANTIFIED`, and is bound to an exact fixture `TARGET_USE_PERMISSION`
(ref + authority + operation bonded together in `requested_output_grain`).

---

## 3. Result (full numbers in `01_INDEPENDENT_TWO_CONDITIONAL_FACT_EXECUTION.json`)

| | q1 = q(Y\|A=0) | q2 = q(Y\|A=0,B=0) |
|---|---|---|
| typed state | `SUPPORTED` | `SUPPORTED` |
| `raw_denominator_support` | **5** | **3** |
| Y=1 cell numerator | **3** | **1** |
| Y=0 cell numerator | 2 | 2 |
| `raw_resolved_target_support` | 5 | 3 |
| `denominator_member_refs` | P01,P02,P03,P04,P05 | P01,P02,P05 |
| risk-set (Y-routed eligible) | 10 respondents | 10 respondents |
| replay verified identical fact ref | yes | yes |

Independently recomputed oracle: `S = {P01…P07}` (7), `R1` (5), `R2` (3), `K1` (3), `K2` (1),
`q1 = 3/5`, `q2 = 1/3`. **R2 ⊆ R1 ⊆ S**, and every number agrees with the engine.

R2 (3) ⊊ R1 (5) ⊊ S (7) ⊊ routed-eligible (10): four distinct closure sizes, each one
predicate-defined. `N1 ≠ N2` was chosen deliberately and `q1 ≠ q2` visibly.

---

## 4. Precise engine semantic that the return must not blur

For a fully resolved **unary** target, `EmpiricalFact.raw_numerator_support` is the
**resolved-target support** (`_evaluate_index_group`'s `raw_resolved`), which equals the
denominator when every member resolves. It is **not** the Y=1 cell count. The per-value
numerator lives in
`fact.target_topology["complete_cell_semantic_projection"][cell]["raw_numerator_support"]`.
The accepted frontier fixtures read it exactly this way
(`rawlsing_next/tests/pre553_query_frontier_fixtures.py:135-136`:
`_rate(fact) → _cell_map(fact)["1"]["raw_numerator_support"], fact.raw_denominator_support`).

Reporting `raw_numerator_support` as "the numerator of Y=1" would silently turn a denominator
into a numerator. This return reports both, labelled.

---

## 5. Findings for HQ beyond the commissioned demonstration

**F-1 (operator rule, not an engine defect).** The native `SURVEY_RESPONSE_EVENT` `EQ` leaf at
`_pre553_query_predicate.py:240-251` has **no typed-state filter**. It compares
`canonicalize(_semantic_value(event))` against the declared values regardless of
`event.typed_state`. A predicate that omits the `TYPED_RESPONSE_STATE` validity policy therefore
admits typed-`REFUSAL`/`DK` respondents purely on value equality. In this fixture that inflates
the denominator from 5 to 8 and admits P08/P09/P10 including a refusal recoded to `"0"`.
Because P09 cannot resolve a `Y` cell, the resulting fact is typed **UNRESOLVED**
("positive denominator exists but exact target configuration is unresolved for one or more
denominator members") rather than silently numeric — i.e. the engine fails *closed* on this
path, but only because the target cell could not resolve. **Any production conditional predicate
must therefore carry explicit `TYPED_RESPONSE_STATE` validity leaves; value equality is never a
substitute for a declared validity policy.**

**F-2 (the frozen GT12 hazard is reproducible, source-free).** Building both q1 and q2 with a
`DERIVED_BRANCH_COHORT`-only predicate — the exact shape of
`wave1_gt12_i03_positive_facts.py::_predicate_for_members` — yields **one** denominator of 10
and **identical** member sets for both. This is the HQ272 R01 FAIL matrix row
("Query uses only `_predicate_for_members` for both q1/q2 and yet declares conditional
denominators") reproduced as a green, committed regression.

**F-3 (a joint tensor is provably not a substitute).** An arity-3 query over the same predicate
yields denominator **7** — the whole complete-case base `S` — with 8 domain cells. It is neither
5 nor 3. Possessing a tuple of three ordered targets does not by itself perform the
conditioning.

**F-4 (routing never coerces).** An unresolved routing state (`ROUTING_UNKNOWN`) is refused as
`UNAVAILABLE` / `RISK_SET_UNAVAILABLE` with zero denominator and empty member refs; absence is
never converted to non-membership (`_pre553_query_eval.py:92-98`).

**F-5 (identity gates bite).** A non-`PREDICATE_GRAMMAR` query authority, a foreign release ref,
and a target-use permission governing a different operation each fail closed with zero
denominator. An extra forged snapshot present in the registry but not named by the query does not
license a fact.

---

## 6. What this is explicitly NOT

`DEVELOPMENT_FIXTURE_ONLY`. This is **not** a factual R5 source row, **not** an I03 source
release or source-use permission, **not** a C1 selected-service join, **not** T1/T2/G0b, **not**
a source-backed true conditional, **not** an adopted GT3, and **not** an FF02/structural result.
The source-free fixture demonstrates engine competence only; it says nothing about what the R5
source can support.

**Terminal:** `HQ273_C01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`
