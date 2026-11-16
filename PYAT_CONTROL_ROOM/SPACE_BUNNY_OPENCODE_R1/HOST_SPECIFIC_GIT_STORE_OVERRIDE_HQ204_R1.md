# HQ204 — host-specific Git store override — R1

Status:
`ADOPTED__STORE_PATH_IS_HOST_SPECIFIC__DO_NOT_PORT_SECOND_MAC_PATH_LITERALLY`

The earlier second-Mac storage law was host-specific.

It described a host on which:
- `$HOME/Desktop/Rawlsing` existed as a large NON-GIT payload; and
- the lawful shared Git object store was `$HOME/Desktop/as2b-lits1-DiSDJn/repository`.

That law MUST NOT be transplanted literally to a different Mac.

## General host rule

For any HQ204 local worker:

1. Use the existing local `maidiu/rawlsing` Git repository on THAT host when one already exists and passes identity checks.
2. Do not create a duplicate clone merely to satisfy a path literal from another host.
3. A path described as forbidden because it was NON-GIT on one host is not globally forbidden if, on the current host, it is the legitimate Rawlsing Git repository.
4. Verify before use:
   - it is a Git repository;
   - origin resolves to `maidiu/rawlsing`;
   - the commissioned remote branch resolves to the exact governed startup SHA.
5. Use isolated sparse worktrees for workers.
6. Fetch only exact governed refs needed by the commission.
7. Do not reset/rebase/merge existing governed branches or mutate unrelated worktrees.
8. Do not create another clone while a valid local shared object store exists.

## HQ204 V556 application

For `agent/rabochii-pyat-hq204-v556-r1` on the host where:

`$HOME/Desktop/Rawlsing`

is a valid Git repository for `maidiu/rawlsing`,

HQ explicitly AUTHORIZES that path as the canonical local object store for this tranche.

The prior SECOND-MAC instruction naming:

`$HOME/Desktop/as2b-lits1-DiSDJn/repository`

does not apply on this host.

The worker must still use an isolated sparse worktree under:

`$HOME/Desktop/Rawlsing_Worktrees`

and preserve all other HQ204 commission law.

No new clone is authorized or needed.
