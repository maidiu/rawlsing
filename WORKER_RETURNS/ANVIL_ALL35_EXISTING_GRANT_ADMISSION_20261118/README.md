# ANVIL existing-grant → R157 reader binding

**Scope:** source-read/C11 construction preparation only. This is not a new source right, scientific eligibility, CURRENT issuer, or I03/I05 authority.

## Exact pins

- R157 implementation: `aee95429609c372564e996c2d3d3eb30e9253cbf`
- SRC04 admission evidence: `f3000966fb05bda55fce8a804396a04eaf627a33`
- R157 config index: `ad3386b718fd9ace234a00dab3b32ee51039b77f`
- SRC04 grant: `303a57851785557fff8229e29a5554717168cbd1`
- SRC17 construction-only grant: `5b1b9bd5f04f0456eac319264a6f2b64d4e87038`
- SRC04 config: `da23c65d1e211cb7e8ce416e98757f321b78d25e`
- SRC17 config: `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`

The module imports the exact R157 `SourceReadRequest`, `IssuedSourceReadDecision`, constants, and `SourceReadDecisionResolver` interface from the frozen snapshot. It never imports or invokes a decoder and never opens/stats/hashes/reads the source path.

## Run

```bash
cd WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118
PYTHONPATH=. ANVIL_R157_SNAPSHOT=/path/to/aee954-snapshot \
  python3 run_binding.py
```

`SRC04_BINDING.json` is a request-only result. The actual run is intentionally **held**: no independently authenticated CURRENT evidence is supplied. A static grant hash is not CURRENT.

## Executable contract

- Static grant bytes are checked against `TRUST_POLICY.json` (`d8f13c67…`), schema, source identity, host, purpose, consumer, full-source scope, and exact request fields.
- The exact R157 `SourceReadRequest` is built from the frozen SRC04 config identity, locator, metadata witness, host, purpose, consumer, exact-file decode operation, and source-native/no-adoption scope.
- A positive decision requires an external Ed25519-signed current envelope whose signature, issuer, grant permission ref, request digest, decision ref, currentness, revocation, effective interval, and retention/export limits all match. The signer key and expected envelope hash come from external trust.
- A missing/tampered/non-current/revoked/mismatched current record fails closed. There is no fallback to the grant document's static `currentness`.
- `ExistingGrantResolver` is the concrete R157 `resolve_current` adapter; a hold raises rather than returning a fabricated decision.

## SRC17 check

`SRC17_SCOPE.json` records the exact construction-only grant/auth probe. It is source-specific to SRC17, purpose `SECOND_FAMILY_ORIGINAL_SOURCE_C11_POSITIVE`; it is **not reusable for SRC04**, and it authorizes **no I03/I05 expansion**. No SRC17 source read was performed.

## Outcome

`RUNTIME_ISSUER_HOLD__INDEPENDENT_CURRENT_EVIDENCE_MISSING`

The request/contract is executable. The existing exact SRC04 grant is structurally valid, but no independently authenticated CURRENT evidence exists in the available evidence set. A caller cannot manufacture that evidence by asserting `CURRENT_GRANTED` or by hashing the grant.

Tests use a **TEST_ONLY** ephemeral key solely to exercise the signed-current contract; they do not create production authority.

```text
9 tests passed
```
