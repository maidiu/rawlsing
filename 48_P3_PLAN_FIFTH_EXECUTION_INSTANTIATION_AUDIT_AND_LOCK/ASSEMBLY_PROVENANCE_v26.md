# Assembly provenance v26

Built from the byte-verified cumulative v25 outer archive plus the delivered section 48 Plan v6 contract and the v26 mutable restart controls. The source archive is explicit; it is not a hidden dependency.

- Source outer ZIP: `Rawlsing_J_Family_Authority_Strategy_Handoff_v25_20260801.zip`
- Source outer ZIP SHA-256: `29448f6a7e800288ca08796003a4b78680a7817aa0f6d40c293b488a95659c03`
- Governing builder: `validation/build_handoff_v26.py`
- Governing verifier: `validation/verify_handoff_v26.py`
- Whole-tree auditor: `validation/whole_tree_type_and_archive_audit_v26.py`
- Build rule: extract the accepted v25 archive; preserve sections 01-47 byte-for-byte; add section 48; replace only the enumerated mutable restart/release controls; regenerate section and package manifests; verify fail-closed.
- Live write performed: no.
