"""Private sourcefree country I02 response-header retention.

Not a body archive, evaluator, authority or self-certifying cache. The operator
must retain the producer pin independently of this artifact. A cold reader
authenticates the exact bytes BEFORE parsing, binds current facade identity,
rebuilds the remaining I02 sections and compares the exact prior release.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
from io import BytesIO
import gzip
import json
import os
import stat
import struct
import tempfile

from .pre553_empirical_objects import (
    ExactRef, canonical_json, _freeze_semantic_descendants,
)
from ._pre553_c11_execution_view import (
    _CountryEventHeader, _compact_identity,
    _COUNTRY_OCCURRENCE_PREFIX, _COUNTRY_GROUP_PREFIX,
)

SCHEMA_V1="PYAT_COUNTRY_PREPARED_HEADERS@1"
SCHEMA="PYAT_COUNTRY_PREPARED_HEADERS@2"
# Three independent SHA256 identities, six uint32 locators/dictionary
# indices and one dependency-count byte. Neither digest is regenerated
# from another, and arbitrary/noncompact headers retain the JSON path.
_BINARY_HEADER=struct.Struct("<32s32s32s6IB")
_U32=struct.Struct("<I")
MAX_COMPRESSED=128*1024**2
MAX_EXPANDED=512*1024**2
MAX_LINE=8*1024**2
# Invalidate across changes to this exact producer/validation representation.
_OWNERS=("_pre553_country_preparation.py","pre553_country_numeric_carrier.py",
         "pre553_source_backed_c11_facade.py","pre553_c11_ingest.py",
         "pre553_c11_integrity.py","pre553_empirical_authority.py",
         "pre553_empirical_objects.py","_pre553_c11_execution_view.py",
         "pre553_r5_codec.py","pre553_physical_decoder.py","pre553_c11_repository.py")

def _error(message):
    from .pre553_country_numeric_carrier import CountryCarrierError
    return CountryCarrierError("country preparation: "+message)

def _abi():
    base=Path(__file__).parent
    return sha256(canonical_json([(name,sha256((base/name).read_bytes()).hexdigest())
                                  for name in _OWNERS]).encode()).hexdigest()

def _key(key):
    return canonical_json(asdict(key))

def _release(release):
    return canonical_json({
        "release":release.release_ref.as_dict(),
        "replay":release.replay_manifest.ref.as_dict(),
        "source":release.source_artifact_ref.as_dict(),
        "source_manifest":release.source_release_manifest_hash,
        "semantic_release":release.semantic_release_hash,
    })

@dataclass(frozen=True)
class CountryPreparationPin:
    artifact_sha256: str
    artifact_bytes: int
    facade_key: str
    release_identity: str
    owner_abi: str

    def __post_init__(self):
        for value in (self.artifact_sha256,self.owner_abi):
            if type(value) is not str or len(value)!=64 or any(c not in "0123456789abcdef" for c in value):
                raise _error("invalid exact pin digest")
        if type(self.artifact_bytes) is not int or not 0<self.artifact_bytes<=MAX_COMPRESSED:
            raise _error("invalid pinned artifact extent")
        if any(type(x) is not str or not x for x in (self.facade_key,self.release_identity)):
            raise _error("invalid external preparation binding")

def _read_pinned(path,pin):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as file:
        info=os.fstat(file.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid()
                or info.st_mode&0o077 or info.st_size!=pin.artifact_bytes):
            raise _error("private file or pinned extent mismatch")
        data=file.read(pin.artifact_bytes+1)
    if len(data)!=pin.artifact_bytes or sha256(data).hexdigest()!=pin.artifact_sha256:
        raise _error("external artifact digest mismatch")
    return data

def _encode_headers(out,headers,key,*,legacy=False):
    total=0
    def emit(raw):
        nonlocal total
        total+=len(raw)
        if len(raw)>MAX_LINE or total>MAX_EXPANDED:
            raise _error("expanded preparation cap")
        out.write(raw)
    def line(value):
        emit((canonical_json(value)+"\n").encode())
    line([SCHEMA_V1 if legacy else SCHEMA,key,len(headers)])
    # Compact records refer to already emitted shared payload and reference
    # dictionaries. No expanded response body, per-event selector object,
    # or repeated long question/respondent IDs retained on disk.
    refs={}; payloads={}
    def ref_code(ref):
        k=ref.key
        if k not in refs:
            refs[k]=len(refs)
            line(["r",ref.kind,ref.object_id,ref.content_hash])
        return refs[k]
    for header in headers:
        if type(header) is not _CountryEventHeader:
            raise _error("unsupported event header")
        pkey=tuple(id(x) for x in header.payload)
        if pkey not in payloads:
            payloads[pkey]=len(payloads)
            line(["p",header.payload])
        u=ref_code(header.empirical_universe_ref)
        respondent=ref_code(header.scoped_respondent_ref)
        deps=[ref_code(x) for x in header.dependency_refs]
        event=header.event_identity
        occ=header.occurrence_identity
        group=header.group_identity
        coords=header.source_coordinates
        nums=(payloads[pkey],u,respondent,*coords)
        # Shared dictionary rows are still exact canonical JSON. The
        # per-occurrence high-entropy plane is binary instead of hex text.
        # Only the canonical compact identity form takes this fast path.
        if (not legacy and all(type(x) is bytes and len(x)==32 for x in (event,occ,group))
                and type(coords) is tuple and len(coords)==3 and len(deps)<=255
                and all(type(x) is int and 0<=x<2**32 for x in (*nums,*deps))):
            emit(b"H"+_BINARY_HEADER.pack(event,occ,group,*nums,len(deps))
                 +b"".join(_U32.pack(i) for i in deps))
        else:
            line(["h",event.hex() if type(event) is bytes else list(event),
                  header.response_event_id_or_deterministic_index,
                  header.event_group_id,payloads[pkey],u,respondent,deps,coords])
    line(["end",len(headers)])

def _decode_headers(data,key):
    refs=[]; payloads=[]; headers=[]; total=0
    with gzip.GzipFile(fileobj=BytesIO(data),mode="rb") as stream:
        def account(raw):
            nonlocal total
            total+=len(raw)
            if len(raw)>MAX_LINE or total>MAX_EXPANDED:
                raise _error("expanded preparation cap")
            return raw
        def exact(n):
            raw=account(stream.read(n))
            if len(raw)!=n:
                raise _error("truncated binary preparation")
            return raw
        def at(items,i):
            if type(i) is not int or not 0<=i<len(items):
                raise _error("invalid preparation dictionary index")
            return items[i]
        start=json.loads(account(stream.readline(MAX_LINE+1)))
        if (type(start) is not list or len(start)!=3 or start[0] not in (SCHEMA,SCHEMA_V1)
                or start[1]!=key or type(start[2]) is not int or start[2]<1):
            raise _error("preparation schema/binding mismatch")
        count=start[2]
        while True:
            lead=account(stream.read(1))
            if lead==b"H" and start[0]==SCHEMA:
                if len(headers)>=count:
                    raise _error("preparation census overflow")
                event,occ,group,p,u,respondent,r,s,o,n=_BINARY_HEADER.unpack(exact(_BINARY_HEADER.size))
                deps=tuple(at(refs,i) for i, in struct.iter_unpack("<I",exact(4*n)))
                headers.append(_CountryEventHeader(event,occ,at(payloads,p),
                    at(refs,u),at(refs,respondent),deps,group,(r,s,o)))
                continue
            row=None if not lead else json.loads(lead+account(stream.readline(MAX_LINE)))
            if type(row) is not list or not row:
                raise _error("truncated preparation")
            if row[0]=="end":
                if row!=["end",count] or len(headers)!=count or account(stream.read(1)):
                    raise _error("preparation census mismatch")
                return tuple(headers)
            if row[0]=="r" and len(row)==4:
                refs.append(ExactRef(*row[1:]))
            elif row[0]=="p" and len(row)==2:
                p=row[1]
                if type(p) is not list or len(p)!=8:
                    raise _error("invalid selector payload")
                payloads.append((p[0],*(None if x is None else tuple(x) for x in p[1:4]),
                    tuple(tuple(x) for x in p[4]),
                    *(_freeze_semantic_descendants(x) for x in p[5:])))
            elif row[0]=="h" and len(row)==9 and len(headers)<count:
                _,event,occ,group,p,u,respondent,deps,coords=row
                identity=bytes.fromhex(event) if type(event) is str else tuple(event)
                if type(identity) is bytes and len(identity)!=32:
                    raise _error("invalid event digest")
                headers.append(_CountryEventHeader(identity,
                    _compact_identity(occ,_COUNTRY_OCCURRENCE_PREFIX),
                    at(payloads,p),at(refs,u),at(refs,respondent),
                    tuple(at(refs,i) for i in deps),
                    _compact_identity(group,_COUNTRY_GROUP_PREFIX),tuple(coords)))
            else:
                raise _error("invalid preparation record")

class _CountryPreparation:
    def __init__(self,path,pin):
        self.path=Path(path).absolute()
        if pin is not None and type(pin) is not CountryPreparationPin:
            raise _error("exact external producer pin required")
        self.pin=pin
        self._pin_material=None if pin is None else canonical_json(asdict(pin))

    def load(self,key):
        if self.pin is None:
            if self.path.exists() or self.path.is_symlink():
                raise _error("existing artifact without independently held pin")
            return None
        if (canonical_json(asdict(self.pin))!=self._pin_material
                or self.pin.facade_key!=_key(key) or self.pin.owner_abi!=_abi()):
            raise _error("external pin or current producer binding drift")
        try:
            return _decode_headers(_read_pinned(self.path,self.pin),_key(key))
        except (OSError,ValueError,TypeError,IndexError,EOFError) as exc:
            raise _error("pinned preparation refused: "+str(exc)) from exc

    def finish(self,key,release,headers):
        if self.pin is not None:
            if (canonical_json(asdict(self.pin))!=self._pin_material
                    or self.pin.facade_key!=_key(key)
                    or self.pin.release_identity!=_release(release)
                    or self.pin.owner_abi!=_abi()):
                raise _error("restored release or replay identity differs from producer pin")
            return
        if not headers:
            raise _error("validated producer header census required")
        directory=self.path.parent
        info=directory.stat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid!=os.getuid() or info.st_mode&0o077:
            raise _error("preparation requires private operator directory")
        fd,name=tempfile.mkstemp(prefix=".country-preparation-",dir=directory)
        stage=Path(name)
        try:
            with os.fdopen(fd,"wb") as file:
                with gzip.GzipFile(fileobj=file,mode="wb",mtime=0,filename="") as out:
                    _encode_headers(out,headers,_key(key))
                file.flush();os.fsync(file.fileno())
            size=stage.stat().st_size
            if not 0<size<=MAX_COMPRESSED:
                raise _error("compressed preparation cap")
            digest=sha256()
            with stage.open("rb") as file:
                for chunk in iter(lambda:file.read(1024**2),b""):
                    digest.update(chunk)
            pin=CountryPreparationPin(digest.hexdigest(),size,_key(key),_release(release),_abi())
            # No replacement or silently trusted preexisting artifact.
            os.link(stage,self.path)
            self.pin=pin
            self._pin_material=canonical_json(asdict(pin))
        finally:
            stage.unlink(missing_ok=True)
