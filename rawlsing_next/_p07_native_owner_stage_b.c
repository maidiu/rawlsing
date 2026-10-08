/* HQ245 Stage B -- F7 native P07 FULL ADJUDICATOR in quarantine.
 *
 * NON-PRODUCTION. NOT imported by production P07 or F7. Does NOT replace the accepted
 * Python SourceRelationResolver and is NOT an adopted authority.
 *
 * Extends the HQ244 Stage A owner into the COMPLETE actual P07 adjudicator:
 *   - accepted P07 canonical semantic custody hash (replaces the Stage A FNV-1a walk)
 *   - real _relation_object_key_from_relation material (replaces the ref-derived key)
 *   - deep-validated, deep-copied pinned relation and authority-snapshot custody
 *   - resolve_exact WITH semantic_projection() re-hash and replay-identity validation
 *   - the entire _validate_positive_from_owner_state guard chain
 *   - the entire _decide_from_owner_state ladder and CONFLICTING_AUTHORITY precedence
 *   - _relation_decision_replay_identity and decision replay validation
 *
 * TRUSTED SEAM (HQ245 clause 3). Byte-exact parity for canonical JSON and semantic_hash
 * is obtained from THREE trusted Python callables pinned INTO C MEMORY AT CONSTRUCTION:
 * semantic_hash, canonicalize and require_positive_authority. They are captured by
 * object identity at admission, validated to be callable, and NEVER re-read from any
 * caller-visible attribute afterwards. The live caller registry and the production
 * Python owner are never consulted for a positive decision. All caller data is deep
 * validated and deep copied BEFORE any trusted call. The final adjudication is native.
 *
 * There is NO parallel Python positive decision authority on this path: decide() and
 * require() are implemented here and cannot delegate a positive outcome to Python.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define STAGE_B_CONTRACT "PRE553_I07_SOURCE_PLURALITY_COMPOSITION@1.0.0"
#define DEFAULT_RELATION_STATE "DISTINCT_BY_DEFAULT"
#define STATE_AUTHORIZED "AUTHORIZED"
#define STATE_CONFLICTING "CONFLICTING_AUTHORITY"
#define STATE_UNKNOWN "UNKNOWN_AUTHORITY"
#define STATE_OUT_OF_SCOPE "OUT_OF_SCOPE"

/* One sealed relation. Identity and authority material are C-owned copies taken at
 * admission; only an owned reference to the object itself is retained so it can be
 * re-verified (never trusted) on every decision. */
typedef struct {
    PyObject *rel;               /* owned; re-verified, never trusted              */
    char *ref_key;               /* kind|object_id|content_hash                    */
    char *content_hash;
    char *object_key;            /* real P07 relation object key (semantic_hash)   */
    char *relation_kind;
    char *decision_value;        /* semantic_fields['decision'] or UNKNOWN_AUTHORITY*/
    char *authority_operation;
    char *target_use;
    char *authority_key;         /* relation_authority_ref key                     */
    char *replay_identity;       /* sealed replay identity string (or "")          */
    char *proj_json;             /* sealed canonical JSON of semantic_projection   */
    PyObject *ref_dict;          /* owned frozen dict copy of relation.ref.as_dict() */
    PyObject *sources;           /* owned tuple of ref dicts, sorted by ref key   */
    PyObject *operation_scope;   /* owned canonicalised copy                      */
    /* HQ246-P1: the TRUE effective_scope and directionality, taken from the admitted
     * object at admission. Stage B previously hardcoded DISTINCT_BY_DEFAULT/"SYMMETRIC"
     * here, which produced a WRONG object key and made by_key candidate selection
     * incapable of ever matching a genuine relation. */
    PyObject *effective_scope;
    PyObject *directionality;
} SealedRelation;

/* One sealed authority snapshot. */
typedef struct {
    PyObject *snap;              /* owned; exact AuthoritySnapshot, re-verified    */
    char *authority_key;
    char *content_hash;
    char *proj_json;
    PyObject *authority_ref_dict;
} SealedSnapshot;

typedef struct {
    PyObject_HEAD
    int sealed;
    SealedRelation *rels;
    Py_ssize_t n_rels;
    SealedSnapshot *snaps;
    Py_ssize_t n_snaps;
    char *custody_hash;          /* accepted P07 canonical semantic custody hash  */
    /* TRUSTED TCB: pinned callable identities, C-owned, never re-read from Python */
    PyObject *t_semantic_hash;
    PyObject *t_canonicalize;
    PyObject *t_require_positive;
    /* module refs used only for exception construction and exact-type checks */
    PyObject *exc_integrity;
    PyObject *exc_authz;
    PyObject *relation_cls;
    PyObject *snapshot_cls;
} StageBOwner;

static PyObject *STBIntegrityError = NULL;
static PyObject *STBAuthzError = NULL;

/* ---------------------------------------------------------------- helpers */

/* The accepted P07 relation kind set and its RELATION_DECISION_MATRIX defaults.
 * Byte-copied from rawlsing_next/pre553_source_relations.py @ 8053d30d. */
static const char *P07_KINDS[] = {
    "SOURCE_SEMANTIC_EQUIVALENCE", "RESPONDENT_LINKAGE", "OVERLAP_NON_DUPLICATION",
    "SAMPLE_POOLING", "ESTIMAND_COMPOSITION", "BACKFILL",
    "PROVENANCE_ORIGIN", "HARMONIZATION_ALIAS", NULL,
};
static int is_p07_kind(const char *k)
{
    int i;
    for (i = 0; P07_KINDS[i]; i++) if (strcmp(P07_KINDS[i], k) == 0) return 1;
    return 0;
}
static const char *matrix_default(const char *k)
{
    if (strcmp(k, "OVERLAP_NON_DUPLICATION") == 0) return "UNKNOWN_OVERLAP";
    if (strcmp(k, "PROVENANCE_ORIGIN") == 0) return "PROVENANCE_ONLY";
    if (strcmp(k, "HARMONIZATION_ALIAS") == 0) return "ALIAS_ONLY";
    return DEFAULT_RELATION_STATE;
}
static int is_descriptive_kind(const char *k)
{
    return strcmp(k, "PROVENANCE_ORIGIN") == 0 || strcmp(k, "HARMONIZATION_ALIAS") == 0;
}

static char *xstrdup(const char *s)
{
    size_t n;
    char *o;
    if (!s) return NULL;
    n = strlen(s) + 1;
    o = (char *)PyMem_Malloc(n);
    if (!o) return NULL;
    memcpy(o, s, n);
    return o;
}

static int stb_integrity(const char *msg)
{
    PyErr_SetString(STBIntegrityError, msg);
    return -1;
}

static int stb_authz(const char *state, const char *msg)
{
    PyObject *args, *exc, *st;
    st = PyUnicode_FromString(state);
    if (!st) return -1;
    args = Py_BuildValue("(sO)", msg, st);
    if (!args) { Py_DECREF(st); return -1; }
    exc = PyObject_CallObject(STBAuthzError, args);
    Py_DECREF(args);
    if (!exc) return -1;
    PyObject_SetAttrString(exc, "state", st);
    Py_DECREF(st);
    PyErr_SetObject((PyObject *)Py_TYPE(exc), exc);
    Py_DECREF(exc);
    return -1;
}

/* Read a str attribute into a fresh C string. */
static char *str_attr(PyObject *o, const char *name)
{
    PyObject *v = PyObject_GetAttrString(o, name);
    char *out;
    if (!v) { PyErr_Clear(); return NULL; }
    if (!PyUnicode_Check(v)) { Py_DECREF(v); PyErr_Clear(); return NULL; }
    out = xstrdup(PyUnicode_AsUTF8(v));
    Py_DECREF(v);
    return out;
}

/* PyObject_GetItemString is not part of the public C-API; provide it. */
static PyObject *dget(PyObject *d, const char *name)
{
    PyObject *k, *v;
    if (!d) return NULL;
    k = PyUnicode_FromString(name);
    if (!k) return NULL;
    v = PyObject_GetItem(d, k);
    Py_DECREF(k);
    if (!v) PyErr_Clear();
    return v;
}

/* Return the canonical exact key string for a ref given either as an object exposing
 * `.key` (ExactRef / AuthorityRef) or as a plain mapping of kind/object_id/content_hash.
 * Returns a NEW reference to a str, or NULL with a typed error. */
static PyObject *exact_key_of(PyObject *ref)
{
    PyObject *k, *k2, *o2, *c2, *out;
    k = PyObject_GetAttrString(ref, "key");
    if (k && PyUnicode_Check(k)) return k;
    Py_XDECREF(k);
    PyErr_Clear();
    if (!PyMapping_Check(ref)) {
        stb_integrity("exact ref material exposes neither .key nor a ref mapping");
        return NULL;
    }
    /* AuthorityRef-shaped material uses authority_id/authority_version/
     * authority_content_hash; ExactRef-shaped material uses kind/object_id/
     * content_hash. Both are exact refs with different key separators. */
    /* dget() returns an OWNED reference (and already clears any lookup error), so the
     * first probe must not be discarded. Retaining it leaked one object per
     * exact_key_of() call -- measured ~13-15 allocated blocks per decide(). */
    k2 = dget(ref, "kind");
    if (!k2) k2 = dget(ref, "authority_id");
    o2 = k2 ? dget(ref, "object_id") : NULL;
    if (!o2) { PyErr_Clear(); o2 = dget(ref, "authority_version"); }
    c2 = o2 ? dget(ref, "content_hash") : NULL;
    if (!c2) { PyErr_Clear(); c2 = dget(ref, "authority_content_hash"); }
    if (!k2 || !o2 || !c2 || !PyUnicode_Check(k2) || !PyUnicode_Check(o2)
        || !PyUnicode_Check(c2)) {
        Py_XDECREF(k2); Py_XDECREF(o2); Py_XDECREF(c2);
        stb_integrity("exact ref mapping lacks unicode kind/object_id/content_hash");
        return NULL;
    }
    out = PyUnicode_FromFormat("%s|%s|%s", PyUnicode_AsUTF8(k2),
                               PyUnicode_AsUTF8(o2), PyUnicode_AsUTF8(c2));
    Py_DECREF(k2); Py_DECREF(o2); Py_DECREF(c2);
    return out;
}

/* Plain-dict deep copy of exact ref material (ExactRef-shaped or AuthorityRef-shaped).
 * Returns a NEW dict, or NULL. */
static PyObject *ref_dict_copy(PyObject *ref)
{
    PyObject *d = NULL, *src = NULL, *k, *v;
    static const char *SETS[2][3] = {
        {"kind", "object_id", "content_hash"},
        {"authority_id", "authority_version", "authority_content_hash"},
    };
    int which;
    PyObject *ad = PyObject_CallMethod(ref, "as_dict", NULL);
    if (ad) {
        if (!PyMapping_Check(ad)) { Py_DECREF(ad); return NULL; }
    }
    {
        /* dget returns an OWNED reference; it must be released, otherwise every
         * ref_dict_copy() call leaks one object. */
        PyObject *probe = ad ? dget(ad, "kind") : NULL;
        which = probe ? 0 : 1;
        Py_XDECREF(probe);
    }
    Py_XDECREF(ad);
    src = PyObject_CallMethod(ref, "as_dict", NULL);
    if (!src) { PyErr_Clear(); src = ref; Py_INCREF(src); }
    d = PyDict_New();
    if (!d) { Py_XDECREF(src); return NULL; }
    for (which = 0; which < 2; which++) {
        int i, ok = 1;
        PyObject *tmp = PyDict_New();
        if (!tmp) { Py_DECREF(d); Py_XDECREF(src); return NULL; }
        for (i = 0; i < 3; i++) {
            k = PyUnicode_FromString(SETS[which][i]);
            v = dget(src, SETS[which][i]);
            if (!k || !v || !PyUnicode_Check(v) || PyDict_SetItem(tmp, k, v) < 0) {
                Py_XDECREF(k); Py_XDECREF(v); Py_DECREF(tmp); ok = 0; break;
            }
            Py_DECREF(k); Py_DECREF(v);
        }
        if (ok) { Py_DECREF(d); d = tmp; Py_XDECREF(src); return d; }
        Py_DECREF(tmp);
    }
    Py_XDECREF(src);
    Py_DECREF(d);
    return NULL;
}

static int obj_is_exact(PyObject *o, PyObject *cls)
{
    return o != NULL && cls != NULL && Py_TYPE(o) == (PyTypeObject *)cls;
}

/* Call the pinned trusted semantic_hash on a value. Returns a new str or NULL. */
static PyObject *trusted_hash(StageBOwner *self, PyObject *value)
{
    PyObject *r;
    if (!self->t_semantic_hash) {
        stb_integrity("stage B trusted semantic_hash is not pinned");
        return NULL;
    }
    r = PyObject_CallFunctionObjArgs(self->t_semantic_hash, value, NULL);
    if (!r) return NULL;
    if (!PyUnicode_Check(r)) {
        Py_DECREF(r);
        stb_integrity("trusted semantic_hash returned a non-str");
        return NULL;
    }
    return r;
}

static int is_hex64(const char *s)
{
    int i;
    if (!s) return 0;
    for (i = 0; i < 64; i++) {
        char c = s[i];
        if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) return 0;
    }
    return s[64] == '\0';
}

/* Build a dict from a NULL-terminated array of alternating key/value (value may NULL). */
static PyObject *mkdict(const char **keys, PyObject **vals)
{
    PyObject *d = PyDict_New();
    int i;
    if (!d) return NULL;
    for (i = 0; keys[i]; i++) {
        if (PyDict_SetItemString(d, keys[i], vals[i]) < 0) {
            Py_DECREF(d);
            return NULL;
        }
    }
    return d;
}

/* ------------------------------------------------------------- key material */

/* Native build of _relation_key_material, hashed by the pinned trusted semantic_hash.
 * Byte-exact because canonical_json sorts keys, so C dict insertion order is irrelevant.
 * On success stores the hex key in *out_key (caller frees). */
static int compute_relation_key(StageBOwner *self, const char *relation_kind,
                                PyObject *sources,          /* tuple of ref dicts */
                                PyObject *operation_scope,  /* canonicalised */
                                const char *target_use,
                                PyObject *effective_scope,
                                PyObject *directionality,
                                char **out_key)
{
    PyObject *d = NULL, *h = NULL;
    const char *keys[] = {"relation_kind", "source_universe_refs", "operation_scope",
                          "target_use", "effective_scope",
                          "directionality_or_symmetric", NULL};
    PyObject *vals[6];

    vals[0] = PyUnicode_FromString(relation_kind);
    vals[1] = sources;
    vals[2] = operation_scope;
    vals[3] = PyUnicode_FromString(target_use);
    vals[4] = effective_scope;
    vals[5] = directionality;
    if (!vals[0] || !vals[3]) { Py_XDECREF(vals[0]); Py_XDECREF(vals[3]); return -1; }

    d = mkdict(keys, vals);
    Py_DECREF(vals[0]);
    Py_DECREF(vals[3]);
    if (!d) return -1;

    h = trusted_hash(self, d);
    Py_DECREF(d);
    if (!h) return -1;

    *out_key = xstrdup(PyUnicode_AsUTF8(h));
    Py_DECREF(h);
    if (!*out_key) { PyErr_NoMemory(); return -1; }
    return 0;
}

/* Canonicalise a value through the pinned trusted seam.
 *
 * The accepted P07 `canonicalize` returns a canonical structural value (a frozen
 * mapping/sequence/scalar), NOT a string -- canonical_json performs the string step.
 * So the result is accepted as an opaque canonical value and returned to the caller,
 * which owns it. Only a NULL result is a failure. */
static PyObject *trusted_canon(StageBOwner *self, PyObject *v)
{
    PyObject *r;
    if (!self->t_canonicalize) {
        stb_integrity("stage B trusted canonicalize is not pinned");
        return NULL;
    }
    r = PyObject_CallFunctionObjArgs(self->t_canonicalize, v, NULL);
    if (!r) return NULL;
    /* MEMORY-SAFETY: the accepted `canonicalize` can return its INPUT object unchanged
     * (e.g. canonicalize({}) is {}). Taking ownership of that result without an extra
     * INCREF would make the caller steal a reference from the live input and eventually
     * free an object still in use -- observed as EXC_BAD_ACCESS inside
     * object_recursive_isinstance. Take a real owned reference unconditionally. */
    Py_INCREF(r);
    return r;
}

/* --------------------------------------------------------- free / dealloc */

static void free_rels(StageBOwner *self)
{
    Py_ssize_t i;
    if (self->rels) {
        for (i = 0; i < self->n_rels; i++) {
            PyMem_Free(self->rels[i].ref_key);
            PyMem_Free(self->rels[i].content_hash);
            PyMem_Free(self->rels[i].object_key);
            PyMem_Free(self->rels[i].relation_kind);
            PyMem_Free(self->rels[i].decision_value);
            PyMem_Free(self->rels[i].authority_operation);
            PyMem_Free(self->rels[i].target_use);
            PyMem_Free(self->rels[i].authority_key);
            PyMem_Free(self->rels[i].replay_identity);
            PyMem_Free(self->rels[i].proj_json);
            Py_XDECREF(self->rels[i].rel);
            Py_XDECREF(self->rels[i].ref_dict);
            Py_XDECREF(self->rels[i].sources);
            Py_XDECREF(self->rels[i].operation_scope);
            Py_XDECREF(self->rels[i].effective_scope);
            Py_XDECREF(self->rels[i].directionality);
        }
        PyMem_Free(self->rels);
        self->rels = NULL;
    }
    self->n_rels = 0;
}

static void free_snaps(StageBOwner *self)
{
    Py_ssize_t i;
    if (self->snaps) {
        for (i = 0; i < self->n_snaps; i++) {
            PyMem_Free(self->snaps[i].authority_key);
            PyMem_Free(self->snaps[i].content_hash);
            PyMem_Free(self->snaps[i].proj_json);
            Py_XDECREF(self->snaps[i].snap);
            Py_XDECREF(self->snaps[i].authority_ref_dict);
        }
        PyMem_Free(self->snaps);
        self->snaps = NULL;
    }
    self->n_snaps = 0;
}

static void stb_free_contents(StageBOwner *self)
{
    free_rels(self);
    free_snaps(self);
    PyMem_Free(self->custody_hash);
    self->custody_hash = NULL;
    Py_CLEAR(self->t_semantic_hash);
    Py_CLEAR(self->t_canonicalize);
    Py_CLEAR(self->t_require_positive);
    Py_CLEAR(self->exc_integrity);
    Py_CLEAR(self->exc_authz);
    Py_CLEAR(self->relation_cls);
    Py_CLEAR(self->snapshot_cls);
    self->sealed = 0;
}

/* D5 CYCLE REPAIR: StageBOwner holds strong references to admitted relations, admitted
 * authority snapshots, three trusted callables and two exact classes. Without
 * tp_traverse/tp_clear the collector cannot see those references, so any object graph
 * that refers back to the owner forms an uncollectable cycle and leaks permanently. */
static int
StageBOwner_traverse(StageBOwner *self, visitproc visit, void *arg)
{
    Py_ssize_t i;
    Py_VISIT(self->t_semantic_hash);
    Py_VISIT(self->t_canonicalize);
    Py_VISIT(self->t_require_positive);
    Py_VISIT(self->relation_cls);
    Py_VISIT(self->snapshot_cls);
    Py_VISIT(self->exc_integrity);
    Py_VISIT(self->exc_authz);
    for (i = 0; i < self->n_rels; i++) {
        if (self->rels[i].rel)       Py_VISIT(self->rels[i].rel);
        if (self->rels[i].ref_dict)   Py_VISIT(self->rels[i].ref_dict);
        if (self->rels[i].sources)    Py_VISIT(self->rels[i].sources);
        if (self->rels[i].operation_scope) Py_VISIT(self->rels[i].operation_scope);
        if (self->rels[i].effective_scope)  Py_VISIT(self->rels[i].effective_scope);
        if (self->rels[i].directionality)   Py_VISIT(self->rels[i].directionality);
    }
    for (i = 0; i < self->n_snaps; i++) {
        if (self->snaps[i].snap)          Py_VISIT(self->snaps[i].snap);
        if (self->snaps[i].authority_ref_dict) Py_VISIT(self->snaps[i].authority_ref_dict);
    }
    return 0;
}

static int
StageBOwner_clear(StageBOwner *self)
{
    stb_free_contents(self);
    return 0;
}

static void StageBOwner_dealloc(StageBOwner *self)
{
    stb_free_contents(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

/* ------------------------------------------------------------- admission */

/* Deep-validate and deep-copy ONE relation into sealed custody.
 *
 * Every Python read happens HERE, before the seal. Nothing Python-reachable is kept as
 * a mutable identity source: identity, authority and projection material are copied into
 * C memory (identity as C strings, projections as canonical JSON text). */
static int admit_relation(StageBOwner *self, PyObject *rel, SealedRelation *out,
                          Py_ssize_t idx)
{
    char *rk = NULL, *ch = NULL, *kind = NULL, *dec = NULL;
    char *aop = NULL, *tuse = NULL, *akey = NULL, *repl = NULL;
    char *okey = NULL, *pjson = NULL;
    PyObject *refobj = NULL, *refdict = NULL, *srcs = NULL, *scope = NULL;
    PyObject *sf = NULL, *proj = NULL, *item;
    PyObject *arel = NULL, *authkey = NULL, *tup = NULL;
    PyObject *eff = NULL, *dir = NULL;
    Py_ssize_t i, n;

    if (!obj_is_exact(rel, self->relation_cls)) {
        PyErr_Format(PyExc_TypeError,
            "stage B admission: relation[%zd] must be exact SourceUniverseRelation", idx);
        return -1;
    }
    refobj = PyObject_GetAttrString(rel, "ref");
    if (!refobj) return -1;
    {
        PyObject *kk = exact_key_of(refobj);
        if (!kk) { Py_DECREF(refobj); return -1; }
        rk = xstrdup(PyUnicode_AsUTF8(kk));
        Py_DECREF(kk);
        if (!rk) { Py_DECREF(refobj); PyErr_NoMemory(); return -1; }
    }

    refdict = ref_dict_copy(refobj);
    Py_DECREF(refobj);
    if (!refdict) return -1;

    ch = str_attr(rel, "content_hash");
    if (!ch || !is_hex64(ch)) {
        stb_integrity("relation content_hash is not an exact lowercase sha256");
        goto fail;
    }
    kind = str_attr(rel, "relation_kind");
    if (!kind) { stb_integrity("relation lacks relation_kind"); goto fail; }

    /* sealed canonical projection text -- the resolve-time re-hash reference */
    proj = PyObject_CallMethod(rel, "semantic_projection", NULL);
    if (!proj) goto fail;
    /* sealed projection identity: the trusted semantic_hash of the projection */
    {
        PyObject *hh = trusted_hash(self, proj);
        if (!hh) goto fail;
        pjson = xstrdup(PyUnicode_AsUTF8(hh));
        Py_DECREF(hh);
    }
    Py_DECREF(proj);
    if (!pjson) { PyErr_NoMemory(); goto fail; }

    /* decision value: semantic_fields.get('decision', 'UNKNOWN_AUTHORITY') */
    sf = PyObject_GetAttrString(rel, "semantic_fields");
    if (!sf) goto fail;
    item = dget(sf, "decision");
    Py_DECREF(sf);
    if (!item) {
        PyErr_Clear();
        item = PyUnicode_FromString(STATE_UNKNOWN);
    }
    if (!item) goto fail;
    if (!PyUnicode_Check(item)) {
        Py_DECREF(item);
        stb_integrity("relation decision value is not str");
        goto fail;
    }
    dec = xstrdup(PyUnicode_AsUTF8(item));
    Py_DECREF(item);
    if (!dec) { PyErr_NoMemory(); goto fail; }

    aop = str_attr(rel, "authority_operation");
    tuse = str_attr(rel, "target_use");

    arel = PyObject_GetAttrString(rel, "relation_authority_ref");
    if (!arel) goto fail;
    authkey = exact_key_of(arel);
    if (!authkey) goto fail;
    akey = xstrdup(PyUnicode_AsUTF8(authkey));
    Py_DECREF(authkey);
    if (!akey) { PyErr_NoMemory(); goto fail; }

    /* sealed replay identity string (may be absent) */
    {
        PyObject *sfi = PyObject_GetAttrString(rel, "semantic_fields");
        PyObject *v = sfi ? dget(sfi, "replay_identity") : NULL;
        PyErr_Clear();
        Py_XDECREF(sfi);
        if (v && PyUnicode_Check(v)) repl = xstrdup(PyUnicode_AsUTF8(v));
        Py_XDECREF(v);
        PyErr_Clear();
        if (!repl) repl = xstrdup("");
        if (!repl) { PyErr_NoMemory(); goto fail; }
    }

    /* canonicalised operation_scope copy */
    {
        PyObject *osc = PyObject_GetAttrString(rel, "operation_scope");
        if (!osc) goto fail;
        scope = trusted_canon(self, osc);
        Py_DECREF(osc);
        if (!scope) goto fail;
    }

    /* canonical ordered source ref dicts, sorted by ref key, deduped, >= 2 */
    {
        PyObject *srl = PyObject_GetAttrString(rel, "source_universe_refs");
        PyObject *pairs = NULL;
        if (!srl) goto fail;
        n = PySequence_Size(srl);
        if (n < 0) { Py_DECREF(srl); goto fail; }
        pairs = PyList_New(0);
        if (!pairs) { Py_DECREF(srl); goto fail; }
        for (i = 0; i < n; i++) {
            PyObject *one = PySequence_GetItem(srl, i);
            PyObject *r2, *k2, *d2, *pr;
            if (!one) { Py_DECREF(pairs); Py_DECREF(srl); goto fail; }
            r2 = exact_key_of(one);
            d2 = ref_dict_copy(one);
            Py_DECREF(one);
            if (!r2 || !d2) { Py_XDECREF(r2); Py_XDECREF(d2);
                              Py_DECREF(pairs); Py_DECREF(srl); goto fail; }
            k2 = PyUnicode_FromString(PyUnicode_AsUTF8(r2));
            Py_DECREF(r2);
            if (!k2) { Py_DECREF(d2); Py_DECREF(pairs); Py_DECREF(srl); goto fail; }
            pr = Py_BuildValue("(sO)", PyUnicode_AsUTF8(k2), d2);
            Py_DECREF(k2);
            if (!pr) { Py_DECREF(pairs); Py_DECREF(srl); goto fail; }
            if (PyList_Append(pairs, pr) < 0) { Py_DECREF(pr); Py_DECREF(pairs);
                                                 Py_DECREF(srl); goto fail; }
            Py_DECREF(pr);
        }
        Py_DECREF(srl);
        if (PyList_Sort(pairs) < 0) { Py_DECREF(pairs); goto fail; }
        /* dedupe by key */
        {
            /* Dedupe by exact ref key. The previous key is kept as an OWNED C string
             * so no pointer into a DECREFed temporary is ever compared. */
            PyObject *uniq = PyList_New(0);
            char *prev = NULL;
            if (!uniq) { Py_DECREF(pairs); goto fail; }
            for (i = 0; i < PyList_Size(pairs); i++) {
                PyObject *pr = PyList_GetItem(pairs, i);
                PyObject *kk = PySequence_GetItem(pr, 0);
                PyObject *dd = PySequence_GetItem(pr, 1);
                char *ks = NULL;
                int dup = 0;
                if (kk && PyUnicode_Check(kk)) ks = xstrdup(PyUnicode_AsUTF8(kk));
                if (!ks) {
                    Py_XDECREF(kk); Py_XDECREF(dd); Py_DECREF(uniq);
                    Py_DECREF(pairs);
                    stb_integrity("source ref lacks an exact unicode key");
                    goto fail;
                }
                if (prev && strcmp(ks, prev) == 0) dup = 1;
                if (!dup && PyList_Append(uniq, dd) < 0) {
                    PyMem_Free(ks); Py_XDECREF(kk); Py_XDECREF(dd);
                    Py_DECREF(uniq); Py_DECREF(pairs);
                    goto fail;
                }
                if (!dup) { PyMem_Free(prev); prev = ks; } else { PyMem_Free(ks); }
                Py_XDECREF(kk); Py_XDECREF(dd);
            }
            PyMem_Free(prev);
            srcs = uniq;
        }
        Py_DECREF(pairs);
        if (PyList_Size(srcs) < 2) {
            stb_integrity("source relation requires at least two exact source universes");
            goto fail;
        }
        tup = PyList_AsTuple(srcs);
        Py_DECREF(srcs);
        srcs = tup;
        if (!srcs) goto fail;
    }

    /* HQ246-P1: derive the true effective_scope and directionality_or_symmetric from the
     * AUTHENTICATED admitted object, exactly as _relation_object_key_from_relation does.
     * Never a default and never an assumed "SYMMETRIC". */
    {
        PyObject *ev = PyObject_GetAttrString(rel, "effective_scope");
        PyObject *dv = PyObject_GetAttrString(rel, "directionality_or_symmetric");
        if (!ev || !dv) {
            Py_XDECREF(ev); Py_XDECREF(dv);
            stb_integrity("relation must expose effective_scope and "
                          "directionality_or_symmetric for an exact object key");
            goto fail;
        }
        eff = trusted_canon(self, ev);
        Py_DECREF(ev);
        dir = trusted_canon(self, dv);
        Py_DECREF(dv);
        if (!eff || !dir) goto fail;
    }

    /* REAL relation object key via the pinned trusted hash over native key material. */
    if (compute_relation_key(self, kind, srcs, scope, tuse, eff, dir, &okey) < 0)
        goto fail;

    out->rel = rel;            Py_INCREF(rel);
    out->ref_key = rk;         rk = NULL;
    out->content_hash = ch;    ch = NULL;
    out->object_key = okey;    okey = NULL;
    out->relation_kind = kind; kind = NULL;
    out->decision_value = dec; dec = NULL;
    out->authority_operation = aop; aop = NULL;
    out->target_use = tuse;    tuse = NULL;
    out->authority_key = akey; akey = NULL;
    out->replay_identity = repl; repl = NULL;
    out->proj_json = pjson;    pjson = NULL;
    out->ref_dict = refdict;   refdict = NULL;
    out->sources = srcs;       srcs = NULL;
    out->operation_scope = scope; scope = NULL;
    out->effective_scope = eff; eff = NULL;
    out->directionality = dir; dir = NULL;
    return 0;

fail:
    PyMem_Free(rk); PyMem_Free(ch); PyMem_Free(kind); PyMem_Free(dec);
    PyMem_Free(aop); PyMem_Free(tuse); PyMem_Free(akey); PyMem_Free(repl);
    PyMem_Free(okey); PyMem_Free(pjson);
    Py_XDECREF(refdict); Py_XDECREF(srcs); Py_XDECREF(scope);
    Py_XDECREF(eff); Py_XDECREF(dir);
    return -1;
}

static int admit_snapshot(StageBOwner *self, PyObject *s, SealedSnapshot *out,
                          Py_ssize_t idx)
{
    char *akey = NULL, *ch = NULL, *pjson = NULL;
    PyObject *snap = NULL, *aref = NULL, *akeyobj = NULL, *arfd = NULL;
    PyObject *proj = NULL;

    if (!obj_is_exact(s, self->snapshot_cls)) {
        PyErr_Format(PyExc_TypeError,
            "stage B admission: authority_snapshots[%zd] must be exact AuthoritySnapshot", idx);
        return -1;
    }
    snap = s; Py_INCREF(snap);
    aref = PyObject_GetAttrString(snap, "authority_ref");
    if (!aref) goto fail;
    akeyobj = exact_key_of(aref);
    if (!akeyobj) goto fail;
    akey = xstrdup(PyUnicode_AsUTF8(akeyobj));
    arfd = ref_dict_copy(aref);
    Py_DECREF(aref);
    if (!akey || !arfd) goto fail;

    ch = str_attr(snap, "content_hash");
    if (!ch || !is_hex64(ch)) {
        stb_integrity("authority snapshot content_hash is not an exact lowercase sha256");
        goto fail;
    }
    proj = PyObject_CallMethod(snap, "semantic_projection", NULL);
    if (!proj) goto fail;
    /* sealed projection identity: the trusted semantic_hash of the projection */
    {
        PyObject *hh = trusted_hash(self, proj);
        if (!hh) goto fail;
        pjson = xstrdup(PyUnicode_AsUTF8(hh));
        Py_DECREF(hh);
    }
    Py_DECREF(proj);
    if (!pjson) { PyErr_NoMemory(); goto fail; }

    out->snap = snap;          snap = NULL;
    out->authority_key = akey; akey = NULL;
    out->content_hash = ch;    ch = NULL;
    out->proj_json = pjson;    pjson = NULL;
    out->authority_ref_dict = arfd; arfd = NULL;
    return 0;

fail:
    PyMem_Free(akey); PyMem_Free(ch); PyMem_Free(pjson);
    Py_XDECREF(snap); Py_XDECREF(arfd);
    return -1;
}

/* ------------------------------------------- accepted P07 semantic custody hash */

/* Native construction of the ACCEPTED P07 custody hash material, hashed by the pinned
 * trusted semantic_hash. Byte-identical to the Python factory's custody_hash:
 *   {"contract": I07_CONTRACT_ID,
 *    "relations": [{ref, semantic_content_hash, replay_identity} ... sorted by ref key],
 *    "authority_snapshots": [{authority_ref, snapshot_semantic_content_hash} ... sorted]}
 * Sorting is by ref.key / authority_ref.key. */
static int compute_custody_hash(StageBOwner *self, char **out)
{
    PyObject *rl = NULL, *al = NULL, *mat = NULL, *h = NULL;
    Py_ssize_t i, n;

    n = self->n_rels;

    /* Build both lists directly from the sealed arrays, ordered by the C ref_key /
     * authority_key using an explicit index sort (ASCII keys: byte order == code point). */
    rl = PyList_New(0);
    if (!rl) goto fail;
    {
        Py_ssize_t *order = (Py_ssize_t *)PyMem_Calloc((size_t)(n > 0 ? n : 1),
                                                        sizeof(Py_ssize_t));
        if (!order) { PyErr_NoMemory(); goto fail; }
        for (i = 0; i < n; i++) order[i] = i;
        /* insertion sort by ref_key (keys are ASCII hex/URN, byte order == code point) */
        for (i = 1; i < n; i++) {
            Py_ssize_t k = order[i], j = i - 1;
            while (j >= 0 && strcmp(self->rels[order[j]].ref_key,
                                    self->rels[k].ref_key) > 0) {
                order[j + 1] = order[j]; j--;
            }
            order[j + 1] = k;
        }
        for (i = 0; i < n; i++) {
            SealedRelation *R = &self->rels[order[i]];
            PyObject *ri = (R->replay_identity[0] != '\0')
                ? PyUnicode_FromString(R->replay_identity) : NULL;
            PyObject *ent;
            if (!ri) { ri = Py_None; Py_INCREF(Py_None); }
            ent = Py_BuildValue("{s:O,s:s,s:O}",
                "ref", R->ref_dict,
                "semantic_content_hash", R->content_hash,
                "replay_identity", ri);
            Py_DECREF(ri);
            if (!ent) { PyMem_Free(order); goto fail; }
            if (PyList_Append(rl, ent) < 0) { Py_DECREF(ent);
                                               PyMem_Free(order); goto fail; }
            Py_DECREF(ent);
        }
        PyMem_Free(order);
    }

    {
        Py_ssize_t m = self->n_snaps, j;
        Py_ssize_t *order = (Py_ssize_t *)PyMem_Calloc((size_t)(m > 0 ? m : 1),
                                                        sizeof(Py_ssize_t));
        al = PyList_New(0);
        if (!order || !al) { Py_XDECREF(order); PyErr_NoMemory(); goto fail; }
        for (j = 0; j < m; j++) order[j] = j;
        for (j = 1; j < m; j++) {
            Py_ssize_t k = order[j], p = j - 1;
            while (p >= 0 && strcmp(self->snaps[order[p]].authority_key,
                                    self->snaps[k].authority_key) > 0) {
                order[p + 1] = order[p]; p--;
            }
            order[p + 1] = k;
        }
        for (j = 0; j < m; j++) {
            SealedSnapshot *S = &self->snaps[order[j]];
            PyObject *ent = Py_BuildValue("{s:O,s:s}",
                "authority_ref", S->authority_ref_dict,
                "snapshot_semantic_content_hash", S->content_hash);
            if (!ent) { PyMem_Free(order); goto fail; }
            if (PyList_Append(al, ent) < 0) { Py_DECREF(ent);
                                               PyMem_Free(order); goto fail; }
            Py_DECREF(ent);
        }
        PyMem_Free(order);
    }

    mat = Py_BuildValue("{s:s,s:O,s:O}",
        "contract", STAGE_B_CONTRACT,
        "relations", rl,
        "authority_snapshots", al);
    if (!mat) goto fail;
    h = trusted_hash(self, mat);
    if (!h) goto fail;
    *out = xstrdup(PyUnicode_AsUTF8(h));
    Py_DECREF(h);
    if (!*out) { PyErr_NoMemory(); goto fail; }
    Py_DECREF(mat);
    return 0;

fail:
    Py_XDECREF(rl); Py_XDECREF(al); Py_XDECREF(mat); Py_XDECREF(h);
    return -1;
}

/* --------------------------------------------------------------- constructor */

static int StageBOwner_init(StageBOwner *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"relations", "authority_snapshots",
                             "trusted_semantic_hash", "trusted_canonicalize",
                             "trusted_require_positive_authority",
                             "relation_class", "authority_snapshot_class",
                             NULL};
    PyObject *relations = NULL, *snaps = NULL, *tsh = NULL, *tc = NULL, *trp = NULL;
    PyObject *rcls = NULL, *acls = NULL;
    PyObject *fast = NULL, *fasts = NULL;
    Py_ssize_t n, m, i;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOOOOO:StageBOwner", kwlist,
                                     &relations, &snaps, &tsh, &tc, &trp, &rcls, &acls))
        return -1;

    if (self->sealed)
        return stb_integrity("stage B custody is one-shot: this native owner is already "
                             "sealed and cannot be re-initialised, resealed or re-admitted");
    if (relations == Py_None || snaps == Py_None)
        return stb_integrity("stage B admission requires explicit relations and "
                             "authority_snapshots");
    /* D1 MEMORY-BOUNDARY REPAIR (this is the defect HQ statically verified at the exact
     * Stage B blob 2d8ffc686fcdb3f7108f0c8bafe7f60273fcf304, lines 827-876).
     *
     * PyList_Check/PyTuple_Check accept SUBCLASSES. PySequence_Size() on a subclass
     * dispatches to an attacker-overridden __len__, whose return value does not describe
     * the real storage. That value was used to size self->rels / self->snaps AND as the
     * loop bound over PySequence_Fast_GET_ITEM(fast, i), which is an out-of-bounds array
     * read when __len__ over-reports and a silent custody truncation when it under-reports.
     *
     * Repair: accept ONLY exact built-in list/tuple, whose length is a C-API count no
     * Python code can lie about; convert with PySequence_Fast; then derive EVERY bound
     * from PySequence_Fast_GET_SIZE of the converted sequence. */
    if (!PyList_CheckExact(relations) && !PyTuple_CheckExact(relations))
        return stb_integrity("stage B admission requires an EXACT list or tuple (not a "
                             "subclass) of relations, so no overridden __len__ can "
                             "supply the iteration bound");
    if (!PyList_CheckExact(snaps) && !PyTuple_CheckExact(snaps))
        return stb_integrity("stage B admission requires an EXACT list or tuple (not a "
                             "subclass) of authority snapshots, so no overridden __len__ "
                             "can supply the iteration bound");
    if (!PyCallable_Check(tsh) || !PyCallable_Check(tc) || !PyCallable_Check(trp))
        return stb_integrity("stage B requires three trusted pinned callables: "
                             "semantic_hash, canonicalize, require_positive_authority");
    if (!PyType_Check(rcls) || !PyType_Check(acls))
        return stb_integrity("stage B requires exact relation and authority snapshot classes");

    /* Pin the trusted TCB and exact classes into C memory FIRST, before any user data
     * is read, so the callback set cannot be swapped by a later caller-side mutation. */
    Py_INCREF(tsh); Py_INCREF(tc); Py_INCREF(trp); Py_INCREF(rcls); Py_INCREF(acls);
    Py_XINCREF(STBIntegrityError); Py_XINCREF(STBAuthzError);
    self->t_semantic_hash = tsh;
    self->t_canonicalize = tc;
    self->t_require_positive = trp;
    self->relation_cls = rcls;
    self->snapshot_cls = acls;
    self->exc_integrity = STBIntegrityError;
    self->exc_authz = STBAuthzError;

    /* D3: from here on EVERY failure path must clean up, because the trusted callables
     * and classes are already pinned. `fail_init` performs the full release. */
    fast = PySequence_Fast(relations, "relations");
    if (!fast) goto fail_init;
    /* D1: the ONLY authoritative bound is the converted sequence's ACTUAL length. */
    n = PySequence_Fast_GET_SIZE(fast);
    if (n > 0) {
        self->rels = (SealedRelation *)PyMem_Calloc((size_t)n, sizeof(SealedRelation));
        if (!self->rels) { Py_DECREF(fast); PyErr_NoMemory(); goto fail_init; }
    }
    for (i = 0; i < n; i++) {
        if (admit_relation(self, PySequence_Fast_GET_ITEM(fast, i), &self->rels[i], i) < 0) {
            Py_DECREF(fast); goto fail_init;   /* nothing sealed */
        }
        self->n_rels = i + 1;
    }
    Py_DECREF(fast);

    fasts = PySequence_Fast(snaps, "authority snapshots");
    if (!fasts) goto fail_init;
    m = PySequence_Fast_GET_SIZE(fasts);
    if (m > 0) {
        self->snaps = (SealedSnapshot *)PyMem_Calloc((size_t)m, sizeof(SealedSnapshot));
        if (!self->snaps) { Py_DECREF(fasts); PyErr_NoMemory(); goto fail_init; }
    }
    for (i = 0; i < m; i++) {
        if (admit_snapshot(self, PySequence_Fast_GET_ITEM(fasts, i), &self->snaps[i], i) < 0) {
            Py_DECREF(fasts); goto fail_init;
        }
        self->n_snaps = i + 1;
    }
    Py_DECREF(fasts);

    if (compute_custody_hash(self, &self->custody_hash) < 0) goto fail_init;

    self->sealed = 1;
    return 0;

fail_init:
    /* D3 TRANSACTIONAL CLEANUP: release the pinned TCB, the pinned classes, the pinned
     * exception refs and every partially admitted relation/snapshot, so a failed
     * construction leaks nothing and leaves no dirty owner. */
    stb_free_contents(self);
    return -1;
}

/* ------------------------------------------------------------- resolve_exact */

static SealedRelation *find_by_ref_key(StageBOwner *self, const char *key)
{
    Py_ssize_t i;
    for (i = 0; i < self->n_rels; i++) {
        if (strcmp(self->rels[i].ref_key, key) == 0) return &self->rels[i];
    }
    return NULL;
}

static SealedSnapshot *find_snapshot(StageBOwner *self, const char *akey)
{
    Py_ssize_t i;
    for (i = 0; i < self->n_snaps; i++) {
        if (strcmp(self->snaps[i].authority_key, akey) == 0) return &self->snaps[i];
    }
    return NULL;
}

/* FULL resolve_exact: exact key lookup + semantic_projection() RE-HASH + ref/content
 * identity re-verification + replay identity presence verification.
 * Returns a new reference to the relation, or NULL with a typed negative. */
static PyObject *
stb_resolve_exact(StageBOwner *self, PyObject *arg)
{
    PyObject *key = NULL, *r, *k;
    const char *want;
    SealedRelation *R;
    PyObject *live = NULL, *proj = NULL, *h = NULL;
    const char *hs;

    if (!self->sealed)
        return (stb_integrity("stage B owner is not sealed"), NULL);

    if (PyMapping_Check(arg) && !PyUnicode_Check(arg)) {
        /* Shape 2: an exact ref mapping supplied directly. */
        PyObject *k2 = dget(arg, "kind"), *o2 = dget(arg, "object_id"),
                   *c2 = dget(arg, "content_hash");
        if (!k2 || !o2 || !c2 || !PyUnicode_Check(k2) || !PyUnicode_Check(o2)
            || !PyUnicode_Check(c2)) {
            Py_XDECREF(k2); Py_XDECREF(o2); Py_XDECREF(c2);
            return (stb_integrity("stage B resolve_exact requires exact ref material"), NULL);
        }
        key = PyUnicode_FromFormat("%s|%s|%s", PyUnicode_AsUTF8(k2),
                                   PyUnicode_AsUTF8(o2), PyUnicode_AsUTF8(c2));
        Py_DECREF(k2); Py_DECREF(o2); Py_DECREF(c2);
        if (!key) return NULL;
    } else {
    k = PyObject_GetAttrString(arg, "key");
    if (!k) {
        PyObject *mapping, *k2, *o2, *c2;
        PyErr_Clear();
        mapping = PyObject_CallMethod(arg, "as_dict", NULL);
        if (!mapping) {
            PyErr_Clear();
            PyErr_SetString(STBIntegrityError,
                "stage B resolve_exact requires an exact ref or ref mapping");
            return NULL;
        }
        k2 = PyMapping_GetItemString(mapping, "kind");
        o2 = PyMapping_GetItemString(mapping, "object_id");
        c2 = PyMapping_GetItemString(mapping, "content_hash");
        if (!k2 || !o2 || !c2) {
            Py_XDECREF(k2); Py_XDECREF(o2); Py_XDECREF(c2); Py_DECREF(mapping);
            return (stb_integrity("stage B resolve_exact requires exact ref material"), NULL);
        }
        key = PyUnicode_FromFormat("%s|%s|%s",
            PyUnicode_AsUTF8(k2), PyUnicode_AsUTF8(o2), PyUnicode_AsUTF8(c2));
        Py_DECREF(k2); Py_DECREF(o2); Py_DECREF(c2); Py_DECREF(mapping);
        if (!key) return NULL;
    } else {
        key = k;
    }
    }
    want = PyUnicode_AsUTF8(key);
    if (!want) { Py_DECREF(key); return NULL; }

    R = find_by_ref_key(self, want);
    if (!R) {
        Py_DECREF(key);
        return (stb_integrity("exact SourceUniverseRelation unavailable from authenticated "
                              "owner custody; no label/ID/latest/default inference"), NULL);
    }

    /* (a) ref key re-verification */
    live = R->rel;
    r = PyObject_GetAttrString(live, "ref");
    if (!r) { Py_DECREF(key); return NULL; }
    k = PyObject_GetAttrString(r, "key");
    Py_DECREF(r);
    if (!k || !PyUnicode_Check(k)) {
        Py_XDECREF(k); Py_DECREF(key);
        return (stb_integrity("owner custody relation ref drift"), NULL);
    }
    if (strcmp(PyUnicode_AsUTF8(k), R->ref_key) != 0) {
        Py_DECREF(k); Py_DECREF(key);
        return (stb_integrity("owner custody relation ref drift"), NULL);
    }
    Py_DECREF(k);

    /* (b) content_hash re-verification */
    {
        char *ch = str_attr(live, "content_hash");
        if (!ch || strcmp(ch, R->content_hash) != 0) {
            PyMem_Free(ch); Py_DECREF(key);
            return (stb_integrity("owner custody relation semantic identity drift"), NULL);
        }
        PyMem_Free(ch);
    }

#ifdef STAGE_B_FAULT_INJECT_RESOLVE
    /* DELIBERATE TEST-ONLY FAULT: skip the semantic_projection() re-hash so a
     * post-seal projection mutation is returned as if trusted. Never compiled into the
     * shipped build; used only to prove the Stage B court actually turns RED. */
#else
    /* (c) FULL semantic_projection() RE-HASH through the pinned trusted semantic_hash */
    proj = PyObject_CallMethod(live, "semantic_projection", NULL);
    if (!proj) { Py_DECREF(key); return NULL; }
    h = trusted_hash(self, proj);
    Py_DECREF(proj);
    if (!h) { Py_DECREF(key); return NULL; }
    hs = PyUnicode_AsUTF8(h);
    if (!hs || strcmp(hs, R->content_hash) != 0) {
        Py_DECREF(h); Py_DECREF(key);
        return (stb_integrity("owner custody relation semantic hash mismatch"), NULL);
    }
    Py_DECREF(h);
#endif /* STAGE_B_FAULT_INJECT_RESOLVE */

    /* (d) replay identity must still be present and equal to the sealed value */
    {
        PyObject *sfi = PyObject_GetAttrString(live, "semantic_fields");
        PyObject *v = sfi ? dget(sfi, "replay_identity") : NULL;
        int bad = 0;
        PyErr_Clear();
        Py_XDECREF(sfi);
        if (!v || !PyUnicode_Check(v)) bad = 1;
        else if (strcmp(PyUnicode_AsUTF8(v), R->replay_identity) != 0) bad = 1;
        Py_XDECREF(v);
        if (bad) {
            Py_DECREF(key);
            return (stb_integrity("owner custody relation replay identity drift"), NULL);
        }
    }

    Py_DECREF(key);
    Py_INCREF(R->rel);
    return R->rel;
}

/* ---------------------------------------------- full positive guard chain */

/* Native port of _validate_positive_from_owner_state.
 *
 * Returns 0 and fills *out_auth (authority ref dict, new ref), *out_op (malloc'd),
 * *out_snap_hash (malloc'd) on an established positive.
 * Returns -1 with SourceRelationAuthorizationError set (state retrievable via
 * PyObject_GetAttrString(exc,"state")) on every negative.
 *
 * On ANY negative the caller must read the exception and continue the ladder; the
 * exception must be cleared before continuing. */
static int validate_positive(StageBOwner *self, SealedRelation *R,
                             PyObject *expected_op, PyObject **out_auth,
                             char **out_op, char **out_snap_hash)
{
    SealedSnapshot *S;
    char *op = NULL;

    /* descriptive kinds can never authorize */
    if (is_descriptive_kind(R->relation_kind))
        return stb_authz(DEFAULT_RELATION_STATE,
            "PROVENANCE_ORIGIN is descriptive and has zero composition effect");

    if (strcmp(R->decision_value, STATE_AUTHORIZED) != 0)
        return stb_authz(R->decision_value,
            "relation receipt is not a positive exact authority");

    op = xstrdup(R->authority_operation ? R->authority_operation : "");
    if (!op) { PyErr_NoMemory(); return -1; }

    if (expected_op != NULL) {
        const char *eo = PyUnicode_AsUTF8(expected_op);
        if (!eo || strcmp(op, eo) != 0) {
            PyMem_Free(op);
            return stb_authz(STATE_OUT_OF_SCOPE,
                "exact relation authority operation does not match requested operation");
        }
    }

    S = find_snapshot(self, R->authority_key);
    if (!S)
        return stb_authz(STATE_UNKNOWN,
            "relation authority snapshot is absent from authenticated owner custody");

    /* snapshot semantic identity: content_hash AND full projection re-hash */
    {
        PyObject *proj = PyObject_CallMethod(S->snap, "semantic_projection", NULL);
        PyObject *h;
        const char *hs;
        char *live_ch;
        if (!proj) return -1;
        h = trusted_hash(self, proj);
        Py_DECREF(proj);
        if (!h) return -1;
        hs = PyUnicode_AsUTF8(h);
        live_ch = str_attr(S->snap, "content_hash");
        if (!hs || !live_ch || strcmp(hs, S->content_hash) != 0 ||
            strcmp(live_ch, S->content_hash) != 0) {
            Py_XDECREF(h); PyMem_Free(live_ch);
            return stb_authz(STATE_UNKNOWN,
                "custodied authority snapshot semantic identity drift");
        }
        Py_DECREF(h); PyMem_Free(live_ch);
    }

    /* the trusted positive-authority check, per exact source universe */
    {
        static const struct { const char *kind; const char *auth; } KINDS[] = {
            {"SOURCE_SEMANTIC_EQUIVALENCE", "SOURCE_EQUIVALENCE"},
            {"RESPONDENT_LINKAGE",         "SOURCE_RESPONDENT_LINKAGE"},
            {"OVERLAP_NON_DUPLICATION",    "SOURCE_UNIVERSE_RELATION"},
            {"SAMPLE_POOLING",             "SOURCE_COMPOSITION_POOLING"},
            {"ESTIMAND_COMPOSITION",       "SOURCE_COMPOSITION_POOLING"},
            {"BACKFILL",                   "SOURCE_BACKFILL"},
        };
        const char *auth_kind = NULL;
        Py_ssize_t i;
        for (i = 0; i < (Py_ssize_t)(sizeof(KINDS) / sizeof(KINDS[0])); i++) {
            if (strcmp(R->relation_kind, KINDS[i].kind) == 0) { auth_kind = KINDS[i].auth; break; }
        }
        if (!auth_kind) {
            PyMem_Free(op);
            return stb_authz(DEFAULT_RELATION_STATE,
                "descriptive relation cannot authorize an operation");
        }
        {
            PyObject *osc = PyObject_GetAttrString(R->rel, "operation_scope");
            PyObject *tuse = PyObject_GetAttrString(R->rel, "target_use");
            Py_ssize_t si;
            if (!osc || !tuse) { Py_XDECREF(osc); Py_XDECREF(tuse); PyMem_Free(op); return -1; }
            for (si = 0; si < PyTuple_Size(R->sources); si++) {
                PyObject *src = PyTuple_GET_ITEM(R->sources, si);
                PyObject *kw = Py_BuildValue("{s:s,s:s,s:s,s:O,s:O,s:O}",
                    "authority_kind", auth_kind,
                    "operation", op,
                    "object_family", "SourceUniverseRelation",
                    "source_universe_ref", src,
                    "target_use_ref", tuse,
                    "predicate_or_risk_set_ref", osc);
                PyObject *args, *res;
                if (!kw) { Py_DECREF(osc); Py_DECREF(tuse); PyMem_Free(op); return -1; }
                /* HQ246-B2 REPAIR: PyObject_Call(callable, args, kwargs) requires `args`
                 * to be a TUPLE of positional arguments and `kwargs` to be a DICT.
                 * require_positive_authority takes the snapshot as its FIRST POSITIONAL
                 * argument, so args must be the 1-tuple (snapshot,). The previous code
                 * passed the snapshot object itself as `args`, which is malformed. */
                args = PyTuple_Pack(1, S->snap);
                if (!args) { Py_DECREF(kw); Py_DECREF(osc); Py_DECREF(tuse);
                             PyMem_Free(op); return -1; }
                res = PyObject_Call(self->t_require_positive, args, kw);
                Py_DECREF(args);
                Py_DECREF(kw);
                if (!res) {
                    /* HQ246-B3 REPAIR: fetch the full 3-slot exception, NORMALISE it,
                     * read the message from the NORMALISED value, and release every
                     * owned reference including the traceback. */
                    PyObject *pt = NULL, *pv = NULL, *tb = NULL, *msg = NULL;
                    const char *ms;
                    PyErr_Fetch(&pt, &pv, &tb);
                    PyErr_NormalizeException(&pt, &pv, &tb);
                    if (pv) {
                        msg = PyObject_Str(pv);
                        if (!msg) PyErr_Clear();
                    }
                    ms = msg ? PyUnicode_AsUTF8(msg) : NULL;
                    (void)stb_authz(STATE_UNKNOWN,
                        ms ? ms : "positive authority requirement failed");
                    Py_XDECREF(msg);
                    Py_XDECREF(pt);
                    Py_XDECREF(pv);
                    Py_XDECREF(tb);
                    Py_DECREF(osc); Py_DECREF(tuse); PyMem_Free(op);
                    return -1;
                }
                Py_DECREF(res);
            }
            Py_DECREF(osc); Py_DECREF(tuse);
        }
    }

    *out_op = op;
    *out_snap_hash = xstrdup(S->content_hash);
    *out_auth = S->authority_ref_dict;
    Py_INCREF(S->authority_ref_dict);
    return 0;
}

/* --------------------------------------------------------- decision ladder */

/* Build the canonical decision preimage dict, byte-identical to
 * _relation_decision_replay_identity's input, and return it (new reference). */
static PyObject *build_replay_preimage(StageBOwner *self, const char *relation_kind,
    PyObject *sources, PyObject *operation_scope, const char *target_use,
    PyObject *effective_scope, PyObject *directionality, const char *state_value,
    PyObject *relation_ref, PyObject *authority_ref, const char *authority_operation,
    const char *snap_hash)
{
    PyObject *d = NULL, *req = NULL, *rk = NULL, *tu = NULL, *st = NULL;
    PyObject *ar = NULL, *ao = NULL, *och = NULL, *ash = NULL, *v;

    /* "request" is the exact _relation_key_material mapping */
    rk = PyUnicode_FromString(relation_kind);
    tu = PyUnicode_FromString(target_use);
    if (!rk || !tu) goto fail;
    {
        const char *keys[] = {"relation_kind", "source_universe_refs", "operation_scope",
            "target_use", "effective_scope", "directionality_or_symmetric", NULL};
        PyObject *vals[6];
        vals[0] = rk; vals[1] = sources; vals[2] = operation_scope;
        vals[3] = tu; vals[4] = effective_scope; vals[5] = directionality;
        req = mkdict(keys, vals);
    }
    if (!req) goto fail;

    st = PyUnicode_FromString(state_value);
    if (relation_ref) { ar = relation_ref; Py_INCREF(ar); }
    else { ar = Py_None; Py_INCREF(ar); }
    if (authority_ref) { ao = authority_ref; Py_INCREF(ao); }
    else { ao = Py_None; Py_INCREF(ao); }
    if (authority_operation) { v = PyUnicode_FromString(authority_operation); }
    else { v = Py_None; Py_INCREF(Py_None); }
    {
        PyObject *authority_operation_val = v;
        och = PyUnicode_FromString(self->custody_hash);
        ash = snap_hash ? PyUnicode_FromString(snap_hash) : (Py_INCREF(Py_None), Py_None);
        if (!st || !och || !ash) goto fail;
        {
            const char *keys[] = {"contract", "request", "state", "relation_ref",
                "authority_ref", "authority_operation", "owner_custody_hash",
                "authority_snapshot_content_hash", NULL};
            PyObject *vals[8];
            vals[0] = PyUnicode_FromString(STAGE_B_CONTRACT);
            vals[1] = req;
            vals[2] = st;
            vals[3] = ar;
            vals[4] = ao;
            vals[5] = authority_operation_val;
            vals[6] = och;
            vals[7] = ash;
            d = mkdict(keys, vals);
            Py_DECREF(vals[0]);
            Py_DECREF(authority_operation_val);
        }
    }
    goto done;
fail:
    Py_XDECREF(d);
    d = NULL;
done:
    Py_XDECREF(rk); Py_XDECREF(tu); Py_XDECREF(st);
    Py_XDECREF(ar); Py_XDECREF(ao); Py_XDECREF(och); Py_XDECREF(ash);
    Py_XDECREF(req);
    return d;
}

/* Assemble the native decision record returned to Python. */
static PyObject *mk_decision(StageBOwner *self, const char *relation_kind,
    PyObject *sources, PyObject *operation_scope, const char *target_use,
    PyObject *effective_scope, PyObject *directionality, const char *state_value,
    PyObject *relation_ref, PyObject *authority_ref, const char *authority_operation,
    const char *reason, const char *snap_hash)
{
    PyObject *pre = NULL, *h = NULL, *out = NULL, *k;
    PyObject *kind_s = NULL, *use_s = NULL, *state_s = NULL, *reason_s = NULL;
    PyObject *och_s = NULL, *ash_s = NULL, *ao_s = NULL, *rr = NULL, *ar = NULL;

    pre = build_replay_preimage(self, relation_kind, sources, operation_scope, target_use,
                                effective_scope, directionality, state_value,
                                relation_ref, authority_ref, authority_operation, snap_hash);
    if (!pre) return NULL;
    h = trusted_hash(self, pre);
    Py_DECREF(pre);
    if (!h) return NULL;

    kind_s  = PyUnicode_FromString(relation_kind);
    use_s   = PyUnicode_FromString(target_use);
    state_s = PyUnicode_FromString(state_value);
    reason_s= PyUnicode_FromString(reason);
    och_s   = PyUnicode_FromString(self->custody_hash);
    ash_s   = snap_hash ? PyUnicode_FromString(snap_hash) : (Py_INCREF(Py_None), Py_None);
    ao_s    = authority_operation ? PyUnicode_FromString(authority_operation)
                                   : (Py_INCREF(Py_None), Py_None);
    /* relation_ref / authority_ref are BORROWED parameters of mk_decision: the caller
     * still owns them. Do NOT decref them here; only the Py_None placeholders created
     * below are owned by this function. (An unconditional Py_XDECREF here released a
     * caller-owned reference.) */
    rr      = relation_ref ? relation_ref : (Py_INCREF(Py_None), Py_None);
    ar      = authority_ref ? authority_ref : (Py_INCREF(Py_None), Py_None);
    if (!kind_s || !use_s || !state_s || !reason_s || !och_s || !ash_s || !ao_s
        || !rr || !ar) goto done;

    out = PyDict_New();
    if (!out) goto done;
#define SET(kk, vv) do { k = PyUnicode_FromString(kk); \
        if (!k || PyDict_SetItem(out, k, (vv)) < 0) { Py_XDECREF(k); Py_DECREF(out); \
            out = NULL; goto done; } Py_DECREF(k); } while (0)
    SET("state", state_s);
    SET("relation_kind", kind_s);
    SET("source_universe_refs", sources);
    SET("operation_scope", operation_scope);
    SET("target_use", use_s);
    SET("effective_scope", effective_scope);
    SET("directionality_or_symmetric", directionality);
    SET("reason", reason_s);
    SET("relation_ref", rr);
    SET("authority_ref", ar);
    SET("authority_operation", ao_s);
    SET("owner_custody_hash", och_s);
    SET("authority_snapshot_content_hash", ash_s);
    SET("replay_identity", h);
#undef SET
    {
        /* authorized == (state == AUTHORIZED and relation_ref is not None) */
        PyObject *b = PyBool_FromLong(strcmp(state_value, STATE_AUTHORIZED) == 0 &&
                                      !(relation_ref == NULL));
        if (!b) { Py_DECREF(out); out = NULL; goto done; }
        k = PyUnicode_FromString("authorized");
        if (!k || PyDict_SetItem(out, k, b) < 0) {
            Py_XDECREF(k); Py_DECREF(b); Py_DECREF(out); out = NULL; goto done;
        }
        Py_DECREF(k); Py_DECREF(b);
    }
done:
    Py_XDECREF(h); Py_XDECREF(kind_s); Py_XDECREF(use_s); Py_XDECREF(state_s);
    Py_XDECREF(reason_s); Py_XDECREF(och_s); Py_XDECREF(ash_s); Py_XDECREF(ao_s);
    /* rr / ar are borrowed unless they are the Py_None placeholders created above. */
    if (!relation_ref) Py_XDECREF(rr);
    if (!authority_ref) Py_XDECREF(ar);
    return out;
}

/* Full native _decide_from_owner_state port: the complete ladder and the exact
 * CONFLICTING_AUTHORITY precedence order. No positive outcome is delegated. */
static PyObject *
stb_decide(StageBOwner *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"relation_kind", "source_universe_refs", "operation_scope",
        "target_use", "effective_scope", "directionality_or_symmetric", "relation_ref",
        "expected_authority_operation", NULL};
    PyObject *relation_kind = NULL, *srcs_in = NULL, *operation_scope = NULL;
    PyObject *target_use = NULL, *effective_scope = NULL, *directionality = NULL;
    PyObject *relation_ref = NULL, *expected_op = NULL;
    const char *rk_s, *tu_s;
    PyObject *sources = NULL, *osc = NULL, *eff = NULL, *dir = NULL;
    char *key = NULL;
    Py_ssize_t i;
    PyObject *cands = NULL;
    char *neg[64];
    Py_ssize_t n_neg = 0, n_pos = 0;
    char *pos_op = NULL, *pos_snap = NULL;
    PyObject *pos_auth = NULL, *pos_ref = NULL;
    PyObject *out = NULL, *tmp_list = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOOO|OOO:decide", kwlist,
        &relation_kind, &srcs_in, &operation_scope, &target_use, &effective_scope,
        &directionality, &relation_ref, &expected_op)) return NULL;

    if (!self->sealed)
        return (stb_integrity("stage B owner is not sealed"), NULL);
    /* PyArg_ParseTupleAndKeywords leaves an ABSENT optional argument as NULL, not
     * Py_None. Every absent/None value must be normalised here or a NULL would be
     * handed to the trusted seam as "no argument". */
    if (!relation_kind || relation_kind == Py_None ||
        !target_use || target_use == Py_None)
        return (stb_integrity("relation_kind and target_use are required"), NULL);
    if (!operation_scope || operation_scope == Py_None ||
        !effective_scope || effective_scope == Py_None)
        return (stb_integrity("operation_scope and effective_scope are required"), NULL);
    if (!directionality || directionality == Py_None) {
        directionality = PyUnicode_FromString("SYMMETRIC");
        if (!directionality) return NULL;
    } else {
        /* MEMORY-SAFETY: a caller-supplied directionality arrives BORROWED. The
         * cleanup path unconditionally DECREFs it, so take a real reference here or
         * the caller's object is freed while still live -- observed as EXC_BAD_ACCESS
         * in _PyObject_Malloc on a later call. */
        Py_INCREF(directionality);
    }
    if (!relation_ref || relation_ref == Py_None) {
        Py_XDECREF(relation_ref);
        relation_ref = NULL;
    } else Py_INCREF(relation_ref);
    if (!expected_op || expected_op == Py_None) {
        Py_XDECREF(expected_op);
        expected_op = NULL;
    } else Py_INCREF(expected_op);

    /* HQ246-B4 REPAIR: the exact-key request fields must be REAL unicode before any
     * PyUnicode_AsUTF8 call. Previously a non-str relation_kind or target_use reached
     * PyUnicode_AsUTF8 and produced NULL, which was then passed to PyUnicode_FromFormat /
     * strcmp -- undefined behaviour and a crash path. A malformed replay request now
     * raises an exact typed integrity error instead. */
    if (!PyUnicode_Check(relation_kind)) {
        PyErr_SetString(STBIntegrityError,
            "stage B relation_kind must be an exact str for an exact relation key");
        goto fail;
    }
    if (!PyUnicode_Check(target_use)) {
        PyErr_SetString(STBIntegrityError,
            "stage B target_use must be an exact str for an exact relation key");
        goto fail;
    }
    rk_s = PyUnicode_AsUTF8(relation_kind);
    tu_s = PyUnicode_AsUTF8(target_use);
    if (!rk_s || !tu_s) {
        PyErr_SetString(STBIntegrityError,
            "stage B relation_kind and target_use must be encodable unicode");
        goto fail;
    }

    /* canonical ordered source refs (>= 2), reused from an admitted relation when the
     * request refs match exactly one sealed relation's ordered source set */
    {
        Py_ssize_t cnt = 0;
        PyObject *seq = srcs_in;
        if (PyList_CheckExact(seq) || PyTuple_CheckExact(seq)) {
            PyObject *raw = PySequence_Fast(seq, "source_universe_refs");  /* owned */
            if (!raw) goto fail;
            for (i = 0; i < PySequence_Fast_GET_SIZE(raw); i++) {
                PyObject *one = PySequence_Fast_GET_ITEM(raw, i);
                PyObject *k1 = exact_key_of(one);
                PyObject *d1;
                if (!k1) { Py_DECREF(raw); goto fail; }
                Py_DECREF(k1);
                d1 = ref_dict_copy(one);
                if (!d1) { Py_DECREF(raw); goto fail; }
                if (!tmp_list) {
                    tmp_list = PyList_New(0);
                    if (!tmp_list) { Py_DECREF(d1); Py_DECREF(raw); goto fail; }
                }
                {
                    /* store (exact_key, ref_dict) so the sort is by KEY: two ref dicts
                     * are not mutually orderable in C. */
                    PyObject *ks = exact_key_of(one);
                    PyObject *pr;
                    if (!ks) { Py_DECREF(d1); Py_DECREF(raw); goto fail; }
                    pr = Py_BuildValue("(sO)", PyUnicode_AsUTF8(ks), d1);
                    Py_DECREF(ks); Py_DECREF(d1);
                    if (!pr) { Py_DECREF(raw); goto fail; }
                    if (PyList_Append(tmp_list, pr) < 0) {
                        Py_DECREF(pr); Py_DECREF(raw); goto fail;
                    }
                    Py_DECREF(pr);
                }
                cnt++;
            }
            /* `raw` is released exactly ONCE here and cleared, so no later error path
             * can double free it. */
            Py_CLEAR(raw);
            if (cnt < 2) {
                stb_integrity("source relation requires at least two exact source universes");
                goto fail;
            }
            if (PyList_Sort(tmp_list) < 0) goto fail;
            /* HQ247-OPEN-001 REPAIR: the previous implementation materialised THREE
             * parallel lists (tmp_list of (key,dict) pairs, then keys[] and vals[]) and
             * then handed the ordered dicts to PyList_AsTuple. That double bookkeeping
             * leaked ~15 pymalloc blocks per decide() call. There is now a single sorted
             * pass that appends each ordered ref dict exactly once, skipping adjacent
             * duplicate keys, and PyList_AsTuple receives the list that owns exactly one
             * reference per element and is consumed exactly once. */
            {
                PyObject *ordered = PyList_New(0);
                char *prev_key = NULL;      /* owned copy, never a borrowed pointer */
                if (!ordered) goto fail;
                for (i = 0; i < PyList_Size(tmp_list); i++) {
                    PyObject *pr = PyList_GetItem(tmp_list, i);   /* borrowed */
                    PyObject *keystr = PySequence_GetItem(pr, 0); /* owned */
                    PyObject *dv = PySequence_GetItem(pr, 1);     /* owned */
                    int dup = 0;
                    if (!keystr || !dv || !PyUnicode_Check(keystr)) {
                        Py_XDECREF(keystr); Py_XDECREF(dv);
                        PyMem_Free(prev_key); Py_DECREF(ordered);
                        goto fail;
                    }
                    if (prev_key && strcmp(prev_key, PyUnicode_AsUTF8(keystr)) == 0)
                        dup = 1;
                    if (!dup) {
                        if (PyList_Append(ordered, dv) < 0) {
                            Py_XDECREF(keystr); Py_XDECREF(dv);
                            PyMem_Free(prev_key); Py_DECREF(ordered);
                            goto fail;
                        }
                        PyMem_Free(prev_key);
                        prev_key = xstrdup(PyUnicode_AsUTF8(keystr));
                        if (!prev_key) {
                            Py_XDECREF(keystr); Py_XDECREF(dv);
                            Py_DECREF(ordered);
                            goto fail;
                        }
                    }
                    Py_XDECREF(keystr);
                    Py_XDECREF(dv);
                }
                PyMem_Free(prev_key);
                Py_CLEAR(tmp_list);
                /* PyList_AsTuple CONSUMES the `ordered` reference; `sources` therefore
                 * owns exactly the references the returned tuple needs. */
                sources = PyList_AsTuple(ordered);
                if (!sources) goto fail;
            }
        } else { stb_integrity("source_universe_refs must be a list or tuple"); goto fail; }
    }

    osc = trusted_canon(self, operation_scope);
    eff = trusted_canon(self, effective_scope);
    dir = trusted_canon(self, directionality);
    if (!osc || !eff || !dir) goto fail;

    if (compute_relation_key(self, rk_s, sources, osc, tu_s, eff, dir, &key) < 0)
        goto fail;

    /* candidate selection: exact by_key match, or exact ref resolution + object key */
    cands = PyList_New(0);
    if (!cands) goto fail;
    if (relation_ref == NULL) {
        for (i = 0; i < self->n_rels; i++) {
            if (strcmp(self->rels[i].object_key, key) == 0) {
                PyObject *ix = PyLong_FromSsize_t(i);
                if (!ix || PyList_Append(cands, ix) < 0) { Py_XDECREF(ix); goto fail; }
                Py_DECREF(ix);
            }
        }
    } else {
        PyObject *cand = stb_resolve_exact(self, relation_ref);
        if (!cand) goto fail;
        {
            /* The resolved candidate qualifies only when its REAL P07 object key
             * equals the requested relation key. */
            SealedRelation *R = NULL;
            for (i = 0; i < self->n_rels; i++) {
                if (self->rels[i].rel == cand) { R = &self->rels[i]; break; }
            }
            if (R && strcmp(R->object_key, key) == 0) {
                PyObject *ix = PyLong_FromSsize_t(i);
                if (!ix || PyList_Append(cands, ix) < 0) {
                    Py_XDECREF(ix); Py_DECREF(cand); goto fail;
                }
                Py_DECREF(ix);
            }
        }
        Py_DECREF(cand);
    }

    /* unknown relation kind is a hard negative, checked before any custody work */
    if (!is_p07_kind(rk_s))
        return (stb_integrity("unknown P07 relation kind"), NULL);

    /* descriptive kinds never authorize; they report their MATRIX default state */
    if (is_descriptive_kind(rk_s)) {
        char buf[320];
        PyOS_snprintf(buf, sizeof(buf), "%s is descriptive only and never grants "
                     "adjacent relation semantics", rk_s);
        out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir, matrix_default(rk_s),
                          NULL, NULL, NULL, buf, NULL);
        goto cleanup;
    }
    if (PyList_Size(cands) == 0) {
        out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir, DEFAULT_RELATION_STATE,
                          NULL, NULL, NULL,
                          "no exact positive relation receipt for this kind/scope/use", NULL);
        goto cleanup;
    }

    for (i = 0; i < PyList_Size(cands); i++) {
        PyObject *ix = PyList_GetItem(cands, i);
        SealedRelation *R = &self->rels[PyLong_AsSsize_t(ix)];
        if (strcmp(R->decision_value, STATE_AUTHORIZED) == 0) {
            PyObject *auth = NULL;
            char *op = NULL, *sh = NULL;
            if (validate_positive(self, R, expected_op, &auth, &op, &sh) < 0) {
                /* capture the negative STATE and continue the ladder */
                PyObject *pt = NULL, *pv = NULL;
                /* HQ246-B3 REPAIR: fetch all three exception slots, normalise them
                 * together, and release every owned reference INCLUDING the traceback.
                 * Reading `.state` may itself fail, so the error indicator is cleared
                 * defensively before continuing the ladder. */
                PyObject *tb = NULL;
                PyErr_Fetch(&pt, &pv, &tb);
                PyErr_NormalizeException(&pt, &pv, &tb);
                if (pv) {
                    PyObject *sv = PyObject_GetAttrString(pv, "state");
                    PyErr_Clear();
                    if (sv && PyUnicode_Check(sv) && n_neg < 64) {
                        neg[n_neg++] = xstrdup(PyUnicode_AsUTF8(sv));
                    }
                    Py_XDECREF(sv);
                }
                if (n_neg == 0 && n_neg < 64) {
                    neg[n_neg++] = xstrdup(STATE_UNKNOWN);
                }
                PyErr_Clear();
                Py_XDECREF(pt); Py_XDECREF(pv); Py_XDECREF(tb);
                PyMem_Free(op); PyMem_Free(sh); Py_XDECREF(auth);
            } else {
                n_pos++;
                if (n_pos == 1) {
                    pos_ref = R->ref_dict; Py_INCREF(pos_ref);
                    pos_auth = auth;
                    pos_op = op;
                    pos_snap = sh;
                } else { Py_XDECREF(auth); PyMem_Free(op); PyMem_Free(sh); }
            }
        } else if (n_neg < 64) {
            neg[n_neg++] = xstrdup(R->decision_value);
        }
    }

    if (n_pos == 1 && n_neg == 0) {
        out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir, STATE_AUTHORIZED,
                          pos_ref, pos_auth, pos_op,
                          "exact operation-specific relation authority established from "
                          "authenticated owner custody", pos_snap);
        goto cleanup;
    }
    if (n_pos > 1 || (n_pos > 0 && n_neg > 0)) {
        out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir, STATE_CONFLICTING,
                          NULL, NULL, NULL,
                          "multiple or conflicting exact relation dispositions exist", NULL);
        goto cleanup;
    }
    {
        static const char *PRECEDENCE[] = {STATE_CONFLICTING, "EXPIRED_OR_STALE", "DENIED",
            "NOT_APPLICABLE", STATE_UNKNOWN, STATE_OUT_OF_SCOPE, NULL};
        Py_ssize_t p, j;
        for (p = 0; PRECEDENCE[p]; p++) {
            for (j = 0; j < n_neg; j++) {
                if (strcmp(neg[j], PRECEDENCE[p]) == 0) {
                    out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir,
                                      PRECEDENCE[p], NULL, NULL, NULL,
                                      "exact relation receipt is nonpositive or unavailable",
                                      NULL);
                    goto cleanup;
                }
            }
        }
    }
    out = mk_decision(self, rk_s, sources, osc, tu_s, eff, dir, DEFAULT_RELATION_STATE,
                      NULL, NULL, NULL,
                      "no positive exact relation authority established", NULL);

cleanup:
    for (i = 0; i < n_neg; i++) PyMem_Free(neg[i]);
    PyMem_Free(key); PyMem_Free(pos_op); PyMem_Free(pos_snap);
    Py_XDECREF(pos_auth); Py_XDECREF(pos_ref);
    Py_XDECREF(tmp_list);
    Py_XDECREF(cands); Py_XDECREF(sources); Py_XDECREF(osc); Py_XDECREF(eff); Py_XDECREF(dir);
    Py_XDECREF(relation_ref); Py_XDECREF(expected_op); Py_XDECREF(directionality);
    return out;

fail:
    for (i = 0; i < n_neg; i++) PyMem_Free(neg[i]);
    PyMem_Free(key); PyMem_Free(pos_op); PyMem_Free(pos_snap);
    Py_XDECREF(pos_auth); Py_XDECREF(pos_ref);
    Py_XDECREF(tmp_list);
    Py_XDECREF(cands); Py_XDECREF(sources); Py_XDECREF(osc); Py_XDECREF(eff); Py_XDECREF(dir);
    Py_XDECREF(relation_ref); Py_XDECREF(expected_op); Py_XDECREF(directionality);
    return NULL;
}

/* --------------------------------------------------- require + replay validate */

/* require(): native positive-authority gate. Returns the canonical positive material
 * or raises. Implemented natively; never delegates a positive decision to Python. */
static PyObject *
stb_require(StageBOwner *self, PyObject *args, PyObject *kwds)
{
    PyObject *res = stb_decide(self, args, kwds);
    if (!res) return NULL;
    {
        PyObject *st = PyDict_GetItemString(res, "state");
        PyObject *s = st ? PyUnicode_FromString(PyUnicode_AsUTF8(st)) : NULL;
        if (!s) { PyErr_SetString(STBIntegrityError,
            "stage B require produced a decision without an exact state"); Py_DECREF(res); return NULL; }
        if (strcmp(PyUnicode_AsUTF8(s), STATE_AUTHORIZED) != 0) {
            PyObject *rsn = PyDict_GetItemString(res, "reason");
            PyErr_SetString(STBAuthzError,
                rsn ? PyUnicode_AsUTF8(rsn) : "no positive exact relation authority");
            Py_DECREF(s); Py_DECREF(res);
            return NULL;
        }
        Py_DECREF(s);
        return res;
    }
}

/* validate_decision_replay(): native port of validate_relation_decision_replay_identity. */
static PyObject *
stb_validate_replay(StageBOwner *self, PyObject *decision)
{
    PyObject *d = NULL, *pre = NULL, *h = NULL, *st = NULL;
    const char *state_s;
    int is_auth = 0, has_snap = 0;

    if (!PyDict_Check(decision))
        return (stb_integrity("owner decision must be an exact native decision dict"), NULL);
    if (!self->sealed)
        return (stb_integrity("stage B owner is not sealed"), NULL);

    st = PyDict_GetItemString(decision, "state");
    if (!st || !PyUnicode_Check(st))
        return (stb_integrity("owner decision lacks an exact state"), NULL);
    state_s = PyUnicode_AsUTF8(st);

    {
        PyObject *och = PyDict_GetItemString(decision, "owner_custody_hash");
        const char *o = och ? PyUnicode_AsUTF8(och) : NULL;
        if (!och || !PyUnicode_Check(och) || !is_hex64(o))
            return (stb_integrity("owner decision lacks exact custody identity"), NULL);
        if (strcmp(o, self->custody_hash) != 0)
            return (stb_integrity("owner decision custody identity does not match native "
                                  "owner custody"), NULL);
    }
    {
        PyObject *sh = PyDict_GetItemString(decision, "authority_snapshot_content_hash");
        if (sh && sh != Py_None) {
            const char *o = PyUnicode_Check(sh) ? PyUnicode_AsUTF8(sh) : NULL;
            if (!o || !is_hex64(o))
                return (stb_integrity("owner decision authority snapshot semantic identity "
                                      "is malformed"), NULL);
            has_snap = 1;
        }
    }
    is_auth = (strcmp(state_s, STATE_AUTHORIZED) == 0);
    if (is_auth && !has_snap)
        return (stb_integrity("authorized owner decision lacks exact authority snapshot "
                              "semantic identity"), NULL);

    {
        PyObject *g[13];
        const char *names[11];
        int i = 0;
        static const char *NEED[11] = {"state", "relation_kind", "source_universe_refs",
            "operation_scope", "target_use", "effective_scope",
            "directionality_or_symmetric", "relation_ref", "authority_ref",
            "authority_operation", "authority_snapshot_content_hash"};
        for (i = 0; i < 11; i++) {
            names[i] = NEED[i];
            g[i] = PyDict_GetItemString(decision, NEED[i]);
            if (!g[i]) return (stb_integrity("owner decision is missing canonical preimage "
                                             "material"), NULL);
        }
        /* HQ246-B4 REPAIR: the replay preimage's relation_kind and target_use must be
         * real unicode before they are converted, so a malformed decision dict yields a
         * typed integrity error rather than a NULL dereference. */
        {
            PyObject *rko = PyDict_GetItemString(decision, "relation_kind");
            PyObject *tuo = PyDict_GetItemString(decision, "target_use");
            if (!rko || !PyUnicode_Check(rko))
                return (stb_integrity("owner decision replay relation_kind is not an "
                                      "exact str"), NULL);
            if (!tuo || !PyUnicode_Check(tuo))
                return (stb_integrity("owner decision replay target_use is not an "
                                      "exact str"), NULL);
            g[11] = rko;
            g[12] = tuo;
        }
        pre = build_replay_preimage(self,
            PyUnicode_AsUTF8(g[11]),
            g[2], g[3], PyUnicode_AsUTF8(g[12]), g[5], g[6], state_s,
            g[7] == Py_None ? NULL : g[7], g[8] == Py_None ? NULL : g[8],
            (g[9] == Py_None) ? NULL : PyUnicode_AsUTF8(g[9]),
            (g[10] == Py_None) ? NULL : PyUnicode_AsUTF8(g[10]));
        if (!pre) return NULL;
    }
    h = trusted_hash(self, pre);
    Py_DECREF(pre);
    if (!h) return NULL;
    {
        PyObject *ri = PyDict_GetItemString(decision, "replay_identity");
        if (!ri || !PyUnicode_Check(ri) || strcmp(PyUnicode_AsUTF8(ri),
                                                  PyUnicode_AsUTF8(h)) != 0) {
            Py_DECREF(h);
            return (stb_integrity("owner decision replay identity is stale or corrupt"), NULL);
        }
    }
    Py_DECREF(h);
    d = decision; Py_INCREF(d);
    return d;
}

/* ----------------------------------------------------------------- type */

static PyObject *stb_no_copy(PyObject *self, PyObject *unused)
{ (void)self; PyErr_SetString(PyExc_TypeError,
    "native Stage B owner custody cannot be copied"); return NULL; }
static PyObject *stb_no_reduce(PyObject *self, PyObject *unused)
{ (void)self; PyErr_SetString(PyExc_TypeError,
    "native Stage B owner custody cannot be reconstructed"); return NULL; }
static PyObject *stb_no_setattr(PyObject *self, PyObject *args)
{ PyObject *n; (void)self;
  if (!PyArg_ParseTuple(args, "O:__setattr__", &n)) return NULL;
  PyErr_Format(PyExc_AttributeError,
    "native Stage B owner custody attributes are immutable: %R", n); return NULL; }

static PyObject *stb_get_custody(StageBOwner *self, void *c)
{ (void)c;
  if (!self->sealed || !self->custody_hash) {
    stb_integrity("stage B owner is not sealed"); return NULL; }
  return PyUnicode_FromString(self->custody_hash); }
static PyObject *stb_get_sealed(StageBOwner *self, void *c)
{ (void)c; return PyBool_FromLong(self->sealed); }
/* D7 EVIDENCE: the trusted TCB is native-owned. These expose the pinned identities for
 * harness assertions WITHOUT allowing any re-binding. */
static PyObject *stb_get_trusted_seam(StageBOwner *self, void *c)
{
    (void)c;
    if (!self->sealed)
        return (stb_integrity("stage B owner is not sealed"), NULL);
    return Py_BuildValue("(OOO)",
        self->t_semantic_hash, self->t_canonicalize, self->t_require_positive);
}
static PyObject *stb_get_counts(StageBOwner *self, void *c)
{ (void)c; return Py_BuildValue("(nn)", (Py_ssize_t)self->n_rels,
                                (Py_ssize_t)self->n_snaps); }

static PyMethodDef StageB_methods[] = {
    {"resolve_exact", (PyCFunction)stb_resolve_exact, METH_O,
     "Full exact resolve: key lookup + semantic_projection re-hash + replay verification."},
    {"decide", (PyCFunction)stb_decide, METH_VARARGS | METH_KEYWORDS,
     "Full native P07 adjudication: complete state ladder + CONFLICTING_AUTHORITY precedence."},
    {"require", (PyCFunction)stb_require, METH_VARARGS | METH_KEYWORDS,
     "Native positive-authority gate."},
    {"validate_decision_replay", (PyCFunction)stb_validate_replay, METH_O,
     "Native decision replay-identity authentication."},
    {"__copy__", (PyCFunction)stb_no_copy, METH_NOARGS, "Always fails."},
    {"__deepcopy__", (PyCFunction)stb_no_copy, METH_O, "Always fails."},
    {"__reduce__", (PyCFunction)stb_no_reduce, METH_NOARGS, "Always fails."},
    {"__reduce_ex__", (PyCFunction)stb_no_reduce, METH_VARARGS, "Always fails."},
    {"__setattr__", (PyCFunction)stb_no_setattr, METH_VARARGS, "Always fails."},
    {NULL, NULL, 0, NULL}
};
static PyGetSetDef StageB_getset[] = {
    {"sealed", (getter)stb_get_sealed, NULL, "True once one-shot custody sealed.", NULL},
    {"custody_hash", (getter)stb_get_custody, NULL,
     "Accepted P07 canonical semantic custody hash.", NULL},
    {"counts", (getter)stb_get_counts, NULL, "(n_relations, n_authority_snapshots).", NULL},
    {"trusted_seam", (getter)stb_get_trusted_seam, NULL,
     "Read-only tuple of the three pinned trusted callables (identity evidence).", NULL},
    {NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject StageBOwnerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "rawlsing_next._p07_native_owner_stage_b.StageBOwner",
    .tp_basicsize = sizeof(StageBOwner),
    .tp_dealloc = (destructor)StageBOwner_dealloc,
    /* D5: Py_TPFLAGS_HAVE_GC activates tp_traverse/tp_clear. Py_TPFLAGS_BASETYPE is
     * intentionally ABSENT -> NON-SUBCLASSABLE. */
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .tp_traverse = (traverseproc)StageBOwner_traverse,
    .tp_clear = (inquiry)StageBOwner_clear,
    .tp_doc = "HQ245 Stage B native P07 full adjudicator prototype (quarantined).",
    .tp_methods = StageB_methods,
    .tp_getset = StageB_getset,
    .tp_init = (initproc)StageBOwner_init,
    .tp_new = PyType_GenericNew,
};

static PyMethodDef module_methods[] = {{NULL, NULL, 0, NULL}};
static struct PyModuleDef stagebmodule = {
    PyModuleDef_HEAD_INIT,
    "rawlsing_next._p07_native_owner_stage_b",
    "HQ245 Stage B native P07 full adjudicator prototype. QUARANTINED, NON-PRODUCTION. "
    "Not imported by production P07/F7 and not an adopted authority.",
    -1, module_methods, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__p07_native_owner_stage_b(void)
{
    PyObject *m;
    if (PyType_Ready(&StageBOwnerType) < 0) return NULL;
    m = PyModule_Create(&stagebmodule);
    if (!m) return NULL;

    STBIntegrityError = PyErr_NewException(
        "rawlsing_next._p07_native_owner_stage_b.SourceRelationIntegrityError", NULL, NULL);
    STBAuthzError = PyErr_NewException(
        "rawlsing_next._p07_native_owner_stage_b.SourceRelationAuthorizationError", NULL, NULL);
    /* D4 REPAIR: every PyModule_AddObject return is checked. On failure the module is
     * discarded and only the references THIS function still owns are released; the
     * failing AddObject's partially-added object is not released twice. */
    if (!STBIntegrityError || !STBAuthzError) { Py_DECREF(m); return NULL; }
    Py_INCREF(STBIntegrityError); Py_INCREF(STBAuthzError);
    if (PyModule_AddObject(m, "SourceRelationIntegrityError",
                           STBIntegrityError) < 0) {
        Py_DECREF(STBIntegrityError);
        Py_DECREF(STBAuthzError);
        Py_DECREF(m);
        return NULL;
    }
    if (PyModule_AddObject(m, "SourceRelationAuthorizationError",
                           STBAuthzError) < 0) {
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&StageBOwnerType);
    if (PyModule_AddObject(m, "StageBOwner", (PyObject *)&StageBOwnerType) < 0) {
        Py_DECREF(&StageBOwnerType);
        Py_DECREF(m);
        return NULL;
    }

    PyModule_AddStringConstant(m, "STAGE_B_CONTRACT", STAGE_B_CONTRACT);
    PyModule_AddStringConstant(m, "STAGE", "B");
    PyModule_AddIntConstant(m, "PRODUCTION_INTEGRATED", 0);
    PyModule_AddIntConstant(m, "SUBCLASSABLE", 0);
    PyModule_AddIntConstant(m, "TRUSTED_SEAM", 1);
    return m;
}
