# R08 R5 repair amendment — authenticated served-result projection and live-mode pin

This amendment extends R08 R4 under the settled R61Q D1-D6 contract. No new
science, authority, service or trust decision is introduced.

## Shared authenticated projection

`ExecutedEvidenceEnvelope` is the sole authority for productive served output.
One canonical projection is derived from the signed envelope and used by:

- `EvidenceConsumerReader.read` / `e04_step` (live and cache results),
- cache export (result material written is the signed projection),
- cache import/replay (public `result` material must equal the signed projection).

Qualified `read` returns only envelope `consumer_values_read` plus the verified
evaluator replay hash/state/material and trust labels. Any supplied result whose
signed field categories differ from the envelope (K, axes, status, uncertainty,
evidence ref, producer receipt/fact/state, consumer query/result, denominator,
cells, cells/values) is refused. Evidence/query/rule objects must match the
envelope content digests; matching labels on a different object are insufficient.
Unsigned result fields never reach `read`, `e04_step`, cache export or replay.

## Live execution vs verifier-only replay

- Live producer execution requires a non-null configured `admitted_producer`
  callable identity. A binding with a copied valid owner admission and a
  substituted callable is not admitted; `resolve` refuses before invocation.
- Omitting the live producer pin disables live execution; it is not "accept any
  callable".
- A verifier-only resolver (no executor/admitted producer) may import and read
  already-authenticated cache entries; it cannot execute new producers.
- Cache cannot choose/rotate root, producer or verifier configuration.

## Preserved

Actual provider/evaluator positive 54/6/60, changed native 54/16/70, observed
zero, ZERO_SUPPORT, status partitions, Z UNRESOLVED16, typed typed/condition/
order/currentness identities and independent-root cold replay remain unchanged.
Legacy implicit-default records continue to refuse. No full J42/P41/E04
integration claim.
