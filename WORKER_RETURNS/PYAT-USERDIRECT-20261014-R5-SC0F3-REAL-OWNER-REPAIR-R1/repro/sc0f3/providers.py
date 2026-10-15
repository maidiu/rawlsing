"""Two distinct lossless physical encodings of a bounded synthetic world."""
import copy
import json
from .common import digest, require
from .fixture_owner import fixture_world


class ProviderOperations:
    def __init__(self, world=None, variant='54_6'):
        self._write_world(copy.deepcopy(fixture_world() if world is None else world))
        self.variant = variant
        self.binding_generation = 0
        self.publication_generation = 0
        self.read_count = 0
        self.revoked_atoms = frozenset()

    @property
    def physical_lineage(self):
        return dict(physical_provider_id=type(self).__name__,
                    physical_storage_locator='TEST_ONLY:'+type(self).__name__,
                    physical_serialization=self.encoding, physical_lineage_blob=self.encoding,
                    nonsemantic_cache_ids=[self.encoding])

    def resolve_world_selection(self, demand):
        w=self._read_world()
        return dict(world=w, demand=copy.deepcopy(demand), provider=self.physical_lineage,
                    selection_state='COMPLETE', binding_generation=self.binding_generation,
                    publication_generation=self.publication_generation, empirical_variant=self.variant)

    def revoked_use(self, selection, atom):
        ceiling=self._read_world()['permission_ceiling']
        require(atom in ceiling['use_atoms'] and atom not in ceiling['revoked_atoms'] and atom not in self.revoked_atoms,
                'DENIED_USE', 'Live '+atom+' revoked or absent')

    def read_values(self, selection, keys):
        self.revoked_use(selection, 'WORLD_READ')
        self.read_count += 1
        live=self._read_world()
        data={**live['values'], **live['routes']}
        require(all(k in data for k in keys), 'REJECT_UNVERIFIABLE_CONSUMER_USE', 'Missing readable value')
        out={k:copy.deepcopy(data[k]) for k in keys}
        return dict(values=out, digest=digest(out))

    def refresh_binding_generation(self):
        self.binding_generation += 1
        w=self._read_world()
        w['generated_binding_echo']['caller_fact']='location-binding-echo-'+str(self.binding_generation)
        self._write_world(w)

    def refresh_publication_generation(self):
        w=self._read_world()
        require(w['source_release_ref']=='fx:release:fixture1', 'NO_CURRENT', 'No further frozen publication successor')
        # Actual source-release/publication boundary, not a counter-only refresh.
        w['source_release_ref']='fx:release:fixture2'
        w['time_axes']['published']='2010-06'
        self._write_world(w)
        self.publication_generation += 1


class ProviderA(ProviderOperations):
    encoding='single-json-object'
    def _write_world(self, world):
        self._json=json.dumps(world, sort_keys=True)
    def _read_world(self):
        return json.loads(self._json)


class ProviderB(ProviderOperations):
    encoding='independent-key-value-tuples'
    def _write_world(self, world):
        self._rows=tuple((k,json.dumps(v,sort_keys=True)) for k,v in sorted(world.items()))
    def _read_world(self):
        return {k:json.loads(v) for k,v in self._rows}
