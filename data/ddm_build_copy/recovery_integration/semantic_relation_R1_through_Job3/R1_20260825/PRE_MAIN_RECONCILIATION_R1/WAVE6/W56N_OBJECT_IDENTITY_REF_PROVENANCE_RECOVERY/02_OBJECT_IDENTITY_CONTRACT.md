# Object identity contract

Required proposition:

`TRUST_BEARING_GIT_OBJECT_BYTES_ARE_CRYPTOGRAPHICALLY_BOUND_TO_THEIR_REQUESTED_OBJECT_IDS`

For every trust-bearing Git object read:

- the request begins with one exact lowercase hexadecimal OID, 40 hex digits for SHA-1 or 64 for SHA-256;
- the OID width selects the hash algorithm and the object IDs referenced by a verified commit/tree must remain in the same hash family;
- the already-bounded trusted Git executable must report the expected object type and return the payload for that exact OID;
- before the payload is exposed as governance evidence, Python stdlib computes `H(expected_type || 0x20 || ASCII(decimal(len(payload))) || 0x00 || payload)`;
- the recomputed hexadecimal OID must equal the requested OID byte-for-byte; any mismatch fails closed.

The rule applies to trust-bearing `commit`, `tree`, and `blob` reads. A verified commit is the only source from which its root tree and parent OIDs are trusted. A verified tree is the only source from which child object OIDs and repository path components are trusted. A verified blob is the only payload used for canonical schemas, manifests, authorization/audit JSON, or other governance file bytes.

## Object location is not object identity

`OBJECT_LOCATION != OBJECT_IDENTITY`.

Git objects are content-addressed. W56N therefore does not require every descendant of `.git/objects` to be physically unique merely to prove identity. Normal loose and packed object storage remain admissible. Even if trusted Git follows some internal storage representation, the returned bytes have no authority until the independent Git-object hash recomputation binds them to the requested OID. Storage provenance cannot rescue a hash mismatch, and alternate storage cannot create a second authoritative object for the same OID without satisfying the same cryptographic identity condition.