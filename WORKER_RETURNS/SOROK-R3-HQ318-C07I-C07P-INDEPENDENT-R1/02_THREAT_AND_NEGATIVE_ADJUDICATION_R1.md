# SOROK HQ318 C07I — threat and negative-result adjudication

All rows are **observed by the reviewer**, preregistered in
`01_PREREGISTERED_REVIEWER_EXPECTATIONS_R1.md`, and executed with real subprocesses and real
filesystem state. Nothing here is inherited from the C07P return's own tables.

## 1. Cross-process custody claim — INDEPENDENTLY CONFIRMED

| # | Claim | Reviewer result |
|---|---|---|
| IP1 | A builds the authorised lifecycle through the public API only | **confirmed** — ops `COMMIT, UNBLIND, RELEASE, EXPOSURE`, `verify_ledger_integrity() == True` |
| IP2 | A and B are distinct processes on the pinned module | **confirmed** — PIDs `63441` / `63442`; blob `4c185c18…`, SHA256 `ca85b844…`, 36 648 bytes in both |
| IP3 | B restores by public-API replay with integrity | **confirmed** — `chain.ok`, `integrity True` |
| IP4 | all 18 capsule fields and the seal are byte-equal across the boundary | **confirmed** |
| IP5 | every one of the 18 fields is bound to the seal | **confirmed** — 18/18 perturbations change the commitment |
| IP6 | canonical JSONL, contiguous `seq`, chained `prev`, correct `rec` | **confirmed** — every line round-trips to its canonical form byte-for-byte |
| IP7 | B can continue the lifecycle safely | **confirmed** — `['cap-A','cap-B']` committed and released, integrity `True` |
| IP8 | a single head digest identifies the journal and is stable | **confirmed** |

The A→B result is reproduced with **reviewer-authored tooling**, not the candidate's own worker.

## 2. Crash timing — observed, and one point deliberately left unsettled

Real, uncatchable `SIGKILL` (exit `137`) delivered in place.

| # | Point | Observed | Reviewer classification |
|---|---|---|---|
| IC1 | before temp fsync | previous journal intact, restore succeeds, `cap-C` absent | `CLEAN_ROLLBACK` |
| IC2 | after temp fsync, pre-rename | previous journal intact, **orphaned temp present**, restore succeeds | `CLEAN_ROLLBACK` |
| IC3 | post-rename, pre-dir-fsync | new journal visible, restore succeeds | **`NOT_SETTLED`** |
| IC4 | post-dir-fsync | new journal present, temp absent, restore succeeds | `COMMITTED` for *process* death only |
| IC5 | all four | journal parses cleanly, chain verifies, **no torn record** | — |

**IC1 was reached without editing the adapter.** The candidate exposes no crash hook before the temp
file is fsynced, so the reviewer shadowed `os.fsync` inside its **own worker only**, killing the process
the instant the adapter first requests a flush. That is a genuine pre-fsync kill.

### 2.1 The refusal rule, honoured

**IC3 and IC4 are observations about process death only.** A `SIGKILL` does not exercise power-loss
semantics: the kernel page cache survives, so post-rename bytes remain visible whether or not the
directory entry was made durable.

Neither point is evidence of durability across a machine crash or power loss, and **neither is
classified as such here.** Settling IC3 would need a real power cut or a separate filesystem, neither of
which is authorised. Any future document that reads IC3 as durability proof is wrong.

## 3. Hostiles — refused as expected

| # | Attack | Refused by | Observed message |
|---|---|---|---|
| IH1 | payload byte tampered | per-record unkeyed SHA-256 | `digest mismatch … payload tampered` |
| IH2 | middle record deleted | seq contiguity | `record N: seq is …` |
| IH3 | two records swapped | seq / prev chain | `seq is` / `prev chain break` |
| IH4 | record duplicated | seq contiguity | `record N: seq is …` |
| IH5 | **whole journal forked into one file** | seq contiguity | `record N: seq is …` |
| IH6 | trailing bytes after the final newline | strict parse | refusal |
| IH7 | final record truncated mid-line | strict parse | refusal |
| IH8 | pretty-printed / non-canonical JSON | canonical re-serialisation | refusal — **not silently accepted as canonical** |
| IH9 | capsule substituted, chain **re-sealed** | capsule commitment | `forged capsule` |
| IH11 | unblind of an uncommitted capsule | native escrow | `IdentityMismatchError` |
| IH12 | exposure of an uncommitted capsule | native escrow | `IdentityMismatchError` |
| IH13 | unblind by a holder with no grant | native escrow | `IdentityMismatchError` |
| IH14 | holder rewritten on an already-unblinded capsule | native escrow | refused |
| IH16 | blank line inserted inside the journal | strict parse | `blank line inside journal` |
| IH17 | unknown record `kind` | record builder | `unknown journal kind` |
| IH18 | capsule field set missing **or extra** | field-set check | `field set mismatch` |

IH5, IH8 and IH18's *extra-key* half are **cases the candidate's own suite does not cover**; the
reviewer added them and they all behave correctly.

## 4. The ceiling — PRESERVED, and extended by one route

This is the most important section. The commission requires the demonstrated ceiling be preserved, not
repaired. It was, and the reviewer found a **second, distinct route** to the same failure.

### 4.1 IC-A — self-consistent prefix rollback (author's route, re-confirmed)

Rewinding to the earlier cap-A prefix **and recomputing every hash** restores with **no refusal**,
`verify_ledger_integrity()` returns `True`, and `cap-B` is **silently lost**.

### 4.2 IC-B — the escrow cannot tell

Both the journal chain check and the native escrow integrity check report success on the rolled-back
state. This is precisely why a local unkeyed journal is not a trust anchor.

### 4.3 IC-C — truncating to an even shorter prefix is equally invisible

Reducing the journal to a single `AUTHORIZE` record restores to an **empty escrow** with
`verify_ledger_integrity() == True`. Same class, different magnitude.

### 4.4 IH10 — NEW route found by the reviewer, preregistered as ACCEPTED

The candidate's documented ceiling is prefix rollback. The reviewer preregistered, in advance, that the
following would **also** be accepted:

> An attacker edits a COMMIT record's capsule fields **and** rewrites the recorded `commitment` so it
> matches, then re-seals the whole chain.

**Observed: accepted.** The restored escrow carries `content_digest="attacker-digest"` and
`scenario_frame="attacker-frame"`, and `verify_ledger_integrity()` returns `True`.

Both defences the candidate relies on — the per-record chain and the capsule commitment — are
**unkeyed digests computed by the same party that writes the file**. Rewriting the data and the digest
together defeats both simultaneously. The preregistration anticipated this, so it is reported as part
of the ceiling rather than as a surprise.

Had it been *refused*, the test would have **failed loudly** with "stronger than preregistered" rather
than silently accepting the better outcome. It did not.

### 4.5 What would actually close this

1. An **external append-only anchor** the writer cannot rewind.
2. A **key held outside the journal's trust domain** — HSM, remote custody, threshold-signed log.
3. An **OS-protected store** the local process cannot recompute.

None exists here. Inventing one is a real institutional-custody authority that this review may not
fabricate. **An unkeyed hash plus an ordinary local file establishes no external trust anchor.**

## 5. Holds — both confirmed OPEN by direct measurement

| # | Hold | Reviewer measurement | Status |
|---|---|---|---|
| IH-T1 | timestamp-faithful replay impossible | `inspect.signature` shows **no** `at`/`timestamp` parameter on `unblind` or `record_exposure`; measured escrow times differ from the journal's after replay, **while integrity stays `True`** | **OPEN** |
| IH-T2 | holder revocation not expressible | `dir(EscrowState)` has **no** `revoke*`/`deauthor*`; only `authorize_holder` | **OPEN** |

Because IH-T2 is open, **this review makes no revoked-custodian cross-process claim at all.** The
reviewer did not access private dicts, did not mutate `holder_roles`, and did not force either
expectation green. An AST check (`IH-T3`) verifies the adapter itself contains no `pickle` import, no
`__setattr__` call and no subscript access to escrow internals — note this needed AST because a
substring scan falsely matched the adapter's own docstring, which legitimately contains the word
"pickles".

## 6. Mutation discrimination — every defence is load-bearing

| Mutant | Change | Killed by | Result |
|---|---|---|---|
| M-A | neuter the per-record digest comparison | `test_IH1_tampered_payload_is_refused` | 1 failed / 44 passed |
| M-B | neuter the capsule-commitment re-check on restore | `test_IH9_capsule_substituted_with_chain_resealed_is_refused` | 1 failed / 44 passed |
| M-C | replace `os.replace` with a non-atomic plain write | `test_IC4_crash_after_dir_fsync_has_no_temp_left` | 1 failed / 44 passed |

The adapter was restored to blob `def46aed3288117903b961e66dc0259c1fa44d6b` afterwards and re-verified
green. Each defence is independently load-bearing; the suite is not trivially satisfied.

## 7. Preservation of the accepted custody boundary

Both accepted courts were run **unchanged**, against the pinned OC6 source, with 16/16 closure objects
blob-verified from the true binary preimage (two `.tar.xz` members extracted, never transcribed):

| Court | Cases | PASS | RED | skip |
|---|---:|---:|---:|---:|
| inherited 131 (OC1/OCR1/OC2/OC3) | 131 | 121 | **10** | 0 |
| OC4 author controls | 36 | 36 | 0 | 0 |
| OC5 prior predictions | 23 | 23 | 0 | 0 |
| OC5E native hostiles | 159 | 148 | **11** | 0 |
| OC6 author controls | 273 | 273 | 0 | 0 |
| OC7 independent v2 | 276 | 276 | 0 | 0 |
| **total** | **898** | **877** | **21** | **0** |

C07P v2 ran unchanged: **30 PASS / 0 RED**.

All **21 retained literal REDs** are recorded by name and suite in
`observations/c07i_retained_red_identities.json`, and are exactly the 21 OC7 adjudicated: 10 historical
contract REDs, 9 self-invalidating OC5E witnesses (including the pinned-unrepaired-blob provenance
pin), and the 2 disputed malformed homoglyph cases. **No RED was edited, xfailed or suppressed.**

## 8. Reviewer custody note — a divergence worth recording

The HQ318 **sealed startup `76649a99f` does not contain the C07P return tree at all.** It branches from
`c0d8d84d` (the HQ317 fan-in), which predates C07P's work; `git merge-base --is-ancestor` confirms
`805d0a07` is **not** an ancestor of this review branch, and the 42 C07P files are absent from the
startup tree.

This is not a defect in C07P, and nothing of C07P's was altered here. It is exactly why the review
staged the candidate **by pinned commit and authenticated blob** (`git cat-file` + recomputed binary
preimage + SHA-256 + `git rev-parse` cross-check) rather than by checking it out. Had the reviewer
relied on the working tree, it would have reviewed nothing at all.

Verified unmodified at the end of this review:

- pinned OC6 `custody_protocol.py` → `4c185c18dbee57603038e97886da8fc4aa834082`
- C07P adapter `c07_journal.py` → `def46aed3288117903b961e66dc0259c1fa44d6b`
- C07P worker `c07_worker.py` → `d0c5797afa6993d852f2e0c75efcbc2cdd491eca`
