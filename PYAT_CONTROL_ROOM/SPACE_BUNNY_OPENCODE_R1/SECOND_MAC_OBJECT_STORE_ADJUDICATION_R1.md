# SECOND MAC OBJECT-STORE ADJUDICATION — R1

Decision:
`AUTHORIZE_EXISTING_SHARED_BLOBLESS_STORE__DO_NOT_TOUCH_UNGOVERNED_RAWLSING_DIRECTORY`

Context:
- `$HOME/Desktop/Rawlsing` exists on the second Mac but is NOT a Git repository.
- It is an ungoverned large payload and MUST NOT be initialized, overwritten, absorbed into a worktree, moved, or deleted under this adjudication.
- A valid shared Rawlsing Git object store already exists at:
  `$HOME/Desktop/as2b-lits1-DiSDJn/repository`
- That repository has origin `maidiu/rawlsing`, is non-shallow, partial/blobless, and already backs multiple unrelated historical worktrees.

HQ authorizes that existing repository as the canonical object store for the HQ203 H-D and H-E workers only.

Canonical object store:
`$HOME/Desktop/as2b-lits1-DiSDJn/repository`

New worker worktree root:
`$HOME/Desktop/Rawlsing_Worktrees`

Required worker branches:
- `agent/rabochii-pyat-hq203-hd-r1 @ de129fea321981a8b47c3239f3858a0b6a535e46`
- `agent/rabochii-pyat-hq203-he-r1 @ 95c4eba0b556b397e1decb5fad07ea2ce7158bd8`

Required evidence/control refs:
- `codex/prev3-terminal-backward-audit-r1 @ b3ea471a3771113bf408a4e434a4b480b26d5856`
- `integration/pre-main-reconciliation-r1 @ 127c46658bf97fff809995b890cc8ad31db79c87`

Law:
1. Do not use or mutate `$HOME/Desktop/Rawlsing`.
2. Do not fresh-clone while the authorized shared store passes identity checks.
3. Fetch only the named refs needed for these two workers.
4. Existing unrelated linked worktrees must not be reset/rebased/removed.
5. New H-D/H-E worktrees must be sparse and isolated.
6. Prepare the two new worktrees serially; after preparation the workers may run concurrently.
7. Historical evidence outside sparse manifests is read through exact Git objects.
8. A missing blob in the partial clone may be lazily fetched by Git; do not broaden to a full checkout.
9. No gc/repack/prune/branch deletion/force push.
10. If the authorized shared store fails origin/integrity checks, STOP. Fallback blobless store creation at `$HOME/Desktop/Rawlsing_git` is authorized only after recording the failed check; it must be one shared no-checkout partial clone, never one clone per worker.

This adjudication supersedes the earlier second-Mac bootstrap requirement that the canonical object store live at `$HOME/Desktop/Rawlsing`.
