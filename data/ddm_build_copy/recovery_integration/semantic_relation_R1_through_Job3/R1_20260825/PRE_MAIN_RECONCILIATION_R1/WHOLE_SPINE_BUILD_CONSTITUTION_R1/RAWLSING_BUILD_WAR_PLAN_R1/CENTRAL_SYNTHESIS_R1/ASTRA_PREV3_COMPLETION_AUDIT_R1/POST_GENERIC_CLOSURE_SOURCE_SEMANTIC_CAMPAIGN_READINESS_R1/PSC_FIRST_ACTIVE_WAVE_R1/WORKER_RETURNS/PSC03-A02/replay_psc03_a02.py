#!/usr/bin/env python3
import argparse,base64,csv,hashlib,io,pathlib,zlib
R=pathlib.Path(__file__).resolve().parent
transport=R/"01_EXACT_122_ADJUDICATION_LEDGER.csv.zlib.b64"
raw=zlib.decompress(base64.b64decode(transport.read_bytes().strip()))
assert hashlib.sha256(raw).hexdigest()=="07793b862bca9002b169bbef3f4c68b33b8af5f5f930295b93962dae63f92cd2"
rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
assert len(rows)==122
assert len({r["question_implementation_id"] for r in rows})==122
assert {r["disposition"] for r in rows}=={"CURRENT_AUTHORITY_ALREADY_RESOLVES"}
qid_hash=hashlib.sha256(("\n".join(sorted(r["question_implementation_id"] for r in rows))+"\n").encode()).hexdigest()
assert qid_hash=="aab2ebac5d7d4f833384ebad12468a0a2d7b21778a6baa0a0028951ef56f1ec0"
ap=argparse.ArgumentParser()
ap.add_argument("--emit-csv")
ns=ap.parse_args()
if ns.emit_csv:
    pathlib.Path(ns.emit_csv).write_bytes(raw)
print("PASS",len(rows),hashlib.sha256(raw).hexdigest(),qid_hash)
