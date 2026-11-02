"""Source-backed P1 whole-program seed for the living reference.

This is a seed data module, not a second database.  It preserves original
identifiers and exact source locators.  Maturity statuses are separate
evidential axes, not a completion percentage.
"""
from __future__ import annotations


def S(commit, path, blob, quote, line_start=1, line_end=1, depth="SELECTED_TEXT_READ", **extra):
    item = {
        "commit": commit,
        "path": path,
        "blob": blob,
        "object_type": "blob",
        "line_start": line_start,
        "line_end": line_end,
        "quote": quote,
        "depth": depth,
        "reader": "PROGRAMMA_ENGINEER_R1",
    }
    item.update(extra)
    return item


def L(path, sha256, symbol, line_start, line_end, note):
    return {
        "repository": "LOCAL_EXTERNAL_RAWLSING_DESKTOP",
        "path": path,
        "sha256": sha256,
        "symbol": symbol,
        "line_start": line_start,
        "line_end": line_end,
        "depth": "LOCAL_EXTERNAL_DIRECT_READ",
        "reader": "PROGRAMMA_ENGINEER_R1",
        "note": note,
    }


def M(I, T, A, E, C, V):
    return {
        "I": {"status": I},
        "T": {"status": T},
        "A": {"status": A},
        "E": {"status": E},
        "C": {"status": C},
        "V": {"status": V},
    }


def N(nid, layer, kind, title, summary, owner, status, refs, maturity=None, acceptance=None):
    node = {
        "id": nid,
        "layer": layer,
        "kind": kind,
        "title": title,
        "summary": summary,
        "owner": owner,
        "status": status,
        "source_refs": refs,
        "programma_p1": True,
    }
    if maturity is not None:
        node["maturity"] = maturity
    if acceptance is not None:
        node["acceptance_record"] = acceptance
    return node


PRODUCT = "865b5b01e1a27e99020cf2bb389af8cd4c874b57"
ORIGINAL = "4f2ce6f9bdfdd2232a23d839905cb386cde96dcd"
CAN = "25830fe7462bb9e29bc4087e6ae14f3f84cec377"
P1 = "b65c75a9e62618690f7d02265bc9e850af549161"
JOIN = "4387dc818a96fda2d5271672505fbd9da1059703"
RRIF = "cf578514434532b48e86c76c1d38d6250323a1ce"
PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
W1A = "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7"
W1B = "5ab447a447620e65d441d2d2cfd745cb3d354a7c"
W1C = "12433b89e100d2c4b9b20a94c4ccca7d2af7529a"
W1D = "950ace6fe8a63c225134ada0c79e97bb57d296a0"
W1E = "a64ff782ad2dd8f8f6617564655d09f6c3349ffb"
SYNTH = "e5a25cbc4f2b9d7476a72637d3e371ee3254742e"

CHARTER = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/01_PRODUCT_CHARTER.md", "b715c67766073ee363720020466ea979ac29653a", "Rawlsing presents a neighbor. Attachment, trust, health, pleasure, compliance, intimacy, benefit, dependency and access must remain distinct.", 7, 43, "FULL_TEXT_READ")
ALPHA = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/03_REAL_ALPHA_SPINE.md", "ae4c120b4e15bd9e5088cacc9c4d1fa5257d1770", "KERNEL = UNRESOLVED. None is yet adjudicated as the unique or sufficient generative kernel of Rawlsing.", 19, 34)
MAP = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/05_PROGRAM_MAP.md", "2a0a3a42d66f566f92d5c333fbbea4a5adb383b2", "S5 flourishing; S13 monetization; S14 safety/privacy; S15 alpha/evaluation are constitutive constraints, not optional administration.", 1, 149, "FULL_TEXT_READ")
COURT = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/24_COURT10_FLOURISHING_MORAL_PHYSICS_R1.md", "9871b31ebf2697fde7d72dccd2b7f41a26cf6a43", "Do not collapse affection, attachment, dependence, gratitude, compliance, conflict reduction, relationship persistence, subjective happiness, user approval, flourishing. Care can become domination. Refusal can be care.", 15, 132)
ALPHA100 = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/100_MINIMAL_WHITE_WHALE_ALPHA_AND_FIDELITY_ESCALATION_CONSTITUTION_R1.md", "bd08a138ebf82522d7c90bb7e702d79697b3c240", "What is the cheapest bounded product in which the user still encounters an unchosen, independently caused person through partial perception, actual user-owned action, irreversible history and non-player-centric consequence? CORE INVARIANT MAY NOT BE BRACKETED. FIDELITY MAY BE BRACKETED.", 9, 35)
ALPHA101 = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/101_BINDING_SURFACE_ACTOR_PHENOMENOLOGY_SEGREGATION_AND_TWO_CALL_RENDERING_R1.md", "51f0fd1fa95da641d40ec5fb94e879fcbf0ae7a1", "CAUSAL NADIA != OBSERVABLE NADIA != USER-EXPERIENCED NADIA != USER-INTERPRETED NADIA. Actor/world realization must occur before user-phenomenal personalization.", 18, 90)
CALLS101 = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/101_BINDING_SURFACE_ACTOR_PHENOMENOLOGY_SEGREGATION_AND_TWO_CALL_RENDERING_R1.md", "51f0fd1fa95da641d40ec5fb94e879fcbf0ae7a1", "NORMAL LIVE TURN = DEEPSEEK-CLASS TRANSDUCTION CALL x1 + CLAUDE-CLASS ACTOR REALIZATION CALL x1. NORMAL_LIVE_MODEL_CALL_TARGET = TWO.", 637, 659)
QUESTIONS = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/registers/QUESTIONS.jsonl", "1d099797cd3e43f574efe394e91f8aebae07ebb7", "Q-GAME-001 and Q-ACTION-001: status OPEN and closure_state CLOSED_FOR_ALPHA. Q-HEALTH-001: OPEN_DISCOVERY, post-alpha.", 1, 1, "EXACT_ROW_READ")
DECISIONS = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/registers/DECISIONS.jsonl", "52eb00706787b8be4193a02feca420ccac50cd72", "SPD-0003: Attachment, trust, health, pleasure, compliance, intimacy, benefit and dependency must remain distinguishable system variables or concepts.", 3, 3, "EXACT_ROW_READ")
D002 = S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/dockets/D002_ALPHA_CORE_LOOP_ACTION_SURFACE/12_SMALLEST_LAWFUL_PLAYABLE_MOMENT_ADJUDICATION_R1.md", "fdd35b39f1eb569eb635e5cfddd71ac078cc4f9f", "Actual contribution is morally neutral: objection, refusal, silence, inaction and moral neutrality count. No register promotion or playtest claim.", 58, 123)
STRATA = S(ORIGINAL, "SOROK_PRODUCT_CONTROL_ROOM/ASTRA_NATIVE_GAMEPLAY_NECESSITY_SYNTHESIS_R1/STRATA_MAP.md", "12c5be617bff53162c88bd78d76af4eecd0545e2", "Scales A-H are scales of possible experience, not stages through which a person should progress. A quiet scene need not be packed with competing demands. A narrowing relation is not automatically evidence of bad play.", 1, 97, "FULL_TEXT_READ")
NEGATIVE = S(ORIGINAL, "SOROK_PRODUCT_CONTROL_ROOM/ASTRA_NATIVE_GAMEPLAY_NECESSITY_SYNTHESIS_R1/NEGATIVE_CONTROLS.md", "1e3d1084d3e15a9b6f3ba3aef568c8e9efe4a951", "Reject persona-as-puzzle/reward, savior destiny, content vending, engagement-triggered crisis, disclosure ladders, universal timed quests and moral scores.", 1, 40)
CAN11 = S(CAN, "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_011_V3_MIDDLE_STATE/AUTHORITY.md", "1ed04e62a363493bc7032a99139454a3126e6ea0", "Permitted generic operations: CREATE, REINFORCE, WEAKEN, TRANSFORM, SET_DORMANT, REACTIVATE, END, NO_CHANGE. Operation names supply no content; the accepted update rule defines qualification and effect. MIDDLE_STATE_UPDATE_RULE_MISSING: no exact accepted update rule; mutation blocked.", 238, 276)
CAN8 = S(CAN, "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY.md", "976c59086b938992114f68621f149687670e306d", "External event may have happened without the actor receiving it; response rule and effect legality are separate.", 1, 80, "RETURN_REPORT_READ")
P1DOC = S(P1, "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/00_PLAIN_ENGLISH_PRODUCT.md", "fecd5dbcfdc3733ce6ec2ad345e7d3e7eb3931f6", "Grade: TEST_ONLY_SOURCEFREE_NOT_NATIVE. A speech label is not the causal source.", 1, 85, "FULL_TEXT_READ")
P1CODE = S(P1, "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_consumer.py", "6b8b9a38b7deaf1b43100b5662d34d03f67ec5e4", "run_trajectories constructs share/access/request, share/no-access, refusal and share/perform-versus-omit lives.", 1, 120)
P1S35 = S(P1, "WORKER_RETURNS/PROGRAMMA_SOROK_P1_MATERIAL_HISTORICAL_PERSON_SOURCEFREE_CONSUMER_R1/candidate/p1_s35.py", "02d656868b1963fc6468bab1b25ef98fecdb5141", "p1_s35.evaluate always returns T_NO_CHANGE; it is an isolated TEST_ONLY adapter and never installs a C9R automatic route.", 1, 80)
JOINV = S(JOIN, "WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md", "52dfc715bed3ef14cc3dc4639132c409c4e99712", "REVIEWED FORK-ATOMICITY CUT 7bf2da302996491ddf34b9a039fea47ac982d135... Exact-cut engineering verdict: ACCEPT_SCOPED. Science remains TEST_ONLY/H0; authority remains none.", 1, 60, "FULL_TEXT_READ")
RRIFDOC = S(RRIF, "WORKER_RETURNS/SOROK-RRIF-E-F2-FULL-R2-BLOB-GATE-R1/00_RETURN.md", "536f243bee3fc258d3170b9f08acf0bde73f9e77", "F1 checked 444 vendor blobs and 459 path names but not 15 nonvendor bytes. F2 checks all 459. First consumer PARTIAL. C9_SOURCE_MISSING and OWNER_ANCHOR_REQUIRED remain.", 15, 70, "FULL_TEXT_READ")
M6 = S(PREMAIN, "rawlsing_next/m6_actor_safe_expression.py", "74d9701cdc7dabccf61eb5089498db290c1efd9c", "situated phenomenology/disclosure/salience/inhibition/affect/interlocutor/register behavior requires a separately accepted named authority; M6 is only the semantic ceiling.", 915, 924)
GT0 = S(PREMAIN, "rawlsing_next/wsc_gt0_end_to_end.py", "62b6ea39c605874af6d7aef85693472f88087f57", "TERMINAL = BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS", 11, 60)
PROGRESS_MD = S(PREMAIN, "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md", "fd6ce00595e7b1ea9bb997cf7bd9fcb4e83eccbe", "revision36; two productive work orders STATUS=PUBLISHED_NOT_LAUNCHED (no session/process inferred).", 1, 12)
PROGRESS_JSON = S(PREMAIN, "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json", "c7fb05d8e5d0240959191041a73e76e2f14cb436", "RAWLSING_CROSS_HQ_PROGRESS@1 revision 35.", 1, 8)
W1A_DOC = S(W1A, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md", "b457bebf63d4ae12d01b8481481368bcd082e269", "SOURCE_GROUNDED__PARTIAL_WHOLE_ESTATE_COVERAGE__NO_SCIENCE_OR_PRODUCT_ADOPTION.", 1, 40, "FULL_TEXT_READ")
W1B_DOC = S(W1B, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_B_DEVELOPMENTAL_SCIENCE_R1/00_FINDINGS_AND_RECOMMENDATIONS.md", "21c018830bb64ba5eb4d4545fd6017869a20bc68", "SOURCE_GROUNDED_SCIENTIFIC_ARCHITECTURE_RESEARCH__ALTERNATIVES_OPEN__NO_NATIVE_ISSUANCE.", 1, 40, "FULL_TEXT_READ")
W1C_DOC = S(W1C, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_C_ORIGINAL_NEO_ENGINEERING_R1/00_FINDINGS_AND_RECOMMENDATIONS.md", "992fa1e23ada3d34d8ee1931d375375694882f7d", "RESEARCH_RETURN; independent I3 documentary investigation, not scientific issuance, native integration, independent self-review or HQ adoption.", 1, 40, "FULL_TEXT_READ")
W1D_DOC = S(W1D, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_D_HISTORY_WORK_CONTROL_R1/00_HISTORICAL_ORGANIZATIONAL_FINDINGS_AND_MINIMUM_AGENT_PROTOCOL.md", "05204c9c6a18fb8c1e7e599f09cee767aea54ffc", "SOURCE-GROUNDED PARTIAL WHOLE-ESTATE INVESTIGATION; FINITE DESIGN RETURN; NOT owner adoption.", 1, 40, "FULL_TEXT_READ")
W1E_DOC = S(W1E, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_E_LIVING_REFERENCE_ARCHITECTURE_R1/00_FINDINGS_AND_RECOMMENDATIONS.md", "b0413cdfccbb45d62df682786a5543e117d6a174", "Provisional choice: evolve the one O-LIVE persistent reference, not replace it.", 1, 40, "FULL_TEXT_READ")
SYNTH_DOC = S(SYNTH, "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/20261101_W1_JOINT_ARCHITECTURE_SYNTHESIS_AND_MINIMAL_BUILD_DECISION.md", "fa329d1c4c95114ab7d92b6e0265ace5fe6cfae4", "One linked logical state, multiple views, original purpose first, exact source/function/consumer/reviewer/owner connections.", 1, 80, "FULL_TEXT_READ")
V3YEAR = L("/Users/matthewsmith/Desktop/Rawlsing/v3/engine/yearly_step.py", "47c97bfae08134f14fbd38b0cc997823a047474e0fbf7da6ddff9f1412a5235d", "run_one_year", 12, 60, "Direct local external copy. SHA-256 differs from W1-C prior member hash da3147c3; do not conflate.")
V3SHEET = L("/Users/matthewsmith/Desktop/Rawlsing/v3/io/persona_sheet.py", "b90fe456b010cb7f8f8d09275c77be7a205a0b7748140dec4c4c103fa0b9c74a", "build_persona_sheet", 446, 490, "Direct local external copy. SHA-256 differs from W1-C prior member hash 4a000953; do not conflate.")
V3SIM = L("/Users/matthewsmith/Desktop/Rawlsing/server/generation/simulation.py", "ac0ce203becfbb3d3a7ac942014d8eb2257bfd1fb450ddc2536a98d97058cd6b", "run_simulation_for_session", 160, 170, "Imports run_one_year and build_persona_sheet; calls at lines 563 and 749.")
V3TURN = L("/Users/matthewsmith/Desktop/Rawlsing/server/chat/turn.py", "10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3", "chat_turn", 110, 160, "Imports load_persona_sheet_with_integrity at line 127 and calls it at line 157.")
V3LOAD = L("/Users/matthewsmith/Desktop/Rawlsing/v2/run_conversation_chat.py", "4d8b5772a8291d0c12e29c8809a2edfdb13d3942141edbc124aa036abeb41f91", "load_persona_sheet_with_integrity", 37, 175, "Historical V2 persona-sheet loader; not a current PRE-MAIN importer.")


NODES = [
    N("PURPOSE_UNCHOSEN_NEIGHBOR", "L0", "PURPOSE", "Meet an unchosen neighbor whose life places a claim on the user", "The product begins with a neighbor rather than a user-selected attractive, useful or congenial persona. Attachment, trust, health, pleasure, compliance, intimacy, benefit, dependency and access remain distinct.", "SOROK_ORIGINAL_PRODUCT_OWNER", "PROVISIONAL_PRODUCT_LAW_R1", [CHARTER], M("PRESENT", "PARTIAL", "PARTIAL", "MISSING", "TEST_ONLY", "MISSING")),
    N("SOROK_100_ALPHA", "L1", "PRODUCT_CONSTITUTION", "Minimal white-whale alpha: independent person, partial perception, action and irreversible history", "Fidelity may be bracketed; the core invariant may not. No production feasibility is claimed.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "PROVISIONAL_ALPHA_ARCHITECTURE_STRATEGY", [ALPHA100], M("PRESENT", "PARTIAL", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("SOROK_101_BINDING", "L1", "ARCHITECTURE_CONSTITUTION", "101 binding surface: actor occurrence before user-phenomenal projection", "CAUSAL NADIA != OBSERVABLE NADIA != USER-EXPERIENCED NADIA != USER-INTERPRETED NADIA. User attention filters an already existing occurrence; it may not cause the occurrence.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "PROVISIONAL_ARCHITECTURE_DIRECTION_NO_IMPLEMENTATION_PROOF", [ALPHA101, CALLS101], M("PRESENT", "PROPOSED", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("Q_KERNEL_001", "L1", "OPEN_QUESTION", "KERNEL_UNRESOLVED", "No single generative kernel is adopted. Relational personhood, independent otherness, partial knowledge, irreversible history and person x event mediation coexist as candidate invariants.", "SOROK_ORIGINAL_SCIENCE_OWNER", "OPEN_DISCOVERY", [ALPHA], M("PRESENT", "CONTESTED", "MISSING", "MISSING", "MISSING", "MISSING")),
    N("W1_JOINT_SYNTHESIS", "L1", "ARCHITECTURE_DECISION_CANDIDATE", "W1 joint synthesis: one living reference, P0 trust repair before breadth", "Five independent W1 returns converge on one logical reference, original identities, typed evidence edges, append-only change and derived views. Not owner-adopted law.", "SOROK_HQ", "SOURCE_GRADED_HQ_PROPOSAL_NOT_ADOPTED", [SYNTH_DOC], M("PRESENT", "PROPOSED", "PROPOSED", "PARTIAL", "TEST_ONLY", "MISSING")),
    N("ASTRA_B_SCENE", "L2", "EXPERIENTIAL_SCALE", "Astra B: scene / minutes", "Sustained attention, timing, explanation and responsiveness with independent resistance. A quiet scene need not be packed with demands and can have value without later attachment.", "ASTRA_RESEARCH_OWNER", "UNADOPTED_RESEARCH_VIEW", [STRATA], M("PRESENT", "PARTIAL", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("ASTRA_D_LONGITUDINAL", "L2", "EXPERIENTIAL_SCALE", "Astra D: longitudinal single-person continuity", "Person-specific memory, independent advancement, changed availability and humane absence. A narrowing relation is not automatically bad play.", "ASTRA_RESEARCH_OWNER", "UNADOPTED_RESEARCH_VIEW", [STRATA], M("PRESENT", "PARTIAL", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("ASTRA_NEGATIVE_CONTROLS", "L2", "REJECTED_DESIGN_SPACE", "Astra negative controls", "Rejects persona-as-puzzle, savior destiny, engagement-triggered crisis, disclosure ladders, universal timed quests and moral scores.", "ASTRA_RESEARCH_OWNER", "UNADOPTED_RESEARCH_VIEW", [NEGATIVE], M("PRESENT", "PRESENT", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "REVIEWED_NEGATIVE")),
    N("Q_GAME_001", "L3", "HISTORICAL_QUESTION", "Q-GAME-001: smallest repeatable gameplay loop", "Raw historical status OPEN coexists with closure_state CLOSED_FOR_ALPHA and resolution refs. It is historical alpha closure, not a newly reopened P0 task.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "OPEN_TEXT__CLOSED_FOR_ALPHA", [QUESTIONS], M("PRESENT", "PARTIAL", "PRESENT", "HISTORICAL", "MISSING", "MISSING")),
    N("Q_ACTION_001", "L3", "HISTORICAL_QUESTION", "Q-ACTION-001: meaningful action beyond conversation", "Raw OPEN status coexists with CLOSED_FOR_ALPHA and D002/27/29/SPD refs. The alpha answer is historical and not automatically a fresh P0.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "OPEN_TEXT__CLOSED_FOR_ALPHA", [QUESTIONS, D002], M("PRESENT", "PARTIAL", "PRESENT", "HISTORICAL", "MISSING", "MISSING")),
    N("D002_SMALLEST_MOMENT", "L3", "HISTORICAL_DECISION", "D002 smallest lawful playable moment", "Actual contribution is morally neutral: objection, refusal, silence, inaction and moral neutrality count. No register promotion or playtest claim.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "PROVISIONAL_D002_ADJUDICATION_NO_REGISTER_PROMOTION", [D002], M("PRESENT", "PARTIAL", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("Q_HEALTH_001", "L3", "HISTORICAL_QUESTION", "Q-HEALTH-001: defensible flourishing independent of attachment and approval", "Raw status OPEN, closure_state OPEN_DISCOVERY, post-alpha. A defensible plural measurement and actual evaluation remain missing.", "SOROK_ORIGINAL_SCIENCE_OWNER", "OPEN_DISCOVERY", [QUESTIONS], M("PRESENT", "CONTESTED", "MISSING", "MISSING", "MISSING", "MISSING")),
    N("Q_ONTO_001", "L3", "HISTORICAL_QUESTION", "Q-ONTO-001: relational ontology boundary", "Relational personhood hypothesis must not become a novel sovereign dyadic engine; person != dyad != network.", "SOROK_ORIGINAL_SCIENCE_OWNER", "OPEN", [S(PRODUCT, "SOROK_PRODUCT_CONTROL_ROOM/02_PROVISIONAL_RELATIONAL_ONTOLOGY.md", "72a1a5838ec66de6edbe77a064ba2e9a80d4407e", "person != dyad != network; relationally constituted personhood is a hypothesis, not governed V3 law.", 1, 40, "RETURN_REPORT_READ")], M("PRESENT", "CONTESTED", "PARTIAL", "MISSING", "MISSING", "MISSING")),
    N("SPD_0003", "L3", "PROVISIONAL_PRODUCT_LAW", "SPD-0003: attachment, trust, health, pleasure, compliance, intimacy, benefit and dependency remain distinct", "Provisional product law. Reopen only for a stronger ontology preserving all distinctions with fewer objects.", "SOROK_ORIGINAL_PRODUCT_OWNER", "PROVISIONAL_PRODUCT_LAW", [DECISIONS], M("PRESENT", "PARTIAL", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("COURT10_FLOURISHING", "L3", "OPEN_COURT", "Court 10: flourishing, harm and non-dominating care", "Plural partially incommensurable flourishing dimensions; care can become domination; refusal can be care; no hidden moral grade.", "SOROK_ORIGINAL_SCIENCE_OWNER", "OPEN_COURT_NOT_ADOPTED", [COURT], M("PRESENT", "CONTESTED", "MISSING", "MISSING", "MISSING", "MISSING")),
    N("FLOURISHING_ALT_ATTACHMENT", "L3", "SCIENTIFIC_ALTERNATIVE", "Alternative: attachment or retention as welfare proxy", "Rejected as a flourishing measure by 01/24/SPD-0003: increased attachment can coexist with reduced agency, exit or outside relations.", "SOROK_ORIGINAL_SCIENCE_OWNER", "REVIEWED_NEGATIVE", [COURT], M("PRESENT", "REVIEWED_NEGATIVE", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "REVIEWED_NEGATIVE")),
    N("FLOURISHING_ALT_RETENTION", "L3", "SCIENTIFIC_ALTERNATIVE", "Alternative: session count or user satisfaction as flourishing", "Rejected by the product charter and Court 10; S13 incentives must not monetize attachment, suffering or compulsive return.", "SOROK_BUSINESS_OWNER", "REVIEWED_NEGATIVE", [MAP], M("PRESENT", "REVIEWED_NEGATIVE", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "NOT_REQUIRED_WITH_REASON", "REVIEWED_NEGATIVE")),
    N("FLOURISHING_ALT_PLURAL", "L3", "SCIENTIFIC_ALTERNATIVE", "Alternative: plural, partially incommensurable flourishing dimensions", "Court 10 candidate: agency, boundaries, multiple relations, material security, reality contact, repair, care, play, exit from coercive dependency and meaningful projects; not averaged.", "SOROK_ORIGINAL_SCIENCE_OWNER", "PROPOSED_CONTESTED", [COURT], M("PRESENT", "CONTESTED", "MISSING", "MISSING", "MISSING", "MISSING")),
    N("SCIENCE_LEONTIEV", "L3", "SCIENTIFIC_ALTERNATIVE", "Leontiev: object-directed activity, motive, action and operation", "A performed action is not proof of a new motive or personality trait. Preserve object/goal/operation and historical activity separately.", "SOROK_ORIGINAL_SCIENCE_OWNER", "RIVAL_EXPLANATION_OPEN", [W1B_DOC], M("PRESENT", "CONTESTED", "NOT_REQUIRED_WITH_REASON", "MISSING", "MISSING", "MISSING")),
    N("SCIENCE_LAHIRE", "L3", "SCIENTIFIC_ALTERNATIVE", "Lahire: plural actor, context-conditioned dispositions", "Past incorporation does not entail global manifestation; context can select or inhibit dispositions.", "SOROK_ORIGINAL_SCIENCE_OWNER", "RIVAL_EXPLANATION_OPEN", [W1B_DOC], M("PRESENT", "CONTESTED", "NOT_REQUIRED_WITH_REASON", "MISSING", "MISSING", "MISSING")),
    N("SCIENCE_ARCHER", "L3", "SCIENTIFIC_ALTERNATIVE", "Archer: reflexive deliberation over concerns", "Internal deliberation may causally mediate projects rather than merely rationalize after action.", "SOROK_ORIGINAL_SCIENCE_OWNER", "RIVAL_EXPLANATION_OPEN", [W1B_DOC], M("PRESENT", "CONTESTED", "NOT_REQUIRED_WITH_REASON", "MISSING", "MISSING", "MISSING")),
    N("SCIENCE_SEVE", "L3", "SCIENTIFIC_ALTERNATIVE", "Seve: historically ordered acts and capacities", "Personality as a system of social relations between acts; use-time and biography shape what is reproducible.", "SOROK_ORIGINAL_SCIENCE_OWNER", "RIVAL_EXPLANATION_OPEN", [W1B_DOC], M("PRESENT", "CONTESTED", "NOT_REQUIRED_WITH_REASON", "MISSING", "MISSING", "MISSING")),
    N("CAN011_AUTHORITY", "L3", "SCIENCE_AUTHORITY", "CAN-011 V3 developmental middle state", "Three registered state kinds (MEDIATOR, TENSION, PRACTICE); generic operations CREATE/REINFORCE/WEAKEN/TRANSFORM/SET_DORMANT/REACTIVATE/END/NO_CHANGE; operation names supply no content.", "CAN011_OWNER", "AUTHORITY_1_0_0_REGISTERED", [CAN11], M("PRESENT", "PARTIAL", "PRESENT", "MISSING", "MISSING", "MISSING")),
    N("CAN008_AUTHORITY", "L3", "SCIENCE_AUTHORITY", "CAN-008 V3 pressure-flow response", "Separates admitted precipitating event, receivability, uptake appraisal, situated recruitment, immediate response and separately authorized target effects.", "CAN008_OWNER", "AUTHORITY_REGISTERED", [CAN8], M("PRESENT", "PARTIAL", "PRESENT", "MISSING", "MISSING", "MISSING")),
    N("CAN011_RULE_T_MISSING", "L2", "MISSING_FUNCTION", "Positive practice-acquisition Rule T is not issued", "Generic transition forms and a sourcefree T=NO_CHANGE exist. No positive acquisition/longitudinal discriminator is issued. A missing Rule T is not an evaluated NO_CHANGE.", "CAN011_OWNER", "MISSING_RULE", [CAN11, P1S35], M("PRESENT", "MISSING", "PARTIAL", "MISSING", "MISSING", "MISSING")),
    N("FLOURISHING_EVALUATOR_MISSING", "L2", "MISSING_FUNCTION", "No defensible flourishing evaluator", "Court 10 supplies plural candidate dimensions and counterexamples, but no adopted measurement, causal attribution or human evaluation. Increased attachment with reduced agency is not automatically benefit.", "SOROK_ORIGINAL_SCIENCE_OWNER / SOROK_ALPHA_OWNER", "MISSING", [COURT, DECISIONS], M("PRESENT", "CONTESTED", "MISSING", "MISSING", "MISSING", "MISSING")),
]

NODES += [
    N("V3_RUN_ONE_YEAR", "L4", "HISTORICAL_IMPLEMENTATION", "Historical V3 yearly_step.run_one_year", "Actual historical external Python function; old numeric defaults, pseudo-random events and type inference are not current native science.", "ORIGINAL_V3_SOURCE_OWNER", "HISTORICAL_EXTERNAL_SOURCE", [V3YEAR, W1C_DOC], M("PRESENT", "SUPERSEDED", "HISTORICAL", "HISTORICAL", "HISTORICAL", "MISSING")),
    N("V3_PERSONA_SHEET", "L4", "HISTORICAL_IMPLEMENTATION", "Historical V3 persona sheet compiler", "Actual historical bridge to V2 chat. Concealed biography/voice input conflicts with later prompt-access and claim-ceiling rules.", "ORIGINAL_V3_SOURCE_OWNER", "HISTORICAL_EXTERNAL_SOURCE", [V3SHEET], M("PRESENT", "SUPERSEDED", "HISTORICAL", "HISTORICAL", "HISTORICAL", "MISSING")),
    N("V3_EXTERNAL_SIMULATION", "L4", "HISTORICAL_CONSUMER", "Historical external server simulation.run_simulation_for_session", "Actual historical external caller of run_one_year and build_persona_sheet.", "ORIGINAL_V3_SOURCE_OWNER", "HISTORICAL_EXTERNAL_CONSUMER", [V3SIM], M("PRESENT", "HISTORICAL", "HISTORICAL", "HISTORICAL", "HISTORICAL", "MISSING")),
    N("V3_SERVER_TURN", "L4", "HISTORICAL_CONSUMER", "Historical server chat_turn", "Historical server turn loads persona sheet through V2 loader.", "ORIGINAL_V3_SOURCE_OWNER", "HISTORICAL_EXTERNAL_CONSUMER", [V3TURN], M("PRESENT", "HISTORICAL", "HISTORICAL", "HISTORICAL", "HISTORICAL", "MISSING")),
    N("V3_V2_LOADER", "L4", "HISTORICAL_CONSUMER", "Historical V2 run_conversation_chat loader", "Historical V2 persona-sheet loader. Not evidence of a current PRE-MAIN importer.", "ORIGINAL_V3_SOURCE_OWNER", "HISTORICAL_EXTERNAL_CONSUMER", [V3LOAD], M("PRESENT", "HISTORICAL", "HISTORICAL", "HISTORICAL", "HISTORICAL", "MISSING")),
    N("V3_EXTERNAL_MEMBER_HASH_MISMATCH", "L4", "EVIDENCE_INCONSISTENCY", "Local external V3 copy is not the W1-C member cut", "The historical call chain was read from a local external copy, but current witness availability is derived per node; recorded SHA-256 values differ from W1-C member hashes. Container identity and member identity remain separate unresolved evidence.", "ORIGINAL_V3_SOURCE_OWNER", "EVIDENCE_MISMATCH_UNRESOLVED", [V3YEAR, W1C_DOC], M("PRESENT", "UNRESOLVED", "UNREAD", "UNKNOWN", "MISSING", "MISSING")),
    N("M6_ACTOR_SAFE", "L4", "CURRENT_BARRIER", "PRE-MAIN M6 actor-safe expression ceiling", "M6 owns no positive situated phenomenology. require_situated_expression_owner raises M6NamedAuthorityRequired; the renderer positive plan is BLOCKED_NAMED_AUTHORITY_REQUIRED.", "C11_OWNER", "BLOCKED_NAMED_AUTHORITY_REQUIRED", [M6], M("PRESENT", "PRESENT", "PRESENT", "TESTED_NEGATIVE", "MISSING", "NOT_REQUIRED_WITH_REASON")),
    N("GT0_END_TO_END", "L4", "CURRENT_NEGATIVE_CONSUMER", "PRE-MAIN GT0 end-to-end conservation", "GT0 requires a BLOCKED terminal, no permission widening, no V3 mutation and no fabricated V2 actor claim. It is a tested negative boundary, not a person consumer.", "C11_OWNER", "TESTED_NEGATIVE", [GT0], M("PRESENT", "PRESENT", "PRESENT", "TESTED_NEGATIVE", "PRESENT_NEGATIVE", "NOT_REQUIRED_WITH_REASON")),
    N("CURRENT_V3_IMPORTER_MISSING", "L4", "MISSING_EDGE", "No verified current V3 person importer", "Historical external V3 to V2 does not establish a current PRE-MAIN V3 person import. M6/GT0 block a positive actor path.", "ORIGINAL_V3_SOURCE_OWNER / C11_OWNER", "MISSING", [W1C_DOC, M6], M("PRESENT", "MISSING", "MISSING", "MISSING", "MISSING", "MISSING")),
    N("P1_RETURN", "L4", "RETURNED_ARTIFACT", "P1 material-historical person sourcefree return", "Four contrasting lives over the same B source, A access/no-access, refusal and omission/performance; TEST_ONLY, not native, not independently accepted.", "P1_OWNER", "TEST_ONLY_SOURCEFREE_NOT_NATIVE", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_CONSUMER_CODE", "L4", "IMPLEMENTATION", "P1 candidate/p1_consumer.py", "Actual runner constructs the four contrasting lives and invokes JOIN/R31E and S35 adapters.", "P1_OWNER", "AUTHOR_TESTED_SOURCEFREE", [P1CODE], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LIFE_A_SHARE_ACCESS", "L4", "TEST_TRAJECTORY", "P1 life A: B shares, A has access, A requests, later HELP_ACCEPT", "B SHARE_TOOL hash 16f1...; A access admitted by fixture; A REQUEST_TOOL; later HELP_ACCEPT.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LIFE_B_SHARE_NO_ACCESS", "L4", "TEST_TRAJECTORY", "P1 life B: identical B share, A access denied, no invented help response", "Same B share; A access denied; no target; no A response invented.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LIFE_C_REFUSE", "L4", "TEST_TRAJECTORY", "P1 life C: B refuses, A refuses, later HELP_REFUSE", "B REFUSE_TOOL hash 3e00...; targetless NO_CHANGE; later HELP_REFUSE; never help accept.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LIFE_D_OMIT", "L4", "TEST_TRAJECTORY", "P1 life D omit: B shares, A omits inspection, later HELP_ACCEPT", "Identical SHARE_TOOL; A no E2; one tool; later HELP_ACCEPT.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LIFE_D_PERFORM", "L4", "TEST_TRAJECTORY", "P1 life D perform: B shares, A inspects and exhausts tool, later HELP_REFUSE", "Identical SHARE_TOOL; A ATTEND_OBJECT inspection; zero tools; later HELP_REFUSE.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_SAME_SPEECH_DIFFERENT_CAUSE", "L4", "CAUSAL_DISTINCTION", "Same HELP_REFUSE speech, different material causes", "C refusal and D performed inspection both end HELP_REFUSE. The speech label does not identify B refusal versus A's own consumption.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_A_ACCESS_PATH", "L4", "TEST_PREREQUISITE", "P1 A access path (test-only)", "Actor E1 access was admitted by fixture choice. It is not a validated access-selection algorithm.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_B_MATERIAL_SOURCE", "L4", "TEST_PREREQUISITE", "P1 independent B material source (test-only)", "Actual B SHARE/REFUSE source hashes are sealed before C8. This is sourcefree, not a native B/Pyat grant.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_LATER_HELP_CONSUMER", "L4", "TEST_CONSUMER", "P1 later first-neighbor help consumer (test-only)", "R31ESession.do_help consumes the C9/C12 target and material stock. It is deterministic template expression, not a live language model.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_NO_ACCESS_CONSUMER", "L4", "TEST_CONSUMER", "P1 no-access targetless consumer (test-only)", "B share remains in a targetless C12 root; no A response is invented.", "P1_OWNER", "TEST_ONLY", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("P1_TEST_ONLY_GRADE", "L4", "GRADE_CONSTRAINT", "P1 remains TEST_ONLY/non-native", "Author tests and cold reads are not independent acceptance, native C9/C12, original Rule A/T or human A5.", "P1_OWNER", "TEST_ONLY_SOURCEFREE_NOT_NATIVE", [P1DOC], M("PRESENT", "TEST_ONLY", "SOURCEFREE_PARTIAL", "AUTHOR_TESTED", "TEST_ONLY", "MISSING")),
    N("JOIN_E_7BF", "L4", "REVIEWED_IMPLEMENTATION", "JOIN-E 7bf2da3 exact fork-atomicity subject", "Exact sourcefree subject reviewed by JOIN-V. Acceptance is scoped to fork atomicity/shared lineage and same-root cold behavior; native C9/C12 remains held.", "JOIN_E_OWNER", "INDEPENDENT_ACCEPT_SCOPED", [JOINV], M("PRESENT", "TEST_ONLY", "SCOPED", "INDEPENDENTLY_TESTED_SCOPED", "TEST_ONLY", "MISSING")),
    N("JOIN_V_SCOPE_ACCEPTANCE", "L4", "SCOPED_ACCEPTANCE", "JOIN-V scoped acceptance of 7bf", "Acceptance coexists with native C9/C12 and external-anchor holds.", "JOIN_V_REVIEWER", "ACCEPT_SCOPED", [JOINV], M("PRESENT", "TEST_ONLY", "SCOPED", "INDEPENDENTLY_TESTED_SCOPED", "TEST_ONLY", "MISSING")),
    N("JOIN_C9_HOLD", "L4", "NATIVE_HOLD", "C9 actor metadata/source held", "C9_SOURCE_MISSING and native C9 actor owner remain held.", "C9_C12_OWNER", "HELD", [RRIFDOC], M("PRESENT", "TEST_ONLY", "HELD", "HELD", "HELD", "MISSING")),
    N("JOIN_C12_HOLD", "L4", "NATIVE_HOLD", "C12 external anchor and compatible reader held", "Local hashes are not external custody; C9/C12 cut compatibility and owner migration remain unresolved.", "C9_C12_OWNER", "HELD", [RRIFDOC], M("PRESENT", "TEST_ONLY", "HELD", "HELD", "HELD", "MISSING")),
    N("RRIF_F1_DEFECT", "L4", "INDEPENDENT_NEGATIVE", "RRIF F1 nonvendor-byte verification defect", "F1 verified only 444 vendor blobs and 15 path names, not nonvendor bytes; a comment appended to joined/session.py passed.", "RRIF_REVIEWER", "REVISE_ONE_EXACT_PACKET_DEFECT", [RRIFDOC], M("PRESENT", "PRESENT", "PRESENT", "INDEPENDENT_NEGATIVE", "PRESENT_NEGATIVE", "NOT_REQUIRED_WITH_REASON")),
    N("RRIF_F2_REPAIR", "L4", "REPAIR", "RRIF F2 all-459-blob gate repair", "Corrected verifier checks all 459 R2 blobs. Nonvendor tamper fails and exact restore passes.", "RRIF_F2_OWNER", "AUTHOR_TESTED_SOURCEFREE", [RRIFDOC], M("PRESENT", "PRESENT", "PRESENT", "AUTHOR_TESTED", "PARTIAL", "MISSING")),
    N("RRIF_F2_FIRST_CONSUMER", "L4", "PARTIAL_CONSUMER", "RRIF F2 first consumer PARTIAL", "20 R2 + 9 R3 + 6 E tests and a clean stage; first consumer terminal is PASS_PARTIAL_SAME_ROOT_C9_C12 with C9 actor owner held and CP-A5 separate root.", "RRIF_F2_OWNER", "PASS_PARTIAL", [RRIFDOC], M("PRESENT", "PRESENT", "PRESENT", "AUTHOR_TESTED", "PARTIAL", "MISSING")),
    N("RRIF_NATIVE_HOLD", "L4", "NATIVE_HOLD", "RRIF native adoption and anchor held", "No PRE-MAIN merge, production adoption, owner signature, native grant or actor/CP-A5 science claim.", "C9_C12_OWNER", "HELD", [RRIFDOC], M("PRESENT", "TEST_ONLY", "HELD", "HELD", "HELD", "MISSING")),
]

for _node in NODES:
    if _node["id"] in {"JOIN_E_7BF", "JOIN_V_SCOPE_ACCEPTANCE"}:
        _node["subject_sha"] = "7bf2da302996491ddf34b9a039fea47ac982d135"
        _node["acceptance_binding"] = "JOIN_V_EXISTING_RECORD_AT_EXACT_SUBJECT"

NODES += [
    N("W1_A_RETURN", "L4", "RETURNED_ARTIFACT", "W1-A vision/Astra return at e7787d7", "Real independent documentary return. Candidate evidence, not owner adoption.", "W1_A_RESEARCHER", "RETURNED_CANDIDATE_EVIDENCE", [W1A_DOC], M("PRESENT", "PRESENT", "PROPOSED", "RETURNED", "CANDIDATE", "MISSING")),
    N("W1_B_RETURN", "L4", "RETURNED_ARTIFACT", "W1-B developmental science return at 5ab447a", "Real independent documentary return. Rival explanations preserved; no new psychological law.", "W1_B_RESEARCHER", "RETURNED_CANDIDATE_EVIDENCE", [W1B_DOC], M("PRESENT", "CONTESTED", "PROPOSED", "RETURNED", "CANDIDATE", "MISSING")),
    N("W1_C_RETURN", "L4", "RETURNED_ARTIFACT", "W1-C original/Neo engineering return at 12433b8", "Real independent documentary return. Historical external code and current barriers distinguished.", "W1_C_RESEARCHER", "RETURNED_CANDIDATE_EVIDENCE", [W1C_DOC], M("PRESENT", "PRESENT", "PROPOSED", "RETURNED", "CANDIDATE", "MISSING")),
    N("W1_D_RETURN", "L4", "RETURNED_ARTIFACT", "W1-D history/work-control return at 950ace6", "Real independent documentary return. Historical closures, owner powers and controller observed effort.", "W1_D_RESEARCHER", "RETURNED_CANDIDATE_EVIDENCE", [W1D_DOC], M("PRESENT", "PRESENT", "PROPOSED", "RETURNED", "CANDIDATE", "MISSING")),
    N("W1_E_RETURN", "L4", "RETURNED_ARTIFACT", "W1-E living-reference architecture return at a64ff78", "Real independent documentary return. Recommends evolving O-LIVE after trust repair.", "W1_E_RESEARCHER", "RETURNED_CANDIDATE_EVIDENCE", [W1E_DOC], M("PRESENT", "PRESENT", "PROPOSED", "RETURNED", "CANDIDATE", "MISSING")),
    N("SOROK_101_OUTWARD_OCCURRENCE", "L4", "ARCHITECTURE_SEAM", "101 objective actor/world outward occurrence", "Full causal person/world state must produce an exact observable occurrence before the user-specific phenomenal filter.", "C11_OWNER / V2_OWNER", "PROPOSED_NO_IMPLEMENTATION", [ALPHA101], M("PRESENT", "PROPOSED", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("SOROK_101_USER_PHENOMENAL", "L4", "ARCHITECTURE_SEAM", "101 user phenomenal access", "User attention, recognition and prior knowledge may select or lexicalize an already existing occurrence. They may not enter its causal production.", "C11_OWNER / V2_OWNER", "PROPOSED_NO_IMPLEMENTATION", [ALPHA101], M("PRESENT", "PROPOSED", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("SOROK_101_HIDDEN_INTERIORITY", "L4", "CONSTRAINT", "101 hidden interiority must not cross the phenomenal membrane", "Hidden motive, model-of-user and unobserved fact cannot become user-visible merely because the system knows them.", "C11_OWNER / V2_OWNER", "PROPOSED_NO_IMPLEMENTATION", [ALPHA101], M("PRESENT", "PRESENT", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("SOROK_101_TWO_CALL_PROPOSAL", "L4", "ARCHITECTURE_ALTERNATIVE", "101 normal live turn target: two model calls", "DeepSeek-class transduction x1 + Claude-class actor realization x1. Brand names are placeholders; additional model calls are exceptional.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "PROPOSED", [CALLS101], M("PRESENT", "PROPOSED", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("SOROK_101_BATCHING_ALT", "L4", "ARCHITECTURE_ALTERNATIVE", "Alternative: batching or iterative appellate rendering", "Different call-count/batching proposals preserved at their actual scopes; iterative review loops are not normal architecture.", "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER", "PROPOSED_SCOPED_ALTERNATIVE", [CALLS101], M("PRESENT", "PROPOSED", "PROPOSED", "MISSING", "MISSING", "MISSING")),
    N("CONTROLLER_R63_QUEUE", "L5", "WORK_OBSERVATION", "Controller R63 queued High", "Queue accepted gpt-6.1-sol/high, message 01a16c7d...", "CONTROLLER_OWNER", "QUEUED_HIGH", [S("409f6c78e9d9ed77377c778476b2c23e9eb15e8a", "INTEGRATION/INTELLIGENCE_ROUTING/ROUTING_HOLD.json", "070e239e6717d5d93f0aad39f5043bb04a8f2999", "queue.requested_setting effort=high; queue.message_id 01a16c7d-af19-7061-bd63-ea0fd139fb27", 1, 40, "VERIFIED_GITHUB_API_READ", repository="maidiu/rawlsing-controller")], M("PRESENT", "PRESENT", "PRESENT", "QUEUED", "NOT_OBSERVED", "NOT_REQUIRED_WITH_REASON")),
    N("CONTROLLER_R63_OBSERVED", "L5", "WORK_OBSERVATION", "Controller R63 observed same-HQ turn at Low", "Observed turn 01a16c7e... recorded model gpt-6.1-sol effort=low despite assistant marker. Marker text is not proof.", "CONTROLLER_OWNER", "OBSERVED_LOW", [S("409f6c78e9d9ed77377c778476b2c23e9eb15e8a", "INTEGRATION/INTELLIGENCE_ROUTING/ROUTING_HOLD.json", "070e239e6717d5d93f0aad39f5043bb04a8f2999", "observed.effort=low; observation.code INTELLIGENCE_SETTING_NOT_APPLIED; no_further_queue=true", 20, 80, "VERIFIED_GITHUB_API_READ", repository="maidiu/rawlsing-controller")], M("PRESENT", "PRESENT", "PRESENT", "OBSERVED_NEGATIVE", "OBSERVED_LOW", "NOT_REQUIRED_WITH_REASON")),
    N("CONTROLLER_R63_HOLD", "L5", "WORK_HOLD", "Controller routing HOLD", "Automatic same-HQ settings routing is NOT_ENABLED and NOT_PROVEN. No automatic retry or fallback transport.", "CONTROLLER_OWNER", "HELD", [S("409f6c78e9d9ed77377c778476b2c23e9eb15e8a", "INTEGRATION/INTELLIGENCE_ROUTING/RETURN.md", "07c01868b7ff786b9df1853d777603ef2d1eb4fe", "Result: BLOCKED / HOLD at the effective-settings transport boundary. No automatic capability is claimed.", 1, 20, "VERIFIED_GITHUB_API_READ", repository="maidiu/rawlsing-controller")], M("PRESENT", "PRESENT", "PRESENT", "HELD", "HELD", "MISSING")),
    N("LIBRARY_LATEST_20261031", "L5", "CONTINUITY_SNAPSHOT", "Native Library LATEST: 2026.10.31.17.40", "Dated native Library continuity snapshot reported by W1-D. No fresh Library read in this flight; not live worker state.", "SOROK_HQ", "REPORTED_NOT_ACCESSED_NOW", [S(W1D, "WORKER_RETURNS/PROGRAMMA_SOROK_W1_D_HISTORY_WORK_CONTROL_R1/00_HISTORICAL_ORGANIZATIONAL_FINDINGS_AND_MINIMUM_AGENT_PROTOCOL.md", "05204c9c6a18fb8c1e7e599f09cee767aea54ffc", "Native Library /Rawlsing/SOROK HQ/LATEST.json points to verified immutable 2026.10.31.17.40 snapshot; prior 2026.10.30.17.49.", 90, 120, "RETURN_REPORT_FULL_READ")], M("PRESENT", "PRESENT", "REPORTED", "REPORTED", "NOT_ACCESSED_NOW", "MISSING")),
    N("PREMAIN_PROGRESS_MD", "L5", "SOURCE_CURRENTNESS", "PRE-MAIN CURRENT_PROGRESS.md revision 36", "MD reports revision36 and two published-not-launched work orders; no session/process inferred.", "PREMAIN_RECEIVING_OWNER", "REVISION_36", [PROGRESS_MD], M("PRESENT", "PRESENT", "PRESENT", "PRESENT", "NOT_RUNNING", "MISSING")),
    N("PREMAIN_PROGRESS_JSON", "L5", "SOURCE_CURRENTNESS", "PRE-MAIN CURRENT_PROGRESS.json revision 35", "JSON reports revision 35 at the same cut as MD revision 36. Stale cross-cut, not silently overwritten.", "PREMAIN_RECEIVING_OWNER", "REVISION_35", [PROGRESS_JSON], M("PRESENT", "PRESENT", "PRESENT", "PRESENT", "NOT_RUNNING", "MISSING")),
    N("WORKER_BRANCH_READY", "L5", "WORK_STATE", "Worker branch READY/PUBLISHED", "A published branch or READY status is not a running process.", "SOROK_HQ", "PUBLISHED_NOT_LAUNCHED", [PROGRESS_MD], M("PRESENT", "PRESENT", "PRESENT", "NOT_RUNNING", "NOT_RUNNING", "NOT_REQUIRED_WITH_REASON")),
    N("WORKER_RUNNING_UNKNOWN", "L5", "WORK_STATE", "Live worker capacity UNKNOWN", "No verified process/session/lease was observed. Branch existence is not evidence of running.", "SOROK_HQ", "UNKNOWN", [PROGRESS_MD], M("PRESENT", "PRESENT", "UNKNOWN", "UNKNOWN", "UNKNOWN", "MISSING")),
    N("NO_AUTO_REDISPATCH", "L5", "WORK_CONSTRAINT", "No automatic redispatch from READY or queued state", "A new HQ must check live Git, returns and dated Library continuity before reissuing work. Queued High did not become observed High.", "SOROK_HQ", "CONSTRAINT", [W1D_DOC], M("PRESENT", "PRESENT", "PRESENT", "PRESENT", "CONSTRAINT", "NOT_REQUIRED_WITH_REASON")),
    N("JOIN_V_4387", "L4", "INDEPENDENT_REVIEW_RECORD", "JOIN-V independent hostile review at 4387dc8", "Separate reviewer identity and exact reviewed subject. It does not transfer to other versions/roots or native authority.", "JOIN_V_REVIEWER", "ACCEPT_SCOPED", [S(JOIN, "WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md", "52dfc715bed3ef14cc3dc4639132c409c4e99712", "ROLE: independent hostile engineering reviewer; not JOIN-E. REVIEWED FORK-ATOMICITY CUT 7bf2da30. EXACT COMMISSION SEAL 2b8d3067. independent accession 3de08102. HQ appointment; effective owner 6456fc57. ACCEPT_SCOPED.", 1, 45, "FULL_TEXT_READ")], M("PRESENT", "TEST_ONLY", "SCOPED", "INDEPENDENTLY_TESTED_SCOPED", "TEST_ONLY", "MISSING"), acceptance={
        "reviewer_principal": "JOIN-V",
        "reviewer_role": "INDEPENDENT_HOSTILE_ENGINEERING_REVIEWER",
        "author_principal": "JOIN_E_OWNER",
        "subject_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
        "assertion": "fork atomicity/shared lineage exact scope",
        "scope": ["JOIN_E_7BF"],
        "appointment_ref": "2b8d3067d894941c21ec7fd23d1f883f51b15026",
        "record_ref": "4387dc818a96fda2d5271672505fbd9da1059703:WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md",
        "verdict": "ACCEPT_SCOPED",
        "limitations": ["not native C9/C12", "not PRE-MAIN adoption", "does not migrate across versions/roots"],
    }),
]


def E(frm, to, relation, dependency, grade, refs=None):
    return {
        "from": frm,
        "to": to,
        "relation": relation,
        "dependency": dependency,
        "grade": grade,
        "source_refs": refs or [],
    }


EDGES = [
    E("PURPOSE_UNCHOSEN_NEIGHBOR", "SOROK_100_ALPHA", "constrained_by_unchosen_neighbor", "CONSTRAINT", "SOURCE_DEFINED_CONSTRAINT", [CHARTER, ALPHA100]),
    E("SOROK_100_ALPHA", "SOROK_101_BINDING", "binding_surface_constrained_by_alpha", "CONSTRAINT", "SOURCE_DEFINED_CONSTRAINT", [ALPHA100, ALPHA101]),
    E("SOROK_100_ALPHA", "ASTRA_B_SCENE", "experiential_projection_b_scene", "HYPOTHESIS", "RESEARCH_PROJECTION", [ALPHA100, STRATA]),
    E("SOROK_100_ALPHA", "ASTRA_D_LONGITUDINAL", "experiential_projection_d_longitudinal", "HYPOTHESIS", "RESEARCH_PROJECTION", [ALPHA100, STRATA]),
    E("ASTRA_B_SCENE", "SOROK_100_ALPHA", "supports_bounded_alpha_experience", "EVIDENCE", "RESEARCH_EVIDENCE", [STRATA]),
    E("ASTRA_D_LONGITUDINAL", "SOROK_100_ALPHA", "supports_bounded_alpha_experience", "EVIDENCE", "RESEARCH_EVIDENCE", [STRATA]),
    E("ASTRA_NEGATIVE_CONTROLS", "SOROK_100_ALPHA", "rejects_extractive_design_space", "CONSTRAINT", "REVIEWED_NEGATIVE", [NEGATIVE]),
    E("P1_RETURN", "SOROK_100_ALPHA", "sourcefree_test_only_realization", "TEST_ONLY", "TEST_ONLY_SOURCEFREE", [P1DOC]),
    E("P1_CONSUMER_CODE", "P1_RETURN", "implements_test_trajectories", "EVIDENCE", "AUTHOR_TESTED", [P1CODE]),
    E("P1_LATER_HELP_CONSUMER", "P1_CONSUMER_CODE", "first_consumed_by_runner", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_RETURN", "CAN011_RULE_T_MISSING", "missing_native_positive_rule_t", "MISSING_EDGE", "MISSING", [CAN11, P1S35]),
    E("P1_RETURN", "A5", "human_validation_required_by", "CONSTRAINT", "NOT_RUN", [P1DOC]),
    E("SOROK_100_ALPHA", "A5", "human_validation_required_by", "CONSTRAINT", "NOT_RUN", [ALPHA100]),
    E("SOROK_101_BINDING", "SOROK_101_OUTWARD_OCCURRENCE", "requires_outward_occurrence", "CONSTRAINT", "PROPOSED", [ALPHA101]),
    E("SOROK_101_OUTWARD_OCCURRENCE", "SOROK_101_USER_PHENOMENAL", "precedes_user_phenomenal_projection", "CONSTRAINT", "PROPOSED", [ALPHA101]),
    E("SOROK_101_HIDDEN_INTERIORITY", "SOROK_101_USER_PHENOMENAL", "must_not_leak_to", "CONSTRAINT", "PROPOSED", [ALPHA101]),
    E("SOROK_101_TWO_CALL_PROPOSAL", "SOROK_101_BATCHING_ALT", "alternative_to", "ALTERNATIVE", "PROPOSED_ALTERNATIVE", [CALLS101]),
    E("SOROK_101_BINDING", "SOROK_101_TWO_CALL_PROPOSAL", "proposes_two_call_target", "EVIDENCE", "PROPOSED", [CALLS101]),
    E("SOROK_101_BINDING", "SOROK_101_BATCHING_ALT", "preserves_batching_alternative_scope", "EVIDENCE", "PROPOSED", [CALLS101]),
    E("Q_GAME_001", "D002_SMALLEST_MOMENT", "closed_for_alpha_by", "EVIDENCE", "HISTORICAL_CLOSURE", [QUESTIONS, D002]),
    E("Q_ACTION_001", "D002_SMALLEST_MOMENT", "closed_for_alpha_by", "EVIDENCE", "HISTORICAL_CLOSURE", [QUESTIONS, D002]),
    E("Q_GAME_001", "Q_ACTION_001", "historical_dependency", "HISTORICAL", "HISTORICAL", [QUESTIONS]),
    E("Q_HEALTH_001", "COURT10_FLOURISHING", "theory_contested_by", "EVIDENCE", "CONTESTED", [COURT]),
    E("Q_HEALTH_001", "SPD_0003", "constrained_by_distinctions", "CONSTRAINT", "PROVISIONAL_LAW", [DECISIONS]),
    E("Q_HEALTH_001", "Q_ONTO_001", "depends_on_relational_ontology", "HISTORICAL", "OPEN", [QUESTIONS]),
    E("COURT10_FLOURISHING", "FLOURISHING_ALT_PLURAL", "proposes_plural_dimensions", "EVIDENCE", "PROPOSED", [COURT]),
    E("FLOURISHING_ALT_ATTACHMENT", "Q_HEALTH_001", "contradicts_flourishing_measure", "CONTRADICTS", "REVIEWED_NEGATIVE", [COURT]),
    E("FLOURISHING_ALT_RETENTION", "Q_HEALTH_001", "contradicts_flourishing_measure", "CONTRADICTS", "REVIEWED_NEGATIVE", [MAP]),
    E("Q_HEALTH_001", "S5", "addresses_workstream_s5", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP, QUESTIONS]),
    E("Q_HEALTH_001", "S13", "incentive_constraint", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP]),
    E("FLOURISHING_ALT_RETENTION", "S13", "incentive_constraint", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP]),
    E("Q_HEALTH_001", "S14", "privacy_abuse_constraint", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP]),
    E("Q_HEALTH_001", "S15", "human_evaluation_required", "CONSTRAINT", "NOT_RUN", [MAP]),
    E("Q_HEALTH_001", "FLOURISHING_EVALUATOR_MISSING", "missing_evaluation_contract", "MISSING_EDGE", "MISSING", [COURT]),
    E("S13", "FLOURISHING_EVALUATOR_MISSING", "incentive_adverse_case_required", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP]),
    E("S14", "FLOURISHING_EVALUATOR_MISSING", "privacy_abuse_case_required", "CONSTRAINT", "PRODUCT_OBLIGATION", [MAP]),
    E("FLOURISHING_EVALUATOR_MISSING", "A5", "human_validation_required", "MISSING_EDGE", "NOT_RUN", [COURT]),
    E("S5", "A5", "human_validation_required", "CONSTRAINT", "NOT_RUN", [MAP]),
    E("COURT10_FLOURISHING", "S5", "theory_for_s5", "EVIDENCE", "CONTESTED", [COURT]),
    E("SCIENCE_LEONTIEV", "CAN011_RULE_T_MISSING", "alternative_explanation_for_durable_change", "ALTERNATIVE", "CONTESTED", [W1B_DOC]),
    E("SCIENCE_LAHIRE", "CAN011_RULE_T_MISSING", "alternative_explanation_for_durable_change", "ALTERNATIVE", "CONTESTED", [W1B_DOC]),
    E("SCIENCE_ARCHER", "CAN011_RULE_T_MISSING", "alternative_explanation_for_durable_change", "ALTERNATIVE", "CONTESTED", [W1B_DOC]),
    E("SCIENCE_SEVE", "CAN011_RULE_T_MISSING", "alternative_explanation_for_durable_change", "ALTERNATIVE", "CONTESTED", [W1B_DOC]),
    E("CAN011_AUTHORITY", "CAN011_RULE_T_MISSING", "generic_contract_without_positive_rule", "EVIDENCE", "MISSING_RULE", [CAN11]),
    E("CAN008_AUTHORITY", "CAN011_RULE_T_MISSING", "separate_response_and_durable_change_owners", "CONSTRAINT", "SOURCE_DEFINED", [CAN8, CAN11]),
    E("V3_EXTERNAL_SIMULATION", "V3_RUN_ONE_YEAR", "historically_calls", "HISTORICAL", "HISTORICAL_EXTERNAL", [V3SIM, W1C_DOC]),
    E("V3_EXTERNAL_SIMULATION", "V3_PERSONA_SHEET", "historically_calls", "HISTORICAL", "HISTORICAL_EXTERNAL", [V3SIM, W1C_DOC]),
    E("V3_RUN_ONE_YEAR", "V3_EXTERNAL_SIMULATION", "historically_called_by", "HISTORICAL", "HISTORICAL_EXTERNAL", [V3SIM]),
    E("V3_PERSONA_SHEET", "V3_SERVER_TURN", "historically_consumed_by", "HISTORICAL", "HISTORICAL_EXTERNAL", [V3SHEET, V3TURN]),
    E("V3_SERVER_TURN", "V3_V2_LOADER", "historically_calls", "HISTORICAL", "HISTORICAL_EXTERNAL", [V3TURN, V3LOAD]),
    E("V3_EXTERNAL_MEMBER_HASH_MISMATCH", "V3_RUN_ONE_YEAR", "qualifies_source_identity", "EVIDENCE", "UNRESOLVED", [V3YEAR, W1C_DOC]),
    E("V3_EXTERNAL_MEMBER_HASH_MISMATCH", "V3_PERSONA_SHEET", "qualifies_source_identity", "EVIDENCE", "UNRESOLVED", [V3SHEET]),
    E("V3_RUN_ONE_YEAR", "CURRENT_V3_IMPORTER_MISSING", "no_current_importer_found", "MISSING_EDGE", "MISSING", [W1C_DOC]),
    E("V3_PERSONA_SHEET", "CURRENT_V3_IMPORTER_MISSING", "no_current_importer_found", "MISSING_EDGE", "MISSING", [W1C_DOC]),
    E("M6_ACTOR_SAFE", "CURRENT_V3_IMPORTER_MISSING", "blocks_positive_actor_path", "CONSTRAINT", "TESTED_NEGATIVE", [M6]),
    E("GT0_END_TO_END", "CURRENT_V3_IMPORTER_MISSING", "tested_negative_boundary", "EVIDENCE", "TESTED_NEGATIVE", [GT0]),
    E("W1_C_RETURN", "V3_RUN_ONE_YEAR", "evidence_for_historical_external_route", "EVIDENCE", "RETURN_REPORT", [W1C_DOC]),
    E("P1_LIFE_A_SHARE_ACCESS", "P1_B_MATERIAL_SOURCE", "uses_same_b_share_source", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_LIFE_B_SHARE_NO_ACCESS", "P1_B_MATERIAL_SOURCE", "uses_same_b_share_source", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_LIFE_C_REFUSE", "P1_B_MATERIAL_SOURCE", "uses_b_refusal_source", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_LIFE_D_OMIT", "P1_A_ACCESS_PATH", "uses_a_omission", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_LIFE_D_PERFORM", "P1_A_ACCESS_PATH", "uses_a_performed_inspection", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_SAME_SPEECH_DIFFERENT_CAUSE", "P1_LIFE_C_REFUSE", "evidence_for_b_refusal_cause", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_SAME_SPEECH_DIFFERENT_CAUSE", "P1_LIFE_D_PERFORM", "evidence_for_a_consumption_cause", "EVIDENCE", "TEST_ONLY", [P1DOC]),
    E("P1_LATER_HELP_CONSUMER", "CAN011_RULE_T_MISSING", "pending_native_acceptance", "MISSING_EDGE", "MISSING", [P1DOC, P1S35]),
    E("P1_NO_ACCESS_CONSUMER", "CAN008_AUTHORITY", "pending_native_access_rule", "MISSING_EDGE", "MISSING", [P1DOC, CAN8]),
    E("JOIN_E_7BF", "JOIN_V_SCOPE_ACCEPTANCE", "accepted_by_exact_scope", "SCOPE_ACCEPTANCE", "ACCEPT_SCOPED", [JOINV]),
    E("JOIN_V_4387", "JOIN_E_7BF", "reviewed_exact_subject", "EVIDENCE", "INDEPENDENT_REVIEW", [JOINV]),
    E("JOIN_V_SCOPE_ACCEPTANCE", "JOIN_C9_HOLD", "coexists_with_native_c9_hold", "CONSTRAINT", "HELD", [JOINV, RRIFDOC]),
    E("JOIN_V_SCOPE_ACCEPTANCE", "JOIN_C12_HOLD", "coexists_with_native_c12_hold", "CONSTRAINT", "HELD", [JOINV, RRIFDOC]),
    E("RRIF_F1_DEFECT", "RRIF_F2_REPAIR", "repaired_by_exact_f2", "EVIDENCE", "REPAIRED", [RRIFDOC]),
    E("RRIF_F2_REPAIR", "RRIF_F2_FIRST_CONSUMER", "first_consumed_by_partial_stage", "EVIDENCE", "PARTIAL", [RRIFDOC]),
    E("RRIF_F2_FIRST_CONSUMER", "RRIF_NATIVE_HOLD", "coexists_with_native_hold", "CONSTRAINT", "HELD", [RRIFDOC]),
    E("RRIF_F2_FIRST_CONSUMER", "JOIN_C9_HOLD", "partial_blocked_by_c9_source", "CONSTRAINT", "HELD", [RRIFDOC]),
    E("RRIF_F2_FIRST_CONSUMER", "JOIN_C12_HOLD", "partial_blocked_by_c12_anchor", "CONSTRAINT", "HELD", [RRIFDOC]),
    E("P1_A_ACCESS_PATH", "P1_LATER_HELP_CONSUMER", "required_prerequisite", "REQUIRED_CAUSAL", "TEST_ONLY_PREREQUISITE", [P1DOC]),
    E("P1_B_MATERIAL_SOURCE", "P1_LATER_HELP_CONSUMER", "required_prerequisite", "REQUIRED_CAUSAL", "TEST_ONLY_PREREQUISITE", [P1DOC]),
    E("P1_B_MATERIAL_SOURCE", "P1_NO_ACCESS_CONSUMER", "required_prerequisite", "REQUIRED_CAUSAL", "TEST_ONLY_PREREQUISITE", [P1DOC]),
    E("P1_LIFE_B_SHARE_NO_ACCESS", "P1_NO_ACCESS_CONSUMER", "required_prerequisite", "REQUIRED_CAUSAL", "TEST_ONLY_PREREQUISITE", [P1DOC]),
    E("CONTROLLER_R63_QUEUE", "CONTROLLER_R63_OBSERVED", "queued_setting_not_observed", "STATUS_OBSERVATION", "OBSERVED_MISMATCH", [S("409f6c78e9d9ed77377c778476b2c23e9eb15e8a", "INTEGRATION/INTELLIGENCE_ROUTING/ROUTING_HOLD.json", "070e239e6717d5d93f0aad39f5043bb04a8f2999", "requested high; observed low; INTELLIGENCE_SETTING_NOT_APPLIED", 1, 80, "VERIFIED_GITHUB_API_READ", repository="maidiu/rawlsing-controller")]),
    E("CONTROLLER_R63_OBSERVED", "CONTROLLER_R63_HOLD", "confirms_routing_hold", "EVIDENCE", "OBSERVED_NEGATIVE", [S("409f6c78e9d9ed77377c778476b2c23e9eb15e8a", "INTEGRATION/INTELLIGENCE_ROUTING/RETURN.md", "07c01868b7ff786b9df1853d777603ef2d1eb4fe", "Result: BLOCKED / HOLD at the effective-settings transport boundary.", 1, 20, "VERIFIED_GITHUB_API_READ", repository="maidiu/rawlsing-controller")]),
    E("PREMAIN_PROGRESS_MD", "PREMAIN_PROGRESS_JSON", "stale_cross_cut_revision_36_vs_35", "STALE_CROSS_CUT", "STALE", [PROGRESS_MD, PROGRESS_JSON]),
    E("WORKER_BRANCH_READY", "WORKER_RUNNING_UNKNOWN", "not_evidence_of_running", "NOT_EVIDENCE", "UNKNOWN", [PROGRESS_MD]),
    E("LIBRARY_LATEST_20261031", "WORKER_RUNNING_UNKNOWN", "dated_continuity_not_live_capacity", "CONTINUITY", "REPORTED_NOT_ACCESSED_NOW", [W1D_DOC]),
    E("NO_AUTO_REDISPATCH", "WORKER_RUNNING_UNKNOWN", "constrains_redispatch", "CONSTRAINT", "CONSTRAINT", [W1D_DOC]),
    E("W1_D_RETURN", "CONTROLLER_R63_OBSERVED", "evidence_for_controller_observed_effort", "EVIDENCE", "RETURN_REPORT", [W1D_DOC]),
    E("W1_D_RETURN", "LIBRARY_LATEST_20261031", "reported_dated_library_continuity", "EVIDENCE", "RETURN_REPORT", [W1D_DOC]),
    E("W1_A_RETURN", "PURPOSE_UNCHOSEN_NEIGHBOR", "supports_unchosen_neighbor_and_astra_alternatives", "EVIDENCE", "RETURN_REPORT", [W1A_DOC]),
    E("W1_B_RETURN", "SCIENCE_LEONTIEV", "preserves_rival_scientific_explanation", "EVIDENCE", "RETURN_REPORT", [W1B_DOC]),
    E("W1_B_RETURN", "CAN011_RULE_T_MISSING", "evidences_missing_positive_rule", "EVIDENCE", "RETURN_REPORT", [W1B_DOC]),
    E("W1_E_RETURN", "W1_JOINT_SYNTHESIS", "supports_reuse_olive_after_repair", "EVIDENCE", "RETURN_REPORT", [W1E_DOC]),
    E("W1_JOINT_SYNTHESIS", "Q_KERNEL_001", "preserves_kernel_unresolved", "CONSTRAINT", "PROPOSED", [SYNTH_DOC]),
]


def G(gid, parent, domain, node, status, missing, evidence, alternatives, dependencies, consumer, owner, action, falsifier, blocked_by=None, actionable=True):
    return {
        "id": gid,
        "parent_obligation": parent,
        "domain": domain,
        "node": node,
        "status": status,
        "missing_stages": missing,
        "existing_evidence": evidence,
        "alternatives": alternatives,
        "dependencies": dependencies,
        "affected_consumer": consumer,
        "owner": owner,
        "smallest_useful_next_action": action,
        "falsifier": falsifier,
        "blocked_by": blocked_by or [],
        "independently_actionable": actionable,
        "hq_judgment_required": True,
    }


GAPS = [
    G("GAP-Q-HEALTH-FLOURISHING", "S5 / Q-HEALTH-001: benefit to the other independent of liking, compliance or dependency", "S5_FLOURISHING", "Q_HEALTH_001", "UNKNOWN", ["T", "E", "C", "V"], ["01_PRODUCT_CHARTER", "SPD-0003", "24_COURT10", "05_PROGRAM_MAP"], ["attachment proxy", "retention/satisfaction proxy", "plural incommensurable dimensions"], ["Q-ONTO-001", "S13", "S14", "S15"], "A5 and any future product benefit metric", "SOROK_ORIGINAL_SCIENCE_OWNER / SOROK_ALPHA_OWNER", "Adjudicate a plural flourishing rule with explicit non-collapse and a falsifiable human evaluation design; do not write a health_score.py stub.", "A model reports improved welfare because attachment rose while the actor lost agency, exit or outside relations.", actionable=True),
    G("GAP-CAN011-PRACTICE-ACQUISITION", "CAN-011 durable practice: distinguish acquired practice from opportunity, tool change, external scaffolding or evaluated NO_CHANGE", "LEARNED_PRACTICE", "CAN011_RULE_T_MISSING", "MISSING", ["T", "E", "C", "V"], ["CAN_011 AUTHORITY 1.0.0", "P1 p1_s35.py T=NO_CHANGE", "S35 nonissuing resource"], ["Leontiev activity/object", "Lahire context inhibition", "Seve act/capacity use-time", "Archer reflexive project"], ["CAN008 Rule A", "ADP actor access", "C9 actor consumer"], "native C9 later action", "CAN011_OWNER / ADP_OWNER", "Issue an exact positive acquisition rule with rival discriminators, or retain MISSING_RULE and do not score missing T as NO_CHANGE.", "A later action after a tool or opportunity change is counted as acquired practice without a positive rule or actor evidence.", actionable=True),
    G("GAP-V3-YEARLY-PERSONA-MIGRATION", "Historical yearly_step/persona_sheet: preserve historical external function while deciding current reuse", "ORIGINAL_V3_ENGINEERING", "V3_RUN_ONE_YEAR", "UNKNOWN", ["T", "A", "C", "V"], ["historical external simulation -> persona_sheet -> server turn -> V2 loader", "W1-C prior member hashes", "local external copy hashes differ"], ["port old V3 wholesale", "discard old V3", "source-grade exact sequencing/transaction patterns and require a current consumer"], ["CAN008/CAN011/ADP", "M6/V2", "original V3 source custodian"], "current user alpha or NONE", "ORIGINAL_V3_SOURCE_OWNER / C11_OWNER", "Resolve the container/member cut and name one exact current-compatible consumer before adapting any old mechanism.", "A current importer or consumer is claimed from the historical external call chain without exact source and test evidence.", actionable=True),
    G("GAP-S13-NONEXTRACTIVE-REVENUE", "S13: sell without making attachment, suffering or compulsive return the revenue engine", "ECONOMICS", "S13", "MISSING", ["T", "A", "E", "C", "V"], ["05_PROGRAM_MAP S13", "01_PRODUCT_CHARTER anti-goals"], ["subscription", "usage-based", "no-charge alpha"], ["S5 flourishing", "S14 privacy/abuse"], "business + user", "SOROK_BUSINESS_OWNER", "Specify a non-extractive price/notification/retention rule and an adverse-incentive falsifier before any monetization build.", "Revenue rises when the actor manufactures distress or the user returns compulsively.", actionable=True),
    G("GAP-S14-PRIVACY-ABUSE", "S14: consent, deletion, coercion, harassment, stalking and cross-branch boundaries", "SAFETY_PRIVACY", "S14", "MISSING", ["T", "A", "E", "C", "V"], ["05_PROGRAM_MAP S14", "01_PRODUCT_CHARTER anti-goals"], ["per-branch privacy", "abuse simulation law", "consent/deletion receipts"], ["S13", "C9/C12", "S15"], "real users and personas", "SOROK_SAFETY_OWNER", "Define a minimum abuse/consent/deletion contract with a hostile scenario and actual first consumer; do not treat storage hashes as social safety.", "A user can stalk, coerce or extract another person's history without a boundary the system enforces.", actionable=True),
    G("GAP-S11-ACCESSIBLE-ENCOUNTER-UX", "S11: encounter, opacity, time, commitment and repair without reducing people to stats", "UX_ACCESSIBILITY", "S11", "MISSING", ["T", "A", "E", "C", "V"], ["05_PROGRAM_MAP S11", "Astra A-E experience scales"], ["conversational-only", "structured action surface", "local phenomenal compositor"], ["SOROK_101_BINDING", "S15"], "alpha user", "SOROK_PRODUCT_UX_OWNER", "Design and test one accessible ordinary scene with control return and honest opacity; no fabricated connection.", "The interface needs the user to guess hidden mechanics or rewards disclosure with access.", actionable=True),
    G("GAP-A5-HUMAN-ALPHA", "S15 / A5: actual human encounter and evaluation distinct from sourcefree and native code", "HUMAN_ALPHA", "A5", "MISSING", ["C", "V"], ["100/101 alpha constraints", "P1 TEST_ONLY trajectory", "Astra P1-P3 proposals"], ["lab demo", "sourcefree reader", "actual participant study"], ["C11 native source", "C9/C12", "ethics"], "A5", "SOROK_ALPHA_OWNER", "Design a bounded consented participant study with actor-independent outcome measures and negative cases; do not infer A5 from code tests.", "A sourcefree or native code pass is presented as human validation.", actionable=False, blocked_by=["native C11 source", "C9/C12 actor", "ethics approval"]),
    G("GAP-SOROK101-PHENOMENAL-MEMBRANE", "101: separate objective actor/world occurrence from user-phenomenal access and hidden interiority", "EXPRESSION_BINDING", "SOROK_101_OUTWARD_OCCURRENCE", "PROPOSED", ["E", "C", "V"], ["101 binding surface", "M6 semantic ceiling", "GT0 tested negative"], ["two-call realizer", "batching/appellate alternative", "local phenomenal compositor"], ["C11", "V2", "M6"], "alpha user", "C11_OWNER / V2_OWNER", "Prototype the anti-mirror wall with one exact occurrence and a changed user-attention filter; measure whether the occurrence stays fixed.", "Changing user preferences changes the objective outward occurrence itself, or hidden interiority becomes user-visible without an admissible cue.", actionable=True),
    G("GAP-RRIF-F2-NATIVE-CONSUMER", "RRIF F2: exact packet integrity repaired, but native receiving consumer remains partial", "RECEIVING_CUSTODY", "RRIF_F2_FIRST_CONSUMER", "PARTIAL", ["C", "V"], ["F1 independent defect", "F2 all-459 repair", "PASS_PARTIAL_SAME_ROOT_C9_C12"], ["separate guarded adapter", "hold until native C9/C12 owner cut"], ["C9 actor source", "C12 anchor", "PRE-MAIN receiving owner"], "PRE-MAIN receiver / CP-A5", "C9_C12_OWNER / PREMAIN_RECEIVING_OWNER", "Select one compatible C9/C12 cut and external anchor; rerun the exact F2 negative/restore against the chosen cut.", "A packet integrity pass is treated as PRE-MAIN adoption or native person evidence.", actionable=True),
    G("GAP-CONTROLLER-OBSERVED-EFFORT", "Controller: queued model/effort is not observed execution", "WORK_CONTROL", "CONTROLLER_R63_OBSERVED", "REVIEWED_NEGATIVE", ["E", "C"], ["R63 ROUTING_HOLD", "observed low vs requested high", "assistant marker not proof"], ["manual dispatch", "bounded controller activation", "mechanical evidence only"], ["user launch grant", "controller identity/lease"], "HQ operator", "CONTROLLER_OWNER / SOROK_HQ", "Require an actual turn/process receipt before claiming model/effort or running state; no automatic retry.", "A queue label, branch READY, session title or assistant marker is reported as observed execution.", actionable=True),
    G("GAP-JOIN-NATIVE-C9-C12", "JOIN-V scoped acceptance: preserve exact sourcefree acceptance without migrating native C9/C12", "NATIVE_PERSON_CUSTODY", "JOIN_E_7BF", "SCOPED_ACCEPTANCE", ["C", "V"], ["JOIN-V ACCEPT_SCOPED exact 7bf", "C9_SOURCE_MISSING", "OWNER_ANCHOR_REQUIRED"], ["compatible migration", "honest unbridged hold"], ["C9/C12 owners", "external anchor"], "native person", "C9_C12_OWNER", "Keep the exact scope; open a separate owner decision for compatible writer/reader and external anchor.", "Acceptance is moved across versions or roots, or used as native C9/C12 evidence.", actionable=True),
    G("GAP-KERNEL-UNRESOLVED", "K0: no adjudicated generative kernel", "KERNEL", "Q_KERNEL_001", "UNKNOWN", ["T", "A", "V"], ["03_REAL_ALPHA_SPINE", "W1-A five rival spines", "W1-B competing science"], ["relational organism", "Astra A-H", "original V3 M40", "Neo CAN/ADP", "S0-S16"], ["S0-S16", "CAN008/CAN011/ADP"], "whole program", "SOROK_ORIGINAL_SCIENCE_OWNER", "Run a hostile derivation comparing candidate kernels against actual consumer faults; do not elect a slogan.", "A kernel is declared because it organizes documents but cannot derive or fail against a real consumer.", actionable=True),
]



