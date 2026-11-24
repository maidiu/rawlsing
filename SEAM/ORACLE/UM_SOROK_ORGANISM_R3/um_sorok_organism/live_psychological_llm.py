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


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError("REMOTE_MODEL_REDIRECT_REFUSED")


_ALLOWED=("actor_attempt","development","adult_constructor",
          "blind_adult_interview","expression")


class ExplicitJSONLLMProvider:
    """Opt-in HTTP transport for an OpenAI-*compatible* chat JSON interface.

    JSON-completions compatibility is a deployment requirement, not a
    guarantee about any particular vendor's current model or API. Direct
    callback providers remain available without this adapter.
    """
    grade="EXPLICIT_REMOTE_LLM_UNCALIBRATED_CONSTRUCTION"
    def __init__(self,*,endpoint,model,api_key,allow_private_actor_data=False,
                 timeout_seconds=45,transport=None):
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

    def propose(self,task,packet):
        if task not in _ALLOWED:
            raise ValueError("UNSUPPORTED_LIVE_PSYCHOLOGICAL_TASK")
        if type(packet) is not dict:
            raise TypeError("REMOTE_MODEL_PACKET_NOT_OBJECT")
        serialized=canonical(packet)
        if len(serialized.encode("utf-8"))>128000:
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
            "For expression disclose only actor-accessible "
            "content. The engine will independently reject invalid effects. "
            "Never describe these as proven real human-development laws. "
            "Return valid JSON and no Markdown."
        )
        req={"model":self.model,
             "messages":[
                 {"role":"system","content":instructions},
                 {"role":"user","content":canonical({
                     "task":task,"actor_source_packet":packet})}],
             "response_format":{"type":"json_object"}}
        # Injected transport permits local hermetic contract tests; production
        # uses the real HTTPS request, never a fake response behind the scenes.
        result=(self._transport(copy(req)) if self._transport is not None
                else self._request(req))
        if type(result) is not dict or type(result.get("choices")) is not list:
            raise ValueError("REMOTE_MODEL_RESPONSE_SCHEMA_INVALID")
        choices=result["choices"]
        if len(choices)!=1 or type(choices[0]) is not dict:
            raise ValueError("REMOTE_MODEL_AMBIGUOUS_CHOICES")
        message=choices[0].get("message")
        if type(message) is not dict or type(message.get("content")) is not str:
            raise ValueError("REMOTE_MODEL_NO_JSON_CONTENT")
        if len(message["content"].encode("utf-8"))>256000:
            raise ValueError("REMOTE_MODEL_RESPONSE_TOO_LARGE")
        data=json.loads(message["content"])
        if type(data) is not dict:
            raise ValueError("REMOTE_MODEL_NOT_JSON_OBJECT")
        if data.get("task")!=task:
            raise ValueError("REMOTE_MODEL_TASK_MISMATCH")
        if task=="development" and type(data.get("candidates")) is not list:
            raise ValueError("REMOTE_MODEL_BAD_DEVELOPMENT_CANDIDATES")
        if task=="actor_attempt" and type(data.get("action")) is not str:
            raise ValueError("REMOTE_MODEL_BAD_ACTION")
        # No underlying authoring authority is conferred by this transport.
        return copy(data)
