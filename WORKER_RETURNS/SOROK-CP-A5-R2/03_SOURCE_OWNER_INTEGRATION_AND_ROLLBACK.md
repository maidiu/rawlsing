# Source-owner integration and rollback

## 1. What is preserved

The candidate copies I1's complete guarded product and tests:

- `bp2p4/i1_product.py` (`GuardedJoinedProduct`);
- `bp2p4/product.py`, `bp2p4/assertion.py`, `bp2p4/severance.py`;
- `bp2p4/c12_guard.py`, C9 writer gate, vendor closure;
- the named `joined_downstream_a0_a2_assertion`;
- all ten BP2P4J severance trials;
- 50 I1/BP2P4J/BP4R tests, unchanged.

The only new production surface is additive:

```text
cp_a5/events.py
cp_a5/scenario.py
cp_a5/encounter.py
cp_a5/assertion.py
run_cp_a5.py
tests/test_cp_a5_multicontext.py
candidate/evidence/cp_a5_junit.xml
```

No I1 source file was edited by CP-A5.

## 2. Source cuts and owner surfaces

| Surface | Cut | Used as |
|---|---|---|
| PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` | base only |
| I1 | `7d44e30064f8e873e1a3ff9cb05fe75456756b88` | actual guarded joined consumer |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | joined source/practice/E2 |
| BP4R | `693d25bf40f76b09ccf2cc1ec5218a262e201fcd` | C12 origin/fork/schema guard |
| O1 | `501ea1f5bf07468b2c0437f452a81f3515cfdb6f` | A3-A5 construction target |
| R5 | `aebb2452b277bfc91fc78dec8d6001f8a844cc8c` | source/custody findings; no F1CR executable claim |

No B3AS, G17I2, F1CR, C9 R3B, Pyat or native C0 source is adopted by CP-A5.

## 3. Coactor ownership

### B

B is the existing BP1/BP2 sourcefree actor in the I1 seed. CP-A5 adds only
performed sourcefree actions:

- return to workshop;
- take tool;
- carry tool to market;
- complete a commission with `cash_delta: 2`, `completed_delta: 1`,
  `material_delta: 0`;
- return tool.

The actions use sealed CP world events with owner receipts and the actual
workshop tool resource. B's state is checkpointed through the existing BP4
`_checkpoint` path. CP-A5 does not author B's interior, create a new B source,
or duplicate M35/S35.

### C

C is an explicit test-only coactor fixture:

```text
actor_id: TEST_ONLY_CP_A5_ACTOR_C
source_ref: TEST_ONLY_CP_A5_COACTOR_SOURCE_C
source_grade: TEST_ONLY_SOURCEFREE_COACTOR
snapshot: role=carrier, cash=41, material=1, free_hours=8, completed=0
native: false
```

C's source/snapshot hashes are in the trace and events. C requests the tool,
withdraws independently, and leaves. C is not a native source, not a BP1 actor
row, and not a claim about an original person. The event table permits the
`C` actor id; C has no C12 perception row because the branch's actors are A/B.

This is the largest lawful coactor step available from the frozen substrate. An
owner may reject the fixture and require a separately issued actor source; that
is a remaining authority decision, not a test failure.

## 4. A3-A5 contract

- A3: actual `INSPECT` events at workshop, market, workshop over clocks 40, 45,
  50; derived evidence requires 3 inspections and 2 contexts.
- A4: C request/withdrawal; test-only custody rule at clock 62; B independent
  tool-taking/commission/return at clocks 68-90.
- A5: read-only C12 reader; `EncounterReader`/`run_cp_a5.py`; no write on
  `view`, `ask`, `verify`, or `assert`.
- New material consequence: B's tool possession blocks A's repair at clock 80;
  after B returns it, A repairs at clock 100.

The `RETAIN_TOOL` decision is not a personality inference. It is a test-only
transition over repeated, context-differentiated performed inspections. Missing
rule or insufficient evidence emits `HELD` with no decision.

## 5. Integration order

1. Review the CP-A5 candidate at the pinned SHA.
2. Run the 59-test command from `02`.
3. Inspect the A5 trace and JUnit.
4. Owner accepts/rejects the C coactor fixture and the custody rule.
5. If accepted, integrate only additive `cp_a5/` and `run_cp_a5.py`; I1 remains
   the default consumer for old assertions.
6. A later C9/C12 anchor and durable actor readset is a separate owner lane and
   is not a prerequisite for this sourcefree return.

## 6. Rollback

Rollback is deletion of:

```text
cp_a5/
run_cp_a5.py
tests/test_cp_a5_multicontext.py
candidate/evidence/cp_a5_junit.xml
```

I1's `GuardedJoinedProduct`, named assertion, 50 tests, C12 store, guard, and
old severance evidence are unaffected. No database migration, schema bump,
branch rewrite, or PRE-MAIN operation is required.

## 7. Authority and limits

- `OWNER_ANCHOR_REQUIRED` remains for C12 authenticity/completeness.
- C9 durability and the C9 R3B separate reader remain unresolved.
- I1's `material_delta: -1` at zero stock remains an old event; CP-A5 does not
  present it as new consumption.
- No native person, native coactor, CAN/ADP issuance, Pyat world, or C0
  receiver is claimed.
- Independent review and owner adoption are separate from this return.
