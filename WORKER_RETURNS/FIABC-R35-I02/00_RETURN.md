# FIABC-R35-I02 — Generic Derivative Parentage / Provenance Receipt

Status: `COMPLETE__IMPLEMENTED__BROWSER_ONLY_QUALIFICATION_NOT_EXECUTED`

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-premain-fiabc-s35-fanin-r1`

Branch: `agent/rabochii-premain-fiabc-r35-i02-derivative-parentage-r1`

## Holding

The S35 generic derivative-parentage gap is closed at the implementation/consumer-contract level.

The governing chain is now mechanically expressible and verifiable as:

`DERIVATIVE IDENTITY -> GOVERNED PRODUCER / OPERATION / CONFIG -> IMMUTABLE PARENT RECEIPT -> CANONICAL SOURCE SHA`.

A derivative's own `source_sha256` field is not accepted as parentage.

The generic implementation is `rawlsing_next/fiabc_derivative_parentage.py`. It creates immutable external source-verification receipts, derivative-parentage receipts, and sealed bundles. Receipts bind canonical source identity/SHA, observed raw SHA, producer identity/blob/version, derivation operation, reader/config, scope/currentness determinants, ownership, exact parent receipt identity, optional replay-parent identity, derivative identity/hash, and derivative metadata.

## Current dangerous edges

### LiTS-I Candidate A preserved R5

The production consumer no longer accepts `RAWLSING_EE_P2X_LITS_A_R5_ROOT` by path plus self-consistent root alone.

It additionally requires:

- `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT`;
- `RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY`.

The pinned receipt must close to canonical LiTS-I SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`, the exact R5 physical root, logical stream/member inventory evidence, frozen Candidate-A owner/runtime determinants, exact builder identity, and the physical-only latin1 compatibility reader configuration.

The implementation does **not** fabricate a historical receipt for an already-existing carrier. If that historical carrier has no admissible external first-build receipt, current consumption stops. That is the required disposition, not a permission to infer ancestry from its embedded source SHA.

### WVS7 structural preimage

When the canonical WVS7 SAV is available, the exact accepted materializer performs the source-backed structural extraction; the backend then seals:

1. a canonical raw-SHA verification receipt;
2. a structural-preimage derivative receipt;
3. an external parentage bundle;
4. the receipt identities into durable candidate state.

Source-free reopen requires all four identities to agree with the frozen lineage. A detached/copied/self-rehashed structural JSON is rejected even if it asserts the canonical WVS7 SHA and reproduces the expected geometry.

## Hostile coverage authored

`tests/test_fiabc_derivative_parentage.py` covers:

- forged derivative with correct asserted source SHA but no receipt;
- copied/old R5 root;
- recomputed WVS structural-preimage self-hash;
- correct row count with wrong ancestor;
- compatibility-decoded persisted copy lacking derivation receipt;
- wrong reader/config;
- currentness drift;
- positive WVS and LiTS parentage closure.

No raw source carrier was opened in-browser. No measured P2X was run. No local-machine Codex was used. Tests were authored but not executed in this GitHub/browser-only commission; the exact qualification command is recorded in `04_TEST_PROTOCOL.md`.

## Scope boundary

This receipt proves governed physical/provenance ancestry. It does not certify survey meaning, documentary authority, population/weight authority, source retirement, or I05 semantic parity.

## Terminal

`FIABC_R35_I02_GENERIC_DERIVATIVE_PARENTAGE_IMPLEMENTED__CURRENT_LITS_WVS_EDGES_BOUND`
