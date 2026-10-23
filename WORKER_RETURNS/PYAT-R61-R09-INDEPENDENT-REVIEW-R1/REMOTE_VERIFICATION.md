# R61-R09V remote verification

- Assigned reviewer branch only:
  `agent/opencode-pyat-r61-r09v-independent-review-r1`.
- Author branch `agent/opencode-pyat-r61-r09-local-runner-r1` was not pushed and
  remains `c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8`.
- Reviewer branch before return: `c8dbdd017b216e01dc43e0e15d4e044f3ec6d6e8`.
- First return commit pushed non-force:
  `6b400865bfcf7a26ad7ecc815d893334bb7f3414`.
- Direct readback after that push:

```
$ git push origin HEAD:agent/opencode-pyat-r61-r09v-independent-review-r1
   c8dbdd017..6b400865b  HEAD -> agent/opencode-pyat-r61-r09v-independent-review-r1

$ git ls-remote origin refs/heads/agent/opencode-pyat-r61-r09v-independent-review-r1
6b400865bfcf7a26ad7ecc815d893334bb7f3414	refs/heads/agent/opencode-pyat-r61-r09v-independent-review-r1
```

- This file is in the subsequent final return commit (the commit containing it).
  That commit was pushed non-force to the same branch and its direct
  `ls-remote` SHA was verified after push; the exact final SHA is stated in the
  final response because a file cannot contain the hash of the commit that
  contains it.
- No force push, no other branch, no candidate-file change.
