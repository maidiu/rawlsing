# CLR3 repair candidate R1

`candidate/recursive_court.py` repairs the two new I2 validation counterexamples. Original source, review, tests and evidence remain frozen in the parent return. Read `00_REPAIR_RETURN.md` for the exact scope and limits.

Using the existing Python 3.11 and parent `.runtime` dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 run_repair.py
```

If needed, install only the original pinned requirements into the parent ignored runtime directory:

```sh
python3 -m pip install --target ../.runtime -r ../reconstructed/clr3/requirements.txt
```

Expected combined exit **1**: 38 original CLR3 + 6 unchanged independent + 11 added repair cases PASS; the original six historical assertions stay RED. Separate suite receipts/JUnit make those outcomes explicit. Full valid trajectories and cold replay must remain unchanged. No model/network/native-actor execution is needed for the court.

This is an authored repair candidate. It does not self-adopt or replace the frozen independent review, nor resolve archive lineage or native owner grants.
