"""HQ196-R1 — budget type vocabulary and invariant predicates.

Kept separate from the generator so the vocabulary is stated once and the
invariants can be asserted against the emitted instrument.
"""

from __future__ import annotations

BUDGET_TYPES_DOC = {
    "EXACT": {
        "meaning": "Authority froze a specific count. The observed count must equal it.",
        "example": "SRC02 selected_column_reads = 1",
    },
    "MAX": {
        "meaning": "Authority froze a ceiling. The observed count may be lower but never higher.",
        "example": "SRC27 governed_full_route_passes max = 1",
    },
    "ZERO": {
        "meaning": "Hard zero. A single non-zero observation is a STOP condition, not a reportable variance.",
        "example": "retries = 0 for all seven sources",
    },
    "FLOOR": {
        "meaning": "Authority froze a minimum that must be reached. It is NOT a ceiling and MUST NOT be promoted to one.",
        "example": "SRC27 metadata_reads floor = 1, from the 'at minimum' wording of the hardened note",
        "promotion_prohibited": True,
    },
    "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE": {
        "meaning": "Authority named the account as mandatory but supplied no number. The value awaits technical "
                   "acceptance. This is a TYPED BUDGET STATE, not a null, and it waives nothing.",
        "non_waiving": True,
        "example": "path_level_opens on the six non-SRC27 sources",
    },
}

RETURN_METRIC_NULL_LAW = {
    "permitted": True,
    "requires_typed_reason": True,
    "citation": "07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.O1_C08_failure_law.unreached_stage_or_metric_reporting",
    "never_a_fabricated_zero": True,
    "never_a_fabricated_pass": True,
}

PRE_LAUNCH_BUDGET_NULL_LAW = {
    "permitted": False,
    "unsupplied_must_be_typed_as": "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
    "absence_prohibited": True,
    "rationale": "A null or absent pre-launch budget would silently waive a mandatory launch prerequisite.",
}

MANDATORY_SEPARATE_ACCOUNTS = [
    "source-path existence/access checks",
    "file hash passes (full SHA-256 over the file)",
    "path-level opens",
    "metadata reads",
    "header-prefix reads",
    "decoder invocations",
    "selected-column reads",
    "full reads",
    "byte counts where measurable",
    "retries",
]


def account_by_name(acct_block: dict, name: str) -> dict | None:
    for a in acct_block["accounts"]:
        if a["account_name"] == name:
            return a
    return None


def check_invariants(successor: dict) -> list[dict]:
    """Assert the structural laws. Returns a list of {id, ok, detail}."""
    results: list[dict] = []

    def add(i: str, ok: bool, detail: str) -> None:
        results.append({"id": i, "ok": bool(ok), "detail": detail})

    # ---- instrument status ----
    status_ok = (
        successor["signed"] is False
        and successor["issued"] is False
        and successor["authorizes_access"] is False
        and successor["execution_authorized"] is False
    )
    add("INV-STATUS", status_ok, "signed/issued/authorizes_access/execution_authorized are all false")

    appr = successor["approvals"]
    appr_ok = all(appr[k]["status"] == "UNSET" and appr[k]["name"] is None for k in appr)
    add("INV-APPROVALS-UNSET", appr_ok, "both approvals UNSET with null name")

    # ---- seven sources, SRC35 excluded ----
    keys = [s["source_key"] for s in successor["sources"]]
    add("INV-SEVEN-SOURCES", keys == ["SRC02", "SRC06", "SRC08", "SRC12", "SRC14", "SRC26", "SRC27"],
        f"per_source keys = {keys}")
    add("INV-SRC35-EXCLUDED",
        all(s["source_key"] != "SRC35" for s in successor["sources"])
        and successor["excluded_from_fresh_warrant"][0]["fresh_reads"] == 0,
        "SRC35 absent from the seven and carries fresh_reads = 0")

    # ---- DQ-01: accounting block restored everywhere ----
    restored = all("source_access_accounting" in s and s["source_access_accounting"]["account_count"] > 0
                   for s in successor["sources"])
    add("INV-DQ01-RESTORED", restored, "every one of the seven carries a populated source_access_accounting block")

    # ---- every account: budget never null, basis complete, observed typed ----
    # The typed-null law in force: a null budget VALUE is lawful ONLY under the
    # UNBOUND_PENDING_TECHNICAL_ACCEPTANCE type. EXACT/MAX/ZERO/FLOOR must carry a
    # value, and the budget object itself must always be present and typed.
    bad_budget: list[str] = []
    bad_basis: list[str] = []
    bad_observed: list[str] = []
    bad_mech: list[str] = []
    n_accounts = 0
    n_unbound = 0
    for s in successor["sources"]:
        for a in s["source_access_accounting"]["accounts"]:
            n_accounts += 1
            nm = f"{s['source_key']}/{a['account_name']}"
            b = a["expected_pre_launch_budget"]
            has_val = b["budget_value"] is not None or b["budget_expression"] is not None
            if b["budget_type"] == "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE":
                n_unbound += 1
                if has_val:
                    bad_budget.append(nm + ":unbound_must_not_carry_a_value")
            else:
                if not has_val:
                    bad_budget.append(nm + ":" + b["budget_type"] + "_requires_a_value")
            if b["budget_type"] not in BUDGET_TYPES_DOC:
                bad_budget.append(nm + ":unknown_type")
            if b.get("may_be_null") is not False:
                bad_budget.append(nm + ":budget_object_must_declare_may_be_null_false")
            mb = a["measurement_basis"]
            for f in ("what_measured", "layer", "mechanism", "point_in_run"):
                if not mb.get(f):
                    bad_basis.append(f"{nm}:{f}")
            o = a["runtime_observed_exact_count"]
            if o["value"] is not None or not o.get("typed_reason"):
                bad_observed.append(nm)
            if not a.get("stop_condition_if_exceeded"):
                bad_mech.append(nm)
            if not a.get("provenance"):
                bad_mech.append(nm + ":provenance")

    add("INV-NO-NULL-PRELAUNCH-BUDGET", not bad_budget,
        f"{n_accounts} accounts checked ({n_unbound} typed UNBOUND); violations: {bad_budget or 'none'}")
    add("INV-BASIS-COMPLETE", not bad_basis,
        f"measurement basis fields missing in: {bad_basis or 'none'}")
    add("INV-OBSERVED-TYPED-NULL", not bad_observed,
        f"return metric null without typed reason in: {bad_observed or 'none'}")
    add("INV-STOP-AND-PROVENANCE", not bad_mech,
        f"missing stop condition or provenance in: {bad_mech or 'none'}")

    # ---- retries zero everywhere ----
    bad_retry = []
    for s in successor["sources"]:
        a = account_by_name(s["source_access_accounting"], "retries")
        if not a or a["expected_pre_launch_budget"]["budget_type"] != "ZERO" \
                or a["expected_pre_launch_budget"]["budget_value"] != 0:
            bad_retry.append(s["source_key"])
    add("INV-RETRIES-ZERO", not bad_retry, f"retries not ZERO/0 in: {bad_retry or 'none'}")

    # ---- SRC02/06/14 selected = 1, full = 0 ----
    bad_sel = []
    for k in ("SRC02", "SRC06", "SRC14"):
        s = next(x for x in successor["sources"] if x["source_key"] == k)
        sel = account_by_name(s["source_access_accounting"], "selected_column_reads")
        full = account_by_name(s["source_access_accounting"], "full_reads")
        if not sel or sel["expected_pre_launch_budget"]["budget_value"] != 1 \
                or sel["expected_pre_launch_budget"]["budget_type"] != "EXACT":
            bad_sel.append(k + ":selected")
        if not full or full["expected_pre_launch_budget"]["budget_value"] != 0:
            bad_sel.append(k + ":full")
    add("INV-SEL-1-FULL-0", not bad_sel, f"SRC02/06/14 selected_reads=1 EXACT and full_reads=0; violations: {bad_sel or 'none'}")

    # ---- SRC08/12 zeros ----
    bad_meta = []
    for k in ("SRC08", "SRC12"):
        s = next(x for x in successor["sources"] if x["source_key"] == k)
        b = s["source_access_accounting"]
        m = account_by_name(b, "metadata_reads")
        rd = account_by_name(b, "row_data_reads")
        sc = account_by_name(b, "selected_columns")
        sel = account_by_name(b, "selected_column_reads")
        if not m or m["expected_pre_launch_budget"]["budget_value"] != 1:
            bad_meta.append(k + ":metadata")
        if not rd or rd["expected_pre_launch_budget"]["budget_value"] != 0:
            bad_meta.append(k + ":row_data_reads")
        if not sc or sc["expected_pre_launch_budget"]["budget_value"] != 0:
            bad_meta.append(k + ":selected_columns")
        if not sel or sel["expected_pre_launch_budget"]["budget_value"] != 0:
            bad_meta.append(k + ":selected_column_reads")
    add("INV-SRC08-12-METADATA-ZEROS", not bad_meta, f"violations: {bad_meta or 'none'}")

    # ---- SRC26: 176 at its own account; 174/332 separate; not equality-required ----
    s26 = next(x for x in successor["sources"] if x["source_key"] == "SRC26")
    b26 = s26["source_access_accounting"]
    hp = account_by_name(b26, "header_prefix_bytes")
    rn = account_by_name(b26, "raw_nominal_case_size")
    dd = account_by_name(b26, "decoded_dictionary_data_width")
    add("INV-SRC26-176", hp is not None and hp["expected_pre_launch_budget"]["budget_value"] == 176,
        "header_prefix_bytes = 176 at its declared account")
    add("INV-SRC26-GEOMETRY-SEPARATE",
        rn is not None and rn["expected_pre_launch_budget"]["budget_value"] == 174
        and dd is not None and dd["expected_pre_launch_budget"]["budget_value"] == 332
        and rn.get("equality_required") is False and dd.get("equality_required") is False,
        "174 and 332 preserved as separate accounts, equality_required = false")

    # SRC26 header-prefix READ count is not authority-supplied; the byte count is.
    hpr = account_by_name(b26, "header_prefix_reads")
    add("INV-SRC26-HEADER-READ-NOT-INVENTED",
        hpr is not None and hpr["expected_pre_launch_budget"]["budget_type"] == "FLOOR"
        and hpr["expected_pre_launch_budget"]["budget_value"] == 1
        and hpr.get("reviewer_confirmation_required") is True,
        "SRC26 header_prefix_reads bound as FLOOR 1 and flagged; only the BYTE count 176 is authority-supplied")

    # ---- SRC27: route pass EXACT 1; floors not promoted ----
    s27 = next(x for x in successor["sources"] if x["source_key"] == "SRC27")
    b27 = s27["source_access_accounting"]
    rp = account_by_name(b27, "governed_full_route_passes")
    add("INV-SRC27-ROUTE-PASS-EXACT-1",
        rp is not None and rp["expected_pre_launch_budget"]["budget_type"] == "EXACT"
        and rp["expected_pre_launch_budget"]["budget_value"] == 1,
        "governed_full_route_passes = EXACT 1 (max 1 supplied by authority)")
    floor_names = ["source_path_existence_access_checks", "full_file_sha256_passes", "metadata_reads", "full_reads"]
    bad_floor = [n for n in floor_names
                 if (account_by_name(b27, n) or {}).get("expected_pre_launch_budget", {}).get("budget_type") != "FLOOR"]
    add("INV-SRC27-FLOORS-NOT-PROMOTED", not bad_floor,
        f"SRC27 'at minimum' accounts bound as FLOOR and not promoted: {bad_floor or 'none'}")
    s27_sel = account_by_name(b27, "selected_column_reads")
    add("INV-SRC27-NO-INVENTED-SELECTED",
        s27_sel is not None
        and s27_sel["expected_pre_launch_budget"]["budget_type"] == "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE"
        and s27_sel["expected_pre_launch_budget"]["budget_value"] is None
        and s27_sel["expected_pre_launch_budget"]["budget_expression"] is None,
        "SRC27 selected reads typed UNBOUND, not invented, not null")
    s27_po = account_by_name(b27, "path_level_opens")
    add("INV-SRC27-PATH-OPENS-UNBOUND",
        s27_po is not None
        and s27_po["expected_pre_launch_budget"]["budget_type"] == "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
        "SRC27 path opens unbound; authority's 'multiple' recorded, not numerified")

    # ---- nothing invented: no numeric budget on the forbidden accounts ----
    forbidden = ["path_level_opens", "decoder_invocations", "byte_counts_where_measurable"]
    bad_invent = []
    for s in successor["sources"]:
        for a in s["source_access_accounting"]["accounts"]:
            if a["account_name"] in forbidden:
                b = a["expected_pre_launch_budget"]
                if b["budget_value"] is not None:
                    bad_invent.append(f"{s['source_key']}/{a['account_name']}")
    add("INV-NO-INVENTED-BUDGETS", not bad_invent,
        f"numeric budgets asserted on forbidden accounts in: {bad_invent or 'none'}")

    # ---- typed-null distinction present ----
    tn = successor["typed_null_law"]["machine_readable_rule"]
    add("INV-TYPED-NULL-LAW",
        tn["pre_launch_budget_null_permitted"] is False
        and tn["return_metric_null_requires_typed_reason"] is True
        and tn["pre_launch_budget_unsupplied_representation"] == "UNBOUND_PENDING_TECHNICAL_ACCEPTANCE",
        "typed-null distinction is machine-readable")

    # ---- locators unfilled ----
    add("INV-LOCATORS-UNFILLED",
        all(s["locator_filled"] is False and s["access_locator"].startswith("<REQUIRED_FILL_IN_SLOT")
            for s in successor["sources"]),
        "all seven locator slots remain unfilled placeholders")

    # ---- two stages never merged ----
    ok_stage = all(
        "expected_pre_launch_budget" in a and "runtime_observed_exact_count" in a
        and a["expected_pre_launch_budget"] is not a["runtime_observed_exact_count"]
        for s in successor["sources"] for a in s["source_access_accounting"]["accounts"]
    )
    add("INV-STAGES-SEPARATE", ok_stage,
        "every account holds expected budget and observed count in distinct objects")

    return results
