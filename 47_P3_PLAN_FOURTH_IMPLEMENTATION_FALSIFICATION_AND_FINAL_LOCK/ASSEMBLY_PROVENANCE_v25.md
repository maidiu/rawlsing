# Assembly provenance v25

Built from the byte-verified v24 outer archive `Rawlsing_J_Family_Authority_Strategy_Handoff_v24_20260731.zip`. Section 47 is the fourth bounded implementation-falsification lock. It does not add a new ontology or platform. It repairs only executable contradictions or omissions exposed by instantiating the v24 contract against the real P2 graph topology and persistence requirements.

- Source outer ZIP SHA-256: `06de4c421dcb6c7c3d41b02037570c2e5cb4a368c84de0750e253512a69bdd16`
- Governing builder: `validation/build_handoff_v25.py`
- Governing verifier: `validation/verify_handoff_v25.py`
- Whole-tree auditor: `validation/whole_tree_type_and_archive_audit_v25.py`
- Build rule: extract the accepted v24 archive, replace only mutable restart/release controls, add section 47, regenerate manifests, and preserve all inherited substantive payload byte-for-byte.
