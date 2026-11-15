# Mechanism I design and contracts

The existing Sorok world owns objective events, material state, actor
identity, branch and clock. Mechanism I adds a branch-scoped resource to
that owner's checkpoint. It holds targets, obligations, attempt receipts,
admitted physical facts and rebuildable indexes. The existing actor and
psychology owners retain their state.

## Entry and background work

P4 captures a coarse tool affordance from the world and a perceived
arrival. The S46 path captures a completed unit from a confirmed,
source-owned repair. The repair journal and world checkpoint must agree
on the exact event. Recovery scans the branch-local journal suffix and
recreates a missed obligation by occurrence identity. The projection only
publishes a target when its introducing event is perceived at the current
location.

A target and its outbox obligation share a checkpoint transaction. The
opening or turn wakes a bounded worker after saving the foreground ledger.
A foreground reopen can wake undelivered work. Each automatic wake handles
up to three jobs and stops on retryable failure or stale response.
The configured HTTP adapter receives a compact constraint packet and
returns a candidate and receipt. Runtime releases the foreground lock
during inference and reacquires it for local owner operations.

| Contract | Bound data |
|---|---|
| Target | Root and branch, referent key, actual occurrence ID and hash, admitted surface, unresolved dimensions and version |
| Lease | Job and target version, attempt token and expiry, sealed packet digest and world readset |
| Constraint packet | Current world clock and root, exact event and target refs, admitted values, authority ceiling, bounded actor identity and prior repair context where supported |
| Candidate | Request ID, proposed facts, occurrences and links, and dependency groups |
| Commit | Accepted fact IDs, held and rejected groups, current target version and world readset |
| Inspection | Exact perceived inspection event, permitted physical fact IDs and status at the observation clock |

## Admission and replay

The pure evaluator normalizes claims and groups and checks closure,
chronology, source refs and proposed H class. The world owner consumes
that normalized result, rechecks the current lease and readset, and
writes compatible H0 physical groups. It records source, claim and
dependency references with each fact. Objective repair participation
is a relation derived from a committed event and sealed actor identity.
A prior repair may contextualize a request while the current repair
remains its event parent.

A saved candidate can be admitted after restart without calling the
provider again. Expired attempts are fenced by token. A stale result
cannot write facts. A still-relevant job can obtain a bounded fresh
attempt. Inspection rechecks the exact source event before returning
newly indexed physical facts. A selected missing visible predicate can
receive a narrow follow-up job after the initial request settles.

Forked checkpoints can contain copied history bytes. The received C12
store checks the recorded ancestor prefix at each fork edge. The child
reads and writes its own historical state. Current historical targets
are branch-local. The owner does not presently issue shared pre-contact
historical choices.

See [03](03_HISTORICAL_ADMISSION_AND_INDEX_EVIDENCE.md) for provenance and
index evidence and [07](07_EXPLICIT_AUTHORITY_HOLDS.md) for the current
authority boundary.
