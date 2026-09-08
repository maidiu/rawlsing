# Rawlsing / Rabochii Return Beacon Contract R1

Status: repository-operational infrastructure. This contract does **not** alter Rawlsing empirical, semantic, authority, PRE-V3, V3, V2, campaign, adoption, or project-current law.

## Purpose

A ChatGPT/Rabochii turn is not considered operationally complete merely because its UI stops thinking or because a worker says "done" in chat. Completion is certified from durable repository state.

For newly commissioned repository workers, the final worker commit MUST write or update both:

1. the worker's durable human-readable return packet; and
2. `.rabochii/return_manifest.json` conforming to `RABOCHII_RETURN_MANIFEST@1.0.0`.

The manifest and return packet MUST be changed in the same final branch-tip commit. The branch tip containing them is the certified return identity; the manifest does not attempt to contain its own commit SHA.

## Completion versus success

`PASS`, `FAIL`, and `BLOCKED` can all be **complete turn outcomes** when they are the lawful result of the commissioned work. `INCOMPLETE` is never a certified return.

A manifest is certifiable only when it states and the beacon verifies that:

- the exact commission authority and exact starting SHA are identified;
- the exact branch matches the branch being inspected;
- every required output is durably present as a Git path/blob or resolvable commit;
- the return packet itself is durably present with the declared Git blob SHA;
- no commissioned work remains;
- no background work remains;
- the worker has entered `CLOSURE_ONLY`;
- the exact return terminal has `...__RETURN_TO_...` form;
- the worker performed only the commissioned role and did not add an uncommissioned repair or review;
- when governed evidence is required, the declared Actions run is completed and its workflow name, conclusion, and evidence execution SHA independently match GitHub; and
- when an artifact ID is declared, the artifact exists and is not expired.

If any of those checks fails, the beacon MUST NOT emit a certified-completion notification.

## Required final-commit discipline

For all newly commissioned `agent/*` repository work:

- final commit message SHOULD begin with or clearly contain `Return`;
- final return packet and `.rabochii/return_manifest.json` MUST be written together;
- a worker MUST NOT write the manifest while required work is still pending;
- a worker MUST NOT use the manifest to promise future/background work;
- a worker MUST NOT treat a green CI run alone as turn completion;
- after the certified return commit, the worker enters `CLOSURE_ONLY` and makes no further substantive mutation unless separately recommissioned.

## Notification paths

The central workflow `.github/workflows/rabochii-return-beacon.yml` provides two paths:

1. **Fast governed-return watch:** completion of `Rabochii Governed Bounded Court` starts a bounded watcher for that exact worker branch. It waits for a certified durable return instead of relying on the ChatGPT UI.
2. **Repository sweep:** every five minutes, and on manual dispatch, the beacon checks recent `agent/*` branch tips whose commit headline is a return. This covers repo work that does not use the governed court and recovers notifications missed by the fast path.

Both paths deduplicate by exact `branch + certified tip SHA` and post to issue `#304` (`Rawlsing Worker Return Inbox`).

## Legacy compatibility

Workers already in flight before R1 cannot retroactively contain the machine manifest. For those branches only, the beacon has a conservative `LEGACY_STRICT` compatibility path. It recognizes a return only when the final return markdown simultaneously contains:

- `CLOSURE_ONLY`;
- no `INCOMPLETE` / `NOT COMPLETE` declaration;
- an exact `...__RETURN_TO_...` terminal;
- a PASS/FAIL/BLOCKED outcome;
- separation/no-extra-review-or-repair language; and
- if a governed run is named, a GitHub-completed run with success/failure conclusion.

Legacy recognition is transitional. New commissions MUST use the manifest contract.

## Notification meaning

A `✅ Certified worker return` comment on issue `#304` means:

> the repository contains a durable terminal return for that commissioned turn, the completion contract has passed, and no required/background work remains.

It does **not** mean the semantic result is necessarily PASS. The notification explicitly reports PASS, FAIL, or BLOCKED.
