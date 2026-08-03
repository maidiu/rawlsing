# Assembly provenance v27

Built from the byte-verified cumulative v26 outer archive plus the governing section 49 Plan v7 executable-closure correction and the enumerated v27 restart controls. The source archive is explicit; it is not a hidden dependency.

- Source outer ZIP: `Rawlsing_J_Family_Authority_Strategy_Handoff_v26_20260801(1).zip`
- Source outer ZIP SHA-256: `872cbff62dc03f964d0f09b8b2f545126700899e1377c4aa426f9827560d1fae`
- Source file count: `1,401`
- Governing builder: `validation/build_handoff_v27.py`
- Governing verifier: `validation/verify_handoff_v27.py`
- Whole-tree auditor: `validation/whole_tree_type_and_archive_audit_v27.py`
- Build rule: extract the accepted v26 archive; preserve every non-mutable v26 path byte-for-byte; apply the explicit v27 release overlay; regenerate section and package manifests; verify fail-closed.
- Live PostgreSQL write performed: no.
