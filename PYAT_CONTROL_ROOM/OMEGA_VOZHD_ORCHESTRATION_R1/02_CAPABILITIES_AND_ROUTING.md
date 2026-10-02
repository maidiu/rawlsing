# Capability census and execution routing

[Start](README.md) · [Codex handoff](prompts/CODEX_EXECUTOR.md) · [Source notes](15_CAPABILITY_SOURCE_NOTES.md)

## Distinguish capability, access, authority and evidence

The user reports substantial Library access and full GitHub write tools for browser agents. Record that as user-reported availability. Verify the actual methods, repository permissions and execution limits once per worker environment; do not assume this Codex session's tools or filesystem exist there. API model capabilities do not establish a particular ChatGPT agent's enabled tools.

Initialize [capability_profile.template.json](templates/capability_profile.template.json). Each cell is VERIFIED, USER_REPORTED, UNAVAILABLE, or UNKNOWN, with session/surface, observed tool, timestamp, exact proof and limits. UNKNOWN is not false and not permission.

| Capability | Minimal useful check | What the check does not establish |
|---|---|---|
| Exact GitHub reads | Resolve control ref; fetch and hash one required blob at exact commit | Default-branch contents are current authority |
| Branch/file writes | Use the first real assigned commission commit on an isolated branch and refetch it | Force pushes, protected-branch access or workflow changes are allowed |
| Git graph operations | Verify create-tree/commit/ref or clone/push methods and fast-forward behavior | Ability to merge without independent review |
| Code execution | Run the required source-free baseline test in the actual sandbox, capture version/exit/output | A browser tab or successful code upload is an execution environment |
| CI | Identify an existing bounded source-free workflow; bind run, job, attempt and tested commit | Write tools include dispatch permission, secrets or sufficient CI minutes |
| Dependencies | Record Python/platform/package versions and required native-library imports | The model's knowledge cutoff or this Mac's Python version pins the worker runtime |
| Persistence | Save a needed small artifact, refetch it or recover it after a supported process restart | A long-running job survives a chat ending |
| Library | Resolve a named documentary resource/version and retained citation | Complete holdings, local path access or raw-payload authorization |
| Agent orchestration | Verify explicit dispatch/message/status tools and model selection | UI browser access permits scripting ChatGPT itself or unlimited parallel agents |
| Costs/limits | Read available account/runtime telemetry; otherwise mark unknown | User-reported browser usage treatment implies free CI, storage or unlimited throughput |

Do not invent a maximum file size, job duration, memory allowance or concurrency count. Measure the relevant operation, record the discovered ceiling and route around it through supported tools. No security-control bypass, hidden credential extraction or UI workaround for a prohibited tool.

## Preferred route order

1. Browser Sol High plus structured GitHub/Library tools for research, contract work, patch creation, evidence assembly and review.
2. The same browser worker's supported sandbox or an already-authorized bounded CI workflow for source-free tests. Pin the tested commit and runtime. Prefer direct tool/API operations over repetitive UI actions where available.
3. A user-authorized Codex 5.6/6.0 worker for a minimal execution job if the browser lacks required dependency support, reliable filesystem/process control, artifact capacity, or reproduction tools.
4. Astra only when the question is about correctness/authority/architecture and survives ordinary diagnosis; never merely because a shell is needed.

A proven missing runtime capability is enough to route to Codex; do not spend many browser attempts proving the same absence. For transient failures, follow the applicable runner retry law. Where none exists, allow one bounded diagnostic/retry with a changed premise; then use another supported route. A preserved failed governed run with a no-retry rule overrides this default.

## Choosing a Codex fallback

Use an available 5.6 worker as the initial fallback for deterministic patch/test jobs; use an available 6.0 worker where the 5.6 attempt reveals a concrete reasoning/implementation limit or measured time-to-correctness favors it. Do not pretend one is universally cheaper without account evidence. Set a bounded output, exact base/branch, file allowlist, fixture scope, command, artifact path and stop condition. Return the result to browser HQ; do not send the whole project to Codex or Astra.

The user has made Codex available as a fallback while preferring avoidance. HQ may prepare a complete fallback assignment and route it through a supported authorized mechanism. If actual task creation/model selection requires the user, request only that mechanical launch. Do not repeatedly ask whether source-free development is allowed.

## Honest test provenance

`PATCH_PREPARED` is not `TESTED`. `CI_QUEUED` is not `PASS`. A green run at a parent commit is not a green run at the candidate commit. Capture run/job/attempt, head SHA, command and dependency environment, exit status, test totals, skips, log/artifact digests and source-access declaration. A missing exit, inaccessible log or partial run remains unverified.
