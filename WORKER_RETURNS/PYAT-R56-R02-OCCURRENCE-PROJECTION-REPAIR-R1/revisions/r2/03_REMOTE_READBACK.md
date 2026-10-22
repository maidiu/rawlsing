# R02 r2 — remote publication and readback

**Branch:** `agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`
**Parent:** `236fd4d1064f7c14113616db300c955294a474ac`
**Successor commit:** `453a951307bbf9112f576907f48f88524247261f`
**Remote readback:** `453a951307bbf9112f576907f48f88524247261f`
**Ancestry:** parent verified as an ancestor of the successor with
`git merge-base --is-ancestor`.
**Push:** ordinary non-force update `236fd4d10..453a95130`.

## Changed-file allowlist

```
rawlsing_next/pre553_source_native_preimage_adapter.py
rawlsing_next/tests/test_universal_source_projection.py
rawlsing_next/tests/test_universal_source_projection.py.proof.json
WORKER_RETURNS/PYAT-R56-R02-OCCURRENCE-PROJECTION-REPAIR-R1/revisions/r2/
```

No facade, C11, I03, decoder, policy, foreign return, or prior revision was
edited. The author test file above the attributed R02V addition block is
unchanged from `236fd4d1`.

## Readback

- Remote branch ref equals local successor commit.
- `git show HEAD:rawlsing_next/pre553_source_native_preimage_adapter.py` hashed
  equal to the worktree adapter (`c9ea22ad...`).
- `git show HEAD:.../revisions/r2/manifest.json` hashed equal to the worktree
  manifest.
- This readback file and the updated manifest are a separate documentary
  commit; re-read the final remote head with:

```
git ls-remote origin refs/heads/agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1
```
