# PROGRAMMA DELTA — P2 interval repair independent closure

- Repair `7a256ed4873155dfad86faf2464110ee6f1e2ad4` / code parent `dde8287a806a802cd8d6a3dc122870f8cf8c5c3a`; historical bdad REVISE preserved; accepted41bf base preserved.
- Verdict: **REVISE**.
- Primary auto-help repair passes: observation creates no user event/encounter/DO_HELP; explicit do-help attempts exactly once; ACTUAL refuses; SCHEDULED accepts; cold/cutrestore focused tests pass.
- Remaining failures: public result still exposes exact keys `<root>.admission` and `<root>.c9`; `evidence/result.json` still lists three missing `__pycache__` entries.
- Narrow repairs: rename/omit admission/c9 public fields; exclude pycache entries and recompute receipt.
- Later event 76 remains separately REVISE; fan-in 579 not reviewed. No native/human/protected acceptance.
