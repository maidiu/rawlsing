# Replay recipe: Job3-R3 court accounting

1. Load O12-R3 frozen candidate universe and existing governed topology.
2. Load six Job3 worker returns as evidence.
3. Load central terminal decision ledger.
4. Verify exactly 1,264 candidate dispositions: 552 ACCEPT, 697 REJECT, 15 BLOCKED.
5. Verify 638 pre-existing positives + 552 new accepts = 1,190 governed-positive topology.
6. Preserve rejected-candidate reasons and blocked obligations; neither may be erased by compacting to the final positive graph.
