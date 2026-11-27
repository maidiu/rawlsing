"""FIELD FORGE R6: local, retrospective native evidence reader candidate.
Not an authority issuer, crosswalk, sampler, world writer or PYAT query replacement.
Requires pandas/openpyxl; ILOSTAT RDS additionally requires pyreadr.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

import pandas as pd

FILES = {
    "EPR": "01_CORE/EPR/EPR-2021.csv",
    "ED": "03_INTERSUBJECTIVE/EPR/ED-2021.csv",
    "TEK": "03_INTERSUBJECTIVE/EPR/TEK-2021.csv",
    "WBL": "01_CORE/WBL/WBL1-0-1971-2024.dta",
    "JOIN": "01_CORE/JOIN/join_database_w_definitions.xlsx",
    "FINDEX": "01_CORE/Findex/GlobalFindexDatabase2025.dta",
}
JOIN_STATUS = ("Wage employees, aged 15-64 ", "Self-employed, aged 15-64",
               "Unpaid, aged 15-64", "Employers, aged 15-64")
WBL_QUESTIONS = ("gr4_13obeymrd", "gr4_16dvrcjdgmnt", "gr7_30prtylegadmin",
                 "gr7_31valnonmntry", "gr5_19govleaveprov", "gr5_22pregdism",
                 "mtrnity_days")
FINDEX_MARGINS = ("account_t_d", "save_any_t_d", "borrow_any_t_d", "fin24aP",
                  "fin24aN", "fin32", "fin37_38")


def native_scalar(v):
    if pd.isna(v):
        return None
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float) and not math.isfinite(v):
        raise ValueError("nonfinite native number")
    return v


class NativePack:
    def __init__(self, root):
        self.root = Path(root)
        with (self.root / "PACK_MANIFEST.tsv").open(newline="", encoding="utf-8") as f:
            self.manifest = {r["relative_path"]: r for r in csv.DictReader(f, delimiter="\t")}
        self.cache = {}

    def load(self, source):
        if source in self.cache:
            return self.cache[source]
        if source.startswith("ILO:"):
            indicator = source[4:]
            if not indicator or not all(c.isalnum() or c == "_" for c in indicator):
                raise ValueError("invalid native indicator")
            rel = f"02_ILOSTAT/indicator/{indicator}.rds"
        else:
            rel = FILES[source]
        record = self.manifest[rel]
        path = self.root / rel
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != record["sha256"] or path.stat().st_size != int(record["bytes"]):
            raise ValueError(f"source file differs from manifest: {rel}")
        if path.suffix == ".csv":
            d = pd.read_csv(path)
        elif path.suffix == ".dta":
            d = pd.read_stata(path, convert_categoricals=False)
        elif path.suffix == ".xlsx":
            d = pd.read_excel(path, sheet_name="Sheet1", header=3)
            d = d.loc[:, ~d.columns.str.startswith("Unnamed:")]
        else:
            import pyreadr
            objects = pyreadr.read_r(str(path))
            if len(objects) != 1:
                raise ValueError("RDS object selection ambiguous")
            d = next(iter(objects.values()))
        self.cache[source] = (d, rel, digest)
        return self.cache[source]

    def select(self, source, keys, fields=None, year=None):
        d, rel, digest = self.load(source)
        mask = pd.Series(True, index=d.index)
        for k, v in keys.items():
            if v is None:
                raise ValueError("explicit nonnull key required")
            mask &= d[k].eq(v).fillna(False)
        if year is not None:
            if source != "EPR" or type(year) is not int:
                raise ValueError("interval query only for EPR integer reference year")
            mask &= (d["from"] <= year) & (d["to"] >= year)
        selected = d.loc[mask, list(fields) if fields is not None else list(d.columns)]
        rows = [{"data_row_index": int(i), "values": {k: native_scalar(v) for k, v in row.items()}}
                for i, row in selected.iterrows()]
        return {"source": source, "file": rel, "sha256": digest, "keys": keys,
                "epr_reference_year": year, "grade": "NATIVE_FILE_READ_NOT_ADMITTED",
                "time_use": "RETROSPECTIVE_ONLY", "status": "ROWS" if rows else "NO_MATCH",
                "rows": rows}

    def context(self, *, gwid, epr_year, economy, wbl_year, join_year, subsample,
                fin_year, fin_group, fin_group2):
        """Explicit independent source keys; no inferred territorial or temporal equivalence."""
        epr = self.select("EPR", {"gwid": gwid}, year=epr_year)
        formations = []
        for row in epr["rows"]:
            g = row["values"]["gwgroupid"]
            key = {"gwid": gwid, "gwgroupid": g}
            ed = self.select("ED", key)
            links = self.select("TEK", key)
            kin = [self.select("TEK", {"tekid": x["values"]["tekid"]}) for x in links["rows"]]
            formations.append({"epr_row": row, "ed_undated": ed, "tek_undated": links,
                               "tek_sets_not_contacts": kin})
        wbl = self.select("WBL", {"economycode": economy, "year": wbl_year},
                          ("economycode", "year", "reportyr", *WBL_QUESTIONS))
        join = self.select("JOIN", {"Country Code": economy, "Year of survey": join_year,
                                   "Subsample": subsample},
                           ("Country Code", "Year of survey", "Survey Data Source", "Survey Type",
                            "Subsample", *JOIN_STATUS, "Share of work contract",
                            "Share of health insurance", "Share of social security",
                            "Average weekly working hours", "Total flags in survey"))
        for row in join["rows"]:
            row["employment_partition"] = partition(row["values"])
        fin = self.select("FINDEX", {"codewb": economy, "year": fin_year,
                                    "group": fin_group, "group2": fin_group2},
                          ("codewb", "year", "group", "group2", *FINDEX_MARGINS))
        return {"grade": "PROVISIONAL_RETROSPECTIVE_CONTEXT_NOT_WORLD_FACT",
                "alignment": "CALLER_SELECTED_KEYS_NOT_QUALIFIED_CROSSWALK",
                "epr": epr, "formations": formations, "wbl": wbl, "join": join, "findex": fin,
                "unresolved": ["historical and group correspondence", "PYAT coherent D1/D2",
                               "actual actor roles, public norms, resource access and rules",
                               "independent Other selection, contact and acquisition"],
                "boundaries": {"wbl": "standardized legal case, not actual applicability",
                               "epr": "Jan 1 reference (first independence year exception)",
                               "ed_tek": "undated; no inherited year, individual joint or contact",
                               "join_findex": "native fractions, not independent person draws"}}


def partition(values, tolerance=1e-6):
    v = [values[k] for k in JOIN_STATUS]
    if any(x is None for x in v):
        return {"status": "PARTIAL", "native_shares": v}
    if any(type(x) not in (int, float) or not math.isfinite(x) or not 0 <= x <= 1 for x in v):
        return {"status": "INVALID_SHARE", "native_shares": v}
    total = math.fsum(v)
    return {"status": "COMPLETE" if abs(total - 1) <= tolerance else "NONUNIT_SUM",
            "native_shares": v, "sum": total, "tolerance": tolerance}


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pack")
    p.add_argument("--gwid", type=int, required=True)
    p.add_argument("--epr-year", type=int, required=True)
    p.add_argument("--economy", required=True)
    p.add_argument("--wbl-year", type=int, required=True)
    p.add_argument("--join-year", type=int, required=True)
    p.add_argument("--subsample", required=True)
    p.add_argument("--fin-year", type=int, required=True)
    p.add_argument("--fin-group", required=True)
    p.add_argument("--fin-group2", required=True)
    args = vars(p.parse_args())
    pack = NativePack(args.pop("pack"))
    print(json.dumps(pack.context(**args), ensure_ascii=False, allow_nan=False, indent=2))
