# Publication status

**Source delivery:** complete.
**Branch push:** complete.
**Draft PR creation:** blocked by credential scope.

## Remote branch

- Remote: `origin` (`https://github.com/maidiu/rawlsing.git`)
- Branch: `agent/sorok-cga-982-composite-stale-receipt-20261113-r1`
- Code/test cut: `ff30c13eea54e37e2dc8edfa73a7c7447127b735`
- Report cut: the commit containing this file (`git rev-parse HEAD`)
- Compare URL emitted by GitHub on push:
  `https://github.com/maidiu/rawlsing/pull/new/agent/sorok-cga-982-composite-stale-receipt-20261113-r1`

## Draft PR attempt

Attempted against base branch `agent/sorok-cga-p4-source-owner-local-20261112-r1` with `draft: true`.

GitHub REST response:

```text
HTTP 403
{"message": "Resource not accessible by personal access token",
 "documentation_url": "https://docs.github.com/rest/pulls/pulls#create-a-pull-request"}
```

The current fine-grained credential can read/write repository contents and push branches, but cannot create pull requests or read issue/PR metadata. No PR number is claimed. The branch and exact source cut above are the delivery subject for the one independent G5 receiving.
