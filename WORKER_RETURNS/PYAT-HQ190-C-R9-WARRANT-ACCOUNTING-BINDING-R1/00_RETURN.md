# PYAT HQ190-C — Return: R9 warrant per-access-layer accounting binding

Lane: **PYAT-HQ190-C — R9 warrant per-access-layer accounting binding — R1**
Role: **RABOCHII / documentary-forensic implementer — Space Bunny**
Repository: `maidiu/rawlsing`
Worker branch: `agent/rabochii-pyat-hq190-c-r9-warrant-accounting-binding-r1`
Commissioned startup SHA: `be64ec98e648e1e6f1a9cb1ad32d7be4b2a84d33`

## Final disposition

`R9_EVIDENCE_INSUFFICIENT__WARRANT_BLOCKER_REMAINS`

Not `R9_ACCOUNTING_BINDING_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW` — because
the specified repair cannot be completed without inventing at least three
counts. Not `R9_MATERIAL_CONTRADICTION_FOUND` — the governing evidence is
internally consistent; it is *silent* on four accounts, not contradictory.

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq190-c-r9-warrant-accounting-binding-r1` |
| Commissioned startup SHA | `be64ec98e648e1e6f1a9cb1ad32d7be4b2a84d33` |
| Substantive result SHA | recorded in `06_FINAL_DISPOSITION.json` after commit |
| Pushed remote branch-tip SHA | reported in the lane completion message |
| Final disposition | `R9_EVIDENCE_INSUFFICIENT__WARRANT_BLOCKER_REMAINS` |
| Terminal | `HQ190_C_R9_WARRANT_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED` |

Per HQ190's standing protocol correction, return artifacts bind the stable
substantive result commit and the branch-tip SHA is reported separately. No
self-referential tip chasing.

---

## 1. The finding

**R9 cannot be closed from documentary evidence.** The reason is precise and
was not previously stated.

Both independent reviews specified the *same* repair. ALT-B
(`3a5b2cbc`, `05_WARRANT_CANDIDATE_REVIEW.json`):

> "At issuance, restore the per-source `source_access_accounting` block for all
> seven sources with the seven exact-count slots and their basis/config
> requirements, **populated or bound to the frozen expectations in artifact
> 07**."

The R2 re-check (`afb1eb49`, `04_C4_R9_GAP.json`):

> "Restore a per-source `source_access_accounting` block for all seven sources
> with the seven slots above and their basis/config/reason qualifiers,
> **populated or bound to the frozen expectations in artifact 07**."

Both assume artifact 07 can supply the values. **It cannot, for three of the
seven slots.**

| C4B slot | Qualifier | artifact 07 expectation? | Bind status |
|---|---|---|---|
| `full_file_sha256_passes` | `REQUIRED_EXACT_COUNT` | **none** | **NOT BINDABLE** |
| `path_opens` | `REQUIRED_EXACT_COUNT_AND_BASIS` | **none** | **NOT BINDABLE** |
| `decoder_invocations` | `REQUIRED_EXACT_COUNT` | **none** | **NOT BINDABLE** |
| `metadata_header_reads` | `REQUIRED_EXACT_COUNT` | SRC08, SRC12 = 1 | partial, 2 of 7 |
| `selected_reads` | `REQUIRED_EXACT_COUNT_AND_CONFIG` | 6 sources | partial, 6 of 7 |
| `full_reads` | `REQUIRED_EXACT_COUNT_AND_CONFIG` | 6 sources | partial, 6 of 7 |
| `retries` | `REQUIRED_EXACT_COUNT_AND_REASON` | all 8 = 0 | **fully bindable, 7 of 7** |

**1 fully bindable · 3 partially bindable · 3 not bindable.**

Plus: `source-path existence/access checks` is a mandatory O1-C07 account named
in artifact 07's `mandatory_separate_accounts`, but it is **not one of C4B's
seven slots**. No slot to populate, no expectation to bind to.

**Four mandatory accounts cannot be bound.**

### Why C4B cannot supply them

C4B's template (`3e4bbe967fa6`) carries `source_access_accounting` on all seven
sources with seven slots each — 49 slots, and **every single value is a
requirement token, not a number**:

```
21 × "REQUIRED_EXACT_COUNT"          (3 slots × 7 sources)
 7 × "REQUIRED_EXACT_COUNT_AND_BASIS" (1 slot  × 7 sources)
14 × "REQUIRED_EXACT_COUNT_AND_CONFIG"(2 slots × 7 sources)
 7 × "REQUIRED_EXACT_COUNT_AND_REASON" (1 slot  × 7 sources)
= 49 tokens, 0 numeric values
```

C4B deliberately deferred the numbers to whoever issues the warrant on the
authorized surface. That deferral is lawful. It is also exactly why R9 is not
a documentary defect a document can finish.

### Omega-1's acceptance criterion cannot be met

> **Acceptance:** Freeze expected budgets and instrumentation before launch.

A budget that exists nowhere cannot be frozen. Ten O1-C07 accounts are
mandatory; four have no budget. **The acceptance criterion is not currently
satisfiable.**

---

## 2. What I produced

| Artifact | SHA-256 | Bytes |
|---|---|---|
| `OPS-04/07_R9_WARRANT_ACCOUNTING_SUCCESSOR_CANDIDATE.json` | `dd9758ab018cde2a702a2671313333e987928904a29ae74e658b05e46f72078b` | 42643 |
| `OPS-04/08_R9_ACCOUNTING_BINDING_CROSSWALK.md` | `1940c0b816ae364ea6530e79752db1775b8e1125200b2c1242bb5543b7ed96b8` | 18679 |

Plus the seven-file return packet in
`WORKER_RETURNS/PYAT-HQ190-C-R9-WARRANT-ACCOUNTING-BINDING-R1/`.

The successor candidate binds every layer the evidence establishes, with
provenance, at the correct access layer, and converts every unestablished layer
into one of **eight individually-identified unfilled issuance-time
obligations**, each carrying a named prohibition against fabrication.

---

## 3. Governing facts preserved — all verified

| Required fact | Preserved | Evidence in the successor |
|---|---|---|
| Six sources have explicit read counters | yes | SRC02/06/14 selected=1, full=0; SRC08/12 metadata=1, selected=0, full=0; SRC26 header-prefix 176 bytes, selected=0, full=0 — all with artifact-07 provenance |
| SRC27: exactly one governed full Route-B pass, max one, zero retries | yes | `operation_level_law` = 1 / 1 / 0, retry law verbatim |
| SRC27's four access layers are separate, never "one file open" | yes | all four listed individually, each `FLOOR_ONLY` with `established_ceiling: null`; accounting warning and hardened note verbatim; explicit refusal to collapse |
| SRC35 zero fresh reads, retained-only | yes | excluded, `fresh_reads: 0`, `NONE__RETAINED_ONLY`, hard zero, **explicitly not unconstrained** |
| All locator placeholders remain placeholders | yes | all 7 literal `<REQUIRED_FILL_IN_SLOT…>`; 0 searches |
| All seven entries retain zero retry | yes | `max_retry_budget: 0` × 7 |
| Successor authorizes nothing | yes | `signed/issued/authorizes_access/execution_authorized` all `false`; `issued_by`/`issue_date`/`signature_or_commit` all `null` |

Ten safety invariants, ten passed. Eight governing facts, eight preserved.
Zero failures. Zero fabricated values.

---

## 4. Two refusals worth stating plainly

**SRC27's `full_reads`.** Artifact 07 carries no `expected_full_reads` for
SRC27. The hardened note establishes a **floor** of one full compatibility
read. Binding a floor into a slot demanding an *exact count* would convert a
minimum into a limit. **Refused.**

**SRC27's `selected_reads`.** SRC27 has no `expected_selected_reads`. Its
compatibility read is a full-route read governed by the route-pass law. Mapping
a route pass into a selected-read slot would be a fabrication. **Refused.**

Also: **176, 174 and 332 are three different quantities** — bounded header-prefix
bytes, raw nominal case size, decoded dictionary width. Artifact 07 requires
them preserved separately and never collapsed. They are recorded separately.

---

## 5. Independent-review prerequisite — evidenced, not decided

`04_ISSUANCE_PREREQUISITE_INVENTORY.json` PRQ-07 gathers the exact current
evidence and marks the authority decision:

```
status:             HQ_ADJUDICATION_REQUIRED
decided_by_this_lane: false
```

**This lane offers no vote, no recommendation and no inference on whether that
blocker is discharged.** HQ's call.

Evidence gathered: Lane A `fe6103cd` (`APPROVE_AT_DECLARED_GRAIN`, independently
recomputed the historical candidate's SHA-256, matched, recorded
`instrumentation` bound but its own blocker list worded the fifth item as *"HQ
adjudication after this independent review"*); ALT-B `3a5b2cbc`
(`APPROVE_AT_DECLARED_GRAIN`, `instrumentation_bound_per_source: false` × 7,
and its own note: *"This review discharges the fifth blocker at the source-free
freeze grain only"*); R2 `afb1eb49` (`MATERIAL_CORRECTION_REQUIRED`, scoped as a
narrow four-claim re-check, not a freeze re-review); HQ187 `HQD-2026-10-02-187`
adjudicating R2; HQ190 `02309f4e7` accepting the consolidation with no new
freeze-evidence blocker.

One tension recorded for HQ: **none of the three reviews examined this
successor candidate.** The candidate has had no independent review at all.

---

## 6. Issuance prerequisites — none closed

| ID | Kind | Status |
|---|---|---|
| PRQ-01 | Technical R9 closure | **NOT_CLOSED** |
| PRQ-02 | Seven locator fills | OPEN, 0 discovered |
| PRQ-03 | User/resource-owner approval | UNSET |
| PRQ-04 | HQ approval | UNSET |
| PRQ-05 | Signature and issuance act | NOT_PERFORMED |
| PRQ-06 | R7 live-runtime prerequisite | OPEN (blocks live execution, **not** issuance) |
| PRQ-07 | Independent integration review | **HQ_ADJUDICATION_REQUIRED** |

Closed: **0**. Stage register unchanged: **0 / 1 / 1 / 9 / 1**.

---

## 7. Hard holds — all observed

| Hold | State |
|---|---|
| Locator discovery / fill | **0 / 0** |
| Raw source stat / hash / open / metadata read / decode / materialization | **0 / 0 / 0 / 0 / 0 / 0** |
| Directory inspection for sources | **0** |
| Warrant issued or signed | **no** |
| Live C4 | **not executed** |
| Production mutation | **none**; `rawlsing_next` 0 files changed |
| C7 / actor-person work | **none** |
| `HQ_HANDOFF/**` edit | **none** |
| Historical warrant candidate | **blob and SHA-256 reverified unchanged** |
| Historical C4 returns, custody records | **not edited** |
| Astra contacted | **no** |
| Self-adopted / merged into control | **no / no** |

The historical candidate is **not on this branch's ancestry** (merge-base
`87029d34`), so overwriting was structurally impossible as well as forbidden.
Reverified after every write:

```
blob    9f6b113151f7c05f0a22432b034347b631e1a895
sha256  d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a
bytes   17073
```

---

## 8. Verification discipline

`git` plumbing and `node` v18.14.2; `shasum -a 256`. `python3` not relied upon.

**Non-equality law:** nothing rests on `null == null` or absent-field equality.
Every identity resolves to a nonempty exact 40-hex blob or complete 64-hex
digest. **Absence** findings — the three NOT_BINDABLE slots — rest on exhaustive
token census across five governing artifact groups plus direct enumeration of
the parsed C4B template and artifact 07's per-source block, never on sampling.

My per-source layer census was cross-checked against R2's independently
produced `field_presence_matrix` and **agrees on all six fields**.

---

## 9. What would actually close R9

**(a) Supply governing evidence** fixing exact per-source values for the four
unbound accounts, each with the four required measurement-basis fields.

**(b) An instrument-level determination on the authorized execution surface**,
recorded with its measurement basis — itself an issuance-time act requiring all
seven locator fills plus both approvals. **Neither exists.**

Route (b) is where C4B always intended these numbers to come from. R9 is a
**warrant-issuance-time obligation partially discharged on paper**, not a
documentary defect a document can finish.

---

Terminal:
`HQ190_C_R9_WARRANT_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED`