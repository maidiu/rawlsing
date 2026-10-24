# R95 R06R4 pre-code contract — pinned owner, trusted original, held structural authority

Status: frozen before the R4 code commit. Startup
`02800fcfd77abde178851031f877838bedb5e242`; same R95 branch/author session.
Prior evidence immutable. Only the two authorized R06 code paths and this R4
return are written. No new signer/R09 service.

## 1. Pinned P41 runtime

The wrapper does not import from the caller's `p41_runtime` string. It derives
the workspace root from its own file, extracts the fixed Git packet
`f27d1101048638bba395143a48efb7ef00bfcda4` /
`WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime`
into a private host temporary directory, and computes a deterministic tree
SHA256 over the actual runtime files excluding bytecode. The caller path is
accepted only if its tree hash equals the pinned tree. Imports use the pinned
copy, purge preloaded `bootstrap`/`p41_service`/`fixture`/`readthrough`/`product`
modules, and verify imported module files live under the pinned root. A forged
runtime returning canned receipts refuses before import
(`UNTRUSTED_P41_RUNTIME`); path/classname alone is never authority.

## 2. Trusted R05 execution context

`configure_trusted_execution_context` takes the actual accepted R05 learned,
step, empirical input, coordinator, execution request and original, verifies the
P41 pin, executes the actual `TrustedNativeGraphCoordinator`, and checks that
the returned original, consumer result and step are the captured ones. It
registers an opaque local handle in a module-private context registry. The
public view request supplies `execution_handle` plus view/field claims, not the
verifier, original or runtime. Actual-execution claims are compared to the
trusted context: forged runtime/original/learned/step refuse. A request without
a configured handle refuses (`TRUSTED_EXECUTION_HANDLE_REQUIRED`). This is a
trusted-host private context, not a cryptographic or R09 issuer.

## 3. Structural authority is honestly held

Every public wrapper (`select_world_view`, `select_joined_world_view`,
`select_r05_world_view`) returns `CONTEXT_STRUCTURAL_AUTHORITY_HELD` for any
CONTEXT field. A non-null arbitrary or real-type FF object is not issuance; no
competent retained FF issuance/authority closure is configured here, so the
edge stays HELD. No F5/F6/F7 science is issued. Directly declared synthetic
STRUCTURAL fields remain the genuine positive path.

## 4. Preserved repairs

Actual R05 learned/empirical -> actual P41 N9/N10W/E04 positive, two fields,
actual temporal payload change, cross-unit `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE`,
learned/source/evidence/fact/step/receipt severance and restore, cold
fresh-process replay and current/as-of/revocation remain. No original F7
measured-wave claim.

## Acceptance evidence

Author suite plus prior R06V probes and R3 successor probes (forged runtime,
forged original, equal-payload clock/hash, transport label, forged real-type FF
in R05 and joined wrappers, genuine positive/restore). Commands/JUnit/logs and
manifest are recorded in this R4 return. Distinct reviewer required; no
self-adoption.
