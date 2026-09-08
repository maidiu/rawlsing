# VOZHD ADOPTION — CERTIFIED WORKER RETURN / RETURN BEACON PROTOCOL R1

Disposition:

`ADOPTED__RABOCHII_CERTIFIED_RETURN_PROTOCOL_R1__CURRENT_WORKER_ORCHESTRATION_LAW`

Parent orchestration law:

`ADOPTED__RABOCHII_EXECUTION_CONSTITUTION_R1__CURRENT_WORKER_ORCHESTRATION_LAW`

This amendment extends worker orchestration/closure discipline only. It does **not** alter Rawlsing empirical, semantic, authority, PRE-V3, V3, V2, campaign, adoption, comparator, occurrence, OEE, or project-current object law.

## Installed operational substrate

Repository-wide Return Beacon installed on default branch `main` at immutable commit:

`f24d1207d64458dbbe1d145d958ab27cd9747e25`

Installed tree:

`04f8606339a813462a4ae0e140f2a255350ee60e`

Installation PR:

`#305`

Independent installation self-test:

- workflow: `Rawlsing Worker Return Beacon`
- run: `34259418220`
- exact tested head: `312021638d785763fad8cfcaa9f5c17463f7a7e5`
- result: `SUCCESS`

Notification inbox:

`#304 — Rawlsing Worker Return Inbox`

Canonical installed contract:

`.rabochii/RETURN_BEACON_CONTRACT.md`

Canonical schema:

`RABOCHII_RETURN_MANIFEST@1.0.0`

Canonical final manifest path:

`.rabochii/return_manifest.json`

## Standing law for all newly commissioned repository workers

For every newly commissioned ChatGPT/Rabochii worker whose work is to be performed durably in `maidiu/rawlsing`, the commissioning authority MUST require the final worker return to satisfy the certified-return contract unless an explicit higher authority states that the turn is intentionally non-durable/non-repository work.

A worker turn is **not** operationally complete merely because the ChatGPT UI stops thinking, emits prose, or appears idle. The authoritative completion event is a certifiable durable repository return.

The worker's final branch-tip commit MUST write or update, together in that exact commit:

1. the durable human-readable return packet; and
2. `.rabochii/return_manifest.json` conforming to `RABOCHII_RETURN_MANIFEST@1.0.0`.

The final manifest MUST identify and bind:

- exact worker branch;
- exact commissioning authority ref;
- exact worker starting SHA;
- exact task/commission identity;
- final result as one of `PASS`, `FAIL`, or `BLOCKED`;
- exact `...__RETURN_TO_...` terminal;
- `CLOSURE_ONLY` phase;
- every required output and its durable Git path/blob SHA or commit SHA;
- the durable human-readable return packet and its Git blob SHA;
- whether governed evidence is required and, when required, exact workflow/run/evidence-execution identities;
- separation of duties for the commissioned role.

Before setting the completion manifest, the worker MUST truthfully establish all of the following:

`commission_consumed = true`

`all_required_outputs_durable = true`

`no_required_work_remaining = true`

`no_background_work_remaining = true`

`return_packet_durable = true`

`terminal_state_entered = true`

`performed_only_commissioned_role = true`

`no_uncommissioned_repair = true`

`no_uncommissioned_review = true`

If any commissioned work, required evidence, required output, repository freeze, return packet, or required follow-up by that same worker remains unfinished, the worker MUST NOT emit a certifiable manifest and MUST NOT claim a certified return.

`INCOMPLETE` is never a certified return state.

`PASS`, `FAIL`, and `BLOCKED` may each be certified **complete** outcomes when that result is the lawful terminal result of the exact commission. Completion is distinct from semantic success.

## Independent repository certification

The Return Beacon MUST independently cross-check, rather than merely trust worker prose:

- current branch tip;
- manifest/branch identity;
- durable return-packet blob identity;
- all declared required path/blob or commit identities;
- that manifest and return packet were written/updated in the same final branch-tip commit;
- when evidence is required, GitHub Actions run completion, workflow name, conclusion, and exact evidence-execution SHA;
- declared artifact existence/non-expiry when artifact identity is supplied.

If any required check fails, no `Certified worker return` notification is lawful.

## Notification / watch operation

The installed Return Beacon provides:

1. a fast post-court watch triggered by completion of `Rabochii Governed Bounded Court`, waiting for the same worker branch to produce its certifiable final return; and
2. a repository-wide periodic sweep over recent `agent/*` return tips, covering repository workers that do not use the governed court and recovering missed fast-path notifications.

Certified returns are posted to issue `#304` and deduplicated by exact worker branch plus certified branch-tip SHA.

A watcher timeout is explicitly **not** a completion event. The periodic sweep continues to observe the repository.

## Legacy transition

Workers already in flight before this amendment cannot retroactively have been commissioned to write the new manifest. The installed beacon may therefore recognize those already-running workers through its conservative `LEGACY_STRICT` compatibility path only when their durable final return unambiguously contains `CLOSURE_ONLY`, a PASS/FAIL/BLOCKED terminal result, an exact `...__RETURN_TO_...` terminal, separation/no-extra-role evidence, no incomplete declaration, and completed governed evidence where named.

This compatibility is transitional. All newly commissioned repo workers after this adoption MUST use the machine manifest.

## Chat/UI expendability after certification

Once a worker branch has a certified durable return, the associated ChatGPT worker turn/window is no longer required for project continuity. A still-spinning, delayed, disconnected, or otherwise unresponsive ChatGPT UI MUST NOT cause duplicate work, restart the worker, or invalidate the certified repository return.

The consuming SUB-VOZHD/VOZHD may proceed from the certified repository state without waiting for the worker chat to emit final prose.

## Post-return mutation law

After a certified return, that worker is in `CLOSURE_ONLY` and MUST perform no further substantive repository mutation under the completed commission. Any further substantive work requires a new explicit commission or lawful continuation authority.

## Applicability

This amendment is prospective operating law for newly commissioned repository workers across Rawlsing repo campaigns, not only SUB-VOZHD E. It governs completion certification and notification only; it does not transfer proof ownership, semantic jurisdiction, adoption authority, or project-current effect between campaigns.

Terminal:

`ADOPTED__RABOCHII_CERTIFIED_RETURN_PROTOCOL_R1__OPERATIVE_FOR_NEW_REPOSITORY_WORKER_COMMISSIONS`
