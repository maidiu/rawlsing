# ANVIL existing-grant → R157 reader binding

**Scope:** source-read/C11 construction preparation only. This is not a new source right, scientific eligibility, CURRENT issuer, or I03/I05 authority.

## Correction

The prior revision invented an Ed25519 envelope that is not part of the accepted `SourceReadDecisionResolver` contract. It is removed. This revision follows the historical accepted SRC04 route at `303a57851785557fff8229e29a5554717168cbd1` (`validate_grant_document` + `FullGrantResolver`) adapted only to the exact typed `aee954` R157 interface.

No stronger adopted authority requirement was located in the cited evidence; the accepted exact-grant route remains the control.

## Exact pins

- R157 implementation: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- SRC04 admission evidence: `f3000966fb05bda55fce8a804396a04eaf627a33`
- R157 config index: `ad3386b718fd9ace234a00dab3b32ee51039b77f`
- SRC04 grant: `303a57851785557fff8229e29a5554717168cbd1`
- SRC17 construction-only grant: `5b1b9bd5f04f0456eac319264a6f2b64d4e87038`
- SRC04 config: `da23c65d1e211cb7e8ce416e98757f321b78d25e`
- SRC17 config: `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`

## Bind/check semantics

- Exact grant file location and SHA-256 pinned by `TRUST_POLICY.json`.
- Exact grant schema/source SHA/rows/columns/bytes, host, purpose, consumer, full-source scope, authorization, currentness `CURRENT_GRANTED`, and revocation `NONE_RECORDED` validated.
- Exact R157 `SourceReadRequest` built from frozen SRC04 config identity, locator, metadata witness, host, purpose, consumer, `SOURCE_RESPONSE_DECODE`, `EXACT_FILE`, and source-native/no-adoption scope.
- `ExistingGrantResolver.resolve_current` is the concrete R157 callback. Every call rechecks the identical bound request and re-reads the exact grant at the exact location, refusing grant drift and revocation.
- No source path is opened, stat'ed, hashed, or decoded. No caller claim or mere snapshot presence can become permission.
- Retention/export is fixed: export DENY, rowwise artifacts DENY, local runtime only, source bytes outside Git.
- SRC17 remains exact construction-only and is not reusable for SRC04 or I03/I05.

## Run

```bash
cd WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118
PYTHONPATH=. ANVIL_R157_SNAPSHOT=/path/to/aee954-snapshot \
  python3 run_binding.py
```

Actual request-only result: `REQUEST_ONLY_ALLOWED`; decision ref `FULL_SOURCE_READ_DECISION|…|63983453…`; pre/post callback decisions identical. No source operation performed.

## Tests

11 passed: exact request-only allow; callback recheck twice; wrong request; grant drift; grant location drift; revocation; wrong scope; snapshot-presence-alone refusal; wrong survey config; expanded operation/extent; SRC17 boundary.

```text
11 tests in 0.012s — OK
```
