"""Sourcefree J product connected to E admission without a second product root."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J = ROOT / 'vendor' / 'j'
E = ROOT / 'vendor' / 'e'
for path in reversed((J, J/'r29m/source', J/'candidate', J/'candidate/vendor/bp2',
                      J/'candidate/vendor/bp4', J/'r29p', J/'r26e', J/'n1')):
    sys.path.insert(0, str(path))
from r31j.build import c9_only, product as build_product
from r31j.scenarios import evaluated
sys.path.insert(0, str(E))
from r31e.session import R31ESession
from r30a.first_session import SessionRefusal
from .closure import audit_loaded, source_manifest_sha256
from .readonly import ReadOnlyR31JProduct


class JoinedSession(R31ESession):
    """One persistent same-person session over the J product and E admission."""

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
            state_root, gm01=scenario['gm01'], case=scenario['case'],
            variant=variant)
        producer.close()
        try:
            if perform == 'e2':
                product.material_inspect()
            else:
                product.record_omission()
            root_verify = product.c12_verify('root')
            if not root_verify.get('ok'):
                raise SessionRefusal('ROOT_C12_VERIFY_FAILED',
                                     json.dumps(root_verify.get('errors', [])))
            source = dict(product.source)
            if source.get('b_operation') != 'SHARE_TOOL' or not source.get('b_performed'):
                raise SessionRefusal('J_SOURCE_NOT_POSITIVE', json.dumps(source, sort_keys=True))
            session = cls._attach_new(product, state_root, scenario='available',
                                      attention=attention, variant=variant)
            session.meta.update(
                schema='SOROK_SAME_PERSON_JOIN@1',
                grade='TEST_ONLY_SOURCEFREE_NOT_NATIVE',
                material_performance=perform,
                root_branch_id='root',
                j_source_ref='64fec28c374d8f77fb0b412d0c934d798ede03e8',
                e_source_ref='a2760d3687b063513fe0a5b9589c56c998d4ccb5',
                j_source=source,
                j_c8_state_digest=built['c8_state_digest'],
                j_e1_event_hash=built['e1_event_hash'],
                j_target_id=built['target_id'],
                source_manifest_sha256=source_manifest_sha256(),
                expression_port='R31E_EXPRESSION_PORT@1',
                actor_model='LIVE_ACTOR_MODEL_NOT_RUN',
            )
            session._save_join_meta()
            closure = audit_loaded()
            if not closure.get('ok'):
                raise SessionRefusal('IMPORT_CLOSURE_INVALID',
                                     ';'.join(closure.get('problems', [])))
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            return session
        except Exception:
            product.close()
            raise

    def _save_join_meta(self):
        (self.state_root/'session.json').write_text(
            json.dumps(self.meta, indent=2, sort_keys=True) + '\n',
            encoding='utf8')

    @classmethod
    def open(cls, state_root, *, attention=None):
        state_root = Path(state_root).resolve()
        meta = json.loads((state_root/'session.json').read_text())
        if meta.get('schema') != 'SOROK_SAME_PERSON_JOIN@1':
            raise SessionRefusal('WRONG_PRODUCT_LINEAGE')
        if 'j_source' not in meta:
            raise SessionRefusal('JOIN_META_INCOMPLETE__J_SOURCE_MISSING')
        try:
            product = ReadOnlyR31JProduct.reopen(
                Path(meta['product_root']), branch_id=meta['branch_id'])
        except Exception as exc:
            raise SessionRefusal('COLD_REOPEN_REFUSED',
                                 type(exc).__name__ + ':' + str(exc)) from exc
        try:
            if product.source != meta.get('j_source'):
                raise SessionRefusal('J_SOURCE_IDENTITY_CHANGED')
            root_verify = product.c12_verify('root')
            if not root_verify.get('ok'):
                raise SessionRefusal('ROOT_C12_VERIFY_FAILED',
                                     json.dumps(root_verify.get('errors', [])))
            branch_verify = product.c12_verify(meta['branch_id'])
            if not branch_verify.get('ok'):
                raise SessionRefusal('BRANCH_C12_VERIFY_FAILED',
                                     json.dumps(branch_verify.get('errors', [])))
            session = cls(product, state_root, meta)
            if attention and attention != session.meta.get('attention'):
                session.meta['attention'] = attention
                session._save_join_meta()
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            closure = audit_loaded()
            if not closure.get('ok'):
                raise SessionRefusal('IMPORT_CLOSURE_INVALID',
                                     ';'.join(closure.get('problems', [])))
            return session
        except Exception:
            product.close()
            raise

    @classmethod
    def probe_refusal(cls, state_root, *, variant='A_REPAIR_LONG'):
        """Return the typed no-target boundary; never fabricate a C9 target."""
        state_root = Path(state_root).resolve()
        root = state_root / 'refusal'
        root.mkdir(parents=True, exist_ok=True)
        scenario = evaluated(share=False, e2=False)
        partial, producer = c9_only(
            root, gm01=scenario['gm01'], case=scenario['case'], variant=variant)
        producer.close()
        return {
            'schema': 'SOROK_JOIN_E_REFUSAL_PROBE@1',
            'status': 'HOLD',
            'code': 'JOIN_REFUSAL_NO_TARGET__OWNER_CONTRACT_REQUIRED',
            'source': partial['gm01_source'],
            'c8_state_digest': partial['c8_state_digest'],
            'e1_event_hash': partial['e1_event_hash'],
            'c9': partial['c9'],
            'target_id': '',
            'owner_contract': {
                'request': ('The original BP2P4 consumer requires a committed C9 '
                            'CREATE target before it can assemble a product; the '
                            'E first-neighbor session requires a product root.'),
                'required_decision': ('Provide a lawful no-target C10/C12 '
                                      'representation, or accept this typed HOLD.'),
                'owner': 'BP2P4/C9 consumer owner with C12/C10 owner',
                'unaffected_paths': ('share+E2, share+omit, E expression, '
                                     'attention, privacy, cold positive'),
            },
        }

    def verify(self) -> dict:
        result = super().verify()
        root = self.product.c12_verify('root')
        result['root'] = root
        result['ok'] = bool(result.get('ok')) and bool(root.get('ok'))
        return result

    def fork_alt(self, new_branch_id='alt'):
        result = self.product.fork(new_branch_id)
        self.branch_id = new_branch_id
        self.meta['branch_id'] = new_branch_id
        self.product.use(new_branch_id)
        self._save_join_meta()
        return result

    def status(self) -> dict:
        result = super().status()
        result['j_source_ref'] = self.meta.get('j_source_ref')
        result['e_source_ref'] = self.meta.get('e_source_ref')
        result['j_target_id'] = self.meta.get('j_target_id')
        result['root_branch_id'] = self.meta.get('root_branch_id')
        result['material_performance'] = self.meta.get('material_performance')
        return result
