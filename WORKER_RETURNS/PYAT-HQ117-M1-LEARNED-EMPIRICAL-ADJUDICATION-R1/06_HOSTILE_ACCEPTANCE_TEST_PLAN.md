# M1 HOSTILE ACCEPTANCE TEST PLAN R1

A future implementation must pass these source-free hostile tests before any production use.

| ID | Attack | Fixture | Required result |
|---|---|---|---|
| H01 | provenance self-authorizes | valid hashes, full replay, rich provenance, supported facts, no M1 family-rule binding | `BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY` |
| H02 | support self-authorizes | `EVALUATED_SUPPORTED` + positive support, no substantive rule | blocked; no semantic claim |
| H03 | I05 rule-id escalation | receipt carries family/rule/validation material; no separately competent M1 binding | blocked |
| H04 | latest-wins | two validator authorities, newer timestamp/version on one, no explicit current selection | ambiguous/block; never pick newer |
| H05 | default fallback | requested family has no exact validator; generic default exists | blocked; default never invoked |
| H06 | family mismatch | T/family A binding points at validator for family B | integrity/block |
| H07 | scope mismatch | correct rule identity but wrong source universe/risk/measure/time scope | blocked/out-of-scope |
| H08 | observed-zero collapse | denominator > 0, numerator 0 | preserve `OBSERVED_ZERO`; no automatic reject/valid-empty |
| H09 | zero-support collapse | denominator 0 | preserve `ZERO_SUPPORT`; never become observed zero |
| H10 | valid-empty laundering | valid-empty discovery receipt | preserve `VALID_EMPTY`; no positive/negative truth unless exact rule explicitly governs emptiness |
| H11 | noncomparability laundering | rule requires comparability; exact state NONCOMPARABLE | abstain/block; no no-difference/negative claim |
| H12 | coverage overclaim | nonexhaustive/coverage-limited input used for global absence claim | block stronger claim; retain bounded coverage |
| H13 | missing measurement portability | validator declares portability required; neighboring semantic/source relation exists but no portability authority | blocked |
| H14 | pooling/composition widening | sample-pooling authority supplied where measurement-equivalence authority is required | blocked |
| H15 | rule authority denied | exact binding names authority whose current scoped decision is DENY | blocked; denial preserved |
| H16 | rule authority conflict | two explicit applicable authorities conflict and no governed resolution | unresolved/block |
| H17 | replay substitution | exact historical replay attempted, newer validator available | replay pinned historical validator; no substitution |
| H18 | replay mismatch | same declared inputs produce mismatched projection/hash | `INTEGRITY_FAILURE` |
| H19 | same members role swap | family proposition uses same members with changed constitutive role mapping | different proposition identity or fail; never same by member set |
| H20 | authority recertification identity | same P1 claim, new competent authority instance | new M1 disposition identity may result while semantic claim identity remains same |
| H21 | reject becomes negative truth | family rule returns NOT_SATISFIED with no negative-claim constructor | no negative semantic claim identity |
| H22 | block becomes false | missing authority/blocker | `BLOCKED`; no negative truth |
| H23 | FF02 candidate promotion | pending/candidate FF02 rule supplied without competent current adoption/binding | blocked |
| H24 | C07 architecture promotion | C07 learned-world DAG used as validation rule | blocked; architecture precedent is not rule authority |
| H25 | I04 cross-jurisdiction promotion | structural-admission authority supplied as M1 validator authority absent explicit M1 family binding | blocked |
| H26 | diagnostic promotion | MI/NMI/etc diagnostic supplied in place of EmpiricalFact | integrity/semantic-collapse failure |
| H27 | semantic-ceiling breach | validator result tries causal/person/V3 or structural claim above its ceiling | block/fail |
| H28 | release side effect | validator asks wrapper to publish/release product | reject side effect; M1 output only |
| H29 | currentness side effect | validator asks M1 to select current product | reject side effect; M3 jurisdiction |
| H30 | structural side effect | validator asks M1 to mint structural admission | reject side effect; I04/Field Forge jurisdiction |

## Decisive acceptance proof

H01 is mandatory and dispositive.

If a future M1 implementation can produce `RULE_SATISFIED` in H01, it has collapsed evidence sufficiency into semantic authority and fails this constitution.

The implementation test suite must also demonstrate that H08/H09/H10 produce three distinguishable serialized outputs with distinct conserved evidence states.
