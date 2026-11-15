"""Derived targetless C12 session for the lawful B REFUSE / NO_CHANGE path.

The original BP2P4 consumer requires a C9 CREATE target before it can assemble
a product. B's refusal has no target by contract, so this module does not
fabricate one. It derives a world/C12 representation from the real J refusal
source and the keyed C8/E1 values, attaches the real E expression admission
port, and binds the persisted source and branch lineage to C12/C8 authority.
"""
from __future__ import annotations

import json
from pathlib import Path

from .imports import install
install()
from .lineage import ROOT_BRANCH, create_fork, validate as validate_lineage
from bp4.product import BP4Product
from bp4.world import initial_world
from c8_readonly_consumer import C8ReadOnlyConsumer
from historical_actor_producer import build_life
from r26e.c12_integrity import QualifiedC12Store
from r31j.build import c9_only
from r31j.scenarios import evaluated
from r31e.session import R31ESession
from r30a.first_session import SessionRefusal

GRADE = 'TEST_ONLY_SOURCEFREE_TARGETLESS_C12_NOT_NATIVE'
ROOT_BRANCH = 'first_session'


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


def _sidecar_document(source, c8_binding, variant):
    return {
        'schema': 'SOROK_JOIN_E_TARGETLESS_C12@1',
        'j_source': source,
        'j_c8_state_digest': c8_binding['c8_state_digest'],
        'j_e1_event_hash': c8_binding['e1_event_hash'],
        'c8': dict(c8_binding),
        'variant': variant,
        'target_id': '',
        'native': False,
    }


def _read_c8_source(binding: dict):
    view = C8ReadOnlyConsumer(str(binding['journal_path'])).load()
    event = view.get(binding['occurrence_id'])
    if not event:
        raise ValueError('C8_OCCURRENCE_ABSENT')
    source = (event.get('payload') or {}).get('gm01_pre_c9_source')
    if not isinstance(source, dict):
        raise ValueError('C8_GM01_SOURCE_ABSENT')
    return source, event


def validate_targetless(product, meta: dict, sidecar: dict, branch_id: str) -> dict:
    """Compare sidecar/meta with C12, keyed C8 and actor/receipt identity."""
    checks: dict[str, bool] = {}
    observed: dict = {}
    try:
        source = product.source
        c8_binding = sidecar.get('c8') or {}
        c8_source, c8_event = _read_c8_source(c8_binding)
        rows = [row for row in product.store.episodes(branch_id)
                if row['kind'] == 'GM01_REFUSAL']
        if len(rows) != 1:
            raise ValueError('C12_GM01_REFUSAL_COUNT:' + str(len(rows)))
        body = rows[0].get('body') or {}
        c12_source = body.get('gm01_source')
        seed = product.seed.public()
        expected_map = {
            'TEST_ONLY_R31J_A': seed['actor_a'],
            'TEST_ONLY_R31J_B': seed['actor_b'],
        }
        payload = c8_event.get('payload') or {}
        actor = payload.get('actor') or {}
        other = payload.get('other_actor') or {}
        checks.update({
            'sidecar_matches_c8': source == c8_source,
            'sidecar_matches_c12': source == c12_source,
            'meta_matches_c8': meta.get('j_source') == c8_source,
            'meta_matches_c12': meta.get('j_source') == c12_source,
            'sidecar_matches_meta': sidecar.get('j_source') == meta.get('j_source'),
            'c8_actor_is_seed_a': actor.get('actor_id') == seed.get('actor_a'),
            'c8_other_is_seed_b': other.get('actor_id') == seed.get('actor_b'),
            'source_actor_map': meta.get('source_actor_map') == expected_map,
            'source_b_is_seed_b': source.get('b_actor') == 'TEST_ONLY_R31J_B',
            'source_b_to_is_seed_a': source.get('b_to_actor') == 'TEST_ONLY_R31J_A',
            'meta_c8_matches_sidecar': meta.get('j_c8_state_digest') ==
            c8_binding.get('c8_state_digest'),
            'meta_e1_matches_sidecar': meta.get('j_e1_event_hash') ==
            c8_binding.get('e1_event_hash'),
            'c12_c8_matches_sidecar': body.get('c8_state_digest') ==
            c8_binding.get('c8_state_digest'),
            'c12_e1_matches_sidecar': body.get('e1_event_hash') ==
            c8_binding.get('e1_event_hash'),
            'target_is_absent': meta.get('target_id') == ''
            and body.get('target_id') == ''
            and (sidecar.get('target_id') == ''),
            'native_grants_false': all(
                value is False
                for value in product.seed.custody()['native_grants'].values()),
            'no_native_sidecar': sidecar.get('native') is False,
        })
        observed.update({
            'b_event_hash': source.get('b_event_hash'),
            'b_operation': source.get('b_operation'),
            'b_actor': source.get('b_actor'),
            'b_to_actor': source.get('b_to_actor'),
            'c8_state_digest': c8_binding.get('c8_state_digest'),
            'e1_event_hash': c8_binding.get('e1_event_hash'),
            'source_actor_map': meta.get('source_actor_map'),
            'seed_actors': {'a': seed.get('actor_a'), 'b': seed.get('actor_b')},
        })
    except Exception as exc:  # missing/orphan source is a failed provenance check
        checks['provenance_readable'] = False
        observed['error'] = type(exc).__name__ + ':' + str(exc)
    checks.setdefault('provenance_readable', True)
    return {'ok': all(checks.values()), 'checks': checks, 'observed': observed}


class RefusalProduct(BP4Product):
    """C12/world representation with no C9 target and no C10 target read."""

    def __init__(self, root, *, life, source, c8_binding, variant,
                 write_sidecar=False, branch_id='root', sidecar_document=None):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.source = source
        self.c8_binding = dict(c8_binding)
        self.variant = variant
        self.sidecar = (sidecar_document if sidecar_document is not None
                        else _sidecar_document(source, c8_binding, variant))
        self.sidecar_path = self.root / 'refusal.json'
        if write_sidecar and not self.sidecar_path.exists():
            self.sidecar_path.write_text(
                json.dumps(self.sidecar, indent=2, sort_keys=True) + '\n',
                encoding='utf8')
        self.seed = _RefusalSeed(
            life, source, c8_binding['c8_state_digest'],
            c8_binding['e1_event_hash'])
        self.store = QualifiedC12Store(self.root / 'c12.sqlite')
        self.branch_id = branch_id
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
        c8_binding = {
            'occurrence_id': producer.out9.occurrence_id,
            'journal_path': str(producer.env.journal_path),
            'key_path': str(producer.env.key_path),
            'key_id': producer.env.key_store.key_id,
            'anchor_log': str(producer.env.anchor.log_path),
            'anchor_watermark': str(producer.env.anchor.watermark_path),
            'c8_state_digest': partial['c8_state_digest'],
            'e1_event_hash': partial['e1_event_hash'],
        }
        life = producer.historical_life
        producer.close()
        product = RefusalProduct(
            state_root / 'product', life=life, source=partial['gm01_source'],
            c8_binding=c8_binding, variant=variant, write_sidecar=True)
        try:
            product._append_episode(
                'root', 'A', 'GM01_REFUSAL', product._world('root').clock, {
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
            seed = product.seed.public()
            session.meta.update(
                schema='SOROK_SAME_PERSON_REFUSAL@1',
                grade=GRADE,
                material_performance='refused',
                root_branch_id='root',
                branch_lineage=None,
                target_id='',
                targetless=True,
                j_source_ref='64fec28c374d8f77fb0b412d0c934d798ede03e8',
                e_source_ref='a2760d3687b063513fe0a5b9589c56c998d4ccb5',
                j_source=partial['gm01_source'],
                j_c8_state_digest=partial['c8_state_digest'],
                j_e1_event_hash=partial['e1_event_hash'],
                source_actor_map={
                    'TEST_ONLY_R31J_A': seed['actor_a'],
                    'TEST_ONLY_R31J_B': seed['actor_b'],
                },
                c8=dict(c8_binding),
                c9=partial['c9'],
                variant=variant,
                expression_port='R31E_EXPRESSION_PORT@1',
                actor_model='LIVE_ACTOR_MODEL_NOT_RUN',
            )
            session._save_refusal_meta()
            provenance = validate_targetless(
                product, session.meta, product.sidecar, session.branch_id)
            if not provenance.get('ok'):
                raise SessionRefusal(
                    'J_PROVENANCE_MISMATCH',
                    json.dumps(provenance.get('checks', {}), sort_keys=True))
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
        if not state_root.exists() or not state_root.is_dir() or not path.is_file():
            raise SessionRefusal('SESSION_NOT_FOUND', str(path))
        meta = json.loads(path.read_text())
        if meta.get('schema') != 'SOROK_SAME_PERSON_REFUSAL@1':
            raise SessionRefusal('WRONG_PRODUCT_LINEAGE')
        recorded_state = meta.get('state_root')
        if recorded_state and Path(recorded_state).resolve() != state_root:
            raise SessionRefusal('SESSION_ROOT_MOVED')
        product_root = Path(meta.get('product_root', '')).resolve()
        if product_root != (state_root / 'product').resolve():
            raise SessionRefusal('FOREIGN_PRODUCT_ROOT')
        sidecar_path = product_root / 'refusal.json'
        if not sidecar_path.is_file():
            raise SessionRefusal('J_BINDING_MISSING', str(sidecar_path))
        sidecar = json.loads(sidecar_path.read_text())
        if not sidecar.get('j_source') or not sidecar.get('c8'):
            raise SessionRefusal('J_BINDING_MISSING', 'refusal source/c8 absent')
        branch = meta.get('branch_id')
        life = build_life(meta.get('variant', 'A_REPAIR_LONG'))
        product = RefusalProduct(
            product_root, life=life, source=meta['j_source'],
            c8_binding=sidecar['c8'], variant=meta.get('variant', 'A_REPAIR_LONG'),
            write_sidecar=False, branch_id=branch, sidecar_document=sidecar)
        try:
            if product.source != meta.get('j_source'):
                raise SessionRefusal('J_SOURCE_IDENTITY_CHANGED')
            lineage_result = validate_lineage(meta, branch, product.store)
            if not lineage_result.get('ok'):
                raise SessionRefusal(
                    'BRANCH_LINEAGE_MISMATCH',
                    json.dumps(lineage_result.get('checks', {}), sort_keys=True))
            provenance = validate_targetless(product, meta, sidecar, branch)
            if not provenance.get('ok'):
                raise SessionRefusal(
                    'J_PROVENANCE_MISMATCH',
                    json.dumps(provenance.get('checks', {}), sort_keys=True))
            if not product.c12_verify('root').get('ok') or not product.c12_verify(branch).get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED')
            session = cls(product, state_root, meta)
            if attention and attention != session.meta.get('attention'):
                session.meta['attention'] = attention
                session._save_refusal_meta()
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            return session
        except Exception:
            product.close()
            raise

    def _lineage_result(self):
        return validate_lineage(self.meta, self.branch_id, self.product.store)

    def verify(self):
        result = super().verify()
        root = self.product.c12_verify('root')
        lineage_result = self._lineage_result()
        result['root'] = root
        result['targetless'] = True
        result['lineage'] = lineage_result
        provenance = validate_targetless(
            self.product, self.meta, self.product.sidecar, self.branch_id)
        result['provenance'] = provenance
        result['ok'] = (bool(result.get('ok')) and bool(root.get('ok'))
                        and bool(lineage_result.get('ok'))
                        and bool(provenance.get('ok')))
        return result

    def fork_alt(self, new_branch_id='alt'):
        lineage_result = self._lineage_result()
        if not lineage_result.get('ok'):
            raise SessionRefusal(
                'BRANCH_LINEAGE_MISMATCH',
                json.dumps(lineage_result.get('checks', {}), sort_keys=True))
        parent = self.branch_id
        try:
            fork, lineage = create_fork(
                self.product, parent, new_branch_id,
                self.meta.get('branch_lineage'))
        except Exception as exc:
            code = getattr(exc, 'code', type(exc).__name__)
            raise SessionRefusal('FORK_REFUSED', code + ':' + str(exc)) from exc
        self.branch_id = new_branch_id
        self.meta['branch_id'] = new_branch_id
        self.meta['branch_lineage'] = lineage
        self.product.use(new_branch_id)
        self._save_refusal_meta()
        return fork

    def status(self):
        lineage_result = self._lineage_result()
        if not lineage_result.get('ok'):
            raise SessionRefusal(
                'BRANCH_LINEAGE_MISMATCH',
                json.dumps(lineage_result.get('checks', {}), sort_keys=True))
        result = super().status()
        result['target_id'] = ''
        result['targetless'] = True
        result['c9'] = self.meta.get('c9')
        result['branch_lineage'] = self.meta.get('branch_lineage')
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
