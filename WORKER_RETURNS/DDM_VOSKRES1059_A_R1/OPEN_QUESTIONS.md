# Open questions and evidence holds — A first pass

## Exact missing source (NOT_INSPECTED, not NOT_FOUND)

| Pin | Intended object | Status |
|---|---|---|
| `098ea6bea0ef37177fecb185a5c97dd8824216ba` | ZAK-02S R10 V550 missing distributions and metric semantics | commit object absent locally (`git cat-file` fatal) |
| `21bbe210a068001e99785ac954618a14be93b1bc` | ZAK-03S consolidated R3 return / T0006–0011 | commit object absent locally |
| `69804f88abc8e84cf91ee256aa66fb607a49f5a7` | ZAK-04S historical R7 temporal reader | commit object absent locally |
| `89768120d391c385ec81f15f3f035281c7361cb4` | ZAK-04S corrected documentary descendant | commit object absent locally |

`14b232b76eedffa005db4456eaacfc1ed0b4a7a4` (#1058 controller cut) exists and was used only as intake orientation. Its embedded ZAK findings were not treated as independently verified here.

## Unresolved factual questions

1. **Actual old reuse frequency.** No historical shard logs, manifests or output row counts were inspected. Did the country prefetch cache actually hit for most questions, or did alias/empty mismatches trigger frequent per-question SQL? `HISTORICAL_RUNTIME_UNKNOWN`.
2. **V550 on-disk shared cache usage.** `ddm_v550_shared_cache.py` is imported by V550J country-slice code but not by the V550 shard's in-memory question cache. Were there other historical callers, and did any use it for question responses? Not established.
3. **Exact cardinalities.** Number of questions, countries, respondents, selected aliases, cloud emission rate and V550J family counts are not in the inspected source. All cost formulas remain symbolic.
4. **Bridge noninjectivity.** The reduced payload (`ddm_v550_bridge.py:804-860`) omits secondary/branch-specific fields. Does any actual producer table produce two rows that collapse to one `empirical_object_id`? Requires historical bridge/table data, not read.
5. **V551/V552 signed and certified semantics.** Actual V551 atom adjudication, V552 pressure and V551J certified-vector behavior were only located as consumers; no historical output was read. Modern equivalence is `COMPARE_UNKNOWN`.
6. **Modern grouped-core economics.** `I03GroupedExecutionScope` exists and is tested in its own unit tests, but no production/batch first-consumer witness or matched 100/1000-query measurement was inspected. Its effect on FORGE S1–S5 cost is unmeasured.
7. **Cold estate qualification.** Is the grouped-cache ban for `DirectEstateI03Session` (`pre553_empirical_query.py:756-757`) a temporary qualification gap or a semantic necessity? Unknown; needs owner answer, not inference.
8. **Old checkpoint correctness.** Resume trusts parquet existence without content identity (`repository_v550.py:972-1000`). Whether historical resumes ever mixed stale/foreign checkpoints is unknown.
9. **Weight semantics in old entropy.** `distribution_entropy` accepts weights, but `branch_nodes_rows` and some secondary paths do not pass them consistently (`branching.py:380,412`). Whether that was intentional is unknown; source shows inconsistency.
10. **Pooled vs country use.** Which downstream consumers actually used `country_answer_distribution` rather than the pooled table? Bridge maps both to `direct_relation_response`; first actual consumer not witnessed.

## Bounded follow-ups for a later round (do not start now)

- If HQ supplies frozen opponent evidence, reconcile only concrete discrepancies: old-vs-modern reuse boundary, MI population defect, bridge identity, and grouped-core cold-estate status.
- If any historical run metadata becomes available, fill `COST_CARDINALITY.tsv` measured columns; do not invent relative speed.
- If governed bridge outputs become lawfully available, run a documentary hash-collision count; otherwise keep the identity issue `RELATED_UNPROVED`.
