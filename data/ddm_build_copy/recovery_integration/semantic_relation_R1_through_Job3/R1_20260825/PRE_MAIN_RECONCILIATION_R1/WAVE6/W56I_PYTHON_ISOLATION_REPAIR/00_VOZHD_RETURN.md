# W56I — PYTHON ISOLATION / SHADOW-IMPORT REPAIR

Launch base: `f0d2b8300a1f9a860a283c37da341e2ef928ee22`
Prior hostile blocker: `8e792a9c6a6b8f8de4e34fd6aed64d0df554787e`

Status: `LOCAL_COMPLETE_UNRECONCILED`

Exact repair scope:

1. `validate_enforcement_candidate_from_canonical.py` now imports only built-in `sys` before an interpreter-isolation barrier.
2. The gate refuses execution unless `isolated`, `ignore_environment`, `no_user_site`, `no_site`, and `safe_path` are all true.
3. Required authoritative invocation is `python3 -I -S ...`.
4. Only after the barrier does the gate import path-resolved stdlib modules.
5. The gate additionally rejects any active `sys.path` entry resolving inside the repository.
6. `GOVERNANCE_ENFORCEMENT_CHANGE_PROTOCOL.md` now makes isolated Python process provenance part of the trusted predecessor dependency closure.

Threat closed at intended repository-governance grain:

- sibling `argparse.py` / `json.py` / `subprocess.py` shadow imports;
- repository-local `sitecustomize.py` / `usercustomize.py`;
- `PYTHONPATH` candidate injection;
- script-directory / current-directory import-path insertion;
- ordinary non-isolated invocation being mistaken for authoritative predecessor execution.

External trust boundary retained:

The host Python executable/runtime is an external machine prerequisite. Host interpreter compromise/replacement is outside repository-governance authority and is not claimed solved here.

No Ground, project-state, obligation, runtime, serving, empirical-carrier, or substantive authority changes were made.

No PRE-MAIN or main movement is authorized by this repair.

Next action: fresh hostile W56J audit of the exact final W56I candidate, focused on Python process isolation and regression only.
