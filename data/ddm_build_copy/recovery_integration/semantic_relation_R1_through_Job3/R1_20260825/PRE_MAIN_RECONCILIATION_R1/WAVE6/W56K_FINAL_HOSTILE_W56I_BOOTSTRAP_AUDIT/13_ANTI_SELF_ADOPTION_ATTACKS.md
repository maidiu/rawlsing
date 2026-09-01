# Anti-self-adoption attacks

## G14 — FAIL

Expected defenses hold against direct self-claims:
- candidate receipt says `LOCAL_COMPLETE_UNRECONCILED` and does not authorize PRE-MAIN/global adoption;
- external authorization is outside candidate lineage;
- bootstrap audit has no integration authority;
- written protocol reserves ref movement to external VOZHD/HQ;
- candidate schema/manifest has no formal self-adoption role.

But an executable-substitution attack remains:

1. expose an attacker-controlled executable named `git` earlier on process PATH than the intended host Git;
2. invoke the exact predecessor script under the required `python3 -I -S` flags;
3. Python isolation succeeds, but `subprocess.run(["git", ...])` resolves the hostile executable;
4. the shim can fabricate repository root, live ref, canonical blobs, manifest/schema contents, ancestry, changed paths, authorization ancestry, audit branch tip and hash-object results;
5. the script has no independent provenance barrier for the executable supplying those facts.

W56K directly confirmed step 3 with all five isolation flags true and `MALICIOUS_GIT_EXECUTED` returned by the shim.

A fully weaponized shim would require implementing the finite Git argv surface used by the validator, but nothing in candidate code prevents that substitution. Under a hostile audit, the route therefore cannot be assumed closed.

`G14 = FAIL_EXECUTABLE_SUBSTITUTION_ROUTE_TO_FALSE_CANONICAL_FACTS`.