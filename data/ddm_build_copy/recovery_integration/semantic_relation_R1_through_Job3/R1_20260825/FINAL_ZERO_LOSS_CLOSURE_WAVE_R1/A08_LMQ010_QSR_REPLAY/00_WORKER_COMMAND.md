# A08 — LMQ-010 COMPLETE QSR LOWER-LEVEL PRODUCER DEPENDENCY / REPLAY CLOSURE R1

Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-a08-lmq010-qsr-replay-r1`
Exact pre-command base: `477ca6997087676a844e997a1f12d809908119b3`

Read Authority 41 and Z03 result. You have Library access.

Goal: close `LMQ-010` only.

Starting from the current recovered 18,792-row QSR carrier whose manual-core succession was closed by Z03, recover the complete lower-level primary-source/audit producer dependency set needed to deterministically regenerate and verify every QSR row. Preserve source hashes, row identity, manual-review provenance, semantic rule/version, typed unresolved states, and dependency lineage.

Perform destructive replay where possible: rebuild the QSR projection from canonical owners rather than accepting the existing carrier as proof. Compare row-for-row/content-hash parity with the current recovered carrier. A carrier checksum alone is insufficient.

If some producer dependency is unavailable, return exact affected row count/IDs and missing resource refs. Do not adjudicate LMQ-011 again and do not infer routing authority. Remain sibling-blind. Return to HQ.