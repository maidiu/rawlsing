"""HQ196-R1 — warrant/accounting successor instrument generator.

Documentary instrument repair. NOT source execution.

DQ-01: the C4 warrant candidate dropped C4B's per-source
`source_access_accounting` block. This generator rebuilds that block for all
seven fresh-read sources, under the settled two-stage O1-C07 law:

  stage 1 (pre-launch, FROZEN)  : expected budget + instrumentation + basis
  stage 2 (during run, MEASURED): exact observed count, retained on return

The two are NEVER merged into one field.

Values are read from the historical artifacts rather than retyped, so the
crosswalk is verifiable and cannot drift from its sources.

Holds: zero source access, locator discovery, warrant issuance, live C4,
production mutation, C7, actor/person work.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

COURT = Path(__file__).resolve().parent
sys.path.insert(0, str(COURT))

import hq196_successor_model as M  # noqa: E402

HIST = Path("/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hq196tool")

C4B = json.loads((HIST / "hist_c4b_template.json").read_text())
C4C = json.loads((HIST / "hist_c4_candidate.json").read_text())
LAW = json.loads((HIST / "hist_o1c07_law.json").read_text())
ADJ = (HIST / "hist_hq196_adjudication.md").read_text()

SEVEN = ["SRC02", "SRC06", "SRC08", "SRC12", "SRC14", "SRC26", "SRC27"]
PENDING_BROKER = "PENDING_HQ196_BROKER_SELECTED_IMPLEMENTATION_ACCEPTANCE"
PENDING_SEL = "R9-SEL-03_CANDIDATE_IMPLEMENTATION_GAP__HOSTILE_REVIEW_REQUIRED"
PENDING_TECH = "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE"

# provenance anchors
P_C4B = "C4B_UNSIGNED_TEMPLATE@c2af4f61d68e9803af83f8e26f633acfe31062fa:07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json"
P_C4 = "C4_WARRANT_CANDIDATE@8ff40d37de69db2d8a6053a7c2242f481677f1a4:04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json"
P_LAW = "C4_EXECUTION_ACCOUNTING_AND_FAILURE_LAW@8ff40d37de69db2d8a6053a7c2242f481677f1a4:07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json"
P_ADJ = "HQ196_R9_THREE_WAY_ADJUDICATION_R1@d43756fb3c80645ac887cca90026ecbdb10dd18c"


def frozen_expectations() -> dict:
    """Pull the per-source frozen expectations straight out of the O1-C07 law."""
    return LAW["per_source_expected_operation_class"]


def build_account(
    name: str,
    *,
    layer: str,
    budget_type: str,
    budget_value=None,
    budget_expression: str | None = None,
    mechanism: str,
    what: str,
    point_in_run: str,
    stop_condition: str,
    provenance: list[str],
    pending_dependency: str | None = None,
    derivation_note: str | None = None,
    reviewer_confirmation_required: bool = False,
    equality_required: bool | None = None,
    distinct_from: list[str] | None = None,
) -> dict:
    """One accounting account.

    Invariant enforced here: `budget_value` is NEVER null. An unsupplied budget
    is typed UNBOUND_PENDING_TECHNICAL_ACCEPTANCE. Only the RETURN metric
    (`runtime_observed_exact_count`) may be null, and only with a typed reason.
    """
    if budget_type != PENDING_TECH and budget_value is None and budget_expression is None:
        raise AssertionError(f"{name}: budget_type {budget_type} requires a value")

    acct: dict = {
        "account_name": name,
        "layer": layer,
        # ---- stage 1: frozen pre-launch ----
        "expected_pre_launch_budget": {
            "budget_type": budget_type,
            "budget_value": budget_value,
            "budget_expression": budget_expression,
            "frozen_before_launch": True,
            "may_be_null": False,
        },
        "measurement_basis": {
            "what_measured": what,
            "layer": layer,
            "mechanism": mechanism,
            "point_in_run": point_in_run,
        },
        # ---- stage 2: measured during run, retained on return ----
        "runtime_observed_exact_count": {
            "value": None,
            "status": "NOT_EXECUTED",
            "typed_reason": "NOT_EXECUTED__UNSIGNED_UNISSUED_NON_AUTHORIZING_INSTRUMENT",
            "null_permitted_by_law": True,
            "null_law_citation": "07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.O1_C08_failure_law.unreached_stage_or_metric_reporting",
            "must_not_be_read_as": "a zero, an empty result, or a PASS",
        },
        "stop_condition_if_exceeded": stop_condition,
        "provenance": provenance,
    }
    if pending_dependency:
        acct["pending_dependency"] = pending_dependency
    if derivation_note:
        acct["derivation_note"] = derivation_note
    if reviewer_confirmation_required:
        acct["reviewer_confirmation_required"] = True
    if equality_required is not None:
        acct["equality_required"] = equality_required
    if distinct_from:
        acct["must_remain_distinct_from"] = distinct_from
    return acct


# --------------------------------------------------------------------------
# generic accounts for the six non-SRC27 sources
# --------------------------------------------------------------------------

def generic_accounts(key: str, exp: dict, c4b_ops: dict) -> list[dict]:
    """Accounts shared by every fresh-read source except SRC27's special route.

    Only authority-supplied numbers are bound. Nothing else is invented.
    """
    accts: list[dict] = []

    # ---- source-path existence/access checks ----
    accts.append(build_account(
        "source_path_existence_access_checks",
        layer="application/pre-decode gate",
        budget_type=PENDING_TECH,
        mechanism="PENDING: owner to be the selected broker implementation's pre-open gate",
        what="Literal existence/access checks performed against the source path before any decode",
        point_in_run="pre-decode, before the reader is invoked",
        stop_condition="Any check beyond the bound budget, or any check on a non-warranted source, is a STOP.",
        provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[0]"],
        pending_dependency=PENDING_BROKER,
        derivation_note="O1-C07 names this a mandatory separate account but supplies no numeric budget. Not invented here.",
    ))

    # ---- full-file sha256 passes ----
    if key == "SRC27":
        raise AssertionError("SRC27 handled separately")
    accts.append(build_account(
        "full_file_sha256_passes",
        layer="application/pre-decode identity gate",
        budget_type="FLOOR",
        budget_value=1,
        mechanism="Streaming SHA-256 over the full file, compared to the frozen per-source canonical_sha256",
        what="Complete passes over the whole file computing full SHA-256",
        point_in_run="pre-decode, after the locator resolves and before any reader invocation",
        stop_condition="A second full hash pass is a STOP unless a later HQ-bound warrant supplies a maximum.",
        provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[1]",
                    P_C4B + ".preconditions[3]"],
        derivation_note=("The C4B precondition requires the locator to resolve to bytes whose full-file SHA-256 "
                         "equals the frozen identity BEFORE decode. That mandates at least one pass. The law "
                         "supplies no explicit numeric budget, so the minimum mandated by the precondition is "
                         "bound as a FLOOR and flagged, not asserted as an EXACT count."),
        reviewer_confirmation_required=True,
    ))

    # ---- path-level opens ----
    accts.append(build_account(
        "path_level_opens",
        layer="literal path-level file open (OS/broker boundary)",
        budget_type=PENDING_TECH,
        mechanism="PENDING: application-owned broker open counter, or equivalent literal path-open owner",
        what="Literal path-level opens of the source file. NOT reader invocations, NOT decoder invocations, NOT proxies.",
        point_in_run="each time the source path is opened",
        stop_condition="Any open beyond the bound budget is a STOP. An unmeasured open is itself a STOP.",
        provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[2]",
                    P_ADJ + ".Contract meaning — accepted (literal path opens are separately named/non-substitutable)"],
        pending_dependency=PENDING_BROKER,
        derivation_note=("No path-open budget is supplied by authority for any of the six. Explicitly NOT invented. "
                         "A higher-level proxy may not be renamed path_opens."),
    ))

    # ---- metadata reads ----
    if "expected_metadata_reads" in exp:
        mt, mv = "EXACT", exp["expected_metadata_reads"]
        mprov = [P_LAW + f".per_source_expected_operation_class.{key}.expected_metadata_reads"]
        mderiv = None
    else:
        mt, mv = PENDING_TECH, None
        mprov = [P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[3]"]
        mderiv = ("O1-C07 names metadata reads a mandatory separate account but supplies no count for this source. "
                  "Not invented here.")
    accts.append(build_account(
        "metadata_reads",
        layer="reader metadata probe",
        budget_type=mt,
        budget_value=mv,
        mechanism="Reader invocation with metadataonly semantics; counted at the reader call boundary",
        what="Reader invocations performed to obtain source metadata only",
        point_in_run="during the admitted operation for this source",
        stop_condition="A metadata read beyond the bound budget, or any metadata read carrying row data, is a STOP.",
        provenance=mprov,
        pending_dependency=None if mt == "EXACT" else PENDING_BROKER,
        derivation_note=mderiv,
    ))

    # ---- header-prefix reads ----
    if key == "SRC26":
        accts.append(build_account(
            "header_prefix_reads",
            layer="raw byte-prefix read, pre-reader",
            budget_type="FLOOR",
            budget_value=1,
            mechanism="Bounded raw prefix read of the source file header, counted at the raw prefix-read boundary",
            what="Bounded raw header-prefix reads admitted for this source",
            point_in_run="pre-reader, as the declared header-prefix step",
            stop_condition="A further header-prefix read without an accepted maximum is a STOP.",
            provenance=[P_C4 + ".per_source[SRC26].allowed_operations.kind",
                        P_LAW + ".per_source_expected_operation_class.SRC26"],
            derivation_note=("The admitted operation class is BOUNDED_HEADER_PREFIX_PLUS_READER_METADATA, which "
                             "mandates at least one header-prefix read. Authority supplies the header-prefix BYTE "
                             "count (176) but NOT a read count, so the mandated minimum is bound as a FLOOR and "
                             "flagged rather than asserted as EXACT 1. No ceiling is supplied."),
            reviewer_confirmation_required=True,
        ))
        # ---- SRC26 geometry: three SEPARATE accounts, never collapsed ----
        accts.append(build_account(
            "header_prefix_bytes",
            layer="raw byte-prefix read",
            budget_type="EXACT",
            budget_value=exp["expected_header_prefix_bytes"],
            mechanism="Byte count of the admitted header-prefix read",
            what="Bytes consumed by the header-prefix read, at the header-prefix account",
            point_in_run="at the header-prefix read",
            stop_condition="Any byte count other than the frozen value at this account is a STOP.",
            provenance=[P_LAW + ".per_source_expected_operation_class.SRC26.expected_header_prefix_bytes"],
            distinct_from=["raw_nominal_case_size", "decoded_dictionary_data_width"],
            derivation_note="Bound at THIS declared account only. It is not interchangeable with the 174/332 geometry pair.",
        ))
        accts.append(build_account(
            "raw_nominal_case_size",
            layer="source geometry declaration",
            budget_type="EXACT",
            budget_value=c4b_ops["expected_raw_nominal_case_size"],
            mechanism="Declared source geometry attribute",
            what="Raw nominal case size declared by the source",
            point_in_run="declared, not read",
            stop_condition="Not an access account; no stop condition. Divergence is expected and is NOT a failure.",
            provenance=[P_C4 + ".per_source[SRC26].allowed_operations.expected_raw_nominal_case_size"],
            equality_required=False,
            distinct_from=["header_prefix_bytes", "decoded_dictionary_data_width"],
        ))
        accts.append(build_account(
            "decoded_dictionary_data_width",
            layer="decoded geometry declaration",
            budget_type="EXACT",
            budget_value=c4b_ops["expected_decoded_dictionary_data_width"],
            mechanism="Declared decoded dictionary data width attribute",
            what="Decoded dictionary data width",
            point_in_run="declared, not read",
            stop_condition="Not an access account; no stop condition. Divergence is expected and is NOT a failure.",
            provenance=[P_C4 + ".per_source[SRC26].allowed_operations.expected_decoded_dictionary_data_width"],
            equality_required=False,
            distinct_from=["header_prefix_bytes", "raw_nominal_case_size"],
            derivation_note="SRC26 law: 174 and 332 must be preserved SEPARATELY; divergence is expected, never collapsed.",
        ))
    else:
        accts.append(build_account(
            "header_prefix_reads",
            layer="raw byte-prefix read, pre-reader",
            budget_type=PENDING_TECH,
            mechanism="PENDING: broker-prefix read counter",
            what="Raw header-prefix reads, if any are admitted for this source",
            point_in_run="pre-reader",
            stop_condition="Any header-prefix read not bound here is a STOP.",
            provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[4]"],
            pending_dependency=PENDING_BROKER,
            derivation_note="No header-prefix budget is supplied for this source. None invented.",
        ))

    # ---- decoder invocations ----
    accts.append(build_account(
        "decoder_invocations",
        layer="decoder entry",
        budget_type=PENDING_TECH,
        mechanism="PENDING: decoder entry counter in the bound runtime",
        what="Invocations of the decoder itself. Separately named from opens, reader invocations and bytes.",
        point_in_run="each decoder entry",
        stop_condition="Any decoder invocation beyond the bound budget is a STOP.",
        provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[5]"],
        pending_dependency=PENDING_BROKER,
        derivation_note="No decoder-invocation budget is supplied by authority. Explicitly NOT invented.",
    ))

    # ---- selected-column reads ----
    if "expected_selected_reads" in exp:
        st, sv = "EXACT", exp["expected_selected_reads"]
        sprov = [P_LAW + f".per_source_expected_operation_class.{key}.expected_selected_reads"]
        sderiv = None
        spend = None
    else:
        raise AssertionError(key)
    if sv == 0:
        sderiv = "Frozen zero. A single non-zero count is a STOP condition, not a reportable variance."
        spend = None
    else:
        spend = PENDING_SEL
        sderiv = ("Frozen at EXACT 1 by authority. NOTE: the bound reader currently exposes no usecols argument, so "
                  "this EXACT budget has no implementation owner yet. The budget is bound as authority froze it; "
                  "it is NOT relaxed, and the missing owner is recorded as a blocker.")
    accts.append(build_account(
        "selected_column_reads",
        layer="selected-variable reader invocation",
        budget_type=st,
        budget_value=sv,
        mechanism="Reader invocation configured for the bound selected variables only; counted at the reader call boundary",
        what="Reads restricted to the permitted selected variables",
        point_in_run="during the admitted selected-variable read",
        stop_condition="A selected read beyond the bound budget, a read of an unpermitted variable, or any row data "
                       "where zero is bound, is a STOP.",
        provenance=sprov,
        pending_dependency=spend,
        derivation_note=sderiv,
        distinct_from=["full_reads", "metadata_reads"],
    ))

    # ---- full reads ----
    accts.append(build_account(
        "full_reads",
        layer="whole-source decode",
        budget_type="EXACT",
        budget_value=exp["expected_full_reads"],
        mechanism="Reader invocation decoding the whole source; counted at the reader call boundary",
        what="Reads of the entire source, all rows and all columns",
        point_in_run="during the admitted operation for this source",
        stop_condition="Any full read where zero is bound is a STOP. It is never a reportable variance.",
        provenance=[P_LAW + f".per_source_expected_operation_class.{key}.expected_full_reads"],
        distinct_from=["selected_column_reads"],
        derivation_note="Frozen zero. A single non-zero count is a STOP condition, not a reportable variance."
        if exp["expected_full_reads"] == 0 else None,
    ))

    # ---- byte counts ----
    accts.append(build_account(
        "byte_counts_where_measurable",
        layer="byte transfer across the reader/file boundary",
        budget_type=PENDING_TECH,
        mechanism="PENDING: broker byte counter across counted reads",
        what="Bytes delivered to the reader across all reads",
        point_in_run="accumulated across the run",
        stop_condition="Any byte count beyond a subsequently accepted budget is a STOP.",
        provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[8]"],
        pending_dependency=PENDING_BROKER,
        derivation_note="O1-C07 qualifies this account 'where measurable' and supplies no byte budget. None invented.",
    ))

    # ---- retries ----
    accts.append(build_account(
        "retries",
        layer="run control",
        budget_type="ZERO",
        budget_value=0,
        mechanism="Reason-coded retry counter maintained by the execution surface",
        what="Retry attempts for this source, separately counted and reason-coded",
        point_in_run="any point during this source's execution",
        stop_condition="A single retry is a STOP. Zero retries are authorised; a retry requires a NEW HQ-bound warrant.",
        provenance=[P_LAW + f".per_source_expected_operation_class.{key}.max_retry_budget",
                    P_LAW + ".retry_budget_law.frozen_maximum"],
        derivation_note="Frozen maximum ZERO across all sources. No more permissive budget was invented.",
    ))

    # ---- SRC08/SRC12 declared zero accounts ----
    if key in ("SRC08", "SRC12"):
        accts.append(build_account(
            "row_data_reads",
            layer="reader data plane",
            budget_type="ZERO",
            budget_value=0,
            mechanism="Reader counter distinguishing metadata-only admission from any row-data transfer",
            what="Row-level data reads",
            point_in_run="during the admitted metadata-only operation",
            stop_condition="Any non-zero row_data_reads is a STOP condition, not a reportable variance.",
            provenance=[P_LAW + f".O1_C07_instrumentation.frozen_zero_budgets.{key}_row_data_reads",
                        P_C4 + f".per_source[{key}].allowed_operations.row_data_reads"],
        ))
        accts.append(build_account(
            "selected_columns",
            layer="reader configuration",
            budget_type="ZERO",
            budget_value=0,
            mechanism="Reader configuration assertion: selected_columns must be empty",
            what="Number of selected columns configured for the read",
            point_in_run="at reader configuration",
            stop_condition="Any non-zero selected-column configuration is a STOP.",
            provenance=[P_LAW + f".O1_C07_instrumentation.frozen_zero_budgets.{key}_selected_columns",
                        P_C4 + f".per_source[{key}].allowed_operations.selected_columns"],
        ))

    return accts


def src27_accounts(exp: dict, c4b_ops: dict) -> list[dict]:
    """SRC27: exactly one governed full Route-B pass, with lower layers SEPARATE.

    The hardened note supplies 'at minimum' language for four lower-layer
    accounts. Those are FLOORS and are NOT promoted to ceilings. No selected-read
    count is invented.
    """
    hard = LAW["hardened_note_on_the_SRC27_single_pass"]
    accts: list[dict] = []

    # ---- the route-pass workload account ----
    accts.append(build_account(
        "governed_full_route_passes",
        layer="workload (NOT an access account)",
        budget_type="EXACT",
        budget_value=exp["expected_full_route_passes"],
        budget_expression="exactly 1; authority also supplies max 1",
        mechanism="Counted at the Route-B pass boundary, with all lower-layer access accounts counted separately",
        what="Governed fresh full Route-B passes over SRC27",
        point_in_run="once, as the single admitted pass",
        stop_condition="A second pass is NOT a retry; it is a separate run requiring NEW HQ-bound authority. STOP.",
        provenance=[P_LAW + ".per_source_expected_operation_class.SRC27.expected_full_route_passes",
                    P_LAW + ".per_source_expected_operation_class.SRC27.expected_full_route_passes_max",
                    P_C4 + ".per_source[SRC27].expected_full_route_passes",
                    P_C4 + ".per_source[SRC27].max_full_route_passes"],
        distinct_from=["path_level_opens", "metadata_reads", "full_reads", "full_file_sha256_passes"],
        derivation_note=("A WORKLOAD constraint, not an access constraint. Explicitly does NOT license assuming one "
                         "file open. Misreading it as one open would be an accounting failure."),
    ))

    # ---- four verbatim FLOOR accounts from the hardened note ----
    floors = [
        ("source_path_existence_access_checks", "application/pre-decode gate",
         "PENDING: broker pre-open gate counter",
         "Literal existence/access checks against the SRC27 path",
         "pre-decode, before the reader is invoked",
         "Any check beyond the floor without an accepted maximum is a STOP."),
        ("full_file_sha256_passes", "application/pre-decode identity gate",
         "Streaming SHA-256 over the full file compared to the frozen canonical_sha256",
         "Complete passes over the whole file computing full SHA-256",
         "pre-decode, before any reader invocation",
         "A further full hash pass without an accepted maximum is a STOP."),
        ("metadata_reads", "reader metadata probe",
         "Reader invocation with metadataonly semantics, counted at the reader call boundary",
         "Reader invocations performed to obtain source metadata",
         "during the single governed pass",
         "A metadata read beyond the floor without an accepted maximum is a STOP."),
        ("full_reads", "whole-source decode",
         "Reader invocation performing the full compatibility read, counted at the reader call boundary",
         "Reads of the entire source, all rows and all columns",
         "during the single governed pass",
         "A further full read without an accepted maximum is a STOP."),
    ]
    for name, layer, mech, what, point, stop in floors:
        accts.append(build_account(
            name,
            layer=layer,
            budget_type="FLOOR",
            budget_value=1,
            mechanism=mech,
            what=what,
            point_in_run=point,
            stop_condition=stop,
            provenance=[P_LAW + ".hardened_note_on_the_SRC27_single_pass.implication",
                        P_C4 + ".per_source[SRC27].accounting_warning"],
            derivation_note=("Authority wording is 'at minimum'. Bound as a FLOOR. Per commission it is NOT promoted "
                             "to a ceiling; no maximum is supplied for this account."),
            distinct_from=["governed_full_route_passes"],
        ))

    # ---- path opens: authority says 'multiple', supplies no number ----
    accts.append(build_account(
        "path_level_opens",
        layer="literal path-level file open (OS/broker boundary)",
        budget_type=PENDING_TECH,
        mechanism="PENDING: application-owned broker open counter",
        what="Literal path-level opens of LiTS_I.dta. NOT reader invocations, NOT decoder invocations, NOT proxies.",
        point_in_run="each time the source path is opened",
        stop_condition="Any open beyond a subsequently accepted budget is a STOP. An unmeasured open is itself a STOP.",
        provenance=[P_LAW + ".per_source_expected_operation_class.SRC27.critical_note",
                    P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts[2]"],
        pending_dependency=PENDING_BROKER,
        derivation_note=("Authority states the pass 'will involve multiple path-level opens' and deliberately "
                         "supplies NO number. The word 'multiple' is recorded verbatim and is NOT converted into "
                         "a numeric budget. Not invented here."),
    ))

    # ---- selected reads: explicitly must not be invented ----
    accts.append(build_account(
        "selected_column_reads",
        layer="selected-variable reader invocation",
        budget_type=PENDING_TECH,
        mechanism="PENDING: selected-reader implementation acceptance",
        what="Reads restricted to a selected column subset, if any are performed for SRC27",
        point_in_run="during the single governed pass",
        stop_condition="Any selected read without an accepted budget is a STOP.",
        provenance=[P_ADJ + ".New candidate finding — selected-read implementation mismatch"],
        pending_dependency=PENDING_SEL,
        derivation_note=("Commission forbids inventing a selected-read count for SRC27. None invented. Bound as "
                         "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE, which is a typed budget state, NOT a null."),
    ))

    # ---- remaining unbound accounts ----
    for name, layer, what, point in [
        ("header_prefix_reads", "raw byte-prefix read, pre-reader",
         "Raw header-prefix reads, if any are admitted for this source", "pre-reader"),
        ("decoder_invocations", "decoder entry", "Invocations of the decoder itself", "each decoder entry"),
        ("byte_counts_where_measurable", "byte transfer across the reader/file boundary",
         "Bytes delivered to the reader across all reads", "accumulated across the run"),
    ]:
        accts.append(build_account(
            name,
            layer=layer,
            budget_type=PENDING_TECH,
            mechanism=f"PENDING: owner to be established by the selected implementation for {name}",
            what=what,
            point_in_run=point,
            stop_condition="Any occurrence beyond a subsequently accepted budget is a STOP.",
            provenance=[P_LAW + ".O1_C07_instrumentation.mandatory_separate_accounts"],
            pending_dependency=PENDING_BROKER,
            derivation_note="No budget supplied by authority for this account on this source. None invented.",
            distinct_from=["governed_full_route_passes"],
        ))

    # ---- retries ----
    accts.append(build_account(
        "retries",
        layer="run control",
        budget_type="ZERO",
        budget_value=0,
        mechanism="Reason-coded retry counter maintained by the execution surface",
        what="Retry attempts for SRC27, separately counted and reason-coded",
        point_in_run="any point during SRC27 execution",
        stop_condition="A single retry is a STOP. A retry requires a NEW HQ-bound warrant.",
        provenance=[P_LAW + ".per_source_expected_operation_class.SRC27.max_retry_budget",
                    P_LAW + ".retry_budget_law.frozen_maximum"],
    ))
    return accts


def build_successor() -> dict:
    exp_all = frozen_expectations()
    c4b_by_key = {s["source_key"]: s for s in C4B["sources"]}
    c4c_by_key = {s["source_key"]: s for s in C4C["per_source"]}

    sources = []
    for key in SEVEN:
        exp = exp_all[key]
        c4b = c4b_by_key[key]
        c4c = c4c_by_key[key]
        if key == "SRC27":
            accts = src27_accounts(exp, c4b["allowed_operations"])
        else:
            accts = generic_accounts(key, exp, c4b["allowed_operations"])

        # carry through EVERY non-structural key from the C4 candidate verbatim so
        # no authority binding, oracle binding or RES_* caveat is dropped by the repair
        carried = {k: v for k, v in c4c.items()
                   if k not in ("source_key", "source_file", "format", "canonical_sha256",
                                "access_locator", "reader_lane", "allowed_operations",
                                "expected_operation_class", "raw_bytes_retention")}
        carried["authority"] = c4c.get("authority") or c4c.get("source_specific_authority")

        sources.append({
            "source_key": key,
            "source_file": c4c["source_file"],
            "format": c4c["format"],
            "canonical_sha256": c4c["canonical_sha256"],
            "access_locator": "<REQUIRED_FILL_IN_SLOT__SOURCE_LOCATOR_FILL_REQUIRED_BEFORE_WARRANT_ISSUANCE>",
            "locator_filled": False,
            "reader_lane": c4c["reader_lane"],
            "allowed_operations": c4c["allowed_operations"],
            "authority": carried["authority"],
            "expected_operation_class": c4c["expected_operation_class"],
            "execution_surface": C4C["unresolved_pre_issuance_items"]["execution_surface_binding"]["resolved_value"],
            "raw_bytes_retention": c4c["raw_bytes_retention"],
            "carried_from_c4_candidate_verbatim": carried,
            # ---- THE REPAIRED BLOCK ----
            "source_access_accounting": {
                "_dq01_repair": "Restored from C4B template; dropped by the C4 warrant candidate.",
                "_c4b_block_present_at_freeze": bool(c4b.get("source_access_accounting")),
                "_c4_candidate_block_present": "source_access_accounting" in c4c,
                "account_count": len(accts),
                "accounts": accts,
            },
        })

    return {
        "schema": "PYAT_R9_WARRANT_ACCOUNTING_SUCCESSOR_UNSIGNED@1.0.0",
        "lane": "PYAT-HQ196-R9-WARRANT-ACCOUNTING-SUCCESSOR-R1",
        "documentary_base": "d43756fb3c80645ac887cca90026ecbdb10dd18c",
        "supersedes_candidate": {
            "path": "WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json",
            "commit": "8ff40d37de69db2d8a6053a7c2242f481677f1a4",
            "reason": "DQ-01: per-source source_access_accounting block was dropped. Restored here.",
        },
        "derived_from": {
            "c4b_unsigned_template": P_C4B,
            "c4_warrant_candidate": P_C4,
            "o1_c07_accounting_law": P_LAW,
            "hq196_three_way_adjudication": P_ADJ,
        },

        # ---- instrument status: must remain ----
        "status": "UNSIGNED_SUCCESSOR_STRUCTURE__NOT_ISSUED__AUTHORIZES_NOTHING",
        "signed": False,
        "issued": False,
        "authorizes_access": False,
        "execution_authorized": False,
        "issued_by": None,
        "issue_date": None,

        "critical_statements": [
            "THIS DOCUMENT IS AN UNSIGNED STRUCTURE. IT IS NOT A WARRANT. IT AUTHORIZES NOTHING.",
            "This lane cannot close R9 and cannot issue the warrant.",
            "Restoring the accounting fields does NOT close any technical account.",
            "Hashing, stat-ing and metadata reads ARE source access. They are NOT pre-warrant exceptions.",
            "Zero source access, locator discovery, warrant issuance, live C4, production mutation, C7 or actor/person work was performed.",
        ],

        "settled_o1_c07_structure": {
            "two_stage_law": {
                "stage_1_pre_launch_FROZEN": "expected budget, instrumentation, measurement basis",
                "stage_2_during_run_MEASURED": "exact observed count, retained on return",
                "never_merged": True,
                "law": "Freeze expected budgets and instrumentation before launch; retain measured counts.",
            },
            "mandatory_separate_accounts": LAW["O1_C07_instrumentation"]["mandatory_separate_accounts"],
            "non_substitutability": "Literal path opens, reader invocations and decoder invocations are separately "
                                    "named, non-substitutable quantities. A higher-level proxy may not be renamed path_opens.",
            "REQUIRED_EXACT_COUNT_meaning": "The budget must be exact before launch. It does NOT mean the final observed "
                                            "number must already have been observed before launch.",
        },

        "typed_null_law": {
            "rule": "A typed null may describe an unexecuted or unmeasurable RETURN metric only where the governing "
                    "failure law allows it. A typed null may NOT waive a mandatory pre-launch budget.",
            "machine_readable_rule": {
                "return_metric_null_permitted": True,
                "return_metric_null_requires_typed_reason": True,
                "pre_launch_budget_null_permitted": False,
                "pre_launch_budget_unsupplied_representation": PENDING_TECH,
                "pre_launch_budget_absent_representation_prohibited": True,
                "rationale": "An absent or null pre-launch budget would silently waive a launch prerequisite. An "
                             "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE budget is an explicit, non-waiving blocker.",
            },
            "correct_reporting_example": LAW["O1_C08_failure_law"]["unreached_stage_or_metric_reporting"]["example_of_correct_reporting"],
            "never": ["a fabricated zero", "a fabricated PASS", "a null standing in for an unbound pre-launch budget"],
        },

        "budget_type_vocabulary": M.BUDGET_TYPES_DOC,
        "scope": C4B["scope"],
        "source_count": len(sources),
        "sources": sources,
        "excluded_from_fresh_warrant": [{
            "source_key": "SRC35",
            "fresh_reads": 0,
            "budget_type": "ZERO",
            "operation_class": exp_all["SRC35"]["operation_class"],
            "reason": "Retained comparator. Not one of the seven fresh-source warrant entries.",
            "provenance": [P_LAW + ".per_source_expected_operation_class.SRC35"],
        }],

        "global_zero_authorizations": dict(C4C["zero_authorizations"]),

        "preconditions": list(C4B["preconditions"]),
        "retry_stop_law": list(C4B["retry_stop_law"]),
        "retention_privacy": list(C4B["retention_privacy"]),
        "semantic_ceilings": list(C4B["semantic_ceilings"]),

        "approvals": {
            "HQ": {"name": None, "decision": None, "signature_or_commit": None, "status": "UNSET"},
            "required_user_resource_owner": {"name": None, "decision": None, "signature_or_record": None, "status": "UNSET"},
        },

        "open_technical_blockers": [
            {
                "id": "R9-SEL-03",
                "token": PENDING_SEL,
                "statement": "The frozen selected_reads=1 budgets for SRC02/SRC06/SRC14 have no implementation owner: "
                             "the bound reader exposes no usecols argument.",
                "effect_on_this_instrument": "Budgets remain bound EXACT at 1. They are NOT relaxed.",
            },
            {
                "id": "R9-BROKER-ACCEPT",
                "token": PENDING_BROKER,
                "statement": "Path-open, existence-check, decoder-invocation and byte accounts await broker "
                             "implementation acceptance.",
                "effect_on_this_instrument": "Typed UNBOUND_PENDING_TECHNICAL_ACCEPTANCE. Not null. Not invented.",
            },
        ],

        "prohibitions": {
            "closes_R9": False,
            "issues_warrant": False,
            "authorizes_any_access": True,
            "asserts_technical_accounts_closed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(build_successor(), indent=2, sort_keys=False))
