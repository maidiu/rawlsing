"""Offline typed referent compiler for actor-safe RFA-05B packets.

Atom grounding and documented physical world effects are separate authorities.
This code never mutates a prompt, response, or source fixture.
"""
import re

REFERENCE_ID = re.compile(
    r"^(?:W\d{2}|H\d{3}|MEM\d{2}|R\d{2}[A-Z]?|NP\d{2}|REL\d{2}|"
    r"PR\d{2}|ORG\d{2}|D\d{2}|K\d{2}|MAT\d{2}|BIO\d{2}|T\d{2})$")
CATEGORIES = (
    ("MEM","ACTOR_ACCESSIBLE_MEMORY_OR_HISTORY_REFERENT"),
    ("MAT","OTHER_SEMANTIC_GROUNDING_REFERENT"),
    ("ORG","ORGANIZATIONAL_OR_INSTITUTIONAL_REFERENT"),
    ("REL","RELATIONAL_REFERENT"),
    ("BIO","OTHER_SEMANTIC_GROUNDING_REFERENT"),
    ("PR","TASK_PROJECT_OBLIGATION_REFERENT"),
    ("NP","RELATIONAL_REFERENT"),
    ("H","ACTOR_ACCESSIBLE_MEMORY_OR_HISTORY_REFERENT"),
    ("R","RELATIONAL_REFERENT"),
    ("T","OTHER_SEMANTIC_GROUNDING_REFERENT"),
    ("K","OTHER_SEMANTIC_GROUNDING_REFERENT"),
    ("D","OTHER_SEMANTIC_GROUNDING_REFERENT"),
    ("W","PHYSICAL_SCENE_REFERENT"),
)

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def category(identifier):
    require(isinstance(identifier,str) and REFERENCE_ID.fullmatch(identifier),
            "INVALID_SOURCE_ID: " + repr(identifier))
    return next(kind for prefix,kind in CATEGORIES if identifier.startswith(prefix))

def compile_grounding(packet):
    """Allow IDs only from typed, actor-visible input locations for THIS case/arm."""
    payload=packet["model_payload"]
    shared=payload["shared"]
    items={}
    def add(identifier,kind,field,delivery="GROUNDING_ONLY_NOT_NARRATION_PERMISSION"):
        require(identifier in ("NADIA","P0") or REFERENCE_ID.fullmatch(identifier),
                "BAD_GROUNDING_ID: "+repr(identifier))
        if identifier in items:
            row=items[identifier]
            require(row["class"] == kind, "GROUNDING_CLASS_MISMATCH: "+identifier)
            row["sources"].append(field)
            row["delivery"].add(delivery)
        else:
            items[identifier]={"class":kind,"sources":[field],"delivery":{delivery},
                               "physical":kind=="PHYSICAL_SCENE_REFERENT"}
    add("NADIA","ACTOR_OR_PARTICIPANT_REFERENT",
        "shared.actor_projection_exact_from_RFA05.actor_identity")
    add("P0","ACTOR_OR_PARTICIPANT_REFERENT","shared.exact_user_event.speaker")
    physical=set()
    for i,row in enumerate(shared["scene"]["facts"]):
        identifier=row["source_ref"]
        require(category(identifier)=="PHYSICAL_SCENE_REFERENT",
                "SCENE_FACT_NOT_WORLD_REF: "+identifier)
        require(identifier not in physical,"DUPLICATE_SCENE_REF: "+identifier)
        physical.add(identifier)
        add(identifier,"PHYSICAL_SCENE_REFERENT",f"shared.scene.facts[{i}].source_ref")
    proj=shared["actor_projection_exact_from_RFA05"]
    require(set(proj["scene_documented_refs"])==physical,"SCENE_REF_SET_DIFFERS")
    pattern=re.compile(
        r"^(W\d{2}|H\d{3}|MEM\d{2}|R\d{2}[A-Z]?|NP\d{2}|REL\d{2}|"
        r"PR\d{2}|ORG\d{2}|D\d{2}|K\d{2}|MAT\d{2}|BIO\d{2}|T\d{2})"
        r"(?: (partial|fragment|known false to actor|actor-private))?$")
    for i,annotation in enumerate(proj["actor_accessible_refs"]):
        match=pattern.fullmatch(annotation)
        require(match is not None,"UNKNOWN_ACTOR_REF_ANNOTATION: "+annotation)
        identifier=match.group(1)
        kind=category(identifier)
        if kind=="PHYSICAL_SCENE_REFERENT":
            require(identifier in physical,"UNSUPPORTED_PHYSICAL_REF: "+identifier)
        add(identifier,kind,f"shared.actor_projection_exact_from_RFA05.actor_accessible_refs[{i}]")
    ext=payload.get("whole_person_extension")
    if ext is not None:
        for field in ("whole_current_developed_person",
                      "selectively_retrieved_biographical_anchors",
                      "event_relevant_accessible_memory_or_safe_effects"):
            for i,row in enumerate(ext[field]):
                identifier=row["id"]
                kind=category(identifier)
                require(kind!="PHYSICAL_SCENE_REFERENT","WORLD_ID_IN_PERSON_EXTENSION")
                add(identifier,kind,f"whole_person_extension.{field}[{i}].id",row["delivery"])
        relations=ext["differentiated_relations"]
        for field in ("objective_shared_episodes","Nadia_perceived_P0","other_distinct_relations"):
            for i,row in enumerate(relations[field]):
                identifier=row["id"]
                require(category(identifier)=="RELATIONAL_REFERENT","INVALID_RELATION_CLASS")
                add(identifier,"RELATIONAL_REFERENT",
                    f"whole_person_extension.differentiated_relations.{field}[{i}].id",
                    row["delivery"])
    return {id_:{**entry,"delivery":sorted(entry["delivery"])}
            for id_,entry in sorted(items.items())}
