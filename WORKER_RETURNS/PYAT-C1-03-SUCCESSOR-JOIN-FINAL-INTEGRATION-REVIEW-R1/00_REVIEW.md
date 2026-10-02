# PYAT C1-03 — SUCCESSOR-QUALIFIED JOIN FINAL INDEPENDENT INTEGRATION REVIEW — R1

Reviewer lane. No implementation mutation. No self-adoption. No C1-R. No Omega-1
action. No C4/live/raw-source execution.

Result under review: `063ee8b77fc4e05c37456ff0168e946247f919ef`
Code-bearing tested commit: `933a3d31aa961719c73e6ce7eebcfe40bc8cd45e`

## Disposition

`APPROVE_AT_DECLARED_GRAIN`

No blocking counterexample was found in any of the ten commissioned areas.

## Reviewer execution note

Section 8 states that the Browser lane cannot execute the worker-local pytest
court and must then rely on documentary inspection. **Execution was available to
this reviewer**, so I did not take that allowance. I independently:

- re-ran the 15-file court: **454 passed, 0 failed, 0 errors, 0 skipped**, exit 0;
- re-derived the historical R8 digests with my own canonicalizer, both directions;
- re-derived the adopted successor digests, both directions;
- compared the complete 44-field production preimage against the adopted oracle
  preimage, both directions;
- collected per-file counts independently rather than trusting the receipt;
- re-hashed the five production-owner blobs at the reviewed head.

Where a receipt asserted something, I recomputed it. A digest match alone was
never accepted as sufficient evidence for a preimage claim.

## Section-by-section findings

### 1. Lineage / commit structure — PASS

Review base is exactly `063ee8b77...`. Final head is exactly one documentary
commit after the code-bearing commit, and that commit adds only the ten required
return-packet files. `933a3d31...`'s parent is merge `4d7b07d0...`, which has
exactly two parents: historical join commission lineage `02ab6785...` and the
accepted successor spine `069ac61b...`.

The merge is **ancestry-preserving, not copied digests**. The successor freeze
commit `92ddee2...` is a genuine ancestor of the joined tree; the full 42-file
oracle package is present and **byte-identical** to the accepted branch; the HQ
adoption record is present. The worker's own code-bearing commit changes only the
three declared test/fixture files and **zero production files**.

### 2. Five production-owner blob conservation — PASS

All five blobs byte-identical at the reviewed head. No production-owner mutation.
Any such mutation would have been blocking; none occurred.

### 3. Historical R8 truth remains historical — PASS, and strengthened

Both historical digests unchanged. Critically, they are **actually re-derived**:
`historical_digest()` computes a hash over the pinned 38-field historical preimage,
so the assertion cannot be satisfied by a literal string comparison. I reproduced
both digests independently, and both equal the value recorded in the R8 summary
spine. Fixture-law bindings — universe, release, query authority, producer
predicate/hash, producer query, consumer query, witness, generated evidence,
denominator — remain intact.

The P7 court was **split, not reduced**. AST comparison of old versus new provider
courts shows exactly one removed name
(`test_p7_frozen_spine_bindings_still_hold_for_the_fixture_law`), which is the
parent of the split; every other historical court survives. The split is *stronger*
than before: the fixture-law half retains every binding, and the identity half now
re-derives the historical digest from the pinned preimage and proves it distinct
from current in both directions. Zero `pytest.skip`, zero `xfail` markers.

### 4. AT17 requalification, both directions — PASS

The real public path `provider -> composition -> generated evidence -> named
positioned-subject consumer` is exercised in both directions.

| | forward | reverse |
|---|---|---|
| denominator | 60 | 62 |
| cells | yes=54 / no=6 | P1=54 / P2=8 |
| fraction | 9/10 | 27/31 |
| consumer | `EXACT_SUPPORTED` | `EXACT_SUPPORTED` |

The tests compare the **complete 44-field production preimage** against the
adopted oracle preimage, not merely the final digest. My independent comparison:
44 fields compared, zero missing, zero extra, zero mismatches, all 38 conserved
fields equal, and the six additions exact — `discovery_receipt_refs=[]`,
`discovery_frontier_ref=None`, `recursive_handoff_refs=[]`,
`recursive_lineage_refs=[]`, `joint_component_count=1`,
`joint_order_semantics="SEMANTIC_ORDERED"`.

Expected truth is loaded from the adopted oracle package and never derived from
production output. The helper `n10e_at17_successor_requal.py` imports **no
production module at all** — only `json`, `hashlib`, and `pathlib` — which is the
structural reason this cannot be circular.

### 5. AT17 regression / custody surface — PASS

Provider suite 30 -> 43. AST-verified: 30 old, 43 new, delta +13, with the one
renamed/split court and 14 added names. P7 split accounts for +1; twelve
successor-specific courts added; **no old court deleted to offset additions**.

I attacked all ten required targets independently and found each genuinely
enforced: historical forward and reverse preservation, forward and reverse
full-preimage equality, forward and reverse digest equality, wrong-direction
successor rejection, six-field omission failure, six-field wrong-value failure, and
rejection of an old R8 digest masquerading as current.

Unchanged obligations confirmed: source law, 16-field witness custody, generated
evidence, named consumer, refusal law, anti-handwritten geometry, changed-source
P6, replay, fresh-process provider replay. No unexplained identity drift beyond
the adopted composed-result succession.

### 6. Join integration — PASS

Join suite 22 -> 28, with all 22 historical obligations present and green.

Successor identities are **real, not asserted**. The AT17 composition dependent
carried by the lifecycle graph carries content hash `01c381d3f3c386cf...`, equal to
the adopted successor forward identity and **not** the historical R8 digest. The
replaced dependent is a genuine AT17 evidence ref, not a fabricated identity.

Historical evidence does not become current by existing: a retained historical R8
ref stays `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT`, and the resolver **refuses** it
by raising `OwnerUnknownDependent`. Preserved: lawful replacement, explicit
noncurrent, unaffected CURRENT, zero-release-known ->
`NOT_GOVERNED / NO_GOVERNING_RELEASE`, unknown -> `NOT_GOVERNED /
OWNER_UNKNOWN_DEPENDENT`, negative analytical vocabulary distinct from R lifecycle
vocabulary, mutation, atomic rollback, checkpoint replay, no production join glue.

### 7. Fresh-process / replay limitation — adjudicated nonblocking

All four accepted replay grades are distinct. AT17 fresh-process provider replay,
R checkpoint/replay, and join fresh-process lifecycle reconstruction all still
execute separately.

The known limitation — no accepted single owner contract carrying
`provider recomputation -> named consumer -> lifecycle restore` in one fresh
process — is **nonblocking** on the commissioned test: all three accepted
obligations still execute separately; no current C1-03 acceptance claim pretends
they form one owner contract; and no semantic or currentness fact is inferred from
the absent bridge. I checked the acceptance claim itself, not just the tests, and
no concrete reason appears for why this prevents lawful acceptance at the declared
grain. The worker recorded the limitation rather than fabricating a bridge, which
is the correct disposition of a known gap.

### 8. Test-count and false-green audit — PASS

`454 passed` was not taken on trust. My independent per-file collection matches the
commission's specification exactly: 92 / 35 / 32 / 17 / 14 / 13 / 13 / 8 / 3 / 2 /
43 / 57 / 54 / 43 / 28, totalling **454**. Reconciliation holds: accepted union
413 -> 426 (+13), join 22 -> 28 (+6), total 435 -> 454 (+19).

No tests removed or disabled; zero skipped; zero xfailed. I rebuilt the file list
from the filesystem with an existence assertion, reproducing the guard that
removes the `pre753`/`pre553` false-green failure mode. The only `pre753`
occurrence anywhere in the worker's final evidence is inside the worker's own
written disclosure of its typo — which is correct behaviour, not a defect. The
historical 434/1 run remains recorded as failed evidence with `relabelled: false`.

### 9. Final acceptance question — coherent as one integrated result

The whole C1-03 source-free join is coherent as one integrated result: C1-03A
AT14-16; AT17 successor-qualified under current C1-02 identity law; C1-03R AT18-19;
historical R8 preserved strictly as historical evidence; current successor
identities under adopted C1-02 law; cross-owner lifecycle and replay behaviour;
negative-state preservation; and owner/blob conservation. The historical and
current identity planes are cleanly separated and neither is used to authenticate
the other.

## Observations recorded, not treated as blocking

1. The fresh-process bridge limitation in section 7 remains genuinely open. It is
   correctly declared and does not support any current acceptance claim.
2. The P7 split changes the historical court's *shape*, not its strength. A future
   reader should understand that the removed test name is a rename of a split
   parent, not a dropped obligation.
3. The worker's own report volunteered its repeated `pre753`/`pre553` typo and
   responded with a structural guard rather than a one-off correction. That is the
   right class of fix and I verified the guard actually works.

## Scope discipline

This review created no review layer beyond the commissioned one, modified no
implementation, self-adopted nothing, began no C1-R, took no Omega-1 action, and
executed no live or raw-source production path. Writes were confined to
`WORKER_RETURNS/PYAT-C1-03-SUCCESSOR-JOIN-FINAL-INTEGRATION-REVIEW-R1/**`.

Terminal: `C1_03_SUCCESSOR_JOIN_FINAL_INTEGRATION_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`