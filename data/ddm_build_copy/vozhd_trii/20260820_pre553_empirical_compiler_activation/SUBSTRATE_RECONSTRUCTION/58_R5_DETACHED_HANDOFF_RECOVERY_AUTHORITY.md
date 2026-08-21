# VOZHD TRII — R5 DETACHED HANDOFF RECOVERY AUTHORITY

Status: `AUTHORIZED__DETACHED_HANDOFF_RECOVERY_ONLY__NO_REIMPLEMENTATION__NO_FULL_SOURCE`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Binding implementation authority:

`57_R5_LONG_SHARDED_SHADOW_IMPLEMENTATION_AUTHORITY.md`

Original R5 implementation branch:

`agent/vozhd-trii-r5-long-sharded-shadow`

Original exact implementation starting head:

`ab19862b9485741228dfa84f4c976c6110171065`

## 0. Recovery fact

The first R5 implementation worker did not obtain a trustworthy real Rawlsing checkout. It therefore returned a detached handoff bundle instead of committing branch state.

GitHub verification after receipt established that the implementation branch remained exactly identical to `ab19862b9485741228dfa84f4c976c6110171065`: no partial implementation commit, accepted-runtime mutation, or branch contamination exists.

The received handoff ZIP has SHA-256:

`606939a44f1b10113d49e730df9cda4218bb88fa1fdb98dd33af78d202ff110f`

Its internal `FILE_MANIFEST.sha256` was independently checked by HQ:

`32 / 32 files verified; 0 mismatches; 0 missing.`

This identity check certifies only the handoff bundle's internal integrity. It does NOT certify semantic correctness or implementation acceptance.

## 1. Admissible evidence from detached worker

The bundle reports a detached local court of:

- `40 passed`;
- `4 skipped`;
- no observed test failures;
- memory plateau at approximately 113 MB RSS across 4k, 16k and 64k logical-row synthetic cases;
- destructive oracle controls rejected;
- benign physical relayout accepted;
- local integrity/publication/determinism tests passed.

The four skips are explicitly the real-checkout integration gates for:

1. accepted C11 bounded-reference roundtrip;
2. frozen I03 exact fact identity;
3. frozen I05 unforeseen-XOR coverage/receipt identity;
4. frozen I04 decision/receipt identity.

Therefore the detached bundle's current disposition remains:

`R5_BLOCKED__SEMANTIC_EQUIVALENCE`

This is an evidence-status block, not an observed semantic mismatch.

## 2. Recovery mission

Do NOT rebuild R5 from scratch.

Do NOT redo the two-round design campaign.

Do NOT autopsy failed R4 full-source execution.

Do NOT run WVS7 or LiTS I full scale.

The recovery worker shall:

1. establish a trustworthy real repository checkout whose HEAD is exactly `ab19862b9485741228dfa84f4c976c6110171065` on `agent/vozhd-trii-r5-long-sharded-shadow`;
2. independently verify the supplied ZIP SHA-256 and internal file manifest before applying anything;
3. apply only the files listed in the bundle's `CHANGED_FILES.txt` and only where Authority 57 permits them;
4. verify that no existing accepted runtime file has changed;
5. run the complete R5 test surface in the real repository environment;
6. ensure the four previously skipped frozen-integration tests actually execute rather than skip;
7. repair failures only inside the existing Authority-57 R5 write scope;
8. if repair requires modification of any accepted runtime module, STOP with `R5_BLOCKED__EXISTING_RUNTIME_MODIFICATION_AUTHORITY_REQUIRED`;
9. rerun the complete bounded G0-G8 court required by Authority 57 after any repair;
10. commit and push only after all required bounded gates genuinely close.

## 3. Checkout hygiene

Checkout/worktree failure is an environment/mechanics problem, not authority to alter repository history.

Forbidden recovery shortcuts:

- `git reset --hard` against an unrelated dirty user checkout;
- force-moving an occupied worktree or user branch;
- deleting user worktrees/files to free the branch;
- setting `R5_ALLOW_NONEXACT_HEAD=1` merely to bypass the bundle guard;
- applying onto a different semantic base and calling it equivalent;
- cherry-picking unrelated commits;
- committing helper scripts or README material outside Authority-57 write scope.

Preferred recovery environment:

- a fresh disposable clone/worktree dedicated to this branch; or
- another demonstrably clean repository checkout at the exact mandated head.

If the environment cannot establish the exact checkout safely, STOP and return a mechanical checkout block. Do not improvise around Git state.

## 4. Bundle application law

The handoff's helper script is convenience only. Authority is the verified bundle identity + `CHANGED_FILES.txt` + Authority 57.

Only these classes may enter the branch:

- `rawlsing_next/pre553_r5_*.py`;
- `rawlsing_next/test_pre553_r5_*.py`;
- small R5 receipts under `.../R5_LONG_SHARDED_SHADOW/`.

The recovery worker must compare the post-application diff against `CHANGED_FILES.txt` before testing and before commit.

## 5. Required exit

If the complete real-checkout bounded court passes, the worker may return:

`R5_SHADOW_IMPLEMENTATION_READY_FOR_FULL_SOURCE_COURT`

and the required implementation token:

`PRE553_R5_LONG_SHARDED_SHADOW_IMPLEMENTATION_RETURNED`

If any frozen integration mismatch exists, return the exact Authority-57 block disposition with a minimal mismatch witness.

If checkout itself remains impossible without violating hygiene, return:

`R5_BLOCKED__TRUSTWORTHY_CHECKOUT_UNAVAILABLE`

with the exact Git/worktree error and no implementation claim.

No full-source execution is authorized by this recovery authority.
