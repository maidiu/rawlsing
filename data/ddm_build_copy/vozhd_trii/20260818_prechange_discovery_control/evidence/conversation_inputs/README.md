# Conversation Input Evidence

This directory records user-supplied evidence that materially changed the Vozhd Trii investigation.

The repository should not silently absorb historical binary packs or large database dumps as if they were production authority. Evidence is therefore preserved in one of two forms:

1. **exact repository copy** where the file is small, text-native, and directly useful to repeated courts;
2. **content-addressed reference** where the file is a historical archive, chat transcript, or large dump better retained outside production source control.

`SHA256SUMS.txt` is the identity manifest for the complete five-file conversation evidence bundle.

## Exact copy present here

- `Rawlsing_WVS_authority_reconcile_schema.sql`
  - SHA-256 `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`

## Hash-addressed source evidence referenced here

- `Rawlsing_WVS_public_schema.sql`
  - SHA-256 `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
  - current conversation attachment; 316,288 bytes
- `rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED.zip`
  - SHA-256 `e9c66a9638371966d620ef73c30f03c5dcca255cd874acbdf66e3738654b5861`
  - historical design/provenance evidence
- `rawlsing_v5_home_stretch_build_pack_v18_FINAL_LOCKED_NO_GHOSTS.zip`
  - SHA-256 `a654014fb56032544fc4044ee230cf69823e076cb5f3e4fc3df91eb3148f12bd`
  - historical design/provenance evidence
- `rawlsing_chatlog_DDM_chatgpt_1.txt`
  - SHA-256 `b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a`
  - historical conversation/design evidence only

The control documents record the high-value tables, internal pack paths, and already-established findings so workers can decide whether they actually need the original attachment before requesting/materializing it.

A hash match establishes file identity. It does **not** elevate historical material to current semantic authority.
