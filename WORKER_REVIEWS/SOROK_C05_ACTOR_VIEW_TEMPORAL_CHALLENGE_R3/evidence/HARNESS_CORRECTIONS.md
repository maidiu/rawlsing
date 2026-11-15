# C05 R3 harness corrections (disclosed, oracle preserved)

The product was not patched. The final probe oracles and source under test were
not weakened. These are independent test-harness corrections.

1. **Challenge 1 initial independent-start fixture produced different P2
   admission receipts.** Three separately started P2 worlds with the same seed,
   actors, event clock and participants still produced different BP4 event IDs /
   `admission_id` / `contract_hash` values. The event document itself is not the
   same relevant input under that construction. I discarded that comparison and
   used one real P2 event/state, read before and after controlled C12 relation
   writes. That gives the same event ID/hash/clock for A, B and C and isolates the
   relation write. The first run's logs were replaced; no product state was
   changed.

2. **Copying a P2 state root was refused.** An attempt to copy the fixture state
   to independent paths failed closed with `SESSION_ROOT_MOVED` from the S37
   session root binding. I did not patch or bypass that binding; the final
   fixture uses one state root and sequential relation writes.

3. **Challenge 3 local KeyError.** The first challenge-3 run used
   `document["private_state"]` instead of `document["context"]["private_state"]`;
   the harness stopped with `KeyError`. The check was corrected to the actual
   reader field, rerun, and all assertions passed. No product code or oracle was
   changed.

4. **No full unrelated campaign.** The accepted mechanical custody/promotion
   results from review `c0cbe82f` and the R2 suite were not reopened or rerun as
   a broad campaign. This court is limited to the three hostile actor-view
   challenges and cold/sever controls.
