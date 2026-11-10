"""Event-time handoff to the installed ADP-010 availability gate."""

from dataclasses import asdict

from developmental_recursion.contracts import digest
from rawlsing_next import gt34_adp010_input_authority_acceptance as acceptance
from rawlsing_next import v3_adp010_oee_executor_obl055_replay_canonical as oee


def movement_context(evidence):
    """Address the committed conduct and recipient scope without minting authority."""
    return oee.ExactRef(
        "CONTEXT_RECEIPT",
        f"p6:{evidence['root']}:{evidence['branch']}:{evidence['event_id']}:{evidence['recipient']}",
        digest(evidence),
    )


def attempt_movement_admission(evidence):
    """Pass an eligible cue to the owner with absent owner inputs left absent."""
    if evidence["eligibility"] != "ELIGIBLE":
        return {"recipient": evidence["recipient"], "status": "NOT_SUBMITTED",
                "reason": evidence["eligibility"]}

    context = movement_context(evidence)
    # The cue is the candidate subject. P6 cannot issue its OBL054 subject
    # ingress, attest an actor phase, or translate a world tick into V3 time.
    try:
        oee.admit_available(
            subject=None,
            actor=None,
            causal_use_acceptance_receipt=None,
            effective_from=None,
            effective_until=None,
            time_granularity=None,
            context_or_world_receipt_refs=(context,),
            prior_ledger_anchor_ref=None,
            provenance_refs=(),
        )
    except oee.OEEAdmissionError as refusal:
        registry = acceptance.candidate_registry_artifact()
        return {
            "recipient": evidence["recipient"],
            "status": "OWNER_REFUSED",
            "gate": "AVAILABLE",
            "reason": str(refusal),
            "context": asdict(context),
            "registry_ref": registry["registry_ref"],
            "registry_state": registry["current_registry_state"],
        }
    raise RuntimeError("ADP-010 admitted a cue without governed subject or actor inputs")
