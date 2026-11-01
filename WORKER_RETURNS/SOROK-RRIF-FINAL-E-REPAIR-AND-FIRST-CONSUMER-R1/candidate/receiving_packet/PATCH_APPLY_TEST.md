# Receiving patch apply test

A clean copy of the exact R2 base was placed at a repository-relative path with
the same parent depth, then `patch -p1` applied `RRIF_E_ADDITIVE.patch`.

```text
patch=0
26 passed in 14.52s
```

The 26 tests are the unchanged R2 20 plus the six RRIF-E repair tests. The
temporary copy was deleted; no PREMAIN tree, branch or production DB was
modified.
