# Hypothetical post-installation replay

## G10 — BLOCKED / FAIL

An exact isolated local ref replay with `LIVE_CANONICAL_SHA=6e50b535...` could not be constructed in the audit execution environment without a local repository object database; network clone was unavailable. The command explicitly permits strongest static + Git-object proof with the runtime limitation stated.

Strong Git-object evidence:
- candidate predecessor-validator blob: `84f833b9...`;
- candidate protected-manifest blob: `da701532...`;
- candidate authorization-schema blob: `10221289...`;
- candidate result-schema blob: `23a0abbc...`.

The repository's already-moved current commit `b53f8843...` contains those four exact same blob SHAs, plus the same enforcement-change protocol blob `88def2ad...`. Thus the files W56J found absent from pre-bootstrap `8b13...` are in fact installed together unchanged after the candidate entered canonical ancestry.

If the canonical ref were exactly `6e50b535...` and the genuine host Git executable were trusted, static code shows:
- executing-copy blob equality would be satisfiable;
- manifest/schema canonical reads would resolve from that commit;
- the manifest declares all four core predecessor dependencies;
- candidate worktree mutations do not provide fallback schemas/manifests.

But the replay cannot certify the required *trusted* dependency closure because the exact candidate script obtains every one of those facts through unpinned PATH-resolved `git`. The hostile executable-resolution replay demonstrated that `-I -S` does not close this path.

`G10 = FAIL_POST_INSTALLATION_TRUSTED_EXECUTABLE_CLOSURE_NOT_PROVED`.