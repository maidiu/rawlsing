# M2 local verification and publication

Grade remains **`TEST_ONLY_M1_SOURCE_TIME_REPAIR_CANDIDATE_PENDING_I2`**. This worker verified and published supplied code; it did not reimplement, scientifically accept, integrate B3, or issue CAN/ADP authority.

Assigned startup and directly verified initial remote: `6eebdf23fec3d24d29df1f95fd567f3599316e11`. Branch: `agent/rabochii-sorok-v2-hq328-m2-m1-source-time-identity-repair-r1`.

The user supplied an already-extracted handoff directory. No ZIP container was present at the supplied path or found by the bounded Desktop/Downloads filename search, so no ZIP-container hash is claimed. Its subtree was copied to an isolated temporary directory, all 23 listed file SHA-256 hashes plus the manifest were verified, and the frozen M1/I2 archive bytes were compared directly with the existing authorized Git blob store. Only that verified subtree was copied into the isolated branch worktree. The original 24 package files, including source, tests, archives, author logs, passport and manifest, remain byte-identical. Local receipts are additional files under this `local_publication/` directory; the supplied manifest's `NOT_PUSHED` is its preserved handoff-time state, not the final remote state.

## Fresh execution

Python **3.11.3**, pytest **9.1.1**. The author's Python 3.13.5 / pytest 9.0.2 results reproduced with no per-test outcome divergence.

| Suite | PASS | RED | Errors |
|---|---:|---:|---:|
| New M2 | 41 | 0 | 0 |
| Original M1 tests against original code | 37 | 0 | 0 |
| I2 tests against original M1 | 14 | 9 | 0 |
| Original M1 tests against M2 | 18 | 19 | 0 |
| I2 tests against M2 | 13 | 10 | 0 |

`verify_local.py` runs each comparison in its own fresh Python process and isolated directory, with unchanged frozen tests and the selected exact `kernel.py`. The positive 41-case court runs directly in the copied return. Actual imported module paths and hashes are checked and recorded. Source-archive `kernel.py` and `test_m2.py` also match the supplied loose files. All supplied manifest hashes are rechecked after execution. Every per-case outcome matches its supplied JUnit counterpart; no inherited RED was suppressed or rewritten. `commands.json`, five raw `.log` files, five JUnit `.xml` files and `verification.json` are the fresh local evidence; hostnames/local paths are removed from these evidence copies only.

Reproduce from the repository root:

```sh
python3 WORKER_RETURNS/SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1/local_publication/verify_local.py
```

## Exact source identities

| Artifact | SHA-256 |
|---|---|
| Supplied manifest | `b841a0e99059ba7cf7d3fc23fef051d378121df41f974da56d9f8220cbe4dcf0` |
| M2 kernel | `888d73fff63f70a22932f1001f5c9003104b0e5a9cdef84e93456151428676c8` |
| M2 tests | `112114ee13545791cd003f30f1c9aa2cfdeccd1fba8b93cae7ff25c26456fbbc` |
| Original M1 archive | `30b820eda81089c89d9e2df8145860386d33b973f5c7f6a028e7e16b21dbe7b4` |
| Frozen I2 archive | `449f9cf8c8db7befc8b2358b776adee636db70f884e7d2fdffa069b07c19d72f` |

M1 binary Git blob: `37174efcf6689f87110ef97023e91cc83786fe2a`. I2 binary Git blob: `23ebc5a15df242b288555ec415ef6533b4420a7f`. All other supplied hashes remain in the unchanged original `manifest.json`.

Read the exact M2 commission at startup, 00D at startup and HQ328 intake at `2f46ceab2df8cb21c6ba7b373d174808f7a13d65`. 00C is absent from the startup tree; reused the same-session complete read of its governing copy at `3c685eb4734856b61f2d601e082eb325e3f6f1d1`, blob `c33afd5d00b6c2ca735baa759d17ebaa932a2b03`, verified again. The user's local handoff instruction explicitly supersedes the older commission's Browser-only execution surface for this publication task. No new model, provider, dependency installation or original-source execution was used.

All changed paths must lie under `WORKER_RETURNS/SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1/`; the supplied ZIP/prompt are not committed. `published_paths.json` lists the exact committed paths. The final commit identity is verified by normal push, a fresh fetch and direct remote-ref read, and reported outside its own commit preimage.

The 29 inherited REDs against M2 remain real candidate incompatibilities requiring independent I2 adjudication. No scientific acceptance, native actor, B3 integration, original survey, or adopted CAN008/CAN011/ADP016/017 authority is established by this handoff.
