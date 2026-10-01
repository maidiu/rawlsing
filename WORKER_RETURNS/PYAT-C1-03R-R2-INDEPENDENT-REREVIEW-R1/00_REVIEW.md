# PYAT C1-03R — OWNER FAIL-CLOSED R2 — INDEPENDENT REREVIEW — R1

**Disposition:** `CHANGES_REQUIRED`
**Terminal:** `C1_03R_R2_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
**Review branch:** `agent/reviewer-pyat-hq156-c1-03r-r2-rereview-r1`
**Commissioned tip:** `f6e2b059883bee29b2dadfc1cc59df7a5a4c7735`
**Implementation return reviewed:** `7f64493758f6b3b77d7e9ce1486c1324ff709edc` (base `88d949301…`)
**Prior review:** `380a79cde63d9ee239e5812f89283e997e16da96` — also `CHANGES_REQUIRED`

No implementation mutation. No merge, no self-adoption.

---

## Verdict at a glance

| Item | Verdict |
|---|---|
| RVW-001 duplicate replacement rows | **APPROVED** |
| RVW-002 negative serialization / schema | **APPROVED** |
| RVW-003 owner-unknown currentness | **APPROVED** on the requirement itself |
| RVW-003 *flagged* known-but-never-transitioned reading | **DEFECTIVE — blocking** |
| RVW-004 checkpoint U replay | **APPROVED** |
| Shared owner law / rollback fixture | **APPROVED** |
| Preserve accepted architecture | **APPROVED** |

Three of four blockers are genuinely closed, and closed *harder* than the worker's own
courts demonstrated. The fourth is closed for the case the review asked about
(owner-unknown), but the reading the worker flagged for adjudication is defective. So:
`CHANGES_REQUIRED`, scoped to one boundary.

---

## 1. Method: I did not use the worker's courts as evidence

The worker added 16 courts. Those courts are the worker's own account of its own repair,
so treating them as proof would be circular. I wrote **54 probes from the reviewer's
side**, deliberately reaching for forms the worker's courts do not exercise — and I
rewrote the RVW-004 resealer and rebuilt the legacy-compatibility receipt independently
rather than importing the worker's helpers.

That effort is what found the defect. None of the 16 worker courts touch it.

## 2. What held up under attack

**RVW-001 — approved, and more robust than claimed.** Nine forms refused, including
several the worker never tried: three-row duplicates; the forged target placed *first*
(an ordering attack); duplicate rows expressed as distinct `ExactRef` objects with equal
keys; a **cross-table** duplicate where one source appears in both the replacement table
and the noncurrent table. The rejection is genuinely unconditional and ordering-independent.

**RVW-002 — approved, and the null check is stronger than advertised.** I tested
`replacement_ref` set to `False`, `0`, the string `'None'`, and `{}`. All four refused.
That matters: a truthiness check would have accepted every one of them. The actual check
is `is not None`. I also confirmed schema *version* mutation (`1.0.0`→`1.0.1`) and
trailing whitespace are refused, so the comparison is exact equality. Legacy
positive-only compatibility I verified positively: ref preserved, bytes preserved, no
extra keys, and a tampered legacy `record_ref` still raises.

**RVW-003 owner-unknown — approved.** `NOT_GOVERNED` with `OWNER_UNKNOWN_DEPENDENT`, and
`resolve_current_analytical_product` raises `OwnerUnknownDependent`. The worker's court
polluted the snapshot cache; I also polluted the **evidence** cache, and the result was
unchanged — confirming the gate reads only `known_dependent_refs` and nothing else.

**RVW-004 — approved.** Both commission-required forms refused against a fully
self-consistently resealed checkpoint, using my own resealer, with `reseal_consistent=True`
asserted before each probe. I added two checks the commission did not require: U set-equal
**reordering is accepted** (so the equality is set-based and does not over-reject), and U
inflation is refused at construction by the pre-existing overlap guard.

**Rollback fixture — approved, and genuinely not theater.** This was the commission's
specific worry. I measured the graph *before* driving anything: all three transitions
independently show A=3, U=1, disjoint, covering K. Then I drove all three with my own
registries: each receipt shows R=1, N=2, A=3, U=1 with both laws holding. The rollback
cites its prior lawful release, its receipt round-trips, and a missing callback with no
declaration still errors with the current pointer unchanged.

**Preserve — approved.** One generic disposition; DEFERRED/UNAVAILABLE/DELETED all
refused; error never auto-converts to noncurrent; unchanged-ref callback errors; sealed
successor, decoy and consumed are three distinct refs with the decoy sharing the consumed
content hash; AT18 four grades with stored material ceiling at `SERIALIZATION_REPLAY`.
`pre553_replay_audit.py`, `pre553_analytical_composition.py` and C1-03A are **absent from
the R2 diff**, and `AuthorityCandidate` is untouched.

## 3. The blocking finding

**F-1. A known-but-never-transitioned ref is reported CURRENT and served as a current
analytical product when no release exists at all.**

```python
ex = AuthorityMaintenanceExecutor(
    initial_snapshots=(model_authority_snapshot("forward"),),
    initial_current_selection={old_model.authority_id: old_model},
    determinant_graph=SemanticDeterminantGraph(
        known_dependent_refs=(fabricated,)),   # ref in no event/evidence/snapshot/release
)
ex.dependent_lifecycle_status(fabricated)
# -> lifecycle_state = 'CURRENT', governing_release_ref = None
resolve_current_analytical_product(executor=ex, dependent_ref=fabricated)
# -> SERVED AS A CURRENT ANALYTICAL PRODUCT
```

Zero releases recorded. The ref appears in no event, no evidence receipt, no snapshot and
no release. The only thing that knows it is `known_dependent_refs` — a caller-supplied
constructor argument. And it is served as current.

**Why the flagged reading cannot stand.** I verified the structural fact that settles this:
on a real release, `A | U == K`. Every known dependent is covered by the governing release
and therefore takes the row / pair / unaffected branch. So the `latest is None` + known-ref
`CURRENT` branch is reachable **only in the zero-release state** — precisely the state where
no governed transition has established anything. The reading's only reachable case is the
unsupported one.

The owner is also currently inconsistent between two neighbours in that same state: an
*unknown* ref returns `NOT_GOVERNED`, while a *known* ref returns `CURRENT`. The second is
the unsupported one, and the commission's criterion — blocking only if the reading creates
an authority claim the owner has not established — is met exactly.

**This is not an R2 regression.** The pre-R2 code returned `CURRENT` unconditionally in that
branch. R2 narrowed the unknown case and left the known-untouched case alone, which is why
the worker disclosed it rather than concealing it. I am adjudicating an inherited defect
that the commission asked me to adjudicate, not faulting the repair for introducing it.

**Minimal correction:** in `dependent_lifecycle_status`, require a governing release to
exist before attributing currentness in the no-release-mentions-this-ref case; return the
typed `NOT_GOVERNED` state instead. Confined to one function in
`pre553_authority_maintenance.py`. It reopens nothing.

## 4. The second flagged reading — approved as correct

**A receipt declaring the new schema with zero noncurrent rows is refused, not
normalized — CORRECT at this grain.**

The two shapes are mutually exclusive *by construction*: the owner emits `receipt_schema`
and `noncurrent_dependents` only when a dependent is noncurrent, and otherwise emits
exactly the historical field set. Declaring the new schema while asserting no rows is
therefore a shape the owner cannot produce. Accepting it would silently reinterpret
positive-only legacy material — which is the precise thing the commission required to fail
closed. A normalizing read is defensible in the abstract, but it would require accepting an
owner-impossible shape and would weaken the mutual-exclusivity invariant that makes the
historical identity strategy sound. The refusal is also narrowly scoped: clean legacy
material is untouched.

## 5. Residuals and a self-correction

**F-2 (non-blocking).** `from_dict` tolerates an unknown extra top-level field. It is
dropped, is not hashed into identity, and does not survive re-emission — so it is not a
laundering route. Tightening it without knowing the full historical corpus risks rejecting
legitimate stored material, so it is an owner-versioning decision, not a fail-closed repair.

**F-3 (my own probe was defective).** My "schema uppercased" probe returned `ACCEPTED` and
on first read looked like a defeated repair. It was not: the schema id contains no
lowercase characters, so `.upper()` is the identity function and the probe mutated nothing.
I verified that directly. The meaningful variants — trailing whitespace and a version bump —
are both refused. Disclosed because a reviewer reporting a clean sweep should report
defective probes too.

## 6. Execution and provenance

Four-file court: **160 passed, 0 failed, 0 errors, 0 skipped, 0 xfailed** in 71.92 s
(42 / 51 / 54 / 13), independently reproducing the worker's claim exactly. The worker's 16
new courts verified present (9 + 7).

Diff `88d949301…` → `7f6449375…` is confined to the commissioned terrain: the two owner
modules, two test modules, the fixture, and the return packet.

**Provenance caveat.** An external controller removed this review worktree mid-task; I
recreated it and verified it at `eb9e0938d…` before running anything. The shared working
tree is **not** the provenance for this review.

## 7. Next required action

One bounded correction to `AuthorityMaintenanceExecutor.dependent_lifecycle_status`: stop
reporting `CURRENT` for a known dependent when no governing release exists to attribute the
claim to — return the typed `NOT_GOVERNED` state instead. Then narrow rereview of that
single boundary. Nothing else in the repair needs to move.

```
C1_03R_R2_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED
```
