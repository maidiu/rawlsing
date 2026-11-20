"""C7: genuine C6 sourcefree empirical hypotheses -> independent Sorok R4 world runtime.

The R4 code is NEVER copied or rewritten: a separately checked-out R4 package
is authenticated against all its source Python bytes, then the actual R4
ConstitutiveRuntime runs world/actors/attempts/history on a new private ledger.
C6 pair association is explicitly FICTION, not survey partner-selection.
No survey answer becomes a psychological form or independent interview proof.
Sourcefree implementation, NOT a protected Sorok/Pyat issuer or whole person.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from importlib import import_module
import hashlib
import json
import sys
from typing import Any, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, exact_ref, semantic_hash
from rawlsing_next.pre553_s04_field_forge_v3_bridge import V3SeamEnvelope, V3SeamExternalPin
from rawlsing_next.pre553_ff_prev3_possibility_navigation import V3ContextPath
from rawlsing_next.pre553_c6_seam_contextual_entrances import (
    ENTRY_PARENT, GRADE as C6_GRADE, C6ContextualEntrance, C6IndependentParents,
    replay_two_sourcefree_parent_entrances,
)

INPUT_CONTRACT="PYAT_C7_ACTUAL_R4_WORLD_INPUT@1"
RUN_CONTRACT="PYAT_C7_ACTUAL_R4_WORLD_EXECUTION@1"
R4_HEAD="7bff10db7adb7b17bcf035a27561ea59e9a3b2be"
R4_SOURCE_SHA256={
  "__init__.py": "e950fe1409237dfdd752d1fc61d740ce687a4e8a37683976c5a00f7de8355c4e",
  "__main__.py": "cf7390a2508a0fcad4777a4a629fc5212ab655cb45845975995f835676a834e3",
  "activity.py": "7f6c401fde7dc31f3a4ab9f6f9b1b2a53125502f37d93863aa712fb293b0517b",
  "adapters.py": "e8ecb4f3afaeedd6165ef9e6f6259e6b4250ba413e46be600824634d29cf9753",
  "becoming.py": "c64bce1af9a60c129204ba3baedaf08993054cc58b43e88ff30c8404f96d6665",
  "cli.py": "a9a6e9258971f11bfa78774f1f80e39dd2304dd1a748a2cdc5dccaa838197a33",
  "constitution.py": "c7269661769ec610e32465865c4fc29874fe8519341a62f3a338dbbc59886326",
  "development.py": "0957ecbbb452c46071cfb99421877fb18a8d21825bdcd9acbece686e4cff9326",
  "model_provider.py": "54e815e5bf4a8aa23d868bc7bbb9e9b780ed57c9ab19b87f4092220214215a0e",
  "ordinary_life.py": "08f19f4847f3e996071dfea6188221841d8d2935b7795dd33ad7125eac11e17b",
  "organism.py": "c20b4471a8d2fdbddeed960da2f2ce2488c4df3571470bf9bfd8a1a818abbba2",
  "parents.py": "f55957b114ca758907cec1a527d288fd6b8ea5ab29794c2092a8b12b796af30a",
  "plans.py": "50fd7e3d0c31431463cd889452a861663b8e2e30b0fc7d6b47887216de0b5198",
  "psychodynamics.py": "0edda0cbb1fc0333905d120403f07e634819368325237db509bf7a06a6ee05ae",
  "relational.py": "4900dea233b44e0583a1bfc741129dd2a90ca19ea586be35033538641b621faf",
  "runtime.py": "98e54d6a3f13e1afa61a84cb6a3df3856110d211736f099d4b45f4da1072b25a",
  "semantics.py": "313db7078db1849bb81fff012e0353d8f057cb22a25368d3c0d8c977cb011453",
  "storage.py": "f2177b391093fad25170fa65a9742fe2d4e53cb1f686b775f72ce9dde9574364",
  "types.py": "5132882b752b532ed0424a29c8aa5ac5477e29c77060d2f6fe27feef45c2a4b5",
  "world.py": "2613105940b1d49b301920e80bb891f9288b7874fa012c9196fda4d85d0ffe3e"
}
GRADE="SOURCEFREE_EMPIRICAL_HYPOTHESES_IN_EXPLICIT_FICTIONAL_SOROK_R4"
FICTIONAL_WORLD_PREMISE="EXPLICIT_FICTIONAL_SHARED_HOUSEHOLD_NOT_SURVEY_PARTNER_EVIDENCE"
NOT_ISSUED=(
    "REAL_PARENT_RELATIONSHIP_OR_PARTNER_SELECTION",
    "SURVEY_WAVE_OR_ORIGINAL_DISCLOSURE_AUTHORITY",
    "INDEPENDENT_WHOLE_SURVEY_PERSONALITY_RECONSTRUCTION",
    "PROTECTED_SOROK_WORLD_P2_P3_CAN_ADP_OR_SEAM_WRITER",
    "SCIENTIFIC_PSYCHOLOGICAL_CAUSALITY_OR_INFERENCE",
    "INDEPENDENT_G5_OR_PROTECTED_RECEIVING",
)

class C7BridgeError(ValueError):
    pass

@dataclass(frozen=True)
class C7Receipt:
    payload_json:str
    digest:str

    def __post_init__(self):
        try:
            m=json.loads(self.payload_json)
            if (type(m) is not dict
                or m.get("contract") not in (INPUT_CONTRACT,RUN_CONTRACT)
                or canonical_json(m)!=self.payload_json
                or semantic_hash(m)!=self.digest):
                raise C7BridgeError("invalid C7 exact receipt")
        except (TypeError,ValueError) as e:
            raise C7BridgeError("invalid C7 receipt material") from e

    @property
    def ref(self):
        c=self.material()["contract"]
        return ExactRef(c,"urn:rawlsing:c7:"+c+":sha256:"+self.digest,self.digest)

    def material(self):
        return json.loads(self.payload_json)

def _seal(m):
    return C7Receipt(canonical_json(m),semantic_hash(m))

def _source_tuple(x,name):
    if (type(x) is not tuple or len(x)!=3
        or type(x[0]) is not V3SeamEnvelope
        or type(x[1]) is not V3SeamExternalPin
        or type(x[2]) is not V3ContextPath):
        raise C7BridgeError(name+" requires actual C4 envelope/pin/C5 path")
    return x

def _adult_source(c6, label):
    m=c6.material()
    if (m.get("grade")!=C6_GRADE or m.get("entrance")!=ENTRY_PARENT
        or m.get("world_or_actor_issuer") is not None
        or m.get("actor_state_transition") is not None
        or m.get("original_data_usable") is not False
        or m.get("no_partner_coupling_inference") is not True):
        raise C7BridgeError(label+" C6 source/actor authority changed")
    n=m.get("original_selected_cell_n_if_disclosable")
    floor=m.get("min_disclosure_cell_n")
    cells=m.get("hypothetical_joint_configuration")
    if (m.get("whole_case_state")!="SOURCEFREE_CELL_PROPOSAL_ONLY__NO_PERSON"
        or type(n) is not int or type(floor) is not int or floor<2 or n<floor
        or type(cells) is not list or not cells):
        raise C7BridgeError(label+" whole-joint cell WITHHELD; refuse adult genesis")
    answers={}
    refs=[]
    for i,cell in enumerate(cells):
        if type(cell) is not dict or cell.get("source_dimension")!=i:
            raise C7BridgeError(label+" source joint dimension lost")
        r=exact_ref(cell.get("target_ref"),label+" exact source axis")
        key="opaque_axis_"+str(i)+"_"+r.content_hash[:16]
        if key in answers:raise C7BridgeError("duplicate original source axis")
        answers[key]=cell["candidate_state"]
        refs.append(r.as_dict())
    return {
        "c6_ref":c6.ref.as_dict(),"c4_ref":m["source_c4_handoff_ref"],
        "c5_ref":m["source_c5_path_ref"],"ff01_ref":m["source_ff01_ref"],
        "raw_selected_joint_cell_n":n,
        "source_target_refs":refs,
        "answers":answers,
        "no_real_respondent":True,
        "source_grade":GRADE,
    }

def prepare_c7_world_input(
    *,pair:C6IndependentParents,expected_pair_ref:ExactRef,
    first:C6ContextualEntrance,second:C6ContextualEntrance,
    first_source:tuple[V3SeamEnvelope,V3SeamExternalPin,V3ContextPath],
    second_source:tuple[V3SeamEnvelope,V3SeamExternalPin,V3ContextPath],
    first_expected_ref:ExactRef,second_expected_ref:ExactRef,
    fictional_world_premise:str,
)->C7Receipt:
    """Both parents have independent C6 roots; actual relationship is UNISSUED."""
    if fictional_world_premise!=FICTIONAL_WORLD_PREMISE:
        raise C7BridgeError("an explicit independent fictional world premise required")
    if (type(pair) is not C6IndependentParents or type(expected_pair_ref) is not ExactRef
        or pair.ref!=expected_pair_ref
        or type(first_expected_ref) is not ExactRef
        or type(second_expected_ref) is not ExactRef):
        raise C7BridgeError("separately held C6 source and pair pins required")
    a=_source_tuple(first_source,"first")
    b=_source_tuple(second_source,"second")
    replay_two_sourcefree_parent_entrances(
        receipt=pair, first=first, second=second,
        first_source=a,second_source=b,
        first_expected_receipt_ref=first_expected_ref,
        second_expected_receipt_ref=second_expected_ref,
    )
    pm=pair.material()
    if (pm.get("partner_selection_evidence") is not None
        or pm.get("inferred_parental_relationship") is not None
        or pm.get("actor_state_transition") is not None
        or pm.get("no_fabricated_cross_person_correlation") is not True):
        raise C7BridgeError("survey evidence cannot issue a real couple")
    if first.ref==second.ref:
        raise C7BridgeError("two distinct independent C6 hypotheses required")
    return _seal({
        "contract":INPUT_CONTRACT,"grade":GRADE,
        "c6_parent_pair_ref":pair.ref.as_dict(),
        "adult_one":_adult_source(first,"adult one"),
        "adult_two":_adult_source(second,"adult two"),
        "household_grade":FICTIONAL_WORLD_PREMISE,
        "r4_source_cut":R4_HEAD,
        "actor_issuer":None,
        "not_issued":list(NOT_ISSUED),
    })

def _verify_r4_source(r4_package_dir:Path):
    """Check separately checked-out authentic R4, not a surrogate Sorok."""
    if type(r4_package_dir) not in (str,Path):
        raise C7BridgeError("explicit R4 package directory required")
    root=Path(r4_package_dir)
    if not root.is_dir() or root.is_symlink() or root.name!="um_sorok_organism":
        raise C7BridgeError("genuine nonsymlink Sorok R4 package required")
    root=root.resolve(strict=True)
    actual={p.name for p in root.glob("*.py")}
    if actual!=set(R4_SOURCE_SHA256):
        raise C7BridgeError("R4 package Python module inventory differs from exact source")
    for name,want in R4_SOURCE_SHA256.items():
        p=root/name
        if (p.is_symlink() or not p.is_file()
            or p.resolve(strict=True).parent!=root
            or hashlib.sha256(p.read_bytes()).hexdigest()!=want):
            raise C7BridgeError("R4 byte/source fidelity violation: "+name)
    return root

class _NoSurveyAnswerBootstrap:
    """R4 remains world/psychic owner; no survey answers become innate forms."""
    grade="SOURCEFREE_C7_SURVEY_DIRECT_ANSWER_BOOTSTRAP_DISABLED"
    def __init__(self,delegate):
        self.delegate=delegate
        self.provider=self
    def proposal(self,task,packet):
        if task=="adult_constructor":
            return {
                "forms":[],"projects":[],"links":[],
                "fictional_backfill":{
                    "state":"ABDUCTION_NOT_ISSUED__NO_DIRECT_ANSWER_SEED",
                    "questionnaire_as_operative_psyche":False,
                },
            }
        return self.delegate.proposal(task,packet)

def run_c7_pinned_r4_world(
    *,input_receipt:C7Receipt,expected_input_ref:ExactRef,
    r4_package_dir:Path,db_path:Path,
    interventions:Sequence[tuple[str,str]],background_days:int=0,
)->C7Receipt:
    """Run real R4 world, ledger, Others, embodiment and developmental afterlife.

    Requested actions are labeled external interventions; outcomes and other
    people's consent are exclusively resolved by unmodified R4.
    """
    if (type(input_receipt) is not C7Receipt
        or type(expected_input_ref) is not ExactRef
        or input_receipt.ref!=expected_input_ref):
        raise C7BridgeError("independently pinned C7 receipt required")
    m=input_receipt.material()
    if (m.get("contract")!=INPUT_CONTRACT or m.get("household_grade")!=FICTIONAL_WORLD_PREMISE
        or m.get("actor_issuer") is not None or m.get("grade")!=GRADE):
        raise C7BridgeError("invalid world/actor source grade")
    if (not isinstance(interventions,(tuple,list)) or len(interventions)>32
        or any(type(item) not in (list,tuple) or len(item)!=2
               or item[0] not in ("adult-one","adult-two","nadia")
               or type(item[1]) is not str for item in interventions)):
        raise C7BridgeError("bounded research action interventions required")
    if type(background_days) is not int or not 0<=background_days<=365:
        raise C7BridgeError("ordinary life period must be bounded nonnegative days")
    root=_verify_r4_source(r4_package_dir)
    for name,mod in list(sys.modules.items()):
        if name=="um_sorok_organism" or name.startswith("um_sorok_organism."):
            path=getattr(mod,"__file__",None)
            if not path or not Path(path).resolve().is_relative_to(root):
                raise C7BridgeError("preloaded nonpinned Sorok code refused")
    if str(root.parent) not in sys.path:sys.path.insert(0,str(root.parent))
    runtime_mod=import_module("um_sorok_organism.runtime")
    semantics=import_module("um_sorok_organism.semantics")
    if Path(runtime_mod.__file__).resolve()!=root/"runtime.py":
        raise C7BridgeError("Sorok R4 execution import not pinned source")
    db=Path(db_path)
    if db.exists():raise C7BridgeError("new research SQLite ledger required")
    def packet(source):
        return {
            "source_ref":source["c6_ref"],
            "answers":source["answers"],
            "source_grade":GRADE,
            "world_premise_grade":FICTIONAL_WORLD_PREMISE,
            "fictional_seed":{},
        }
    semantic=_NoSurveyAnswerBootstrap(semantics.ValidatingSemanticService())
    runtime=runtime_mod.ConstitutiveRuntime(db,semantic=semantic)
    try:
        init=runtime.initialize(parent_packets=[
            ("adult-one","Fictional adult one",packet(m["adult_one"])),
            ("adult-two","Fictional adult two",packet(m["adult_two"])),
        ],child_id="nadia",child_name="Nadia")
        if set(init["actors"])!={"adult-one","adult-two","nadia"}:
            raise C7BridgeError("R4 actual actor genesis mismatch")
        # No fabricated inter-person survey association. The scenario names
        # an independent fictional shared world, nothing more.
        initial_forms=[
            len(runtime.ledger.actor(actor)[1]["forms"])
            for actor in ("adult-one","adult-two")
        ]
        if initial_forms!=[0,0]:
            raise C7BridgeError("survey answers laundered into parent constitution")
        episodes=[]
        for actor,action in interventions:
            experience=runtime.step(actor,requested_action=action)
            episodes.append({
                "actor":actor,
                "requested_action":action,
                "choice_grade":experience["selection_grade"],
                "R4_actual_event_id":experience["receipt"],
                "R4_actual_status":experience["status"],
                "objective_outcome":experience["objective_outcome"],
            })
        ordinary=runtime.background(background_days) if background_days else None
        witness=runtime.verify()
        if witness.get("valid") is not True:
            raise C7BridgeError("genuine R4 event history failed verification")
        world=runtime.ledger.world(runtime.world_id)[1]
        return _seal({
            "contract":RUN_CONTRACT,"grade":GRADE,
            "source_c7_input_ref":input_receipt.ref.as_dict(),
            "r4_pinned_commit":R4_HEAD,
            "r4_verified_module_count":len(R4_SOURCE_SHA256),
            "actor_ids":init["actors"],
            "fictional_shared_world_premise":FICTIONAL_WORLD_PREMISE,
            "parent_initial_psychic_form_counts":initial_forms,
            "research_interventions":episodes,
            "ordinary_life_receipt":ordinary["receipt"] if ordinary else None,
            "final_world_clock":world["clock"],
            "source_parent_c6_refs":[m["adult_one"]["c6_ref"],m["adult_two"]["c6_ref"]],
            "R4_event_chain_count":witness["events"],
            "R4_event_chain_hash":witness["last_hash"],
            "R4_event_chain_verified":True,
            "genuine_R4_world_actor_development_owner_used":True,
            "native_Sorok_or_original_source_authorized":False,
            "not_issued":list(NOT_ISSUED),
        })
    finally:
        runtime.close()


def replay_c7_pinned_r4_world(
    *,run_receipt:C7Receipt,expected_run_ref:ExactRef,
    source_input:C7Receipt,expected_source_input_ref:ExactRef,
    r4_package_dir:Path,db_path:Path,
)->C7Receipt:
    """Independent cold re-read of actual, unmodified R4 SQLite hash chain.

    Both C7 refs must be held OUTSIDE the candidate receipt or a forged
    self-rehashed run could authenticate itself. Validates the real R4 ledger
    and both sealed parent packets against the earlier admitted C7 input.
    """
    if (type(run_receipt) is not C7Receipt or type(expected_run_ref) is not ExactRef
        or run_receipt.ref!=expected_run_ref
        or type(source_input) is not C7Receipt
        or type(expected_source_input_ref) is not ExactRef
        or source_input.ref!=expected_source_input_ref):
        raise C7BridgeError("independent input and execution roots required")
    source=source_input.material()
    result=run_receipt.material()
    if (result.get("contract")!=RUN_CONTRACT
        or source.get("contract")!=INPUT_CONTRACT
        or result.get("source_c7_input_ref")!=source_input.ref.as_dict()
        or result.get("r4_pinned_commit")!=R4_HEAD
        or result.get("R4_event_chain_verified") is not True):
        raise C7BridgeError("run/source/Sorok R4 root mismatch")
    root=_verify_r4_source(r4_package_dir)
    for name,mod in list(sys.modules.items()):
        if name=="um_sorok_organism" or name.startswith("um_sorok_organism."):
            file=getattr(mod,"__file__",None)
            if not file or not Path(file).resolve().is_relative_to(root):
                raise C7BridgeError("preloaded nonpinned Sorok code refused")
    if str(root.parent) not in sys.path:sys.path.insert(0,str(root.parent))
    storage=import_module("um_sorok_organism.storage")
    if Path(storage.__file__).resolve()!=root/"storage.py":
        raise C7BridgeError("R4 storage import path not pinned")
    db=Path(db_path)
    if not db.is_file() or db.is_symlink():
        raise C7BridgeError("expected existing nonsymlink R4 sourcefree ledger")
    ledger=storage.ResearchLedger(db)
    try:
        proof=ledger.verify_chain()
        if (proof.get("valid") is not True
            or proof["events"]!=result["R4_event_chain_count"]
            or proof["last_hash"]!=result["R4_event_chain_hash"]):
            raise C7BridgeError("cold Sorok R4 actual event ancestry mismatch")
        if set(ledger.actors())!=set(result["actor_ids"]):
            raise C7BridgeError("cold Sorok R4 actor roster mismatch")
        for aid,key in (("adult-one","adult_one"),("adult-two","adult_two")):
            sealed=ledger.source("fictional_source:"+aid)
            if (not sealed or sealed["category"]!="CONDITIONING_NOT_REAL_PERSON"
                or sealed["content"].get("source_ref")!=source[key]["c6_ref"]
                or sealed["content"].get("answers")!=source[key]["answers"]
                or sealed["content"].get("world_premise_grade")!=FICTIONAL_WORLD_PREMISE):
                raise C7BridgeError("cold Sorok R4 sealed parent source mismatch")
        if ledger.world("w1")[1]["clock"]!=result["final_world_clock"]:
            raise C7BridgeError("cold Sorok R4 material world clock changed")
        return run_receipt
    finally:
        ledger.close()


__all__=["INPUT_CONTRACT","RUN_CONTRACT","R4_HEAD","R4_SOURCE_SHA256",
         "GRADE","FICTIONAL_WORLD_PREMISE","NOT_ISSUED","C7BridgeError",
         "C7Receipt","prepare_c7_world_input","run_c7_pinned_r4_world",
    "replay_c7_pinned_r4_world"]
