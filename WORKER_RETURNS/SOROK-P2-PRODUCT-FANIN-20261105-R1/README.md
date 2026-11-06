# Sorok P2 product fanin

Actual TEST_ONLY throughline over the accepted S45-S47 base plus the exact P2 lifecycle, explicit-interval and later-event returns.

```text
python3 run_fanin_cli.py new --state <path>
python3 run_fanin_cli.py view --state <path> [--text]
python3 run_fanin_cli.py say --state <path> "Can I help?"
python3 run_fanin_cli.py do-help --state <path>
python3 run_fanin_cli.py attend --state <path>
python3 run_fanin_cli.py exit --state <path>
python3 run_fanin_cli.py return --state <path>
python3 run_fanin_cli.py status --state <path>
python3 run_fanin_cli.py lifecycle --state <path>
python3 run_fanin_cli.py interval --state <path> --mode ACTUAL --span 4
python3 run_fanin_cli.py later-event --state <path> [--history-ref <ref>]
python3 run_fanin_cli.py opportunity --state <path> --event-ref <ref>
python3 run_fanin_cli.py verify --state <path>
```

`later-event` and `opportunity` only admit/read and project the opportunity; they do not execute a user `DO_HELP`. Use `do-help` explicitly for that attempt. `OUTSIDE` blocks only user encounter actions `SAY`/`DO_HELP`/`ATTEND`; explicit interval/later-event inputs remain explicit producer/world continuation, never automatic on exit. Local `return` restores `PORTAL` without canonical actor/world mutation.

Read `00_RETURN.md` for exact sources, results, upstream defect note and holds.
