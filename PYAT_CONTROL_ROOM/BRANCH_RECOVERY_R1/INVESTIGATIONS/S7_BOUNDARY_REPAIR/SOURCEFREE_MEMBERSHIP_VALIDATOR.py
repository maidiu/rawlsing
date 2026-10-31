#!/usr/bin/env python3
"""Sourcefree membership validator for the PYAT S7-FIX boundary repair.

Reads only the seven S7_BOUNDARY_REPAIR artifacts. It does not import, parse, or
execute historical/production source. It checks exact function-ID custody,
outer/nested AST ownership, the single join, review-negative and first-consumer
preservation, external zero-member cases, and the 845-branch roster.
"""
import argparse
import copy
import hashlib
import json
import os
import sys

EXPECTED = {'adverse_count': 1571,
 'branch_count': 845,
 'branch_names_json_sha256': '92bd27c766e4aa5a7b9fc80b31d5d5ca53b3917231148880a6ec5e3ff47dce2f',
 'branch_names_newline_sha256': 'c781d59aafff7154726f8d6d4c0c61e9f2ae409df7643ad4b2d3cbea3063ca0e',
 'branch_pair_json_sha256': 'cf73dac1489d1db3ed1e9f8923235d1ca2ba3b758cb7c90cde8a9bf3f6f76fd2',
 'branch_pair_newline_sha256': '639ce73148494c254e2f76186e4469c5d5d1750a4acbcee7d39af694143613bd',
 'branch_shard_counts': {'S1': 175, 'S2': 175, 'S3': 174, 'S4': 161, 'S5': 160},
 'branch_tips_newline_sha256': '5f7fe08942cc90831509ea23e221f9897a0386f73595ad9ddb730a3dd7d20837',
 'expected_corrected_families': 1885,
 'expected_external': ['S6EXT-P41-SERVICE', 'S6EXT-R61-R09-NEGATIVE'],
 'expected_old_groups': 1881,
 'expected_shard_counts': {'S1': 1279, 'S2': 218, 'S3': 398, 'S4': 897, 'S5': 343},
 'expected_total': 3135,
 'first_consumer_count': 6887,
 'first_consumer_sha256': '79a135e0910568007357083187ffb0ae337b729b94890440f29dbc5c3474e533',
 'inherited_branch_union_count': 225,
 'inherited_branch_union_sha256': '5c586812883afd4333cbdae95a9ad83b68e2a774340fee9d637f7a8cb8fa2bb9',
 'join': {'family': 'S7FAM-41da3f505673271b',
          'members': ['4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445',
                      'rawlsing_next/pre553_physical_decoder.py::PhysicalSourceIncidence.iter_batches.emit'],
          'old_groups': ['FAM_bd6118ca46930519', 'S6FAM-23dd9c27fe2a7c60'],
          'path': 'rawlsing_next/pre553_physical_decoder.py',
          'qual': 'PhysicalSourceIncidence.iter_batches.emit'},
 'negative_count': 2595,
 'negative_sha256': '93cdb8e28653e42aebc7fe2b2c511333e85320eecee2710a37fe833fb80122f7',
 'overall_id_order_sha256': '5917b3bd58bb56f101d0daa35a0259761234a58a6c4bf9adaf6f0586d3593a68',
 'shard_id_order_sha256': {'S1': 'b3393f7ba5fc452f4225d46f9bbec870478466c562be82ac848463260214185d',
                           'S2': 'a2395017983425c16634dd9900eefe148b66775cfd1a3e8a50c0c6f15405075d',
                           'S3': '8976b390e86127faf76c4323ac9c6659291c51056af1c451995e7642de4b4fd4',
                           'S4': '2c99213df5bcc2064ce3e18ab8bc6a8a582f0137deee931c6c82717a8b5b5958',
                           'S5': '76dfba2e30b4d7fc421622eec0c641481f1d9169f48fb5733e2ddc84d3b82a33'},
 'split_specs': {'FAM_1427a684892de839': {'nested': ['0d719b06e1689c10095dfd9da701dbb02f28bb36'],
                                          'nested_family': 'S7FAM-0808b82fba697141',
                                          'nested_qual': '_make_sealed_source_relation_owner.SourceRelationResolver.require',
                                          'outer': ['1d789a2f1ade746a79847ff1a8f6bf3a9eea97ee',
                                                    'rawlsing_next/pre553_source_relations.py::SourceRelationResolver.require'],
                                          'outer_family': 'S7FAM-82686a98a4281425',
                                          'outer_qual': 'SourceRelationResolver.require',
                                          'path': 'rawlsing_next/pre553_source_relations.py'},
                 'FAM_214c6eaf1fe2a42d': {'nested': ['8fcb028899610f219a6b85dc09ef67d429834376'],
                                          'nested_family': 'S7FAM-739724b429c79765',
                                          'nested_qual': '_make_sealed_source_relation_owner.SourceRelationResolver._validate_positive',
                                          'outer': ['52bf494350f4abe5c16149241da8506a82401345',
                                                    'rawlsing_next/pre553_source_relations.py::SourceRelationResolver._validate_positive'],
                                          'outer_family': 'S7FAM-5823124c837704c1',
                                          'outer_qual': 'SourceRelationResolver._validate_positive',
                                          'path': 'rawlsing_next/pre553_source_relations.py'},
                 'FAM_6813a575a7ce67c0': {'nested': ['920b54cd009151c9c9b9fd7913201d14ce739511'],
                                          'nested_family': 'S7FAM-dabfb5ad4dc9f0a4',
                                          'nested_qual': '_make_sealed_source_relation_owner.SourceRelationResolver.decide',
                                          'outer': ['8dd873c436acfb407ad330294a910e2b082b197a',
                                                    'rawlsing_next/pre553_source_relations.py::SourceRelationResolver.decide'],
                                          'outer_family': 'S7FAM-6054813ba02c8e44',
                                          'outer_qual': 'SourceRelationResolver.decide',
                                          'path': 'rawlsing_next/pre553_source_relations.py'},
                 'FAM_b8e8a1c5bac3370d': {'nested': ['d8a2f70fc0de05bfe0f0db6d42e207d8d915ee64',
                                                     '733bdba8281c6cdf1fe5ce22cadd060627bd1b6c'],
                                          'nested_family': 'S7FAM-3ced5b9ab5b98431',
                                          'nested_qual': '_make_sealed_source_relation_owner.SourceRelationResolver.__init__',
                                          'outer': ['828fbc7fea7fdcaf419a79ea78c63c574e473f2d',
                                                    'rawlsing_next/pre553_source_relations.py::SourceRelationResolver.__init__'],
                                          'outer_family': 'S7FAM-0869c56ad5e0c899',
                                          'outer_qual': 'SourceRelationResolver.__init__',
                                          'path': 'rawlsing_next/pre553_source_relations.py'},
                 'FAM_c0d48f7daa8cc28d': {'nested': ['1e88e2680b5d88f8115575c5b382dc9c0658dbb2'],
                                          'nested_family': 'S7FAM-c7246db42c0322e0',
                                          'nested_qual': '_make_sealed_source_relation_owner.SourceRelationResolver.resolve_exact',
                                          'outer': ['7473e1e908d78e3a3f5bc9537dc922deaae81a6f',
                                                    'rawlsing_next/pre553_source_relations.py::SourceRelationResolver.resolve_exact'],
                                          'outer_family': 'S7FAM-a7fe27d3f45643c3',
                                          'outer_qual': 'SourceRelationResolver.resolve_exact',
                                          'path': 'rawlsing_next/pre553_source_relations.py'}}}

FILES = {
    "return": "00_RETURN.md",
    "mapping": "FUNCTION_ID_TO_CORRECTED_FAMILY.jsonl",
    "oldmap": "OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl",
    "review": "REVIEW_NEGATIVE_AND_VARIANT_PRESERVATION.md",
    "corrected": "CORRECTED_RECEIVER_AND_INTEGRATABILITY.json",
    "validator": "SOURCEFREE_MEMBERSHIP_VALIDATOR.py",
    "receipts": "TEST_RECEIPTS_AND_ABI_LIMITS.md",
}


class ValidationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha_obj(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def id_digest(seq):
    return hashlib.sha256(("\n".join(seq) + "\n").encode("utf-8")).hexdigest()


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                raise ValidationError("invalid JSONL %s:%d: %s" % (path, lineno, exc))
    return rows


def load_data(base):
    missing = [name for name in FILES.values() if not os.path.exists(os.path.join(base, name))]
    require(not missing, "missing required outputs: %s" % ", ".join(missing))
    with open(os.path.join(base, FILES["corrected"]), "r", encoding="utf-8") as handle:
        corrected = json.load(handle)
    return {
        "base": base,
        "mapping": load_jsonl(os.path.join(base, FILES["mapping"])),
        "oldmap": load_jsonl(os.path.join(base, FILES["oldmap"])),
        "corrected": corrected,
        "review_text": open(os.path.join(base, FILES["review"]), "r", encoding="utf-8").read(),
        "return_text": open(os.path.join(base, FILES["return"]), "r", encoding="utf-8").read(),
        "receipts_text": open(os.path.join(base, FILES["receipts"]), "r", encoding="utf-8").read(),
    }


def family_index(corrected):
    index = {}
    for family in corrected["corrected_families"]:
        fid = family["family_id"]
        require(fid not in index, "duplicate corrected family_id %s" % fid)
        index[fid] = family
    return index


def member_index(families):
    index = {}
    for family in families:
        for member in family["members"]:
            mid = member["function_id"]
            require(mid not in index, "function ID %s occurs in multiple family member records" % mid)
            index[mid] = (family, member)
    return index


def validate_data(data):
    mapping = data["mapping"]
    oldmap = data["oldmap"]
    corrected = data["corrected"]
    checks = []

    # ---- corrected family container ----
    require(corrected.get("schema") == "PYAT_S7FIX_CORRECTED_RECEIVER_AND_INTEGRATABILITY@1", "bad corrected schema")
    families = corrected.get("corrected_families") or []
    require(len(families) == EXPECTED["expected_corrected_families"],
            "corrected family count %d != %d" % (len(families), EXPECTED["expected_corrected_families"]))
    require([f.get("family_order") for f in families] == list(range(1, len(families) + 1)), "family_order not 1..N")
    fam_by_id = family_index(corrected)
    mem_by_id = member_index(families)
    checks.append("corrected_family_count")

    # ---- mapping custody ----
    require(len(mapping) == EXPECTED["expected_total"], "mapping row count %d != %d" % (len(mapping), EXPECTED["expected_total"]))
    require([r.get("order") for r in mapping] == list(range(1, len(mapping) + 1)), "mapping order not 1..N")
    ids = [r.get("function_id") for r in mapping]
    require(len(set(ids)) == len(ids), "duplicate function IDs in mapping")
    for shard, expected_count in EXPECTED["expected_shard_counts"].items():
        shard_rows = [r for r in mapping if r.get("shard") == shard]
        require(len(shard_rows) == expected_count, "%s row count %d != %d" % (shard, len(shard_rows), expected_count))
        require([r.get("shard_order") for r in shard_rows] == list(range(1, expected_count + 1)), "%s shard_order not 1..N" % shard)
        got = id_digest([r["function_id"] for r in shard_rows])
        require(got == EXPECTED["shard_id_order_sha256"][shard], "%s ordered ID digest drift" % shard)
    require(id_digest(ids) == EXPECTED["overall_id_order_sha256"], "overall ordered ID digest drift")
    for row in mapping:
        fid = row["function_id"]
        require(fid in mem_by_id, "mapping function ID %s absent from corrected family members" % fid)
        family, member = mem_by_id[fid]
        require(row.get("corrected_family_id") == family["family_id"], "mapping family mismatch for %s" % fid)
        require(row.get("old_group_id") == member.get("original_group_id"), "mapping old group mismatch for %s" % fid)
        require(row.get("identity") == member.get("identity"), "mapping identity mismatch for %s" % fid)
        require(row.get("correction_type") == family["correction"]["type"], "mapping correction type mismatch for %s" % fid)
    checks.append("function_id_custody")

    # ---- corrected family membership ----
    all_family_members = []
    for family in families:
        require(family.get("schema") == "PYAT_S7FIX_CORRECTED_FUNCTION_FAMILY@1", "bad family schema")
        require([m["function_id"] for m in family["members"]] == family.get("member_function_ids"),
                "family %s members[] != member_function_ids" % family["family_id"])
        require(len(family["member_function_ids"]) == family.get("member_count"),
                "family %s member_count mismatch" % family["family_id"])
        require(len(set(family["member_function_ids"])) == len(family["member_function_ids"]),
                "family %s duplicate member IDs" % family["family_id"])
        all_family_members.extend(family["member_function_ids"])
        require(family["correction"].get("behavioral_equivalence") == "NOT_CLAIMED",
                "family %s claims behavioral equivalence" % family["family_id"])
        require(family["correction"].get("science_acceptance") == "NOT_CLAIMED",
                "family %s claims science acceptance" % family["family_id"])
        cri = family.get("current_receiver_and_integratability") or {}
        require(cri.get("behavioral_equivalence") == "NOT_CLAIMED", "family %s receiver claims behavioral equivalence" % family["family_id"])
        require(cri.get("science_acceptance") == "NOT_CLAIMED", "family %s receiver claims science acceptance" % family["family_id"])
    require(len(all_family_members) == EXPECTED["expected_total"], "family membership total %d != %d" % (len(all_family_members), EXPECTED["expected_total"]))
    require(len(set(all_family_members)) == EXPECTED["expected_total"], "function ID appears in multiple corrected families")
    require(set(all_family_members) == set(ids), "mapping IDs and family member IDs differ")
    checks.append("corrected_family_membership")

    # ---- old-group map ----
    require(len(oldmap) == EXPECTED["expected_old_groups"], "old map row count %d != %d" % (len(oldmap), EXPECTED["expected_old_groups"]))
    require([r.get("old_group_order") for r in oldmap] == list(range(1, len(oldmap) + 1)), "old group order not 1..N")
    old_ids = [r.get("old_group_id") for r in oldmap]
    require(len(set(old_ids)) == len(old_ids), "duplicate old group IDs")
    legacy_to_families = {}
    for family in families:
        for old in family.get("legacy_group_ids") or []:
            legacy_to_families.setdefault(old, []).append(family)
    require(set(legacy_to_families) == set(old_ids), "old map IDs and legacy_group_ids differ")
    for row in oldmap:
        old = row["old_group_id"]
        fs = legacy_to_families[old]
        require(row.get("corrected_family_ids") == [f["family_id"] for f in fs],
                "old group %s corrected_family_ids mismatch" % old)
        for assignment in row.get("corrected_member_assignments") or []:
            family = fam_by_id.get(assignment["family_id"])
            require(family is not None, "old group %s assignment to missing family" % old)
            require(assignment["member_function_ids"] == family["member_function_ids"],
                    "old group %s assignment members mismatch" % old)
    require(sum(r["old_member_count"] for r in oldmap) == EXPECTED["expected_total"], "old group member sum drift")
    checks.append("old_group_map")

    # ---- external zero-member cases ----
    for ext in EXPECTED["expected_external"]:
        family = fam_by_id.get(ext)
        require(family is not None, "missing external zero-member family %s" % ext)
        require(family["member_count"] == 0 and family["member_function_ids"] == [], "external %s has members" % ext)
        require((family.get("preserved_group_fields") or {}).get("not_in_3135_original_rows") is True,
                "external %s not marked external" % ext)
        require(ext not in ids, "external %s leaked into function mapping" % ext)
    require(sum(1 for f in families if f["member_count"] == 0) == len(EXPECTED["expected_external"]),
            "unexpected zero-member family count")
    checks.append("external_zero_member_cases")

    # ---- split repairs ----
    split_types = {"SPLIT_MERGE_DEFECT__OUTER_OWNER", "SPLIT_MERGE_DEFECT__NESTED_OWNER"}
    split_families = [f for f in families if f["correction"]["type"] in split_types]
    require(len(split_families) == 10, "split family count %d != 10" % len(split_families))
    expected_split_ids = set()
    for old, spec in EXPECTED["split_specs"].items():
        outer = fam_by_id.get(spec["outer_family"])
        nested = fam_by_id.get(spec["nested_family"])
        require(outer is not None and nested is not None, "missing split families for %s" % old)
        expected_split_ids.update([spec["outer_family"], spec["nested_family"]])
        require(outer["correction"]["type"] == "SPLIT_MERGE_DEFECT__OUTER_OWNER", "bad outer split type for %s" % old)
        require(nested["correction"]["type"] == "SPLIT_MERGE_DEFECT__NESTED_OWNER", "bad nested split type for %s" % old)
        require(outer["family_name"] == spec["path"] + "::" + spec["outer_qual"], "outer family_name mismatch for %s" % old)
        require(nested["family_name"] == spec["path"] + "::" + spec["nested_qual"], "nested family_name mismatch for %s" % old)
        require(outer["actual_qualnames"] == [spec["outer_qual"]], "outer actual_qualnames mismatch for %s" % old)
        require(nested["actual_qualnames"] == [spec["nested_qual"]], "nested actual_qualnames mismatch for %s" % old)
        require(outer["member_function_ids"] == spec["outer"], "outer member IDs mismatch for %s" % old)
        require(nested["member_function_ids"] == spec["nested"], "nested member IDs mismatch for %s" % old)
        require(set(spec["outer"]).isdisjoint(set(spec["nested"])), "outer/nested member overlap for %s" % old)
        for mid in spec["outer"]:
            require(mem_by_id[mid][1]["identity"]["actual_qualname"] == spec["outer_qual"],
                    "outer member %s actual qualname mismatch" % mid)
            require("_make_sealed_source_relation_owner" not in mem_by_id[mid][1]["identity"]["actual_qualname"],
                    "nested owner leaked into outer member %s" % mid)
        for mid in spec["nested"]:
            require(mem_by_id[mid][1]["identity"]["actual_qualname"] == spec["nested_qual"],
                    "nested member %s actual qualname mismatch" % mid)
            require(mem_by_id[mid][1]["identity"]["actual_qualname"].startswith("_make_sealed_source_relation_owner."),
                    "nested member %s lacks nested owner" % mid)
        old_row = next((r for r in oldmap if r["old_group_id"] == old), None)
        require(old_row is not None, "missing old map row for %s" % old)
        require(old_row["correction_type"] == "SPLIT_MERGE_DEFECT", "old map correction type mismatch for %s" % old)
        require(old_row["corrected_family_ids"] == [spec["outer_family"], spec["nested_family"]],
                "old map split target order mismatch for %s" % old)
        require(set(old_row["old_member_function_ids"]) == set(spec["outer"]) | set(spec["nested"]),
                "old map split membership mismatch for %s" % old)
        # Negative ownership must remain separated.
        for rec in outer.get("review_negative_preservation") or []:
            require(rec.get("attribution") != "NESTED_OWNER", "nested negative attached to outer family %s" % old)
        for rec in nested.get("review_negative_preservation") or []:
            require(rec.get("attribution") != "OUTER_OWNER", "outer negative attached to nested family %s" % old)
            require(rec.get("attribution") != "CONTEXTUAL_ONLY__NESTED_SEALED_OWNER__NOT_OUTER_DEFECT",
                    "contextual nested record placed in nested family %s" % old)
    require({f["family_id"] for f in split_families} == expected_split_ids, "unexpected split family IDs")
    checks.append("split_repairs")

    # ---- join repair ----
    join_spec = EXPECTED["join"]
    join_families = [f for f in families if f["correction"]["type"] == "JOIN_SPLIT_DEFECT"]
    require(len(join_families) == 1, "join family count %d != 1" % len(join_families))
    join = join_families[0]
    require(join["family_id"] == join_spec["family"], "join family ID mismatch")
    require(join["member_function_ids"] == join_spec["members"], "join member IDs mismatch")
    require(join["actual_qualnames"] == [join_spec["qual"]], "join actual qualname mismatch")
    require(join["family_name"] == join_spec["path"] + "::" + join_spec["qual"], "join family_name mismatch")
    for mid in join_spec["members"]:
        require(mem_by_id[mid][1]["identity"]["actual_qualname"] == join_spec["qual"],
                "join member %s actual qualname mismatch" % mid)
    for old in join_spec["old_groups"]:
        row = next((r for r in oldmap if r["old_group_id"] == old), None)
        require(row is not None, "missing join old group %s" % old)
        require(row["correction_type"] == "JOIN_SPLIT_DEFECT", "join old map type mismatch for %s" % old)
        require(row["corrected_family_ids"] == [join_spec["family"]], "join old map target mismatch for %s" % old)
        require("preserved_old_group_record" in row, "join old group %s full record not preserved" % old)
    checks.append("join_repair")

    # ---- review-negative preservation ----
    all_negative = []
    for family in families:
        for rec in family.get("review_negative_preservation") or []:
            all_negative.append(rec)
            if rec.get("scope") == "FUNCTION":
                mid = rec.get("function_id")
                require(mid in family["member_function_ids"], "negative record %s outside its family" % mid)
                require(rec.get("s6_member_review_findings") is not None, "negative record %s lost S6 member findings" % mid)
                require(rec.get("source_review_evidence_sha256"), "negative record %s lacks source review digest" % mid)
            else:
                require(rec.get("old_group_id") in (family.get("legacy_group_ids") or []),
                        "group negative record outside legacy group set")
                require(rec.get("s6_group_review_findings") is not None, "group negative record lost full findings")
    require(len(all_negative) == EXPECTED["negative_count"],
            "negative record count %d != %d" % (len(all_negative), EXPECTED["negative_count"]))
    require(sha_obj(all_negative) == EXPECTED["negative_sha256"], "negative preservation digest drift")
    adverse = sum(1 for rec in all_negative if rec.get("adverse_review_signal"))
    require(adverse == EXPECTED["adverse_count"], "adverse review count %d != %d" % (adverse, EXPECTED["adverse_count"]))
    # Every split/join member keeps its own negative record; no cross-owner attribution.
    for old, spec in EXPECTED["split_specs"].items():
        for mid in spec["outer"] + spec["nested"]:
            family = mem_by_id[mid][0]
            recs = [r for r in family.get("review_negative_preservation") or [] if r.get("function_id") == mid]
            require(len(recs) == 1, "split member %s lacks exactly one negative record" % mid)
    for mid in join_spec["members"]:
        family = mem_by_id[mid][0]
        recs = [r for r in family.get("review_negative_preservation") or [] if r.get("function_id") == mid]
        require(len(recs) == 1, "join member %s lacks exactly one negative record" % mid)
    checks.append("review_negative_preservation")

    # ---- first-consumer preservation, no invention ----
    all_first = []
    for family in families:
        for member in family["members"]:
            fe = member.get("first_consumer_evidence") or {}
            rec = {
                "schema": "PYAT_S7FIX_FIRST_CONSUMER_EVIDENCE@1",
                "scope": "FUNCTION",
                "function_id": member["function_id"],
                "shard": member["shard"],
                "actual_qualname": member["identity"]["actual_qualname"],
                "source_field": fe.get("source_field"),
                "data": fe.get("data"),
                "source_row_sha256": member.get("source_row_sha256"),
                "source_record_sha256": sha_obj({"source_field": fe.get("source_field"), "data": fe.get("data")}),
            }
            require(rec["source_field"], "member %s lacks first-consumer source field" % member["function_id"])
            all_first.append(rec)
        for rec in family.get("first_consumer_evidence") or []:
            require(rec.get("scope") != "FUNCTION", "family stores duplicate function-scope first consumer record")
            require(rec.get("old_group_id") in (family.get("legacy_group_ids") or []),
                    "group first-consumer record outside legacy group set")
            require(rec.get("source_field"), "group first-consumer record lacks source field")
            require(rec.get("source_record_sha256") == sha_obj(rec.get("data")),
                    "group first-consumer record digest mismatch")
            require(rec.get("invented") is not True, "invented first-consumer record")
            all_first.append(rec)
    require(len(all_first) == EXPECTED["first_consumer_count"],
            "first-consumer record count %d != %d" % (len(all_first), EXPECTED["first_consumer_count"]))
    require(sha_obj(all_first) == EXPECTED["first_consumer_sha256"], "first-consumer preservation digest drift")
    for old, spec in EXPECTED["split_specs"].items():
        for fid in (spec["outer_family"], spec["nested_family"]):
            family = fam_by_id[fid]
            require(not family.get("first_consumer_evidence"), "split family %s has reassigned group-level consumer" % fid)
    checks.append("first_consumer_preservation")

    # ---- branch identity custody ----
    roster = (corrected.get("branch_identity_custody") or {}).get("branches") or []
    require(len(roster) == EXPECTED["branch_count"], "branch roster %d != %d" % (len(roster), EXPECTED["branch_count"]))
    names = [b.get("branch") for b in roster]
    require(len(set(names)) == EXPECTED["branch_count"], "duplicate branch names")
    for shard, count in EXPECTED["branch_shard_counts"].items():
        require(sum(1 for b in roster if b.get("shard") == shard) == count, "%s branch count drift" % shard)
    require(id_digest(names) == EXPECTED["branch_names_newline_sha256"], "branch name order digest drift")
    require(id_digest([b.get("roster_tip") for b in roster]) == EXPECTED["branch_tips_newline_sha256"], "branch tip digest drift")
    require(id_digest([b.get("branch") + "|" + b.get("roster_tip") for b in roster]) == EXPECTED["branch_pair_newline_sha256"],
            "branch pair digest drift")
    require(sha_obj([{"branch": b.get("branch"), "roster_tip": b.get("roster_tip"), "shard": b.get("shard"), "shard_order": b.get("shard_order")} for b in roster]) == EXPECTED["branch_pair_json_sha256"],
            "branch pair JSON digest drift")
    roster_set = set(names)
    inherited = set()
    for family in families:
        pg = family.get("preserved_group_fields")
        if isinstance(pg, list):
            for item in pg:
                inherited.update(item.get("inherited_branches") or [])
        elif isinstance(pg, dict):
            inherited.update(pg.get("inherited_branches") or [])
        pg2 = family.get("preserved_group_fields_NOT_REASSIGNED") or {}
        inherited.update((pg2.get("fields") or {}).get("inherited_branches") or [])
    require(inherited <= roster_set, "inherited S6 branch missing from 845 roster")
    require(len(inherited) == EXPECTED["inherited_branch_union_count"],
            "inherited branch union count %d != %d" % (len(inherited), EXPECTED["inherited_branch_union_count"]))
    require(sha_obj(sorted(inherited)) == EXPECTED["inherited_branch_union_sha256"], "inherited branch union digest drift")
    checks.append("branch_identity_custody")

    # ---- count formula and external preservation ----
    require(corrected["counts"]["corrected_families"] == EXPECTED["expected_corrected_families"], "counts.corrected_families drift")
    require(corrected["counts"]["function_ids"] == EXPECTED["expected_total"], "counts.function_ids drift")
    require(len(corrected.get("external_zero_member_cases") or []) == len(EXPECTED["expected_external"]), "external case summary count drift")
    checks.append("counts_and_external_cases")

    return {
        "status": "PASS",
        "checks": checks,
        "counts": {
            "function_ids": len(mapping),
            "old_groups": len(oldmap),
            "corrected_families": len(families),
            "branches": len(roster),
        },
        "digests": {
            "function_ids": id_digest(ids),
            "negative_records": sha_obj(all_negative),
            "first_consumer_records": sha_obj(all_first),
            "branches": id_digest(names),
            "inherited_branches": sha_obj(sorted(inherited)),
        },
    }


def expect_failure(data, label, mutate):
    mutate(data)
    try:
        validate_data(data)
    except ValidationError:
        return "%s: detected" % label
    raise ValidationError("self-test mutation was NOT detected: %s" % label)


def self_test(base):
    baseline = validate_data(load_data(base))
    results = ["baseline: PASS (%d checks)" % len(baseline["checks"])]

    def mutate_missing_mapping(data):
        data["mapping"].pop()

    def mutate_duplicate_mapping(data):
        data["mapping"].append(copy.deepcopy(data["mapping"][0]))

    def mutate_split_ownership(data):
        spec = next(iter(EXPECTED["split_specs"].values()))
        outer = next(f for f in data["corrected"]["corrected_families"] if f["family_id"] == spec["outer_family"])
        nested = next(f for f in data["corrected"]["corrected_families"] if f["family_id"] == spec["nested_family"])
        moved = nested["member_function_ids"].pop(0)
        nested["member_count"] = len(nested["member_function_ids"])
        outer["member_function_ids"].append(moved)
        outer["member_count"] = len(outer["member_function_ids"])

    def mutate_false_join(data):
        join = next(f for f in data["corrected"]["corrected_families"] if f["correction"]["type"] == "JOIN_SPLIT_DEFECT")
        join["actual_qualnames"] = ["PhysicalSourceIncidence.emit"]
        for member in join["members"]:
            member["identity"]["actual_qualname"] = "PhysicalSourceIncidence.emit"

    def mutate_lost_negative(data):
        for family in data["corrected"]["corrected_families"]:
            if family.get("review_negative_preservation"):
                family["review_negative_preservation"].pop()
                return
        raise ValidationError("no negative record available for mutation")

    def mutate_invented_consumer(data):
        family = data["corrected"]["corrected_families"][0]
        family.setdefault("first_consumer_evidence", []).append({
            "schema": "PYAT_S7FIX_FIRST_CONSUMER_EVIDENCE@1",
            "scope": "GROUP",
            "old_group_id": family["legacy_group_ids"][0],
            "source_field": "INVENTED",
            "data": {"status": "REAL_CONSUMER"},
            "source_record_sha256": sha_obj({"status": "REAL_CONSUMER"}),
            "invented": True,
        })

    def mutate_branch_drift(data):
        data["corrected"]["branch_identity_custody"]["branches"].pop()

    def mutate_oldmap_drift(data):
        data["oldmap"].pop()

    results.append(expect_failure(load_data(base), "missing mapping ID", mutate_missing_mapping))
    results.append(expect_failure(load_data(base), "duplicate mapping ID", mutate_duplicate_mapping))
    results.append(expect_failure(load_data(base), "outer/nested mis-nesting", mutate_split_ownership))
    results.append(expect_failure(load_data(base), "false join identity", mutate_false_join))
    results.append(expect_failure(load_data(base), "lost adverse review", mutate_lost_negative))
    results.append(expect_failure(load_data(base), "invented first consumer", mutate_invented_consumer))
    results.append(expect_failure(load_data(base), "branch roster drift", mutate_branch_drift))
    results.append(expect_failure(load_data(base), "old group map drift", mutate_oldmap_drift))
    return {"status": "PASS", "baseline": baseline, "self_test": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)), help="artifact directory")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    parser.add_argument("--self-test", action="store_true", help="run fail-capability mutations")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            result = self_test(args.dir)
        else:
            result = validate_data(load_data(args.dir))
    except ValidationError as exc:
        result = {"status": "FAIL", "error": str(exc)}
        if args.json:
            print(json.dumps(result, indent=1, ensure_ascii=False))
        else:
            print("FAIL: %s" % exc)
        return 1
    if args.json:
        print(json.dumps(result, indent=1, ensure_ascii=False))
    else:
        print("PASS: %s" % ", ".join(result.get("checks", [])))
        if args.self_test:
            for line in result.get("self_test", []):
                print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
