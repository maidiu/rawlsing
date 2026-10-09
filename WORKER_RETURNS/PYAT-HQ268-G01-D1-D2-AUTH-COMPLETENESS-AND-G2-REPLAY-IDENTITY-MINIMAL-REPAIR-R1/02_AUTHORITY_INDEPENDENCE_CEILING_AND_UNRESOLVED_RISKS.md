# PYAT HQ268 G01 — authority, independence ceiling, and unresolved risks — R1

**STATUS:** HQ268_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION
**BRANCH:** `agent/space-bunny-pyat-hq268-g01-d1-d2-auth-and-replay-identity-repair-r1`
**COMMISSION TIP:** `e64f53a70a5167a7c79712038c9b1e14ae6c747c`
**CODE SHA:** `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd`

This document exists to state plainly what this return does **not** establish, what residual risk remains, and where the ceiling is. Nothing below is softened elsewhere.

---

## 1. Actual model and effort

| | |
|---|---|
| **Model actually used** | **MiMo V2.6-Flash**, model id **`opencode/mimo-v2.6-flash-free`** |
| **Not** | GPT-6 Sol High. Not "Sol". Not a larger or differently-named model. |
| **Lane** | Existing Space Bunny / OpenCode source-free engineering **author** lane — the same lane that authored the HQ266 candidate. |
| **Effort** | Full implementation of D1, D2 and the safe portion of R2; 21 new tests; re-execution of all four courts plus the STEP A positive control at the final committed SHA; a separately written cross-check script; four return documents. |

The commission's instruction to state the actual model rather than a flattering label is honored literally. **A model name is not evidence of capability or independence**, and none is claimed from it.

---

## 2. Independence ceiling — the hard limit of this return

**There is no independent QA behind anything in this return.**

1. **Author-adjacent, full stop.** The same session and the same model authored the HQ266 candidate, executed the HQ267 R01 review of it, and now executes the HQ268 correction. Every number in this return — 96, 199, 80, 375, 49 — is **author evidence**.
2. **The HQ267 review was already disqualified as independent**, and this return does not rehabilitate it. HQ's own characterization stands: *author-adjacent self-review, not a separate independent hostile acceptance*. Its findings D1 and D2 were independently **source-verified by HQ**; that verification is HQ's, not this worker's, and it validates the *defects*, not the review's independence.
3. **No self-review of this correction was performed, and none may be substituted for one.** I did not review my own work in any capacity that could be called review. Writing tests that my own code passes is author evidence, not review.
4. **No self-adoption, no G1 PASS, no trust root, no T1/T2 claim.**
5. **The commission's requirement stands:** a genuinely **separate GPT-6 Sol High session, unconnected to this author, that did not write or execute the author lane**, must perform real independent hostile review before any G1 acceptance. Model label alone does not establish independence; prior author involvement must be disclosed to that reviewer.

**Ceiling statement:** this return proves *that the two named defects are repaired in the source at the named SHA and that the named courts are green*. It proves **nothing** about whether the result is correct as a matter of independent judgment.

---

## 3. Residual risks retained

### 3.1 R1 — the expected identity is self-referential (RETAINED, EXPLICITLY)

The owner-held expectation is produced by `court._expected_identity(...)`, which **re-executes the same `_compose(source, qauth, registry)`** over the owner-held fixture. Expected and observed are therefore derived from **one honest run**.

Consequences, stated exactly:

- This is an **owner-controlled, source-free development invariant**. It makes authentication non-vacuous against accidental incompleteness (D1) and against material divergence (F3), and nothing more.
- It is **NOT an independent cryptographic custody root**, **NOT a source-authorized preimage**, and **NOT a trust root**.
- An in-process principal who can control `_compose` can control both sides of the comparison.

**D1 does not change this.** Making the expectation complete makes it *meaningful*; it does not make it *independent*. No independent root was created, and the commission explicitly forbade creating one.

### 3.2 R2 — live trusted objects are only shallowly frozen (PARTIALLY CLOSED, RESIDUAL RETAINED)

**Closed:** the `_source` and `_cells` containers are now read-only mappings (`MappingProxyType`), and mutating the dict handed in at construction no longer reaches the ingress. `_owner_identity` remains deeply frozen, and the returned `owner_scope_material()` snapshot remains deeply frozen.

**Retained residual, precisely bounded:** the freeze is **shallow**. The NESTED objects inside `_source` — `universe`, `release_ref`, `repository`, `respondents` — remain the owner's own shared objects and are still mutable by any in-process principal holding a reference.

This was **not** deep-frozen because deep-converting those objects would change the semantic ref objects the accepted C1/G2 owners consume, which the commission explicitly forbade ("Do NOT change source objects' semantic refs").

The blanket prose that had implied broader immutability was corrected: the module docstring now carries an explicit **BOUNDED RESIDUAL (R2)** section, and the class docstring a matching **WHAT IS FROZEN** block, both stating exactly which fields are frozen and which are not.

**Classification:** a precisely bounded **trusted-harness limitation**, not a closed property, not a custody root, not deployed security.

### 3.3 D2 residual — `canonical_replay_only_order` is outside the accepted owner's replay identity

The commission listed `canonical_replay_only_order` among the six omitted fields. It is one of the receipt's **12 dataclass fields**, but the accepted owner's own `_material()` **does not include it** — so `replay_identity()` cannot carry it.

The D2 minimum forbade deviating: `g2_receipt_hash` must equal the exact `receipt.replay_identity()`. So the field could not be added there without violating the requirement it was meant to satisfy.

**What was done instead:** `origin_receipt_hash` now binds it directly via a new `"g2_canonical_replay_only_order"` key in the ingress's own `origin_material`. This is strictly additive, inside the authorized file, and closes the *binding* gap for the origin receipt.

**What remains open:** the **accepted SA owner's `_material()` still omits `canonical_replay_only_order`**, so that field remains outside `replay_identity()` for every consumer of the accepted primitive — not just this ingress. Closing that would require editing `rawlsing_next/pre553_service_source_applicability.py`, an adopted, read-only owner that this commission forbade touching. **Referred to HQ as an open question against the adopted owner.**

### 3.4 The threat model is unchanged and bounded

- **In scope:** the bounded external **DATA-ONLY** service client fixed by HQ262.
- **Explicitly UNPROVED / out of scope:** same-process arbitrary Python executed by a malicious principal; independently certified root; real deployment.
- `SelectedRequest` remains data-only and cannot carry evidence, receipts, grants, authorities or executable objects.
- `authorizing` remains `False`. No fake CURRENT is claimed. No native F7/AT07, no V3, no EE14 grant.

### 3.5 D1's own scope limit

D1 closes an **internal owner-setup completeness defect**. It is not, and is not presented as, a fix for any deployed-client exploit — no external data-only adversary can supply `owner_identity` at all. The added tests demonstrate that owner setup can no longer be vacuous; they do not extend the threat model.

### 3.6 F8 parity does not prove custody

Unchanged from HQ266/HQ267 and still true: bound-F8 equal to the direct C1 result is **not** evidence of custody. The custody false positive demonstrated in HQ267 P6 (identical F8 hash for genuine and forged provenance, refused only at the ingress boundary with `f8_calls=0`) remains an accurate description of where the protection actually lives — **at the ingress authentication gate**, not in the F8 hash.

---

## 4. Evidence-grade notes and known oddities

1. **Court counts are author evidence.** 96 / 199 / 80 / 375 were produced by me, on my machine, by my commands, at my SHA. The commission already classifies them as *author evidence, NOT independent QA*; nothing here upgrades that.
2. **The historical 199-vs-99 commit-message discrepancy** remains a confirmed one-character prose typo at author-adjacent evidence grade (HQ266 `bdc65ff89`'s message says `99`; the frozen return says `199`, which 199 independently reproduces). Not repeated here: this return's counts were cross-checked arithmetically (`96 + 199 + 80 = 375`) before writing.
3. **Pre-existing unrelated failures observed, not caused and not touched:**
   - `test_f07_second_canary_prev3_admission.py::test_existing_m1_v554_ingress_accepts_and_same_input_replay_is_identical` fails with a `FileNotFoundError` on an untracked data file. Present before this work; outside the authorized paths; not addressed.
   - Wide test sweeps produce 9 pre-existing collection errors from absent `pyarrow` / `pandas` / `numpy`. Not addressed; the four named courts do not depend on them.
4. **Environment quirks recorded:** zsh does not word-split unquoted parameter expansion (a first attempt to pass file lists yielded `no tests ran`), and `${PIPESTATUS[0]}` is empty in zsh — exit codes were captured by redirect-to-file and `$?` instead. All reported exit codes are real.
5. **The independently written cross-check (`49 PASS / 0 FAIL`)** is mine, not a third party's. It is included because it reconstructs the *pre-D2 six-field hash* and demonstrates concretely that it was blind to `receipt_id` — i.e. it shows the old defect, not merely the new state. It is still author code.

---

## 5. What is required next, and what must never happen

**Required by HQ:** a new **GPT-6 Sol High** session **unconnected to this author**, which did not write or execute the author lane, to perform **real independent hostile review** of the correction at SHA `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd`. That reviewer must be told that the same session authored HQ266, executed the HQ267 R01 review, and executed this HQ268 correction, and that the actual model throughout was `opencode/mimo-v2.6-flash-free`.

**Must not happen:**

- No G1 PASS or adoption based on this return or on the HQ267 review.
- No self-review, self-acceptance, or "review" performed by this lane.
- No trust root, T1, T2, EE14 grant, native F7/AT07, V3, or deployment claim derived from this work.
- No silent reinterpretation of D1/R2 improvements as independent custody or as closure of the same-process threat model.
- No edit to the adopted owners, the AT09 fixture, or the frozen XOR figures.

---

## 6. Terminal

**STOP: `HQ268_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.**
