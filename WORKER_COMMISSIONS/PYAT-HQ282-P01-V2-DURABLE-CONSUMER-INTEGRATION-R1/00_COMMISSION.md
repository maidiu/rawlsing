# Pyat HQ282 P01 — connect the workload verifier, batch processing, and downstream consumer

**Status:** Commission prepared; waiting for the secondary-Mac worktree to be set up. No engineering work has been launched by this document.

**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/rabochii-pyat-hq282-p01-v2-durable-consumer-integration-r1`  
**Startup:** Use the exact remote commit containing this revised commission, supplied in the accompanying launch message. Confirm that commit before beginning.  
**Worker:** Local integration engineer  
**Machine:** Secondary Mac  
**Model:** GPT-6.1 Sol  
**Reasoning level:** Medium. Do not automatically increase it.  
**Repository permissions:** Source-free implementation and tests only.  
**Governing project decision:** `HQD-2026-10-10-280`. This commission does not change scientific or release authority.

## 1. Writing and communication

Use plain, ordinary engineering language throughout your work, terminal notes, code comments, reports, and conversations. Describe a test in terms of the behavior it checks, such as "missing-item test," "incorrect release reference," "duplicate-result check," or "process interruption and recovery." Avoid unnecessary dramatic or adversarial labels when precise technical wording will do.

Do not change, weaken, omit, or misrepresent the required tests to obtain more agreeable wording. If a tool or platform gives a warning or requests an unfamiliar external login, special security device, or account enrollment, do not attempt to bypass it. Stop that step, record the exact request in neutral language, and ask for an authorized alternative. This task does not call for a Daybreak account or hardware security key.

## 2. Worktree setup must be completed first

The user has confirmed that this commission's secondary-Mac worktree **does not exist yet**. Do not assume a directory exists, run the integration tests in a different worker's directory, or create a fresh repository clone.

Before using Codex for the engineering work, have the user or an already authorized inexpensive shell helper follow:

`PYAT_CONTROL_ROOM/RESOURCE_AWARE_COMMISSION_COMMAND_R1/HQ282_P01_SECONDARY_BOOTSTRAP_HANDOFF_R1.md`

That setup note is on the working HQ branch `agent/vozhd-pyat-hq280-pre-v3-parallel-operating-seal-r1`, not necessarily present in this commission's checkout.

The setup should attach **one separate sparse worktree** for this existing branch to the **existing Rawlsing Git object store on the secondary Mac**. A fresh clone is not permitted merely because the worktree is missing. If there is no existing shared repository on the secondary, return `SECONDARY_REPOSITORY_SETUP_REQUIRED` and wait for separate machine-level instructions.

Before coding, confirm and record:
- The actual working directory, branch and full commit.
- That the directory is the dedicated P01 worktree and has no unexpected edits.
- The shared Git directory, available Python interpreter, and pytest installation.
- The required source-code commits and any missing dependencies.
- The actual available secondary Codex allowance, approved environment and model setting.

If any required item cannot be confirmed, report `SETUP_INCOMPLETE` and the missing detail. Do not consume Codex usage trying to guess how the machine was arranged.

## 3. Engineering goal

Previous work produced two separate parts that have been individually tested but not yet exercised together:

1. A verifier that checks whether the expected source-free work was fully and correctly represented.
2. A batch execution component that records progress and supports recovery after an interrupted process.

Build **one working source-free integration** connecting these parts and an existing downstream empirical or Field Forge consumer. Reuse the real existing C11, Route B, I03/I05, batch, C1 and Field Forge interfaces where relevant, rather than writing parallel replacements.

Demonstrate this sequence:

`independently prepared expected tasks → existing verifier → existing batch runner and saved execution record → actual downstream consumer → independently checked result`.

Use a small deterministic synthetic dataset. The expected task set must be prepared separately from the execution output, before running that output. Keep item, subject, release and response identities consistent across steps.

### Exact previously committed inputs

- V2 verifier and associated tests: `d6e766cd6ba7dc46b19cc61123d968a274015ddd`
- Batch integration and recovery candidate: `92cb25340c49fb51e2b8d6e00d5a4f471296fc8f`
- Independent integration review: `59d644ccf35cd79c67e7e26e6b9e4de74039b442`
- Independent expected-work checking script: `9491d0296c95ee2942fe80eadc6aa9f54b07c634`
- Exact independent checking script Git blob: `00a4cc84d321c3fbace0f4aa09be62dbb31994fc`

Read these from Git using the exact commit and file identities. Do not assume the source files from separate branches are already available as a single installed module. Bring only the required code and synthetic test dependencies into the new P01 candidate in a controlled, documented way. Do not merge the original branches into the project's main or accepted implementation branches.

Some older verifier tests contain file paths pointing to worktrees on the primary Mac. On the secondary Mac they may be skipped because those folders are absent. Record every skipped test separately. Verify the independent checking script using the exact Git objects and create portable test checks where appropriate. A test that did not run must not be reported as passed.

## 4. Tests and expected results

Run a positive example showing that every expected task is included, the batch component completes an ordinary run, the result is saved and can be read again, and an existing downstream consumer actually uses that result.

Also test the important failure cases:
- An expected original item is missing from the submitted work.
- The submitted work contains a different item, release, or subject identity.
- Two items or saved results incorrectly reuse an identity.
- A process ends before its result is fully recorded.
- The process resumes after an interrupted save without repeating completed external effects.
- A task remains unresolved, so later tasks must not be counted as completed.
- The downstream consumer receives outdated, unrelated, or incomplete input.
- The expected task list is generated from the observed output instead of being independently prepared.

Use the actual project test framework and report commands, exit codes, counts of passed/failed/skipped tests, and the exact code revision. For interruption tests, use the project's existing safe synthetic subprocess test harness; do not run against real services or respondent records.

If there is a necessary interface change to an accepted owner, document exactly what is missing and stop at a proposed change rather than editing the accepted owner.

## 5. Scope and resource limits

- Work only in **new, isolated source-free candidate code and tests** and the P01 return directory.
- Do not access real survey data, move the primary Mac's private files, or change accepted scientific meaning.
- Do not publish any output as a current or authorized Rawlsing product.
- Do not change canonical integration, semantic PRE-MAIN, the HQ handoff pointer, or another worker's branch.
- Primary Mac Codex is reserved for full-repository Astra work. The **secondary Mac** is the only proposed Codex account for P01.
- Last observed screenshot: secondary **98% weekly remaining**. This is historical; check live usage before starting and after each bounded phase. Proposed P01 allowance is no more than **two weekly percentage points**, with a provisional **95% weekly floor** across ordinary jobs before 18 October. Dashboard percentages are not enforceable hard caps.
- Do not use reset credits, enable paid overage, change accounts, or raise reasoning beyond **Medium** without the user's express approval.

Read and apply the original resource-selection contract at:

`agent/vozhd-pyat-rcm01-resource-aware-commission-command-r1 @ c71f83c731fe1465b59f5ad701a5e1bb3018b34a`

and the later working-HQ resource and shared-worktree instructions. Where earlier wording conflicts with this revised, user-directed route, the secondary-Mac/MEDIUM/model and plain-language requirements above govern this assignment. Existing scientific, source and security decisions remain binding.

## 6. Completion and handoff

Once actual engineering begins, make a commit on **this branch only**, push it and verify the remote commit. Put the return under:

`WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1/`

Include a short `00_RETURN.md` describing what works and what remains blocked; a precise implementation and consumer record; actual test commands and results; resource usage if observed (or `unknown`); and the relevant code/test commit identities. Existing structured return filenames in earlier commission instructions may be retained for compatibility, but write reports in the plain technical style specified here.

A separate reviewer will assess the completed integrated candidate. Do not treat passing your own tests as final scientific or integration acceptance.

**Expected first response if the worktree is still absent:** `SETUP_INCOMPLETE — secondary P01 worktree not prepared; engineering not started; no Codex engineering usage`.

**Expected successful handoff:** A reproducible source-free integration, evidence of actual consumer use, independently reviewable test results, and an exact pushed commit.