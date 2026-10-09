# HQ257 R01 — source diff, exact identity semantics and refusal precedence

Subject: frozen P02 return `cb4a8c5548dbe559825681e4a9f9d49af2ac7e8d`. Reviewed at reviewer
HEAD `8636c0dcbbfb9a2749077280a6d4a57c150ffe71` (the P02 commit plus the HQ257 commission file
only), clean worktree, governed CPython 3.11.3.

## 1. Exact chain and blob identity

```
428be759  pre-candidate base        binder 4ba00b8e...
23438ab5  P01 frozen candidate      binder 848d2d0e...  (+33/-0)   test e5464a0c...
ea5110f7  P02 commission            binder 848d2d0e...  (unchanged) test e5464a0c...
cb4a8c55  P02 final return          binder 848d2d0e...  (unchanged) test cdb4dc22...  (+62/-7)
8636c0dc  HQ257 commission tip      binder 848d2d0e...  (unchanged) test cdb4dc22...
```

- `git diff --name-status ea5110f7 cb4a8c55` is exactly the one test file (M) plus the four P02
  return artifacts (A); **no production blob changed** P01 → P02.
- On-disk binder sha256 at the reviewed HEAD is
  `5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b`, which is exactly the
  constant the repaired test pins.
- `BINDING_PERMISSION_IDENTITY_MISMATCH` occurs 0 times in the baseline binder blob; it is
  candidate vocabulary, present exactly once in the candidate blob.

## 2. The P02 test repair — what it actually does

`test_adopted_binder_baseline_was_the_unmodified_owner` (which read `git rev-parse HEAD:<binder>`
and asserted the PRE-candidate baseline, so it could only pass with the production edit
uncommitted) is replaced by `test_adopted_binder_baseline_is_pinned_to_a_fixed_commit_not_head`:

- **Layer A — git-free, always executed.** The on-disk binder must hash to the pinned candidate
  sha256, the refusal vocabulary must occur exactly once, the recorded baseline and candidate
  blobs must be distinct, and the module-level baseline constant must still name the true
  pre-candidate baseline.
- **Layer B — git at FIXED commits.** Resolves `428be759:<binder>` → `4ba00b8e` and
  `23438ab5:<binder>` → `848d2d0e`, and asserts `HEAD:<binder>` equals the candidate blob.
  If the git object store is unavailable the layer `pytest.skip`s (terrain), never fails.

Independently measured control matrix (4 cells, each its own process):

| binder | git | result | provenance witness |
|---|---|---|---|
| candidate `848d2d0e` | yes, clean sparse worktree | **16 passed, exit 0** | passes both layers |
| candidate `848d2d0e` | no (`/tmp` copy) | **15 passed, 1 skipped, exit 0** | layer B skipped, layer A passes |
| reverted `4ba00b8e` | yes, detached worktree at `428be759` + P02 test injected | **10 failed, 6 passed, exit 1** | layer A fails (`0a5d3020… != 5221d8c2…`) |
| reverted `4ba00b8e` | no (`/tmp` copy) | **10 failed, 6 passed, exit 1** | layer A fails git-free |

**Judgement:** the guard genuinely distinguishes candidate-present from reverted binder.
Layer A alone is sufficient and terrain-independent; Layer B adds fixed-commit blob pinning and is
correctly *skipped*, not failed, without git. This is the correct repair of the HQ255 R01 finding.

## 3. Exact permission identity semantics — independently probed

On the final committed code (binder byte-identical to the P01 blob already reviewed):

| probe | result |
|---|---|
| honest single matching permission | **BOUND** |
| honest three matching permissions | **BOUND** |
| unrelated permission | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| superset (invents an extra) | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| subset (silently drops one) | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| replacement within a set | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| **same `object_id`, different content_hash** | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| identical set declared in reverse order | **BOUND** (material records the declaration order) |
| duplicate binding refs `[A, A]` vs receipt `[A]` | **BOUND** (material records the duplicate twice) |
| receipt given duplicate input | stored deduped (`[A]`) |

`ExactRef.key` is `kind|object_id|content_hash`, so the comparison is over full exact identity
including the SHA. The comparison is **set** equality and is therefore **order- and
duplicate-insensitive**.

**Normative grain judgement (as requested):** the accepted grain is *exact permission-ref identity
as a set*. That is:
- **Sensitive** to kind, object_id and content_hash — i.e. to any addition, omission, replacement
  or same-id/different-hash substitution. This is the security-relevant axis and it is enforced.
- **Insensitive** to declaration order and to a repeated declaration of the same exact ref.
  The receipt side can never carry a duplicate (the applicability owner dedupes and sorts via
  `_ref_list`), so only the binding side can repeat; a repeat grants nothing new.
- The output is the **declared binding material**, faithfully recording what the request declared
  (order and multiplicity included). It is deliberately **not** a normalised receipt form and
  should not be described as one; the receipt's own canonical ordering is a separate artifact.
- No in-repo consumer of `bound_target_use_permission_refs` requires ordered or subset semantics,
  so set equality is safe at this grain.

## 4. Refusal precedence — assessed

| multi-grain request state | code returned |
|---|---|
| wrong target use + wrong permission | `BINDING_TARGET_USE_GRAIN_MISMATCH` (prior sibling preserved) |
| wrong permission + wrong release | `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| wrong release, permissions agree | `BINDING_RELEASE_GRAIN_MISMATCH` (unchanged) |

The changed priority (permission before release) is **fail-closed**: it refuses earlier on a
request that is dishonest on two grains, does not shadow the target-use sibling, and leaves every
pre-existing single-grain code untouched. Acceptable as-is; if HQ prefers the older release-first
order, the block would simply move below the release check — nothing in the accepted owner surface
requires either order.

## 5. Malformed path vs caller-forged object

- **Caller-forged objects**: duck-typed receipt or request objects are refused with
  `BINDING_INTEGRITY_FAILURE` (`isinstance` checks on the adopted classes).
- **Malformed receipt permission mapping**: if a receipt's stored mapping were not exactly
  `kind/object_id/content_hash`, `exact_ref(...)` raises plain `Pre553IntegrityError` rather than
  the binder's `ServiceF8ScopeBindingError` subclass. This is **not reachable through the genuine
  applicability owner** (which builds only exact refs and refuses an empty set upstream with
  `SERVICE_REQUEST_UNDETERMINED` / `TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED`); it is reachable
  only by mutating the receipt object's internals, which is not a supported owner path. Recorded as
  a defensive-surface note, not a blocker.

## 6. Honest material and replay — unchanged at the byte level

For an identical matching two-permission binding, the candidate and the **baseline** binder
produce **byte-identical** `material()` (`sha256 f03decea409eb6a9dfa9dfc369ce88e8fc9291b6530a11b495c28db436b149fd`)
and identical binding/receipt replay identities. Against the same probe the **baseline** binder
BOUND all five mismatch shapes, which both reproduces the original defect and proves the candidate
guard is the discriminating change.

## 7. No grant, no custody, narrow scope

- `bound_permission_refs_are_inputs_not_grants: true`, `grants_no_authority: true`, and the binding
  statement ends `...NO_PERMISSION_GRANT_NO_ACTOR_INFERENCE`.
- `forbidden_binding_purposes` still lists `TARGET_USE_PERMISSION_GRANT`, `SOURCE_SELECTION`,
  `SOURCE_RANKING`, `POOLING`, `ACTOR_OR_PERSON_STATE` and 20 more.
- No custody vocabulary appears in the binding material or in the binder source; no producer/C1
  custody is claimed. The HQ253 T01 G1/C1 provenance gap, EE14/T1 use, F8 custody, native F7 and
  F7-RR-04G are untouched and remain open.

## 8. Integration question

The only code artefacts involved are the **binder** (already byte-identical to the P01 candidate
the guard was written for) and the **new P01 court file** with the P02 repair. HQ can lawfully
consider integrating exactly those two paths **without** forwarding the P02 return documentation,
which is evidence paperwork rather than code. Any such integration remains an HQ act: this return
is not adoption, not a merge, not an EE14 grant and not a T1 authorisation.

## 9. Regression and negative limits (complete)

- Regressions actually run: new court 16/16; four adopted baseline courts 199/199; combined
  215/215; all exit 0, clean worktree at the final committed code.
- Negative controls actually run: reverted binder in a git worktree (10F/6P) and in a no-git copy
  (10F/6P); candidate-present no-git (15P/1S).
- **Not run:** any wider sweep beyond the four adopted courts (would require widening past the
  commission sparse manifest); no raw source, Library, issuer, actor/V3 or native runtime; no OOM
  or platform fault injection; no ordered/subset consumer audit beyond the in-repo grep (none
  exist).
- Terrain limit: without git the guard's Layer B is skipped, so a no-git execution loses
  fixed-commit blob pinning but keeps the git-free sha256 layer.
