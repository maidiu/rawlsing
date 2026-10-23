# R08 R4 API / trust contract

Status: TEST_ONLY sourcefree local callable. This is not production, protected
capture, R09 enforcement, source/science issuance or full J42/P41/E04 adoption.

## Roles

- **Trusted supervisor/host** configures one immutable resolver/consumer trust
  domain before subject traffic: admission verifier, execution authority,
  admitted producer callable, and accepted owner recipes. Configuration is not
  request/binding/result/cache data.
- **Trusted execution authority** issues producer admissions during trusted setup
  and signs complete executed-result envelopes only after the actual admitted
  provider and unchanged evaluator complete. It exposes issuance only to trusted
  setup; it is not reachable from subject request/cache/reader APIs.
- **Subject-facing resolver/consumer** accepts untrusted requests, bindings and
  cache bytes. It exposes verification only, never signing, key export, trust
  root replacement or configuration mutation.

## D1 no implicit authority

`EvidenceResolver()` with no configured verifier/executor accepts no admission
and cannot produce admitted support. Requests/bindings resolve as typed
`UNKNOWN`; cache import refuses with the typed integrity/configuration error.
There is no default key, module singleton authority, source-derived secret or
data-supplied verifier.

## D2 owner permission is not execution

A producer admission is issued only by the configured execution authority over
the exact admitted context ref and actual owner identity material. Bind checks
the admission, exact owner/context, typed conditions, source/release, query,
predicate, risk, role/direction/design/currentness and consumer/model identity.
The producer callable must be the configured admitted callable; a callable placed
in an untrusted binding is not authorized. Producer permission alone never
certifies a measurement.

## D3 complete executed-result envelope

A SUPPORTED result carries `ExecutedEvidenceEnvelope@1` plus its authority
signature. The envelope binds full K hash/material, context/owner identity,
source/release, provider receipt/fact refs and states, evidence ref and complete
content digest, consumer query/model identities, evaluator result hash, separate
eligibility/execution/result axes, uncertainty, denominator/cells/values read,
trust-domain/version/grade. Only the trusted execution path signs after actual
execution. Export/cache preserve this envelope; no export operation re-signs
caller-supplied results.

## D4 verification-only ingress and real consumer

The resolver/verifier has no signing or key-export method. `EvidenceConsumerReader`
requires the same configured verifier and a valid signed envelope; a caller-made
`EvidenceResult` plus self-consistent evidence/evaluator hash is refused.
Association-only reads are not the qualified productive path. A different
attacker-configured resolver does not alter the already configured consumer.

## D5 cold replay

Cold cache carries request/owner/envelope/evidence/query/rule/result material and
the envelope signature, never the accepted key or root replacement. The verifier
configuration is delivered separately from cache to a fresh process via an
explicit trusted fixture channel (stdin pipe in tests, no key in committed files,
logs, argv or cache). Missing/wrong/legacy root, changed K/source/edition/clock/
design/status/query/model/evidence or forged values refuse before the real
consumer reads.

## D6 compatibility and unchanged meaning

Legacy implicit-public-key/self-sealed caches and default unconfigured acceptance
are intentionally incompatible; they refuse and are not auto-upgraded. K/typed
condition semantics, actual provider/evaluator values, valid zero/null/diffuse/
empty states, ZERO_SUPPORT/UNKNOWN and Z `UNRESOLVED` denominator 16 remain
unchanged. Original provider positive (AT07 54/6/60) remains the positive control.

## Retained limits

No defense claim against hostile same-UID host code/key inspection,
monkeypatching trusted code, ptrace/root or a dishonest competent issuer. R09
protected capture remains separate. J42/P41/E04 live maintained integration is
NOT_REACHED; archived returns are not edited.
