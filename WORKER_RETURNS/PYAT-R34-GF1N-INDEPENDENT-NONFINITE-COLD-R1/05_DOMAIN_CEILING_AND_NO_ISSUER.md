# GF1N — measured typed-domain ceiling and explicit no-issuer boundary

## Demonstrated positive ceiling

The only native positive claimed here is the original source-native binary string
domain `'0'/'1'`, with exact native roles, exact 2×2 denominators, `RAW`
`SINGLE_UNIVERSE` scope and `SOURCE_FREE_DEV` custody. It passes the original 44,
the frozen GF1G/GF1H 26, GF1J 3, GF1L 14+10, GF1K 12, the author guard 26, the
current 102+19 successor courts and the two-process 82-case cold replay.

Additional **TEST_ONLY finite controls** were accepted only when the inherited
result serializer can preserve them losslessly:

- integers and finite floats with distinct result keys: `(0, 1.5)`, `(2**100, 2**100+1)`,
  `(5e-324, -5e-324)`, `(1e308, -1e308)`, `(1.7976931348623157e308, 1.0)`,
  `(2.2250738585072014e-308, 5e-324)`;
- strings and heterogeneous scalars: `('a', 1)`, `('é', 'e\u0301')`, `('a:b', 'a|b')`,
  `('', 'a')`, `('0', '00')`, 10k-character strings.

For an accepted shape, the exact counts, conditioner/target role keys and types,
support total, two rows/two cells, deterministic 64-hex result hash and strict JSON
(`allow_nan=False`, no duplicate object names) are conserved. Reverse orientation
of a symmetric heterogeneous domain preserves the support vectors; an asymmetric
6-support case preserves every count and the `NO_PAIR_SEPARATION` class under
`(0,1.5)→(1.5,0)` reversal.

## Refused or fail-closed shapes

| Shape | Independent result |
|---|---|
| `+inf`, `-inf`, `NaN` in conditioner or target domain | `CONSUMER_RELATION_INTEGRITY_REJECTED`; class `None`; no downstream hash/support/signature; strict JSON |
| nonfinite in row/cell state or in counts | typed consumer refusal |
| nonfinite float subclass (`InfFloat('inf')`) | typed consumer refusal |
| `(0, False)`, `(0, 0.0)`, `(1, True)`, `(1, 1.0)` | typed refusal: Python mapping-key collision |
| `(0, '0')`, `(0.5, '0.5')`, `(-1, '-1')`, `('0', `Text('0')`)` | typed refusal: result-key serialization collision |
| `(1.0, '1.0')`, `(1e308, '1e+308')` | typed refusal: same serialized key text |
| `(True, 'true')`, `(False, 'false')`, `(None, 'null')` | typed consumer refusal (mixed legacy canonicalization sort) |
| `(-0.0, 0.0)` as the two domain states | typed refusal: same-type equal categories are not two states |
| swapped target cells, duplicated condition rows | typed consumer refusal |
| `True`/`1.0`/`-1` as a count or denominator | typed consumer refusal (exact nonnegative `int` only) |
| joint support > eligible risk; denominator ≠ row sum | fail-closed, class `None`, downstream false |
| typed `ZERO_SUPPORT` | `UNDETERMINED_ZERO_SUPPORT_RISK`, downstream false |
| observed zero with eligible risk | `UNDETERMINED_ZERO_SUPPORT_RISK` computed, strict JSON |
| eligible risk set empty | `UNDETERMINED_NO_ELIGIBLE_RISK` computed, strict JSON |
| missing / unresolved / nonresponse typed state | producer-blocked HOLD, class `None`, downstream false |
| valid empty profile | `RESPONSE_INPUTS_VALID_EMPTY`, downstream false |
| non-relation input | `CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION`, no downstream |
| self-rehashed forged provenance/authority | computes as TEST_ONLY, `production_owner_commit=false`, no issuer field |
| mismatched self-hash/object-id | typed native construction refusal |

## Explicit limits (not hidden as passes)

1. **Arbitrary Python objects are not claimed.** `Decimal('Infinity')`, `Decimal('NaN')`,
   `complex` and `bytes` fail in the original producer's canonicalization
   (`PRODUCER_DOMAIN_LIMIT`, `TypeError`) before any consumer value. The candidate
   guard is not a universal serializer and no such support is adopted.
2. **Signed-zero row alias.** A finite `0.0` domain with a `-0.0` row state is
   matched by exact type-and-value Python equality (`-0.0 == 0.0`), so the sign bit
   is not a separate scientific identity. The *domain pair* `(-0.0, 0.0)` is refused
   because two declared states are not distinct. This is a measured value-equality
   limit, not a claimed bit-preserving category storage.
3. **Auxiliary signature text.** `separation_signature` concatenates category
   text for human audit; it can be ambiguous for exotic concatenations. It is not
   the support vector and is bound into `result_hash` together with the exact
   `support_vectors`, counts, class and relation identity. No count is lost by it.
4. **The guard is not a general JSON round-trip claim.** It refuses shapes the
   inherited serializer cannot preserve; it does not promise that arbitrary JSON
   decode/encode reconstructs every Python type.
5. **In-memory tamper limit (non-blocking, outside the value contract).** If a caller
   bypasses the frozen dataclass with `object.__setattr__` and installs a mixed-key
   dict as a relation ref, the defence-in-depth `_verify_identity` recomputation
   raises an untyped `TypeError` from legacy canonicalization instead of returning a
   typed refusal. No downstream value, class or result hash is produced. The same
   `_verify_identity` body exists in the prior `d97a5df8` consumer and is unchanged
   by the nonfinite repair. Recommended hardening: broaden that handler to
   `(GenericNativePairError, TypeError, ValueError)` and return the existing
   `CONSUMER_RELATION_IDENTITY_MISMATCH`. Exact falsifier:
   `postinspection/in_memory_tamper_limit.json`. This is not a native-category
   acceptance and not a scientific RED; a caller who can mutate a frozen attribute
   in-process can replace the consumer module itself.

## No issuer

`GenericNativePairRelation` content hashes and object ids are structural
self-identities. A consistent attacker can rehash its own relation and provenance
references; the schema contains no independent issuer/signature field. GF1N
independently re-ran the forged-provenance control: the result still computes at
TEST_ONLY grain with `production_owner_commit=false`, `generic_native_semantics_hold=RETAINED`
and no issuer field. Exact source import proof is custody evidence, not signatory
authentication. No external issuer, source-artifact revocation, temporal ownership,
OC05, N11/N12, original35, Field Forge, N10W, Sorok, actor/V3 or production
authority is created.
