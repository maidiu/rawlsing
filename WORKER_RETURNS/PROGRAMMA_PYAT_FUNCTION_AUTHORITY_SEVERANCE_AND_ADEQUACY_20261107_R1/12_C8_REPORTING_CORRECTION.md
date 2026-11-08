# C8 mechanical reporting correction

C8 immutable review `356124ee452d8cababaae7f2f57d05e8f0d17deb` returned REVISE on metadata4ded5734/content5efb9fa3. HQ repaired only its three observed schema/lineage defects. Independent focused confirmation remains pending; goal_complete=false.

- C8-001/002: all51 CASE EVIDENCE_GRADE cells in02 now derive from canonical03;23 stale fields corrected, counts21 FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED /30 NOT_RUN. Inventory/noncase rows retained.
- C8-003: exact C1/C2/C4 lane cuts synchronized in02 SOURCE_SHA,06/09 tables,03 C4source_cut andCHECKPOINT.source_cuts. C5/C6 integration cuts retained for their own families; no changes to underlying A-J cases.
- Canonical/alias03 byte-identical, newSHA256 `cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251`;51uniqueIDs and all other record fields retained. Old cuts and prior report remain inGit; C8review immutable.

No code/test/source/respondent/native/S3/science/actor/CI/protected changes; no new investigation or full review. Commands: deterministic Python JSONL/TSV mapping against canonical03; assertions on ID sets, A-J/content equality except two C4source_cut fields,23changedgrades and21/30counts; SHA256 equality.
