"""Sourcefree J product connected to E admission without a second product root."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J = ROOT / 'vendor' / 'j'
E = ROOT / 'vendor' / 'e'
for path in reversed((J, J/'r29m/source', J/'candidate', J/'candidate/vendor/bp2',
                      J/'candidate/vendor/bp4', J/'r29p', J/'r26e', J/'n1')):
    sys.path.insert(0, str(path))
from r31j.build import product as build_product
from r31j.product import R31JProduct
from r31j.scenarios import evaluated
sys.path.insert(0, str(E))
from r31e.session import R31ESession
from r30a.first_session import SessionRefusal


class JoinedSession(R31ESession):
    @classmethod
    def start(cls, state_root, *, perform='e2', attention='focused',
              variant='A_REPAIR_LONG'):
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root/'session.json').exists():
            raise SessionRefusal('SESSION_EXISTS__NO_AUTOMATIC_REROLL')
        if perform not in ('e2', 'omit'):
            raise SessionRefusal('UNKNOWN_PERFORMANCE')
        scenario = evaluated(share=True, e2=perform == 'e2')
        product, built, producer = build_product(
            state_root, gm01=scenario['gm01'], case=scenario['case'], variant=variant)
        producer.close()
        try:
            if perform == 'e2':
                product.material_inspect()
            else:
                product.record_omission()
            session = cls._attach_new(product, state_root, scenario='available',
                                      attention=attention, variant=variant)
            session.meta.update(schema='SOROK_SAME_PERSON_JOIN@1',
                                grade='TEST_ONLY_SOURCEFREE_NOT_NATIVE',
                                material_performance=perform,
                                j_source_ref='64fec28c374d8f77fb0b412d0c934d798ede03e8',
                                e_source_ref='a2760d3687b063513fe0a5b9589c56c998d4ccb5')
            session._save_join_meta()
            return session
        except Exception:
            product.close()
            raise

    def _save_join_meta(self):
        (self.state_root/'session.json').write_text(json.dumps(self.meta, indent=2)+'\n')

    @classmethod
    def open(cls, state_root, *, attention=None):
        state_root = Path(state_root).resolve()
        meta = json.loads((state_root/'session.json').read_text())
        if meta.get('schema') != 'SOROK_SAME_PERSON_JOIN@1':
            raise SessionRefusal('WRONG_PRODUCT_LINEAGE')
        product = R31JProduct.reopen(Path(meta['product_root']), branch_id=meta['branch_id'])
        try:
            session = cls(product, state_root, meta)
            if attention:
                session.meta['attention'] = attention
                session._save_join_meta()
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            return session
        except Exception:
            product.close()
            raise
