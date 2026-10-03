# PYAT HQ195 — R9 governing-contract independent interpretation — R1

**Disposition:** `CONTRACT_REQUIRES_LITERAL_PATH_OPEN_ACCOUNT__RUNTIME_OR_ARCHITECTURE_CHANGE_REQUIRED`

**Terminal:** `HQ195_R9_CONTRACT_INTERPRETATION_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq195-r9-contract-independent-interpretation-r1`
Commissioned startup SHA: `a48acdc2f7e26557fca8e387b12c619bb94fe447` — **verified equal**.
Checkout mode: `SPARSE_REQUIRED` — **honored**. Canonical clone used; **no clone, no full
worktree**; sparse checkout **not widened**; every historical authority read by exact Git
object (`git show`).

Reviewer identity: DeepSeek Harness, **DeepSeek V4.1 Flash**. The parallel Space Bunny
stage-ownership branch/return was **not opened** before this interpretation was formed.

---

## 1. The answer in one paragraph

The frozen contract **requires a literal OS-level path-open account**, and the qualified
runtime **cannot produce it**. The requirement is not ambiguous: O1-C07 names
"path-level opens and their measurement basis" as a separate mandatory account, the C4
accounting law enumerates it among ten *mandatory separate accounts*, the C4B template gives
that one slot the unique qualifier `REQUIRED_EXACT_COUNT_AND_BASIS`, and the law contains an
explicit warning that OS-level path opens, reader invocations and decoder calls *"are
different quantities"* frozen *"as separate accounts"*. A higher-level proxy therefore does
**not** discharge R9. Crucially, the stage rule is **not** the problem: *"Freeze expected
budgets and instrumentation before launch; retain measured counts"* is a clean two-stage
obligation — budgets/instrumentation frozen, counts measured — so a pre-launch budget and a
runtime-measured exact count are not merely compatible, they are the required structure. The
blocker is a **capability** blocker against an unambiguous requirement.

## 2. Startup and read-law compliance

| Step | Result |
|---|---|
| `git fetch origin` (no blind pull) | OK |
| review branch == `a48acdc2f…` | **MATCH** |
| commission read from exact object | OK |
| sparse worktree via canonical `prepare_sparse_worktree.sh` | `SPARSE_WORKTREE_READY` |
| sparse patterns | exactly the three commissioned paths |
| sparse checkout widened | **NO** |
| historical authorities read by `git show` | **YES** (never checked out) |
| parallel stage-ownership branch read | **NO** |

## 3. What must be frozen before launch

From *"Freeze expected budgets and instrumentation before launch"*:

1. **The account SET** — the ten mandatory separate accounts, fixed in advance rather than
   discovered at runtime.
2. **The instrumentation** — the measurement mechanism per account, chosen and frozen.
3. **The measurement basis per account** — *"what was measured, at which layer, by what
   mechanism, at what point in the run"*.
4. **Expected budgets** where a budget exists.
5. **Hard-zero constraints** — WVS/SRC35 fresh opens, excluded-source fresh opens, Candidate
   A/B/C, measured P2X, raw respondent pooling, new cross-source joins, SRC08/SRC12 row-data
   reads and selected columns, all `= 0`, where *"a single non-zero count ... is a STOP
   condition, not a reportable variance."*
6. **Per-source operation-class expectations** (e.g. SRC02 `expected_selected_reads = 1`,
   SRC27 `expected_full_route_passes = 1`).
7. **Retry/stop law** — frozen maximum **zero** retries across all eight sources.
8. **Runtime identity/qualification** (adjacent `O1-C05`).

## 4. What is measured during execution

The **observed count per account, retained and returned with its basis**. Ten accounts are
enumerated; on the exercised path seven are governed and enforceable (HQ191), while
`path-level opens + basis`, selected-column reads and byte counts are not governable at any
enforceable layer, and header-prefix reads are not performed by the exercised decoder path.

## 5. What `REQUIRED_EXACT_COUNT` means here

**Context-dependent in object, constant in force.** The token forces the slot to carry an
*exact* value; it does **not** force every eventual observed count to be numerically known
before launch. Concretely:

- `frozen_zero_budgets` and per-source `expected_*` are **pre-launch declarations**, exact by
  construction.
- Runtime accounts are **exact measured counts**, reported with their basis.

Two readings were tested and one is defeated:

- *"every final measured count must be known before launch"* — **defeated**, because it makes
  *"retain measured counts"* meaningless and would require the run to have already happened.
- *"reader invocations are close enough"* — **defeated**, see §6.

The `_AND_BASIS` / `_AND_CONFIG` / `_AND_REASON` suffixes are exactly the pre-launch
invariants that must accompany the runtime count.

## 6. Literal OS path-open accounting is non-substitutable

| Evidence | Bearing |
|---|---|
| **Q5 explicit warning**: *"A count of 'opens' is meaningless without stating whether it means OS-level path opens, reader invocations, or decoder calls. **These are different quantities** and C4B froze them as separate accounts."* | Names the substitution and forbids it |
| **Q3** lists `path-level opens` **and** `decoder invocations` as separate accounts | Collapsing them is incoherent |
| **Q4**: *"Each account must state its measurement BASIS ... A count without a stated basis is not an account."* | A proxy states the wrong basis → **not an account at all** |
| **Q8**: `path_opens` uniquely carries `_AND_BASIS` | Deliberately the hardest, least substitutable slot |
| **Q6**: the SRC27 single pass *"does NOT license assuming one file open"*; that misreading is *"expressly forbidden by Omega-1"* | Forbids the analogous collapse |
| **Q2**: *"Access must be separately accounted at every distinct layer."* | Absolute in form |
| **Q11/Q12/Q14** independent prior findings | ACC-03 unbound; neither count nor basis observable; proxy explicitly **not** relabelled |

HQ191's refusal to relabel is the correct behaviour and the strongest practical confirmation:
it reports the reader-invocation ceiling as *"an upper bound on accesses, NOT an account of
opens"*.

## 7. Can a pre-launch budget coexist with a runtime-measured exact count?

**Yes, and it is the required structure.** The two objects are an **authorization** (frozen
before launch: budgets, instrumentation, basis, zeros, retry law) and **evidence** (measured
during execution and returned). For `ACC-03` the *budget/instrumentation* side is itself
unsatisfiable on this host, because neither a count nor a basis is obtainable — which is why
R9 remains open even though the stage rule is clear.

## 8. Nature of the inability

- **Not a warrant-document defect.** The requirement is stated three times and carries the
  strongest qualifier. *(The warrant candidate did separately omit the per-source
  `source_access_accounting` block — a real completeness gap found by HQ192/HQ190-C — but
  restoring it does not make ACC-03 measurable.)*
- **Not authority ambiguity as to meaning.** Only one reading is textually supported.
- **Part implementation gap**, but not closable within the current unprivileged authority:
  DYLD interposition and `__DATA,__interpose` both fail, SIP is enabled, and root tracing is
  outside the no-sudo authority.
- **An architecture warrant is indicated** at the measurement grain — a required named
  account the existing jurisdictions cannot represent or lawfully succeed. *Indicated only:
  declaring it is an authority act this review does not perform.*
- **The remedy is open; the meaning is not.** Building an instrumented reader surface,
  authorizing privileged tracing, or formally **amending** the frozen contract are all
  available governance choices — the last being a contract *change*, not an interpretation.

## 9. Strongest case for the other side (and why it fails)

Fully developed in `03_COMPETING_INTERPRETATIONS.md`. In brief, the proxy reading leans on
purpose ("anti-collapse is served"), the `where measurable` hedge, conservatism of an upper
bound, AT20's "declared read/decoder counts ... remain exact", and practicality. It fails
because the contract **explicitly enumerates** the quantities as different; `where
measurable` attaches to *byte counts* specifically, not as a general licence; the conservatism
argument is filed under a different account; AT20's exactness concerns the *declared* count;
and practicality is barred — the commission says convenience is not authority.

## 10. Answers to the four acceptance questions

1. **What must be frozen before launch** — budgets, instrumentation, basis fields, hard zeros, per-source expectations, retry/stop law (§3).
2. **What is measured during execution** — the exact observed count per account with its basis (§4).
3. **`REQUIRED_EXACT_COUNT`** — exactness is mandatory; the *object* of the exactness is context-dependent (§5).
4. **Is literal OS path-open accounting non-substitutable?** — **YES** (§6). A pre-launch budget can and must coexist with runtime-measured counts (§7). The current inability is a **runtime/architecture capability** problem, not a document defect and not meaning-ambiguity (§8).

## 11. Holds observed

Zero raw-source access; zero locator discovery; zero warrant issuance; zero live C4; zero
production mutation; zero C7/actor work. No adoption or self-adoption. Nothing written
outside the commissioned return directory. Every historical authority was read as a Git
object; the sparse checkout was never widened.
