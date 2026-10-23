# R61-R09V R2 remote verification

- Assigned reviewer branch only:
  `agent/opencode-pyat-r61-r09v-r2-independent-review-r1`.
- Author branch `agent/opencode-pyat-r61-r09-local-runner-r1` at review start:
  `4a10c82aa8ba2a31938d3d35e12dc42f4456264c`.
- Reviewer branch at review start:
  `4a10c82aa8ba2a31938d3d35e12dc42f4456264c`.
- Expectations freeze commit: `ef39f11e494745b90259fbc35ffc8eddfdbac01e`.
- The final return commit is pushed non-force to the same reviewer branch only;
  its direct `ls-remote` SHA is stated in the final response (a file cannot
  contain the hash of the commit that contains it).
- This file documents the push/readback commands; the exact final SHA is in the
  final response.

```
$ git push origin HEAD:agent/opencode-pyat-r61-r09v-r2-independent-review-r1
$ git ls-remote origin refs/heads/agent/opencode-pyat-r61-r09v-r2-independent-review-r1
```

- No force push, no other branch, no candidate-file change.
