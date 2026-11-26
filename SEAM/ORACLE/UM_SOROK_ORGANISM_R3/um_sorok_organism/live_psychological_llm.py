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


class ExplicitJSONLLMProvider:
    """Opt-in HTTP transport for an OpenAI-*compatible* chat JSON interface.

    JSON-completions compatibility is a deployment requirement, not a
    guarantee about any particular vendor's current model or API. Direct
    callback providers remain available without this adapter.
    """
    grade="EXPLICIT_REMOTE_LLM_UNCALIBRATED_CONSTRUCTION"
    def __init__(self,*,endpoint,model,api_key,allow_private_actor_data=False,
                 timeout_seconds=45,transport=None,compact_task_prompt=False,
                 metrics_capacity=0,compact_exact_packet=False,compact_structured_packet=False):
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
        def request(prompt,body):
            return {"model":self.model,
                 "messages":[{"role":"system","content":prompt},
                             {"role":"user","content":canonical(body)}],
                 "response_format":{"type":"json_object"}}
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
        # No underlying authoring authority is conferred by this transport.
        return copy(data)
