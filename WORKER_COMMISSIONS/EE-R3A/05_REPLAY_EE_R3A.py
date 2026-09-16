#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, json, pathlib, zlib
from collections import Counter
from rawlsing_next import n04_r2_whole_corpus_t03_release as n04r2

ROOT = pathlib.Path(__file__).resolve().parent
N04_R3_COMMIT = "8e0266703bbf3b060abcd6fbe53c7ef6c49062c5"
STATUS_VECTOR_PATH = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N04-R3/03_CURRENT_18276_BINDING_STATUS_VECTOR.zlib.b64"
EXPECTED_LEDGER_SHA256 = "0ac4cd90c19c859438ec12ddfa69c37e9b9c85607884e0f4ea93bc6b52493723"
EXPECTED_STATUS_RAW_SHA256 = "f3bb9f06508f7eb26d1ee01e6bc865377637da34f5a60b4118006cc5d8a8d283"
EXPECTED_STATUS_ENCODED_SHA256 = "8241edb2bf043105e0eae12dfa8dd312ff14ca09d37141467834529404c161d7"
EXPECTED_STATUS_COUNTS = {1: 41, 2: 22, 3: 18012, 4: 159, 5: 42}
EXPECTED_MASK_RAW_SHA256 = "58f5fc12b968fad266e75e17be9f21d727d684535d0a78bb5e5ff5196d1c112e"
EXPECTED_MASK_ENCODED_SHA256 = "6636108094f8a67d902ccfe5390cf8b3670da09d19f5c84877cbe8cb4730b012"
EXPECTED_ORDINAL_SHA256 = "769fc7c501f60797dd91aae184517edd76b50740db66f9340b6d42884ff3e021"
EXPECTED_ID_STREAM_SHA256 = "582dc702d1c974b5e57931c2462468523cf73ddf997c00f05dc5e5c0e95ba7b0"
EXPECTED_REPLAY_IDENTITY = "f820cf4f698709c92303bb39ea01d7cbb88ddf55fe6a84060da36c1d54a346f6"

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def build() -> dict:
    ledger, _v, summary = n04r2._load_n03_r2_replay()
    assert len(ledger) == 18276 and summary["rows"] == 18276 and summary["unique_ids"] == 18276
    assert summary["ledger_canonical_jsonl_sha256"] == EXPECTED_LEDGER_SHA256
    ledger_ids = [r["question_implementation_id"] for r in ledger]
    assert len(set(ledger_ids)) == 18276

    enc = n04r2._git_bytes(N04_R3_COMMIT, STATUS_VECTOR_PATH).strip()
    assert len(enc) == 572 and sha(enc) == EXPECTED_STATUS_ENCODED_SHA256
    status = zlib.decompress(base64.b64decode(enc, validate=True))
    assert len(status) == 18276 and sha(status) == EXPECTED_STATUS_RAW_SHA256
    assert dict(sorted(Counter(status).items())) == EXPECTED_STATUS_COUNTS

    mask = bytes(1 if code == 3 else 0 for code in status)
    assert sum(mask) == 18012 and sha(mask) == EXPECTED_MASK_RAW_SHA256
    mask_file = (ROOT / "03_SELECTED_18012_MASK.zlib.b64").read_bytes().strip()
    assert sha(mask_file) == EXPECTED_MASK_ENCODED_SHA256
    assert zlib.decompress(base64.b64decode(mask_file, validate=True)) == mask

    ordc = json.loads((ROOT / "04_SELECTED_18012_ORDINALS_COMPLEMENT.json").read_text())
    excluded = set(ordc["excluded_ordinals_1_based"])
    ordinals = [i for i in range(1, 18277) if i not in excluded]
    assert len(ordinals) == 18012
    ordinal_stream = "".join(f"{i}\n" for i in ordinals).encode("ascii")
    assert len(ordinal_stream) == 97135 and sha(ordinal_stream) == EXPECTED_ORDINAL_SHA256
    assert ordinals == [i + 1 for i, bit in enumerate(mask) if bit]

    selected_ids = [ledger_ids[i - 1] for i in ordinals]
    id_stream = "".join(qid + "\n" for qid in selected_ids).encode("ascii")
    assert len(id_stream) == 756504 and sha(id_stream) == EXPECTED_ID_STREAM_SHA256
    contract = json.loads((ROOT / "02_SELECTED_18012_ID_SELECTOR_CONTRACT.json").read_text())
    assert contract["selection"]["selected_count"] == 18012
    assert contract["selection"]["selected_id_stream_sha256"] == EXPECTED_ID_STREAM_SHA256

    identity_material = {
      "authority": {
        "canonical_ledger": {"authority_commit":"3eaf9918e66b9d4bbc3a1c12598baca20c9d594d","rows":18276,"unique_ids":18276,"canonical_jsonl_sha256":EXPECTED_LEDGER_SHA256,"row_order":"ACCEPTED_N01_R2_DETERMINISTIC_CARRIER_REPLAY_ORDER__NO_SORTING"},
        "status_vector": {"authority_commit":N04_R3_COMMIT,"raw_bytes":18276,"raw_sha256":EXPECTED_STATUS_RAW_SHA256,"encoded_stripped_bytes":572,"encoded_stripped_sha256":EXPECTED_STATUS_ENCODED_SHA256},
        "selection_rule":"status_code == 3"
      },
      "outputs": {
        "selected_count":18012,
        "mask":{"raw_bytes":18276,"raw_sha256":EXPECTED_MASK_RAW_SHA256,"encoding":"zlib level 9 then RFC4648 base64, no whitespace","zlib_bytes":378,"zlib_sha256":"7860a2d8a771dc6d20f521f939cb5d91f6875d9b50e8456ada5eed0e3354ef18","encoded_bytes":504,"encoded_sha256":EXPECTED_MASK_ENCODED_SHA256},
        "one_based_ordinal_stream":{"raw_format":"ASCII decimal ordinal + LF; canonical ledger order","raw_bytes":97135,"raw_sha256":EXPECTED_ORDINAL_SHA256,"encoding":"LOSSLESS_COMPLEMENT_CARRIER","excluded_count":264},
        "id_selector_carrier":{"format":"CANONICAL_LEDGER_PLUS_EXACT_SELECTED_ORDINALS","blocks":18012,"reconstructed_id_stream_format":"full question_implementation_id + LF in canonical ledger order","reconstructed_id_stream_bytes":756504,"reconstructed_id_stream_sha256":EXPECTED_ID_STREAM_SHA256}
      }
    }
    replay_identity = sha(json.dumps(identity_material, sort_keys=True, separators=(",", ":")).encode())
    assert replay_identity == EXPECTED_REPLAY_IDENTITY
    return {"status":"PASS","selected_count":18012,"replay_identity":replay_identity}

def main():
    a=build(); b=build(); assert a==b
    print(json.dumps({"schema":"RAWLSING_EE_R3A_INDEPENDENT_REPLAY@1.0.0","status":"PASS","first_run_identity":a["replay_identity"],"second_run_identity":b["replay_identity"],"identical":True,"selected_count":18012}, indent=2, sort_keys=True))
if __name__ == "__main__": main()
