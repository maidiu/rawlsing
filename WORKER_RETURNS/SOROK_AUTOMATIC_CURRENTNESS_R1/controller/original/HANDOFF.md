# Finite local completion automation

Restores the inherited `Popen → process.json → wait → completion.json` supervisor
and pinned R157 kqueue receipt bridge. No periodic polling or background service.
The original files and their recovery identities are under `inherited/` and
`PROVENANCE.json`. No production/scientific authority is conferred.

## Stable installation

```sh
python3 LOCAL_AUTOMATION/install.py /absolute/stable/controller/local-automation
python3 /absolute/stable/controller/local-automation/launch.py --binding /absolute/client.json --job /absolute/job.json
```

Each operator-authored binding requires:

```json
{
  "schema": "LOCAL_COMPLETION_BINDING_V1",
  "recipient_thread": "EXACT_EXISTING_CHAT_UUID",
  "worktree": "/absolute/authorized/worktree",
  "session": "EXACT_EXISTING_WORKER_SESSION_OR_EXPLICIT_LOCAL_TEST",
  "state_root": "/absolute/stable/per-client/state",
  "codex_binary": "/absolute/installed/codex",
  "notify": true,
  "grant": {
    "id": "EXISTING_COMMISSION_OR_EXPLICIT_LOCAL_GRANT",
    "scope": "EXACT_AUTHORIZED_OPERATION",
    "expires_utc": "OPERATOR_CHOSEN_TIME_WITH_TIMEZONE",
    "job_ids": ["UNIQUE_JOB_ID"],
    "argv_sha256": "SHA256_OF_CANONICAL_ARGV_JSON"
  }
}
```

Job JSON: `job_id`, `session`, `grant_id`, and exact `argv` array (absolute
executable, no shell). Hash argv with the shipped `launch.command_digest`.
Worktree and session must match the binding; provider/model/effort remain the
operator's exact granted command. A binding is local launch authorization, not a
signed scientific grant. Existing workload/source permission remains separate.
No credentials are copied or read; children inherit the existing environment.

The unique run directory is an exclusive launch reservation. Existing job IDs
refuse a second launch, including after a crash. Never delete a reservation to
retry. Inspect/reconcile an uncertain launch rather than relaunch it. Each run
contains logs, exact job/binding, process/terminal receipts and notification
reservation/outcome. Exit zero is process completion, not acceptance of the work.
Observer launch itself is not health proof; inspect its ready/finished/error log.
After a supervisor crash, do not infer that a child exited or create success.

Notification uses one supported ordinary `codex queue` attempt with no model or
effort override. A nonzero exit, timeout or unrecognized acknowledgement is
`AMBIGUOUS_HOLD`; no automatic retry. Queue acknowledgement is not proof of an HQ
reply or adoption. A finite observer exits once its targets are terminal.

## SOROK handoff

The same files can serve existing Sorok chats with separate operator bindings,
state directories, exact recipient UUIDs/worktrees/sessions and current grants.
Do not reuse PYAT's recipient, reservations or grants. No Sorok activation is
claimed. Obtain the intended Sorok chat links and competent current job bindings
before activating; titles alone are not authority. On another machine verify
its installed CLI, paths, account and permissions, then run the harmless local
qualification and one authorized notification. Sharing this packet is not proof
of recipient activation. Do not manipulate desktop windows, pets, mouse or drag
controls; CLI delivery does not guarantee absence of unrelated app crashes.
