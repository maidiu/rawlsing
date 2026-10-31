# SOROK O-INDEX R3 — exact source-object integrity and six product-link repair

**Return:** `WORKER_RETURNS/SOROK-OINDEX-R3-SOURCE-AND-PRODUCT-LINK-REPAIR-R1`
**Repository:** `maidiu/rawlsing` private
**Branch:** `agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1`
**Commission head:** `024f3b09b17ca5769c0bdee8d5eec459e31bb247`
**Candidate base:** `96af4f15c993c7a4f32da4cc31ef3175903a0d5c`
**Controlling review:** `3f3d9ec2fddc36bd4047bc6c730382c65a5e692a`
**Build PRE-MAIN:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`
**Last verified:** `87755f02ec5c37499b09e80db6fbdcc9316a6b15`
**Refreshed current PRE-MAIN:** `d0342290b257f85c3e8931f9962e0aecabc84ed3`
**Model/host:** OpenCode 1.18.34 / `opencode-go/deepseek-v4.1-flash`, local oldMac, MAX requested
**Final remote SHA:** reported in the terminal push readback; a file cannot contain its own commit SHA.

## Result

The exact R2-IR source and product-link deficiencies are repaired in the working
O-INDEX candidate.

- A frozen **167-row source manifest** now covers 144 Sorok + 23 Pyat rows plus
  3 reference sources.
- `verify_source_manifest.py` resolves all **167 source rows and 3 references**
  against actual Git objects, object types/ids, timestamps and the R15 tree file
  list; result `PASS`, zero errors.
- The B3A/B3AS/S39_S52 paths, the B1/B2/B3/BP2P4J null blobs and R15_V2's tree
  identity are corrected.
- The validator now rejects forged non-S source objects, forged source
  consumer claims, forged Pyat objects, forged timestamps/metadata, typed actual
  consumers without evidence, damaged lineage evidence and R15 tree-as-blob.
- Six product workstreams have specific L0–L5 paths, alternatives, owner slots
  and falsifiers: S5 flourishing, S7 player praxis, S11 UX, S13 monetization,
  S14 safety/privacy/abuse and S15 alpha/evaluation.
- The candidate now has 219 nodes, 461 edges, 80 L3 nodes, 46 owner slots and
  21 tests plus 4 lineage-source subtests.

## Four-column analysis

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| R2-IR correctly found source path/blob/consumer validation could pass forged values. | A regular expression or nonempty field is not source identity. | Frozen manifest + real Git refresh verifier; offline consistency and Git identity separated. | R3 index engineer |
| B3A/B3AS/S39_S52 paths, B1/B2/B3/BP2P4J blobs and R15 tree were wrong/missing. | The source claims were incomplete even though IDs and witnesses existed. | Exact repository paths, object types/ids and tree files are now frozen; no invented bytes. | O-INDEX author / source owners |
| S5/S7/S11/S13/S14/S15 were flattened into `L1_GOVERNANCE`. | The six original product obligations were not traversable. | Added specific L0 purpose, L1 organ, L2 alternatives, L3 spec/source status, L4 owner output, L5 falsifier and owner slots. | O-INDEX author / Sorok HQ |
| Old counts, proof epoch and current-PREMAIN label were stale. | The map was not a clean current source of truth. | Updated to 219/461/46, 21 tests, `POST_SOURCE_CORRECTION`, build/last/current PRE-MAIN distinction. | O-INDEX author |
| R6/R7, F1CR source absence, ZIP mismatch, four author-tested assets and historical REDs remain separate. | Recovery evidence must not be promoted into native person or scientific acceptance. | Preserved at exact grain and unpooled; no native/A5/priority claim. | R6/R7/asset owners and HQ |

## Three courts

### ENGINEERING

**PASS (local source-index repair).** The source manifest and Git refresh
verifier pass 167/167 + 3 references; the validator passes its 21 tests and 4
lineage subtests; six product paths are present; all required fault classes fail
for their claimed reasons; restored candidate is GREEN.

### SCIENTIFIC

**HOLD.** The six workstreams now carry their exact original questions/outputs
and specific L0–L5 candidate paths, but their normative, praxis, UX, economic,
safety and evaluation outputs remain `SPEC_REQUIRED_NOT_IMPLEMENTED` or
`EXISTING_SOURCEFREE_PARTIAL`. No native science, human A5, or scientific
issuance is claimed.

### AUTHORITY

**HOLD.** No CAN/ADP/SCI05, Pyat N11/N12/C0, C9/C12, native B, native A5,
owner adoption or PRE-MAIN merge is issued. The six product links are
`CONCEPTUAL_HQ_CANDIDATE_EDGE`, not adopted law.

## DONE

- Built the exact Git-object source manifest and S2 refresh verifier.
- Audited all 144 Sorok and 23 Pyat rows; corrected all reviewed path/blob/tree
  defects.
- Strengthened validator and tests to 21 tests + 4 lineage subtests.
- Added six specific S5/S7/S11/S13/S14/S15 L0–L5 product paths and owner slots.
- Corrected counts, epochs, stale readback and build/current PRE-MAIN labels.
- Preserved R6 39/94/133/26/9, R7 102 definitions, F1CR absence/reconstruction
  distinction, V3 ZIP mismatch, historical REDs and four author-tested assets.

## REMAINING

- Independent review of this repaired candidate; none performed here.
- HQ scientific/product synthesis of the six workstreams; the index is an aid,
  not the decision.
- Owner selection for normative flourishing, user-praxis, UX, monetization,
  safety/privacy and alpha/evaluation outputs.
- Any native source grants, C9/C12 adoption or human A5 evidence.

## CRITICAL_BLOCKERS

- No native/owner scientific issuance; no human A5 participant evidence.
- The six product links are conceptual HQ candidate edges, not implemented
  product functions.
- The four engineering assets remain author-tested, unadopted sourcefree
  candidates.
- No priority selection or PRE-MAIN adoption.

## LARGEST_PRODUCTIVE_MOVE

Have an independent reviewer and competent HQ examine this repaired source map
against the six product paths; then decide which owner output, if any, is
required next. Do not turn validator GREEN into native/person acceptance.

## FLIGHT

Local S2 sourcefree Git/Python/pytest only. No original survey, provider/model
call, native actor/world, production import, PRE-MAIN mutation, branch rewrite,
PR edit, self-review or owner adoption.

## DELTA

The O-INDEX moves from a source-blind, generic-governance mapping to a
digest-bound Git-object manifest with a real refresh verifier, corrected source
identities, and six specific product-workstream traversals, while all native,
scientific, authority and priority claims remain held.
