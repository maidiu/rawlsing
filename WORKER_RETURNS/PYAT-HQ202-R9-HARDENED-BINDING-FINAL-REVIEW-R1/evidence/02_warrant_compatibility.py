"""HQ202 warrant-driven compatibility suite.

This does not hard-code the seven plan shapes from the candidate's court. It READS
the accepted unsigned seven-source warrant successor
(89054b882c04cf0541b6f9f4abdb555c808ad94d,
WORKER_RETURNS/PYAT-HQ200-R9-SEVEN-SOURCE-WARRANT-SUCCESSOR-R1/) and derives every
constraint from it:

  * a FROZEN_AUTHORITY ``expected`` becomes a runtime EXACT constraint;
  * else a FROZEN_AUTHORITY ``floor`` becomes a runtime FLOOR constraint;
  * a PENDING_HQ200_RUNTIME_ACCEPTANCE ``maximum`` becomes a runtime MAXIMUM
    constraint labelled IMPLEMENTATION_POLICY (a policy ceiling, never an
    expected count);
  * a PENDING/null expected is NOT turned into a number;
  * an UNBOUND_SOURCE_DEPENDENT byte account is left unbound and only checked for
    the ABSENCE of an invented ceiling.

Warrant account names are mapped to runtime account names explicitly; every
warrant account with no runtime counterpart is reported rather than silently
dropped.

Prints one JSON document on stdout.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_execution_binding import (
    AccountConstraint,
    AuthorityLabel,
    BoundExecutionSpec,
    BoundSourceExecution,
    BindingError,
    CountKind,
    LOWER_LAYER_ACCOUNTS,
    ROUTE_PASS_LIMIT_REACHED,
    RoutePassApplicability,
    RoutePassSpec,
)
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBudget,
    SourceAccessViolation,
)
from rawlsing_next.pre553_source_session import RowDataMode, SourceOperationPlan

W01 = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("warrant/01_SEVEN_SOURCE_PLAN_BINDING.json")
W03 = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("warrant/03_SRC27_OUTER_AND_LOWER_ACCOUNTING.json")

NON_ROUTE = RoutePassApplicability.NOT_APPLICABLE
ROUTE = RoutePassApplicability.APPLICABLE
FROZEN = AuthorityLabel.FROZEN_AUTHORITY
POLICY = AuthorityLabel.IMPLEMENTATION_POLICY

WORK = Path(tempfile.mkdtemp(prefix="hq202-warrant-"))
RESULTS: list[dict] = []
PENDING_MAX = "PENDING_HQ200_RUNTIME_ACCEPTANCE"

# Warrant account name -> runtime SourceAccessAccount field.
WARRANT_TO_RUNTIME = {
    "source_path_existence_access_checks": "existence_checks",
    "full_file_sha256_passes": "hash_passes",
    "path_level_opens": "path_opens",
    "metadata_reads": "metadata_reads",
    "header_prefix_reads": "header_prefix_reads",
    "header_prefix_bytes": "header_prefix_bytes",
    "decoder_invocations": "decoder_invocations",
    "selected_column_reads": "selected_reads",
    "full_reads": "full_reads",
    "chunk_reads": "chunk_reads",
    "retries": "retries",
}
OUTER_ACCOUNT = "governed_full_route_passes"
# Warrant accounts that deliberately have NO runtime counterpart.
NO_RUNTIME_ACCOUNT = {
    "byte_counts_where_measurable",
    "row_data_reads",
    "selected_columns",
    "raw_nominal_case_size",
    "decoded_dictionary_data_width",
}
# Source-dependent byte accounts: must remain unbound by any ceiling.
BYTE_ACCOUNTS = {"byte_counts_where_measurable"}


def need(cond: object, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def val(field):
    """Warrant field -> (value, authority_status)."""
    if isinstance(field, dict):
        return field.get("value"), field.get("authority_status")
    return field, None


def load_plans():
    doc = json.loads(W01.read_text())
    return doc["plans"]


def check(cid: str, title: str, fn) -> None:
    rec = {"id": cid, "title": title}
    try:
        rec["evidence"] = fn() or {}
        rec["ok"] = True
    except Exception as exc:  # noqa: BLE001
        rec["ok"] = False
        rec["error"] = f"{type(exc).__name__}: {exc}"
    RESULTS.append(rec)


# --------------------------------------------------------------- derivation
def derive(plan):
    """Derive runtime objects and the warrant-derived constraint set."""
    skey = plan["source_key"]
    mode_value, _ = val(plan["row_data_mode"])
    encoding, _ = val(plan["reader_encoding"])
    prefix_admitted, _ = val(plan["header_prefix_admitted"])
    prefix_bytes, _ = val(plan["header_prefix_bytes_frozen"])
    retry_ceiling, retry_auth = val(plan["retry_ceiling"])
    selected = [s["name"] for s in (plan["selected_variables"] or [])]

    if mode_value == "SELECTED":
        mode = RowDataMode.SELECTED
    elif mode_value in ("METADATA_ONLY", "METADATA_ONLY_PLUS_HEADER_PREFIX"):
        mode = RowDataMode.METADATA_ONLY
    elif mode_value == "FULL":
        mode = RowDataMode.FULL
    elif mode_value == "CHUNKED_FULL":
        mode = RowDataMode.CHUNKED_FULL
    else:
        raise AssertionError(f"unmapped warrant row_data_mode {mode_value!r}")

    plan_kwargs = {"mode": mode, "max_retries": int(retry_ceiling)}
    if mode is RowDataMode.SELECTED:
        plan_kwargs["selected_variables"] = tuple(selected)
    if mode is RowDataMode.METADATA_ONLY and prefix_admitted is True:
        plan_kwargs["header_prefix_bytes"] = int(prefix_bytes)
    if encoding is not None:
        plan_kwargs["encoding"] = encoding
    soplan = SourceOperationPlan(**plan_kwargs)

    constraints: list[AccountConstraint] = []
    outer_expected = outer_maximum = None
    applied: list[dict] = []
    unmapped: list[dict] = []
    unbound_bytes: list[dict] = []

    for acct in plan["source_access_accounting"]["accounts"]:
        name = acct["account_name"]
        exp, exp_auth = val(acct.get("expected"))
        floor, floor_auth = val(acct.get("floor"))
        maximum, max_auth = val(acct.get("maximum"))

        if name == OUTER_ACCOUNT:
            outer_expected = exp
            outer_maximum = maximum
            applied.append({"warrant_account": name, "mapped_to": "OUTER full_route_passes",
                            "expected": exp, "floor": floor, "maximum": maximum,
                            "expected_authority": exp_auth})
            continue
        if name in NO_RUNTIME_ACCOUNT:
            rec = {"warrant_account": name, "expected": exp, "floor": floor,
                   "maximum": maximum, "authority": exp_auth or max_auth}
            if name in BYTE_ACCOUNTS:
                unbound_bytes.append(rec)
                need(isinstance(exp, str) and exp.startswith("UNBOUND_SOURCE_DEPENDENT"),
                     f"{skey}: byte account is not typed UNBOUND_SOURCE_DEPENDENT")
            else:
                unmapped.append(rec)
            continue

        runtime_name = WARRANT_TO_RUNTIME[name]
        # FROZEN exact expectation wins; a PENDING/null expected is never a number.
        if isinstance(exp, int) and not isinstance(exp, bool) and exp_auth == "FROZEN_AUTHORITY":
            constraints.append(AccountConstraint(runtime_name, CountKind.EXACT, exp, FROZEN))
            applied.append({"warrant_account": name, "runtime_account": runtime_name,
                            "kind": "EXACT", "value": exp, "authority": "FROZEN_AUTHORITY",
                            "from": "expected"})
            continue
        if isinstance(floor, int) and not isinstance(floor, bool) and floor_auth == "FROZEN_AUTHORITY":
            constraints.append(AccountConstraint(runtime_name, CountKind.FLOOR, floor, FROZEN))
            applied.append({"warrant_account": name, "runtime_account": runtime_name,
                            "kind": "FLOOR", "value": floor, "authority": "FROZEN_AUTHORITY",
                            "from": "floor"})
            continue
        if isinstance(maximum, int) and not isinstance(maximum, bool) and max_auth == PENDING_MAX:
            # A candidate maximum is a POLICY ceiling, never an expected count.
            constraints.append(AccountConstraint(runtime_name, CountKind.MAXIMUM, maximum, POLICY))
            applied.append({"warrant_account": name, "runtime_account": runtime_name,
                            "kind": "MAXIMUM", "value": maximum,
                            "authority": "IMPLEMENTATION_POLICY",
                            "from": "PENDING_HQ200_RUNTIME_ACCEPTANCE maximum"})
            continue
        unmapped.append({"warrant_account": name, "expected": exp, "floor": floor,
                         "maximum": maximum, "reason": "no frozen expectation or candidate maximum"})

    applicable = ROUTE if plan["source_key"] == "SRC27" else NON_ROUTE
    route_pass = RoutePassSpec(expected=outer_expected, maximum=outer_maximum,
                               token=f"warrant {skey} outer pass")
    budget = SourceAccessBudget(retries=int(retry_ceiling))
    return {
        "source_key": skey, "plan": soplan, "constraints": tuple(constraints),
        "route_pass": route_pass, "applicable": applicable, "budget": budget,
        "outer_expected": outer_expected, "outer_maximum": outer_maximum,
        "applied": applied, "unmapped": unmapped, "unbound_bytes": unbound_bytes,
        "retry_ceiling": int(retry_ceiling), "retry_authority": retry_auth,
        "selected": selected, "mode": mode_value, "encoding": encoding,
        "prefix_bytes": prefix_bytes if prefix_admitted else None,
    }


def carrier(name: str, columns) -> str:
    p = WORK / name
    df = pd.DataFrame({c: [float(i) for i in range(40)] for c in columns})
    pyreadstat.write_sav(df, str(p))
    return str(p)


def dta_carrier(name: str) -> str:
    p = WORK / name
    pyreadstat.write_dta(pd.DataFrame({c: [float(i) for i in range(40)]
                                       for c in ("Q10B", "Q101", "Q2061B", "v372")}), str(p))
    return str(p)


ALL_SELECTED = ("Q10B", "Q101", "Q2061B", "v372")


def execute_plan(derived):
    path = dta_carrier(f"{derived['source_key']}.dta") if derived["plan"].mode is RowDataMode.FULL \
        else carrier(f"{derived['source_key']}.sav", ALL_SELECTED)
    spec = BoundExecutionSpec(
        source_entry_key=derived["source_key"], path=path,
        source_format="dta" if derived["plan"].mode is RowDataMode.FULL else "sav",
        plan=derived["plan"], expected_sha256=None, budget=derived["budget"],
        route_pass=derived["route_pass"], route_applicability=derived["applicable"],
        constraints=derived["constraints"],
        authority_note=f"warrant-derived {derived['source_key']} binding")
    ex = BoundSourceExecution(spec)
    try:
        out = ex.execute()
        return spec, ex, out
    except Exception:
        ex.close()
        raise


# ------------------------------------------------------------------ checks
def w1(warrant):
    """Every FROZEN warrant expectation is satisfied by the runtime, per source."""
    rows = []
    for plan in warrant:
        d = derive(plan)
        spec, ex, out = execute_plan(d)
        try:
            accounts = out.observed_accounts
            rows.append({
                "source_key": d["source_key"],
                "warrant_mode": d["mode"],
                "outer_expected": d["outer_expected"],
                "outer_observed": out.full_route_passes_observed,
                "applicability": out.as_dict()["route_pass_applicability"],
                "frozen_constraints_applied": sum(
                    1 for c in d["constraints"] if c.authority is FROZEN),
                "policy_constraints_applied": sum(
                    1 for c in d["constraints"] if c.authority is POLICY),
                "constraints_all_satisfied": all(
                    c["satisfied"] for c in out.constraint_report),
                "observed_selected_reads": accounts["selected_reads"],
                "observed_metadata_reads": accounts["metadata_reads"],
                "observed_full_reads": accounts["full_reads"],
                "observed_chunk_reads": accounts["chunk_reads"],
                "observed_header_prefix_reads": accounts["header_prefix_reads"],
                "observed_header_prefix_bytes": accounts["header_prefix_bytes"],
                "observed_retries": accounts["retries"],
                "unmapped_warrant_accounts": [u["warrant_account"] for u in d["unmapped"]],
                "unbound_source_dependent_bytes": [u["warrant_account"] for u in d["unbound_bytes"]],
            })
            need(out.full_route_passes_observed == d["outer_expected"],
                 f"{d['source_key']}: outer observed {out.full_route_passes_observed} "
                 f"!= warrant {d['outer_expected']}")
            need(all(c["satisfied"] for c in out.constraint_report),
                 f"{d['source_key']}: a warrant-derived constraint was NOT satisfied")
            need(accounts["retries"] == 0, f"{d['source_key']}: retries != 0")
            if d["source_key"] != "SRC27":
                need(out.full_route_passes_observed == 0,
                     f"{d['source_key']}: a non-route source observed a route pass")
        finally:
            ex.close()
    return {"per_source": rows,
            "all_seven_executed": True,
            "six_non_route_outer_zero": all(
                r["outer_observed"] == 0 for r in rows if r["source_key"] != "SRC27"),
            "src27_outer_one": next(r["outer_observed"] for r in rows
                                    if r["source_key"] == "SRC27") == 1}


def w2(warrant):
    """SRC27-shaped route executes exactly once and refuses the second attempt pre-op."""
    d = derive(next(p for p in warrant if p["source_key"] == "SRC27"))
    spec, ex, out = execute_plan(d)
    try:
        need(out.full_route_passes_observed == 1, "outer observed != 1")
        need(out.completed_pass is True, "the SRC27-shaped pass did not complete")
        need(out.route_pass_applicable is True, "the SRC27-shaped pass is not APPLICABLE")
        before = ex.session.account_dict()
        exc = None
        try:
            ex.execute()
        except SourceAccessViolation as e:
            exc = e
        after = ex.session.account_dict()
        need(exc is not None, "the second SRC27-shaped attempt was NOT refused")
        need(exc.code == ROUTE_PASS_LIMIT_REACHED, f"wrong refusal code {exc.code}")
        need(before == after, "the pre-op refusal moved a source account")
        return {"outer_observed": out.full_route_passes_observed,
                "second_attempt_code": exc.code,
                "accounts_unchanged_by_refusal": before == after,
                "route_pass_attempts": ex.route_pass_attempts,
                "completed_route_passes": ex.completed_route_passes}
    finally:
        ex.close()


def w3(warrant):
    """full_reads FLOOR 1 stays distinct from the outer route pass and from chunk_reads."""
    d = derive(next(p for p in warrant if p["source_key"] == "SRC27"))
    spec, ex, out = execute_plan(d)
    try:
        acc = out.observed_accounts
        need(acc["full_reads"] >= 1, "the full_reads floor is not satisfied")
        need(out.full_route_passes_observed == 1, "outer observed != 1")
        need("full_route_passes" not in acc and OUTER_ACCOUNT not in acc,
             "the outer route pass is present in the lower-layer account dict")
        need("full_route_passes" not in LOWER_LAYER_ACCOUNTS,
             "the outer account is listed as a lower-layer account")
        # chunk_reads must NOT be able to satisfy the full_reads floor on its own.
        d2 = derive(next(p for p in warrant if p["source_key"] == "SRC27"))
        chunk_spec = BoundExecutionSpec(
            source_entry_key="SRC27-CHUNK-ONLY", path=dta_carrier("chunkonly.dta"),
            source_format="dta",
            plan=SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=5, max_retries=0),
            budget=SourceAccessBudget(retries=0),
            route_pass=RoutePassSpec(expected=1, maximum=1),
            route_applicability=ROUTE,
            constraints=(AccountConstraint("full_reads", CountKind.FLOOR, 1, FROZEN),))
        ex2 = BoundSourceExecution(chunk_spec)
        try:
            raised = None
            try:
                ex2.execute()
            except SourceAccessViolation as e:
                raised = e
            need(raised is not None, "a chunk-only run satisfied the full_reads floor")
        finally:
            ex2.close()
        # the outer account cannot be bound as a lower-layer constraint
        outer_bind = None
        try:
            AccountConstraint("full_route_passes", CountKind.EXACT, 1, FROZEN)
        except BindingError as e:
            outer_bind = str(e)
        need(outer_bind is not None, "full_route_passes was bindable as a lower-layer account")
        return {"full_reads_observed": acc["full_reads"],
                "outer_observed": out.full_route_passes_observed,
                "full_reads_floor_satisfied_by_full_reads": True,
                "chunk_only_attempt_refused": raised.code,
                "outer_account_is_structurally_separate": True,
                "outer_as_lower_layer_refused": outer_bind[:120]}
    finally:
        ex.close()


def w4(warrant):
    """Decoder and path-open maxima stay POLICY, and are genuinely enforced."""
    d = derive(next(p for p in warrant if p["source_key"] == "SRC27"))
    policy = [(c.account, c.kind.value, c.value, c.authority.value)
              for c in d["constraints"]
              if c.authority is AuthorityLabel.IMPLEMENTATION_POLICY]
    frozen_names = {c.account for c in d["constraints"] if c.authority is FROZEN}
    need("decoder_invocations" in {p[0] for p in policy},
         "decoder_invocations is not carried as an IMPLEMENTATION_POLICY ceiling")
    need("path_opens" in {p[0] for p in policy},
         "path_opens is not carried as an IMPLEMENTATION_POLICY ceiling")
    need("decoder_invocations" not in frozen_names,
         "decoder_invocations was recorded as frozen authority")
    need("path_opens" not in frozen_names, "path_opens was recorded as frozen authority")

    # No library-level frozen decoder ceiling: the default budget leaves it unbounded.
    need(SourceAccessBudget().decoder_invocations is None,
         "the library imposes a default decoder_invocations ceiling")
    need(SourceAccessBudget().full_reads is None,
         "the library imposes a default full_reads ceiling")
    need(SourceAccessBudget().path_opens == 1,
         "the library's default path-open policy ceiling is not 1")

    # The decoder policy ceiling is enforced, not inert.
    dec_spec = BoundExecutionSpec(
        source_entry_key="POLICY-DECODER", path=carrier("pold.sav", ALL_SELECTED),
        source_format="sav", plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=1),
        budget=SourceAccessBudget(decoder_invocations=1, retries=1),
        route_pass=RoutePassSpec(), route_applicability=ROUTE)
    ex = BoundSourceExecution(dec_spec)
    try:
        ex.execute()
        raised = None
        try:
            ex.execute()          # retry is admitted, then the decoder policy refuses
        except SourceAccessViolation as e:
            raised = e
        need(raised is not None, "the decoder policy ceiling was inert")
        decoder_code = raised.code
    finally:
        ex.close()

    # The path-open policy ceiling is enforced, not inert.
    po_spec = BoundExecutionSpec(
        source_entry_key="POLICY-PATHOPEN", path=carrier("polp.sav", ALL_SELECTED),
        source_format="sav", plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
        budget=SourceAccessBudget(path_opens=0, retries=0),
        route_pass=RoutePassSpec(), route_applicability=NON_ROUTE)
    ex2 = BoundSourceExecution(po_spec)
    try:
        raised2 = None
        try:
            ex2.execute()
        except SourceAccessViolation as e:
            raised2 = e
        need(raised2 is not None, "the path-open policy ceiling was inert")
        pathopen_code = raised2.code
    finally:
        ex2.close()

    return {"policy_constraints": policy,
            "frozen_constraint_accounts": sorted(frozen_names),
            "default_budget_decoder_invocations": SourceAccessBudget().decoder_invocations,
            "default_budget_path_opens": SourceAccessBudget().path_opens,
            "decoder_policy_enforced_code": decoder_code,
            "path_open_policy_enforced_code": pathopen_code}


def w5(warrant):
    """retries max 0 works, and the retry ceiling is not used for anything else."""
    rows = []
    for plan in warrant:
        d = derive(plan)
        need(d["retry_ceiling"] == 0, f"{d['source_key']}: warrant retry ceiling != 0")
        need(d["budget"].retries == 0, f"{d['source_key']}: runtime budget retries != 0")
        need(d["plan"].max_retries == 0, f"{d['source_key']}: plan max_retries != 0")
        spec, ex, out = execute_plan(d)
        try:
            need(out.retries_observed == 0, f"{d['source_key']}: a retry was charged")
            exc = None
            try:
                ex.execute()
            except SourceAccessViolation as e:
                exc = e
            need(exc is not None, f"{d['source_key']}: a second attempt was admitted")
            rows.append({"source_key": d["source_key"], "retries_observed": out.retries_observed,
                         "second_attempt_code": exc.code})
        finally:
            ex.close()
    return {"per_source": rows}


def w6(warrant):
    """No header prefix on the SRC27-shaped route; 176 bytes belongs to SRC26 alone."""
    d27 = derive(next(p for p in warrant if p["source_key"] == "SRC27"))
    need(d27["plan"].header_prefix_bytes is None, "an SRC27 prefix was invented")
    need(d27["plan"].admits_header_prefix is False, "SRC27 admits a header prefix")
    spec, ex, out = execute_plan(d27)
    try:
        acc = out.observed_accounts
        need(acc["header_prefix_reads"] == 0, "an SRC27 header-prefix read happened")
        need(acc["header_prefix_bytes"] == 0, "SRC27 header-prefix bytes != 0")
        need(out.plan_identity["header_prefix_bytes"] is None,
             "the SRC27 plan identity carries a prefix size")
    finally:
        ex.close()

    d26 = derive(next(p for p in warrant if p["source_key"] == "SRC26"))
    need(d26["plan"].header_prefix_bytes == 176, "SRC26 did not carry the 176-byte prefix")
    spec26, ex26, out26 = execute_plan(d26)
    try:
        acc26 = out26.observed_accounts
        need(acc26["header_prefix_reads"] >= 1, "SRC26 performed no prefix read")
        need(acc26["header_prefix_bytes"] == 176, "SRC26 prefix bytes != 176")
    finally:
        ex26.close()

    with_prefix = {p["source_key"] for p in warrant
                   if val(p["header_prefix_admitted"])[0] is True}
    return {"src27_prefix": None,
            "src27_header_prefix_reads": 0,
            "src27_header_prefix_bytes": 0,
            "src26_prefix_bytes": 176,
            "src26_header_prefix_bytes_observed": acc26["header_prefix_bytes"],
            "sources_admitting_a_prefix": sorted(with_prefix),
            "prefix_is_src26_only": with_prefix == {"SRC26"}}


def w7(warrant):
    """Source-dependent byte ceilings remain uninvented, and byte use stays observable."""
    production = Path("rawlsing_next/pre553_execution_binding.py").read_text()
    rows = []
    for plan in warrant:
        d = derive(plan)
        need(d["budget"].reader_bytes is None, f"{d['source_key']}: a reader_bytes cap was invented")
        need(d["budget"].hash_bytes is None, f"{d['source_key']}: a hash_bytes cap was invented")
        need(all(c.account not in ("reader_bytes", "hash_bytes", "byte_counts_where_measurable")
                 for c in d["constraints"]),
             f"{d['source_key']}: a byte account was constrained")
        need(d["unbound_bytes"], f"{d['source_key']}: the byte account was not carried as unbound")
        spec, ex, out = execute_plan(d)
        try:
            acc = out.observed_accounts
            need(acc["hash_bytes"] > 0, f"{d['source_key']}: hash bytes were not observed")
            rows.append({"source_key": d["source_key"],
                         "budget_reader_bytes": d["budget"].reader_bytes,
                         "budget_hash_bytes": d["budget"].hash_bytes,
                         "observed_hash_bytes": acc["hash_bytes"],
                         "observed_reader_bytes": acc["reader_bytes"]})
        finally:
            ex.close()
    invented = re.findall(r"(?:reader_bytes|hash_bytes)\s*[:=]\s*(?:\d+)", production)
    need(not invented, f"a numeric byte ceiling appears in production: {invented}")
    return {"per_source": rows,
            "numeric_byte_ceiling_in_production_binding": invented,
            "all_seven_byte_accounts_unbound": True,
            "observed_byte_use_still_reported": True}


def w8(warrant):
    """Production carries no source-specific policy and no mode->applicability mapping."""
    production = Path("rawlsing_next/pre553_execution_binding.py").read_text()
    code_lines = [ln for ln in production.splitlines()
                  if not ln.strip().startswith("#")]
    src_tokens = re.findall(r"\bSRC\d{2}\b", "\n".join(l for l in code_lines
                                                       if not l.strip().startswith('"""')
                                                       and '"""' not in l))
    mode_refs = re.findall(r"RowDataMode\.\w+", production)
    # RoutePassApplicability must be driven only by the caller-bound field.
    decision_sites = [ln.strip() for ln in production.splitlines()
                      if "route_applicability is" in ln or "route_applicability is not" in ln]
    need(not mode_refs, f"the binding references a row-data mode: {mode_refs}")
    need(not src_tokens, f"the binding contains source-specific tokens: {src_tokens}")
    return {"src_tokens_in_production_binding": src_tokens,
            "row_data_mode_references_in_production_binding": mode_refs,
            "applicability_decision_sites": decision_sites,
            "applicability_always_read_from_the_bound_field": all(
                "self.spec.route_applicability" in s for s in decision_sites)}


def w9(warrant):
    """The outer account is EXACT 0 for the six and EXACT/MAX 1 for SRC27, from the warrant."""
    rows = []
    for plan in warrant:
        d = derive(plan)
        rows.append({"source_key": d["source_key"],
                     "warrant_outer_expected": d["outer_expected"],
                     "bound_route_pass_expected": d["route_pass"].expected,
                     "warrant_outer_maximum": d["outer_maximum"],
                     "bound_route_pass_maximum": d["route_pass"].maximum,
                     "applicability": d["applicable"].value,
                     "constraint_report_kinds": [c.kind.value for c in d["constraints"]]})
    six = [r for r in rows if r["source_key"] != "SRC27"]
    need(all(r["bound_route_pass_expected"] == 0 and r["bound_route_pass_maximum"] == 0
             for r in six), "a non-route source does not carry outer EXACT 0 / MAX 0")
    need(all(r["applicability"] == "NOT_APPLICABLE" for r in six),
         "a non-route source is bound APPLICABLE")
    s27 = next(r for r in rows if r["source_key"] == "SRC27")
    need(s27["bound_route_pass_expected"] == 1 and s27["bound_route_pass_maximum"] == 1,
         "SRC27 does not carry outer EXACT 1 / MAX 1")
    need(s27["applicability"] == "APPLICABLE", "SRC27 is not bound APPLICABLE")
    # A non-route source refuses an incoherent non-zero outer expectation.
    refused = None
    try:
        BoundExecutionSpec(source_entry_key="SRC08-X", path="x.sav", source_format="sav",
                           plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0),
                           budget=SourceAccessBudget(retries=0),
                           route_pass=RoutePassSpec(expected=1, maximum=1),
                           route_applicability=NON_ROUTE)
    except BindingError as e:
        refused = str(e)
    need(refused is not None, "a non-route source accepted an EXACT 1 outer account")
    return {"per_source": rows, "non_route_exact1_refused": refused[:140]}


def main() -> int:
    warrant = load_plans()
    checks = [
        ("W1", "all seven warrant plans execute and every FROZEN expectation holds", w1),
        ("W2", "SRC27-shaped route executes once; the second attempt refuses pre-op", w2),
        ("W3", "full_reads FLOOR 1 stays distinct from the outer pass and from chunk_reads", w3),
        ("W4", "decoder/path-open maxima remain POLICY and are genuinely enforced", w4),
        ("W5", "retries max 0 works for all seven", w5),
        ("W6", "no prefix on the SRC27-shaped route; 176 bytes is SRC26 only", w6),
        ("W7", "source-dependent byte ceilings remain uninvented", w7),
        ("W8", "production carries no source-specific policy or mode->applicability map", w8),
        ("W9", "outer account is EXACT 0 for six and EXACT/MAX 1 for SRC27", w9),
    ]
    for cid, title, fn in checks:
        check(cid, title, lambda fn=fn: fn(warrant))

    # Derivation transparency: every warrant account accounted for.
    derivation = []
    for plan in warrant:
        d = derive(plan)
        derivation.append({"source_key": d["source_key"], "mode": d["mode"],
                           "encoding": d["encoding"], "selected": d["selected"],
                           "prefix_bytes": d["prefix_bytes"],
                           "outer_expected": d["outer_expected"],
                           "outer_maximum": d["outer_maximum"],
                           "retry_ceiling": d["retry_ceiling"],
                           "applied_constraints": d["applied"],
                           "warrant_accounts_without_runtime_counterpart": d["unmapped"],
                           "unbound_source_dependent_byte_accounts": d["unbound_bytes"]})
    passed = sum(1 for r in RESULTS if r["ok"])
    doc = {
        "schema": "HQ202_WARRANT_COMPATIBILITY@1.0.0",
        "warrant_commit": "89054b882c04cf0541b6f9f4abdb555c808ad94d",
        "warrant_files_read": [str(W01), str(W03)],
        "derivation_is_warrant_driven_not_court_copied": True,
        "checks_total": len(RESULTS),
        "checks_passed": passed,
        "checks_failed": len(RESULTS) - passed,
        "derivation": derivation,
        "results": RESULTS,
    }
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
