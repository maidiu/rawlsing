# Agent A — final counter self-adversarial accounting

Mission: SOROK #1008, original C03/C04, single shared A→B→A lineage. This is an engineering candidate without independently accepted G2, G4 or G5.

## What I proved (by source) and what I did not

- B's full BP4 hash and event-ID validation matches the actual BP4 make_event source blob 5c4a309d376ce2bedce6a8a7e4f09768131f4d46. B was right and the implementation remains.
- B's code still used an OR selection across event_id and operation_id, which could silently select the genuine event corresponding to one selector when the other was invalid. The B hash seal does not detect wrong semantic selection of a genuine event.
- B's direct read_child_uptake still treated absent historical witnessed receipt as NOT_PERCEIVED, and an extra forged child speech receipt for historically unheard speech as PERCEIVED. It did not validate original episode root/branch, embedded admission receipt, or parent own-speech.
- I committed a minimal C04 read-only code correction, an actual-J1/P6 pytest regression file, an isolated probe and this handoff. The private repository's complete runtime could not be executed locally; neither B's nor my current changes are G5 accepted.

## What I inherited and preserved

- A's C03 historically conditioned read-only alternatives, no automatic volition and no source-right elevation.
- A's C04 replay/self-read historical C12 and event custody, and exact writer claims.
- B's actual BP4 event schema, two-part content-address integrity check in all parent/child paths, hostile hash-mutation tests, probe and evidence.
- Predecessor material operations, B02/B04/B05 locks/currency, P3 focal owner, D03 eligibility, J1 source closure and original constraints are unchanged.

## What I broke, repaired and tested

- B-era selector OR -> strict event/operation conjunction when both supplied; single-selector behavior conserved. Actual package pytest committed but NOT_RUN; isolated algorithm test demonstrates both B false accepts and new refusal.
- B-era direct child-uptake receipt mismatch -> require C04 episode/admission receipt and parent own-speech/child receipt exact identities and historical perception; preserve B's hash gate. Source-equivalent isolated probe demonstrates witnessed-severance, false-hearing, missing-parent and duplicated-receipt negatives, with positive witnessed/unheard restoration.
- Isolated script /mnt/data/c04_agent_a_final_isolated_probe.py SHA-256 a3f4d38dce5fc7a623fece2871149d2f2b99b54825c159a3ed0ca0ef1d609911 executed EXIT 0, elapsed 1.29s, maximum resident 96016 KB. This is not an imported test of actual source, and the time/RSS is solely probe economics.

## What I attempted to break in my own repairs

- A genuine original heard utterance should still return PERCEIVED and allow matching simultaneous event+operation keys.
- A genuine original unheard utterance should still return NOT_PERCEIVED even if child's current position is different, never infer retroactive hearing from present co-presence.
- A second actual speech does not match the first event's operation pair.
- Parent self-read/replay still performs B's full world seal; I changed no maker or event writer.
- An embedded receipt with contradictory historical hearing channel must fail rather than be promoted through a separately supplied child receipt.
- Missing and duplicate C12 receipts must fail closed.
- The new source selector and admission checks could refuse a legitimate authorized migration of old sourcefree records; authentic fork/cold fixtures are required to adjudicate that question.

## Strongest vulnerabilities and owner limits

1. Entire code under test has NO full project execution receipt. Regression failures may exist in actual J1/P6 and their import closure; next agent must run it. Do not call a source-equivalent probe a real RED→GREEN.
2. Mother does not independently select. Legacy experimental auto-purchase remains caller-instructed; actor-authored speech is not generated, so original G2 remains held.
3. Caller can claim parent self-read with as_actor=parent_id; there is no session principal authentication at this experimental API. No new authority implied.
4. Self-hashes do not protect against coordinated privileged tampering in the underlying actor/world store; direct owner custody remains essential.
5. Cold/fork, changed/restored and material economic tests, B05 rent, P3/P6 native paths and D03 performed child event remain unverified on this exact SHA.

## Rejected shortcuts

- Reducing B's seal to accept unsealed migrated events without actual source-owner evidence.
- Hardcoding a psychological parent motive from money or care obligations to announce G2 completion.
- Changing B02/B04/B05, D02/D03, J1, P3 or protected integration without source custody.
- Reopening the stopped general fleet #939, creating new review campaigns, or self-issuing G5.

## Exact G1-G5

G1 PARTIAL_SOURCE_GROUNDED.
G2 HOLD_PARENT_OWNED_SELECTOR_AND_ACTUAL_EXPRESSION.
G3 ISOLATED_ALGORITHM_NEGATIVE_PASS; REAL_J1_P6_NOT_RUN.
G4 READ_ONLY_SOURCE_DIFF_CONSERVED; COLD_AND_ECONOMICS_NOT_RUN.
G5 NOT_STARTED_INDEPENDENT_NONAUTHOR.
Scientific native CAN/ADP and memory rules HELD; human and actor rights NOT_ISSUED; protected merge NONE.

STOP for separate nonauthor receiving after final A return. No further A/B round absent an actually reproduced original-contract violation.
