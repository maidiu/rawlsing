# FIABC-R35-I02 — Generic Derivative Parentage Contract

## 1. Governing implication

The only admissible generic ancestry chain is:

```text
canonical raw source observation
  -> immutable source-verification receipt
  -> governed derivative producer / operation / reader config
  -> immutable derivative-parentage receipt
  -> derivative identity/hash
```

The reverse inference is forbidden:

```text
derivative.source_sha256 == canonical_sha
  -/-> derivative descended from canonical source bytes
```

Likewise, filename, path, row count, column count, apparent semantic equality, internal self-hash, or carrier self-consistency do not prove raw ancestry.

## 2. Source-verification receipt

Schema: `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`.

Required bound fields:

- canonical `source_id`;
- canonical source SHA-256;
- observed source SHA-256, required to equal canonical SHA;
- exact raw-verification operation;
- producer identity;
- producer code/blob identity;
- producer version;
- reader/config;
- scope determinants;
- currentness determinants;
- source/root/process/candidate ownership where applicable;
- canonical receipt identity = SHA-256 of canonical unsigned receipt.

A consumer may additionally pin the exact expected source receipt identity.

## 3. Derivative-parentage receipt

Schema: `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`.

Required bound fields:

- canonical source identity/SHA inherited from the verified source receipt;
- derivative class;
- derivative identity;
- derivative SHA-256/hash;
- derivative metadata required by the derivative class;
- exact producer identity/blob/version;
- exact derivation operation;
- exact reader/config when source decoding participates;
- scope determinants;
- currentness determinants;
- source/candidate/root ownership where relevant;
- `parent_receipt_identity`;
- optional `replay_parent_receipt_identity`;
- canonical derivative receipt identity.

The derivative receipt must close to the supplied source receipt by exact receipt identity. Consumers may pin the exact derivative receipt identity independently.

## 4. Bundle

Schema: `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`.

The bundle contains both receipts and is itself sealed by `bundle_identity`. This keeps the receipt external to the derivative payload while preserving a portable immutable chain.

## 5. Admission law

A derivative consumer must fail closed unless:

1. bundle identity recomputes exactly;
2. source receipt identity recomputes exactly;
3. observed raw SHA equals canonical source SHA;
4. any frozen expected source receipt identity matches;
5. derivative receipt identity recomputes exactly;
6. any frozen expected derivative receipt identity matches;
7. derivative `parent_receipt_identity` equals the verified source receipt;
8. derivative identity/hash/metadata equal the derivative being consumed;
9. producer/operation/config equal the governed expected values;
10. scope/currentness/ownership equal the current consumer contract;
11. any replay-parent identity equals the declared replay lineage.

## 6. Compatibility decoding

Compatibility mode is carried as a physical execution determinant only.

For LiTS-I the accepted tag remains:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

A compatibility-decoded persisted copy without an external derivation receipt is not admissible. A successful compatibility decode does not create source-text semantic authority.

## 7. Authority boundary

A passing parentage receipt proves a physical/provenance statement only:

> this derivative is the governed derivative identified by this receipt chain from this canonical source root under these exact determinants.

It does not prove what the survey means, resolve documentary ambiguity, select weights, authorize a population estimand, certify the entire source, retire raw bytes, or replace the I05 semantic court.
