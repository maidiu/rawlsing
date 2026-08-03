# Codex embedding instructions

1. Run `unpack_payloads.sh`.
2. Treat the unpacked repository tree as the integration source. The Git bundle is the authoritative history backup.
3. Start PostgreSQL 15 from the included offline runtime and run `restore_database.sh`.
4. Verify P3A:

```bash
python repository/82_P3A_V40_CLEAN_RECONSTRUCTION_BASELINE/code/verify_p3a_v40_reconstruction.py \
  --root repository \
  --dsn 'host=127.0.0.1 port=55432 dbname=rawlsing_p3c_work user=oai'
```

5. Verify the P3C inventory:

```bash
python repository/83_P3C_EVIDENCE_FIRST_INVENTORY_AND_FAMILY_MAP/validation/validate_section83.py
```

6. Use these Section 83 outputs as the adjudication input:
   - `P3C_EVIDENCE_FIRST_CANDIDATE_DETAIL.json`
   - `P3C_EVIDENCE_FIRST_MEMBER_MAP.csv`
   - `P3C_FINAL_PROPOSITION_FAMILY_MAP.csv`
7. Sections 63–80 are descriptive recovery records only. They may be used as regression clues but never inserted as authority.
8. The immediate implementation task is P3C replay contract installation and governed adjudication, preserving append-only canonical revisions, explicit `ALREADY_CANONICAL` status, split successors, exact obligation resolution, variants, named exclusions, and collision/stronger-boundary gates.
