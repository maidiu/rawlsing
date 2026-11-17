> **HISTORICAL / SUPERSEDED_BY_FINAL.** Authoritative final state: `S2_S3/FINAL_ARCHITECTURE.md`, `S2_S3/FINAL_DECISION.json`, `S2_S3/SPECIALIST_ADJUDICATION.md`, `S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv`, `RETURN.md`. This file is preserved as prior evidence only; its PENDING/provisional/SC-ESTATE statements are not live.

# RESOURCE MODEL — analytic, not a production claim

**Status:** provisional; no native 100k/6 GiB/1-10-100 measurement. The only
numbers below marked “measured” are the sourcefree #1097 witness and the local
sourcefree test runtimes.

## 1. Measured baseline (sourcefree, cut-specific)

| Quantity | Value |
|---|---:|
| writer wall | 3033.723 s |
| retained estate | 310.16 MB |
| staging peak | 5.26 GB |
| temporary writer I02 | ~4.39 GB |
| native session index | 1.30 GB |
| one selected query | 562.362 s |
| prepared-session factor (author report) | 1.69–1.70× |

This is **not** native 100k and **not** a 6 GiB proof. It is a bottleneck
witness: the route performs avoidable duplicate work.

## 2. Cost decomposition

Let `O` = object count, `E` = event count, `R` = respondent count, `B` =
retained estate bytes, `X` = bytes/rows selected by a query, `Q` = distinct
operations, `M` = manifest bytes, `I` = index bytes.

### Current route

| Work | Approx. cost | Notes |
|---|---|---|
| Q2 decode/project | O(source) | once |
| I02 #1 | f(O) ≈ O log O + O | SQLite sort/index/root |
| 13 JSONL journals | O bodies | write + fsync |
| replay JSONL | O parses | second serialization |
| I02 #2 | f(O) | duplicate |
| Parquet write | O serialize + compression | canonical |
| full physical verify | O parse + O `_row` encode | duplicate |
| cold manifest hash | B | every open |
| session index | O SQLite inserts + indexes | every fresh session |
| query | O scan + native R | per operation |
| evidence output | per operation | often full fact/replay |

### SC-ESTATE

| Work | Approx. cost | Notes |
|---|---|---|
| Q2 decode/project | O(source) | once |
| C11 write | O serialize + compression | one pass |
| one I02 root | f(O) | streaming Merkle / bounded sort |
| per-row-group digest | B | one byte-level readback, no object decode |
| derived index | O log O | once per release, rebuildable |
| cold open | M + I + selected row groups | no O(E) scan |
| narrow query | X + native R_native | selected postings/body |
| full F4 | O(R × support) | science-bound, not storage |
| evidence | O(result) + shared refs | deduplicated fragments |

**Predicted direction:** large reduction in writer and staging because the
second I02, JSONL journal/replay and per-row re-encode are removed; cold open
drops from O(E) to O(M+I+selected); retained grows only by the compact index;
query cost is dominated by native risk enumeration for full-domain work, which
is inherent and must be measured.

**No numerical SLA is claimed.** The next lawful measurement must report writer,
retained, peak staging, process-tree RSS, source reads, I02 builds, object
reconstructions, cold open, 1/10/100 distinct operations, and evidence output.

## 3. 1/10/100 model

| Operation pattern | Current | SC-ESTATE |
|---|---|---|
| 1 cold query | full manifest hash + full session index + query | manifest/index root + selected row groups + query |
| 10 repeated distinct in one process | one session index, amortized; prepared P0 1.69–1.70× | one open, one index verify, shared risk/denominator |
| 10 fresh processes | 10 full session indexes | 10 cheap opens; no full scan |
| 100 distinct | index rebuild/scan dominates | index reused; native risk enumeration dominates |
| heavy F4 | true joint computed by native evaluator | same native evaluator; storage not the bottleneck |

The durable index changes the **cold/fresh-process** cost, not the scientific
cost of full-domain F4. If native enumeration dominates at 100k, a columnar
accelerator is a separate bounded decision with an exact native-equivalence
test; it is not assumed here.

## 4. Retained / scratch / RSS

- **Retained:** canonical 13-family Parquet + locator + manifest + compact
  index + small proof root. No second body corpus, no JSONL residual, no SQLite
  session corpus.
- **Scratch:** stage + largest external-sort run + digest; deleted after commit.
  The current 5.26 GB staging is not a target; it is evidence of duplicate
  I02/JSONL work.
- **RSS:** index is memory-mapped/read-only; selected row groups are bounded;
  no whole-corpus Python object graph. The 6 GiB process-tree ceiling remains a
  measurement obligation, not a declaration.

## 5. Recovery / revocation cost

| Event | Behavior | Cost |
|---|---|---|
| crash before manifest | stage orphan, no valid release | cleanup only |
| crash after members before manifest | reader refuses incomplete | rebuild |
| changed member/row group | digest mismatch, typed refusal | no valid query |
| changed locator/index | index root/body-ref mismatch, refusal | rebuild index |
| changed release/source/current | current guard refuses | exact restore |
| revocation after preparation | refuses even with index/session | exact restore |
| exact restore | same manifest/I02/source → same facts | O(verify) |

## 6. What the specialist returns must supply

1. Construction specialist: exact writer/retained/scratch/RSS and attack/restore
   matrix; whether the single-certification proof is equivalent.
2. Query specialist: exact cold/1/10/100/native-enumeration/evidence-output
   matrix; whether the index is non-authoritative and rebuildable.
3. Any material new requirement → S1 version before final decision.
