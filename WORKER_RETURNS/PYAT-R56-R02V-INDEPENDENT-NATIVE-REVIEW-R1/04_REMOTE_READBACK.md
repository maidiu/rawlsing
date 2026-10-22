# R56-R02V — remote publication and readback

**Reviewer branch:** `agent/rabochii-pyat-r56-r02v-independent-projection-review-r1`
**First publication commit:** `f56216646859a691ddfc53b2249a319da606c43b`
**Remote readback at publication:** `f56216646859a691ddfc53b2249a319da606c43b`
**Parent:** `236fd4d1064f7c14113616db300c955294a474ac` (exact candidate)
**Ancestry:** `236fd4d1...` is an ancestor of the reviewer commit; verified with
`git merge-base --is-ancestor`.
**Push:** ordinary non-force push; new remote branch created.

## Changed-file allowlist at `f562166`

```
rawlsing_next/tests/test_universal_source_projection.py
rawlsing_next/tests/test_universal_source_projection.py.proof.json
WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/
```

No production module, frozen policy, author return, or foreign return was
changed. The adapter still equals the candidate:

```
2cf5e98bc29081678c364d3ff591c71f11ce7ebf3564419af8a26f5f04113b64
```

## Content readback

- `git show HEAD:WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/00_RETURN.md`
  hashed equal to the worktree file (`0b32ec33...`).
- The remote ref readback was re-run after the push and equalled the local
  commit.
- This readback file and the updated manifest are a separate documentary
  commit; the final remote head is recorded in the review completion message
  and can be re-read with:

```
git ls-remote origin refs/heads/agent/rabochii-pyat-r56-r02v-independent-projection-review-r1
```
