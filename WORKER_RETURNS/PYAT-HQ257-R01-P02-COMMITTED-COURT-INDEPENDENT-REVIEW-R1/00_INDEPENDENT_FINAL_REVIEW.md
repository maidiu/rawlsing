# HQ257 R01 — independent final committed-state review of P02's repaired P01 permission-guard court

**VERDICT: `ACCEPT_EXACT_GRAIN`**
**TERMINAL: `HQ257_R01_RETURNED_FOR_HQ_INTAKE__NO_SELF_ADOPTION`**

**Branch:** `agent/deepseek-harness-pyat-hq257-p02-committed-court-independent-review-r1`
**Reviewer HEAD:** `8636c0dcbbfb9a2749077280a6d4a57c150ffe71` (P02 final + HQ257 commission only)
**Frozen P02 candidate:** `cb4a8c5548dbe559825681e4a9f9d49af2ac7e8d`
**Runtime:** governed CPython 3.11.3 (`11d6f541…`), pytest 9.1.1, macOS 13.7.8 x86_64, clean sparse worktree
**Live control:** `integration/pre-main-reconciliation-r1 @ 761291ff…`; sealed HQ257 checkpoint
`…P02-N02-INTAKE-T1-ISSUER-HOLD-R01-E02-ISSUED-R1 @ 6ced6f9f…` carries this exact worker row.

## 1. What the commission asked and what I found

The P02 author's own oracle recorded `head_at_run = ea5110f7…`, i.e. its green run happened with
the **repaired test in the working tree and the P01 binder at HEAD, before the repair was
committed**. That is not independent evidence for the pushed P02 SHA. I therefore executed on the
**final committed code** in a clean sparse worktree and recorded HEAD, dirt status, interpreter
hash, pytest version, commands, collected counts, exits and blob hashes.

| Mandated court on the final committed SHA | Collected | Result | Exit |
|---|---|---|---|
| new P01 permission-identity court | 16 | **16 passed** | 0 |
| four adopted baseline courts | 199 | **199 passed** | 0 |
| combined | 215 | **215 passed** | 0 |

All three match the P02 claim — and are now established on a clean checkout of the pushed SHA for
the first time, not from the author's pre-commit working tree.

## 2. Chain and blob identity (verified by direct Git object compare)

```
428be759 base → 23438ab5 P01 candidate (binder +33/-0) → ea5110f7 P02 commission
             → cb4a8c55 P02 final (test +62/-7, four return docs) → 8636c0dc HQ257 commission
```

- Binder blob is `848d2d0e…` at the P01 candidate, the P02 commission and the P02 final —
  **byte-identical; no production change P01 → P02**.
- On-disk binder sha256 at the reviewed HEAD = `5221d8c2…`, exactly the constant the repaired test
  pins.
- `BINDING_PERMISSION_IDENTITY_MISMATCH` is candidate-only vocabulary (0 in the baseline blob,
  exactly 1 in the candidate).

## 3. The repaired provenance guard is real and correctly discriminating

`test_adopted_binder_baseline_was_the_unmodified_owner` — which read `git rev-parse HEAD:<binder>`
against the pre-candidate baseline and could only pass while the production edit was uncommitted —
is replaced by a two-layer witness. Independently measured, each cell its own process:

| binder | git | result |
|---|---|---|
| candidate | yes (clean sparse worktree) | **16 passed** |
| candidate | no (`/tmp`) | **15 passed, 1 skipped** |
| reverted `4ba00b8e` | yes (worktree at `428be759` + P02 test) | **10 failed, 6 passed** |
| reverted `4ba00b8e` | no (`/tmp`) | **10 failed, 6 passed** |

Layer A (git-free sha256 of the on-disk binder + refusal-vocabulary count) alone distinguishes
candidate-present from reverted binder in every terrain; Layer B adds fixed-commit blob pinning and
is skipped, never failed, without git. This directly closes the HQ255 R01 finding.

## 4. Exact identity, duplicates, ordering, precedence, material

- Full exact identity is enforced (`ExactRef.key` includes `content_hash`): unrelated, extra,
  omitted, replacement and **same `object_id` with a different hash** all refuse with
  `BINDING_PERMISSION_IDENTITY_MISMATCH`.
- The comparison is set equality and is therefore **order- and duplicate-insensitive**
  (reversed order binds; `[A,A]` vs `[A]` binds). Judged normatively acceptable at this grain: the
  receipt side is deduped/sorted upstream and cannot itself carry a duplicate, no in-repo consumer
  needs ordered or subset semantics, and the output is the **declared binding material** — I do not
  describe it as a normalised receipt form.
- Refusal priority: target use still precedes permission; the new check precedes release for
  requests wrong on both. Fail-closed, disclosed, and no existing single-grain code is shadowed.
- Honest behaviour is unchanged at the byte level: for a matching binding the candidate and the
  baseline binder produce identical `material()` (`f03decea…`) and identical replay identities;
  against the same probe the baseline BOUND all five mismatch shapes, reproducing the defect and
  proving the guard is the discriminating change.
- Caller-forged duck-typed receipt/request objects are refused with `BINDING_INTEGRITY_FAILURE`.
  The malformed-receipt-mapping path (`Pre553IntegrityError` instead of the binder subclass) is not
  reachable through the genuine owner and is recorded as a defensive note only.
- No permission is granted (`bound_permission_refs_are_inputs_not_grants`,
  `grants_no_authority`, binding statement "…NO_PERMISSION_GRANT…"); no producer/C1 custody is
  claimed anywhere in material or source.

## 5. Integration question

HQ can lawfully consider integrating **only** the binder (`848d2d0e…`, already the P01 blob) and the
new/repaired permission-identity court file `cdb4dc22…` — the four P02 return documents are
evidence paperwork and are not required for the code. This remains an HQ act; this return is not
adoption, not a merge, not an EE14/T1 grant and not an authority transfer.

## 6. Limits of this evidence

Regressions run: the four adopted courts (199) and the new court (16), combined 215, plus the four
negative-control cells and the semantic/forgery probes above. **Not run:** any wider sweep beyond
the four adopted courts (would widen past the commissioned sparse manifest), OOM/fault injection,
or any raw source, Library, issuer, actor/V3 or native F7 runtime. Without git, Layer B is skipped,
so a no-git execution retains Layer A only. HQ253 T01 G1/C1 provenance, EE14/T1 use, F8 custody,
native F7 and F7-RR-04G remain open and untouched.

No source or test modification, no merge, no adoption, no self-certification.
