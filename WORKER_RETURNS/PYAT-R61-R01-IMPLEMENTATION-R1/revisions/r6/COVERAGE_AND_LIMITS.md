# R61 R01 R6 coverage and limits

| R61V requirement | Implementation | Evidence | Status |
|---|---|---|---|
| A trust/ownership | private retained campaign records; no public registration | inspect mutation and forged lineage tests | PASS local trust |
| B canonical records | root/issuance/execution/lineage/activation dataclasses | campaign D3 and snapshot tests | PASS |
| C-1 create | `create_campaign` pins policy/root/source/query/native factory | fixture and fresh restore | PASS |
| C-2 issue | retained parent refs, derived generation, pre-execution plan/predecessor counts, caps | campaign D3, H attacks | PASS |
| C-3 execute | retained plan/lineage revalidation, native I05, exact reconciliation | campaign D3, cold N+1 | PASS |
| C-4 activate | derived next generation, actual receipts/lineage, exploratory distinct | campaign D3 | PASS |
| C-5 inspect | deep detached material | mutation test | PASS |
| C-6 snapshot/restore | external checkpoint pin; fresh process; altered pin refusal | restore tests | PASS |
| D counts/no-work/restore | exact issued ops, zero-cap STOPPED_BUDGET, external pin | zero-cap and altered snapshot tests | PASS |
| E reuse/no engine edit | unchanged I05/handoff/predicate owners | imported blobs | PASS |
| F1 positives | D3, root/parent, hidden minority, exploration | committed suite | PASS |
| F2 H1-H7 successor attacks | campaign + strengthened legacy refusals | tests | PASS for campaign owner path |
| F3 deep/view/registration attacks | detached inspect, no registration API | mutation tests | PASS |
| F4 exact sets/budgets/multibatch | cumulative retained counts, explicit unissued | campaign D3/zero cap | PASS at local grain |
| F5 fresh restore | pinned checkpoint, altered rehash refusal | subprocess test | PASS |
| F6 same consumer mutation/restore | legacy I05 anti-join mutation + campaign execute | suite | PASS |
| R03/R04/R09/original science | not implemented/claimed | NOT_REACHED | HOLD |
| Distributed durability/fork protection | not claimed | local host trust only | NOT_REACHED |
| Serialized replay of restored old executions | restore retains metadata but does not re-run old native execution | explicitly limited | NOT_REACHED |
