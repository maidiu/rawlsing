"""Independent numeric-country mutation / respondent joint oracle.
Sourcefree generated SAV only; no scientific authority or original source.
Pinned production source f5e9c9a03ccddb5bdfab2114c5f5f551002914f6.
"""
from collections import Counter
from dataclasses import replace
from pathlib import Path
import hashlib
import tempfile
import unittest
import pandas as pd
import pyreadstat
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_country_numeric_carrier import build_country, CountryReader
from rawlsing_next.pre553_source_backed_c11_facade import (
    _PackedRoutingFacts, PhysicalSlot, ExactPhysicalCellStream,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, RoutingEligibilityFact
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _query_authority, _branch_predicate, _query, _cell_map, _predicate, _response_leaf
)

class IndependentCountryMutation(unittest.TestCase):
    def test_same_marginals_different_joints_weight_routing_and_restore(self):
        fx = _fixture("review1354-mutants")
        p0 = fx["projection"]
        qa = _query_authority("review1354-mutants")
        pred = _branch_predicate(fx, qa)
        forward = _predicate(fx, qa, _response_leaf(fx,qa,"X","1"), tag="review1354-forward")
        reverse = _predicate(fx, qa, _response_leaf(fx,qa,"Y","1"), tag="review1354-reverse")
        qs = (
            (_query(fx,qa,pred,("X","Y"),tag="review1354-joint"),pred),
            (_query(fx,qa,pred,("Y",),tag="review1354-raw"),pred),
            (_query(fx,qa,pred,("Y",),measure="GOVERNED_WEIGHTED",tag="review1354-weight"),pred),
            (_query(fx,qa,forward,("Y",),tag="review1354-forward"),forward),
            (_query(fx,qa,reverse,("X",),tag="review1354-reverse"),reverse),
        )
        registry = AuthorityRegistry((*fx["authorities"],qa))
        base = pd.DataFrame({
            "X":["1","0","0"],"Y":["1","0","1"],"M":["A","A","A"],
            "O":["AB","BA","AB"],"R":["XY","XZ","XY"],"G":["A","A","A"],
            "W":[2.,1.,3.],"unmapped":[0.125,-0.0,9.75],
        })
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/"source.sav"
            pyreadstat.write_sav(base,str(src))
            baseline_bytes=src.read_bytes()
            def run(label,frame,*,admit_third=False,restore=False):
                if restore:
                    src.write_bytes(baseline_bytes)
                else:
                    pyreadstat.write_sav(frame,str(src))
                sha=hashlib.sha256(src.read_bytes()).hexdigest()
                path=root/(label+".sqlite")
                with decode_sav(src,expected_source_sha256=sha) as inc:
                    ords={v.name:v.ordinal for v in inc.variables}
                    def slots(items):
                        return tuple(replace(x,slot=PhysicalSlot(ords[x.slot.name],x.slot.name)) for x in items)
                    routes=[]
                    for r in p0.routing:
                        if (admit_third and r.scoped_respondent_ref["object_id"]==fx["respondents"]["R3"].ref.object_id
                                and r.question_or_target_ref["object_id"]==fx["qrefs"]["Y"].object_id):
                            doc=r.as_dict()
                            fields=dict(doc["semantic_fields"])
                            fields.update(applicability_state="ELIGIBLE_APPLICABLE",routing_state="ELIGIBLE_APPLICABLE")
                            r=RoutingEligibilityFact(typed_state="ELIGIBLE_APPLICABLE",
                                authority_snapshot_refs=r.authority_snapshot_refs,dependency_refs=r.dependency_refs,
                                producer_replay_locator_or_reference_root=r.producer_replay_locator_or_reference_root,**fields)
                        routes.append(r)
                    projection=replace(p0,expected_source_sha256=sha,
                        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT",p0.source_snapshot_retention_ref.object_id,sha),
                        response_slots=slots(p0.response_slots),coordinate_slots=slots(p0.coordinate_slots),
                        weight_slots=slots(p0.weight_slots),routing=tuple(routes))
                    cells=tuple(inc.iter_cells())
                    rec=build_country(inc,country_variable="G",country_value="A",output=path,
                                      require_current=lambda:True,block_rows=2)
                direct=build_validated_source_backed_c11_release_from_stream(
                    ExactPhysicalCellStream(sha,3,lambda:iter(cells)),projection)
                packed=replace(projection,routing=_PackedRoutingFacts(iter(routes)))
                with CountryReader(path,rec,require_current=lambda:True) as reader:
                    self.assertEqual(list(reader.matching_rows({"unmapped":0.125})),[1])
                    repo,rel=reader.native_repository(packed,current_authorities=(*fx["authorities"],qa))
                    self.assertEqual(rel.release_ref,direct.release_ref)
                    self.assertEqual(rel.replay_manifest.ref,direct.replay_manifest.ref)
                    out=[]
                    for q,condition in qs:
                        def evaluate(repos,r):
                            return execute_empirical_query(repository=repos,query=q,predicate=condition,
                                authority_registry=registry,release_refs=(r.release_ref,))
                        x=evaluate(repo,rel)
                        y=evaluate(C11Repository((direct,)),direct)
                        self.assertEqual(x,y)
                        out.append(x.facts[0])
                    return rel.release_ref,rel.replay_manifest.ref,tuple(out)
            original=run("base",base,restore=True)
            flipped=base.copy(); flipped.loc[0,"Y"]="0"; flipped.loc[1,"Y"]="1"
            alternate=run("flipped",flipped)
            heavy=base.copy(); heavy.loc[0,"W"]=5.
            weighted=run("weight",heavy)
            routed=run("routing",base,admit_third=True,restore=True)
            restored=run("restore",base,restore=True)
            self.assertEqual(original,restored)
            a,b=original[2],alternate[2]
            # Independent counts over actually eligible rows, not a second I03 implementation.
            for frame,facts in ((base,a),(flipped,b)):
                want=Counter(zip(frame.X[:2],frame.Y[:2]))
                self.assertEqual(facts[0].raw_denominator_support,2)
                self.assertEqual({k:v["raw_numerator_support"] for k,v in _cell_map(facts[0]).items()},
                                 {(i,j):want[(i,j)] for i in ("0","1") for j in ("0","1")})
            self.assertNotEqual(_cell_map(a[0]),_cell_map(b[0]))
            self.assertEqual({k:v["raw_numerator_support"] for k,v in _cell_map(a[1]).items()},
                             {k:v["raw_numerator_support"] for k,v in _cell_map(b[1]).items()})
            self.assertEqual(a[2].weighted_denominator_support_if_authorized,{"$exact_fraction":[3,1]})
            self.assertEqual(weighted[2][2].weighted_denominator_support_if_authorized,{"$exact_fraction":[6,1]})
            self.assertEqual(routed[2][1].raw_denominator_support,3)
            print("INDEPENDENT_MUTATION_ORACLE source/weight/routing/restore, same marginal different joint PASS")

if __name__=="__main__":
    unittest.main()
