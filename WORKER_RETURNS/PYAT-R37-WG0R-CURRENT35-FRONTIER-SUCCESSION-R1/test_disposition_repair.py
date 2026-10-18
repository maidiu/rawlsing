import csv
import hashlib
from collections import Counter
import pytest
import account_current35 as a
from recover_disposition_payload import recover


def test_exact_recovery_original_hash_and_surviving_shard():
    data,codes=a.decode_dispositions()
    assert data==recover()
    assert len(data)==18276
    assert hashlib.sha256(data).hexdigest()==a.PACK_SHA
    assert all(not b&192 for b in data)
    shard=next((a.ROOT/'sources/repair_original_git').rglob('part-000.csv'))
    reverse={v:int(k) for k,v in codes.items()}
    for row in csv.DictReader(shard.open()):
        byte=reverse[row['use']]+16*(row['hard_fail']=='Y')+32*(row['route_predicate_required']=='Y')
        assert data[int(row['p2_row_ordinal'])]==byte


def test_recovered_rows_and_independent_documented_counts():
    rows,waves,_=a.load()
    assert len(rows)==18276 and len(waves)==35
    assert Counter(r['governed_use'] for r in rows)==dict(SEM=4681,TOP=3667,POS=2904,END=2113,CTX=1675,SCX=1506,ADM=1026,REJ=454,CPC=183,BLK=67)
    assert sum(r['hard_fail'] for r in rows)==10418
    assert sum(r['route_predicate_required'] for r in rows)==4447
    assert not any(r['execution_state']=='DISPOSITION_CARRIER_REQUIRES_EXACT_REPUBLICATION' for r in rows)


@pytest.mark.parametrize('mutation',['payload','p2','code-map','hash-header','byte-length','duplicate'])
def test_repaired_loader_rejects_corrupt_transport(tmp_path,mutation):
    with a.ACTIVE_PACK.open() as f:
        row=next(csv.DictReader(f));keys=list(row)
    if mutation=='payload':row['payload_b64_0']='A'+row['payload_b64_0'][1:]
    elif mutation=='p2':row['p2_sha256']='0'*64
    elif mutation=='code-map':row['use_code_map']=row['use_code_map'].replace('0=SEM','0=ADM')
    elif mutation=='hash-header':row['payload_sha256']='0'*64
    elif mutation=='byte-length':row['payload_bytes']='18275'
    path=tmp_path/'hostile.csv'
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader();w.writerow(row)
        if mutation=='duplicate':w.writerow(row)
    with pytest.raises(ValueError):a.decode_dispositions(pack_path=path)
