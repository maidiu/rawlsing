#!/usr/bin/env python3
"""Write BP1 authority, native-gap, M2/MP, decision-dossier and privacy receipts."""
from __future__ import annotations

import json
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
EVID = RETURN / "evidence"


def write(name, payload):
    (EVID / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main():
    matrix = {}
    p = EVID / "bp1_court_matrix.json"
    if p.is_file():
        matrix = json.loads(p.read_text())
    passport = {}
    p = EVID / "environment_passport.json"
    if p.is_file():
        passport = json.loads(p.read_text())

    holds = dict(
        schema="BP1_AUTHORITY_HOLD_REGISTER@1",
        authority_rule=("BP1 sourcefree TEST_ONLY actor/history code is not "
                        "native ADP007 actor genesis, not a person, parent, "
                        "biology, psychology, CAN008/CAN011 rule, ADP019 event, "
                        "Pyat world, C8 writer, C11 weld or production grant."),
        native_authority="NOT_GRANTED",
        holds=[
            dict(id="ADP007_ACTOR_GENESIS", status="HOLD_UNISSUED",
                 missing_function=("Native ADP007 actor genesis/activation from a "
                                   "qualified subject and source-qualified parents."),
                 owner="V3 actor developmental causality engine through ADP007; ADP015 parent/genealogy source",
                 required_receipt="ADP007 activation receipt + source/genealogy binding + actor id/clock",
                 blocked_consumer="BP1 native actor source; C12 person generation",
                 bp1_status="BP1 uses explicit TEST_ONLY fixture actors, not U2/native actor identity"),
            dict(id="ADP015_INDEPENDENT_OTHER_AND_FAMILY", status="HOLD_UNISSUED",
                 missing_function=("Source-qualified independent other/parent history "
                                   "and ADP015 relation/household occurrence."),
                 owner="ADP015 relationship/household/genealogy rule owner",
                 required_receipt="ADP015 owner-bound relation/household event and independently sourced other action",
                 blocked_consumer="C4 other history and C9 E1 counterpart",
                 bp1_status="BP1 B actor is a test-only independent ledger; no family/parent claim"),
            dict(id="ADP019_E1_OCCURRENCE", status="HOLD_UNISSUED",
                 missing_function="Actual ADP019 occurrence/admission from a world/event owner.",
                 owner="ADP019 external admission owner + C8 trusted writer",
                 required_receipt="ADP019 occurrence receipt + C8 committed event",
                 blocked_consumer="C9R E1 ingress and later E2",
                 bp1_status="BP1 uses TEST_ONLY declared event; no native occurrence"),
            dict(id="CAN008_RULE_A", status="HOLD_UNISSUED",
                 missing_function="Concrete current CAN008 RULE_A response rule for the finite practice case.",
                 owner="CAN008 R2 competent semantic issuer/currentness owner",
                 required_receipt="Rule id/version/content hash/scope/effective/revocation + issuer adoption",
                 blocked_consumer="C9R response rule lookup",
                 bp1_status="BP1 rule is TEST_ONLY_BP1_CAN008_RULE_A; not native"),
            dict(id="CAN011_RULE_T_AND_GRANT", status="HOLD_UNISSUED",
                 missing_function="Concrete CAN011 RULE_T target rule and owner-specific CREATE/NO_CHANGE/DENY grant.",
                 owner="CAN011 separate target-state jurisdiction",
                 required_receipt="Target rule body/version/hash + grant actor/scope/prestate/expiry/revocation",
                 blocked_consumer="C9R target evaluation and durable practice commit",
                 bp1_status="BP1 target rule/grant are TEST_ONLY; not native"),
            dict(id="ADP010_OEE_ENCOUNTER", status="HOLD_UNISSUED",
                 missing_function="ADP010 AVAILABLE→OPPORTUNITY→ENCOUNTER with OBL056 role acceptance.",
                 owner="ADP010/V3 OEE native issuer + ADP008 phase owner",
                 required_receipt="OBL056 accepted role/contact-independence/currentness receipt",
                 blocked_consumer="ADP019/C9 E1",
                 bp1_status="not used; installed registry is zero-positive"),
            dict(id="C8_TRUSTED_WRITER_ANCHOR", status="HOLD_UNISSUED",
                 missing_function="Exclusive writer gate + external keyed monotonic anchor + ADP019 occurrence.",
                 owner="C8 D1 writer owner / D2 external credential-anchor custodian / D3 ADP019 owner",
                 required_receipt="Keyed anchor receipt and exclusive-writer enforcement",
                 blocked_consumer="C8 journal/C9 E1/E2",
                 bp1_status="not used; BP1 evidence is sourcefree SQLite TEST_ONLY"),
            dict(id="NATIVE_E2_ACTUATOR_AND_OCCURRENCE", status="HOLD_UNISSUED",
                 missing_function="Independently performed native E2 action with owner actuator/occurrence receipt.",
                 owner="ADP019/E2 performer owner + C8 reentry",
                 required_receipt="Performed-action owner receipt with independent actuator and occurrence",
                 blocked_consumer="C10/C12 continuation",
                 bp1_status="BP1 E2 is TEST_ONLY_ACTUATOR_B/TEST_ONLY_OCCURRENCE_E2"),
            dict(id="C11_WELD_AND_C12_PERSON", status="HOLD_UNISSUED",
                 missing_function="Separate C11 physical weld and actual C12 generated person.",
                 owner="Pyat/C11 authority + native person-generation authority",
                 required_receipt="C11 weld grant and C12 person continuity admission",
                 blocked_consumer="production/PRE-MAIN",
                 bp1_status="not attempted; no native person claimed"),
        ],
        user_consultation=("Ask the competent owner once, in plain English, whether to "
                           "build or reuse each missing issuer. Record the answer; "
                           "never substitute a TEST_ONLY fixture for native authority."),
    )
    write("authority_hold_register.json", holds)

    gap = dict(
        schema="BP1_NATIVE_FUNCTIONAL_GAP@1",
        native_authority="NOT_GRANTED",
        cards=[
            dict(function="ADP007_NATIVE_ACTOR_GENESIS",
                 input="qualified ADP007 subject + source-qualified parent(s) + world/time",
                 decision="competent actor genesis/activation, sparse defaults/unknowns, no personality seed",
                 receipt="ADP007 activation receipt + source/genealogy binding",
                 consumer="BP1 native actor source → C4 ledger → C9R ingress",
                 effect="actual native actor; currently BP1 fixture actors only",
                 owner="V3 ADP007/ADP015 competent owners"),
            dict(function="ADP019_NATIVE_E1",
                 input="ADP010 encounter + independently observed other action",
                 decision="actual occurrence admission; no co-presence-only inference",
                 receipt="ADP019 occurrence receipt + C8 committed event",
                 consumer="C9R E1 event witness",
                 effect="actual public event; currently TEST_ONLY declared event",
                 owner="ADP019 + C8 D3"),
            dict(function="CAN008_CONCRETE_RULE_A",
                 input="actor history/receptivity + E1 + world/material constraints",
                 decision="one scoped response rule with alternatives/VALID_EMPTY; no trait/affect coefficients",
                 receipt="signed rule id/version/hash/scope/effective/revocation",
                 consumer="C9R response lookup",
                 effect="actual immediate response; currently TEST_ONLY rule",
                 owner="CAN008 R2 issuer"),
            dict(function="CAN011_CONCRETE_RULE_T_GRANT",
                 input="RULE_A response + before-state + performed activity + target owner",
                 decision="CREATE/NO_CHANGE/DENY for one scoped V3MS_PRACTICE target",
                 receipt="target rule + exact grant + prestate/expiry/revocation",
                 consumer="C9R target/transaction; later E2 reader",
                 effect="actual durable practice; currently TEST_ONLY target",
                 owner="CAN011 separate target owner"),
            dict(function="NATIVE_E2_PERFORMED_ACTION",
                 input="committed target state + independent actuator + occurrence",
                 decision="actual performed action after commit; plan/narration insufficient",
                 receipt="owner performed-action receipt bound to consumed state hash",
                 consumer="C10/C12 continuation",
                 effect="actual later action; BP1 E2 is TEST_ONLY",
                 owner="ADP019/E2 performer owner"),
            dict(function="C10_C11_C12",
                 input="C9 committed state + qualified world + C11 permission",
                 decision="couple actual actor/world; physically weld only under C11",
                 receipt="C10 read/C11 weld/C12 continuity receipts",
                 consumer="product person",
                 effect="actual C12 person; not attempted",
                 owner="C10/C11/C12 competent owners"),
        ],
    )
    write("native_functional_gap.json", gap)

    notrun = dict(
        schema="BP1_NOT_RUN_INVENTORY@1",
        items=[
            dict(item="native ADP007 actor genesis/activation", status="NOT_RUN_HOLD",
                 reason="no native actor source/genealogy grant"),
            dict(item="native ADP015 independent parent/other/family", status="NOT_RUN_HOLD",
                 reason="no source-qualified parent/other history"),
            dict(item="native ADP019 E1 occurrence", status="NOT_RUN_HOLD",
                 reason="no admitted occurrence/C8 writer"),
            dict(item="native CAN008 concrete RULE_A", status="NOT_RUN_HOLD",
                 reason="no concrete rule issuance"),
            dict(item="native CAN011 RULE_T/target grant", status="NOT_RUN_HOLD",
                 reason="no target-owner grant"),
            dict(item="native ADP010 OEE encounter", status="NOT_RUN_HOLD",
                 reason="OBL056 registry zero-positive"),
            dict(item="native E2 performed action", status="NOT_RUN_HOLD",
                 reason="no independent actuator/occurrence owner"),
            dict(item="C8 trusted writer/external anchor", status="NOT_RUN_HOLD",
                 reason="no D1/D2/D3 grant"),
            dict(item="C11 physical weld", status="NOT_RUN_HOLD",
                 reason="no Pyat/C11 authority"),
            dict(item="C12 native generated person", status="NOT_RUN_HOLD",
                 reason="no native person-generation authority"),
            dict(item="M2 23-event native replay", status="HOLD",
                 reason="archive grammar/owner mapping unissued; see m2_mp_holds.json"),
            dict(item="MP F_EXISTING native reuse", status="HOLD",
                 reason="no source-qualified second-parent history; see m2_mp_holds.json"),
            dict(item="original survey/respondent data", status="NOT_RUN",
                 reason="forbidden/unissued"),
            dict(item="Pyat N11/N12 native world", status="NOT_RUN_HOLD",
                 reason="Pyat authority separate"),
            dict(item="external model/API calls", status="NOT_RUN",
                 reason="local deterministic pytest/SQLite only; no paid call observed"),
        ],
        cash_quota="UNKNOWN; no paid API call observed",
    )
    write("not_run_inventory.json", notrun)

    m2mp = dict(
        schema="BP1_M2_MP_TYPED_HOLDS@1",
        m2=dict(
            status="HOLD_C4_M2",
            archive_sha256="9e0efc335e2bfc1e1d9f9bc25604af6d04578e7b6acddb31e439b6ff117a3ab7",
            event_count=23,
            observed_failure="EVENT_OWNER_IDENTITY_INVALID and MISSING_CAUSAL_PARENT; no current WORLD_MATERIAL root",
            frozen_test="test_archived_m2_can_continue_legitimate_prior_life",
            result="RED in G18 strict G16I 21/3",
            action="preserve typed coverage hold; no fabricated mother/child",
            owner="ADP015/ADP020/CAN008/CAN011 or Sorok HQ formal coverage acceptance",
        ),
        mp=dict(
            status="HOLD_C4_MP",
            counterpart_refs=["F_EXISTING", "REL_ADMITTED_F_EXISTING"],
            observed_result="SHARED_HISTORY_CONTRADICTION_HOLD; no_duplicate_actor_or_event=True",
            frozen_test="test_known_counterpart_has_positive_history_reuse_path",
            result="RED in G18 strict G16I 21/3",
            action="preserve typed coverage hold; no fabricated father/second parent",
            owner="ADP015/ADP020/CAN008/CAN011 or Sorok HQ formal coverage acceptance",
        ),
        g18_integrity=dict(
            g13_181="108 PASS / 73 RED exact 56+17",
            g16i_24="21 PASS / 3 RED strict; 2 typed holds + 1 documented legacy schedule supersession",
            do_not_revert="G18 refuses post-issuance caller-mutated payment/task schedule; source-issued variable schedule is the lawful path",
        ),
        native_authority="NOT_GRANTED",
    )
    write("m2_mp_holds.json", m2mp)

    decision = dict(
        schema="BP1_SCIENTIFIC_DECISION_REQUEST@1",
        status="FINITE_REQUEST_PREPARED__NO_SCIENTIFIC_RULE_INVENTED",
        accepted_data=dict(
            engineering=[
                "BP1 sourcefree historical actor composer and two-actor ledgers (15/15 tests)",
                "G18 source-issued material/action receipts preserved (181 108/73, G17I 14/0, G18 20/0)",
                "C9R TEST_ONLY consumer 10/10 and BP1 C4→C9 positive (committed target + later E2 ADMITTED)",
                "six same-edge BP1 source faults PASS→RED→PASS",
            ],
            scientific_test_only=[
                "two finite, materially distinct, independently sourced actor histories with distinct performed actions and unchanged shared objective facts",
                "lawful NO_CHANGE (own material exhausted) and DENY (permission absent); future-child payload refused",
            ],
            authority="TEST_ONLY only; no native actor/rule/person/biology/psychology",
        ),
        proposed_only=dict(
            rule_a="TEST_ONLY_BP1_CAN008_RULE_A (not native; exact history/receptivity predicate unresolved)",
            rule_t="TEST_ONLY_BP1_CAN011_RULE_T (not native; V3MS_PRACTICE formation predicate unresolved)",
            question=("For one finite material practice (coordinated material inspection), "
                      "does the competent CAN008/CAN011 owner adopt, revise, reject or "
                      "request evidence for the proposed response/target predicates?"),
        ),
        finite_input=dict(
            actor_sources=["TEST_ONLY_BP1_ACTOR_A (repair)", "TEST_ONLY_BP1_ACTOR_B (finishing)"],
            as_of=[207, 217],
            event="one shared joint_material_task objective with two performed G18 source-bound actions",
            history_refs="BP1 ledger PRIOR_HISTORY + PERFORMED_ACTION event ids",
            other_action="B independent G18 performed action",
            material="G18 source-issued material event with receipt",
            response_alternatives=["CREATE / undertake bounded practice", "NO_CHANGE", "DENY / VALID_EMPTY"],
            no_effect="exhausted own material → NO_CHANGE; missing permission → DENY",
            forbidden=["invented trait/affect/role coefficient", "P psychology without P source",
                       "future child/backfilled parent", "narrator as performed action",
                       "fixture registry as native grant"],
        ),
        exact_owner_decisions=[
            "CAN008 concrete RULE_A body/version/hash/scope/effective/revocation",
            "CAN011 concrete RULE_T + grant actor/prestate/expiry/revocation",
            "ADP007 actor genesis source/receipt",
            "ADP015 independent other/parent history",
            "ADP019 actual E1 occurrence + C8 writer/anchor",
            "native E2 performer/actuator/occurrence",
        ],
        decision_options=["ADOPT", "REVISE", "REJECT", "REQUEST_EVIDENCE"],
        no_self_issuance=True,
        native_authority="NOT_GRANTED",
    )
    write("scientific_decision_request.json", decision)

    privacy = dict(
        schema="BP1_SOURCE_PRIVACY_AND_LAW@1",
        original_respondent_data_used=False,
        original35_used=False,
        pyat_native_world_used=False,
        production_used=False,
        c9r_canonical_source_edited=False,
        g18_source_edited=False,
        c9ri_branch_or_tests_touched=False,
        actor_identifiers="explicit TEST_ONLY_BP1_* fixtures; not real persons",
        source_grade="SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE",
        native_grant="NOT_GRANTED",
        data_storage="local SQLite/TEST_ONLY evidence only",
        privacy_claim="none; no real respondent or person data",
        law_claim="none; source/permission holders remain the competent owners",
        note=("BP1 does not use recovered U2 identity as an actor; U2/ADP010/ADP007 "
              "native carriers are not self-issued. Native source/permission remains HOLD."),
    )
    write("source_privacy_and_law.json", privacy)

    reuse = dict(
        schema="BP1_CODE_EXISTENCE_AND_BUILD_REUSE@1",
        built=[
            "candidate/bp1/source.py — explicit sourcefree fixture actor source",
            "candidate/bp1/ledger.py — per-actor append-only ledger, own-state conservation, durable snapshot",
            "candidate/bp1/composer.py — two-actor historical lives, shared objective facts, NO_CHANGE/DENY, future firewall",
            "candidate/bp1/c9_bridge.py — actor snapshot → C9R E1 → target → later E2",
            "tests/test_bp1_actor_production.py — 15 author tests",
        ],
        reused=[
            "G18 61713eafe source-issued material/action receipts and historical frozen courts",
            "C9R 6fa29399 exact sourcefree actor/event/conditioning/rule/target/transaction/later-action code",
            "C9RI 5753d9b4 independent 28-row compatibility verdict and C9R reuse release",
        ],
        not_used=[
            "native U2 subject identity as actor (U2 is NONACTOR; no actor self-issue)",
            "native ADP007/ADP010/ADP015/ADP019 receipts (absent)",
            "CAN008/CAN011 concrete native rules (absent)",
            "Pyat N11/N12, C8 D1/D2/D3, C11 weld, production (absent/separate)",
        ],
        native_authority="NOT_GRANTED",
    )
    write("code_existence_and_reuse.json", reuse)

    delta = dict(
        schema="RAWLSING_ENVIRONMENT_PASSPORT@1",
        environment_id="local-bp1-historical-actor-shared-store-1",
        epoch_id=passport.get("time_utc", ""),
        surface="LOCAL_SHARED_STORE",
        session_alias="deepseek-harness-bp1",
        machine_alias="local-macos-shared-store",
        status="LIVE_VERIFIED",
        live_probe=dict(
            observed_at_utc=passport.get("time_utc", ""),
            marker_checked="VERIFIED",
            marker_digest="bp1:historical-actor-production",
            python=passport.get("python", "").split()[0] if passport.get("python") else "",
            pytest=passport.get("pytest", ""),
            git=passport.get("git", ""),
            filesystem="VERIFIED",
            connector="UNKNOWN",
            notes="isolated linked worktree; sourcefree pytest/SQLite/cold subprocess courts",
        ),
        branch=passport.get("git_branch", ""),
        checkout_sha=passport.get("git_head_at_run", ""),
        parent_dispatch="529232d9867a5bdc0889f43fb5293131ef806055",
        shared_store_alias="rawlsing-shared-store",
        worktree_alias="bp1",
        source_closure="BOUNDED",
        permissions=dict(private_repo_access="VERIFIED",
                         original_survey_use="NOT_GRANTED",
                         external_model_use="NOT_GRANTED",
                         actor_execution="NOT_GRANTED",
                         native_can_adp_issuance="NOT_GRANTED"),
        usage=dict(provider_model="DeepSeek V4.1-Flash reasoning MAX (user-selected)",
                   incremental_cash_usd=None, quota_state="UNKNOWN",
                   usage_observed="local Git/pytest/SQLite only; no paid API call observed",
                   retry_count=0),
        native_authority="NOT_GRANTED",
    )
    write("environment_passport_delta.json", delta)
    print("wrote BP1 evidence receipts")


if __name__ == "__main__":
    raise SystemExit(main())
