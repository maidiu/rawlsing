# SOROK HQ318 C07I — independent preregistered expectations

**Status:** `FROZEN_BEFORE_EXECUTION` by the C07I reviewer.
**Reviewer:** fresh independent I2 experimental custody reviewer. **NOT** the C07P author, **NOT** the
OC7 reviewer, **NOT** HQ, **NOT** an institutional escrow authority or signer.
**Candidate under review:** C07P `805d0a071db70bb37ec95df450b9429f46544fe9`.
**Author prereg reviewed:** `82ba75680f7cf296918c6236ef7c0e8df1756dde`.

This document fixes my expectations **before** I run a single new adversarial case. Nothing here may be
edited to match an observed result; a wrong expectation is reported as a finding and corrected only in
a new file with a new freeze.

---

## 1. Independence statement

- A **new** isolated worktree was created for this review. The C07P worktree was not reused and no
  filesystem or runtime state was assumed to carry over.
- The C07P adapter `c07_journal.py` is treated as **code under test**, not as trusted scaffolding. Its
  `EscrowJournal` and helper functions are used only where the mission requires exercising the
  candidate, and every one of its defences is independently re-attacked below.
- I wrote **my own** process worker (`repro/c07i_worker.py`) with my own identity probe, rather than
  reusing `c07_worker.py`, so that the A→B claim does not depend on the author's own helper.
- **I did not modify the pinned OC6 custody source or the C07P adapter.** No byte.

## 2. Preregistered reproduction (already executed, recorded as the baseline)

Both courts run **unchanged**:

| Court | Preregistered expectation | Observed |
|---|---|---|
| C07P v2 suite | 30 PASS | **30 PASS** ✔ |
| inherited closure | 898 cases, 877 PASS, 21 literal RED, 0 skip | **898 / 877 / 21 / 0** ✔ |

All **21 retained RED identities** are recorded by name and suite in
`observations/c07i_retained_red_identities.json`, and must be the same 21 OC7 adjudicated: 10 historical
contract REDs in `inherited_131`, 9 self-invalidating OC5E witnesses, 2 disputed malformed homoglyph
cases.

## 3. Preregistered independent positives

| # | Expectation |
|---|---|
| **IP1** | Process A builds COMMIT/UNBLIND/RELEASE/EXPOSURE through the public API only; `verify_ledger_integrity() == True`. |
| **IP2** | Process A and process B are **distinct OS processes with distinct PIDs**, and B's `module.__file__` is the pinned OC6 file with Git blob `4c185c18…` and SHA256 `ca85b844…`. |
| **IP3** | B restores via public-API replay and reports `verify_ledger_integrity() == True`. |
| **IP4** | Every one of the **18** capsule fields is byte-equal between A and B, and the envelope commitment is byte-equal. |
| **IP5** | Perturbing **any one** of the 18 fields to another *valid value of the same type* changes the commitment. (Bool is tested before int: `isinstance(False, int)` is `True` in Python.) |
| **IP6** | Journal is canonical JSON Lines: each line round-trips through `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=True)` byte-for-byte; `seq` is contiguous from 1; `prev` chains; every `rec` equals the recomputed digest. |
| **IP7** | B can **continue** the lifecycle (second capsule) and integrity still holds afterwards. |
| **IP8** | `verify_chain` returns a single `head` digest that identifies the whole journal, and the head is stable across independent reads. |
| **IP9** | The journal's stored `unblinded_at` / `exposure_ts` are **byte-equal** between A and B. |
| **IP10** | The reconstructed escrow's **own** event timestamps are expected to **differ** from the journal's — this is `C07_DEPENDENCY_TS`, and I expect to *measure* the drift rather than take it on trust. |

## 4. Preregistered crash timing

Real, uncatchable `SIGKILL` (expected exit `137`) delivered **in place** in the write protocol.

| # | Crash point | Preregistered expectation |
|---|---|---|
| **IC1** | `0_before_tmp_fsync` — reached by shadowing `os.fsync` **in my worker only**, since the adapter exposes no hook there | Previous journal intact; temp file exists but is not fsynced; restore succeeds; the attempted capsule is **not** present. |
| **IC2** | `1_after_tmp_fsync_before_replace` | Previous journal intact; orphaned temp; restore succeeds; attempted capsule **not** present. |
| **IC3** | `2_after_replace_before_dir_fsync` | New journal visible; restore succeeds. **MUST be classified `NOT_SETTLED`, never as power-loss durability.** |
| **IC4** | `3_after_dir_fsync` | New journal present, temp absent; restore succeeds. |
| **IC5** | At every crash point | The journal parses cleanly, the chain verifies, and **no torn or partial record** appears. |

### 4.1 Refusal rule for crash point 3-of-4

A process `SIGKILL` does not exercise power-loss semantics; the page cache survives. Therefore IC3 and
IC4 are observations about **process** death only. I will not describe either as proving durability
across a machine crash, and any such claim in a future document is wrong.

## 5. Preregistered independent hostiles

| # | Attack | Preregistered expectation |
|---|---|---|
| **IH1** | Payload byte tampered | refused — `digest mismatch` |
| **IH2** | Middle record deleted | refused — seq contiguity |
| **IH3** | Two records swapped | refused — seq / prev chain |
| **IH4** | Record duplicated | refused — seq |
| **IH5** | Whole journal replayed twice into one file (fork) | refused — seq |
| **IH6** | Trailing bytes appended after the final newline | refused — trailing-garbage refusal |
| **IH7** | Final record truncated mid-line | refused |
| **IH8** | Non-canonical JSON (pretty-printed / spaced / unsorted keys) | refused or non-matching digest; **must not be silently accepted as canonical** |
| **IH9** | Capsule fields substituted, then **the whole chain re-sealed** so digests are self-consistent | refused — capsule commitment mismatch |
| **IH10** | Capsule substituted **and its recorded `commitment` updated** to match | see 5.1 — expected outcome is stated there, not assumed |
| **IH11** | UNBLIND for a capsule that was never committed | refused — native `IdentityMismatchError` |
| **IH12** | EXPOSURE for a capsule that was never committed | refused — native `IdentityMismatchError` |
| **IH13** | UNBLIND by a holder with no grant | refused — native `IdentityMismatchError` |
| **IH14** | UNBLIND attributed to the wrong holder after a legitimate unblind | the escrow's own integrity check must reject the materialised inconsistency |
| **IH15** | Journal from an **older source state** (old-capsule alias) presented as current | behaviour recorded precisely; see 5.2 |
| **IH16** | `blank line` inserted inside the journal | refused |
| **IH17** | unknown record `kind` | refused — unknown kind |
| **IH18** | capsule field set missing/extra | refused — field-set mismatch |
| **IH19** | Empty (zero-byte) journal | refused or treated as empty — recorded, not asserted to be safe |

### 5.1 IH10 — the interesting one, stated in advance

If an attacker edits a COMMIT record's capsule fields **and** rewrites the recorded `commitment` so it
matches, the per-record chain and the commitment check both pass. My preregistered expectation is that
**this is accepted**, because the commitment is an unkeyed digest computed by the same attacker. This
is the same class of failure as IH16/prefix rollback and must be reported as part of the ceiling, not
as a pass. If it is instead refused, that is a *stronger-than-expected* result and I will say so
explicitly rather than quietly accepting the better outcome.

### 5.2 IH15 — old source-state alias

A journal produced from an earlier, legitimate escrow state is, byte-for-byte, a valid journal. I
expect restore to succeed and to reconstruct the *old* state with no error. This is not a bug; it is
the same prefix-rollback ceiling reached by a different route, and I will record it as such.

## 6. Preregistered preservation of the demonstrated ceiling

I must **preserve**, not repair, the following finding. If any of my own tests accidentally make it
look fixed, that is an error in my tests.

> A local unkeyed journal **cannot** detect a coherent rollback by an attacker who controls both the
> journal bytes and the digest. A fully self-consistent earlier prefix restores successfully, reports
> integrity `True`, and silently loses later events.

| # | Expectation |
|---|---|
| **IC-A** | Rewinding to a self-consistent earlier prefix, with **all hashes recomputed**, restores **without any refusal** and silently drops the later events. |
| **IC-B** | `verify_ledger_integrity()` returns `True` on that rolled-back state — the escrow cannot tell. |
| **IC-C** | No reviewer-side hardening, monkeypatch or private-dict access may be used to make this look detected. |

## 7. Preregistered open holds — must remain OPEN

| # | Expectation |
|---|---|
| **IH-T1** | `unblind` / `record_exposure` expose **no** timestamp parameter, so escrow event times cannot be restored faithfully. I expect to measure a non-zero drift and confirm the signature has no `at`. |
| **IH-T2** | `EscrowState` exposes **no** `revoke_holder`. I expect to confirm its absence, and therefore I will **not** claim any revoked-custodian cross-process proof. |
| **IH-T3** | I will not access `state.ledger`, `state.holder_roles`, `_event_proofs` or `_capsule_seals` for mutation in order to force any expectation green. |

## 8. Preregistered mutation discrimination

Re-run the C07P-documented mutation controls, adapted to this staged layout, to check the defences are
load-bearing rather than incidentally satisfied:

| Mutant | Change | Preregistered expectation |
|---|---|---|
| **M-A** | neuter the per-record digest comparison | a tampering test turns RED |
| **M-B** | neuter the capsule-commitment re-check on restore | the forged-capsule test turns RED |
| **M-C** | replace `os.replace` with a non-atomic plain write | a crash/atomicity test turns RED |

## 9. Preregistered verdict options

Only one of:

- `REVIEW_PASS_SCOPED_SOURCEFREE_C07_CROSSPROCESS_WITH_HOLDS`
- `REVIEW_REVISE`
- `REVIEW_HOLD`

Whichever is issued, the following are **not** claimed and cannot be granted by this review: production
durability, real power-loss durability, external/third-party escrow, an independently protected log,
signer authority, holder-authority issuance, C07 passing on arbitrary crashes, semantic adoption,
production privileges or V3 operation.
