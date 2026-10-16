# PYAT R17 GF1 — GENERIC NATIVE PAIR RELATION + FIRST REAL CONSUMER

## Verdict

# `GENERIC_NATIVE_PAIR_RELATION_CANDIDATE_TEST_ONLY__GENERIC_NATIVE_SEMANTICS_HOLD_RETAINED__REQUIRES_SEPARATE_INDEPENDENT_GF1_REVIEWER`

A **genuinely new generic two-binary-item PAIR relation owner** and a **named
downstream consumer that physically reads it** were built and executed against the
**real accepted native chain**. This is not a fourth DTO and not a re-serialized
PV3H proposal.

**`GENERIC_NATIVE_SEMANTICS_HOLD` is RETAINED.** No competent
`FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER` has issued a generic native
contract, and nothing here may be adopted publicly.

**44/44** frozen-expectation tests pass. **6 real P01 durable
`UnitExecutionReceipt`s per profile** across 3 profiles.

---

## 1. The gap, and why it was real

The accepted Field Forge semantic owner hardcodes:

```
CONDITIONER_SOURCE_NATIVE_VARIABLE = "Q86B"
TARGET_SOURCE_NATIVE_VARIABLE     = "Q86A"
RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
```

and rejects any other target-domain identity. **That is a semantic
specialisation, not a data limitation.** The accepted native I03 query already
carries generic source-native identities —
`urn:test:i03:question_native:m01-X` and `...-m01-Y`.

So the smallest honest move was a **separately named candidate owner** that
consumes the *same* real `EmpiricalFact`/`EmpiricalQuerySpec` objects but derives
each role from the **actual native query**, never from a hardcoded label.

**Proof it is genuinely generic, not renamed GT2** (`evidence/02_*.json`):

| Check | Result |
|---|---|
| generic relation material == accepted specialized material | **False in every consumer, every profile** |
| accepted specialized output == its declared original material | **True in every consumer, every profile** |
| accepted `field_forge_conditional_support.py` Git blob | `a70decb20747d84cbcbe27d1280babc6de88ef33`, unmodified |

And the role binding genuinely follows the source:

| Original slot | native component order | generic declares |
|---|---|---|
| `PAIR` | `[m01-X, m01-Y]` | CONDITIONER=`m01-X`, TARGET=`m01-Y` |
| `B` | `[m01-Y, m01-X]` | CONDITIONER=`m01-Y`, TARGET=`m01-X` |

A fixed-label owner could not do that. The accepted owner reports `Q86A`/`Q86B`
for both.

---

## 2. What was physically executed

Real, unmodified, staged byte-exact:

1. `validate_c11_source_release` / `ingest_c11_source_release` (accepted C11)
2. `execute_empirical_query` (I03)
3. `execute_exact_bounded_discovery` (I05)
4. `pre553_batch_runner.UnitExecutionReceipt` — **6 durable P01 receipts per profile**
5. `produce_exact_conditional_support_profile` — the **accepted specialized GT2
   relation, used unmodified as the independent comparator**

Then the **new** GF1 candidate:

6. `generic_native_pair_relation.produce_generic_native_pair_relation`
7. `gf1_pair_support_consumer.compute_pair_support_signature`

**Staging custody:** all **74** pinned native files were staged, then
**re-attested from the ORIGINAL PV3 `source_selector.json`** after running PV3's
own `repro/stage.py` untouched — Git blob SHA-1 (NUL preimage) + sha256 + byte
count, **74/74, 0 mismatches**. 29/29 PV3 court files verified. Per PV3N's §6 I
reused PV3N's qualified frozen evidence rather than re-running all 74 owner
regressions.

---

## 3. The named consumer is not a copy

`GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0` reads the relation object
(verified by its `object_id`/`content_hash`) and emits values that **do not exist
anywhere in the relation**:

- `separation_class` — `EXACT_PAIR_SEPARATION` / `NO_PAIR_SEPARATION` /
  `UNDETERMINED_NO_ELIGIBLE_RISK` / `UNDETERMINED_ZERO_SUPPORT_RISK`
- `support_vectors`, `zero_cell_semantics`, `joint_support_total`,
  `condition_states_with_positive_denominator`, `result_hash`

The test asserts each consumer field is **absent** from the relation material —
a copy would fail immediately (falsifier F2).

Observed downstream values:

| profile | separation classes observed |
|---|---|
| BASELINE | `EXACT_PAIR_SEPARATION`, `UNDETERMINED_NO_ELIGIBLE_RISK` (DISCOVERY) |
| R2_Y1 | + `NO_PAIR_SEPARATION` |
| R1_Y0 | + `NO_PAIR_SEPARATION` |

**The consumer is a value-bearing decision function, not a report.** It makes no
personhood, dyad, peer-trait, weighting or causal claim, and says so in its own
output.

---

## 4. Baseline matched the frozen oracle exactly

`01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json` was committed at `686b1dae`
**before any generic candidate code existed**.

| | frozen | executed |
|---|---|---|
| ordered XY cells `00,01,10,11` | `1,0,0,1` | `1,0,0,1` ✓ |
| conditional profile | `{0:(1,{0:1,1:0}), 1:(1,{0:0,1:1})}` | identical ✓ |
| per-condition positive denominator | `1` | `1` ✓ |
| eligible joint risk (R1+R2) | — | `2` ✓ |
| zero cells | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`, never `ZERO_SUPPORT` | ✓ |
| R3 (Y-ineligible) | never becomes a zero | ✓ |

### 4.1 Two honest clarifications of my own frozen oracle

**(a) `expected_positive_denominator = 1` is the PER-CONDITION denominator, not
the total joint risk.** I read it initially as a total. The native producer
reports `condition_denominator_support = 1` per row while the total joint
eligible risk is `2` (R1+R2). Both are now asserted separately so the two readings
can never be confused. **I did not edit the frozen oracle.**

**(b) The intervention is applied to ONE original source (A), and the two
consumers of source B correctly do not move.** The commission requires exactly
this. Under each intervention exactly 2 of the 4 QUERY-path consumers change and
2 remain at baseline. My earlier draft wrongly expected *all* consumers to move;
the correct behaviour is what the frozen oracle's `interventions.B` clause states
("all source/fact/relation/current material bitwise stable").

The frozen oracle intervention cell set is reached by a native consumer under
each intervention.

---

## 5. Interventions and independence

| profile | changed consumers | frozen oracle cell set reached | separation class |
|---|---|---|---|
| BASELINE | — | `1,0,0,1` | `EXACT_PAIR_SEPARATION` |
| R2 first-item up | 2 of 4 | `0,1,0,1` ✓ | `NO_PAIR_SEPARATION` |
| R1 first-item down | 2 of 4 | `1,0,1,0` ✓ | `NO_PAIR_SEPARATION` |

**F4 (independence) held:** the two consumers of the independent source keep
their exact baseline cell counts, eligible risk `2`, and
`relation_permission_ceiling = ("SOURCE_FREE_DEV",)` under every A intervention.

The other changed consumer legitimately falls to
`UNDETERMINED_NO_ELIGIBLE_RISK`, because one conditioner state has no eligible
respondent left — which is the honest reading, not a bug.

---

## 6. Hostiles executed

All pass. Highlights:

- foreign expected root and foreign register root refuse at the installed owner
- fact content mutation refuses (`semantic identity mismatch`)
- **re-hashed** structural forgeries still refuse: incomplete native domain,
  inconsistent zero cell state, negative support, weighted numerator, nonbinary
  category, domain-identity mismatch — the candidate's own validation refuses,
  not just a hash check
- target/conditioner swap refuses `REVERSE_PAIR_GRANT_REQUIRED`; unknown grant
  refuses; the **authorized reverse operation succeeds only under its own
  separate grant** and yields a distinct relation object
- non-native role ref, permission widening ref, tampered relation object refuses
- deterministic replay binds content

## 7. Custody preserved

- **8 operations unchanged: 6 RUNNABLE + 2 ORDERED HELD**, both HELDs still
  `ORDERED_OWNER_NOT_ISSUED`.
- The **original raw failing generic-label assertion is untouched** — not
  xfailed, skipped, relabeled or suppressed.
- The accepted specialized GT2 owner, its risk, its consumer outputs and its
  relation identity are **unmodified**.

## 8. Not claimed

No original SAV/DTA mutation. No original U/E_pre issuance. No canonical Field
Forge change. No all-35 acceptance. No N11/N12. No V3 operation. No actor/person
work. No public adoption of generic semantics. No dependency on any unaccepted
prior branch. **No separate independent GF1 reviewer has run — this worker
cannot accept its own method.**

## 9. Exact minimum competent-owner signature still required

A real `FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER` must separately issue,
at minimum: the **generic relation family identity**; the **authorized role
binding** for CONDITIONER/TARGET including the reverse operation's separate
grant; the **source-native response domain** and its missingness rules; the
**risk/universe** admissibility; the **producer/relation permission ceilings**;
the **instrument/release/form/administration/language/occurrence/respondent
grain**; and the **consumer contract**. Until then the candidate is TEST_ONLY and
`GENERIC_NATIVE_SEMANTICS_HOLD` stands.

See `04_FIELD_FORGE_GENERIC_SEMANTIC_OWNER_WARRANT.md`.

## 10. Reproduction

```
cd WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/repro
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_gf1_generic_pair.py -q
```
Python 3.11.3, pytest 9.0.2, git 2.43.0. **44 passed.**
JUnit: `junit/gf1_generic_pair.xml`. Evidence: `evidence/`.