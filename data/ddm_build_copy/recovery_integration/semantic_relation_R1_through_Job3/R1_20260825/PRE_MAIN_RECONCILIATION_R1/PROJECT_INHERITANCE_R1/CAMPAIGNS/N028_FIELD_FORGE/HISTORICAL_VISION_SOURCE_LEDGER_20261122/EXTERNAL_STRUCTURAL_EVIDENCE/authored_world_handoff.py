"""R9: prepare the existing R36 authored structural-history input.

The evidence body is retained separately. Explicit fictional choices, not
native observations or survey answers, constitute the R36 rules/positions.
No world mutation, rule evaluation, source issuance, or psychological model.
"""
from copy import deepcopy
import hashlib
import json

from native_priority_readers import FINDEX_MARGINS, JOIN_STATUS, WBL_QUESTIONS


FIELDS = {
    "EPR": ("gwid", "gwgroupid", "from", "to", "status", "size", "reg_aut"),
    "WBL": ("economycode", "year", "reportyr", *WBL_QUESTIONS),
    "JOIN": ("Country Code", "Year of survey", "Survey Data Source", "Survey Type",
             "Subsample", *JOIN_STATUS, "Share of work contract", "Share of social security"),
    "FINDEX": ("codewb", "year", "group", "group2", *FINDEX_MARGINS),
}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def select_world_evidence(pack, requests):
    """Read only demanded sources; keep separate keys, dates and unmatched rows.

    No implicit economy/polity mapping. Explicit requests are caller-selected,
    not source-qualified crosswalks or actual actor memberships.
    """
    results = []
    for request in requests:
        if set(request) != {"source", "keys", "reference_year"}:
            raise ValueError("explicit source, keys and reference_year required")
        source, keys, year = request["source"], request["keys"], request["reference_year"]
        if source not in FIELDS or not isinstance(keys, dict) or not keys:
            raise ValueError("unsupported source or empty native selection")
        required = {"EPR": {"gwid"}, "WBL": {"economycode", "year"},
                    "JOIN": {"Country Code", "Year of survey", "Subsample"},
                    "FINDEX": {"codewb", "year", "group", "group2"}}[source]
        if not required <= keys.keys() or (source == "EPR") != (year is not None):
            raise ValueError("missing native scope")
        results.append(pack.select(source, keys, FIELDS[source], year=year))
    return {"grade": "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY",
            "alignment": "INDEPENDENT_CALLER_SELECTED_NATIVE_SCOPES", "observations": results}


def _prepare(evidence, *, scenario_id, rationale, positions, rules):
    """Translate explicit fictional premises to R36's exact four-key contract.

    Caller supplies complete authored positions/rules except source_ref. The
    incumbent owns admission (actors, sites, operations, intervals, clauses).
    Evidence is never translated automatically into a rule or personal fact.
    The returned sidecar must be retained with the exact authored spec.
    """
    if not all(type(x) is str and x.strip() for x in (scenario_id, rationale)):
        raise ValueError("explicit fictional scenario and rationale required")
    if type(positions) is not list or type(rules) is not list:
        raise ValueError("explicit authored premises required")
    choice = {"scenario_id": scenario_id, "rationale": rationale,
              "positions": deepcopy(positions), "rules": deepcopy(rules)}
    for row in choice["positions"] + choice["rules"]:
        if type(row) is not dict or "source_ref" in row:
            raise ValueError("do not present a native source as rule authority")
    evidence = deepcopy(evidence)
    identity = _digest({"evidence": evidence, "fictional_choice": choice})
    ref = "fictional:ff:authored-history:sha256:" + identity
    spec = {"grade": "EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY", "source_ref": ref,
            "positions": [dict(row, source_ref=ref) for row in choice["positions"]],
            "rules": [dict(row, source_ref=ref) for row in choice["rules"]]}
    return {"grade": "PROVISIONAL_FICTIONAL_HANDOFF_NOT_NATIVE_ADMISSION",
            "evidence": evidence, "fictional_choice": choice,
            "authored_structural_history": spec, "content_hash": identity}


def prepare_authored_history(evidence, *, scenario_id, rationale, positions, rules):
    """Preserve R9 native retrospective evidence contract without widening it."""
    if evidence.get("grade") != "NATIVE_RETROSPECTIVE_CONTEXT_NOT_WORLD_AUTHORITY":
        raise ValueError("unexpected evidence grade")
    return _prepare(evidence, scenario_id=scenario_id, rationale=rationale,
                    positions=positions, rules=rules)


def prepare_repertoire_authored_history(inquiry, *, scenario_id, rationale, positions,
                                        rules, public_notices):
    """R12: retain an R11 sourcefree inquiry beside independent fictional premises.

    A public institutional account is not its objective rule. The caller
    proposes both separately and the world owner admits/executes them. No
    automatic norm-to-rule, actor inference, or source authorization.
    Only the sourcefree experimental lane is eligible; native context stays
    internal and cannot be forwarded through this seam.
    """
    from rawlsing_next.pre553_s04_general_joint_algebra import S04ProjectionAnswer
    from rawlsing_next.pre553_empirical_objects import canonical_json
    if (type(inquiry) is not dict
            or inquiry.get("grade") != "INTERNAL_SOURCEFREE_FF_INQUIRY_NOT_SOURCE_OR_WORLD_ISSUANCE"
            or inquiry.get("state") != "PROVISIONAL_CONCEPT_REVISED_NOT_CERTIFIED"
            or inquiry.get("context_alignment") != "NO_SURVEY_TO_MATERIAL_CROSSWALK"
            or inquiry.get("independent_native_context") != {
                "grade": "HELD_NO_SELECTED_NATIVE_CONTEXT", "observations": []}):
        raise ValueError("only completed sourcefree inquiry without native context can enter this experiment")
    for export in (inquiry["baseline"], inquiry["contrast"]["left"],
                   inquiry["contrast"]["right"], inquiry["reverse"]):
        m = export["material"]
        a = S04ProjectionAnswer(canonical_json(m), export["ref"]["content_hash"])
        if (a.ref.as_dict() != export["ref"]
                or m["knowledge_ref"] != inquiry["knowledge_ref"]
                or m["source_fact_ref"] != inquiry["observation"]["fact_ref"]
                or m["independent_original_source_issuer"] is not None):
            raise ValueError("inconsistent sourcefree projection receipt")
    if inquiry["reverse"]["material"]["state"] != "OBSERVED_FULL_CASE_SUPPORT":
        raise ValueError("no positive observed motif to motivate a modeled alternative")
    _validate_public_notices(public_notices)
    evidence = {"grade": "SOURCEFREE_REPERTOIRE_AND_FICTIONAL_ACCOUNT_NOT_WORLD_AUTHORITY",
                "inquiry": deepcopy(inquiry), "public_notices": deepcopy(public_notices)}
    return _prepare(evidence, scenario_id=scenario_id, rationale=rationale,
                    positions=positions, rules=rules)


def _validate_public_notices(public_notices):
    if type(public_notices) is not list or not public_notices:
        raise ValueError("explicit fictional public account required")
    # Exactly the incumbent R48 authored world notice input, not a new
    # publication API. Keep separate from the structural-history spec.
    for n in public_notices:
        if (type(n) is not dict or set(n) != {
                "id", "public", "location", "public_terms", "public_text",
                "effective_from", "effective_until"} or n["public"] is not True
                or not all(type(n[k]) is str and n[k].strip()
                           for k in ("id", "location", "public_text"))
                or type(n["public_terms"]) is not list
                or not all(type(t) is str and t.strip() for t in n["public_terms"])
                or type(n["effective_from"]) is not int or type(n["effective_until"]) is not int
                or not 0 <= n["effective_from"] <= n["effective_until"]):
            raise ValueError("invalid explicit public account")
    if len({n["id"] for n in public_notices}) != len(public_notices):
        raise ValueError("duplicate public account")

def verify_handoff(packet):
    """Verify exact replay; not an authorization or incumbent admission check."""
    evidence = packet["evidence"]
    if evidence.get("grade") == "SOURCEFREE_REPERTOIRE_AND_FICTIONAL_ACCOUNT_NOT_WORLD_AUTHORITY":
        return prepare_repertoire_authored_history(
            evidence["inquiry"], public_notices=evidence["public_notices"],
            **packet["fictional_choice"]) == packet
    if evidence.get("grade") == "SOURCEFREE_FORMATION_ALTERNATIVES_NOT_WORLD_AUTHORITY":
        return prepare_formation_authored_history(
            evidence["concept_inquiry"], formation_choices=evidence["formation_choices"],
            public_notices=evidence["public_notices"],
            **packet["fictional_choice"]) == packet
    return prepare_authored_history(evidence, **packet["fictional_choice"]) == packet


def repertoire_source_seals(packet):
    """Prepare actual ResearchLedger genesis input for sourcefree sidecar custody.

    The receiving owner performs the atomic initialization and verifies the
    chain. The content address is the sidecar's lookup key, not a credential.
    Native R9 packets MUST NOT be published through this experimental path.
    No new store, native disclosure, actor memory or source-use grant.
    """
    if (packet.get("evidence", {}).get("grade") not in (
            "SOURCEFREE_REPERTOIRE_AND_FICTIONAL_ACCOUNT_NOT_WORLD_AUTHORITY",
            "SOURCEFREE_FORMATION_ALTERNATIVES_NOT_WORLD_AUTHORITY")
            or not verify_handoff(packet)):
        raise ValueError("exact sourcefree repertoire sidecar required")
    spec = packet["authored_structural_history"]
    return [
        ("authored_structural_history", "FICTIONAL_WORLD_CONDITIONING", deepcopy(spec)),
        (spec["source_ref"], "FICTIONAL_FF_REPERTOIRE_CONDITIONING_NOT_NATIVE_ISSUANCE",
         deepcopy(packet)),
    ]


def formation_repertoire_offers(concept_inquiry):
    """R17: exact source-local alternative repertoire offers from R16.

    Use existing sealed I05 inquiry and R15/S04 projection receipts. A
    positive cell is a possible repertoire, not a measured formation or
    institutional membership. All supported cells within each examined
    position slice survive, including minority alternatives. No proxy,
    pooled cohort, inferred source role, or probability of contact.
    """
    from rawlsing_next.pre553_discovery_adaptive import AdaptiveSearchCheckpoint
    from rawlsing_next.pre553_empirical_objects import semantic_hash, canonical_json
    from rawlsing_next.pre553_s04_general_joint_algebra import S04ProjectionAnswer

    if (type(concept_inquiry) is not dict or concept_inquiry.get("grade") !=
            "INTERNAL_SOURCEFREE_CONCEPT_DEVELOPMENT__NO_SOURCE_OR_WORLD_ISSUANCE"
            or concept_inquiry.get("pooled_joint",False) is not None
            or any(concept_inquiry.get(k) is not False for k in (
                "global_negative_claim","semantic_truth_effect","actor_v3_effect"))):
        raise ValueError("exact sourcefree R16 inquiry required")
    checkpoint = AdaptiveSearchCheckpoint.from_dict(concept_inquiry["checkpoint"])
    records = concept_inquiry["records"]
    if len(records)!=len(checkpoint.visits) or not records:
        raise ValueError("concept record/checkpoint mismatch")
    if (concept_inquiry["concept"]!=records[-1]["development"]["concept"]
            or concept_inquiry["determinant_ref"]!=checkpoint.determinant_state_ref.as_dict()):
        raise ValueError("concept result/checkpoint mismatch")
    offers, slices = {}, []
    for rec, visit in zip(records,checkpoint.visits):
        sealed=visit.outcome.sealed_result_ref
        if (sealed.content_hash!=semantic_hash(rec)
                or sealed.kind!="FF_CONCEPT_INQUIRY_RESULT"
                or sealed.object_id!="urn:rawlsing:ff:r16:ff_concept_inquiry_result:"+sealed.content_hash):
            raise ValueError("concept inquiry sealed record mismatch")
        local=rec["local_discovery"]
        if (local["grade"]!="INTERNAL_SOURCEFREE_FF_DISCOVERY_NOT_SOURCE_SCIENCE_OR_WORLD_ISSUANCE"
                or any(local[k] is not False for k in (
                    "global_negative_claim","semantic_truth_effect","actor_v3_effect"))):
            raise ValueError("local discovery not sourcefree")
        def checked(export):
            m=export["material"]
            a=S04ProjectionAnswer(canonical_json(m),export["ref"]["content_hash"])
            if (a.ref.as_dict()!=export["ref"] or m["knowledge_ref"]!=local["knowledge_ref"]
                    or m["independent_original_source_issuer"] is not None):
                raise ValueError("source-local projection mismatch")
            return m
        base=checked(local["baseline"])
        for r in local["records"]:
            checked(r["positions"])
            for export in r["conditional_repertoires"]:
                m=checked(export)
                if m["state"]!="OBSERVED_FULL_CASE_SUPPORT":
                    continue
                sl={"inquiry":rec["inquiry"],"knowledge_ref":local["knowledge_ref"],
                    "observation_ref":local["observation_ref"],"projection_ref":export["ref"],
                    "position_axes":r["position_axes"],"conditions":m["conditions"],
                    "raw_selected_n":m["raw_selected_full_case_n"],
                    "concept_at_inquiry":rec["development"]["concept"],
                    "concept_disposition":rec["development"]["disposition"],
                    "source_scope":{k:m[k] for k in ("source_fact_ref","source_query_ref",
                                                      "source_release_ref","source_risk_set_ref")},
                    "state":"OBSERVED_SOURCEFREE_FULL_CASE_SLICE"}
                sid="ff:formation-slice:sha256:"+_digest(sl)
                ids=[]
                for cell in m["complete_output_cells"]:
                    if cell["raw_count"]<=0:
                        continue
                    offer={"slice_id":sid,"inquiry":rec["inquiry"],
                        "motif":deepcopy(cell["output_states"]),
                        "raw_count":cell["raw_count"],
                        "raw_fraction":cell["raw_fraction_of_selected_full_cases"],
                        "raw_selected_n":m["raw_selected_full_case_n"],
                        "grade":"OBSERVED_REPERTOIRE_ALTERNATIVE_NOT_MEMBERSHIP"}
                    oid="ff:formation-offer:sha256:"+_digest(offer)
                    offers[oid]=dict(offer,id=oid);ids.append(oid)
                slices.append(dict(sl,id=sid,offer_ids=ids))
    return {"grade":"SOURCEFREE_FORMATION_REPERTOIRE_OFFERS_NOT_SOCIAL_MEMBERSHIP",
            "concept":concept_inquiry["concept"],"slices":slices,
            "offers":list(offers.values()),"unexamined":deepcopy(concept_inquiry["unexamined"]),
            "pooled_joint":None}


def prepare_formation_authored_history(concept_inquiry, *, formation_choices, scenario_id,
                                       rationale, positions, rules, public_notices):
    """Compose overlapping possible formations with independent authored relations.

    Formation choices are fictional hypotheses: arena, possible carrier
    roles, supported repertoire offers, public enactment and independently
    authored channels of provision/control/renewal. They do not issue actual
    institutional rules, membership, contact, assent or psychology.
    Actual rules/notices retain their existing R36/R48 ABI and owner.
    """
    available=formation_repertoire_offers(concept_inquiry)
    _validate_public_notices(public_notices)
    if type(formation_choices) is not list or not formation_choices:
        raise ValueError("explicit possible formation choices required")
    if type(rules) is not list or type(positions) is not list:
        raise ValueError("explicit authored material premises required")
    offer_by_id={x["id"]:x for x in available["offers"]}
    slice_by_id={x["id"]:x for x in available["slices"]}
    rule_by_id={r["id"]:r for r in rules}
    notice_by_id={n["id"]:n for n in public_notices}
    choices=deepcopy(formation_choices)
    seen, formations = set(), []
    def text(x):return type(x) is str and bool(x.strip())
    for f in choices:
        if (type(f) is not dict or set(f)!={"id","arena","carrier_roles","offer_ids",
                "public_notice_ids","reproduction_channels","interpretation"}
                or not all(text(f[k]) for k in ("id","arena","interpretation"))
                or f["id"] in seen or type(f["carrier_roles"]) is not list
                or not f["carrier_roles"] or not all(text(v) for v in f["carrier_roles"])
                or len(set(f["carrier_roles"]))!=len(f["carrier_roles"])):
            raise ValueError("invalid fictional formation or carrier roles")
        seen.add(f["id"])
        ids=f["offer_ids"]; notices=f["public_notice_ids"]
        if (type(ids) is not list or not ids or not all(text(i) and i in offer_by_id for i in ids)
                or len(set(ids))!=len(ids) or type(notices) is not list
                or not all(text(i) and i in notice_by_id for i in notices)
                or len(set(notices))!=len(notices)):
            raise ValueError("formation must retain actual positive scoped offers and existing public accounts")
        channels=f["reproduction_channels"]
        if type(channels) is not list or not channels:
            raise ValueError("independent reproduction channels required")
        for ch in channels:
            if (type(ch) is not dict or set(ch)!={"resource","provider_role","controller_role",
                    "beneficiary_role","cost_bearer_role","renewal_condition","rule_id"}
                    or not all(text(v) for v in ch.values())
                    or ch["rule_id"] not in rule_by_id):
                raise ValueError("independent reproduction channel must reference authored material rule")
        # Preserve the entire source-local alternative set for every
        # selected slice. Selecting an illustrative motif never erases
        # the alternative positions/repertoires in that source.
        selected=[offer_by_id[i] for i in ids]
        slids=sorted({o["slice_id"] for o in selected})
        formations.append({"id":f["id"],"arena":f["arena"],"carrier_roles":f["carrier_roles"],
            "selected_offers":selected,
            "retained_slices":[slice_by_id[i] for i in slids],
            "retained_alternatives":[offer_by_id[oid] for i in slids
                                     for oid in slice_by_id[i]["offer_ids"]],
            "public_notice_ids":notices,"reproduction_channels":channels,
            "interpretation":f["interpretation"],
            "grade":"EXPLICIT_FICTIONAL_FORMATION_PROPOSAL_NOT_ACTUAL_MEMBERSHIP"})
    # Relate overlapping possible formations without turning them into a
    # partition. Shared resources/controllers and alternative repertoires
    # are different relations. No empirical overlap count is synthesized.
    relations=[]
    for i,left in enumerate(formations):
        for right in formations[i+1:]:
            shared=sorted(set(left["carrier_roles"])&set(right["carrier_roles"]))
            common_slices=sorted({x["slice_id"] for x in left["selected_offers"]}&
                                 {x["slice_id"] for x in right["selected_offers"]})
            alternatives=[]
            for x in left["selected_offers"]:
                for y in right["selected_offers"]:
                    if x["slice_id"]==y["slice_id"] and x["motif"]!=y["motif"]:
                        alternatives.append([x["id"],y["id"]])
            reproduction=[]
            for x in left["reproduction_channels"]:
                for y in right["reproduction_channels"]:
                    if x["resource"]==y["resource"]:
                        reproduction.append({"resource":x["resource"],
                            "left_controller":x["controller_role"],"right_controller":y["controller_role"],
                            "left_rule":x["rule_id"],"right_rule":y["rule_id"],
                            "same_controller":x["controller_role"]==y["controller_role"],
                            "left_renewal":x["renewal_condition"],"right_renewal":y["renewal_condition"]})
            if shared or common_slices or reproduction or left["arena"]==right["arena"]:
                relations.append({"left":left["id"],"right":right["id"],
                    "shared_possible_carrier_roles":shared,"same_arena":left["arena"]==right["arena"],
                    "shared_observed_slices":common_slices,"distinct_supported_motif_pairs":alternatives,
                    "shared_resource_channels":reproduction,
                    "actual_membership_or_conflict":"NOT_INFERRED",
                    "grade":"MODELED_INTERPENETRATION_NOT_EMPIRICAL_OVERLAP_OR_CAUSAL_FORCE"})
    evidence={"grade":"SOURCEFREE_FORMATION_ALTERNATIVES_NOT_WORLD_AUTHORITY",
        "concept_inquiry":deepcopy(concept_inquiry),"formation_choices":choices,
        "repertoire_offers":available,"formations":formations,"relations":relations,
        "public_notices":deepcopy(public_notices),
        "unresolved":["actual formation membership","actual institutional control and reproduction",
                      "public enactment beyond authored notices","encounter and actor appropriation"],
        "pooled_joint":None}
    return _prepare(evidence,scenario_id=scenario_id,rationale=rationale,positions=positions,rules=rules)
