# WG0RI — exact provenance and custody chain

## The chain, independently bound

1. **Original Git publication.** Commit
   `b44596d880425f6984f208bfa14daee2f15d3f90` contains
   `CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv` with Git blob
   `c93945d158198871f5cc6692a6bed25aeef44028` (24,972 bytes, SHA-256
   `c1d5a9a9b2905f7ed783a21f43eeef91bc173d6e5e077751a67f7025408ee7ad`). Its
   header *claims* the frozen 18,276-byte target `64a43ba2…`, but the declared
   base64 decodes to **18,387 bytes / `3bee6f0e…`** with **2,114 reserved-bit
   violations**. This is the preserved historical RED, not a repair.
2. **Surviving 1,000-row shard.** The original Git commit also contains
   `CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER_SHARDS/part-000.csv`, exact Git
   blob `3a9b5bde2fc479c6fc10280561fe715686e39dd4` (11,944 bytes, SHA-256
   `e9fff20e…`), 1,000 rows with ordinals 0–999. Every row decodes to the
   corresponding recovered payload byte: **1,000/1,000, zero mismatches**.
3. **Retained row-specific authority projections.** S00 workstreams
   (`d0fc960f…`), central O06 routing (`91379e9a…`), O07 diagnostic recall
   (`4b9b4a54…`), O08/O09 conditioner authority (`2daebfe1…`) and O04 worker
   states (`8da69f98…`) are retained with their custody JSON, archive/member
   origins, source hashes and row counts. The exact P2 identity master is
   `d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6`.
4. **Recovered exact payload.** 18,276 bytes, SHA-256
   `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98`, zero
   reserved bits, all use codes 0–9: SEM 4,681 / TOP 3,667 / POS 2,904 /
   END 2,113 / CTX 1,675 / SCX 1,506 / ADM 1,026 / REJ 454 / CPC 183 / BLK 67;
   10,418 hard-fail and 4,447 route-predicate flags.
5. **Repaired disposition ledger and reader.** The active path
   `sources/recovered_disposition/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv`
   holds one `P2_ORDINAL_BYTEPACK_V1` row with the exact P2 hash, 18,276 rows,
   format, code map, byte layout, declared length and payload hash. The reader
   checks cardinality, P2 binding, payload length/hash, header, code map and
   packed-byte legality; the accounting output is 18,276 unique implementations /
   35 waves / 9 families, with no carrier-requires rows and the 76 P10/G1A holds
   preserved within 65,354 accounting units.
6. **Original artifact preserved.** The malformed Git preimage is unchanged and
   still fails the repaired reader closed; the repaired carrier is a separate
   versioned path. The historical bytes were not overwritten in place.

## O07 recall projection boundary

O07 is a two-column diagnostic projection. It never selects a use code; the
recovery code selects use from S00 workstreams and the central O04/S2B ruling.
Independently measured:

- a non-`UNRESOLVED` O07 value change (`ADMIN → SEM`) leaves the recovered
  payload **exactly** at `64a43ba2…` — O07 has no use/disposition-code authority;
- of 30 `UNRESOLVED` rows, changing the diagnostic to `ADMIN` changes the
  payload for **9** rows (the held bit was solely O07) and leaves it exact for
  **21** (held already true for another retained reason); every changed payload
  is **rejected by the frozen payload SHA**, and no different payload is accepted;
- therefore O07 may contribute a diagnostic held status for 9 rows, but cannot
  issue a new disposition meaning or bypass the frozen-SHA acceptance gate.

The S2B special handling is backed by retained central O04 ancestry and the
explicit feelevel ruling in `R10F_O03_O04_CENTRAL_INTEGRATION_REPORT.md` (the
central block count and earlier-wave feelevel instances). The 2,113 accepted O04
endpoints equal the recovered END count (2,113), and the class counts match the
frozen payload; no new semantic decision is introduced beyond the retained
central ruling.

## Manifest discrepancy (REVISE, not a payload failure)

The retained 19-shard manifest covers 18,276 rows and its first/last IDs match
P2 ordinals 0/999, but its part-000 SHA-256 is `e2f5f13ade61…`, which is **not**
the surviving Git shard `e9fff20e…`. The survivor is byte-exact to the original
Git blob and row-correct; the manifest therefore describes a different
serialization/full-shard set and must not be presented as the survivor's byte
manifest or used as a substitute for it. This is a provenance-disclosure
revision, not a recovered-payload mismatch.

## Limits

- The external source archives (S00/O06/O07/O08/O04 origins) are not in this
  return; the retained projections and their custody hashes/row counts are
  verified, but the archive member bytes were not re-extracted here.
- Only the surviving part-000 shard is Git-present; the other 18 manifest shards
  are not in the return. The frozen payload SHA, the 1,000-row survivor, the P2
  master and the retained projections are the acceptance basis.
- The 9 O07-solely-held rows are a diagnostic held-status dependency, not a
  use-code issuance.

## Authority boundary

This repair is exact byte/ledger custody. It is not a source/operation
permission, original U/E_pre, issuer, actor/model or Field Forge grant. WG0I's
P2/O35E crosswalk (18,276 vs 18,259; 26 P2-only hashes; 9 O35E blocked-identity
rows; 17 net delta; 19 measurement candidates), the 76 P10/G1A holds and the
full original35 item/operation frontier **HOLD** remain in force.
