"""Derived targetless C12 session for the lawful B REFUSE / NO_CHANGE path.

The original BP2P4 consumer requires a C9 CREATE target before it can assemble
a product.  B's refusal has no target by contract, so this module does not
fabricate one.  It derives a world/C12 representation directly from the real
J refusal source and C8/E1 values, attaches the real E expression admission
port, and leaves C10 target semantics explicitly absent.
"""
from __future__ import annotations

import json
from pathlib import Path

from .imports import install
install()
from bp4.product import BP4Product
from bp4.world import initial_world
from r26e.c12_integrity import QualifiedC12Store
from r31j.build import c9_only
from r31j.scenarios import evaluated
from r31e.session import R31ESession
from r30a.first_session import SessionRefusal

GRADE = 'TEST_ONLY_SOURCEFREE_TARGETLESS_C12_NOT_NATIVE'


class _RefusalSeed:
    """Minimal seed surface used by BP4 world/store and E contract code."""

    def __init__(self, life, source, c8_state_digest, e1_event_hash):
        self.life = life
        self.source = source
        self.world = initial_world(life)
        self.world.actor_state['A']['tools_remaining'] = (
            1 if source.get('material_feasible_after') else 0)
        self.c8_state_digest = c8_state_digest
        self.e1_event_hash = e1_event_hash
        self.c9_target_id = ''
        self.c9_state_hash = ''
        self.c9_commit_time = 0
        self.c9_e2_admitted = False

    def custody(self):
        return {
            'schema': 'SOROK_JOIN_E_TARGETLESS_CUSTODY@1',
            'grade': GRADE,
            'native': False,
            'target_id': '',
            'target_record_hash': '',
            'consumed_state_hash': '',
            'c8_state_digest': self.c8_state_digest,
            'e1_event_hash': self.e1_event_hash,
            'c9_target_present': False,
            'native_grants': {
                'actor': False, 'rule': False, 'c8_trust': False,
                'e2': False, 'world': False, 'c11': False, 'c12': False,
                'adp019': False,
            },
        }

    def public(self):
        return {
            'schema': 'BP4_TARGETLESS_SOURCEFREE_SEED@1',
            'actor_a': self.life.a_source.actor_id,
            'actor_b': self.life.b_source.actor_id,
            'source_hashes': [self.life.a_source.source_hash,
                              self.life.b_source.source_hash],
            'c8_state_digest': self.c8_state_digest,
            'e1_event_hash': self.e1_event_hash,
            'c9_target_id': '',
            'native': False,
        }


class RefusalProduct(BP4Product):
    """C12/world representation with no C9 target and no C10 target read."""

    def __init__(self, root, *, life, source, c8_state_digest, e1_event_hash,
                 branch_id='root'):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.source = source
        self.seed = _RefusalSeed(life, source, c8_state_digest, e1_event_hash)
        self.store = QualifiedC12Store(self.root / 'c12.sqlite')
        self.branch_id = branch_id
        sidecar = self.root / 'refusal.json'
        if not sidecar.exists():
            sidecar.write_text(json.dumps({
                'schema': 'SOROK_JOIN_E_TARGETLESS_C12@1',
                'j_source': source,
                'j_c8_state_digest': c8_state_digest,
                'j_e1_event_hash': e1_event_hash,
                'variant': 'A_REPAIR_LONG',
                'target_id': '',
                'native': False,
            }, indent=2, sort_keys=True) + '\n', encoding='utf8')
        self._ensure_root()

    def c12_verify(self, branch_id=None):
        return self.store.verify(branch_id or self.branch_id)

    def joined_source(self):
        return {
            'schema': 'SOROK_JOIN_E_TARGETLESS_SOURCE@1',
            'custody': self.seed.custody(),
            'source': self.source,
            'native': False,
        }

    def close(self):
        self.store.close()


class RefusalSession(R31ESession):
    """E admission over the targetless C12 representation; no C9 target."""

    @classmethod
    def start(cls, state_root, *, attention='focused', variant='A_REPAIR_LONG'):
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root / 'session.json').exists():
            raise SessionRefusal('SESSION_EXISTS__NO_AUTOMATIC_REROLL')
        if (state_root / 'product').exists() or (state_root / 'source').exists():
            raise SessionRefusal('ORPHAN_PRODUCT_ROOT')
        scenario = evaluated(share=False, e2=False)
        partial, producer = c9_only(
            state_root / 'source', gm01=scenario['gm01'],
            case=scenario['case'], variant=variant)
        life = producer.historical_life
        producer.close()
        product = RefusalProduct(
            state_root / 'product', life=life, source=partial['gm01_source'],
            c8_state_digest=partial['c8_state_digest'],
            e1_event_hash=partial['e1_event_hash'])
        try:
            product._append_episode('root', 'A', 'GM01_REFUSAL', product._world('root').clock, {
                'gm01_source': partial['gm01_source'],
                'c8_state_digest': partial['c8_state_digest'],
                'e1_event_hash': partial['e1_event_hash'],
                'c9': partial['c9'],
                'target_id': '',
                'native': False,
            })
            product._checkpoint('root', product._world('root').clock,
                                product._world('root'))
            session = cls._attach_new(product, state_root, scenario='available',
                                      attention=attention, variant=variant)
            session.meta.update(
                schema='SOROK_SAME_PERSON_REFUSAL@1',
                grade=GRADE,
                material_performance='refused',
                target_id='',
                j_source_ref='64fec28c374d8f77fb0b412d0c934d798ede03e8',
                e_source_ref='a2760d3687b063513fe0a5b9589c56c998d4ccb5',
                j_source=partial['gm01_source'],
                j_c8_state_digest=partial['c8_state_digest'],
                j_e1_event_hash=partial['e1_event_hash'],
                c9=partial['c9'],
            )
            session._save_refusal_meta()
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            return session
        except Exception:
            product.close()
            raise

    def _save_refusal_meta(self):
        (self.state_root / 'session.json').write_text(
            json.dumps(self.meta, indent=2, sort_keys=True) + '\n',
            encoding='utf8')

    @classmethod
    def open(cls, state_root, *, attention=None):
        state_root = Path(state_root).resolve()
        path = state_root / 'session.json'
        if not path.is_file():
            raise SessionRefusal('SESSION_NOT_FOUND')
        meta = json.loads(path.read_text())
        if meta.get('schema') != 'SOROK_SAME_PERSON_REFUSAL@1':
            raise SessionRefusal('WRONG_PRODUCT_LINEAGE')
        product_root = (state_root / 'product').resolve()
        if Path(meta.get('product_root', '')).resolve() != product_root:
            raise SessionRefusal('FOREIGN_PRODUCT_ROOT')
        sidecar = json.loads((product_root / 'refusal.json').read_text()) \
            if (product_root / 'refusal.json').is_file() else {}
        if sidecar.get('j_source') != meta.get('j_source'):
            raise SessionRefusal('J_SOURCE_IDENTITY_CHANGED')
        # A targetless root has no BP2P4 target; reconstruct only the C12/world.
        from historical_actor_producer import build_life
        life = build_life(meta.get('variant', 'A_REPAIR_LONG'))
        product = RefusalProduct(
            product_root, life=life, source=meta['j_source'],
            c8_state_digest=meta['j_c8_state_digest'],
            e1_event_hash=meta['j_e1_event_hash'])
        try:
            if attention:
                meta['attention'] = attention
                (state_root / 'session.json').write_text(
                    json.dumps(meta, indent=2, sort_keys=True) + '\n',
                    encoding='utf8')
            session = cls(product, state_root, meta)
            if not session.verify().get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED')
            return session
        except Exception:
            product.close()
            raise

    def verify(self):
        result = super().verify()
        result['targetless'] = True
        return result

    def status(self):
        result = super().status()
        result['target_id'] = ''
        result['targetless'] = True
        result['c9'] = self.meta.get('c9')
        return result


def probe_refusal(state_root, *, variant='A_REPAIR_LONG'):
    """Build the typed refusal receipt and targetless C12 representation."""
    state_root = Path(state_root).resolve()
    state_root.mkdir(parents=True, exist_ok=True)
    scenario = evaluated(share=False, e2=False)
    partial, producer = c9_only(
        state_root / 'source', gm01=scenario['gm01'],
        case=scenario['case'], variant=variant)
    producer.close()
    session = RefusalSession.start(state_root / 'session', variant=variant)
    try:
        return {
            'schema': 'SOROK_JOIN_E_REFUSAL_PROBE@1',
            'status': 'HOLD',
            'code': 'JOIN_REFUSAL_NO_TARGET__TARGETLESS_C12_DERIVED',
            'source': partial['gm01_source'],
            'c8_state_digest': partial['c8_state_digest'],
            'e1_event_hash': partial['e1_event_hash'],
            'c9': partial['c9'],
            'target_id': '',
            'c12': session.verify(),
            'session': session.status(),
            'owner_contract': {
                'request': ('The original BP2P4 consumer requires a committed C9 '
                            'CREATE target. A targetless C12 representation now '
                            'carries the real REFUSE/NO_CHANGE source without a '
                            'fabricated target; C10 target semantics remain absent.'),
                'required_decision': ('Accept the derived targetless C12 for the '
                                      'refusal path, or provide a native C10/C12 '
                                      'no-target contract.'),
                'owner': 'BP2P4/C9 consumer owner with C12/C10 owner',
                'unaffected_paths': ('share+E2, share+omit, E expression, '
                                     'attention, privacy, cold positive'),
            },
        }
    finally:
        session.close()
