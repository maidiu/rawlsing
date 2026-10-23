# R61 R01 R7 coverage and limits

| R61AF requirement | Evidence | Status |
|---|---|---|
| Create validates releases/root/query/catalog/native context | create context test; missing release/duplicate/wrong query refusals | PASS |
| Freeze semantic native config, no callable identity claim | `_native_campaign_context`, contract | PASS local host |
| Issue chronology separate from generation; multiple gen1 batches | multibatch test counts 4 then 8 | PASS |
| Every stopped/no-work issuance advances head | zero-cap test and code | PASS |
| Execute revalidates source/root/query/ancestry/receipt/handoff/predecessor | campaign execute + `_projection`; context mutation/refusal test | PASS |
| Completed receipt-backed activation preimage | snapshot after execute before activate restores and activates | PASS |
| No native/budget duplication on retry/activation | monkeypatched native counter | PASS |
| Typed receipt states retained | snapshot preimage states test | PASS |
| Snapshot/restore full closure + external pin | genuine restore PASS; altered/rehashed snapshot fixed-pin refusal | PASS |
| Inspect detaches views; no public registration | mutation test; no registration API | PASS |
| A1-A3 and native positives preserved | 31-test suite | PASS |
| R03/R04/R09/original science | not implemented/claimed | NOT_REACHED |
| Global durability/anti-fork/protected issuer | not claimed; local trusted host only | NOT_REACHED |
| Honest inflight/ambiguous execution | typed HOLD in owner | PASS as typed limitation |
