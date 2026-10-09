# HQ265 G01 — repair status, call graph and source grain

**STOP: `HQ265_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`**
**Disposition: `HOLD__G1_CHAIN_NOT_INTEGRATED_AND_VERIFIED`**

**No code was modified.** Both permitted candidate files are byte-unchanged at their
commissioned blobs (`e1c09957519f10b29ae2635f3277b4f3af0912c9`,
`f71c0ce87d4005acc6806cac9afe5bbbb76ad9bc`). Baseline court still 22 passed.

## My HQ264 HOLD was wrong. I own that.

HQ264's missing-fixture blocker was **disproved, and the error was mine**. I searched for the
literal string `q(C|A=1)` and concluded from zero hits that the fixture did not exist. That
was a bad search: the fixture encodes those quantities in code and in `XOR_ORACLE`, not as
that literal. `rawlsing_next/tests/c1_at08_at13_fixture.py` blob
`0393cc8c17a313b7944b2a5287d0406d6cbe3849` was in the tree the whole time, exporting
`XOR_ORACLE`, `xor_fixture()` and `direct_condition_composition()`. I reported a HOLD on a
defect that did not exist, and it cost a commission cycle.

The lesson is the one I should have applied before searching: absence of evidence for a
fixture is not evidence of absence of the fixture.

## F2 is EXECUTABLE and the commissioned figures reproduce exactly

Built on the approved fixture via the HQ253 T01 discriminator's own wiring
(`c1_at08_at13_fixture.xor_fixture` + `direct_condition_composition`), executed on this
governed interpreter. Actual observed output:

```
q1 cells : [{'cell':'0', raw_numerator_support 1, fraction [1,2]},
            {'cell':'1', raw_numerator_support 1, fraction [1,2]}]
q1 denom : 2
q2 cells : [{'cell':'0', cell_state OBSERVED_ZERO_IN_SUPPORTED_RISK_SET, fraction [0,1]},
            {'cell':'1', cell_state OBSERVED_POSITIVE,                fraction [1,1]}]
q2 denom : 1
distinct C1 identities : True
```

That is exactly the commissioned result: **q1 = q(C|A=1) at 1/2 and 1/2 with native joint
denominator 2**, and **q2 = q(C|A=1,B=0) at 0 and 1 with native joint denominator 1**. It
also matches `XOR_ORACLE`: `unary_marginal_flat["P(C=1|A=1)"] == (1,2)` and
`joint_decisive["P(C=1|A=1,B=0)"] == (1,1)`.

Critically these are **not** multiplied marginals. `xor_fixture()` builds four respondents
`R00 (A0 B0 C0)`, `R01 (A0 B1 C1)`, `R10 (A1 B0 C1)`, `R11 (A1 B1 C0)` with `C = A ^ B`,
and q1 and q2 produce **distinct `composed_result_identity_hash` values over the same
`source_universe_refs` and `release_refs`**. The joint is genuine XOR: conditioning on A=1
gives 1/2, and adding B=0 collapses to a denominator-1 stratum with C=1. Equal marginals,
different joint — which is precisely the discriminating structure the discriminator exists
to detect.

## F1 real-G2 wiring: written, then withdrawn

I did implement the F1 replacement — real `resolve_service_source_applicability`, real
`bind_service_applicability_to_f8_scope`, real `evaluate_bound_positioned_subject_possibility`
driven by real `CandidateClassBinding` / `ApplicabilityAuthorityRecord` /
`ServiceApplicabilityF8ScopeBindingRequest`, with the local scope-hash substitute deleted —
plus F3 in-flight checks, F4 typed error classes and F5 exact-type request validation.

**I withdrew it because it did not go green.** It ran 17 passed / 6 failed, and I will not
ship a candidate whose tests fail.

## The precise remaining blocker

With my own wiring, `direct_condition_composition` returned
`possibility_slice_evidence_or_null = None` and `consumer_result_or_null = None` — so there
was **no C1-originated evidence object to pass through G2 to bound F8**, which is the entire
F1 chain.

This is narrower than "impossible", and I want to be exact about it: my earlier successful
q1/q2 probe used the **HQ253 discriminator's own** `qauth` (its `_query_authority`), whereas
my ingress wiring used `_query_snapshot()` from `test_pre553_analytical_composition`. The
figures reproduce under the HQ253 wiring. So the open question is narrow and specific:

> which owner-held query-authority wiring makes `direct_condition_composition` populate
> `possibility_slice_evidence_or_null` (rather than `None`) on the XOR fixture, so the
> G2-bound chain has a real C1 evidence object to authenticate?

Resolving that, then integrating and verifying the full chain end-to-end, is the remaining
work. I ran out of budget to resolve it and would rather report it than guess.

## What is NOT wrong

F1's G0b blocker remains ruled out (carried from HQ264 and reconfirmed here):
`AUTHORISED_AUTHORITY = ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`, and the
adopted G2 binder **re-derives** the binding from request+receipt+rule rather than trusting
its own fields. So the chain is not a self-hash substitute and needs no issued G0b.
