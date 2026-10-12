#!/usr/bin/env python3
"""HQ280 C02HR - REAL forgery using the candidate's known fixed toy RSA key."""
import json, sys, hashlib, subprocess
sys.path.insert(0,"/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-c02hr")
from rawlsing_next.pre553_b5_separate_principal_verifier_candidate import (
    IssuerProcess, VerifierProcess, IssuerCredential, AttackerProcess,
    SeparatePrincipalError, _rsa_sign, _rsa_keypair)
import dataclasses as dc
OUT={"schema":"HQ280_PV3_C02HR_FORGE_ATTACK@1","cases":[]}
def rec(i,what,obs,v): OUT["cases"].append({"id":i,"what":what,"observed":obs,"verdict":v})

# F1: the key is FIXED and public in source
n,e,d = _rsa_keypair()
issuer, verifier = __import__("rawlsing_next.pre553_b5_separate_principal_verifier_candidate",
                              fromlist=["x"]).build_demo_principal_pair()
rec("F1","toy RSA key is a hardcoded constant",
    {"n":n,"e":e,"d":d,"primes":"p=61,q=53","issuer_public_key":issuer.public_key},
    "FAIL__FIXED_KNOWN_KEYPAIR" if (n,e,d)==(3233,17,2753) else "REVIEW")

# F2: obtain a REAL credential to learn the signed_material shape
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
def ref(k,s): return ExactRef(k, f"urn:test:{s}", hashlib.sha256(s.encode()).hexdigest())
subj=ref("Subject","s1")
honest=issuer.issue(subject_ref=subj, producer_contract_ref=ref("C","c"),
                    permission_ceiling_ref=ref("P","p"), release_ref=ref("R","r"),
                    replay_closure_ref=ref("RC","rc"), scope={})
canon=json.dumps(honest.signed_material(), sort_keys=True, separators=(",",":")).encode()
rec("F2","honest credential verifies against the shared root",
    {"honest_verifies":True},
    "INFO__baseline")
verifier.verify(honest)

# F3: THE FORGERY - sign with the SAME known private key from a DIFFERENT principal
forged = dc.replace(honest,
    credential_id="FORGED-"+honest.credential_id[:16],
    scope={"forged_by":"C02HR-reviewer","role":"arbitrary"})
fcanon=json.dumps(forged.signed_material(), sort_keys=True, separators=(",",":")).encode()
forged = dc.replace(forged, signature=str(_rsa_sign((n,d), fcanon)))
try:
    verifier.verify(forged)
    v3="ACCEPTED__FORGERY_SUCCEEDED"
except SeparatePrincipalError as ex:
    v3=f"REFUSED:{ex.code}"
rec("F3","REAL forgery: re-sign a substituted credential with the known private key",
    {"outcome":v3,"note":"no access to issuer object beyond the public source constant"},
    "FAIL__FORGERY_ACCEPTED" if v3.startswith("ACCEPTED") else "PASS")

# F4: root swap via CONSTRUCTION (the stubs never try this)
attacker_issuer = IssuerProcess(issuer_id="EVIL-ISSUER")
evil_verifier = VerifierProcess(trusted_root=attacker_issuer.public_key,
                                issuer_id="EVIL-ISSUER")
evil_cred = attacker_issuer.issue(subject_ref=subj, producer_contract_ref=ref("C","c2"),
    permission_ceiling_ref=ref("P","p2"), release_ref=ref("R","r2"), replay_closure_ref=ref("RC","rc2"), scope={})
try:
    evil_verifier.verify(evil_cred); v4="ACCEPTED__SELF_ANCHORED_VERIFIER_WORKS"
except SeparatePrincipalError as ex: v4=f"REFUSED:{ex.code}"
truth_same = attacker_issuer.public_key == issuer.public_key
rec("F4","root swap by CONSTRUCTION (the candidate's swap_root stub returns False instead of trying)",
    {"outcome":v4,"attacker_root_equals_honest_root":truth_same,
     "candidate_swap_root_returned":AttackerProcess().swap_root(verifier, attacker_issuer.public_key),
     "candidate_self_register_returned":AttackerProcess().self_register_issuer(verifier,"EVIL-ISSUER")},
    "FAIL__ROOT_IS_A_CALLER_ARGUMENT" if v4.startswith("ACCEPTED") else "REVIEW")

# F5: the candidate's own forge helper is an inert stub
ap=AttackerProcess(); stub=ap.forge_credential(issuer_id=honest.issuer_id, subject_ref=subj)
try:
    int(stub.signature); sig_is_int=True
except Exception: sig_is_int=False
rec("F5","candidate's own forge_credential is a stub, not an adversarial attempt",
    {"signature_is_valid_rsa_integer":sig_is_int,"signature_prefix":str(stub.signature)[:24],
     "swap_root_body":"returns False unconditionally","self_register_issuer_body":"returns False unconditionally"},
    "FAIL__INERT_STUBS_NOT_ADVERSARIAL_TESTS")

OUT["verdict"]={"forgery_with_known_key_succeeded":v3.startswith("ACCEPTED"),
 "trust_root_is_caller_supplied":True,"keypair_is_a_fixed_constant":(n,e,d)==(3233,17,2753),
 "candidate_hostiles_are_inert_stubs":True,
 "grade":"NOT_A_TRUST_BOUNDARY__DEMO_ILLUSTRATION_ONLY"}
print(json.dumps(OUT,indent=1))
