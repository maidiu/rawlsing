# R51 actual native join execution and mutation

## Baseline joined positive

- G50 operation: `urn:g50:op:b547e734c8fda66149098b314f5037aaa7325740f450ffc939f0a55e9249ffef`
- Class/target: `DIST` / `q301_2`; no conditions.
- B49 fixture: `R51-b547e734c8fd`, target `q301_2`, response `1`.
- B49 native consumer: `PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`; Batch `COMPLETED`.
- Fact: `EmpiricalFact@1.0.0` `245098cf814e67594c60120226cfea5591f160c25379254b0b155fcb9c9c6911`.
- Numerator/denominator: **1/1**; source synthetic row S1 has q301_2=1, q301_7=2.
- `ADP019_ADMISSION_RECEIPT_ABSENT`; `e2_performed=False`; no native actor.

## Source-value mutation (same consumer)

Rows changed from q301_2 `(1,3,5)` to `(1,1,5)`; q301_7 unchanged. The same G50 operation and same B49/I03 consumer yield:

| | baseline | mutated |
|---|---:|---:|
| B49 fact | `245098cf…` | `e3e7799b…` |
| numerator | 1 | 2 |
| denominator | 1 | 2 |
| G50 op ID | same | same |
| E_pre root | `1a9bffbe…` | `1a9bffbe…` |

The source value changes the actual downstream fact and support counts; it does not rewrite E_pre membership.

## Frozen-method/policy mutation

Removing `q301_2` from G50 `target_roles` removes the operation: no `DIST q301_2` eligible entry remains. The baseline positive cannot execute under the mutated policy. Restoring the policy gives the same baseline GREEN fact. The test is `test_policy_mutation_removes_the_eligible_native_operation_and_restores`.

## Typed native gaps

- G50 `JOINT q301_2 × q301_7` is eligible but `lower_to_b49` raises `B49_ONE_TARGET_ADAPTER_UNSUPPORTED`; no flattening.
- G50 `CONDITIONAL` operations are similarly unsupported by the one-target B49 fixture.
- G50 `native_i05` (15 candidates/11 rules, 13/13 tests) is separately executed but not joined to B49 U43; the I05 source is G50 synthetic. `R51_I05_NATIVE_JOIN_HOLD`.
- B49 `OperationFixture` is the only real U43 adapter exercised; a genuine pair/joint adapter is the next engineering edge.
- E04/P41/A42 terminal consumer not used; I03/Batch fact is the actual consumer. `E04_TERMINAL_HOLD`.

## Cold/replay

- `r51_native.xml` 10/10; `r51_post_witness.xml` 10/10; `r51_cold_0.xml` 10/10; `r51_cold_1.xml` 10/10.
- Proof witness 5/5 `BOUNDED_MUTATION_DETECTED`; see `evidence/proof_witness_receipt.json`.
- No raw source, no original U/Epre, no N11/N12.
