# 01 — Existing owner and external field adapter

**Read cut:** sealed startup of this commission; N9C return
`9ab4a0192b7c951bb0b387637e6c74333246766c`; D2I return
`2653fff57ac59fe2eaeffd24a0611c45f16f3b54`; current-tree owners verified by
Git blob SHA-1 (NUL header) against the pinned blobs.

## 1. No accepted external-published-aggregate producer exists — REUSED, not reinvented

Search for a versioned accepted external-original-published-aggregate
source/field adapter and issuer in the current tree:

| Candidate | Exact identity | Verdict |
|---|---|---|
| `rawlsing_next/pre553_learned_world_composition.compose_direct_producer` | blob `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` == current tree | **REUSED as transport.** It is not an original-PDF adapter and not a field issuer: it records an explicitly authorized direct consumer route and refuses anything else (BLOCKED receipts otherwise). Requires exact route authority + consumer acceptance. |
| `rawlsing_next/objective_consumer_bounded_evidence.py` OC05 | blob `f30fca20e7b56e00348e82765d95f974b4b6a195` == current tree | **OC05 `NOT_YET_APPLICABLE`, `seam=None`.** Not a consumer; not exercised as one. |
| `pre553_hq297_n9c_two_field_reader` in current `rawlsing_next/` | absent | N9C reader is a candidate return file, **not** an installed owner. Reused by attributed byte copy into this return's isolated terrain (blob `03eb46efccadd6880cb34b2e2ac609ffc9b16c59` verified). |
| Any versioned accepted GSS/NCA `ExternalPublishedAggregateField` product | absent from tree and from both returns | **Not present.** D2I's conclusion stands: N5/N6 field producer/issuer is not positive. No competing issuer is created here. |

**Decision:** reuse the two transport-capable owners exactly as they are
(`compose_direct_producer` as the direct route; the N9C reader as the
two-value consumer), and write the single missing piece — a minimal test-only
`ExternalPublishedAggregateField` candidate producer — without touching either.

## 2. What the reused owners actually do (independent verification)

- `compose_direct_producer(contract, ingress)` with `route="DIRECT_PRODUCER"`:
  records an explicitly authorized direct consumer route; refuses with typed
  BLOCKED receipts for any other route, lifecycle smuggling, or owner/contract
  mismatch. Executed here with a TEST_ONLY contract; receipt
  `terminal_state=SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND`,
  `reason_code=DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED`. This is a recorded
  route on test-only material, **not** N5/N6 issuance, EE13, N7, N9 or OC05.
- `n9c_reader.read_historical_test_only`: dereferences two refs to actual
  numerics under `HISTORICAL_PUBLICATION_AWARE` clock, publication-aware
  cutoffs, revocation, explicit nonpooled relation, no person/pool/model use.
  47/47 reproduced read-only.
- OC05: `NOT_YET_APPLICABLE` everywhere it appears; never invoked as a consumer.

## 3. Typed source authority requirements (producer boundary)

Every produced field must satisfy `check_field_authority`: `fixture_only is
True`, `issued is False`, `issuer_signature is None`, `source_pdf_sha256 is
None`, `issuer_ref is None`, `permission == TEST_ONLY_NO_EXTERNAL_USE_GRANT`.
Anything else is `ISSUER_FORGERY` / `UNVERIFIED_BINARY_CUSTODY` /
`REAL_USE_PERMISSION_NOT_ISSUED` / `FIELD_ISSUANCE_LAUNDERING`. The producer
cannot manufacture issuance; it can only bind test-only rows into versioned,
content-addressed field records.
