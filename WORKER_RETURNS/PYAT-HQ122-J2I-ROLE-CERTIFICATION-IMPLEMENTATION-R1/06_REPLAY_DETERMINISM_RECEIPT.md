# HQ122 J2I — REPLAY / DETERMINISM RECEIPT

Final qualified execution SHA:

`ef46892f8e2752b62eef0778b1bdb53a86d80e70`

Final governed court:

`36342507604`

Result:

`89 passed in 14.61s`

Protocol self-test:

`20 passed in 0.07s`

## Exact deterministic witnesses

1. A produced `ComponentAuthorityVectorReceipt@1.0.0` reloads through `reload_component_authority_vector_receipt` to the same exact ref and serialized semantic body.
2. Two M1 adjudications over the same exact bundle, exact J binding and exact validator registry produce:
   - the same disposition ref;
   - the same M1 replay ref;
   - the same determinant/explanation receipt.
3. The determinant contains the exact ordered per-component contribution rows plus exact aggregate counts and role-vector/prerequisite/replay identities.
4. Validator registration dispatch remains exact; changed validator parameters, role authority, or current-selection authority cannot reuse the old exact registration contract.
5. Role-vector serialized/preimage tampering fails closed before J certification.

Court artifact:

- id: `10939251772`
- ZIP digest: `sha256:e4a1e5f103de9abaf140e312eeca24cd4c2a3dc3e954307753a0922ba168de5d`

The temporary court-spec mutation used only to execute the GitHub court was reverted after qualification. The restored `.rabochii/court_spec.json` blob is exactly:

`67eb1c668c6d03a31f678d6b09db3288bd1ef810`
