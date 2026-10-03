# PYAT HQ195 — R9 stage ownership / architecture-warrant forensic packet — R1

Role: **RABOCHII / DOCUMENTARY AUTHORITY FORENSICS — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq195-r9-stage-ownership-architecture-warrant-r1`
Commissioned startup SHA: `501494b18afdd623fc3561951daf36714e5690c9` — verified exactly.

## Disposition

`R9_ARCHITECTURE_WARRANT_CANDIDATE__LITERAL_ACCOUNT_REQUIRES_RUNTIME_OR_AUTHORITY_CHANGE`

A candidate finding for independent adjudication. Nothing is self-adopted, no account is
waived, no warrant is issued, no authority is exercised. **R9 remains OPEN.**

## The short answer

The staging conflict is a **false alarm**, and the real obstacle is worse than a conflict.

Omega-1's own acceptance sentence already separates the obligations:

> `Freeze expected budgets and instrumentation before launch; retain measured counts.`

That is three obligations with three different stages and owners — expected budget
(pre-launch), instrumentation (pre-launch), measured count (during/return). So
`stage: DURING_EXECUTION_AND_RETURN` and "frozen before launch" reconcile **without
reinterpreting a single word**.

The real problem is that the literal OS path-open count is unavailable at *every* stage, for
**two independent reasons**:

| Limb | Why it fails | Type of gap |
|---|---|---|
| Expected budget (pre-launch) | No frozen artifact states an expected path-opens figure for any of the seven permitted sources | **documentary** |
| Measurement (during run) | No lawful mechanism observes the compiled reader's opens on the bound surface | **capability** |

A budget and a measurement normally compensate for each other. Here **neither can**, and
they fail for unrelated reasons — so fixing one leaves the obligation unmet. That is why
"pair a pre-launch budget with a during-run measurement" cannot work.

## What the architecture-warrant test actually found

The C4 predicate is *"cannot represent **or** cannot lawfully succeed."* I tested both prongs
separately, and the prong that **fails** matters as much as the one that succeeds:

- **Prong 1 — cannot represent: NOT SATISFIED.** The grain is fully expressible.
  `path_opens: REQUIRED_EXACT_COUNT_AND_BASIS` is an explicit per-source slot in C4B's
  template, and O1-C07 names it in `mandatory_separate_accounts`. **The instrument can express
  the account; the host cannot populate it.** An architecture-warrant argument resting on
  unrepresentability would be wrong, and I do not make it.
- **Prong 2 — cannot lawfully succeed: SATISFIED.** HQ194 has already accepted that the bound
  runtime can neither measure nor enforce the literal count, and that "R9 is not closed by
  replacing path opens with reader invocations or Python-level opens."

## The trap I declined

A Python-level open count **now exists and is enforceable** — HQ192 measured **2 opens per
decode**, with excess reads refused before execution. HQ191 also established an enforceable
reader-invocation ceiling. Both are real, lawful and useful.

Neither is the account O1-C07 names, and four separate authorities forbid the substitution —
O1-C07's `measurement_basis_requirement`, its hardened note ("expressly forbidden by
Omega-1"), HQ191 ("not relabelled as one"), and HQ194. The reader-invocation ceiling remains
lawful as an **upper bound on logical accesses**; it is simply not the required account. The
existence of an enforceable near-miss is exactly when a redefinition becomes tempting.

## Two findings worth HQ's attention beyond the disposition

**DQ-01 — a documentary discontinuity.** C4B's frozen template carries seven
`source_access_accounting` token fields on each of seven sources. The **adopted** warrant
candidate at the same freeze carries **no `source_access_accounting` on any source** — it
binds the account list and basis requirement *globally* instead. I verified this field by
field. The accounts survive, but the **per-source fill-in obligation** does not — so under the
adopted candidate's own shape there is no per-source slot into which a path-opens value must
be entered. I did **not** resolve this, because whether a global binding satisfies a
per-source frozen requirement is an authority question, not a documentary one. It is also the
cheapest available fix (OPT-2) and it makes the blocker unskippable at issuance.

**XF-05 — a bound runtime does not close R9.** C4B left `execution_surface` as
`<HQ_TO_BIND_EXACT_RUNTIME…>`; the adopted candidate resolves it to a concrete stack. That is
real progress, but **determinism is not observability**. Binding the runtime guarantees the
count *would* be reproducible if it could be observed — and observability is the missing
precondition. This forecloses the tempting "R9 is just an unfilled placeholder" argument.

## Stage ownership, in brief

Of the ten mandatory separate accounts, **eight are satisfiable** on the current runtime;
header-prefix is **closed at the Python layer** (HQ194 Part C / HDR-03); byte counts are
**partial by the express design** of their "where measurable" qualifier; and exactly **one —
path-level opens with its basis — is unsatisfiable** at issuance, pre-launch and during
execution alike. Full per-stage detail is in `02_STAGE_OWNERSHIP_MATRIX.json`.

A deliberate non-bundle: **SEL-02** (selected-column read *count* has no executable owner) is
a genuine second gap, but materially narrower — its configuration half is frozen and its
exactness is enforced, so its lawful route is a typed null. Merging it into the hard blocker
would misstate the severity and obscure which gap actually needs a runtime or authority
change.

## What the frozen law already requires when a count is unknowable

The answer is not discretion. O1-C07: unreached or unmeasurable metrics are reported as
**null with a typed reason**, "**never** a fabricated zero or a fabricated PASS." So:

```json
{ "account": "path-level opens", "value": null,
  "basis": "OS layer, compiled pyreadstat 1.3.6 extension, no lawful unprivileged interposition on the bound surface",
  "reason": "UNOBSERVABLE_ACCOUNT__NO_LAWFUL_MEASUREMENT_MECHANISM_AT_ANY_AVAILABLE_LAYER",
  "near_miss_not_substituted": "python_level_opens_measured_2_per_decode" }
```

The obligation does not become optional — it becomes a **typed absence**, with the near-miss
disclosed rather than promoted. A fabricated *zero* is forbidden for the same reason a
fabricated *count* is: both assert a measurement never made.

Also worth recording: the only frozen open-related **zeros** — `WVS_SRC35_fresh_source_opens`
and `excluded_source_fresh_opens` — are zero **by construction** (a retained comparator, and
sources not opened at all). Neither constrains the seven permitted sources; reading either as
covering them would be a category error.

## Candidate options for HQ (this lane selects none)

| | Option | Closes R9? | Authority cost |
|---|---|---|---|
| OPT-1 | Typed-null publication + disclosed upper-bound proxy | **No** — available now | none beyond adjudication |
| OPT-2 | Reinstate per-source accounting slots (DQ-01) | No, but makes the gap unskippable | HQ |
| OPT-3 | Narrowly instrumented reader (choke point at the C boundary) | **Potentially** | HQ + requalification; feasibility **undetermined** |
| OPT-4 | Isolation layer counting opens without interposition | Potentially, **unproven here** | HQ + requalification |
| OPT-5 | Privileged tracing authority | Observation only; capping is separate | Highest — conflicts with no-sudo posture |
| OPT-6 | Reinterpret the O1-C07 grain | Nothing — retires the requirement | **Requires Astra/Omega** |

The sibling lane `…hq195-r9-instrumented-runtime-feasibility-r1` has a commission and **no
return**, so OPT-3's feasibility is genuinely undetermined and I do not pre-judge it. AT20
independently caps the conclusion available even after success: "A source-free fixture result
cannot establish live occupancy."

## Authority boundary

I did not waive O1-C07, redefine "path-level opens", issue a warrant, authorize tracing or
raw access, or adopt an architecture decision. **HQ may** fund instrumentation, grant or refuse
tracing, choose the interim reporting form, and reinstate the per-source slots. **Astra/Omega
is required** for any redefinition of the O1-C07 grain, any waiver or satisfaction-finding for
O1-C07, or release of the standing HQ182 non-adoption hold. No one in this chain may issue the
warrant unilaterally — both HQ and resource-owner approvals are `UNSET` and the candidate is
unsigned.

## Checkout law

`SPARSE_REQUIRED` honoured. No clone; canonical clone used; sparse worktree at
`Rawlsing_Worktrees/hq195-r9-stage` with the manifest applied exactly — **4 files materialized
against 6851 tracked**, zero sparse expansions. All historical evidence read via
`git show`/`cat-file`/`ls-tree`; **no historical tree checked out**; `sparse-checkout disable`
never run.

One disclosure: the commission's command invokes `prepare_sparse_worktree.sh` at a path absent
from the canonical clone's working tree, because that clone is checked out at an older commit
while the script is tracked at my commissioned SHA. I read it by git object access, verified
it as blob `22f3f624…` (sha256 `93e3fc97…`), **reviewed it for safety** before running —
confirming it never clones, verifies the remote SHA, refuses on collision, uses
`--no-checkout`, applies only the supplied patterns, and checks HEAD/remote/expected — then
ran a byte-identical copy from a temp path rather than dirtying the user's primary checkout.
One untracked `.DS_Store` (Finder metadata) was cleared so the worktree is clean.

## Holds

Zero raw-source access, source-directory inspection, locator discovery or fills, warrant
issuance, live C4, C7, and actor/person work. Zero historical tree checkouts, zero sparse
expansions, zero full checkouts. No production, `HQ_HANDOFF`, or historical warrant artifact
mutated. No self-adoption, no merge into control. **Zero counts, budgets, maxima or thresholds
invented** — where a value was unavailable it is reported as unavailable with a reason. R7 not
reopened.

## Artifacts

`00_RETURN.md` · `01_AUTHORITY_TEXT_CROSSWALK.json` · `02_STAGE_OWNERSHIP_MATRIX.json` ·
`03_EXPECTED_VS_MEASURED_ACCOUNTING.md` · `04_ARCHITECTURE_WARRANT_TEST.json` ·
`05_MINIMUM_LAWFUL_SUCCESSOR_OPTIONS.json` · `06_AUTHORITY_BOUNDARY_AND_ESCALATION.json` ·
`07_FINAL_DISPOSITION.json`

Terminal: `HQ195_R9_STAGE_OWNERSHIP_RETURNED__HQ_REVIEW_REQUIRED`
