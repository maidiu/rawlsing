"""Exact legacy receipt envelope compatibility, not original-data execution."""
import json
from hashlib import sha256
import pytest
from rawlsing_next.pre553_recorded_result_delivery import deliver_recorded_result, markdown, Q103, SRC16, RecordedDeliveryError


def _ref(name):
    return {"kind":"EXACT","object_id":name,"content_hash":sha256(name.encode()).hexdigest()}


def _files(tmp_path, schema):
    source, operation, question = ("SRC04","Q103-OP-RECORDED-RESPONSE-ONLY","q103") if schema == Q103 else ("SRC16","SRC16-RACPRES-RECORDED-RESPONSE-ONLY","racpres")
    release = _ref("release")
    roots={"source":"s","release":"|".join(release[k] for k in ("kind","object_id","content_hash")),"universe":"u","replay":"r"}
    codes=["1","98"] if schema==Q103 else ["1","-98"]
    owner={"source_id":source,"question_id":question,"scope":"recorded only","source_binding":{"saved_i02":roots},"denominator":{"recorded_raw_codes":codes},"interpretation":{codes[0]:["SUBSTANTIVE_RESPONSE","Positive"],codes[1]:["DK"]}}
    def write(name, doc):
        p=tmp_path/name
        p.write_text(json.dumps(doc))
        return p,sha256(p.read_bytes()).hexdigest()
    owner_path,owner_sha256=write("owner.json",owner)
    op={"source_id":source,"owner_decision_sha256":owner_sha256,"authorized_operation":operation,
        "question_ref":_ref(question),"historical_snapshot_ref":_ref("defer"),"allowed_raw_codes":codes,
        "interpretation":[[c,owner["interpretation"][c][0]] for c in codes],
        **{k+"_root":v for k,v in roots.items()}}
    operation_path,operation_sha256=write("operation.json",op)
    value=int(codes[1]) if schema==Q103 else {"typed_response_state":"DK"}
    result={"schema":schema,"owner_decision_sha256":owner_sha256,"positive_counts_accepted":True,
        "missing":{"system_missing":1,"absent":2},"facts":[{"typed_state":"SUPPORTED","raw_denominator_support":4,
        "raw_numerator_support":4,"replay_ref":_ref("query-replay"),"cells":[[1,1,"OBSERVED_POSITIVE"],[value,3,"OBSERVED_POSITIVE"]]}]}
    if schema==Q103:
        # Actual Q103 writer uses json.dump(default=str) on frozen replay.
        result["facts"][0]["replay_ref"]=repr(result["facts"][0]["replay_ref"])
        result.update(query_ref=_ref("query"),predicate_ref=_ref("predicate"),release_refs=[release])
    else:
        result.update(source_id=source,question_ref=op["question_ref"],historical_snapshot_ref=op["historical_snapshot_ref"],
            positive_snapshot_ref=_ref("allow"),scope_kind="OBSERVED_STORED_CODE_FREQUENCIES",asked_eligibility="HELD_NOT_PROVEN",
            substantive_vote_denominator=False,stored_code_bins=[
                {"raw_code":codes[0],"state":"SUBSTANTIVE_RESPONSE","cell":1,"raw_numerator_support":1},
                {"raw_code":codes[1],"state":"DK","cell":value,"raw_numerator_support":3}])
    result_path,result_sha256=write("result.json",result)
    return dict(result_path=result_path,result_sha256=result_sha256,owner_path=owner_path,owner_sha256=owner_sha256,
                operation_path=operation_path,operation_sha256=operation_sha256)


@pytest.mark.parametrize("schema",[Q103,SRC16])
def test_private_delivery_preserves_scope_and_exact_fraction(tmp_path,schema):
    args=_files(tmp_path,schema)
    result=deliver_recorded_result(**args)
    assert result["raw_recorded_denominator"]==4
    assert result["missing_outside_denominator"]=={"system_missing":1,"absent":2}
    assert [x["recorded_fraction"] for x in result["cells"]]==[[1,4],[3,4]]
    assert "75.00%" in markdown(result)
    assert "CURRENT_NOT_REVALIDATED" in result["status"]
    args["result_path"].write_text("{}")
    with pytest.raises(RecordedDeliveryError,match="HASH_MISMATCH"):
        deliver_recorded_result(**args)
