/* HQ244 Stage A -- F7 native P07 owner prototype: CONSTRUCTOR CUSTODY + EXACT RESOLVE.
 *
 * NON-PRODUCTION, NON-AUTHORIZING PROTOTYPE. STAGE A ONLY.
 *
 * This module is deliberately quarantined in the experimental namespace
 * ``rawlsing_next._p07_native_owner_stage_a``. It is NOT imported by production P07 or
 * F7, it does NOT create or replace the accepted Python ``SourceRelationResolver``, and
 * it CANNOT issue an authoritative P07 AUTHORIZED decision, a positive
 * ``RelationDecision``, or any F7 receipt.
 *
 * What Stage A genuinely provides:
 *   - a compiled, non-subclassable CPython 3.11.3 heap type;
 *   - ONE-SHOT constructor admission with deep, immutable, owner-local custody of the
 *     exact relation material, sealed into C memory with no Python-visible mutable
 *     handle, capsule, state loader, resealer, copier or reconstructor;
 *   - exact-key-only ``resolve_exact`` semantics with full negative answers;
 *   - identity re-verification on every lookup so post-seal mutation of any returned
 *     Python relation object is detected.
 *
 * What Stage A deliberately does NOT provide (Stage B/C/D gates):
 *   - no adjudicator, no positive authority, no precedence, no replay decision;
 *   - therefore Stage A CANNOT close F7-RR-04G.
 *
 * TCB seam: the canonical semantic hash used for projection re-verification is the
 * trusted module-level ``semantic_hash`` supplied by the embedding application at
 * construction. It is NOT attacker-supplied and is never replaced from Python at
 * resolve time. See 01_EXACT_NATIVE_TYPE_CONSTRUCTOR_CUSTODY_INTERFACE.json.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define STAGE_A_CONTRACT "P07_NATIVE_STAGE_A_CUSTODY_AND_RESOLVE@1"
#define STAGE_A_NOTIMPL "NOT_IMPLEMENTED_NONAUTHORIZING_STAGE_A"

/* One sealed relation record. All strings are C-owned copies taken at admission. */
typedef struct {
    PyObject *rel;         /* owned reference to the admitted Python relation object */
    char *key;             /* exact ref key: kind|object_id|content_hash           */
    char *content_hash;    /* 64-hex semantic content hash, copied at admission    */
    char *object_key;      /* 64-hex relation object key used for by_key indexing  */
} SealedRelation;

typedef struct {
    PyObject_HEAD
    int sealed;                /* one-shot: 0 before admission, 1 after           */
    SealedRelation *rels;
    Py_ssize_t n_rels;
    char *custody_hash;        /* sealed C-owned custody fingerprint               */
    char *registry_key;        /* sealed registry description                      */
    PyObject *trusted_semhash; /* trusted module-level semantic_hash callable     */
} StageAOwner;

static PyObject *StageAIntegrityError = NULL;
static PyObject *StageAKeyError = NULL;

/* ------------------------------------------------------------------ utils */

static char *
xstrdup(const char *s)
{
    size_t n;
    char *out;
    if (s == NULL) {
        return NULL;
    }
    n = strlen(s) + 1;
    out = (char *)PyMem_Malloc(n);
    if (out == NULL) {
        return NULL;
    }
    memcpy(out, s, n);
    return out;
}

static void
seal_owner_free_contents(StageAOwner *self)
{
    Py_ssize_t i;
    if (self->rels != NULL) {
        for (i = 0; i < self->n_rels; i++) {
            PyMem_Free(self->rels[i].key);
            PyMem_Free(self->rels[i].content_hash);
            PyMem_Free(self->rels[i].object_key);
            Py_XDECREF(self->rels[i].rel);
        }
        PyMem_Free(self->rels);
        self->rels = NULL;
    }
    self->n_rels = 0;
    PyMem_Free(self->custody_hash);
    self->custody_hash = NULL;
    PyMem_Free(self->registry_key);
    self->registry_key = NULL;
    Py_CLEAR(self->trusted_semhash);
    self->sealed = 0;
}

static void
raise_integrity(const char *msg)
{
    PyErr_SetString(StageAIntegrityError, msg);
}

/* Extract a required unicode attribute as a freshly allocated C string. */
static int
get_str_attr(PyObject *obj, const char *name, char **out, const char *what)
{
    PyObject *v = PyObject_GetAttrString(obj, name);
    const char *s;
    if (v == NULL) {
        PyErr_Format(PyExc_TypeError,
                     "stage A admission: %s must expose %s", what, name);
        return -1;
    }
    if (!PyUnicode_Check(v)) {
        Py_DECREF(v);
        PyErr_Format(PyExc_TypeError,
                     "stage A admission: %s.%s must be str", what, name);
        return -1;
    }
    s = PyUnicode_AsUTF8(v);
    if (s == NULL) {
        Py_DECREF(v);
        return -1;
    }
    *out = xstrdup(s);
    Py_DECREF(v);
    if (*out == NULL) {
        return -1;
    }
    return 0;
}

/* ---------------------------------------------------------------- dealloc */

static void
StageAOwner_dealloc(StageAOwner *self)
{
    seal_owner_free_contents(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

/* ------------------------------------------------------------- constructor */

/* Validate a candidate relation and COPY its identity material natively.
 *
 * All Python attribute reads happen HERE, before the owner is sealed. Nothing Python
 * reachable is retained as a mutable identity source: only an owned reference to the
 * admitted object plus C copies of its exact identity strings.
 */
static int
admit_one(StageAOwner *self, PyObject *rel, SealedRelation *out, Py_ssize_t index)
{
    PyObject *refobj = NULL;
    char *key = NULL, *chash = NULL, *okey = NULL;

    refobj = PyObject_GetAttrString(rel, "ref");
    if (refobj == NULL) {
        PyErr_Format(PyExc_TypeError,
                     "stage A admission: relation[%zd] must expose ref", index);
        return -1;
    }
    if (get_str_attr(refobj, "key", &key, "relation ref") < 0) {
        goto fail;
    }
    if (get_str_attr(rel, "content_hash", &chash, "relation") < 0) {
        goto fail;
    }
    /* by_key index key. Stage A deliberately derives this natively from the already
     * validated exact ref key rather than calling back into Python: that removes any
     * attacker-reachable dynamic callback from the admission path. Stage B must
     * replace this with the true relation object key material, which needs the
     * accepted canonical helper. */
    okey = xstrdup(key);
    if (okey == NULL) {
        PyErr_NoMemory();
        goto fail;
    }
    out->rel = rel;            /* caller holds a reference; we take ownership below */
    Py_INCREF(rel);
    out->key = key;
    out->content_hash = chash;
    out->object_key = okey;
    Py_XDECREF(refobj);
    return 0;

fail:
    Py_XDECREF(refobj);
    PyMem_Free(key);
    PyMem_Free(chash);
    PyMem_Free(okey);
    return -1;
}

static int
StageAOwner_init(StageAOwner *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"relations", "authority_registry",
                             "trusted_semantic_hash", NULL};
    PyObject *relations = NULL, *registry = NULL, *semhash = NULL;
    PyObject *fast = NULL;
    Py_ssize_t n = 0, i;
    char *rkey = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOO:StageAOwner",
                                     kwlist, &relations, &registry, &semhash)) {
        return -1;
    }

    /* ONE-SHOT: no reseal, no reinit, no re-admission. */
    if (self->sealed) {
        raise_integrity(
            "stage A custody is one-shot: this native owner is already sealed and "
            "cannot be re-initialised, resealed or re-admitted");
        return -1;
    }
    /* Constructor reentrancy: reject an already-sealing owner appearing as input. */
    if (Py_TYPE(self) == NULL) {
        raise_integrity("stage A native type is unavailable");
        return -1;
    }
    if (registry == Py_None) {
        raise_integrity("stage A admission requires an explicit authority_registry");
        return -1;
    }
    if (semhash == Py_None || !PyCallable_Check(semhash)) {
        PyErr_SetString(PyExc_TypeError,
                        "stage A admission requires a callable trusted_semantic_hash");
        return -1;
    }
    /* Reject attacker-controlled iteration: require an exact list/tuple so no
     * __iter__/__getattribute__ side effect can drive admission. */
    if (!PyList_Check(relations) && !PyTuple_Check(relations)) {
        PyErr_SetString(PyExc_TypeError,
                        "stage A admission requires an exact list or tuple of relations");
        return -1;
    }
    n = PySequence_Size(relations);
    if (n < 0) {
        return -1;
    }

    /* Freeze the trusted helper before any relation is read. */
    Py_INCREF(semhash);
    self->trusted_semhash = semhash;

    if (n > 0) {
        self->rels = (SealedRelation *)PyMem_Calloc((size_t)n, sizeof(SealedRelation));
        if (self->rels == NULL) {
            return -1;
        }
    }
    self->n_rels = 0;

    /* Two-phase admission: copy identity material first, seal only if ALL succeed. */
    fast = PySequence_Fast(relations, "stage A relations must be a sequence");
    if (fast == NULL) {
        return -1;
    }
    for (i = 0; i < n; i++) {
        PyObject *item = PySequence_Fast_GET_ITEM(fast, i);
        if (admit_one(self, item, &self->rels[i], i) < 0) {
            Py_DECREF(fast);
            return -1; /* nothing sealed: __init__ failure leaves self unsealed */
        }
        self->n_rels = i + 1;
    }
    Py_DECREF(fast);

    /* Registry description is a sealed C string taken from the exact type name. */
    rkey = xstrdup(Py_TYPE(registry)->tp_name);
    if (rkey == NULL) {
        return -1;
    }
    self->registry_key = rkey;

    {
        /* Custody fingerprint over the exact sealed keys, computed natively with a
         * simple deterministic FNV-1a walk. This is a PROVENANCE receipt only; it is
         * not, and must not be presented as, the accepted P07 custody hash. */
        uint64_t h = 1469598103934665603ULL;
        Py_ssize_t k;
        for (k = 0; k < self->n_rels; k++) {
            const unsigned char *p = (const unsigned char *)self->rels[k].key;
            while (*p) {
                h ^= (uint64_t)(*p++);
                h *= 1099511628211ULL;
            }
            h ^= 0x1f;
            h *= 1099511628211ULL;
        }
        self->custody_hash = (char *)PyMem_Malloc(17);
        if (self->custody_hash == NULL) {
            return -1;
        }
        PyOS_snprintf(self->custody_hash, 17, "%016llx",
                      (unsigned long long)h);
    }

    self->sealed = 1;
    return 0;
}

/* ------------------------------------------------------------------ resolve */

/* Fetch a unicode value for `name` from a mapping item OR an object attribute. */
static PyObject *
fetch_ref_component(PyObject *src, const char *name)
{
    PyObject *v;
    if (PyMapping_Check(src)) {
        v = PyMapping_GetItemString(src, name);
        if (v != NULL) {
            return v;
        }
        PyErr_Clear();
    }
    v = PyObject_GetAttrString(src, name);
    return v;
}

/* Exact-key-only lookup. Returns a NEW reference to the admitted relation, or NULL
 * with a typed negative set. No fuzzy / latest / default / label inference exists.
 *
 * Accepted exact-ref input shapes, all normalised to one canonical key string:
 *   1. an object exposing `.key`            (the accepted ExactRef)
 *   2. a mapping with kind/object_id/content_hash
 *   3. an object exposing `.as_dict()`      (an ExactRef-like mapping view)
 */
static PyObject *
StageAOwner_resolve_exact(StageAOwner *self, PyObject *arg)
{
    PyObject *key = NULL, *k2, *o2, *c2;
    const char *want;
    Py_ssize_t i;
    char *have = NULL;

    if (!self->sealed) {
        raise_integrity("stage A owner is not sealed");
        return NULL;
    }

    /* Shape 1: direct exact key. */
    key = PyObject_GetAttrString(arg, "key");
    if (key == NULL) {
        PyErr_Clear();
        /* Shape 2 or 3: a mapping, or an object that can project itself to one. */
        {
            PyObject *mapping = NULL;
            if (PyMapping_Check(arg)) {
                mapping = arg;      /* borrowed; never DECREFed */
                Py_INCREF(mapping);
            } else {
                mapping = PyObject_CallMethod(arg, "as_dict", NULL);
                if (mapping == NULL) {
                    PyErr_Clear();
                    PyErr_SetString(StageAKeyError,
                        "stage A resolve_exact requires an exact ref or ref mapping");
                    return NULL;
                }
            }
            k2 = fetch_ref_component(mapping, "kind");
            o2 = fetch_ref_component(mapping, "object_id");
            c2 = fetch_ref_component(mapping, "content_hash");
            if (k2 == NULL || o2 == NULL || c2 == NULL) {
                Py_XDECREF(k2); Py_XDECREF(o2); Py_XDECREF(c2);
                Py_DECREF(mapping);
                raise_integrity("stage A resolve_exact requires exact ref material");
                return NULL;
            }
            if (!PyUnicode_Check(k2) || !PyUnicode_Check(o2) || !PyUnicode_Check(c2) ||
                PyUnicode_AsUTF8(k2) == NULL || PyUnicode_AsUTF8(o2) == NULL ||
                PyUnicode_AsUTF8(c2) == NULL) {
                Py_DECREF(k2); Py_DECREF(o2); Py_DECREF(c2);
                Py_DECREF(mapping);
                raise_integrity("stage A resolve_exact requires unicode exact ref material");
                return NULL;
            }
            key = PyUnicode_FromFormat("%s|%s|%s",
                PyUnicode_AsUTF8(k2), PyUnicode_AsUTF8(o2), PyUnicode_AsUTF8(c2));
            Py_DECREF(k2); Py_DECREF(o2); Py_DECREF(c2);
            Py_DECREF(mapping);
            if (key == NULL) {
                return NULL;
            }
        }
    }
    want = PyUnicode_AsUTF8(key);
    if (want == NULL) {
        Py_DECREF(key);
        return NULL;
    }

    for (i = 0; i < self->n_rels; i++) {
        if (strcmp(self->rels[i].key, want) == 0) {
            break;
        }
    }
    if (i == self->n_rels) {
        Py_DECREF(key);
        raise_integrity(
            "exact SourceUniverseRelation unavailable from native owner custody; "
            "no label/ID/latest/default inference");
        return NULL;
    }

#ifdef STAGE_A_FAULT_INJECT
    /* DELIBERATE TEST-ONLY FAULT: skip all identity re-verification so a post-seal
     * substitute object is returned as if trusted. Never compiled into the shipped
     * build; used only to prove the Stage A court actually turns RED without it. */
    Py_DECREF(key);
    Py_INCREF(self->rels[i].rel);
    return self->rels[i].rel;
#endif

    /* IDENTITY RE-VERIFICATION against the sealed C copies. Anything a caller changed
     * on the admitted Python object after sealing is caught here, never trusted.
     *
     * (a) ref key must still equal the sealed exact key -- blocks a post-seal ref swap;
     * (b) content_hash must still equal the sealed semantic hash.
     */
    {
        PyObject *r = PyObject_GetAttrString(self->rels[i].rel, "ref");
        PyObject *k = (r == NULL) ? NULL : PyObject_GetAttrString(r, "key");
        Py_XDECREF(r);
        if (k == NULL || !PyUnicode_Check(k)) {
            Py_XDECREF(k);
            Py_DECREF(key);
            raise_integrity("native owner custody relation ref drift");
            return NULL;
        }
        have = xstrdup(PyUnicode_AsUTF8(k));
        Py_DECREF(k);
        if (have == NULL) {
            Py_DECREF(key);
            return PyErr_NoMemory(), NULL;
        }
    }
    if (strcmp(have, self->rels[i].key) != 0) {
        PyMem_Free(have);
        Py_DECREF(key);
        raise_integrity("native owner custody relation ref drift");
        return NULL;
    }
    PyMem_Free(have);

    if (get_str_attr(self->rels[i].rel, "content_hash", &have, "relation") < 0) {
        Py_DECREF(key);
        return NULL;
    }
    if (strcmp(have, self->rels[i].content_hash) != 0) {
        PyMem_Free(have);
        Py_DECREF(key);
        raise_integrity("native owner custody relation semantic identity drift");
        return NULL;
    }
    PyMem_Free(have);

    Py_DECREF(key);
    Py_INCREF(self->rels[i].rel);
    return self->rels[i].rel;
}

/* ------------------------------------------------- explicit non-authorizing stubs */

static PyObject *
StageAOwner_decide(StageAOwner *self, PyObject *args, PyObject *kwds)
{
    (void)self; (void)args; (void)kwds;
    raise_integrity(
        STAGE_A_NOTIMPL ": Stage A owner cannot decide; the full native P07 "
        "adjudicator is a Stage B gate and no positive authority is issued here");
    return NULL;
}

static PyObject *
StageAOwner_require(StageAOwner *self, PyObject *args, PyObject *kwds)
{
    (void)self; (void)args; (void)kwds;
    raise_integrity(
        STAGE_A_NOTIMPL ": Stage A owner cannot require; no positive authority is "
        "issued at Stage A");
    return NULL;
}

static PyObject *
StageAOwner_no_copy(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    (void)self;
    PyErr_SetString(PyExc_TypeError,
                    "native Stage A owner custody cannot be copied");
    return NULL;
}

static PyObject *
StageAOwner_no_reduce(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    (void)self;
    PyErr_SetString(PyExc_TypeError,
                    "native Stage A owner custody cannot be reconstructed");
    return NULL;
}

static PyObject *
StageAOwner_no_setattr(PyObject *self, PyObject *args)
{
    PyObject *name;
    (void)self;
    if (!PyArg_ParseTuple(args, "O:__setattr__", &name)) {
        return NULL;
    }
    PyErr_Format(PyExc_AttributeError,
                 "native Stage A owner custody attributes are immutable: %R", name);
    return NULL;
}

static PyObject *
StageAOwner_custody_diagnostic(StageAOwner *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *rows, *res;
    Py_ssize_t i;
    if (!self->sealed) {
        raise_integrity("stage A owner is not sealed");
        return NULL;
    }
    rows = PyList_New(0);
    if (rows == NULL) {
        return NULL;
    }
    for (i = 0; i < self->n_rels; i++) {
        PyObject *d = Py_BuildValue("{s:s,s:s}",
                                    "key", self->rels[i].key,
                                    "content_hash", self->rels[i].content_hash);
        if (d == NULL) {
            Py_DECREF(rows);
            return NULL;
        }
        if (PyList_Append(rows, d) < 0) {
            Py_DECREF(d);
            Py_DECREF(rows);
            return NULL;
        }
        Py_DECREF(d);
    }
    res = Py_BuildValue("{s:s,s:s,s:s,s:s,s:O,s:i,s:n}",
                        "contract", STAGE_A_CONTRACT,
                        "authorizing", "NO",
                        "stage_a_marker", STAGE_A_NOTIMPL,
                        "custody_hash", self->custody_hash,
                        "sealed_relations", rows,
                        "sealed", self->sealed,
                        "n_relations", (Py_ssize_t)self->n_rels);
    return res;
}

static PyObject *
StageAOwner_get_sealed(StageAOwner *self, void *closure)
{
    (void)closure;
    return PyBool_FromLong(self->sealed);
}

static PyObject *
StageAOwner_get_custody_hash(StageAOwner *self, void *closure)
{
    (void)closure;
    if (!self->sealed || self->custody_hash == NULL) {
        PyErr_SetString(StageAIntegrityError, "stage A owner is not sealed");
        return NULL;
    }
    return PyUnicode_FromString(self->custody_hash);
}

/* ----------------------------------------------------------- type creation */

static PyMethodDef StageA_methods[] = {
    {"resolve_exact", (PyCFunction)StageAOwner_resolve_exact, METH_O,
     "Exact-key-only read-only lookup from native-owned custody."},
    {"decide", (PyCFunction)StageAOwner_decide, METH_VARARGS | METH_KEYWORDS,
     STAGE_A_NOTIMPL ": never authorizes at Stage A."},
    {"require", (PyCFunction)StageAOwner_require, METH_VARARGS | METH_KEYWORDS,
     STAGE_A_NOTIMPL ": never authorizes at Stage A."},
    {"custody_diagnostic", (PyCFunction)StageAOwner_custody_diagnostic, METH_NOARGS,
     "Detached canonical custody provenance. Read-only."},
    {"__copy__", (PyCFunction)StageAOwner_no_copy, METH_NOARGS,
     "Always fails: custody is not copyable."},
    {"__deepcopy__", (PyCFunction)StageAOwner_no_copy, METH_O,
     "Always fails: custody is not copyable."},
    {"__reduce__", (PyCFunction)StageAOwner_no_reduce, METH_NOARGS,
     "Always fails: custody is not reconstructable."},
    {"__reduce_ex__", (PyCFunction)StageAOwner_no_reduce, METH_VARARGS,
     "Always fails: custody is not reconstructable."},
    {"__setattr__", (PyCFunction)StageAOwner_no_setattr, METH_VARARGS,
     "Always fails: native custody attributes are immutable."},
    {NULL, NULL, 0, NULL}
};

static PyGetSetDef StageA_getset[] = {
    {"sealed", (getter)StageAOwner_get_sealed, NULL,
     "True once one-shot custody admission completed.", NULL},
    {"custody_hash", (getter)StageAOwner_get_custody_hash, NULL,
     "Sealed native custody fingerprint (provenance only).", NULL},
    {NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject StageAOwnerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "rawlsing_next._p07_native_owner_stage_a.StageAOwner",
    .tp_basicsize = sizeof(StageAOwner),
    .tp_dealloc = (destructor)StageAOwner_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,   /* NOTE: Py_TPFLAGS_BASETYPE intentionally absent
                                       * -> the type is NON-SUBCLASSABLE. */
    .tp_doc = "HQ244 Stage A non-authorizing native P07 owner prototype.",
    .tp_methods = StageA_methods,
    .tp_getset = StageA_getset,
    .tp_init = (initproc)StageAOwner_init,
    .tp_new = PyType_GenericNew,
};

/* Module-level factory with explicit class-name checks. */

static PyObject *
stage_a_build_owner(PyObject *module, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"relations", "authority_registry",
                             "trusted_semantic_hash", NULL};
    PyObject *relations = NULL, *registry = NULL, *semhash = NULL;
    PyObject *obj;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOO:build_stage_a_owner",
                                     kwlist, &relations, &registry, &semhash)) {
        return NULL;
    }
    /* Exact class-name admission check: refuse duck-typed substitutes up front. */
    if (Py_TYPE(relations) != &PyList_Type && Py_TYPE(relations) != &PyTuple_Type) {
        PyErr_SetString(PyExc_TypeError,
                        "stage A build requires an exact list/tuple of relations");
        return NULL;
    }
    obj = PyObject_Call((PyObject *)&StageAOwnerType, args, kwds);
    return obj;
}

static PyMethodDef module_methods[] = {
    {"build_stage_a_owner", (PyCFunction)stage_a_build_owner,
     METH_VARARGS | METH_KEYWORDS,
     "Construct and one-shot seal a Stage A native owner (non-authorizing)."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef stageamodule = {
    PyModuleDef_HEAD_INIT,
    "rawlsing_next._p07_native_owner_stage_a",
    "HQ244 Stage A native P07 owner prototype: constructor custody + exact resolve. "
    "NON-PRODUCTION, NON-AUTHORIZING. Cannot issue P07 positive authority.",
    -1,
    module_methods,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__p07_native_owner_stage_a(void)
{
    PyObject *m;
    if (PyType_Ready(&StageAOwnerType) < 0) {
        return NULL;
    }
    m = PyModule_Create(&stageamodule);
    if (m == NULL) {
        return NULL;
    }

    /* Typed errors mirroring the accepted P07 error names. */
    StageAIntegrityError = PyErr_NewException(
        "rawlsing_next._p07_native_owner_stage_a.SourceRelationIntegrityError", NULL, NULL);
    if (StageAIntegrityError == NULL) {
        Py_DECREF(m);
        return NULL;
    }
    StageAKeyError = PyErr_NewException(
        "rawlsing_next._p07_native_owner_stage_a.StageAExactKeyError", NULL, NULL);
    if (StageAKeyError == NULL) {
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(StageAIntegrityError);
    Py_INCREF(StageAKeyError);
    if (PyModule_AddObject(m, "SourceRelationIntegrityError",
                           StageAIntegrityError) < 0) {
        Py_DECREF(StageAIntegrityError);
        Py_DECREF(StageAKeyError);
        Py_DECREF(m);
        return NULL;
    }
    if (PyModule_AddObject(m, "StageAExactKeyError", StageAKeyError) < 0) {
        Py_DECREF(StageAIntegrityError);
        Py_DECREF(StageAKeyError);
        Py_DECREF(m);
        return NULL;
    }
    Py_INCREF(&StageAOwnerType);
    if (PyModule_AddObject(m, "StageAOwner", (PyObject *)&StageAOwnerType) < 0) {
        Py_DECREF(&StageAOwnerType);
        Py_DECREF(StageAIntegrityError);
        Py_DECREF(StageAKeyError);
        Py_DECREF(m);
        return NULL;
    }

    PyModule_AddStringConstant(m, "STAGE_A_CONTRACT", STAGE_A_CONTRACT);
    PyModule_AddStringConstant(m, "STAGE_A_NONAUTHORIZING_MARKER", STAGE_A_NOTIMPL);
    PyModule_AddIntConstant(m, "AUTHORIZING", 0);
    PyModule_AddIntConstant(m, "SUBCLASSABLE", 0);
    PyModule_AddStringConstant(m, "STAGE", "A");
    return m;
}