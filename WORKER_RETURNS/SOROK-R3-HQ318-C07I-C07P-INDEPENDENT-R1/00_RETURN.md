# SOROK HQ318 C07I — independent cross-process custody court

## VERDICT: `REVIEW_PASS_SCOPED_SOURCEFREE_C07_CROSSPROCESS_WITH_HOLDS`

**C07I is an independent acceptance of C07P's *scoped, source-free* cross-process result — with both
typed API holds still OPEN and the unkeyed anti-tamper ceiling PRESERVED and, in one respect, extended.**

| | |
|---|---|
| **Reviewer** | Fresh independent I2 experimental custody reviewer. **NOT** the C07P author, **NOT** the OC7 reviewer, **NOT** HQ, **NOT** an institutional escrow authority or signer. |
| **Branch** | `agent/reviewer-sorok-r3-hq318-c07i-c07p-independent-r1` |
| **Sealed startup** | `76649a99f4e8353bc6edfff0e1972c6068d28564`, verified against direct remote HEAD |
| **Candidate reviewed** | C07P `805d0a071db70bb37ec95df450b9429f46544fe9` |
| **Pinned native source** | OC6 blob `4c185c18dbee57603038e97886da8fc4aa834082`, SHA256 `ca85b844…` — **never edited** |
| **Author prereg reviewed** | `82ba75680f7cf296918c6236ef7c0e8df1756dde` |
| **Reviewer prereg** | `01_PREREGISTERED_REVIEWER_EXPECTATIONS_R1.md`, frozen at `536d90f88` **before any new adversarial execution** |
| **Environment** | New isolated local sparse worktree; Python 3.11.3 / pytest 9.1.1 / Git 2.39.1; real subprocesses |
| **Model / editor** | Step 5 Preview in OpenCode (owner-selected). One agent, no helpers, no switches. |

---

## 1. Unchanged reproduction

| Court | Result | Author claimed | |
|---|---|---|---|
| C07P v2 suite | **30 PASS / 0 RED** | 30 PASS | ✔ |
| inherited closure | **898 cases · 877 PASS · 21 RED · 0 skip** | 877 P / 21 RED | ✔ |

16/16 closure objects blob-verified from the true binary preimage, two `.tar.xz` members extracted
rather than transcribed. All **21 retained literal REDs** are recorded by name and suite in
`observations/c07i_retained_red_identities.json` and are exactly the 21 OC7 adjudicated: 10 historical
contract REDs, 9 self-invalidating OC5E witnesses, 2 disputed malformed homoglyph cases. **No RED was
edited, xfailed or suppressed.**

## 2. The cross-process claim is independently confirmed

Re-executed with **my own worker**, not the candidate's, so the claim does not rest on the author's
helper:

| Positive | Result |
|---|---|
| Distinct processes, pinned module in both | PIDs `63441` / `63442`; blob `4c185c18…`, SHA256 `ca85b844…`, 36 648 bytes |
| B restores via public-API replay | `chain.ok`, `verify_ledger_integrity() == True` |
| All 18 capsule fields + seal byte-equal across the boundary | confirmed; 18/18 perturbations change the seal |
| Canonical JSONL: contiguous `seq`, chained `prev`, correct `rec`, byte-identical canonical form | confirmed |
| Single stable head digest identifies the journal | confirmed |
| B safely continues the lifecycle | `['cap-A','cap-B']` committed and released, integrity `True` |

## 3. Crash timing — four points, one deliberately left unsettled

Real uncatchable `SIGKILL` (exit `137`), in place. **No torn record at any point.**

| Point | Observed | Classification |
|---|---|---|
| before temp fsync | previous journal intact, `cap-C` absent | `CLEAN_ROLLBACK` |
| after temp fsync, pre-rename | previous journal intact, **orphaned temp** | `CLEAN_ROLLBACK` |
| post-rename, pre-dir-fsync | new journal visible | **`NOT_SETTLED`** |
| post-dir-fsync | new journal, temp absent | `COMMITTED` for *process* death only |

The before-fsync point was reached **without editing the adapter**: the candidate exposes no hook there,
so I shadowed `os.fsync` inside my own worker and killed the process the instant the adapter first
requests a flush.

**The post-rename observation is explicitly NOT classified as power-loss durability.** A `SIGKILL` kills
the process; the page cache survives, so those bytes are visible whether or not the directory entry was
made durable. Settling it needs a real power cut or a separate filesystem — neither authorised. Any
future document reading it as durability proof is wrong.

## 4. The ceiling is preserved — and I found a second route into it

This is the substance of the review.

**Re-confirmed (author's route):** a self-consistent earlier prefix with **all hashes recomputed**
restores with no refusal, `verify_ledger_integrity()` returns `True`, and `cap-B` is **silently lost**.
Truncating to an even shorter prefix is equally invisible.

**New route, preregistered in advance as ACCEPTED and then observed:** an attacker rewrites a COMMIT
record's capsule fields **and** rewrites the recorded `commitment` to match **and** re-seals the whole
chain. **Observed: accepted.** The restored escrow materialises `content_digest="attacker-digest"` and
`scenario_frame="attacker-frame"` with `verify_ledger_integrity() == True`.

Both defences C07P relies on — the per-record chain and the capsule commitment — are **unkeyed digests
computed by the party that writes the file**. Rewriting the data and the digest together defeats both at
once. My IH10 test was written to **fail loudly** if this were ever refused, so a future improvement
cannot be silently absorbed into the ceiling.

**An unkeyed hash plus an ordinary local file establishes no external trust anchor.** Closing this needs
an external append-only anchor, a key held outside the journal's trust domain, or an OS-protected store
the local process cannot recompute — i.e. exactly the real institutional custody no worker may invent.

I found **three hostiles the candidate's own suite does not cover** — whole-journal fork into one file
(IH5), non-canonical/pretty-printed JSON (IH8), and an *extra* capsule field key (IH18b). All three are
correctly refused.

## 5. Both typed holds confirmed OPEN by direct measurement

| Hold | Measurement | Status |
|---|---|---|
| `C07_DEPENDENCY_TS` | `inspect.signature` shows **no** `at`/`timestamp` on `unblind` or `record_exposure`; escrow times differ from the journal's after replay **while integrity stays `True`** | **OPEN** |
| `C07_DEPENDENCY_REVOKE` | `dir(EscrowState)` has **no** `revoke*`/`deauthor*` | **OPEN** |

Because revocation is not expressible, **this review makes no revoked-custodian cross-process claim.**
I did not touch private dicts, did not mutate `holder_roles`, and did not force either expectation
green. An AST check proves the adapter itself uses no `pickle` import, no `__setattr__` call and no
subscript access to escrow internals.

## 6. Every defence is load-bearing

| Mutant | Killed by | Result |
|---|---|---|
| M-A — neuter per-record digest | `test_IH1_tampered_payload_is_refused` | 1 failed / 44 passed |
| M-B — neuter capsule-commitment re-check | `test_IH9_capsule_substituted_with_chain_resealed_is_refused` | 1 failed / 44 passed |
| M-C — replace `os.replace` with a plain write | `test_IC4_crash_after_dir_fsync_has_no_temp_left` | 1 failed / 44 passed |

Adapter restored to blob `def46aed3288117903b961e66dc0259c1fa44d6b` and re-verified green.

## 7. My own errors, disclosed

First execution: **2 failed, 42 passed, 1 xfailed**. Preserved in
`observations/c07i_independent_v1.{xml,log}` and adjudicated in `04_REVIEWER_CORRECTION_LEDGER.json`.
All three were defects in **my** tests:

1. **A logic inversion in IH10** — I called `xfail` on the branch where the forged capsule *was*
   accepted, while labelling that branch "stronger than expected". Acceptance is the preregistered
   ceiling and must pass. Now asserted directly, with a loud failure if it is ever refused.
2. IH15 snapshot ordering — I ran "continue" before the journal existed, so both files had 5 records.
3. IH-T3 substring scan — searching for `"pickle"` matched the adapter's own docstring *"Never pickles a
   live object"*, which documents the **correct** behaviour. Replaced with AST analysis.

Corrected: **45 passed / 0 failed.**

## 8. Reviewer custody note

The HQ318 **sealed startup does not contain the C07P return tree at all** — it branches from `c0d8d84d`,
which predates C07P, and `805d0a07` is not an ancestor of this branch. This is not a C07P defect and
nothing of C07P's was altered. It is exactly why I staged the candidate **by pinned commit and
authenticated blob** rather than by checking it out; had I trusted the working tree I would have
reviewed nothing.

Verified unmodified at the end of this review:

- pinned OC6 `custody_protocol.py` → `4c185c18dbee57603038e97886da8fc4aa834082`
- C07P adapter `c07_journal.py` → `def46aed3288117903b961e66dc0259c1fa44d6b`
- C07P worker `c07_worker.py` → `d0c5797afa6993d852f2e0c75efcbc2cdd491eca`

## 9. Explicitly NOT claimed

No production durability. **No real power-loss durability.** No external or third-party escrow. No
independently protected log. No signer authority issued. No holder-authority issuance or revocation.
**No C07 pass on arbitrary crashes.** No semantic adoption or leakage-gate widening. No production, V3,
N12, CURRENT or PRE-MAIN privileges. No original respondent data, protected holdout or real experiment
model call.

**Acceptance grain:** a bounded source-free, single-machine, local-file custody prototype. Adopting it
beyond that grain remains the competent owner's decision, and this review does not adopt its own work.

## 10. Artifacts

| Path | Purpose |
|---|---|
| `01_PREREGISTERED_REVIEWER_EXPECTATIONS_R1.md` | reviewer expectations, frozen at `536d90f88` **before execution** |
| `02_THREAT_AND_NEGATIVE_ADJUDICATION_R1.md` | full threat adjudication, ceiling, holds, custody note |
| `03_CROSS_PROCESS_COLD_EVIDENCE.md` | real A/B/C transcripts and field-by-field comparison |
| `04_REVIEWER_CORRECTION_LEDGER.json` | my 3 corrections + mutation controls + ceiling record |
| `environment_passport_delta.json` | `SOROK_WARM_ENVIRONMENT_PASSPORT_R1` |
| `observations/` | JUnit + stdout for every court, 21 RED identities, staging ledger, mutation evidence |
| `repro/c07i_stage.py` | 16/16 blob-authenticated closure staging |
| `repro/c07i_worker.py` | reviewer-authored process roles |
| `repro/c07_journal.py`, `repro/c07_worker.py`, `repro/source/custody_protocol.py` | candidate under review, unedited |
| `tests/test_c07i_independent.py` | 45 independent adversarial cases |
