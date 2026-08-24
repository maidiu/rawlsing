# Root commit proof

## Proven root

Canonical root candidate: `a819fb35337ea28c4a83352d0040030b3da83a7a`  
Commit message: `Publish curated V550+ pipeline source`  
Observed commit date: `2026-08-13T01:08:20-04:00`

The commit's README states that the repository is a **curated source transfer of the existing
V550 through V552J implementation**. It says the transfer includes runtime Python, authority
registries, manifests, CSV crosswalks, validation code, and tests, while intentionally excluding
generated outputs, logs, respondent-level data, database files, archives, caches, virtual
environments, and environment files.

The connected-history session established this commit as the parentless initial commit on the
canonical repository lineage. Because it has no first parent, the required "parent contains no
`data/ddm_build_copy/` path" proof is vacuous. Codex should reproduce this mechanically before seal:

```bash
git rev-list --parents -n 1 a819fb35337ea28c4a83352d0040030b3da83a7a
git ls-tree -r --long a819fb35337ea28c4a83352d0040030b3da83a7a -- data/ddm_build_copy
```

Expected first command: the output contains only `a819fb35337ea28c4a83352d0040030b3da83a7a` and no parent SHA.

## Root tree presence

The exact `data/ddm_build_copy` subtree tree SHA observed through GitHub was:

`6433cc97488196525d360a36841e2aee3bb7253b`

The recursive tree response reported `truncated: false` and contained scripts, bindings, manifests,
and V550→V558/V5 source surfaces already present in the source-transfer snapshot.

This packet's `ROOT_SNAPSHOT_MANIFEST.csv` records the exact high-value objects actually extracted
from that tree response during the connected session. It is **not asserted exhaustive** because the
connector response could not be piped directly into the container. Codex must replace/extend it
from `git ls-tree -r --long` before HIST01 closure.

## Worker branch start proof

Requested branch: `agent/vozhd-trii-hist01-original-ddm-authority-trace`  
Requested exact start: `299ef47a17fc96ea31589ea9e3c846e715e96d5d`

Connected GitHub `compare_commits(base=299ef47a17fc96ea31589ea9e3c846e715e96d5d, head=agent/vozhd-trii-hist01-original-ddm-authority-trace)` returned:

- status: `identical`
- ahead_by: `0`
- behind_by: `0`
- total_commits: `0`

Thus the worker branch was exactly at the requested start when this court began.
