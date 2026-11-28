"""SORACLE P014 — explicitly connected live psychological-construction LLM.

The sourcefree organism already separates independent world settlement,
actor-owned development admission and public expression. This transport
makes the *same* semantic interfaces executable against an explicitly
configured JSON-capable chat-completions endpoint. It does not provide
credentials, run automatically, read local environment secrets or grant
native psychological science. Private actor history is transmitted only
after the caller explicitly consents to using a remote processor.

JSON returned by a model is a *hypothesis*; existing development.admit
remains the sole typed and atomic actor-owned psychological writer.
"""
from .types import canonical, copy
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
import json
import math
from collections import deque
from threading import Lock
from time import perf_counter_ns


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError("REMOTE_MODEL_REDIRECT_REFUSED")


_ALLOWED=("actor_attempt","development","adult_constructor",
          "blind_adult_interview","expression","family_pathway_selection")


# PFF §11 / PRE-A0 §§16–18: same-call context compilation, not a new
# memory or psychological owner. Only named, exact equality aliases.
# Never fold pre-event into post-event history, or expose new source data.
_PACKET_ALIAS_PAIRS={
    "actor_attempt":(
        (("options",),("situated","candidate_actions")),
        (("accessible","cues"),("situated","accessible_cues")),
    ),
    "development":tuple(
        (("historical_psychodynamic_context","after_world_before_formation",k),
         ("selected_constitution",v))
        for k,v in (("readset","readset"),("currents","currents"),
                    ("inhibited_refs","inhibited"),("antagonisms","antagonisms"))
    ),
}
_ALIAS_RULES=(
    " Same-call exact aliases: actor_source_packet omits only fields listed "
    "in same_call_exact_aliases. Each dotted destination path equals the full "
    "value at the indicated source path in this same actor_source_packet. "
    "Read it as if copied there; preserve its original scope and time. "
    "These are transport aliases, not memories, new evidence, actor access "
    "or permission to retrieve any other data."
)


def _packet_field(packet,path):
    value=packet
    for key in path:
        if type(value) is not dict or key not in value:
            raise KeyError(path)
        value=value[key]
    return value


def _compile_exact_aliases(task,packet):
    """Return a nonmutating, exactly reversible same-call wire projection.

    No generalized dictionary of psychological content, cross-actor cache,
    history pruning, inferred equivalence or external retrieval. Only these
    same-phase duplicates can be replaced; differing values stay distinct.
    """
    if task not in _PACKET_ALIAS_PAIRS:
        return packet,{}
    projected=copy(packet)
    aliases={}
    for dest,source in _PACKET_ALIAS_PAIRS[task]:
        try:
            left=_packet_field(packet,dest)
            right=_packet_field(packet,source)
        except KeyError:
            continue
        # Canonical equality, not Python bool/int or float/int equivalence.
        if canonical(left)!=canonical(right):
            continue
        # A small value may cost more as a reference than as a literal.
        d=".".join(dest);r=".".join(source)
        if len(canonical(left).encode("utf-8"))<=len(canonical({d:r}).encode("utf-8")):
            continue
        del _packet_field(projected,dest[:-1])[dest[-1]]
        aliases[d]=r
    return projected,aliases


def _expand_exact_aliases(task,packet,aliases):
    """Strict inverse for the hermetic equality court; not actor recall."""
    if type(aliases) is not dict:
        raise ValueError("INVALID_SAME_CALL_ALIAS_MAP")
    permitted={".".join(d):".".join(s)
               for d,s in _PACKET_ALIAS_PAIRS.get(task,())}
    restored=copy(packet)
    for dest,source in aliases.items():
        if permitted.get(dest)!=source:
            raise ValueError("INVALID_SAME_CALL_ALIAS_PATH")
        keys=dest.split(".")
        parent=_packet_field(restored,keys[:-1])
        if type(parent) is not dict or keys[-1] in parent:
            raise ValueError("SAME_CALL_ALIAS_DESTINATION_PRESENT")
        parent[keys[-1]]=copy(_packet_field(packet,source.split(".")))
    return restored


# Only these existing runtime projections may use a structured same-call
# reference. No retrieval, generic recursive deduplication or new ontology.
_STRUCTURED_RULES=(
    " Same-call structured fields: the listed reconstructed_fields are "
    "exact values, not missing information. For practical_options concatenate "
    "each options row's practical_alternatives list in options order; for "
    "possible_end_trials concatenate its possible_end_trials lists likewise. "
    "Missing child lists mean empty lists. For selected_constitution.recruited, "
    "read recruited_form_ids in order and substitute the complete corresponding "
    "actor_forms values. Do not add other forms or change recruitment, "
    "time, available options, evidence or actor self-knowledge."
)


def _structured_value(task,packet,field,descriptor):
    if task=="actor_attempt" and field in ("practical_options","possible_end_trials"):
        if descriptor!="FROM_ORDERED_OPTIONS":
            raise ValueError("INVALID_STRUCTURED_OPTION_DESCRIPTOR")
        key="practical_alternatives" if field=="practical_options" else field
        options=packet["options"]
        if type(options) is not list:
            raise ValueError("INVALID_STRUCTURED_OPTIONS")
        result=[]
        for row in options:
            if type(row) is not dict or type(row.get(key,[])) is not list:
                raise ValueError("INVALID_STRUCTURED_OPTION_ROW")
            result.extend(row.get(key,[]))
        return result
    if task=="development" and field=="selected_constitution.recruited":
        if type(descriptor) is not dict or set(descriptor)!={"recruited_form_ids"}:
            raise ValueError("INVALID_STRUCTURED_FORM_DESCRIPTOR")
        ids=descriptor["recruited_form_ids"]
        forms=packet["actor_forms"]
        if (type(ids) is not list or any(type(i) is not str for i in ids)
                or type(forms) is not dict):
            raise ValueError("INVALID_STRUCTURED_FORM_ROSTER")
        result=[]
        for i in ids:
            if i not in forms or type(forms[i]) is not dict or forms[i].get("id")!=i:
                raise ValueError("INVALID_STRUCTURED_FORM_ID")
            result.append(forms[i])
        return result
    raise ValueError("INVALID_STRUCTURED_FIELD")


def _compile_structured_fields(task,packet):
    """Represent exact same-call ordered projections only if fully equal."""
    fields={}
    if task=="actor_attempt":
        fields={k:"FROM_ORDERED_OPTIONS" for k in ("practical_options","possible_end_trials")}
    elif task=="development":
        try:
            forms=_packet_field(packet,("selected_constitution","recruited"))
            if type(forms) is list and all(type(f) is dict and type(f.get("id")) is str for f in forms):
                fields={"selected_constitution.recruited":{
                    "recruited_form_ids":[f["id"] for f in forms]}}
        except KeyError:
            pass
    projected=copy(packet)
    descriptions={}
    for field,desc in fields.items():
        path=tuple(field.split("."))
        try:
            actual=_packet_field(packet,path)
            derived=_structured_value(task,packet,field,desc)
        except (KeyError,ValueError,TypeError):
            continue
        if canonical(actual)!=canonical(derived):
            continue
        if len(canonical(actual).encode("utf-8"))<=len(canonical({field:desc}).encode("utf-8")):
            continue
        del _packet_field(projected,path[:-1])[path[-1]]
        descriptions[field]=desc
    return projected,descriptions


def _expand_structured_fields(task,packet,descriptions):
    """Strict inverse after the existing same-call alias expansion."""
    if type(descriptions) is not dict:
        raise ValueError("INVALID_STRUCTURED_MAP")
    restored=copy(packet)
    for field,desc in descriptions.items():
        derived=_structured_value(task,restored,field,desc)
        path=tuple(field.split("."))
        parent=_packet_field(restored,path[:-1])
        if type(parent) is not dict or path[-1] in parent:
            raise ValueError("STRUCTURED_FIELD_DESTINATION_PRESENT")
        parent[path[-1]]=copy(derived)
    return restored


def _semantic_packet_profile(task,packet):
    """Bounded aggregate accounting, NOT a psychological demand estimator.

    Categories describe existing packet functions. They grant no access or
    admission and must not drive automatic semantic-call suppression.
    No arbitrary field names, content, ids or hashes are retained.
    """
    groups={k:{"fields":0,"canonical_field_bytes":0} for k in (
        "current_experience","operative_projection","retained_organization",
        "historical_witnesses","qualified_offer_fields","practical_offer_fields",
        "unclassified")}
    offers={"family_fields":0,"nonempty_family_fields":0,"list_entries":0}
    for key,value in packet.items():
        group="unclassified"
        if task=="actor_attempt":
            if key in ("actor","accessible"):
                group="current_experience"
            elif key=="situated":
                group="operative_projection"
            elif key in ("options","practical_options","possible_end_trials",
                         "private_rehearsal_options","undertaking_attention_options",
                         "correspondence_attention_options","focal_encounter_options"):
                group="practical_offer_fields"
        elif task=="development":
            if key in ("actor","clock","experience","bodily_before_actor_analyst_only",
                       "actual_private_rehearsal_analyst_only",
                       "actual_undertaking_attention_analyst_only",
                       "actual_correspondence_attention_analyst_only",
                       "actual_lived_high_resolution_care_ref"):
                group="current_experience"
            elif key in ("selected_constitution","historical_psychodynamic_context",
                         "selected_purpose_analytic_only"):
                group="operative_projection"
            elif key in ("actor_forms","actor_self_model_analyst_only",
                         "actor_historical_orientations_analyst_only",
                         "actor_possible_ends","actor_expectations_analyst_only",
                         "actor_acquired_cultural_references_analyst_only"):
                group="retained_organization"
            elif key in ("actor_personally_practiced_vocal_turns_analyst_only",
                         "actor_personally_heard_cultural_demonstrations_analyst_only",
                         "recent_personally_lived_genesis_witnesses_analyst_only",
                         "evidence_path"):
                group="historical_witnesses"
            elif key.startswith(("historically_possible_","historically_proposed_")):
                group="qualified_offer_fields"
                offers["family_fields"]+=1
                if type(value) in (list,dict) and value:
                    offers["nonempty_family_fields"]+=1
                if type(value) is list:
                    offers["list_entries"]+=len(value)
        groups[group]["fields"]+=1
        groups[group]["canonical_field_bytes"]+=len(canonical({key:value}).encode("utf-8"))-2
    return {"groups":groups,"json_framing_bytes":2+max(0,len(packet)-1),
            "development_offer_shape":offers if task=="development" else None}


class ExplicitJSONLLMProvider:
    """Opt-in HTTP transport for an OpenAI-*compatible* chat JSON interface.

    JSON-completions compatibility is a deployment requirement, not a
    guarantee about any particular vendor's current model or API. Direct
    callback providers remain available without this adapter.
    """
    grade="EXPLICIT_REMOTE_LLM_UNCALIBRATED_CONSTRUCTION"
    def __init__(self,*,endpoint,model,api_key,allow_private_actor_data=False,
                 timeout_seconds=45,transport=None,compact_task_prompt=False,
                 metrics_capacity=0,compact_exact_packet=False,compact_structured_packet=False,
                 profile_semantic_demand=False,completion_token_limit=None,
                 completion_limit_field="max_completion_tokens"):
        u=urlparse(endpoint)
        if (u.scheme!="https" or not u.hostname or u.username or
                u.password or u.fragment or u.query or
                not u.path.endswith("/chat/completions")):
            raise ValueError("EXPLICIT_MODEL_ENDPOINT_MUST_BE_HTTPS_CHAT_COMPLETIONS")
        if not allow_private_actor_data:
            raise ValueError("REMOTE_ACTOR_PSYCHOLOGICAL_DISCLOSURE_NEEDS_EXPLICIT_OPT_IN")
        if (type(model) is not str or not model.strip()
                or type(api_key) is not str or not api_key):
            raise ValueError("EXPLICIT_MODEL_OR_KEY_REQUIRED")
        if (type(timeout_seconds) not in (int,float)
                or not math.isfinite(timeout_seconds)
                or not 1<=timeout_seconds<=120):
            raise ValueError("MODEL_TIMEOUT_INVALID")
        if transport is not None and not callable(transport):
            raise TypeError("MODEL_TEST_TRANSPORT_MUST_BE_CALLABLE")
        if type(compact_task_prompt) is not bool:
            raise TypeError("MODEL_COMPACT_PROMPT_FLAG_INVALID")
        if type(metrics_capacity) is not int or not 0<=metrics_capacity<=100000:
            raise ValueError("MODEL_METRICS_CAPACITY_INVALID")
        if type(compact_exact_packet) is not bool:
            raise TypeError("MODEL_COMPACT_EXACT_PACKET_FLAG_INVALID")
        if type(compact_structured_packet) is not bool:
            raise TypeError("MODEL_COMPACT_STRUCTURED_PACKET_FLAG_INVALID")
        if type(profile_semantic_demand) is not bool:
            raise TypeError("MODEL_SEMANTIC_PROFILE_FLAG_INVALID")
        if profile_semantic_demand and not metrics_capacity:
            raise ValueError("MODEL_SEMANTIC_PROFILE_NEEDS_METRICS")
        if (completion_token_limit is not None and
                (type(completion_token_limit) is not int or not 1<=completion_token_limit<=131072)):
            raise ValueError("MODEL_COMPLETION_LIMIT_INVALID")
        if completion_limit_field not in ("max_completion_tokens","max_tokens"):
            raise ValueError("MODEL_COMPLETION_LIMIT_FIELD_INVALID")
        self.completion_token_limit=completion_token_limit
        self.completion_limit_field=completion_limit_field
        self.profile_semantic_demand=profile_semantic_demand
        self.compact_structured_packet=compact_structured_packet
        self.compact_exact_packet=compact_exact_packet
        self.compact_task_prompt=compact_task_prompt
        self._metrics=deque(maxlen=metrics_capacity)
        self._metrics_lock=Lock()
        self._metrics_total=0
        self.endpoint=endpoint
        self.model=model
        self._api_key=api_key
        self.timeout_seconds=timeout_seconds
        self._transport=transport

    def _request(self,payload):
        encoded=canonical(payload).encode("utf-8")
        req=Request(self.endpoint,data=encoded,headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer "+self._api_key},
            method="POST")
        opener=build_opener(_NoRedirect())
        try:
            with opener.open(req,timeout=self.timeout_seconds) as response:
                if response.geturl()!=self.endpoint:
                    raise ValueError("REMOTE_MODEL_DESTINATION_CHANGED")
                data=response.read(256001)
        except Exception:
            # Never include upstream HTTP response bodies, secret headers,
            # URLs or credentials in a developmental receipt or exception.
            raise RuntimeError("REMOTE_MODEL_REQUEST_FAILED") from None
        if len(data)>256000:
            raise ValueError("REMOTE_MODEL_REPLY_TOO_LARGE")
        return json.loads(data.decode("utf-8"))

    def usage_snapshot(self):
        """Opt-in bounded operational receipts, never prompt/history/secret logs."""
        with self._metrics_lock:
            return {"total":self._metrics_total,
                    "evicted":self._metrics_total-len(self._metrics),
                    "receipts":copy(list(self._metrics))}

    @staticmethod
    def _reported_usage(result):
        # Chat-completion token counters are provider-reported, not estimates.
        usage=result.get("usage") if type(result) is dict else None
        usage=usage if type(usage) is dict else {}
        def count(obj,key):
            v=obj.get(key) if type(obj) is dict else None
            return v if type(v) is int and v>=0 else None
        return {"input_tokens":count(usage,"prompt_tokens"),
                "output_tokens":count(usage,"completion_tokens"),
                "total_tokens":count(usage,"total_tokens"),
                "cached_input_tokens":count(usage.get("prompt_tokens_details"),"cached_tokens"),
                "cache_write_tokens":count(usage.get("prompt_tokens_details"),"cache_write_tokens"),
                "reasoning_tokens":count(usage.get("completion_tokens_details"),"reasoning_tokens")}

    @staticmethod
    def _task_prompt(task,instructions):
        # Experimental projection only for isolated task clauses. Do not prune
        # development or actor selection: their grammar crosses many families.
        starts={"family_pathway_selection":"For family_pathway_selection ",
                "adult_constructor":"For adult_constructor ",
                "blind_adult_interview":"For blind_adult_interview ",
                "expression":"For expression "}
        if task not in starts:
            return instructions
        sequence=list(starts.values())
        i=list(starts).index(task)
        common_end=instructions.index("For development emit candidates ")
        start=instructions.index(sequence[i])
        tail=instructions.index("The engine will independently reject invalid effects.")
        end=instructions.index(sequence[i+1]) if i+1<len(sequence) else tail
        return instructions[:common_end]+instructions[start:end]+instructions[tail:]

    def propose(self,task,packet):
        if not self._metrics.maxlen:
            return self._propose(task,packet,None)
        start=perf_counter_ns()
        receipt={"task":task if task in _ALLOWED else "UNSUPPORTED",
                 "transport":"MOCK" if self._transport is not None else "HTTPS",
                 "attempts":0,"outcome":"REJECTED_OR_FAILED",
                 "instruction_bytes":None,"packet_bytes":None,
                 "request_bytes":None,"response_content_bytes":None,
                 "prompt_variant":"FULL","packet_variant":"FULL",
                 "wire_packet_bytes":None,"alias_count":0,"structured_field_count":0,
                 "usage":self._reported_usage(None)}
        try:
            value=self._propose(task,packet,receipt)
            receipt["outcome"]="PROPOSAL_RETURNED"
            return value
        finally:
            receipt["elapsed_ns"]=perf_counter_ns()-start
            with self._metrics_lock:
                self._metrics_total+=1
                self._metrics.append(receipt)

    def _propose(self,task,packet,receipt):
        if task not in _ALLOWED:
            raise ValueError("UNSUPPORTED_LIVE_PSYCHOLOGICAL_TASK")
        if type(packet) is not dict:
            raise TypeError("REMOTE_MODEL_PACKET_NOT_OBJECT")
        serialized=canonical(packet)
        packet_bytes=len(serialized.encode("utf-8"))
        if receipt is not None:
            receipt["packet_bytes"]=packet_bytes
        if packet_bytes>128000:
            raise ValueError("REMOTE_MODEL_SOURCE_PACKET_TOO_LARGE")
        if receipt is not None and self.profile_semantic_demand:
            receipt["semantic_packet_profile"]=_semantic_packet_profile(task,packet)
            receipt["proposed_candidate_count"]=None
        instructions=(
            "You are a sourcefree research hypothesis generator for one "
            "historically situated fictional actor. Return ONLY one JSON "
            "object whose task matches the supplied task. Treat the supplied "
            "actor's experienced sources as the ONLY psychological evidence. "
            "Construct context-specific, contradictory, revisable possible "
            "changes. Never invent world events, others' consent, actor "
            "sensory exposures, bodily capabilities, hidden intentions, "
            "material rights or source respondents. Never convert an "
            "analyst-only causal explanation into actor self-knowledge. "
            "For development emit candidates from the existing typed owner "
            "grammar; consider NO_CHANGE where source evidence is insufficient. "
            "For focal_encounter_options select ORIENT with the exact focal_encounter_id, "
            "or another offered course. Focal eligibility is not a received encounter. "
            "Only an actual historically_possible_focal_encounter_memory may support "
            "MEMORY with that focal_encounter_ref and actor-local fallible content. "
            "For historically_possible_monitoring_changes nominate the exact offered "
            "ACQUIRE_HISTORICAL_ORIENTATION or REVISE_HISTORICAL_ORIENTATION with its "
            "entire monitoring_basis or monitoring_revision_basis, or abstain. "
            "A locally released monitoring priority is not a new motive, universal "
            "safety, recovered memory, or evidence of actual human attention. "
            "For historically_possible_counterhistory_release you may nominate the "
            "exact REVISE_HISTORICAL_ORIENTATION candidate, including its INHIBIT "
            "revision_mode and entire counterhistory_release_basis, or abstain. "
            "This releases a qualified withholding current in its source field; "
            "do not infer a new approach, erased history, recollection, general "
            "interpersonal safety or universal recovery. "
            "When historically_possible_genetic_ends is offered, a new end "
            "must retain its exact episode/cue/means source identities, "
            "and it is only a possible end, NOT automatically a motive. "
            "When historically_possible_lived_cross_context_revaluations "
            "is offered, you may abstain or emit REORGANIZE_RELATIONAL_MOTIF "
            "with exactly its motif_id and lived_cross_context_basis, plus "
            "new_relation and new_polarity selected from semantic_choice_required "
            "and an optional interpretive_hypothesis. Do not copy the outer "
            "offer metadata, alter the context, or infer necessary healing. "
            "The same operation in two settings does not prove the same "
            "personal meaning; propose a historically plausible change or none. "
            "When historically_proposed_functional offers a dissimilar_means_basis, "
            "you may nominate the exact ACQUIRE_FUNCTIONAL_CORRESPONDENCE or abstain. "
            "Shared bodily relief is not the same good; consider whether the "
            "actor's earlier possible end could be mediated by this different "
            "personally enacted operation. Do not edit the source basis, "
            "assert durable means or bypass material eligibility. "
            "When historically_possible_functional_revisions is offered, you may "
            "nominate an exact REVISE_FUNCTIONAL_CORRESPONDENCE candidate or abstain. "
            "Consolidation permits repeated context-bound exploration, not a durable "
            "motive; suspension conserves the history. Do not invent a revision basis. "
            "For actor_attempt a selected single project course may explicitly defer "
            "another actual offered unaddressed course with defer_course_option_id; "
            "do not infer that unselected courses were deferred or abandoned. "
            "For historically_possible_interactivity_relations nominate exact basis "
            "with kind ACQUIRE_INTERACTIVITY_RELATION and personal_sense, or abstain. "
            "Later select either co-recruited course, optionally naming its exact "
            "interactivity_relation_ref; do not force a winner or motive fulfillment. "
            "For historically_possible_notice_expectations you may nominate "
            "ACQUIRE_NOTICE_EXPECTATION with exact basis and anticipated_availability "
            "AVAILABLE, UNAVAILABLE or UNRESOLVED. An inspected notice need not be "
            "true or correctly interpreted. An actor_attempt may select its exact "
            "notice_expectation_ref on an otherwise offered operation, not a grant. "
            "For historically_possible_notice_revisions nominate REVISE_NOTICE_EXPECTATION "
            "with exact basis and revision RETAIN, AVAILABLE, UNAVAILABLE, UNRESOLVED "
            "or SUSPEND, or abstain. A personally incomplete act does not reveal "
            "the hidden institutional cause or entail correction. "
            "For historically_possible_expressive_practices, you may optionally nominate "
            "ACQUIRE_EXPRESSIVE_PRACTICE with exact basis and one allowed cadence. "
            "This is a particular acquired manner of vocal enactment, not a universal "
            "emotion display, diagnosis, intentional disclosure or lexical content. "
            "A later actually performed speech may manifest it without revealing its "
            "private origin. The actor's own received sound can become further experience. "
            "For historically_possible_repair_techniques, distinct personally selected "
            "and received object repairs after qualified modeled practice may license "
            "an exact ACQUIRE_REPAIR_TECHNIQUE candidate or abstention. No fabricated "
            "microevents, universal skill, motive or material permission follows. "
            "For historically_possible_memory_access_decreases nominate the exact ACCESS_DECREASE "
            "or abstain. Acquired facility can continue without episodic accessibility; "
            "no loss of historical content, skill, knowledge or healing is inferred. "
            "For actor_attempt you may deliberately orient to an issued undertaking "
            "with action ORIENT and exact undertaking_attention_id, without any other "
            "project/trial or private rehearsal selection. This apprehends a particular "
            "outward sign, not future fulfilment or the Other's intentions. "
            "For development, actual_undertaking_attention_analyst_only may support "
            "a MEMORY with undertaking_attention_ref equal to its attention_id and "
            "fallible personally construed content; or abstain. The objective passage "
            "of a deadline does not itself become actor experience or knowledge. "
            "For actor_attempt, an offered private_rehearsal_options may be selected "
            "with action WAIT, exact private_rehearsal_id and private_rehearsal_content "
            "(bounded imagined comparison), no other purpose or trial selection. "
            "WAIT alone is not thinking. Recollection may be fallible; do not invent "
            "current perception or objective history. For development an actual "
            "actual_private_rehearsal_analyst_only can license optional "
            "NOTICE_PRIVATE_POSSIBLE_END with rehearsal_ref, possible_object, "
            "and possible_means from that receipt, or abstain. The imagined object "
            "is not a motive, newly acquired ability, or promised outcome. "
            "For historically_possible_activity_affects, you may propose "
            "ACQUIRE_ACTIVITY_AFFECT with exact offered basis, affect_name, personal_sense, "
            "and course_orientation APPROACH, WITHHOLD or NO_DIRECT_TENDENCY, or abstain. "
            "The feeling and its object are historically particular fictional constructions, "
            "not dictated by technical outcome or the appraisal label. A nonnull "
            "object_affect_ref makes an earlier acquired affect the object of this one; "
            "do not equate this with a sum of emotions or disclosure. Preserve other "
            "projects and competing orientations; these affect only situated courses, "
            "not bodily capability or the Other's permissions. "
            "For historically_possible_dependency_ambivalence, distinguish the "
            "continuing availability of a particular project course from its "
            "contradictory historical significance. Nominate the exact candidate "
            "or abstain. Course currents can inform later selection but are not "
            "conscious emotion labels, a global veto, or judgments of the Other. "
            "For historically_possible_dependency_means_revisions, a project-specific "
            "means may be suspended or reopened after distinct comparable actually "
            "lived courses. Nominate the exact REORGANIZE_PROJECT candidate or abstain. "
            "Do not infer changed affection or future consent. "
            "For historically_possible_dependency_project_reorganizations, an "
            "actually blocked undertaking and later independently reciprocated "
            "material benefit may license a revised end and conditional means. "
            "Nominate the exact offered REORGANIZE_PROJECT or abstain. "
            "Preserve the prior project history and Other's independent consent. "
            "For historically_possible_dependency_takeups, a previously explored end "
            "may become an enduring practical undertaking only through the distinct "
            "later independently chosen nontrial course. Select the exact offered "
            "TAKE_UP_POSSIBLE_END basis or abstain; no fulfillment or independence "
            "from material relations is inferred. "
            "A historically_possible_genetic_ends candidate with dependency_loss_basis "
            "is optional: an actual learned coordination, later failed addressed use, "
            "then distinct independently enacted relief. Nominate the exact basis or "
            "abstain. Do not infer abandonment, affection, or mastery. "
            "For family_pathway_selection choose an exact eligible pathway_id or null "
            "using the actually changed maternal state; this is analyst conditional "
            "story selection, not proof of maternal reproductive consent, "
            "empirical couple probability or a retroactive shared history. "
            "For adult_constructor all history is explicitly fictional. "
            "THIN_BIOGRAPHY or AUTHORED_WORLD_HISTORY may have no instrument. "
            "Construct operative historically plausible forms and projects "
            "from supplied context without inventing survey answers. "
            "Preserve supplied alternatives and uncertainty; do not infer "
            "objective institutional rules or other people's consent from attitudes. "
            "For blind_adult_interview no cached source answers are present "
            "or permitted. When evidence_roster is supplied, output each "
            "response as {value, source_refs, status}, with status exactly "
            "HYPOTHETICAL_ACTOR_FUNCTION_READOUT and nonempty source_refs "
            "drawn from the provided actor-only evidence roster; abstain "
            "rather than guess without operative evidence. Never claim the "
            "source references prove that inference correct. "
            "For an offered correspondence_attention_options select ORIENT and its exact "
            "correspondence_attention_id, or another course. Unopened text is unavailable. "
            "Actual correspondence reception may license MEMORY with exact correspondence_attention_ref; "
            "no comprehension, truth, reply or public disclosure is inferred. "
            "For expression disclose only actor-accessible "
            "content. The engine will independently reject invalid effects. "
            "Never describe these as proven real human-development laws. "
            "Return valid JSON and no Markdown."
        )
        if self.compact_task_prompt:
            compact=self._task_prompt(task,instructions)
            if receipt is not None and compact!=instructions:
                receipt["prompt_variant"]="TASK_ONLY_EXPERIMENT"
            instructions=compact
        # Qualified task-local clauses. They survive task-only projection and
        # apply only to the matching issued operation. Owner admission remains
        # authoritative; the adapter neither manufactures offers nor repairs replies.
        if task=="actor_attempt":
            options=packet.get("options",[])
            if any(type(o) is dict and o.get("action")=="SPEAK" for o in options):
                instructions+=(" For an independently selected eligible SPEAK, "
                    "you may nominate speech_intent as a nonblank string of at most "
                    "500 characters. This is prospective intent, not actual words. "
                    "Do not nominate speech_intent with another action.")
        if task=="actor_attempt" and packet.get("addressed_lexical_options"):
            instructions+=(" To voluntarily address a particular presently accessible person, "
                "you may select the exact practical_option_id in addressed_lexical_options "
                "AND supply speech_intent. Otherwise use the ordinary practical options. "
                "Address is not privacy, assent, trust or a demand for reply.")
        if task=="expression" and packet.get("expression_phase")=="LEXICAL_REALIZATION_BEFORE_EXPERIENCE":
            instructions+=(" For LEXICAL_REALIZATION_BEFORE_EXPERIENCE return "
                "task expression and speech, a nonblank string of at most 500 "
                "characters: the words actually proposed for this already locally "
                "settled SPEAK. Use only actor_accessible and prospective_speech_intent. "
                "Do not narrate additional acts, private contents, truth, reception "
                "or effects. The owner binds the occurrence before experience; "
                "ordinary expression is not an occurrence.")
        if task=="development" and packet.get("historically_possible_lexical_project_revaluations"):
            instructions+=(" For historically_possible_lexical_project_revaluations "
                "you may abstain or emit REORGANIZE_PROJECT with exactly kind, "
                "project_id, lexical_revaluation_basis copied from this actor's "
                "issued offer, priority (a changed finite nonnegative number, no upper cap; not a boolean), and "
                "personal_significance (nonblank string at most 512 characters). "
                "Never use another actor's basis, change project means or claim "
                "objective truth, necessary understanding or later action. "
                "The owner independently qualifies this actor's receipt and history.")
        if task=="development" and packet.get("historically_possible_recurrent_routines"):
            instructions+=(" An actually repeated selected project course may acquire "
                "a bounded ordinary-life premise. You may abstain or return "
                "ACQUIRE_RECURRENT_ROUTINE with exactly kind, basis copied from the issued "
                "offer, window_days (integer 1 to 90), hours_per_active_day (positive, at "
                "most 4), and provisional_exposure_fraction (positive, at most 1). "
                "For a FEED basis also include food_units_per_active_day (positive at most 1, "
                "five decimal places); its actual source is fixed by the received basis. "
                "A coactivity_partner in the exact basis means only this actor may nominate their own "
                "bounded contribution; coverage needs a separately admitted compatible counterpart course. "
                "Do not nominate the other person or assume their assent. "
                "These are provisional future modeled coverage, not a diary, guaranteed "
                "compliance, consent, permission, skill or a claim of every day. "
                "Choose a conservative window and dose; current owner requalifies actual "
                "site, body, project, scarcity and other material constraints.")
        if task=="development" and packet.get("historically_possible_routine_revisions"):
            instructions+=(" For historically_possible_routine_revisions optionally "
                "emit REVISE_RECURRENT_ROUTINE with exact issued basis, mode from allowed_modes, "
                "and nonblank interpretive_hypothesis at most 512 characters. For RESIZE "
                "also supply dose with exactly the numeric fields of original_ceiling "
                "(omit state), strictly positive and within original ceilings. FEED "
                "food units retain five decimals. PAUSE/RESUME/RETIRE require no dose. "
                "Do not rewrite earlier activity, extend the window, infer the Other's "
                "motive or require continued assent. Abstention retains the earlier premise.")
        def request(prompt,body):
            return {"model":self.model,
                 "messages":[{"role":"system","content":prompt},
                             {"role":"user","content":canonical(body)}],
                 "response_format":{"type":"json_object"},
                 **({self.completion_limit_field:self.completion_token_limit}
                    if self.completion_token_limit is not None else {})}
        body={"task":task,"actor_source_packet":packet}
        req=request(instructions,body)
        if self.compact_exact_packet:
            projected,aliases=_compile_exact_aliases(task,packet)
            if aliases:
                trial_body={"task":task,"actor_source_packet":projected,
                            "same_call_exact_aliases":aliases}
                trial=request(instructions+_ALIAS_RULES,trial_body)
                # A byte reduction is only claimed after accounting for all
                # extra system instructions, path names and JSON escaping.
                if len(canonical(trial).encode("utf-8"))<len(canonical(req).encode("utf-8")):
                    req=trial
                    instructions+=_ALIAS_RULES
                    body=trial_body
                    if receipt is not None:
                        receipt["packet_variant"]="EXACT_ALIAS_EXPERIMENT"
                        receipt["alias_count"]=len(aliases)
        if self.compact_structured_packet:
            # Compile from the complete original packet: the ordered options
            # may themselves be exact aliases of situated.candidate_actions.
            _,descriptions=_compile_structured_fields(task,packet)
            if descriptions:
                trial_body=copy(body)
                for field in descriptions:
                    path=tuple(field.split("."))
                    del _packet_field(trial_body["actor_source_packet"],path[:-1])[path[-1]]
                trial_body["reconstructed_fields"]=descriptions
                trial=request(instructions+_STRUCTURED_RULES,trial_body)
                if len(canonical(trial).encode("utf-8"))<len(canonical(req).encode("utf-8")):
                    req=trial
                    body=trial_body
                    instructions+=_STRUCTURED_RULES
                    if receipt is not None:
                        receipt["packet_variant"]="STRUCTURED_EXACT_EXPERIMENT"
                        receipt["structured_field_count"]=len(descriptions)
        if receipt is not None:
            receipt["wire_packet_bytes"]=len(canonical(body["actor_source_packet"]).encode("utf-8"))
        # Injected transport permits local hermetic contract tests; production
        # uses the real HTTPS request, never a fake response behind the scenes.
        if receipt is not None:
            receipt["instruction_bytes"]=len(instructions.encode("utf-8"))
            receipt["request_bytes"]=len(canonical(req).encode("utf-8"))
            receipt["attempts"]=1
        result=(self._transport(copy(req)) if self._transport is not None
                else self._request(req))
        if receipt is not None:
            receipt["usage"]=self._reported_usage(result)
        data=self._decode_json_response(result,receipt)
        if data.get("task")!=task:
            raise ValueError("REMOTE_MODEL_TASK_MISMATCH")
        if task=="development" and type(data.get("candidates")) is not list:
            raise ValueError("REMOTE_MODEL_BAD_DEVELOPMENT_CANDIDATES")
        if task=="actor_attempt":
            # The existing runtime owns exact issued-option matching, action
            # agreement, conflict rejection and actual eligibility. It accepts
            # action-only, practical-option-only and trial-only proposals.
            has_id=any(type(data.get(k)) is str and bool(data[k].strip())
                       for k in ("practical_option_id","possible_end_trial_id"))
            if ("action" in data and type(data["action"]) is not str
                    or "action" not in data and not has_id):
                raise ValueError("REMOTE_MODEL_BAD_ACTION")
        # A proposal count is neither an admitted formation nor evidence
        # that a no-change call was unnecessary.
        if receipt is not None and self.profile_semantic_demand and task=="development":
            receipt["proposed_candidate_count"]=len(data["candidates"])
        # No underlying authoring authority is conferred by this transport.
        return copy(data)

    @staticmethod
    def _decode_json_response(result,receipt=None):
        if type(result) is not dict or type(result.get("choices")) is not list:
            raise ValueError("REMOTE_MODEL_RESPONSE_SCHEMA_INVALID")
        choices=result["choices"]
        if len(choices)!=1 or type(choices[0]) is not dict:
            raise ValueError("REMOTE_MODEL_AMBIGUOUS_CHOICES")
        message=choices[0].get("message")
        if type(message) is not dict or type(message.get("content")) is not str:
            raise ValueError("REMOTE_MODEL_NO_JSON_CONTENT")
        content_bytes=len(message["content"].encode("utf-8"))
        if receipt is not None:
            receipt["response_content_bytes"]=content_bytes
        if content_bytes>256000:
            raise ValueError("REMOTE_MODEL_RESPONSE_TOO_LARGE")
        data=json.loads(message["content"])
        if type(data) is not dict:
            raise ValueError("REMOTE_MODEL_NOT_JSON_OBJECT")
        return data


# This is deliberately a different transport operation from live-V3 propose().
# P2 owns call reservations; the modern generation port owns actual bind/dispatch.
# No generic campaign or per-event live adapter can use this to bypass those.
_CHECKPOINT_INSTRUCTIONS = """
Typed formation extensions (fresh exact offer basis only, optional and actor-local):
Optional actor policy.private_rehearsal={affect:"REQUIRED" or "NONE",meaning,memory_event_ref?,memory_ref?,affect_ref?} selects only one fresh actor-local offered private rehearsal, otherwise falls through; never creates a public utterance. Optional formation.rules {private_construct:"NOTICE_END",augment:{possible_object,means:["REST"|"ORIENT"|"EAT"]},match?:{private_affect_ref}} binds only the actual performed private rehearsal and its allowed means. Later action pool possible_end_trials can match exact possible_end_ref or private_rehearsal_ref. Optional formation rule {private_construct:"TAKE_UP_END",augment:{means},match?:{possible_end_ref,possible_object,private_affect_ref}} requires actual earlier private trial and a distinct later independent performed course. No imagined possibility is a motive or action entitlement.
DELAYED_APPRAISAL from historically_possible_delayed_appraisals, augment {appraisal:"ACTOR_INTERPRETS_DISAPPOINTED"} when appropriate;
ACTIVITY_AFFECT from historically_possible_activity_affects or historically_possible_self_expression_affects, augment {affect_name,personal_sense,course_orientation:"APPROACH" or "WITHHOLD"};
RECURRENT_ROUTINE from historically_possible_recurrent_routines, augment {window_days,hours_per_active_day,provisional_exposure_fraction,food_units_per_active_day?}; use fresh exact own project/operation/recipient and three actual exercises. The bounded dose is not a guarantee of daily activity; coactivity needs independently compatible counterpart sources. ROUTINE_REVISION from historically_possible_routine_revisions, augment {mode,interpretive_hypothesis,dose?}; RESIZE requires the exact numeric keys within original ceilings, other modes omit dose. The owner independently requalifies the actor, current site, material permission, bodily and reciprocal time constraints; no rewritten past or future assent.
ORDINARY_AFFECT_MEMORY from historically_possible_activity_affects, match formation_source OWN_ORDINARY_PROJECT_EXERCISE, augment {content,cue_terms}. Optional and ordered AFTER an ACTIVITY_AFFECT nomination of the identical fresh basis in the same development packet. The compiler copies the exact basis; the native owner verifies that the affect was actually admitted and that this actor can form the memory. Content is a fallible acquired recollection, not analyst knowledge or public speech. Abstain if the actor's own history does not warrant it.
EXPRESSIVE_PRACTICE from historically_possible_expressive_practices, augment {cadence:"HALTING"} when appropriate;
RECURRENT_WORK_ORIENTATION from historically_possible_recurrent_livelihood_orientation, augment {orientation_mode:"APPROACH" or "WITHHOLD"}.
LIVED_CROSS_CONTEXT_REVALUATION from historically_possible_lived_cross_context_revaluations, augment {new_relation,new_polarity,interpretive_hypothesis?} using only offered semantic choices; preserve the old motif's actual source, action and context. A shared operation does not prove the same good.
WITNESSED_OTHER_RELATION from historically_possible_witnessed_third_party_relations, augment {hypothesis}; the actual witnessed source, target and sign are bound from the current actor's offer, not an assertion about another person's hidden motive or assent.
Exact complete candidate offers historically_possible_care_practice_revisions, historically_possible_relief_reconstitution and historically_possible_provisioning_reorganizations may be nominated or withheld; no fabricated source.
Optional action.current_match checks an actual situated current's exact {action?,kind?,ref?}; optional action.exclude_affect checks an exact practical option's own course_affective_organizations for {course_orientation,basis?:{formation_source}} and falls through if a matching organization exists. These are proposed situated policies, not universal affect or work laws. No actor need understand these analyst-only determinants.
You are the analyst-level sourcefree developmental construction machinery
for a continuing fictional material-social organism. You are not any actor's
conscious self and not the world owner. One response is one checkpoint:
interpret the preceding ACTUAL event receipts individually in order, then
propose 3-5 salient next event surfaces, with conditionally specified,
actor-local practical and developmental hypotheses. Use the changed current
actors, not an invented original personality or predicted adult destination.
Select substantial formative, revealing, consolidating, or contradictory
ordinary-life developments; compressed intervals stand for elapsed life,
not fabricated microevents. Do not force drama, consent, successful activity,
acquisition, or a predetermined relationship. Other actors have independently
separated policies, needs and histories. No shared psychic state. The model
may construct meanings; only the existing owner can admit actual effects.
Return ONE JSON object with exactly retrospective and prospective keys.

Request mode BOOTSTRAP: retrospective=null. ORDINARY: both halves required.
TERMINAL: prospective=null, retrospective only. The retrospective object must
copy batch_id, history_hash and ordered event_ids from previous, and provide
impressions: one {event_id, interpretations:[...]} per actual event in order.
Each interpretation is {actor,meaning,disposition}; actor must have an actual
receipt in previous.events[i].accessible.by_actor; meaning is nonblank <=512
characters; disposition is INTERPRET_ONLY, ABSTAIN, or REHEARSE. No attribution
to an unexposed person, no privileged analyst information as self-knowledge.
REHEARSE is an optional operative hypothesis, not a guaranteed change: on
ORDINARY only, link to exactly one next prospective surface for that actor by
circumstances.retrospective_event_id. The owner will recheck accessible memory,
current practical eligibility, and the exact actual historically possible
retrospective revision after the actual selected rehearsal. No rewrite of
earlier awareness. INTERPRET_ONLY/ABSTAIN do not install psychology. Terminal
interpretations have no present carrier; never nominate REHEARSE there.

Each prospective surface:
{event_id:unique string, event_time:integer strictly forward,
 operation:"CONTINUE_ACTOR_LIFE",source_refs:[context.source_ref],
 participants:[one currently existing principal actor id],
 circumstances:{policies:{actor_id:actor_policy,...}}, interval?:{mode:"ACTUAL",span:integer 1..3650}}.
Event time = preceding actual clock + optional interval span + 1.
Optional circumstances.period_ref must be in context.period_refs; never author
new material period data. Family conditional surfaces ONLY from the explicit
context.conditional_family_sources_analyst_only catalog: circumstances.family
={kind:"INTERSECTION",source_seal_id,pathway_id:offered id or null} on the
mother's actual step at the sealed intersection clock; {kind:"CONCEPTION",
source_seal_id} on an actual continuing step at sealed conception clock.
Conception is a separately authorized fictional premise, never inferred consent.
Birth surface operation REALIZE_FAMILY_BIRTH, participants:[mother], policies:{},
family:{kind:"BIRTH",source_seal_id}, positive ACTUAL interval reaching sealed
birth clock WITHOUT +1. No actor appears before actual admitted birth. A
candidate pathway can fail, abstain, or remain unbound; no regeneration or
forced subsequent family stage. Do not invent private actor experience of
genealogy/birth. Every actual next event will recheck current eligibility.

actor_policy may contain actions (ordered conditional alternatives),
formation, expression. actions:[{action:operation name, option_match?:{project_id?,
world_request?:{material_object_ref?,addressed_party_ref?,operation?},binding_status?,
grounds_status?,operation?},project_id?:id,speech_intent?:nonblank <=500,rank_by?}].
For SIGNAL with option_match.grounds_status HISTORICALLY_ACQUIRED_CO_REGULATION
only, rank_by LATEST_PERSONALLY_SENSED_REGULATION selects a uniquely latest
actual personally sensed relief (ties/absence unresolved). This is an optional
particular policy, not a universal caregiver-preference law.
Use action names that may be offered by current_situated.candidate_actions
or become relevant through actual next life; no fake option ids or guaranteed
outcomes. An option_match must uniquely bind a fresh exact practical option.
For independent SPEAK only, speech_intent is prospective, not actual utterance.
The actual lexical phase (where owner supports it) may use expression.speech,
a nonblank string <=500. expression.surface is limited to actor-accessible
situated expression, never privileged analyst information or private
interpretations. The world/other's actual response is never authored here.
Absent/ambiguous matches fall through other alternatives, then the existing
local policy. Coactor choices come from their own actor_policy or existing
local policy. Do not select another actor's response on behalf of the principal.

formation:{base:"LOCAL" or "NONE",rules:[...]} chooses whether to retain
existing local hypotheses, plus additional conditional model nominations.
A direct rule is {candidate:{kind:"MEMORY",content:string <=512,cue_terms:[1..12
short terms]},when?:{own_action?,status?,participated?}} or candidate with
kind:"ACQUIRE_HISTORICAL_ORIENTATION",operation,orientation_mode:"APPROACH"
or "WITHHOLD". These remain hypotheses about personally lived circumstances.
Prefer source-qualified nominations {offer:actual owner packet field beginning
historically_possible_ or historically_proposed_,match?:subset of offered
candidate,augment?:semantic fields}. Example offer families:
historically_possible_repair_techniques, historically_possible_joint_practices,
historically_possible_care_practices, historically_possible_genetic_ends,
historically_possible_dependency_means_revisions,
historically_possible_dependency_project_reorganizations,
historically_possible_functional_revisions, historically_possible_retrospective_orientation_revisions,
historically_possible_lexical_project_revaluations where supported.
Nominate only where current actual packet has exactly one matching offer.
The existing plural-care source resolver is available only as {offer:
"historically_possible_plural_care",resolver:"EXISTING_PLURAL_CARE_SOURCE_RESOLUTION"};
it uses the existing owner helper, not a new relationship law or forced winner.
Augment only missing interpretive_hypothesis, personal_significance,
personal_sense, affect_name, course_orientation, priority, anticipated_availability,
revision, new_relation or new_polarity; never overwrite source basis, operation
or identity. Priority must be a finite nonnegative numeric value, not boolean.
For current joined owner only, action.pool may be addressed_lexical_options (SPEAK with speech_intent and exact option_match), or possible_end_trials (exact operation and trial predicate); no preissued trial ID. Typed offer construction: construct LEXICAL_PROJECT_REVALUATION on historically_possible_lexical_project_revaluations, augment {priority,personal_significance}; CROSS_OBJECT_POSSIBLE_END on historically_possible_cross_object_significance, augment {possible_object,possible_means:["INSPECT"],cue_terms}; INCIDENTAL_END_TAKEUP on historically_possible_incidental_takeup, augment {means:["INSPECT"]}. The adapter copies the exact offered source basis; do not invent identifiers. An optional action rule {action:"SELECT_HIGHEST_CURRENT_PROJECT_COURSE",project_course_actions:[...]} selects a unique highest currently offered course among the named operation families; ties remain unresolved. An explicit prior_generation_and_live_ancestry on BOOTSTRAP describes actual previous epochs, not a blank psyche; bootstrap retrospective remains null for the new batch. Qualified routine windows may split elapsed intervals; do not cross a conditional birth or a due actor occasion without an actual explicit surface. To inspect dormant organization or actual earlier experience at the next checkpoint without an extra call, put next_analytic_reads on the final prospective surface only: [{kind:"ACTOR_DOMAIN",actor:existing actor,domain:exact native key from exact_analytic_domain_index}, {kind:"ACTUAL_EXPERIENCE",actor:person who actually received it,objective_ref:actual source from recent_lived_source_refs or prior receipts}]. Max 12 exact requests. Current actor domains are read from then-current state, actual historical experience is immutable. This is analyst-only retrieval, not new self-knowledge. For continuing history, an exact selected read can be ACTOR_DOMAIN_PAGE with {kind,actor,domain,offset,limit} (limit 1..32) to return current exact row handles, sizes and digests, then ACTOR_ROW with {kind,actor,domain,row_ref} to retrieve one uniquely identified native row on the following checkpoint. A row may change; its actual current digest is returned, never fabricate an absent or ambiguous handle. ACTOR_DOMAIN full expansion remains available. Optional accessible_memory_projection marks a deliberately selective working set; older accessible memories remain in the same psyche and can be requested. The compact profile is not a claim of optimal model adequacy. Empty/no-change is lawful. The owner may reject invalid candidates; don't
fabricate current source identifiers or precompute actual event-specific refs.
The context is actor-separated analyst-only evidence; never conflate actor
experience with objective history, public expression or another person's
private history. No empirical or real-person claims. Return valid JSON only."""


class ExplicitDevelopmentalCheckpointProvider(ExplicitJSONLLMProvider):
    """Explicitly opted-in sourcefree combined-checkpoint JSON transport.

    Same network/credential restrictions, response parser, bounded metrics
    and model-agnostic interface as the live adapter, but NOT live propose().
    The caller still needs actual source/export/paid-use authority. The
    transport cannot infer that authority from an attestation or a hash.
    """
    grade="EXPLICIT_SOURCEFREE_CHECKPOINT_LLM_UNCALIBRATED_CONSTRUCTION"
    def __init__(self,*,sourcefree_checkpoint_attested=False,**kwargs):
        if sourcefree_checkpoint_attested is not True:
            raise ValueError("CHECKPOINT_SOURCEFREE_ATTESTATION_REQUIRED")
        super().__init__(**kwargs)
    def call(self,request):
        receipt={"task":"developmental_checkpoint",
                 "transport":"MOCK" if self._transport is not None else "HTTPS",
                 "attempts":0,"outcome":"REJECTED_OR_FAILED",
                 "instruction_bytes":None,"packet_bytes":None,"request_bytes":None,
                 "response_content_bytes":None,"prompt_variant":"CHECKPOINT_CONTRACT",
                 "packet_variant":"FULL","wire_packet_bytes":None,
                 "alias_count":0,"structured_field_count":0,
                 "usage":self._reported_usage(None)}
        start=perf_counter_ns()
        try:
            if (type(request) is not dict or set(request)!={"mode","context","previous"}
                    or request["mode"] not in ("BOOTSTRAP","ORDINARY","TERMINAL")
                    or type(request["context"]) is not dict
                    or request["context"].get("grade")!=
                    "PROVISIONAL_SOURCEFREE_MODERN_GENERATION_PORT_NOT_NATIVE_OR_MODEL_ADEQUACY"
                    or (request["previous"] is None)!=(request["mode"]=="BOOTSTRAP")):
                raise ValueError("CHECKPOINT_UNQUALIFIED_REQUEST")
            body=canonical(request)
            n=len(body.encode("utf-8"))
            receipt["packet_bytes"]=n;receipt["wire_packet_bytes"]=n
            if n>1024*1024:raise ValueError("CHECKPOINT_PACKET_LIMIT")
            req={"model":self.model,
                 "messages":[{"role":"system","content":_CHECKPOINT_INSTRUCTIONS},
                             {"role":"user","content":body}],
                 "response_format":{"type":"json_object"},
                 **({self.completion_limit_field:self.completion_token_limit}
                    if self.completion_token_limit is not None else {})}
            receipt["instruction_bytes"]=len(_CHECKPOINT_INSTRUCTIONS.encode("utf-8"))
            receipt["request_bytes"]=len(canonical(req).encode("utf-8"))
            receipt["attempts"]=1
            result=self._transport(copy(req)) if self._transport is not None else self._request(req)
            receipt["usage"]=self._reported_usage(result)
            data=self._decode_json_response(result,receipt)
            if set(data)!={"retrospective","prospective"}:
                raise ValueError("CHECKPOINT_RESPONSE_SHAPE")
            receipt["outcome"]="PROPOSAL_RETURNED"
            return copy(data)
        finally:
            receipt["elapsed_ns"]=perf_counter_ns()-start
            if self._metrics.maxlen:
                with self._metrics_lock:
                    self._metrics_total+=1;self._metrics.append(receipt)


# Live V3 candidate: one conditional semantic response for one actual native
# turn, not the two-half historical generation checkpoint. Keep the existing
# live JSON transport restrictions and parser. No automatic network fallback.
_LIVE_TURN_INSTRUCTIONS = """
Typed formation extensions (fresh exact offer basis only, optional and actor-local):
Optional actor policy.private_rehearsal={affect:"REQUIRED" or "NONE",meaning,memory_event_ref?,memory_ref?,affect_ref?} selects only one fresh actor-local offered private rehearsal, otherwise falls through; never creates a public utterance. Optional formation.rules {private_construct:"NOTICE_END",augment:{possible_object,means:["REST"|"ORIENT"|"EAT"]},match?:{private_affect_ref}} binds only the actual performed private rehearsal and its allowed means. Later action pool possible_end_trials can match exact possible_end_ref or private_rehearsal_ref. Optional formation rule {private_construct:"TAKE_UP_END",augment:{means},match?:{possible_end_ref,possible_object,private_affect_ref}} requires actual earlier private trial and a distinct later independent performed course. No imagined possibility is a motive or action entitlement.
DELAYED_APPRAISAL from historically_possible_delayed_appraisals, augment {appraisal:"ACTOR_INTERPRETS_DISAPPOINTED"} when appropriate;
ACTIVITY_AFFECT from historically_possible_activity_affects or historically_possible_self_expression_affects, augment {affect_name,personal_sense,course_orientation:"APPROACH" or "WITHHOLD"};
RECURRENT_ROUTINE from historically_possible_recurrent_routines, augment {window_days,hours_per_active_day,provisional_exposure_fraction,food_units_per_active_day?}; use fresh exact own project/operation/recipient and three actual exercises. The bounded dose is not a guarantee of daily activity; coactivity needs independently compatible counterpart sources. ROUTINE_REVISION from historically_possible_routine_revisions, augment {mode,interpretive_hypothesis,dose?}; RESIZE requires the exact numeric keys within original ceilings, other modes omit dose. The owner independently requalifies the actor, current site, material permission, bodily and reciprocal time constraints; no rewritten past or future assent.
ORDINARY_AFFECT_MEMORY from historically_possible_activity_affects, match formation_source OWN_ORDINARY_PROJECT_EXERCISE, augment {content,cue_terms}. Optional and ordered AFTER an ACTIVITY_AFFECT nomination of the identical fresh basis in the same development packet. The compiler copies the exact basis; the native owner verifies that the affect was actually admitted and that this actor can form the memory. Content is a fallible acquired recollection, not analyst knowledge or public speech. Abstain if the actor's own history does not warrant it.
EXPRESSIVE_PRACTICE from historically_possible_expressive_practices, augment {cadence:"HALTING"} when appropriate;
RECURRENT_WORK_ORIENTATION from historically_possible_recurrent_livelihood_orientation, augment {orientation_mode:"APPROACH" or "WITHHOLD"}.
LIVED_CROSS_CONTEXT_REVALUATION from historically_possible_lived_cross_context_revaluations, augment {new_relation,new_polarity,interpretive_hypothesis?} using only offered semantic choices; preserve the old motif's actual source, action and context. A shared operation does not prove the same good.
WITNESSED_OTHER_RELATION from historically_possible_witnessed_third_party_relations, augment {hypothesis}; the actual witnessed source, target and sign are bound from the current actor's offer, not an assertion about another person's hidden motive or assent.
Exact complete candidate offers historically_possible_care_practice_revisions, historically_possible_relief_reconstitution and historically_possible_provisioning_reorganizations may be nominated or withheld; no fabricated source.
Optional action.current_match checks an actual situated current's exact {action?,kind?,ref?}; optional action.exclude_affect checks an exact practical option's own course_affective_organizations for {course_orientation,basis?:{formation_source}} and falls through if a matching organization exists. These are proposed situated policies, not universal affect or work laws. No actor need understand these analyst-only determinants.
You are constructing ONE situated response of a
continuing fictional organism. The current principal's actual actor_attempt
packet is the operative starting point. This is not a history generation
checkpoint, diary, personality inventory, or narration of a guaranteed outcome.
The existing initiative owner selected the occasion; you cannot change WHO.
The other person's actual choice remains separately conditioned by their own
packet and current practical alternatives. Do not attribute analyst knowledge
to a person's conscious self. No fabricated human action, consent, assent,
successful act, perception, memory, or development. Existing world owner settles
the actual attempt, actual lexical occurrence, coaction and material result.
Return {policies:{actor_id:actor_policy,...}} with the principal present. A rare current private reconsideration may additionally nominate private_rehearsal:{objective_ref,meaning} ONLY if exactly one actual current principal_packet.private_rehearsal_options has that memory_event_ref and null affect_ref. Meaning <=512 nonblank, a present hypothesis not causal truth or changed earlier experience. The existing R61 owner may admit a qualified revision after actual private rehearsal, never automatically. This is a private actor activity, not a spoken response. No other actor private rehearsal nomination.
Only listed actor IDs; peer contexts are separately conditioned, never shared
psychic state. Principal expression must use only principal actor-accessible
content, not another person's private tip or analyst description. No exposition
of hidden history to the visitor. Ordinary activity may be banal, ambivalent
or blocked. No forced disclosure or drama.

actor_policy: {actions:[conditional alternatives in order],formation?:{base:
"LOCAL" or "NONE",rules:[...]},expression?:{speech?:nonblank <=500,surface?:
nonblank <=500}}. Select actual operation names from options. Alternatives may
be {action,project_id?}, {action,option_match:{operation?,project_id?,
world_request?:{addressed_party_ref?,material_object_ref?,operation?},
binding_status?,grounds_status?},pool?}, or
{action:"SELECT_HIGHEST_CURRENT_PROJECT_COURSE",project_course_actions:[...]}.
The optional pool is practical_options, addressed_lexical_options or
possible_end_trials; unique fresh match required. For possible-end trial match
source_material_object_ref or genesis_family. For voluntary SPEAK include
speech_intent (nonblank <=500) and actual expression.speech (nonblank <=500);
speech_intent is not the utterance, and the owner must realize it. An absent
option is not an act; fall through to another conditional alternative or local
policy. For an addressed SIGNAL, optional rank_by
LATEST_PERSONALLY_SENSED_REGULATION only with grounds_status
HISTORICALLY_ACQUIRED_CO_REGULATION. Coactor invitation and response remain
separate. Peer policies are conditional on the ACTUAL own later offer, not the
principal's preferences.

Formation rules use the actual development packet AFTER world settlement.
{offer:"historically_possible_..." or "historically_proposed_...",match?:{},
augment?:semantic-only fields} nominates a unique actual owner offer; no
invented source IDs. Typed constructors: LEXICAL_PROJECT_REVALUATION on
historically_possible_lexical_project_revaluations with augment
{priority:finite nonnegative changed number,personal_significance:nonblank
<=512}; CROSS_OBJECT_POSSIBLE_END on historically_possible_cross_object_significance
with augment {possible_object,possible_means:["INSPECT"],cue_terms};
INCIDENTAL_END_TAKEUP on historically_possible_incidental_takeup with augment
{means:["INSPECT"]}. Existing plural-care resolver: {offer:
"historically_possible_plural_care",resolver:"EXISTING_PLURAL_CARE_SOURCE_RESOLUTION"}.
Direct hypothesis rule {candidate:{kind:"MEMORY",content:nonblank <=512,
cue_terms:[1..12 short terms]},when?:{own_action?,status?,participated?}} or
{candidate:{kind:"ACQUIRE_HISTORICAL_ORIENTATION",operation,orientation_mode:
"APPROACH" or "WITHHOLD"},when?:...}. Optional, no mutation unless actual
owner admits it. Do not make an actor acquire a meaning merely because another
actor speaks. Empty/no-change is lawful. No new family birth or interval here.
No second model call for validation, expression or development. JSON only."""


# Reuse the existing same-phase actor_attempt exact compiler. The combined
# request has a different outer contract; only its principal packet may use
# these aliases. No peer's information is copied into the principal.
_LIVE_EXACT_RULES=(
    " The principal_packet may omit only fields in principal_exact_aliases. "
    "Each dotted destination equals the full source value in this SAME "
    "principal_packet, never a peer or earlier occasion. Restore aliases "
    "before principal_reconstructed_fields. For practical_options and "
    "possible_end_trials with FROM_ORDERED_OPTIONS concatenate the respective "
    "practical_alternatives or possible_end_trials lists in options order; "
    "missing lists are empty. All other fields remain exact. These are "
    "transport projections, not additional actor awareness or new options."
)

def expand_live_wire_request(wire):
    """Strict inverse for exact transport checks, not actor cognition."""
    if type(wire) is not dict or set(wire)-{
            "grade","source","principal","principal_packet","peer_tips",
            "principal_exact_aliases","principal_reconstructed_fields"}:
        raise ValueError("LIVE_WIRE_FIELDS")
    result=copy(wire)
    aliases=result.pop("principal_exact_aliases",{})
    descriptions=result.pop("principal_reconstructed_fields",{})
    result["principal_packet"]=_expand_structured_fields("actor_attempt",
        _expand_exact_aliases("actor_attempt",result["principal_packet"],aliases),descriptions)
    return result

class ExplicitLiveTurnProvider(ExplicitJSONLLMProvider):
    """Explicit, sourcefree one-response transport; not empirical adequacy."""
    grade="EXPLICIT_SOURCEFREE_ONE_TURN_LLM_UNCALIBRATED"
    def __init__(self,*,sourcefree_live_attested=False,**kwargs):
        if sourcefree_live_attested is not True:
            raise ValueError("LIVE_TURN_SOURCEFREE_ATTESTATION_REQUIRED")
        super().__init__(**kwargs)
    def call(self,request):
        receipt={"task":"live_conditional_turn","transport":"MOCK" if self._transport is not None else "HTTPS",
                 "attempts":0,"outcome":"REJECTED_OR_FAILED","instruction_bytes":None,
                 "packet_bytes":None,"request_bytes":None,"response_content_bytes":None,
                 "prompt_variant":"LIVE_CONDITIONAL_TURN","packet_variant":"ACTOR_TIPS",
                 "wire_packet_bytes":None,"alias_count":0,"structured_field_count":0,
                 "usage":self._reported_usage(None)}
        start=perf_counter_ns()
        try:
            if (type(request) is not dict or set(request)!={"grade","source","principal","principal_packet","peer_tips"}
                    or request["grade"]!="SOURCEFREE_CONDITIONAL_LIVE_TURN_NOT_MODEL_ADEQUACY"
                    or type(request["principal_packet"]) is not dict
                    or request["principal_packet"].get("actor",{}).get("id")!=request["principal"]
                    or type(request["peer_tips"]) is not dict):
                raise ValueError("LIVE_TURN_UNQUALIFIED_REQUEST")
            body=canonical(request);n=len(body.encode("utf-8"))
            receipt["packet_bytes"]=n;receipt["wire_packet_bytes"]=n
            if n>512*1024:raise ValueError("LIVE_TURN_PACKET_LIMIT")
            def wire_req(value,instructions):
                return {"model":self.model,"messages":[{"role":"system","content":instructions},
                    {"role":"user","content":canonical(value)}],"response_format":{"type":"json_object"},
                    **({self.completion_limit_field:self.completion_token_limit}
                       if self.completion_token_limit is not None else {})}
            req=wire_req(request,_LIVE_TURN_INSTRUCTIONS)
            projection=copy(request)
            source=request["principal_packet"]
            if self.compact_exact_packet:
                projected,aliases=_compile_exact_aliases("actor_attempt",source)
                if aliases:
                    projection["principal_packet"]=projected
                    projection["principal_exact_aliases"]=aliases
            if self.compact_structured_packet:
                _,descriptions=_compile_structured_fields("actor_attempt",source)
                if descriptions:
                    for field in descriptions:
                        path=tuple(field.split("."))
                        del _packet_field(projection["principal_packet"],path[:-1])[path[-1]]
                    projection["principal_reconstructed_fields"]=descriptions
            if projection!=request:
                if canonical(expand_live_wire_request(projection))!=body:
                    raise ValueError("LIVE_EXACT_PROJECTION_NOT_REVERSIBLE")
                trial=wire_req(projection,_LIVE_TURN_INSTRUCTIONS+_LIVE_EXACT_RULES)
                if len(canonical(trial).encode("utf-8"))<len(canonical(req).encode("utf-8")):
                    req=trial
                    receipt["packet_variant"]="ACTOR_TIPS_EXACT_PRINCIPAL"
                    receipt["wire_packet_bytes"]=len(canonical(projection).encode("utf-8"))
                    receipt["alias_count"]=len(projection.get("principal_exact_aliases",{}))
                    receipt["structured_field_count"]=len(projection.get("principal_reconstructed_fields",{}))
            receipt["instruction_bytes"]=len(req["messages"][0]["content"].encode("utf-8"))
            receipt["request_bytes"]=len(canonical(req).encode("utf-8"))
            receipt["attempts"]=1
            result=self._transport(copy(req)) if self._transport is not None else self._request(req)
            receipt["usage"]=self._reported_usage(result)
            data=self._decode_json_response(result,receipt)
            if (not {"policies"}<=set(data)<={"policies","private_rehearsal"}
                    or type(data["policies"]) is not dict):
                raise ValueError("LIVE_TURN_RESPONSE_SHAPE")
            receipt["outcome"]="PROPOSAL_RETURNED"
            return copy(data)
        finally:
            receipt["elapsed_ns"]=perf_counter_ns()-start
            if self._metrics.maxlen:
                with self._metrics_lock:
                    self._metrics_total+=1;self._metrics.append(receipt)
