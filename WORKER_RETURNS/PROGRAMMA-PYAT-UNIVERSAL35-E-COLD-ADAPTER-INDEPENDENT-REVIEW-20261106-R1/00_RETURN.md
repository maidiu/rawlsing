# Universal35 E cold-adapter r2 — independent review

**VERDICT: ACCEPT_SCOPED_ENGINEERING** at frozen E head `bddef0b5ca40b750fd51770d47df22f2973679b4`.

- Code: `f708b4688f6aebd408510aa33faca453bd213749`
- Prior repaired head: `7d1aadfd4f655930ca2e65ea64cfa3df180a5f7b`
- Prior E review: `6334063ab290d6497e7b8047eb1292b69661f51e` (`ACCEPT_SCOPED`)
- Review branch: `codex/pyat-universal35-e-cold-adapter-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

The observed cold envelope adapter is an exact serializer/projection around the
already accepted `ingest_empirical_fact` owner. Fact/query objects are rebuilt
through the existing canonical constructors; supplied content hashes/object IDs
and schema identity are verified against computed identity. Replay fact ref,
query replay root, and provenance bind the supplied fact/query. Missing replay,
provenance, or permission fails closed; permissions require a nonempty producer
ceiling, and optional relation ceilings narrow only. Structural grant remains
false.

Direct API, cold `-m` subprocess, and the `run_ingress.py envelope` alias return
the same result. Changed counts/denominator produce a changed profile and
relation ref. Tampered supplied hashes/IDs/refs fail closed. No eval/pickle,
source lookup, second compiler, or native/science grant was introduced.

## GRADES

- **Serialization/trust boundary: PASS_SCOPED.** Exact constructors, schema,
  supplied content hashes/IDs, replay refs/root, provenance, and permissions are
  validated; no missing replay/provenance/permission auto-fill.
- **Owner delegation: PASS_SCOPED.** Existing owner result/profile or typed
  refusal is preserved; `structural_grant=false`.
- **Cold equivalence: PASS_SCOPED.** Direct API == subprocess == alias; changed
  counts change the denominator/profile/ref.
- **Permission/GT2 scope: PASS_SCOPED.** Nonempty producer ceiling; narrower
  relation ceiling preserved; widened relation returns typed refusal; GT2
  two-target RAW behavior remains the existing owner limit.
- **Authentic D/native: NOT_RUN.** No authentic D product, original bytes,
  empirical fact, FieldForge/science result, or protected promotion.

## LIMITS / PRESERVATION

- 20 ingress tests and 25 existing-owner regression tests PASS. Prior E r1
  accepted five-case semantic-linkage and refusal proofs remain unchanged.
- The supplied test envelope is explicitly `TEST_ONLY_SOURCEFREE`; no authentic
  D/native label is established.
- No product/test/guide/progress/controller/protected edit, code repair, native
  grant, source read, or protected merge. D authentic producer and A mappings
  remain independent.
- Canonical object identity is recomputed when optional `object_id`/`content_hash`
  fields are absent; this does not accept contradictory/tampered supplied values
  and grants no authority. `grade` is caller metadata copied to the result; it
  changes no permission, structural state, or profile.
- Output contains metadata only; no raw respondent rows or source bytes.
