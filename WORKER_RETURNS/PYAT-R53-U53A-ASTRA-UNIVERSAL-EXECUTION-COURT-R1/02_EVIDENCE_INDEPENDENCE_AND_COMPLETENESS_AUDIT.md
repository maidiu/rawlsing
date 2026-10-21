# Evidence independence and completeness

Status: **PARTIAL**, with independently corroborated startup census and targeted code findings. Existing requirements oracle was committed at a79dfcf85c65195c9b6d264fd366b50a71b4b5a2 before this continuation consumed U53F interpretations. It is preserved unchanged.

## Proven identity and custody

- Sealed startup f148f9ba34deb0ae2ad3983fe94bbcef8f004b03; commission blob 35ecac4ef3e8406d2a99ef87ed16184da0c9f549.
- U53F actual remote head fdc4d03537e649cd56c19a458ebeb3292298ff3f; manifest observed_head 872aaee746e12ee933af94e58d069b2506b270e7 is an earlier observation.
- GitHub recursive startup tree: truncated=false, 9,129 tree/blob entries, 7,615 blobs. This independently matches the reported ls-tree file count. No AGENTS.md appeared in that tree.
- Six U53F text artifacts were independently SHA256-recomputed in JavaScript and matched the manifest: return, graph, unresolved edges, timeline, refs_inventory.py, graph_build.py. Two known hash vectors passed. Exact results are in evidence/SELECTIVE_HASH_VERIFICATION.json.
- R53 dispatch seal is absent at startup because it was written after the commissions. At immutable R53 checkpoint 13a75d7c0979ea0f7d7cf58afad4cb3d5d1f7c8e its blob is 82d914f336ce744b07e3b4f651d6c68732e899ff and it confirms the user-supplied startup. This is not a contradictory seal.
- Live integration LATEST at read points to that R53 checkpoint, rev37. Its worker statuses are publication-time records, not evidence that returned U53F is still unlaunched.

## U53F challenge

1. Its 966 material refs are selected by name/subject regex, plus eight mandated commits (E:tools/refs_inventory.py). This is a bounded selection, not all relevant code proved reachable. It explicitly did not refresh remotes. Its output retains included refs and aggregate exclusion reasons, not a complete per-excluded-ref reason ledger in that file. Historical unique commits unreachable from retained refs remain outside the claim.
2. Its 22-node graph is curated in graph_build.py. AST/import edges corroborate local code dependency, not runtime reachability, product consumption or all-node completeness. B49/G50/I51 are not graph nodes despite being central to the mission. The node called i05 is the empirical possibility provider; exact I05 discovery is called compiler. Our graph uses distinct meanings.
3. Its statement that compiler and Batch are not statically joined in sealed canonical modules does not establish a missing execution function. U43 candidate execute_issued_workload already calls both Route B and Batch with discoveries (E:issued:270-342). Canonical adoption and general frontier construction remain separate.
4. Candidate-C's source restriction is explicit, rejects unknown sources, and belongs to a bounded physical-route candidate (E:binding:1-12,408-415). It must not be promoted to universal orchestration; its two-source registry alone is not a defect in selected Route B. The current Route B directly binds source-backed C11 (E:routeb:494-590).
5. A zero LiTS/q301 literal scan cannot establish genericity. G50's Y/ID injection and native map are a counterexample; B49 has synthetic identity/topology assumptions.
6. The roster builder labels literal source-name hits as EXPLICIT_LOCAL_ADAPTER_PRESENT (E:roster_builder:83-111). That is a search heuristic, not verified adapter reachability. Its country_scope comes from question-relation authority rows and cannot be promoted to complete survey geography. Format is explicitly unknown. Use the authoritative estate matrix for 35 identity obligations.
7. The timeline labels AS2A by the enclosing R1 date; the primary document names as2a-lits1-shared-cert-20260827 (E:AS2A:15-19). This court records Aug27 lineage rather than claiming the release happened Aug25.

## Unverified denominator

The 1,712,461-byte U53F tree ledger returns empty through fetch_file; raw fetch returns INVALID_ARGUMENT/too-large-or-unsupported. Its full row/blob equivalence is unverified. The 23,268,989- and 14,082,081-byte diff shards and 23,452,783-byte leakage ledger were not retrieved or independently replayed. No claim that every ledger entry received an independent semantic disposition is made. Original 700-row authority CSV also exceeded this fetch mechanism; the 988,616-byte estate matrix was readable and supplies exact 35 SRC identities, names and 54 obligations each.

Targeted source access is sufficient for the findings and proposed repairs in this return. It is insufficient for the complete architectural/historical court acceptance originally demanded. Dynamic loading in world wrappers, current independent adoption of all candidates, omitted branches, all F/EE/AT dossiers and earliest historical promotion remain an exact unresolved frontier. No source runtime, SAV/DTA respondent payload or production code execution was used. Tests below are PROPOSED_NOT_EXECUTED.
