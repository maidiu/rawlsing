from __future__ import annotations

import hashlib

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import MechanismRuleIdentity
from rawlsing_next.sdtf_r4_d1_hosting_replay import (
    D1Context,
    D1FactPointer,
    D1HostingAdapter,
    D1RuleApplicationRef,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _fact(label: str) -> D1FactPointer:
    return D1FactPointer(
        fact_ref=ExactRef("COURT_TEST_FACT", f"urn:court:{label}", _h(label)),
        context=D1Context("world-court", "state-court", "sv1", "t1"),
    )


def prove_blocker() -> dict[str, str | bool]:
    # R1 can identify an exact rule body without making it current.  No R1
    # MechanismRuleAuthorityBinding and no require_current_rule_admission() proof
    # is supplied anywhere in this construction.
    r1_identity = MechanismRuleIdentity(
        "COURT_UNADMITTED_RULE",
        "1.0.0",
        _h("court-unadmitted-rule-body"),
    )

    # R2 independently reconstructs a rule application from raw id/version/hash.
    r2_application = D1RuleApplicationRef(
        rule_application_id="COURT_UNADMITTED_APPLICATION",
        rule_id=r1_identity.rule_id,
        rule_version=r1_identity.rule_version,
        rule_hash=r1_identity.rule_content_hash,
    )

    # Exact identity is not conserved across the seam: the kind differs even
    # though object id and content hash are textually reconstructed from the
    # same three fields.
    assert r1_identity.ref.kind == "SDTF_R4_MECHANISM_RULE"
    assert r2_application.mechanism_rule_ref.kind == "MECHANISM_RULE_RECORD"
    assert r1_identity.ref != r2_application.mechanism_rule_ref

    # Decisive bypass: R2 hosts the derivation and marks it SUPPORTED_CURRENT
    # without any R1 authority binding or rule-current selection evidence.
    repo = D1HostingAdapter()
    determinant = _fact("determinant")
    output = _fact("derived-output")
    revision = repo.host_direct_derivation(
        r2_application,
        determinant_facts=(determinant,),
        output_fact=output,
    )
    assert revision.status == "SUPPORTED_CURRENT"
    assert output.fact_ref in repo.current_output_refs()

    return {
        "r1_rule_kind": r1_identity.ref.kind,
        "r2_rule_kind": r2_application.mechanism_rule_ref.kind,
        "exact_rule_identity_conserved": False,
        "r1_current_admission_supplied": False,
        "r2_current_derivation_hosted": True,
    }


if __name__ == "__main__":
    print(prove_blocker())
