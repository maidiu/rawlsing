# W56M blocker reconciliation

W56M terminal `4d7e806ac31317d500b94a18171d76295ebf01f7` is preserved as the hostile finding that W56L's process provenance repair was genuine but incomplete at the object/ref grain.

Exact W56M blocker token:

`FAIL_CLOSED__INTERNAL_GIT_OBJECT_STORE_SYMLINK_REDIRECTION_ALLOWS_OID_BYTES_SUBSTITUTION`

The blocker has two distinct causes and therefore two distinct repairs.

1. **Object identity.** W56L treated successful `cat-file` output for an exact OID as sufficient immutable-object evidence. W56M demonstrated that redirected loose-object storage could make trusted Git return bytes under a requested pathname while the returned bytes were not cryptographically rebound to that OID. W56N therefore treats Git only as the bounded object-byte transport and independently rehashes every trust-bearing commit/tree/blob payload before trusting it.
2. **Ref provenance.** W56L delegated full-ref resolution to `rev-parse`, allowing a symlinked ref path to source a mutable ref value outside the pinned `.git` tree. W56N therefore reads the trust-bearing full refs directly through a non-following bounded metadata reader, with strict loose/packed rules, before separately verifying the resulting commit OID.

W56N deliberately does **not** respond by recursively requiring physical uniqueness or non-symlink status for every object-store descendant. For object X, storage location is not authority; `GitObjectHash(expected_type, exact_payload) == X` is authority. A loose object, packed object, or other Git-readable storage representation is acceptable only when the returned bytes cryptographically rebind to X. Conversely, bytes that do not rebind to X fail regardless of where Git obtained them.

No W56M negative evidence is erased. W56L remains recorded as the process-trust repair; W56M remains recorded as the court that defeated complete certification; W56N is only the local unreconciled successor submitted for a new independent review.