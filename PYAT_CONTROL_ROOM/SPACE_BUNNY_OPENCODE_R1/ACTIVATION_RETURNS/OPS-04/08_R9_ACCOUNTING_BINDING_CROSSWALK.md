# R9 accounting binding crosswalk — mandatory account → per-source layer → evidence

Lane: **PYAT-HQ190-C — R9 warrant per-access-layer accounting binding — R1**
Role: RABOCHII / documentary-forensic implementer — Space Bunny
Worker branch: `agent/rabochii-pyat-hq190-c-r9-warrant-accounting-binding-r1`
Commissioned startup SHA: `be64ec98e648e1e6f1a9cb1ad32d7be4b2a84d33`
Subject freeze: `8ff40d37de69db2d8a6053a7c2242f481677f1a4`

Successor candidate:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/07_R9_WARRANT_ACCOUNTING_SUCCESSOR_CANDIDATE.json`
SHA-256: `dd9758ab018cde2a702a2671313333e987928904a29ae74e658b05e46f72078b`
Bytes: 42643

Disposition: **`R9_EVIDENCE_INSUFFICIENT__WARRANT_BLOCKER_REMAINS`**

---

## 0. The finding in one line

Both independent reviews specified the same R9 repair: restore C4B's
per-source `source_access_accounting` block, *"populated **or** bound to the
frozen expectations in artifact 07."* I tested all seven slots against that
instruction. **Three can be neither populated nor bound**, and a fourth
mandatory O1-C07 account has no slot at all. The repair as specified cannot be
completed without inventing at least three counts.

---

## 0a. C4B slot-by-slot bind test

The decisive test. For each of C4B's seven slots: does artifact 07 contain a
corresponding expectation to bind to?

| C4B slot | Qualifier | artifact 07 expectation? | Bind status |
|---|---|---|---|
| `full_file_sha256_passes` | `REQUIRED_EXACT_COUNT` | **none** | **NOT BINDABLE** |
| `path_opens` | `REQUIRED_EXACT_COUNT_AND_BASIS` | **none** | **NOT BINDABLE** |
| `decoder_invocations` | `REQUIRED_EXACT_COUNT` | **none** | **NOT BINDABLE** |
| `metadata_header_reads` | `REQUIRED_EXACT_COUNT` | SRC08, SRC12 = 1 | partial — 2 of 7 |
| `selected_reads` | `REQUIRED_EXACT_COUNT_AND_CONFIG` | 6 sources | partial — 6 of 7 |
| `full_reads` | `REQUIRED_EXACT_COUNT_AND_CONFIG` | 6 sources | partial — 6 of 7 |
| `retries` | `REQUIRED_EXACT_COUNT_AND_REASON` | all 8 = 0 | **fully bindable, 7 of 7** |

**1 fully bindable · 3 partially bindable · 3 not bindable.**

Plus: `source-path existence/access checks` is a mandatory O1-C07 account named
in artifact 07's `mandatory_separate_accounts`, but it is **not one of C4B's
seven slots**. It has neither a slot to populate nor an expectation to bind to.

**Four mandatory accounts therefore cannot be bound.**

Two slots deserve explicit refusal:

- **`full_reads` for SRC27.** Artifact 07 carries no `expected_full_reads` for
  SRC27. The hardened note establishes a **floor** of one full compatibility
  read. Binding a floor into a slot demanding an *exact count* would convert a
  minimum into a limit. Refused.
- **`selected_reads` for SRC27.** SRC27 has no `expected_selected_reads`. Its
  compatibility read is a full-route read governed by the route-pass law.
  Mapping a route pass into a selected-read slot would be a fabrication.
  Refused.

---

## 0b. Where the repair specifications come from

**ALT-B** (`3a5b2cbc`), `05_WARRANT_CANDIDATE_REVIEW.json`, residual `R9`:

> "At issuance, restore the per-source `source_access_accounting` block for all
> seven sources with the seven exact-count slots and their basis/config
> requirements, **populated or bound to the frozen expectations in artifact
> 07**."

Its `per_source_binding_completeness` records
`instrumentation_bound_per_source: false` for all seven sources.

**R2 re-check** (`afb1eb49`), `04_C4_R9_GAP.json`, finding C4
`UPHELD__SUBSTANCE_CORRECT`:

> "Restore a per-source `source_access_accounting` block for all seven sources
> with the seven slots above and their basis/config/reason qualifiers,
> **populated or bound to the frozen expectations in artifact 07**."

And its own framing of why the gap matters:

> "An executor holding only the warrant has a global account list but no
> per-source limit field to comply with… **a cross-reference is not the same as
> a bound field.**"

My finding is a **further step beyond both reviews**. Both addressed the
*warrant's* missing per-source block and assumed artifact 07 could supply the
values. It cannot supply them for three slots.

---

## 1. Bottom line

R9 is **not** closable at candidate grain from the governed evidence.

Of the **10** mandatory separate accounts that O1-C07 requires, the evidence
establishes an exact per-source value for **6**. For **4** it establishes none
anywhere — not in Omega-1, not in C4B, not in the freeze packet, not in C4C3.

Those four are:

1. source-path existence/access checks
2. file hash passes (full SHA-256 over the file)
3. path-level opens
4. decoder invocations

C4B's warrant template **specifies** all four and **supplies a requirement
token, never a number**, for every one of them, on every one of the seven
sources. Omega-1's O1-C07 acceptance criterion is *"Freeze expected budgets
and instrumentation before launch."* A budget that exists nowhere cannot be
frozen. **The acceptance criterion is therefore not currently satisfiable.**

I did not invent the four missing numbers. The successor candidate records
them as eight individually-identified unfilled issuance-time obligations, each
with a named prohibition against fabrication.

---

## 2. The requirement being satisfied

**Omega-1, mandatory condition O1-C07** (verbatim):

> Execute exactly one governed fresh full-route LiTS pass, six bounded physical
> witnesses and retained WVS replay/comparison. Account separately for file
> hash passes, path-level opens and their measurement basis, metadata reads,
> header-prefix reads, decoder calls, selected-column/full reads, byte counts
> and retries. **A full Route-B pass is not a claim of one OS-level file open.**

> **Acceptance:** Freeze expected budgets and instrumentation before launch;
> retain measured counts. WVS and excluded-source fresh opens remain zero under
> this scope.

**Artifact 07, `O1_C07_instrumentation`** (verbatim):

> A full Route-B pass is NOT one OS-level file open. Access must be separately
> accounted at every distinct layer.

> Each account must state its measurement **BASIS**, not only a count. A count
> without a stated basis is not an account.

---

## 3. Master crosswalk — all 10 mandatory accounts

Legend — **BOUND**: an exact per-source value exists in governing evidence.
**PARTIAL**: exists for some sources only. **UNBOUND**: exists nowhere.

| # | Mandatory account | Status | Established where | Enforceable? |
|---|---|---|---|---|
| 1 | source-path existence/access checks | **UNBOUND** | nowhere | no |
| 2 | file hash passes (full SHA-256) | **UNBOUND** | nowhere | no |
| 3 | path-level opens | **UNBOUND** | nowhere | no |
| 4 | decoder invocations | **UNBOUND** | nowhere | no |
| 5 | metadata reads | **PARTIAL** | artifact 07, SRC08 & SRC12 only (=1) | partly |
| 6 | header-prefix reads | **PARTIAL** | artifact 07, SRC26 only — as **176 bytes**, not a read count | partly |
| 7 | selected-column reads | **BOUND** | artifact 07, six sources | ceiling via retry law |
| 8 | full reads | **BOUND** | artifact 07, six sources (=0) | ceiling via retry law |
| 9 | byte counts where measurable | **PARTIAL** | SRC26 only (176 / 174 / 332) | partly |
| 10 | retries | **BOUND** | all eight sources (=0) | **yes — hard zero** |

**6 bound or partly bound · 4 unbound.**

---

## 4. Why the four are unbound — the actual evidence

### 4.1 C4B's template names every slot and fills none

`WORKER_RETURNS/PYAT-C4B-WORKLOAD-ORACLE-FREEZE-R1/07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json`
at `c2af4f61d68e9803af83f8e26f633acfe31062fa`, blob `…`, carries
`source_access_accounting` on all seven sources. Every slot value is a
requirement token:

| Slot | Value on all 7 sources |
|---|---|
| `full_file_sha256_passes` | `"REQUIRED_EXACT_COUNT"` |
| `path_opens` | `"REQUIRED_EXACT_COUNT_AND_BASIS"` |
| `decoder_invocations` | `"REQUIRED_EXACT_COUNT"` |
| `metadata_header_reads` | `"REQUIRED_EXACT_COUNT"` |
| `selected_reads` | `"REQUIRED_EXACT_COUNT_AND_CONFIG"` |
| `full_reads` | `"REQUIRED_EXACT_COUNT_AND_CONFIG"` |
| `retries` | `"REQUIRED_EXACT_COUNT_AND_REASON"` |

**Zero numeric values.** C4B specified the taxonomy and made the exact counts an
obligation on the issuer, on the authorized surface, after the locator and
runtime are bound. That deferral is lawful and deliberate. It is also exactly
why R9 cannot be closed from documentary evidence alone.

### 4.2 Nothing else supplies them

| Searched | Result |
|---|---|
| Freeze packet, all 7 artifacts, for any of the four layer tokens | **0 occurrences** |
| C4B `01_EIGHT_SOURCE_WORKLOAD_FREEZE.json` | **0 occurrences** |
| Omega-1 `01_DECISION.json` | **0 occurrences** of any layer slot name |
| C4C3 artifacts (`03`, `04`, `06`) | **0 occurrences** of any layer slot name, `open_count` or `hash_pass` |

C4B's `read_economy` classifies sources but binds no layer counts:

```
fresh_full_route      : SRC27
bounded_fresh_physical: SRC02, SRC06, SRC08, SRC12, SRC14, SRC26
retained_comparator   : SRC35
excluded_fresh_reads  : 0
substitutions_forbidden: true
```

### 4.3 A floor is not a ceiling — the SRC27 case

Artifact 07's hardened note is the strongest access-layer statement in the
evidence, and it is still only a floor:

> "The run will require **at minimum**: one existence/access check, one full
> SHA-256 hash pass, one metadata read, and one full compatibility read. Each
> is a separate account under O1-C07."

**"At minimum"** establishes four floors of 1. It establishes **no ceiling**.
An enforceable limit requires a maximum. So for SRC27 — the single most
consequential read in the workload — the four lower-layer accounts are
`FLOOR_ONLY`, and I have recorded them that way rather than promoting 1 into a
limit.

The successor candidate therefore preserves the operation-level law exactly
(`expected_full_route_passes: 1`, `max_full_route_passes: 1`) **and** lists the
four separate layer accounts with `established_floor: 1,
established_ceiling: null`.

---

## 5. Per-source × per-layer binding matrix

`E` = exact value established · `H0` = hard zero, breach is a STOP · `F1` =
floor 1, no ceiling · `—` = no value anywhere

| Source | Class | exist/access | hash pass | path opens | decoder inv. | metadata | hdr-prefix | selected | full | byte counts | retries |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SRC02 | bounded selected-variable | — | — | — | — | — | — | **E 1** | **E 0** | — | **H0 0** |
| SRC06 | bounded selected-variable | — | — | — | — | — | — | **E 1** | **E 0** | — | **H0 0** |
| SRC08 | metadata-only admission | — | — | — | — | **E 1** | — | **H0 0** | **E 0** | — | **H0 0** |
| SRC12 | metadata-only admission | — | — | — | — | **E 1** | — | **H0 0** | **E 0** | — | **H0 0** |
| SRC14 | bounded witness read | — | — | — | — | — | — | **E 1** | **E 0** | — | **H0 0** |
| SRC26 | header-prefix + metadata | — | — | — | — | **E 0** | **E 176 B** | **E 0** | **E 0** | **E 176/174/332** | **H0 0** |
| SRC27 | exactly one full route pass | **F1** | **F1** | — | — | **F1** | — | — | **F1** | — | **H0 0** |
| SRC35 | retained comparator | **H0 0** | — | — | — | — | — | — | — | — | **H0 0** |

Two rows carry enforceable non-count STOP triggers that must not be lost:

**SRC14 witness counts** — `user_missing 1917`, `ordinary_present 64363`,
`system_missing 0`, `total_rows 66280`; fixture `EVS08_DATE_MISSING_V372`,
fixture blob `12f6adb77ef5692511055c8f0520e42c454f3867`. Artifact 07's O1-C08
stop trigger: *"SRC14 counts differ from 1917/64363/0/66280, or the fixture
identity does not resolve."* **Fully enforceable.**

**SRC26 geometry** — raw nominal case size `174`, decoded dictionary data width
`332`, `equality_required: false`. Artifact 07: *"Geometry divergence between
raw header 174 and decoded dictionary width 332 is expected and NOT
equality-required."* Must be preserved **separately** and never collapsed.
Note `174` and `176` are different quantities — nominal case size versus the
bounded header-prefix byte quantity — and I have not conflated them.

---

## 6. SRC35 — outside the fresh-source target set, and not unconstrained

`SRC35` is **not** an eventual fresh-source access target, so it generates no
fresh-source access-layer accounts at all.

- C4B scope, verbatim: *"Seven future fresh-read sources only; SRC35 is excluded
  because it is a retained comparator."*
- Exclusion reason: `RETAINED_COMPARATOR__ZERO_FRESH_READ`
- Operation class `RETAINED_COMPARATOR_REPLAY_AND_COMPARE`, `fresh_reads: 0`
- Retry law: *"No fresh access at all. Replay uses retained material only."*
- Reader lane `NONE__RETAINED_ONLY`; read path *"NO FRESH LANE. Retained
  comparator; zero fresh raw reads."*; `materialises_frame: false`
- Global hard zero `WVS_SRC35_fresh_source_opens: 0`
- Locator: `NOT_REQUIRED__RETAINED_COMPARATOR__NO_FRESH_ACCESS`

Including SRC35 in a per-access-layer fresh-access binding would misrepresent a
retained comparator as an access target and would **weaken** the accounting.

**Explicitly: SRC35 is not unconstrained.** It carries a zero-fresh-read law, a
hard-zero global open budget, a retained-only lane and a zero retry budget.

---

## 7. Safety invariants — all verified on the successor candidate

| Invariant | Required | Actual | |
|---|---|---|---|
| `signed` | `false` | `false` | PASS |
| `issued` | `false` | `false` | PASS |
| `authorizes_access` | `false` | `false` | PASS |
| `execution_authorized` | `false` | `false` | PASS |
| `warrant_status` | not issued | `SUCCESSOR_CANDIDATE_ONLY__NOT_ISSUED__NOT_SIGNED__NO_RAW_ACCESS_AUTHORIZED` | PASS |
| locator slots unfilled | 7 | 7, all `<REQUIRED_FILL_IN_SLOT…>` | PASS |
| `max_retry_budget` | 0 on all 7 | 0 on all 7 | PASS |
| fresh-source target count | 7 | 7 | PASS |
| SRC27 route passes | 1 / max 1 | 1 / 1 | PASS |
| SRC35 in target set | false | false | PASS |
| raw-source operations | 0 | 0 | PASS |
| locator searches | 0 | 0 | PASS |

No field implies that creating this candidate authorizes hashing, statting,
metadata reads or file opens. The candidate says so in terms.

**Verification artifact:**
`WORKER_RETURNS/PYAT-HQ190-C-R9-WARRANT-ACCOUNTING-BINDING-R1/03_SUCCESSOR_CANDIDATE_VERIFICATION.json`
records the successor's SHA-256, byte count and full invariant check. The digest
is recorded there rather than inside the candidate, because a file cannot
contain its own digest.

---

## 8. Historical candidate preserved

| Field | Value |
|---|---|
| Path | `WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json` |
| Commit | `8ff40d37de69db2d8a6053a7c2242f481677f1a4` |
| Blob | `9f6b113151f7c05f0a22432b034347b631e1a895` |
| SHA-256 | `d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a` |
| Bytes | 17073 |

Re-verified at the freeze after this lane's writes: blob and SHA-256 both
unchanged. Not overwritten, not modified, not deleted. It is also **not on
this worker's ancestry** — the freeze is cross-lineage with merge-base
`87029d349c8a7385cb673060a8e5decd4eb528ff` — so overwriting was structurally
impossible as well as forbidden.

---

## 9. The eight unfilled issuance-time obligations

Every one names the accounts that cannot be bound, and a prohibition on the
specific fabrication that would be tempting.

| ID | Account | Sources | Exact value available | Named prohibition |
|---|---|---|---|---|
| R9-OBL-01 | existence/access checks | all 7 | **no** | MUST NOT be inferred from operation class, retry budget or any lane's estimate |
| R9-OBL-02 | full-file SHA-256 hash passes | all 7 | **no** | MUST NOT be set to 1 by reading the C4B precondition as a count |
| R9-OBL-03 | path-level opens | all 7 | **no** | MUST NOT be collapsed into a reader invocation or decoder call |
| R9-OBL-04 | decoder invocations | all 7 | **no** | MUST NOT be derived from selected-read or full-read figures |
| R9-OBL-05 | SRC27 lower-layer ceilings | SRC27 | **no** | MUST NOT be derived from `max_full_route_passes: 1` |
| R9-OBL-06 | SRC26 header-prefix read **count** | SRC26 | **no** | 176 is bytes, not a read count |
| R9-OBL-07 | metadata read counts where absent | SRC02, SRC06, SRC14, SRC26, SRC27 | **no** | MUST NOT be assumed zero merely because the class is a selected-variable read |
| R9-OBL-08 | byte counts where measurable | 6 sources | **no** | MUST NOT be fabricated |

R9-OBL-02 deserves emphasis. C4B's precondition says the locator *"resolves to
bytes whose full-file SHA-256 equals the frozen identity before decode."* That
establishes a hash pass is **required**. It does **not** say how many. Reading
it as `= 1` would be a fabrication dressed as a derivation.

---

## 10. A gap in the stop-trigger set, recorded not patched

Artifact 07's ten O1-C08 stop triggers govern **identity, locator, authority,
ordinals, runtime, reader lane, oracle custody, physical witness, named
consumer and dependency/currentness**.

**None of them tests an access-layer count against a bound.** Adding a
count-exceedance stop would require a bound that does not exist for four
accounts. I have recorded this gap rather than inventing thresholds to fill it.

---

## 11. What would actually close R9

Two lawful routes, neither available to this lane:

**(a) Supply governing evidence** that fixes exact per-source values for
existence/access checks, hash passes, path opens and decoder invocations, with
the four required measurement-basis fields each.

**(b) An instrument-level determination on the authorized execution surface**,
recorded with its measurement basis — which is itself a warrant-issuance-time
act requiring all seven locator fills plus HQ approval and required
user/resource-owner approval. **Neither the locators nor either approval
exists.**

Route (b) is where C4B always intended these numbers to come from. The correct
finding is that R9 is a *warrant-issuance-time* obligation that has been
partially discharged on paper, not a documentary defect that a document can
finish.

---

## 12. Claims not made

1. That R9 is closed at candidate grain.
2. Any value for existence/access checks, hash passes, path opens or decoder
   invocations.
3. That `expected_*` figures are declared maxima — no artifact says so.
4. That SRC27's four lower-layer accounts are bounded at 1 — only floors.
5. That SRC35 is unconstrained.
6. That creating this candidate authorizes any source operation.
7. That the historical candidate was modified, superseded or replaced.

---

Terminal:
`HQ190_C_R9_WARRANT_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED`