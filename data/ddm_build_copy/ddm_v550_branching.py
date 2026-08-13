#!/usr/bin/env python3
"""Branching and determinicity helpers for V550."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
import pandas as pd

from data.ddm_build_copy.ddm_v550_metrics import (
    conditional_entropy,
    cramers_v,
    distribution_entropy,
    dominant_response,
    normalized_mutual_information,
    uplift_vs_baseline,
)
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, support_threshold_from_total


INDICATOR_FIELDS = [
    "sex",
    "age_group",
    "education_level",
    "income_level",
    "religion_label",
    "urban_rural",
    "region",
    "ethnicity",
    "language",
    "employment",
    "marital",
    "household_size",
]

SECONDARY_INDICATOR_SUMMARY_COLUMNS = [
    "run_id",
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
    "survey_year",
    "var_code",
    "var_name",
    "question_id",
    "question_text",
    "driver_id",
    "driver_facet_id",
    "relation_axis_id",
    "target_entity_id",
    "mapping_status",
    "legacy_final_driver_id",
    "legacy_driver_leak_flag",
    "question_type",
    "handling_rule",
    "recommended_computation",
    "source_structure_classification",
    "response_direction",
    "response_intensity",
    "polarity",
    "ordinal_rank",
    "scale_min",
    "scale_max",
    "scale_direction",
    "directionality_status",
    "response_family",
    "response_semantics_status",
    "response_semantics_source",
    "response_semantics_contract_hash",
    "has_response_option_map",
    "response_option_confidence_min",
    "response_option_confidence_max",
    "n_response_rows",
    "n_respondents",
    "n_countries",
    "weight_status",
    "readiness_status",
    "dominant_response_value",
    "dominant_response_pct",
    "created_at",
    "shard_id",
    "source_structure_fields_joined",
    "source_structure_basis",
    "source_structure_confidence",
    "source_structure_review_required",
    "source_structure_source",
    "source_structure_join_key",
    "source_structure_join_confidence",
    "semantic_role",
    "v551_evidence_role",
    "review_required",
    "disallowed_reason",
    "manual_override_used",
    "manual_override_basis",
    "manual_override_reason",
    "itinerary_review_priority",
    "itinerary_manual_designation_required",
    "itinerary_primary_docs",
    "itinerary_secondary_docs",
    "itinerary_review_notes",
    "authority_table_used",
    "authority_table_basis",
    "authority_semantic_lane",
    "authority_semantic_role",
    "authority_evidence_lane",
    "authority_designation_confidence",
    "authority_review_required",
    "indicator_name",
    "indicator_value",
    "secondary_indicator_name",
    "secondary_gain",
    "indicator_type",
    "n_unweighted",
    "n_weighted",
    "baseline_entropy",
    "conditional_entropy",
    "entropy_reduction",
    "mutual_information",
    "normalized_mutual_information",
    "cramers_v",
    "uplift_vs_baseline",
    "dominant_response_pct_unweighted",
    "dominant_response_pct_weighted",
    "confidence_tier",
]


def prepare_question_frame(question_df: pd.DataFrame) -> pd.DataFrame:
    df = question_df.copy()
    if "response_value_normalized" not in df.columns:
        if "value_text" in df.columns:
            df["response_value_normalized"] = df["value_text"].fillna("").astype(str)
        else:
            df["response_value_normalized"] = df["value_raw"].fillna("").astype(str)
    df["response_value_normalized"] = df["response_value_normalized"].fillna("").astype(str)
    df["response_label"] = df.get("response_label", df["response_value_normalized"])
    return df


def indicator_summary_rows(df: pd.DataFrame, question_meta: dict[str, Any], weights: pd.Series | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    y = df["response_value_normalized"].fillna("").astype(str)
    baseline_h = distribution_entropy(y, weights)
    baseline_dom, baseline_dom_pct = dominant_response(y, weights)
    for indicator in INDICATOR_FIELDS:
        if indicator not in df.columns:
            continue
        x = df[indicator].fillna("").astype(str)
        mask = x.ne("")
        if mask.sum() == 0:
            continue
        x = x[mask]
        yx = y[mask]
        wx = weights[mask] if weights is not None else None
        cond_h = conditional_entropy(yx, x, wx)
        mi = max(0.0, baseline_h - cond_h)
        norm_mi = normalized_mutual_information(x, yx)
        c_v = cramers_v(x, yx)
        if wx is not None:
            weights_df = pd.DataFrame({"x": x, "w": wx, "y": yx})
            grouped = weights_df.groupby("x")
            dominant_value = ""
            dominant_pct = 0.0
            for value, sub in grouped:
                label, pct = dominant_response(sub["y"], sub["w"])
                if pct > dominant_pct:
                    dominant_value = str(value)
                    dominant_pct = pct
                    dominant_label = label
        else:
            label, dominant_pct = dominant_response(yx)
            dominant_value = x.value_counts().index[0] if not x.empty else ""
            dominant_label = label
        rows.append(
            {
                **question_meta,
                "indicator_name": indicator,
                "indicator_value": dominant_value,
                "indicator_type": "demographic_position" if indicator != "region" else "structural_position",
                "n_unweighted": int(mask.sum()),
                "n_weighted": float(wx.fillna(0).sum()) if wx is not None else float(mask.sum()),
                "baseline_entropy": float(baseline_h),
                "conditional_entropy": float(cond_h),
                "entropy_reduction": float(max(0.0, baseline_h - cond_h)),
                "mutual_information": float(mi),
                "normalized_mutual_information": float(norm_mi),
                "cramers_v": float(c_v),
                "uplift_vs_baseline": float(dominant_pct - baseline_dom_pct),
                "dominant_response_value": baseline_dom,
                "dominant_response_label": baseline_dom,
                "dominant_response_pct_unweighted": float(baseline_dom_pct),
                "dominant_response_pct_weighted": float(baseline_dom_pct),
                "confidence_tier": "usable" if mask.sum() >= 50 else "weak",
                "weight_status": "weighted" if weights is not None else "unweighted_only",
            }
        )
    return rows


def secondary_indicator_summary_rows(df: pd.DataFrame, question_meta: dict[str, Any], weights: pd.Series | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    y = df["response_value_normalized"].fillna("").astype(str)
    baseline_h = distribution_entropy(y, weights)
    baseline_dom, baseline_dom_pct = dominant_response(y, weights)

    candidate_scores: list[dict[str, Any]] = []
    for indicator in INDICATOR_FIELDS:
        if indicator not in df.columns:
            continue
        x = df[indicator].fillna("").astype(str)
        mask = x.ne("")
        if mask.sum() == 0:
            continue
        x_mask = x[mask]
        y_mask = y[mask]
        wx = weights[mask] if weights is not None else None
        cond_h = conditional_entropy(y_mask, x_mask, wx)
        mi = max(0.0, baseline_h - cond_h)
        norm_mi = normalized_mutual_information(x_mask, y_mask)
        c_v = cramers_v(x_mask, y_mask)
        if wx is not None:
            weights_df = pd.DataFrame({"x": x_mask, "w": wx, "y": y_mask})
            grouped = weights_df.groupby("x")
            dominant_value = ""
            dominant_pct = 0.0
            for value, sub in grouped:
                label, pct = dominant_response(sub["y"], sub["w"])
                if pct > dominant_pct:
                    dominant_value = str(value)
                    dominant_pct = pct
                    dominant_label = label
        else:
            dominant_label, dominant_pct = dominant_response(y_mask)
            dominant_value = x_mask.value_counts().index[0] if not x_mask.empty else ""
        candidate_scores.append(
            {
                "indicator_name": indicator,
                "indicator_value": dominant_value,
                "indicator_type": "demographic_position" if indicator != "region" else "structural_position",
                "indicator_mask": mask,
                "indicator_values": x,
                "indicator_values_masked": x_mask,
                "response_values_masked": y_mask,
                "weights_masked": wx,
                "baseline_entropy": float(baseline_h),
                "conditional_entropy": float(cond_h),
                "entropy_reduction": float(max(0.0, baseline_h - cond_h)),
                "mutual_information": float(mi),
                "normalized_mutual_information": float(norm_mi),
                "cramers_v": float(c_v),
                "uplift_vs_baseline": float(dominant_pct - baseline_dom_pct),
                "dominant_response_value": baseline_dom,
                "dominant_response_label": baseline_dom,
                "dominant_response_pct_unweighted": float(baseline_dom_pct),
                "dominant_response_pct_weighted": float(baseline_dom_pct),
                "confidence_tier": "usable" if mask.sum() >= 50 else "weak",
                "weight_status": "weighted" if weights is not None else "unweighted_only",
                "n_unweighted": int(mask.sum()),
                "n_weighted": float(wx.fillna(0).sum()) if wx is not None else float(mask.sum()),
            }
        )

    if not candidate_scores:
        return rows

    primary = max(candidate_scores, key=lambda row: (row["mutual_information"], row["cramers_v"], row["n_unweighted"]))
    primary_indicator = str(primary["indicator_name"])
    primary_x = primary["indicator_values_masked"]
    primary_y = primary["response_values_masked"]
    primary_w = primary["weights_masked"]
    primary_cond_h = float(primary["conditional_entropy"])

    for candidate in candidate_scores:
        secondary_indicator = str(candidate["indicator_name"])
        if secondary_indicator == primary_indicator:
            continue
        joint_mask = primary["indicator_mask"] & candidate["indicator_mask"]
        if int(joint_mask.sum()) < 50:
            continue
        x_primary = primary_x.loc[joint_mask]
        x_secondary = candidate["indicator_values"].loc[joint_mask]
        y_joint = y.loc[joint_mask]
        wx_joint = weights.loc[joint_mask] if weights is not None else None
        joint_key = x_primary.astype(str).str.cat(x_secondary.astype(str), sep="||")
        joint_cond_h = conditional_entropy(y_joint, joint_key, wx_joint)
        secondary_gain = max(0.0, primary_cond_h - joint_cond_h)
        if secondary_gain <= 0:
            continue
        if wx_joint is not None:
            weights_df = pd.DataFrame({"x": x_secondary, "w": wx_joint, "y": y_joint})
            grouped = weights_df.groupby("x")
            dominant_value = ""
            dominant_pct = 0.0
            for value, sub in grouped:
                label, pct = dominant_response(sub["y"], sub["w"])
                if pct > dominant_pct:
                    dominant_value = str(value)
                    dominant_pct = pct
        else:
            _, dominant_pct = dominant_response(y_joint)
            dominant_value = x_secondary.value_counts().index[0] if not x_secondary.empty else ""
        row = {
            **question_meta,
            "indicator_name": secondary_indicator,
            "indicator_value": dominant_value,
            "secondary_indicator_name": primary_indicator,
            "secondary_gain": float(secondary_gain),
            "indicator_type": candidate["indicator_type"],
            "n_unweighted": int(joint_mask.sum()),
            "n_weighted": float(wx_joint.fillna(0).sum()) if wx_joint is not None else float(joint_mask.sum()),
            "baseline_entropy": float(candidate["baseline_entropy"]),
            "conditional_entropy": float(candidate["conditional_entropy"]),
            "entropy_reduction": float(candidate["entropy_reduction"]),
            "mutual_information": float(candidate["mutual_information"]),
            "normalized_mutual_information": float(candidate["normalized_mutual_information"]),
            "cramers_v": float(candidate["cramers_v"]),
            "uplift_vs_baseline": float(candidate["uplift_vs_baseline"]),
            "dominant_response_pct_unweighted": float(candidate["dominant_response_pct_unweighted"]),
            "dominant_response_pct_weighted": float(candidate["dominant_response_pct_weighted"]),
            "confidence_tier": "usable" if joint_mask.sum() >= 50 else "weak",
        }
        rows.append(row)
    return rows


def indicator_answer_matrix_rows(df: pd.DataFrame, question_meta: dict[str, Any], weights: pd.Series | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    y = df["response_value_normalized"].fillna("").astype(str)
    for indicator in INDICATOR_FIELDS:
        if indicator not in df.columns:
            continue
        x = df[indicator].fillna("").astype(str)
        mask = x.ne("")
        if mask.sum() == 0:
            continue
        x_mask = x[mask]
        y_mask = y[mask]
        wx = weights[mask] if weights is not None else None
        unweighted_ct = pd.crosstab(x_mask, y_mask, dropna=False)
        if wx is not None:
            weighted_df = pd.DataFrame({"indicator": x_mask, "response": y_mask, "weight": pd.to_numeric(wx, errors="coerce").fillna(0.0)})
            weighted_ct = weighted_df.pivot_table(index="indicator", columns="response", values="weight", aggfunc="sum", fill_value=0.0, dropna=False)
        else:
            weighted_ct = unweighted_ct.astype(float)
        for indicator_value in unweighted_ct.index:
            unweighted_row = unweighted_ct.loc[indicator_value]
            weighted_row = weighted_ct.loc[indicator_value] if indicator_value in weighted_ct.index else pd.Series(dtype=float)
            unweighted_total = float(unweighted_row.sum())
            weighted_total = float(weighted_row.sum()) if not weighted_row.empty else 0.0
            all_response_values = list(unweighted_row.index)
            for response_value in all_response_values:
                unweighted_count = float(unweighted_row.get(response_value, 0))
                weighted_count = float(weighted_row.get(response_value, unweighted_count)) if not weighted_row.empty else float(unweighted_count)
                rows.append(
                    {
                        **question_meta,
                        "indicator_name": indicator,
                        "indicator_value": str(indicator_value),
                        "response_value": str(response_value),
                        "n_unweighted": int(unweighted_count),
                        "pct_unweighted": float(unweighted_count / unweighted_total) if unweighted_total else 0.0,
                        "n_weighted": float(weighted_count),
                        "pct_weighted": float(weighted_count / weighted_total) if weighted_total else 0.0,
                    }
                )
    return rows


def branch_nodes_rows(df: pd.DataFrame, question_meta: dict[str, Any], max_depth: int = 3, min_branch_n: int = DEFAULT_SUPPORT_CAP) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    effective_min_branch_n = support_threshold_from_total(question_meta.get("n_respondents"), support_cap=min_branch_n)

    def recurse(sub: pd.DataFrame, parent_id: str | None, depth: int, available: list[str], path: list[str]) -> None:
        node_id = f"{question_meta['question_id']}::{'/'.join(path) if path else 'root'}"
        y = sub["response_value_normalized"].fillna("").astype(str)
        dom, dom_pct = dominant_response(y)
        node_entropy = distribution_entropy(y)
        rows.append(
            {
                **question_meta,
                "node_id": node_id,
                "parent_node_id": parent_id or "",
                "branch_depth": depth,
                "split_indicator": path[-2] if len(path) >= 2 else "",
                "split_value": path[-1] if path else "",
                "node_entropy": float(node_entropy),
                "entropy_gain_from_parent": 0.0,
                "stop_reason": "pure_or_near_pure" if dom_pct >= 0.95 else "",
                "branch_type": "conforms" if depth == 0 else "split",
                "dominant_response": dom,
                "dominant_response_pct": float(dom_pct),
            }
        )
        if depth >= max_depth or len(sub) < effective_min_branch_n or not available:
            if rows[-1]["stop_reason"] == "":
                rows[-1]["stop_reason"] = "max_depth" if depth >= max_depth else "underpowered" if len(sub) < effective_min_branch_n else "no_remaining_indicators"
            return
        best_indicator = None
        best_gain = 0.0
        best_cond = None
        best_mask = None
        for indicator in available:
            if indicator not in sub.columns:
                continue
            x = sub[indicator].fillna("").astype(str)
            mask = x.ne("")
            if mask.sum() < effective_min_branch_n:
                continue
            cond = conditional_entropy(y[mask], x[mask])
            gain = node_entropy - cond
            if gain > best_gain:
                best_gain = gain
                best_indicator = indicator
                best_cond = x[mask]
                best_mask = mask
        if not best_indicator or best_gain <= 0:
            rows[-1]["stop_reason"] = "no_gain"
            return
        rows[-1]["split_indicator"] = best_indicator
        rows[-1]["entropy_gain_from_parent"] = float(best_gain)
        next_available = [i for i in available if i != best_indicator]
        for value in best_cond.value_counts().index[:2]:
            child = sub[sub[best_indicator].fillna("").astype(str) == str(value)]
            if len(child) < effective_min_branch_n:
                continue
            recurse(child, node_id, depth + 1, next_available, path + [best_indicator, str(value)])

    recurse(df, None, 0, [i for i in INDICATOR_FIELDS if i in df.columns], [])
    return rows


def outlier_cohort_rows(df: pd.DataFrame, question_meta: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    support_threshold = support_threshold_from_total(question_meta.get("n_respondents"))
    baseline_dom, baseline_pct = dominant_response(df["response_value_normalized"].fillna("").astype(str))
    weights = pd.to_numeric(df["weight_value"], errors="coerce") if "weight_value" in df.columns else None
    for indicator in INDICATOR_FIELDS:
        if indicator not in df.columns:
            continue
        for value, sub in df.groupby(df[indicator].fillna("").astype(str)):
            if value == "" or len(sub) < support_threshold:
                continue
            sub_weights = weights.loc[sub.index] if weights is not None else None
            n_weighted = float(sub_weights.fillna(0).sum()) if sub_weights is not None else float(len(sub))
            dom, dom_pct = dominant_response(sub["response_value_normalized"].fillna("").astype(str))
            branch_type = "conforms" if dom == baseline_dom else "deviates"
            if dom != baseline_dom and dom_pct >= baseline_pct:
                branch_type = "minority_converges"
            rows.append(
                {
                    **question_meta,
                    "indicator_name": indicator,
                    "indicator_value": value,
                    "branch_type": branch_type,
                    "n_unweighted": int(len(sub)),
                    "n_weighted": n_weighted,
                    "dominant_response": dom,
                    "dominant_response_pct": float(dom_pct),
                    "baseline_dominant_response": baseline_dom,
                    "baseline_dominant_response_pct": float(baseline_pct),
                }
            )
    return rows
