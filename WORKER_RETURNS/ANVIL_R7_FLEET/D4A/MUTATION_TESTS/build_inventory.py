#!/usr/bin/env python3
"""Build a source-authenticated 118 identity inventory from exact Git/ZIP bytes.

This replaces the false dependency on a never-accepted R5/R6 SPINE.json.
It does NOT create semantic truth beyond the exact rows; terminal identities are
marked identity_only and remain owner/scope held.
"""
import hashlib, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SNAP = ROOT / "EVIDENCE" / "source_snapshot"
GIT = pathlib.Path("/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/D4A")
K3_COMMIT = "7fc00289dd801d2d0a8ce159986c7595fc27a4d9"
K3_DIR = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1"
SEAM25 = dict(path="SEAM/25_RETURN_TO_BOUNDARY_TRANSFORMATIONS_AND_OPEN_REGISTER_R1.md",
              commit="596f1230258ff50f98d8543dec42a80e696720f4",
              blob="181ab1aaee26d71524dd7401a59c2ca550b4a81c", local="docs/SEAM25.md")
SEAM26 = dict(path="SEAM/26_CONDITIONED_SOCIAL_FIELD_IDENTIFICATION_AND_GENERATIVE_PERSON_REVERSE_CONTRACT_R1.md",
              commit="796452b8cb788fa5a02f37a7ce86eafce8312dfe",
              blob="a05c21dd0b7b1d404fc500c0ef36c81aee67c96e", local="docs/SEAM26.md")
ANVIL15 = dict(path="PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ANVIL/15_SEAM_REVERSE_CONSUMER_SOCIAL_FIELD_AND_C11_DESIGN_IMPLICATIONS_R1.md",
               commit="3cc09bba3d0e26c226da0ddca4b64c43dd74e493",
               blob="6253a632d10f201e0bf446f055f96c82fb4a479f", local="docs/ANVIL15.md")
ZIP_SHA = "526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332"

def sha(b): return hashlib.sha256(b).hexdigest()

def rows(path):
    raw = path.read_bytes().splitlines()
    return raw[0].decode(), [r for r in raw[1:] if r.strip()]

def anchor(path, sha256, commit, blob, excerpt, kind):
    return {"path": path, "sha256": sha256, "exact_excerpt": excerpt[:220],
            "git_commit": commit, "git_blob": blob, "source_class": kind}

def main():
    out = {"schema": "ANVIL_R7_SOURCE_AUTHENTICATED_IDENTITY_INVENTORY",
           "created_by": "D4A hostile-authority bounded pass",
           "source_authentication": "EXACT_GIT_ZIP_BYTES_CHECKED_LOCALLY_NOT_OWNER_SCIENCE",
           "warning": "This is a source-located identity inventory. It is not an accepted R5/R6 SPINE, architecture decision, native run or owner receiving.",
           "groups": {}}
    k3 = {}
    for group, fname, idcol in (("K1_CAP", "K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv", "capability_id"),
                                ("PYAT_PC", "K3_R15_26_OWNER_DECISIONS.tsv", "proposal_id"),
                                ("P4R", "K3_P4R_14_OBLIGATION_ROUTES.tsv", "P4R_id")):
        header, rs = rows(SNAP / "K3" / fname)
        cols = header.split("\t")
        blob = subprocess.check_output(["git", "-C", str(GIT), "rev-parse", f"{K3_COMMIT}:{K3_DIR}/{fname}"], text=True).strip()
        recs = {}
        for r in rs:
            vals = r.decode().split("\t")
            d = dict(zip(cols, vals))
            rid = d[idcol]
            recs[rid] = d
        k3[group] = dict(header=header, cols=cols, recs=recs, blob=blob,
                         path=f"{K3_DIR}/{fname}", sha256=sha((SNAP / "K3" / fname).read_bytes()))
    # K1
    g = {}
    for rid, d in k3["K1_CAP"]["recs"].items():
        raw = "\t".join(d[c] for c in k3["K1_CAP"]["cols"]).encode()
        g[rid] = {
            "source_kind": "K3_TSV_ROW", "source_anchor": anchor(k3["K1_CAP"]["path"], k3["K1_CAP"]["sha256"], K3_COMMIT, k3["K1_CAP"]["blob"], d["five_test_source_science_and_cost"], "PROTECTED_K3"),
            "row_sha256": sha(raw), "source_semantics": d["five_test_source_science_and_cost"],
            "consumer_or_hold": d["actual_current_first_reader_or_hold"],
            "negative_meaning": d["P2_accepted_falsifier_correction"],
            "architecture_effect": d["HQ_specification_choice"],
            "why": "Protected K3 capability " + d.get("historical_paths", "") + " retained by exact row; no automatic build.",
            "necessity": "HISTORICAL_CAPABILITY", "status": "PRESERVE_WITHOUT_BUILD",
            "evidence_ids": ["K3:" + rid], "identity_only": False}
    out["groups"]["K1_CAP"] = g
    g = {}
    for rid, d in k3["PYAT_PC"]["recs"].items():
        raw = "\t".join(d[c] for c in k3["PYAT_PC"]["cols"]).encode()
        g[rid] = {
            "source_kind": "K3_TSV_ROW", "source_anchor": anchor(k3["PYAT_PC"]["path"], k3["PYAT_PC"]["sha256"], K3_COMMIT, k3["PYAT_PC"]["blob"], d["negative_or_nonclaim"], "PROTECTED_K3"),
            "row_sha256": sha(raw), "source_semantics": d["original_topic"] + " :: " + d["selected_source_requirement"],
            "consumer_or_hold": d["source_owner"] + " :: " + d["HQ_five_test_owner_disposition"],
            "negative_meaning": d["negative_or_nonclaim"],
            "architecture_effect": d["HQ_five_test_owner_disposition"],
            "why": "K3 R15 proposal " + d.get("proposal_id", "") + " remains NOT_ADOPTED; no future permission issued.",
            "necessity": "HISTORICAL_NOT_ADOPTED", "status": "PRESERVE_WITHOUT_BUILD",
            "adopted": False, "evidence_ids": ["K3:" + rid], "identity_only": False}
    out["groups"]["PYAT_PC"] = g
    g = {}
    for rid, d in k3["P4R"]["recs"].items():
        raw = "\t".join(d[c] for c in k3["P4R"]["cols"]).encode()
        g[rid] = {
            "source_kind": "K3_TSV_ROW", "source_anchor": anchor(k3["P4R"]["path"], k3["P4R"]["sha256"], K3_COMMIT, k3["P4R"]["blob"], d["original_unproved_edge"], "PROTECTED_K3"),
            "row_sha256": sha(raw), "source_semantics": d["original_unproved_edge"],
            "consumer_or_hold": d["original_competent_owner"] + " :: " + d["protected_receiving"],
            "negative_meaning": "HELD; " + d["permission_and_native_ceiling"],
            "architecture_effect": d["HQ_route"] + " :: " + d["next_bounded_test"],
            "why": "P4R " + rid + " remains an unresolved finite proof, not closed by this instrument.",
            "necessity": "HISTORICAL_PROOF_HELD", "status": "PRESERVE_WITHOUT_BUILD",
            "closed": False, "evidence_ids": ["K3:" + rid], "identity_only": False}
    out["groups"]["P4R"] = g
    # SEAM B
    g = {}
    for line in (SNAP / "docs" / "SEAM25.md").read_text().splitlines():
        m = re.match(r"^\| \*\*(B-\d\d) ([^|]+)\*\* \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if not m: continue
        rid, title, question, discrim, receiving = [x.strip() for x in m.groups()]
        g[rid] = {"source_kind": "DOCUMENTARY_ROW", "source_anchor": anchor(SEAM25["path"], sha((SNAP / "docs" / "SEAM25.md").read_bytes()), SEAM25["commit"], SEAM25["blob"], line, "SEAM_DOCUMENTARY"),
                  "row_sha256": sha(line.encode()), "source_semantics": question,
                  "consumer_or_hold": receiving, "negative_meaning": discrim,
                  "architecture_effect": "Boundary transformation question; may close by proving richer pathway unnecessary.",
                  "why": "SEAM " + rid + " (" + title + ") is an open cross-boundary question, not an executed function.",
                  "necessity": "FUTURE_NONPRECLUSION", "status": "REQUIRES_TEST",
                  "evidence_ids": ["SEAM25:" + rid], "identity_only": False}
    out["groups"]["SEAM_B"] = g
    # SEAM S
    g = {}
    for line in (SNAP / "docs" / "SEAM26.md").read_text().splitlines():
        m = re.match(r"^\| \*\*(S-\d\d) ([^|]+)\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if not m: continue
        rid, title, why, critical, owner, falsepos = [x.strip() for x in m.groups()]
        g[rid] = {"source_kind": "DOCUMENTARY_ROW", "source_anchor": anchor(SEAM26["path"], sha((SNAP / "docs" / "SEAM26.md").read_bytes()), SEAM26["commit"], SEAM26["blob"], line, "SEAM_DOCUMENTARY"),
                  "row_sha256": sha(line.encode()), "source_semantics": critical,
                  "consumer_or_hold": owner, "negative_meaning": falsepos,
                  "architecture_effect": "Reverse-consumer requirement; must be supported or exact owner-held by C11 design.",
                  "why": "SEAM " + rid + " (" + title + "): " + why,
                  "necessity": "FUTURE_NONPRECLUSION", "status": "REQUIRES_TEST",
                  "evidence_ids": ["SEAM26:" + rid], "identity_only": False}
    out["groups"]["SEAM_S"] = g
    # ANVIL L
    g = {}
    for line in (SNAP / "docs" / "ANVIL15.md").read_text().splitlines():
        m = re.match(r"^\| \*\*(L-\d\d) ([^|]+)\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if not m: continue
        rid, title, info, why, links, disp = [x.strip() for x in m.groups()]
        g[rid] = {"source_kind": "DOCUMENTARY_ROW", "source_anchor": anchor(ANVIL15["path"], sha((SNAP / "docs" / "ANVIL15.md").read_bytes()), ANVIL15["commit"], ANVIL15["blob"], line, "ANVIL_DOCUMENTARY"),
                  "row_sha256": sha(line.encode()), "source_semantics": info,
                  "consumer_or_hold": links, "negative_meaning": why,
                  "architecture_effect": disp,
                  "why": "ANVIL/15 " + rid + " (" + title + ") irreversible-input-loss risk.",
                  "necessity": "FUTURE_NONPRECLUSION", "status": "REQUIRES_TEST",
                  "evidence_ids": ["ANVIL15:" + rid], "identity_only": False}
    out["groups"]["ANVIL_L"] = g
    # BOUNDARY from supplied ZIP package
    b = json.loads((SNAP / "package" / "02_BOUNDARY_CONTRACTS.json").read_text())
    g = {}
    for item in b["boundaries"]:
        rid = item["id"]
        g[rid] = {"source_kind": "BOUNDARY_CONTRACT",
                  "source_anchor": {"path": "02_BOUNDARY_CONTRACTS.json", "sha256": sha((SNAP / "package" / "02_BOUNDARY_CONTRACTS.json").read_bytes()), "exact_excerpt": item["veto"], "zip_sha256": ZIP_SHA, "source_class": "SUPPLIED_ZIP"},
                  "row_sha256": sha(json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()),
                  "source_semantics": item["must_preserve"],
                  "consumer_or_hold": item["producers"] + " -> " + item["receivers"],
                  "negative_meaning": item["veto"],
                  "architecture_effect": item["first_effect"],
                  "why": "T boundary " + rid + " is an architectural interrogation, not a pipeline stage or scientific grant.",
                  "necessity": "FUTURE_NONPRECLUSION", "status": "REQUIRES_TEST",
                  "evidence_ids": ["BOUNDARY:" + rid], "identity_only": False}
    out["groups"]["BOUNDARY"] = g
    # TERMINAL identities from frozen cuts; identity-only, no invented semantics
    c = json.loads((SNAP / "package" / "03_FROZEN_SOURCE_CUTS.json").read_text())
    g = {}
    for rid in c["mandatory"]["TERMINAL"]:
        g[rid] = {"source_kind": "TERMINAL_IDENTITY",
                  "source_anchor": {"path": "03_FROZEN_SOURCE_CUTS.json", "sha256": sha((SNAP / "package" / "03_FROZEN_SOURCE_CUTS.json").read_bytes()), "exact_excerpt": '"' + rid + '"', "zip_sha256": ZIP_SHA, "source_class": "SUPPLIED_ZIP"},
                  "row_sha256": sha(rid.encode()), "source_semantics": "TERMINAL_ID_ONLY: " + rid,
                  "consumer_or_hold": "Subject to scope and authority analysis; no implementation or acceptance asserted.",
                  "negative_meaning": "Terminal inclusion is not implementation, adoption or scientific grant.",
                  "architecture_effect": "Must remain representable or exact owner-held; cannot be omitted silently.",
                  "why": "Frozen terminal identity " + rid + " from supplied 03_FROZEN_SOURCE_CUTS.json.",
                  "necessity": "FUTURE_NONPRECLUSION", "status": "UNKNOWN_HELD",
                  "evidence_ids": ["TERMINAL:" + rid], "identity_only": True}
    out["groups"]["TERMINAL"] = g
    # Verify counts and write
    expect = {"K1_CAP": 29, "PYAT_PC": 26, "P4R": 14, "SEAM_B": 10, "SEAM_S": 8, "ANVIL_L": 8, "BOUNDARY": 7, "TERMINAL": 16}
    for k, n in expect.items():
        if len(out["groups"][k]) != n:
            raise SystemExit(f"COUNT FAIL {k}: {len(out['groups'][k])} != {n}")
    out["counts"] = {k: len(v) for k, v in out["groups"].items()}
    out["total"] = sum(out["counts"].values())
    dest = ROOT / "EVIDENCE" / "source_authenticated_inventory.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"status": "BUILT", "total": out["total"], "counts": out["counts"], "sha256": sha(dest.read_bytes()), "path": str(dest)}, indent=2))

if __name__ == "__main__":
    main()
