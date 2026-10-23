# R61 R09F remote verification

## At startup

Before any work, the local checkout and direct remote were checked:

```text
git rev-parse HEAD
3470da602618b5c04b1f28885b5ad1835169e2d5

git branch --show-current
agent/opencode-pyat-r61-r09f-facility-preflight-r1

git ls-remote origin refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1
3470da602618b5c04b1f28885b5ad1835169e2d5	refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1
```

An automated collector run later timed out the same `ls-remote` after 45
seconds due to transient network conditions; it is recorded as a timeout, not
as a negative remote result. The direct remote result above was the observed
startup identity.

## After the return commit

The commissioned return is one non-force push to the assigned branch:

```text
git push origin HEAD:agent/opencode-pyat-r61-r09f-facility-preflight-r1
git rev-parse HEAD
git ls-remote origin refs/heads/agent/opencode-pyat-r61-r09f-facility-preflight-r1
```

The final response reports the local final `HEAD` and the directly observed
remote SHA. This file deliberately does not contain a self-referential final
commit SHA. No other branch is pushed.
