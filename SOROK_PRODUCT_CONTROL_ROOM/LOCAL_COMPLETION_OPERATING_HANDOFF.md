# SOROK HQ finite dispatch and completion return

Operational qualification: 2026-11-01 (America/New_York). Existing HQ: `01a161c5-a44a-7b13-ad50-49e10112874d`; permitted worktree `/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing`.

## Installed route

Source `maidiu/rawlsing-controller`, branch `infra/local-completion-restoration-20261101`, exact commit `64d52127b6a24bab5faf2461d75da5141c3baac2`, `LOCAL_AUTOMATION/HANDOFF.md`. All five installed files matched pinned Git bytes at activation.

- Helpers: `/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/`.
- Machine setup and binding template: `/Users/matthewsmith/.config/rawlsing-controller/sorok-01a161c5/{setup.json,binding.example.json}`.
- Actual bindings, commissions and argv: the same config directory's `jobs/`.
- Current operating receipt: the same config directory's `activation-current.json`.
- Persistent per-job state: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/`.

## Launch future authorized commissions

1. Establish actual user-authorized scope, permitted worktree and current provider/model/effort. The helpers confer no account, source, science or product authority.
2. Use a fresh job ID and appropriate current grant. Bind the exact worker session; do not reuse spent qualification sessions or touch unrelated jobs. A new session can be allocated without inference using OpenCode's local session.create API; stop any temporary allocation server afterward. The real qualification used a fresh tools-disabled session and explicit `opencode-go/deepseek-v4.1-flash`, variant `max`.
3. Build the exact absolute-executable argv array, with no shell. Import the installed `launch.command_digest(argv)` and put its result in `grant.argv_sha256`. Complete the exact recipient/worktree/session/state-root, grant ID/scope/expiry/job IDs, and matching job JSON. The example binding alone is not authorization.
4. Invoke once: `python3 /Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/launch.py --binding /absolute/binding.json --job /absolute/job.json`.
5. Inspect `launch.json` and `events/ready.json` for the exact recipient and `KQUEUE_OS_FILE_EVENTS_NO_PERIODIC_POLLING`. The per-job supervisor waits for its exact child and atomically writes `completion.json`. The finite observer uses OS file events, attempts one ordinary `codex queue`, and exits. No periodic wake prompts or polling service are needed.
6. On the automatic notification in this same HQ, read the exact completion receipt and actual stdout/stderr. Match job/session/PID/grant/argv and provider terminal output. Record actual intake separately in the job's `hq-intake.json`; a queue acknowledgement alone never proves intake. Decide acceptance only at the demonstrated scope.

Never delete reservations to retry. Inspect and reconcile an ambiguous launch/send under its exact existing job; do not launch or notify again. A known nonzero child exit is a failed process outcome, not success. Queue timeout/nonzero/unrecognized acknowledgement is AMBIGUOUS_HOLD with no automatic retry. A supervisor crash does not prove child exit. Preserve all failed outcomes.

## Actual observed qualification

Harmless notification: job `sorok-notification-qualification-3e37880aea89`, session `LOCAL_NOTIFICATION_TEST_3e37880aea89`, PID68069, exit0, expected marker verified. Queue message `01a19a5a-cd32-7ff3-8ae4-b94eb5524e0b`; actual same-HQ intake recorded in that job's `hq-intake.json`.

Real OpenCode commission: job `sorok-opencode-roundtrip-5c69dd22ed58`, exact session `ses_e65a2fc2cffeNnmFUn19p4oZ83`, PID68726; model-authored operating checklist, no tools or source edits. Exit0, provider terminal `stop`, exact commission ID in returned JSON. Argv digest `f65c48cf4a8fc865ff0ccc9770cb825c2dff0b7402fa40877605f9b6ae50e280`. Queue message `01a19a5d-f89f-7ab3-b6b6-7bf1188c8a01` actually arrived in the original HQ; receipt and actual return were processed here. One notification reservation, observer ready and finished, no human transfer. Full durable custody is in that job directory: `job.json`, `binding.json`, `process.json`, `completion.json`, `stdout.jsonl`, `stderr.log`, `events/`, `model-return.json`, `hq-intake.json`. Raw return SHA256 `15a005ed38b081321b78b26d7dffe7e205f5a29ad0abfb556801cffb248b212c`.

This establishes finite infrastructure dispatch/return, not automatic work acceptance, OS isolation, scientific validity, PROGRAMMA acceptance or acceptance of the old engineering candidate. The returned checklist is advisory: its generic “no activation claimed” statement describes its source packet, not this subsequently observed activation; its ambiguity wording does not turn a known child failure into success or require replay.

## Optional HQ reasoning-level switching

The existing app `send_message_to_thread` tool exposes `model` and `thinking` overrides for a subsequent turn. The completion helpers do not: their ordinary queue message has no override. No reasoning-level switch was exercised by this qualification and no changed host-selected level is claimed. Do not add model turns merely to demonstrate switching or wait for jobs.

Periodic automations remain paused. The former generic-controller repair, historical scenarios, app UI crash and PROGRAMMA/person-science work were not resumed for this activation.


## Current construction dispatch — 2026-11-05 P2

Three actual controller launches extend the independently accepted sourcefree product at `41bf45813fd0adeffd9b54e1306c2022abe96514`; PR #697 is unchanged and unmerged. Current PROGRAMMA reconciliation is `f9b4595a8f6ddb2fe31f7b350f25df2afeef7340` (published isolated patch, not adopted PRE-MAIN).

- `sorok-p2-encounter-lifecycle-20261105-r1` | `codex/sorok-p2-encounter-lifecycle-20261105-r1` | session `ses_e52b17161ffe7omlNtc0EddtAB` | process `77831` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`. Exact commission and binding: controller `sorok-p2-encounter-lifecycle-20261105-r1/job.json` and `binding.json`.
- `sorok-p2-explicit-interval-flow-20261105-r1` | `codex/sorok-p2-explicit-interval-flow-20261105-r1` | session `ses_e52a51ef1ffeNtPTpxKAP6J37a` | process `77835` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-review-r1`. Exact commission and binding: controller `sorok-p2-explicit-interval-flow-20261105-r1/job.json` and `binding.json`.
- `sorok-p2-later-event-continuation-20261105-r1` | `codex/sorok-p2-later-event-continuation-20261105-r1` | session `ses_e52a51c43ffeuVe7ZZhNcga5YP` | process `77840` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-join-e-b-event-review-r1`. Exact commission and binding: controller `sorok-p2-later-event-continuation-20261105-r1/job.json` and `binding.json`.

Scopes respectively: persistent local exit/return with no actor/world mutation; explicit qualified interval activity to later public consequence with no automatic WAIT-as-action substitution; existing S41–S43 later-event producer/consumer continuation. New separate return directories only; no shared product/vendor/PROGRAMMA writes. DeepSeek V4.1-Flash MAX unchanged, existing session-scoped permissions only. Per-job supervisors and completion observers launched. Receive actual results, fan in compatible code on a later isolated integration branch, independently review consequential new boundaries, and write material results through PROGRAMMA. No new native/B-purpose/human/merge authority.


### P2 returns received and next three commissions dispatched

Lifecycle79b90e4a57cbd1b738a9b9484677736d1b6415ab independently ACCEPT_SCOPED_TEST_ONLY at6398888f1d28152b5d29fef816f0bb45e77dd43b (5tests+5probe groups). Intervalbdadbc57c2664d3155a97853422e74b6128261f8 (6author tests) and later-event76fdb624afc7674f088d10c349bfe15ffd0b865a (5author tests) are remote-verified candidates, not accepted. Actual terminal receipts and returns read in this HQ; intake records saved in original controller job directories.

- `sorok-p2-product-fanin-20261105-r1`: launched existing controller/session; PID84916 observed live without terminal receipt; exact prompt and binding in controller job directory.
- `sorok-p2-interval-later-independent-review-20261105-r1`: launched existing controller/session; PID84920 observed live without terminal receipt; exact prompt and binding in controller job directory.
- `sorok-p2-programma-return-intake-20261105-r1`: launched existing controller/session; PID84924 observed live without terminal receipt; exact prompt and binding in controller job directory.

Fan-in scope: one compatible same-root product CLI with lifecycle, qualified interval activity and later-event consumers. Separate independent review checks actual action/perception distinction and source-cut/cold boundaries. Guide worker owns direct affected-record write-through on existing PROGRAMMA branch; no competing guide edits. PR697/protected branch unchanged; no native/human/B grants.


### PROGRAMMA P2 intake publication and receiving continuation

Actual guide worker return35ae6f9aeaa5437ec497b44bbd044d32f76d4b0a remote-verified and received: existing00/07/08/09/10/14/15 now distinguish lifecycle scoped independent acceptance, interval/later author-tested candidates, running fan-in/review, and guide/protected/native/human holds. Canonical verifier PASS attributed to worker, no product rerun. Existing guide worker resumed as `sorok-programma-selective-receiving-20261105-r1` to stage the smallest compatible existing-record patch against live PRE-MAIN, preserving other owners/newer fields, or name exact indispensable predecessor. This advances actual pending guide receiving; no protected merge authorized. Product fan-in and independent causal review continue separately.


### P2 integrated candidate returned; upstream user-attempt repair dispatched

Fanin579afc5fe63ff305ec49d4c8d42abc8475acf8bb remote-verified, six author tests58.22s, candidate not independently accepted. One S47 root across cold public lifecycle, explicit qualified interval and later-event observation; encounters remain0 until explicit do-help increments1. Exact imported lifecycle/interval/later return trees preserved. Observed standalone interval defect: admit_continuation automatically calls adapter.do_help; integrated path avoids that helper, evidence/upstream_interval_auto_do_help.json preserves finding. Original interval worker resumed in `sorok-p2-interval-attempt-boundary-repair-20261105-r1` to remove automatic action and prove observation-only default plus explicit action; no other improvements. Existing independent interval/later review and guide selective receiving still active. Incumbent reviewer receives exact fanin after current terminal return; no concurrent same-session launch. Pending PROGRAMMA receiving must reconcile this newer candidate/defect rather than retaining fanin-running status. PR697/protected unchanged; holds preserved.


### Guide selective receiving candidate returned

`114d142f7fa34917892aa9480f0cfe695dc32fcd` on `codex/sorok-programma-selective-receiving-20261105-r1` remote-verified against protected8ffec40a. Existing nine guide files only,25stage rows/10seams, canonical/JSON/diff checks PASS attributed to worker. Not adopted/merged. Worker resumed as `sorok-programma-fanin-currentness-20261105-r1` to reconcile newer fanin579af returned candidate and standalone interval auto-help defect on both source and receiving guide branches before PR creation. Other active lanes: independent interval/later review and exact interval-attempt repair. No extra source/science/merge grant.


### Exact interval attempt repair received

Remote-verified repaired interval head7a256ed4873155dfad86faf2464110ee6f1e2ad4 (codedde8287a806a802cd8d6a3dc122870f8cf8c5c3a): author reports6focusedPASS; admit/continue now observation-only, explicit_do_help/CLI do-help separate. AUTHOR_TESTED_REPAIR, not independentaccepted. Original bdad failure preserved. Fan-in original author resumed exact existing branch as `sorok-p2-fanin-interval-repair-intake-20261105-r1` to refresh repaired imported bytes, actual importer/source manifest and affected boundary tests. Existing independent review still addresses original cuts, not thisrepair/fanin. Guide-currentness worker active against its declared cut; next coherent qualified intake must reconcile repair and final fanin, not silently inherit old acceptance. No protected writes/newrights.


### Independent interval/later review received — REVISE preserved

Reviewf1a2872487b3aa492632a497ad7481e8529d937e remote-verified. Original intervalbdad and later76fd bothREVISE;6+5focused tests and primitive material/source/event/cold checks passed. Exact failures: interval automaticDO_HELP (already repaired7a256 author-only, independent closure newly dispatched); later publicpositive/scheduled leaks61privacywalker keys and auto userattempt (primitive chain clean). Narrow laterrepair dispatched existing qualified implementer as `sorok-p2-later-public-boundary-repair-20261105-r1`; independent intervalclosure `sorok-p2-interval-repair-independent-closure-20261105-r1`. Repair fanin intake and PROGRAMMA currentness already active in other sessions;4useful lanes total. Guide write-through must include this later qualified REVISE before claiming currentness/adoption; do not collide with active guidewriter. Original41bfaccepted scope unchanged, fanin candidate remains unaccepted, protectedPR697 unchanged.


### PROGRAMMA receiving PR opened with newer independent review intake

Worker source174658adb/receiving6c5b9a291 received. HQ reconciled later independentREVISEf1a2872487b3aa492632a497ad7481e8529d937e and intervalrepair7a256 author-tested status in affected existing records on source59c861513fca9cf701c1ed04fda04e255de1c9a6 and receiving5b569b130379ee012936e2f6517fc7c49ddcbdea. Canonical verifier PASS on both; no productreruns. Open draft PR699 https://github.com/maidiu/rawlsing/pull/699 targets protected8ffec40a; not merged/adopted, no protectedwrite. Three construction lanes continue: repaired interval import into fanin, later public boundary repair, independent intervalrepair closure. PR697 unchanged. Guide currentness now records actual REVISE rather than running/noverdict, and exact repairedcandidate without acceptancepromotion.


### Refreshed fanin received and bounded receiving rehearsal launched

Exact25d40806d15516b7f7ffa04f47bc651022c6f2b0 remote-verified; imported repairedinterval7a256 tree6bc6632fa3ca67cedcdd16bc6cb5ea61b8e81789 byteexact30files.6interval+7fanin authorPASS, loadedsource checked, observations0encounters and explicitaction1. No fanincallsite change (already avoided faultyhelper); independentacceptance pending. Existing author now running `sorok-p2-protected-base-receiving-rehearsal-20261105-r1` on isolatednewbranch to test actual product25d + guidePR699 against protectedbase with one coldsequence, not fullsuite or selfreview. Other2lanes laterpublicrepair and independentintervalclosure continue. Rehearsal is engineeringonly, no protectedwrite/merge. Next coherent qualified guideintake should combine repairedsource and reviewresult rather than issue per-small-commit documentation work.


### Independent interval repair closure received: primary fix passes; two bounded defects remain

Exactreview89b33453eff13d8a3638a97cf516438c42e7af4f remoteverified REVISE7a256:6focused66.42s and original independentoracle confirm observation0encounters, explicithelp0->1, ACTUALrefuse/SCHEDULEDaccept, cold/sourcecutrestore. Remaining failures only publicreservedkeys admission/c9 (redactedvalues) and3nonexistentpyc evidenceentries. Existingfree guideworker now boundedcodefix `sorok-p2-interval-public-receipt-repair-20261105-r1`; incumbentnon-authorreviewer now actual integratedfirstconsumer review `sorok-p2-fanin-independent-review-20261105-r1` at25d408, preserving rejectedunusedstandalone surfaces. Receivingrehearsal and laterpublicrepair remainactive;4lanes. NextcoherentPROGRAMMA write-through must record primaryfix independentlyverified but7astillREVISE, and completed repair/finalreview as qualified; no oldacceptancepromotion/no newbureaucracy. Protected/source rights unchanged.


### Proven local OpenCode database lock; shared backend retry route

Two terminal worker failures surfaced UnknownError Failed to execute statement. Installed OpenCode log supplies exactcause effect/sql/SqlError/LockTimeoutError -> SQLiteError database is locked, not provider429 and not producttestfailure. Existing concurrent standalone CLI processes write shared database. Started documented localhost-only OpenCode1.18.34 serve --pure endpoint127.0.0.1:4096 (healthverified, PID97878; durable shared-opencode-server/process.json), no global config/permissionchanges. Reviewer retried same session/model/commission through supported run --attach endpoint as `sorok-p2-fanin-independent-review-20261105-r1-retry1`; newbindingargv digest exact. Active legacy workers leftundisturbed; future terminal retries/launches should use thisbackend while healthy, not parallel new standalone DBwriters. This is mitigation awaiting actualsuccessfulreturn, not provenresolved. Preserve existingcontroller finite supervisors/notifications. Diskchecked580MiBavailable, separateobservedconstraint, not establishedcause ofthislock; no unrelatedcleanup/deletionperformed.


### Exact WAL write-lock holder removed; controlled resumptions

Laterrepair attached retry1 exited0 but contained databaseerror and no finalreturn/commit: NOTSUCCESS. Darwin fcntl F_GETLK on opencode.db-shm byte120 identified actualwrite-lock PID94871 (our still-standalone receivingrehearsal), not merely an openfile. Sent SIGINT onlythat managedchild, supervisor durableexit-2, checkout/evidence preserved. Recheck byte120 returned F_UNLCK. Otherprocesses/DBcontents/globalpermissions untouched. Resumed original same sessions via sharedlocalhost documented--attach: rehearsalcont1, laterrepairretry2, intervalpublicreceiptrepairretry4; incumbentfaninreview attachedretry1 alreadyrunning, notduplicated. Allfuturemanagedlaunches use healthy sharedbackend and exactbindingdigest; no more standalonewriter launch. This proves the identified lock was released, NOT completedproduct/recoveryacceptance. Waitfor actual return and errorfree publication.


### First verified successful post-lock shared-server return

Rehearsalcont1 completed errorfree with publishedbf574e5a1c5b46bfd92d272fb9616ac697fbbe6a remoteverified. ActualcoldCLI and guidecanonicalPASS in composed protectedbase/product25d/guide5b569 snapshot tree3894541eeac3e2133a3823252c65f04252e21e93; snapshot-local imports, intended allowlist634changes. This demonstrates this managedshared-server continuation successfully completed, not universalinfrastructure health or independentproductacceptance. DirectPROGRAMMA existingrecord write-through now sourceb8c764f1279e5116d74d98ae7f5e423c5c69f7da, receivingb6d3f8d2b946a38f6336361c2b625c1260699100; PR699 body updated exactheads/receivingproof/interval89b334limits, canonicalPASSboth, notmerged. Other3current sessions continue publicrepairs and integratedreview.


### Second successful shared-backend return: interval public/receipt correction

Exact76d5a3d13e0219c1a085ebadd55071de2dd90e7d remoteverified; noerror+publishedreturn. Author6focusedPASS78.34s, originalprivacywalker and committedreceipt existenceoraclePASS,29actualfiles no pycache/selfreceipt. Primary noautohelp independentlyPASS89b334 preserved; finalkey/censusfix author-tested, no blanketindependentACCEPT. Existingmainintegrator resumed originalfaninbranch as `sorok-p2-final-interval-import-20261105-r1` through healthysharedbackend for exactimport/provenance and only affectedboundaryverification, no fullreruns. Laterpublicrepair and integrated25dreview remainactive;3lanes. Next coherent qualifiedPROGRAMMA intake includes corrected76d5 and integratednewhead without claiming old25dreview applies automatically. No protectedmerge/native/human/B change.


### Later-event public repair completed after shared-server recovery

Remoteverifiedb71624f21d0bc638e8817f3929cc6c01ab8b0f61 (code4bdba46c4d3a667a9cd7845eb57caa980df76373):8authorPASS, repairedpublic0privacyhits, no implicithelp on observation, explicitactiononly0->1encounters, causalprimitives/cold/cutrestore retained. Errorfreeactualpublishedreturn, not independentacceptance. Existingguideowner now `sorok-programma-public-repairs-intake-20261105-r1` directly reconciles interval76d5/laterb716 repairedsource+historicalREVISE+current25dreview/importstatus on source/receivingguidebranches, not justDELTA. Other2lanes finalintervalimport and independent25dreview. Next availableintegrator must consume exactlaterrepair before finalsourceclosure, no same-session overlap. No protected/native/human/B grant; originalengineeringreceivingevidence remains scopedto25d.


### Integrated P2 public path independently accepted at exact25d

Remoteverified332e00cb3da51b859a408a31f820b1afd7fe8fc0 ACCEPT_SCOPED_TEST_ONLY actualintegrated25d40806d15516b7f7ffa04f47bc651022c6f2b0.7focused103.31s plus independentcold/projection/access/sourcecausality probesPASS, actualsnapshotimports. Observations0encounters, explicithelp1, materialACTUAL/SCHEDULED contrast, outsidecold/localreturn, C9sourcecutrestore and S43historyverified. RawengineeringAPI fields remain privileged; publicfirstconsumer public_opportunity/CLI is accepted. Doesnot accept unused standalone7a/76fd, predecessor579, newerimports or native/human/protectedmerge. Existingreviewer now only originalfailureclosure interval76d5/laterb716 as `sorok-p2-public-repairs-focused-closure-20261105-r1`; 3lanes include finalintervalimport and activePROGRAMMA repairsintake. Nextguidequalifiedintake MUST replace integrated25dreview-running with actual332eaccept while preserving newerheadreviewgrades; no competingwrite to activeguideworker. No broadrepeatestate.


### Exact interval correction imported; final later import dispatched

Remoteverifiedd450f96b5de1fcf39bacefbfb4cd9bfbe66a8b18 imports interval76d5 exact30files,29receiptfiles checked, originalprivacy/receiptoraclePASS, fanincallsiteunchanged/no testestate rerun. Independentaccept332e00cb still exact25d, no newerheadpromotion. Same mainintegrator now `sorok-p2-final-later-import-20261105-r1` consumes laterb716 exactsource and only necessary APIchanges; focused actualboundary/coldsequence if callsitechanges, no newfeatures. Other2lanes independentpublicrepairclosure and coherentPROGRAMMApublicrepairsintake. Finalreceiving awaits exactnewhead review/sourceclosure; no protectedmerge.


### Final repaired P2 source assembled

Remoteverified4b2fed81c3f513eb4262ad5de277ce519c74c614 exactimports interval76d5 treef7bd1c51 + laterb716 tree67f01db8 (48filesexact); integratedcalls/primitivesunchanged, publicoraclezero hits, sourceoriginsverified. Earlier25daccept332e remains scoped; final4b2notyetindependentlyaccepted. Sameauthor now `sorok-p2-final-receiving-delta-20261105-r1` only actualfinalsource delta/allowlist/merge-tree and1cold firstconsumer sequence vs priorbf574 receiving, no repeatfullestate. Other2lanes focusedcomponentclosure and PROGRAMMApublicrepairsintake. Nextfinalqualification can reuse accepted25d+verifiedcomponentrepairs+finalreceivingdelta, no automaticbroadthirdreview; preciseindependentfinalcutstatement only if actualreviewerissues it. No protectedmerge/nativehumanBgrant.
