"""R11 actual saved SOURCEFREE I03 -> #1292 -> FF01 -> R8 -> reverse inquiry.

Run against #1292 exact worktree; not original WVS data, nor a mocked S04 export.
"""
from itertools import product
import pytest

from rawlsing_next.pre553_s04_dynamic_research import (
    S04DynamicQuestion, S04DynamicResearchSession, SOURCEFREE_ONLY_ASSERTION,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests import test_pre553_distinct_cold_i03_batch as cold
from relational_context import inquire_repertoire_fracture


def _session(tmp_path, monkeypatch, parity, current=lambda _: True):
    tmp_path.mkdir(parents=True, exist_ok=True)
    captured = {}
    ingest = native.ingest_c11_source_release

    def catch(candidate, repo):
        captured["candidate"] = candidate
        return ingest(candidate, repo)

    # Two contrasting coherent repertoires with identical pairwise margins
    # in the two alternate fixture worlds. Not recoded WVS observations.
    rows = [{"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
            for x, y in product((0, 1), repeat=2)]
    tag = f"FF-R11-PARITY-{parity}"
    with monkeypatch.context() as guard:
        guard.setattr(native, "ingest_c11_source_release", catch)
        source = native._build_source(tag, rows, question_namespace="FF-R11-QUESTIONS")
    qa = native._query_authority(tag)
    predicate = native._branch_predicate(source, qa)
    query = native._query(source, qa, predicate, ("X", "Y", "Z"), tag="ff-r11")
    root, receipt = cold._cold(tmp_path, captured["candidate"], source["universe"].ref, tag)
    estate = cold.VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02, current_authorizer=current,
    )
    catalog = cold.RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)), predicates=(predicate,),
        queries=(query,), discovery_authorities=(),
    )
    executor = cold.CarrierNeutralResearchExecutor(
        repository=estate, release_refs=(source["release_ref"],), runtime_catalog=catalog,
    )
    return (S04DynamicResearchSession(executor=executor,
                sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION),
            S04DynamicQuestion(query.ref, predicate.ref, conditioner_index=0))


def propose(view):
    # Model-authored rival concepts; fixture callback, NOT a live LLM call.
    assert "verified_eligible_member_set_sha256" not in str(view)
    return {"concept": "selective entitlement under narrated scarcity",
            "rival": "a unified exclusion norm independent of reported employment",
            "question": "Which reported employment position carries the mixed norm motif?",
            "motif": ["1", "0"]}


def revise(view, proposal, reverse):
    positive = [c["output_states"][0] for c in reverse["complete_output_cells"]
                if c["raw_count"] > 0]
    return {"interpretation": f"Sample-only mixed motif positions: {positive}",
            "remaining_question": "Are actual allocation rules and alternative livelihood channels different?",
            "recipient_possibility": "Model competing hiring priorities separately; do not assign either to a person."}


def run(session, q, **kwargs):
    options = dict(position_states=("0", "1"), repertoire_axes=(1, 2),
                   response_act_meanings={0: "reported employment position",
                      1: "gendered job priority norm", 2: "citizenship job priority norm"},
                   modeled_context="Fictional employer controls access to wages; independent relief may permit refusal.",
                   propose=propose, revise=revise)
    options.update(kwargs)
    return inquire_repertoire_fracture(session, q, **options)


def test_actual_native_parity_changes_concept_despite_same_margins(tmp_path, monkeypatch):
    results = []
    for parity in (0, 1):
        session, q = _session(tmp_path / str(parity), monkeypatch, parity)
        with session:
            packet = run(session, q)
            assert session.stats()["original_native_i03_queries_executed"] == 1
        assert packet["state"] == "PROVISIONAL_CONCEPT_REVISED_NOT_CERTIFIED"
        assert packet["context_alignment"] == "NO_SURVEY_TO_MATERIAL_CROSSWALK"
        assert packet["observation"]["source_frame_population_n"] is None
        assert packet["recipient_state"].endswith("RECEIVING_HELD")
        results.append(packet)
    a, b = results
    assert a["baseline"]["material"]["complete_output_cells"] == b["baseline"]["material"]["complete_output_cells"]
    assert a["contrast"]["cells"] != b["contrast"]["cells"]
    assert a["revision"]["interpretation"] != b["revision"]["interpretation"]
    assert a["modeled_context"] == b["modeled_context"]


def test_unknown_domain_cannot_become_invented_repertoire(tmp_path, monkeypatch):
    session, q = _session(tmp_path, monkeypatch, 0)
    def invalid(view):
        return dict(propose(view), motif=["NOT_A_SOURCE_STATE", "0"])
    with session, pytest.raises(ValueError):
        run(session, q, propose=invalid)


def test_revocation_during_interpretation_refuses_return(tmp_path, monkeypatch):
    allowed = {"current": True}
    session, q = _session(tmp_path, monkeypatch, 0, lambda _: allowed["current"])
    def revoke(view, proposal, reverse):
        allowed["current"] = False
        return revise(view, proposal, reverse)
    with session, pytest.raises(cold.DirectEstateError, match="(?i)current|revok|authoriz"):
        run(session, q, revise=revoke)


def test_real_native_context_remains_separate(tmp_path, monkeypatch):
    import os
    from native_priority_readers import NativePack
    root = os.environ.get("FF_PRIORITY_PACK")
    if not root:
        pytest.skip("R6 native priority pack not mounted")
    session, q = _session(tmp_path, monkeypatch, 0)
    with session:
        packet = run(session, q, pack=NativePack(root), context_requests=(
            {"source": "JOIN", "keys": {"Country Code": "IND", "Year of survey": 2019,
             "Subsample": "All"}, "reference_year": None},))
    assert packet["independent_native_context"]["observations"][0]["rows"]
    assert packet["context_alignment"] == "NO_SURVEY_TO_MATERIAL_CROSSWALK"
    assert packet["modeled_context"]["grade"] == "EXPLICIT_FICTIONAL_PREMISE"


# R14 reuses the same actual cold I03 test harness, with a four-axis joint.
def _social_session(tmp_path, monkeypatch, rows, current=lambda _: True,
                    targets=("X", "W", "Y", "Z")):
    tmp_path.mkdir(parents=True, exist_ok=True)
    captured = {}
    ingest = native.ingest_c11_source_release
    def catch(candidate, repo):
        captured["candidate"] = candidate
        return ingest(candidate, repo)
    tag = "FF-R14-" + tmp_path.name
    with monkeypatch.context() as guard:
        guard.setattr(native, "ingest_c11_source_release", catch)
        source = native._build_source(tag, rows, question_namespace="FF-R14-QUESTIONS")
    qa = native._query_authority(tag)
    predicate = native._branch_predicate(source, qa)
    query = native._query(source, qa, predicate, targets, tag="ff-r14")
    root, receipt = cold._cold(tmp_path, captured["candidate"], source["universe"].ref, tag)
    estate = cold.VerifiedDirectEstate(root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02, current_authorizer=current)
    catalog = cold.RuntimeObjectCatalog(authorities=tuple((*source["authorities"], qa)),
        predicates=(predicate,), queries=(query,), discovery_authorities=())
    executor = cold.CarrierNeutralResearchExecutor(repository=estate,
        release_refs=(source["release_ref"],), runtime_catalog=catalog)
    return S04DynamicResearchSession(executor=executor,
        sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION), S04DynamicQuestion(
            query.ref, predicate.ref, conditioner_index=0)


def _social_rows(parity):
    # Within each one-coordinate margin all motifs equally distributed.
    # The two-position intersection reverses between fixture worlds.
    return [{"id": f"R{x}{w}{y}", "responses": {"X":x, "W":w, "Y":y, "Z":x ^ w ^ y ^ parity}}
            for x,w,y in product((0,1), repeat=3)]


def _social_propose(view):
    assert "source_fact_ref" not in str(view)
    return {"concept": "selective entitlement", "rival": "position-independent exclusion",
            "question": "Which intersection carries the opposed motifs?", "motifs": [["1","0"],["1","1"]]}


def _social_revise(view, proposal, motifs):
    return {"interpretation": str([m["selected_positions"] for m in motifs]),
            "remaining_question": "Which independent positions actually carry institutional control?",
            "recipient_possibility": "Offer rival repertoires without assigning them to an actual Other."}


def _social_run(session, q, **kwargs):
    from relational_context import inquire_social_field
    opts = dict(position_axes=(0,1), repertoire_axes=(2,3),
        axis_meanings={0:"reported resource position",1:"reported credential position",
                       2:"gender priority",3:"national priority"},
        active_ancestry={i:(f"independent-fixture-item-{i}",) for i in range(4)},
        contrasts=(("resource", {0:"0"}, {0:"1"}), ("credential", {1:"0"}, {1:"1"}),
                   ("intersection", {0:"0",1:"0"}, {0:"0",1:"1"})),
        propose=_social_propose, revise=_social_revise)
    opts.update(kwargs)
    return inquire_social_field(session,q,**opts)


def test_social_field_intersection_and_rivals_without_external_pack(tmp_path, monkeypatch):
    results=[]
    for parity in (0,1):
        session,q=_social_session(tmp_path / str(parity), monkeypatch, _social_rows(parity))
        with session:
            out=_social_run(session,q)
            assert session.stats()["original_native_i03_queries_executed"] == 1
        assert out["state"] == "PROVISIONAL_SOCIAL_FIELD_REVISED_NOT_CERTIFIED"
        assert out["external_context"] == "NOT_REQUIRED_FOR_DESCRIPTIVE_CORRESPONDENCE"
        assert all(v["difference_right_minus_left"] == [0,1]
                   for c in out["contrasts"][:2] for v in c["differences"])
        results.append(out)
    a,b=results
    assert a["baseline"]["material"]["complete_output_cells"] == b["baseline"]["material"]["complete_output_cells"]
    assert a["contrasts"][2]["differences"] != b["contrasts"][2]["differences"]
    assert a["revision"]["interpretation"] != b["revision"]["interpretation"]
    assert a["motifs"][0]["reverse"]["material"]["complete_output_cells"] != b["motifs"][0]["reverse"]["material"]["complete_output_cells"]


def test_social_field_prevalence_composition_and_reach_are_different(tmp_path, monkeypatch):
    # All resource-advantaged respondents express the motif; the other
    # position has more carriers in absolute count, but lower prevalence.
    rows=[]
    for x,w,y,z,n in [(1,1,1,0,2),(0,0,1,0,3),(0,0,0,1,4),(0,1,0,0,1)]:
        for _ in range(n):
            rows.append({"id":f"R{len(rows)}","responses":{"X":x,"W":w,"Y":y,"Z":z}})
    session,q=_social_session(tmp_path, monkeypatch, rows)
    with session:
        out=_social_run(session,q, contrasts=(("resource",{0:"0"},{0:"1"}),
                                             ("absent",{0:"0",1:"0"},{0:"1",1:"0"})))
    m=out["motifs"][0]["selected_positions"]
    assert (m[0]["prevalence"],m[0]["composition"],m[0]["joint_mass"]) == ([3,8],[3,5],[3,10])
    assert (m[1]["prevalence"],m[1]["composition"],m[1]["joint_mass"]) == ([1,1],[2,5],[1,5])
    assert m[3]["prevalence"] is None and m[3]["composition"] == [0,1]
    # An absent motif is not a positive reverse distribution.
    assert out["motifs"][1]["baseline_count"] == 0
    assert out["motifs"][1]["selected_positions"][0]["composition"] is None


def test_social_field_declared_ancestry_overlap_refused_before_query(tmp_path, monkeypatch):
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0))
    with session, pytest.raises(ValueError,match="ancestry"):
        _social_run(session,q,active_ancestry={0:("shared",),1:("w",),2:("shared",),3:("z",)})


def test_social_field_revoke_after_revision(tmp_path, monkeypatch):
    current={"allowed":True}
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0),lambda _:current["allowed"])
    def revoke(*args):
        current["allowed"]=False
        return _social_revise(*args)
    with session, pytest.raises(cold.DirectEstateError,match="(?i)current|revok|authoriz"):
        _social_run(session,q,revise=revoke)


# R15: actual I05 adaptive scheduler + actual S04 DHIKR + R14 on the
# same saved cold fixture. Test authority is the incumbent sourcefree
# fixture authority, not a production discovery/source grant.
def _discover_run(session,q,**kwargs):
    from relational_context import discover_social_field
    from rawlsing_next.tests import test_pre553_discovery_adaptive as adaptive
    authority,registry,root,child=adaptive._authority("ff-r15")
    def interpret(view):
        assert "source_fact_ref" not in str(view)
        first=view["candidates"][0] if view["candidates"] else None
        return {"concept": "position-dependent selective entitlement" if first and first["gap"] != [0,1]
                           else "apparently undifferentiated repertoire",
                "rival":"hidden intersection", "question":"Follow the next position interaction",
                "preferred_axis":next(iter(view["eligible_extension_axes"]),None)}
    def revise_discovered(view, proposal, motifs):
        # Include actual reverse position distributions, not just symmetric
        # low/high fractions whose values can be equal in the two worlds.
        return {"interpretation": str([m["reverse"]["cells"] for m in motifs]),
                "remaining_question":"Which institutional resources make the alignment consequential?",
                "recipient_possibility":"Offer observed alternatives without assigning an actor belief."}
    opts=dict(position_axes=(0,1),repertoire_axes=(2,3),
        axis_meanings={0:"resource",1:"credential",2:"gender priority",3:"national priority"},
        active_ancestry={i:(f"fixture-{i}",) for i in range(4)},
        discovery_authority=authority,authority_registry=registry,root_rule=root,child_rule=child,
        budget=3,max_position_order=2,min_position_n=2,interpret=interpret,revise=revise_discovered)
    opts.update(kwargs)
    return discover_social_field(session,q,**opts)


def test_discover_intersection_without_caller_motif_or_contrast(tmp_path,monkeypatch):
    outcomes=[]
    for parity in (0,1):
        session,q=_social_session(tmp_path/str(parity),monkeypatch,_social_rows(parity))
        with session:
            out=_discover_run(session,q)
            assert session.stats()["original_native_i03_queries_executed"] == 1
        assert out["completeness_state"] == "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED"
        assert len(out["records"]) == 3 and not out["global_negative_claim"]
        assert all(r["followthrough"] is None for r in out["records"] if len(r["position_axes"])==1)
        joint=next(r for r in out["records"] if r["position_axes"]==[0,1])
        assert joint["candidates"][0]["gap"] == [1,2]
        assert joint["followthrough"]["state"] == "PROVISIONAL_SOCIAL_FIELD_REVISED_NOT_CERTIFIED"
        assert len(joint["followthrough"]["motifs"])==2
        assert all(d["material"]["nodes"] for d in out["diagnostics"])
        outcomes.append(joint)
    assert outcomes[0]["candidates"][0]["high"] != outcomes[1]["candidates"][0]["high"]
    assert outcomes[0]["followthrough"]["revision"] != outcomes[1]["followthrough"]["revision"]


def test_discover_budget_retains_unvisited_and_no_global_negative(tmp_path,monkeypatch):
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0))
    with session:
        out=_discover_run(session,q,budget=1)
        assert session.stats()["original_native_i03_queries_executed"] == 1
    assert out["completeness_state"] == "PARTIAL_BUDGET_EXHAUSTED"
    assert out["unvisited"] and all(x["state"]=="UNKNOWN_UNVISITED" for x in out["unvisited"])
    assert out["global_negative_claim"] is False
    assert len(out["records"]) == 1


def test_discover_below_support_does_not_become_absence(tmp_path,monkeypatch):
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0))
    with session:
        out=_discover_run(session,q,min_position_n=3)
    joint=next(r for r in out["records"] if r["position_axes"]==[0,1])
    assert not joint["candidates"] and joint["followthrough"] is None
    assert len(joint["excluded"])==4
    assert all(x["state"]=="BELOW_SELECTED_SUPPORT__NOT_ABSENCE" for x in joint["excluded"])


def test_discover_rejects_illegal_semantic_extension(tmp_path,monkeypatch):
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0))
    def invalid(view):
        return {"concept":"x","rival":"y","question":"z","preferred_axis":99}
    with session,pytest.raises(ValueError,match="eligible next position"):
        _discover_run(session,q,interpret=invalid)


def test_discover_revocation_even_on_null_marginal(tmp_path,monkeypatch):
    allowed={"current":True}
    session,q=_social_session(tmp_path,monkeypatch,_social_rows(0),lambda _:allowed["current"])
    def revoke(view):
        allowed["current"]=False
        return {"concept":"x","rival":"y","question":"z","preferred_axis":None}
    with session,pytest.raises(cold.DirectEstateError,match="(?i)current|revok|authoriz"):
        _discover_run(session,q,interpret=revoke)


def test_discover_semantic_feedback_changes_actual_scheduled_question(tmp_path,monkeypatch):
    rows=[{"id":f"R{x}{w}{v}{y}", "responses":{"X":x,"W":w,"V":v,"Y":y,"Z":x^w^v^y}}
          for x,w,v,y in product((0,1),repeat=4)]
    results=[]
    for preference in (1,2):
        session,q=_social_session(tmp_path/str(preference),monkeypatch,rows,
                                   targets=("X","W","V","Y","Z"))
        def interpret(view):
            # The first root may be any of the three axes under the
            # incumbent tie rule. Ensure all reachable alternatives are
            # visited and the preferred child ranks above other children.
            available=view["eligible_extension_axes"]
            return {"concept":"hidden alignment","rival":"independence","question":"probe interaction",
                    "preferred_axis":preference if preference in available else None}
        with session:
            out=_discover_run(session,q,position_axes=(0,1,2),repertoire_axes=(3,4),
                axis_meanings={i:f"axis-{i}" for i in range(5)},
                active_ancestry={i:(f"fixture-{i}",) for i in range(5)},
                max_position_order=3,budget=7,interpret=interpret)
        assert out["completeness_state"]=="EXPLORATORY_POLICY_FRONTIER_EXHAUSTED"
        records=out["records"]
        root=next(r for r in records if r["position_axes"]==[0])
        assert root["interpretation"]["preferred_axis"]==preference
        visits=out["checkpoint"]["visits"]
        # The selected child of root 0 must have the higher actual
        # scheduler rank and be visited before its sibling.
        first=next(i for i,r in enumerate(records) if r["position_axes"]==[0,preference])
        other=next(i for i,r in enumerate(records) if r["position_axes"]==[0,3-preference])
        assert first<other
        triple=next(r for r in records if r["position_axes"]==[0,1,2])
        assert triple["followthrough"] is not None
        results.append([r["position_axes"] for r in records])
    assert results[0]!=results[1]
