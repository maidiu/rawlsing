# G5 execution log

Host: oldMac.lan, macOS 13.7.8, Darwin 22.6.0, x86_64, Python 3.11.3.
Candidate: bfe420af96e401342b4d36b942532057a4871575.
Checkout: fresh detached worktree, clean before and after.

## Commands and exits

1. `python3 -B -m unittest -v test_measure test_agent_b test_agent_a_relay`
   - cwd: `WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1`
   - exit 0; 26 tests; 23.653 s.

2. `python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/measure.py --repo <checkout> --out <evidence>/measure2`
   - exit 0; index SHA-256 `e35455ddd634f83de883ad82c44dcd3ba70e0368eaad14f7fc3ff5e584b37995`.

3. `python3 -B WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/read_receipts.py <evidence>/measure2 --index-sha256 e35455ddd634f83de883ad82c44dcd3ba70e0368eaad14f7fc3ff5e584b37995 --repo <checkout> --require-expected`
   - exit 0; `expected_scenario_pass=true`.

4. Copied `measure2` to `tamper-copy2`; control reader on the copy before tamper:
   - exit 0; `expected_scenario_pass=true`.

5. Altered `p3_records` seq 1 from `TEXT` length 178 to `BLOB` length 2 (`X'4142'`), checkpointed WAL, left receipts/index untouched.
   - WAL bytes 0 after checkpoint; index unchanged `e35455…`.

6. Reader on tampered copy with the original external index:
   - exit 2; `REJECT STATE_FINAL_CONTENT_MISMATCH`.

## Observed fresh P6 metrics

- Attempts 5; success 4; expected refusal 1; unexpected failed/refused 0; timed out 0.
- `cold_reopened=1`; distinct child PIDs 5.
- Wall total 40.988526213448495 s.
- CPU user 29.39015 s; CPU system 2.604349 s.
- Max direct-child RSS 55,226,368 bytes.
- Provider calls/tokens/retries/billable cost: UNOBSERVED.
- Process-tree RSS/descendants: UNOBSERVED.
