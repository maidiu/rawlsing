#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>

/*
 * OBL058 R12 retained authority-client boundary.
 *
 * Source-origin verification authenticates the exact public_validate built-in.
 * establish_authority_client verifies that exact object by identity, binds the
 * native receipt descriptors once, and places a strong reference to that exact
 * capability inside an immutable native AuthorityClient instance.
 *
 * AuthorityClient is callable. Its tp_call slot invokes the retained capability
 * object directly; no later Python module/class/instance/descriptor/alias/import
 * or cache lookup selects the validation decision path for an issued client.
 */

static PyObject *configured_receipt_type = NULL;
static PyObject *configured_scope_type = NULL;
static PyObject *configured_error_type = NULL;
static PyObject *configured_native_base = NULL;
static PyObject *configured_public_validate = NULL;
static PyObject *validate_descriptor = NULL;
static PyObject *body_descriptor = NULL;

static const char *scope_names[] = {
    "actor_id", "world_id", "subject_id", "time_id", "transition_id"
};
static const char *scope_prefixes[] = {
    "NONCURRENT_SYNTHETIC::actor::",
    "NONCURRENT_SYNTHETIC::world::",
    "NONCURRENT_SYNTHETIC::subject::",
    "NONCURRENT_SYNTHETIC::time::",
    "NONCURRENT_SYNTHETIC::transition::"
};

typedef struct {
    PyObject_HEAD
    PyObject *capability;
} AuthorityClientObject;

static void contract_error(const char *message) {
    if (configured_error_type != NULL) {
        PyErr_SetString(configured_error_type, message);
    } else {
        PyErr_SetString(PyExc_ValueError, message);
    }
}

static void convert_current_to_contract(const char *fallback) {
    PyObject *type = NULL, *value = NULL, *tb = NULL;
    PyErr_Fetch(&type, &value, &tb);
    if (type != NULL && !PyErr_GivenExceptionMatches(type, PyExc_Exception)) {
        PyErr_Restore(type, value, tb);
        return;
    }
    PyObject *text = value != NULL ? PyObject_Str(value) : NULL;
    Py_XDECREF(type);
    Py_XDECREF(value);
    Py_XDECREF(tb);
    if (text != NULL && configured_error_type != NULL) {
        PyErr_SetObject(configured_error_type, text);
        Py_DECREF(text);
        return;
    }
    Py_XDECREF(text);
    contract_error(fallback);
}

static PyObject *canonical_scope_copy(PyObject *scope) {
    if (configured_scope_type == NULL || (PyObject *)Py_TYPE(scope) != configured_scope_type) {
        contract_error("exact_scope_type_required");
        return NULL;
    }
    PyObject *raw_dict = PyObject_GenericGetDict(scope, NULL);
    if (raw_dict == NULL) {
        convert_current_to_contract("scope_state_unavailable");
        return NULL;
    }
    if (!PyDict_CheckExact(raw_dict) || PyDict_Size(raw_dict) != 5) {
        Py_DECREF(raw_dict);
        contract_error("malformed_scope");
        return NULL;
    }

    PyObject *out = PyDict_New();
    if (out == NULL) {
        Py_DECREF(raw_dict);
        return NULL;
    }
    for (int i = 0; i < 5; i++) {
        PyObject *value = PyDict_GetItemString(raw_dict, scope_names[i]);
        if (value == NULL || !PyUnicode_CheckExact(value)) {
            Py_DECREF(raw_dict);
            Py_DECREF(out);
            contract_error("malformed_scope");
            return NULL;
        }
        Py_ssize_t size = 0;
        const char *text = PyUnicode_AsUTF8AndSize(value, &size);
        if (text == NULL) {
            Py_DECREF(raw_dict);
            Py_DECREF(out);
            convert_current_to_contract("malformed_scope");
            return NULL;
        }
        size_t prefix_len = strlen(scope_prefixes[i]);
        if ((size_t)size <= prefix_len || memcmp(text, scope_prefixes[i], prefix_len) != 0) {
            Py_DECREF(raw_dict);
            Py_DECREF(out);
            char message[128];
            snprintf(message, sizeof(message), "noncurrent_synthetic_scope_required:%s", scope_names[i]);
            contract_error(message);
            return NULL;
        }
        int only_space = 1;
        for (Py_ssize_t j = (Py_ssize_t)prefix_len; j < size; j++) {
            unsigned char ch = (unsigned char)text[j];
            if (!(ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n' || ch == '\f' || ch == '\v')) {
                only_space = 0;
                break;
            }
        }
        if (only_space) {
            Py_DECREF(raw_dict);
            Py_DECREF(out);
            char message[128];
            snprintf(message, sizeof(message), "missing_or_invalid_scope:%s", scope_names[i]);
            contract_error(message);
            return NULL;
        }
        if (PyDict_SetItemString(out, scope_names[i], value) < 0) {
            Py_DECREF(raw_dict);
            Py_DECREF(out);
            return NULL;
        }
    }
    Py_DECREF(raw_dict);
    return out;
}

static PyObject *body_authority_instance(PyObject *receipt) {
    PyObject *body = PyObject_CallFunctionObjArgs(body_descriptor, receipt, NULL);
    if (body == NULL) {
        convert_current_to_contract("receipt_not_issued_by_source_authority");
        return NULL;
    }
    if (!PyUnicode_CheckExact(body)) {
        Py_DECREF(body);
        contract_error("malformed_receipt_body");
        return NULL;
    }
    Py_ssize_t size = 0;
    const char *text = PyUnicode_AsUTF8AndSize(body, &size);
    if (text == NULL) {
        Py_DECREF(body);
        convert_current_to_contract("malformed_receipt_body");
        return NULL;
    }
    const char *needle = "\"authority_instance_id\":\"";
    const char *start = strstr(text, needle);
    if (start == NULL) {
        Py_DECREF(body);
        contract_error("wrong_authority_instance");
        return NULL;
    }
    start += strlen(needle);
    const char *end = strchr(start, '\"');
    if (end == NULL || end == start || end > text + size) {
        Py_DECREF(body);
        contract_error("wrong_authority_instance");
        return NULL;
    }
    PyObject *instance = PyUnicode_FromStringAndSize(start, (Py_ssize_t)(end - start));
    Py_DECREF(body);
    return instance;
}

static PyObject *module_public_validate(PyObject *module, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"receipt", "expected_scope", NULL};
    PyObject *receipt = NULL, *expected_scope = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO:public_validate", keywords, &receipt, &expected_scope)) {
        return NULL;
    }
    if (configured_receipt_type == NULL || validate_descriptor == NULL || body_descriptor == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "authority_client_not_established");
        return NULL;
    }
    if ((PyObject *)Py_TYPE(receipt) != configured_receipt_type ||
        !PyType_IsSubtype(Py_TYPE(receipt), (PyTypeObject *)configured_native_base)) {
        contract_error("receipt_not_issued_by_source_authority");
        return NULL;
    }

    PyObject *scope_dict = canonical_scope_copy(expected_scope);
    if (scope_dict == NULL) return NULL;
    PyObject *result = PyObject_CallFunctionObjArgs(validate_descriptor, receipt, scope_dict, NULL);
    Py_DECREF(scope_dict);
    if (result == NULL) {
        convert_current_to_contract("receipt_validation_failed");
        return NULL;
    }
    if (!PyTuple_CheckExact(result) || PyTuple_GET_SIZE(result) != 2) {
        Py_DECREF(result);
        contract_error("authority_broker_protocol_error");
        return NULL;
    }
    PyObject *decision = PyTuple_GET_ITEM(result, 0);
    PyObject *response_instance = PyTuple_GET_ITEM(result, 1);
    if (!PyUnicode_CheckExact(decision) || !PyUnicode_CheckExact(response_instance)) {
        Py_DECREF(result);
        contract_error("authority_broker_protocol_error");
        return NULL;
    }
    int is_permit = PyUnicode_CompareWithASCIIString(decision, "PERMIT") == 0;
    int is_deny = PyUnicode_CompareWithASCIIString(decision, "DENY") == 0;
    if (!is_permit && !is_deny) {
        Py_DECREF(result);
        contract_error("authority_broker_protocol_error");
        return NULL;
    }

    PyObject *body_instance = body_authority_instance(receipt);
    if (body_instance == NULL) {
        Py_DECREF(result);
        return NULL;
    }
    int equal = PyObject_RichCompareBool(response_instance, body_instance, Py_EQ);
    Py_DECREF(body_instance);
    if (equal < 0) {
        Py_DECREF(result);
        convert_current_to_contract("wrong_authority_instance");
        return NULL;
    }
    if (!equal) {
        Py_DECREF(result);
        contract_error("wrong_authority_instance");
        return NULL;
    }

    PyObject *out = Py_NewRef(decision);
    Py_DECREF(result);
    return out;
}

static void authority_client_dealloc(AuthorityClientObject *self) {
    Py_CLEAR(self->capability);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *authority_client_call(PyObject *self_obj, PyObject *args, PyObject *kwargs) {
    AuthorityClientObject *self = (AuthorityClientObject *)self_obj;
    if (self->capability == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "authority_client_capability_unavailable");
        return NULL;
    }
    return PyObject_Call(self->capability, args, kwargs);
}

static PyObject *authority_client_capability_identity(AuthorityClientObject *self, void *closure) {
    (void)closure;
    if (self->capability == NULL) Py_RETURN_NONE;
    return PyLong_FromVoidPtr((void *)self->capability);
}

static PyObject *authority_client_noncopyable(PyObject *self, PyObject *arg) {
    (void)self;
    (void)arg;
    PyErr_SetString(PyExc_TypeError, "authority_client_not_copyable_or_serializable");
    return NULL;
}

static PyObject *authority_client_noncopyable_noargs(PyObject *self, PyObject *Py_UNUSED(ignored)) {
    (void)self;
    PyErr_SetString(PyExc_TypeError, "authority_client_not_copyable_or_serializable");
    return NULL;
}

static PyMethodDef authority_client_methods[] = {
    {"__copy__", (PyCFunction)authority_client_noncopyable_noargs, METH_NOARGS, NULL},
    {"__deepcopy__", (PyCFunction)authority_client_noncopyable, METH_O, NULL},
    {"__reduce__", (PyCFunction)authority_client_noncopyable_noargs, METH_NOARGS, NULL},
    {"__reduce_ex__", (PyCFunction)authority_client_noncopyable, METH_O, NULL},
    {NULL, NULL, 0, NULL}
};

static PyGetSetDef authority_client_getset[] = {
    {"retained_capability_identity", (getter)authority_client_capability_identity, NULL, NULL, NULL},
    {NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject AuthorityClientType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_obl058_r12_authority_client.AuthorityClient",
    .tp_basicsize = sizeof(AuthorityClientObject),
    .tp_dealloc = (destructor)authority_client_dealloc,
    .tp_call = authority_client_call,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_IMMUTABLETYPE,
    .tp_methods = authority_client_methods,
    .tp_getset = authority_client_getset,
    .tp_doc = "Retained OBL058 authority client; call directly to validate a receipt.",
};

static PyObject *new_authority_client(PyObject *capability) {
    AuthorityClientObject *client = PyObject_New(AuthorityClientObject, &AuthorityClientType);
    if (client == NULL) return NULL;
    client->capability = Py_NewRef(capability);
    return (PyObject *)client;
}

static PyObject *module_establish_authority_client(PyObject *module, PyObject *args) {
    PyObject *receipt_type = NULL, *scope_type = NULL, *error_type = NULL, *native_base = NULL;
    PyObject *expected_capability = NULL;
    if (!PyArg_ParseTuple(
            args,
            "OOOOO:establish_authority_client",
            &receipt_type,
            &scope_type,
            &error_type,
            &native_base,
            &expected_capability)) {
        return NULL;
    }
    if (!PyType_Check(receipt_type) || !PyType_Check(scope_type) ||
        !PyType_Check(error_type) || !PyType_Check(native_base)) {
        PyErr_SetString(PyExc_TypeError, "type_arguments_required");
        return NULL;
    }
    if (!PyCFunction_Check(expected_capability) || PyCFunction_GET_SELF(expected_capability) != module) {
        PyErr_SetString(PyExc_TypeError, "authenticated_validation_capability_required");
        return NULL;
    }

    PyObject *module_dict = PyModule_GetDict(module);
    if (module_dict == NULL || !PyDict_CheckExact(module_dict)) {
        PyErr_SetString(PyExc_RuntimeError, "capability_module_dictionary_unavailable");
        return NULL;
    }
    PyObject *owned_public_validate = PyDict_GetItemString(module_dict, "public_validate");
    if (owned_public_validate == NULL || owned_public_validate != expected_capability ||
        !PyCFunction_Check(owned_public_validate) || PyCFunction_GET_SELF(owned_public_validate) != module) {
        PyErr_SetString(PyExc_RuntimeError, "authenticated_validation_capability_identity_mismatch");
        return NULL;
    }

    if (configured_receipt_type != NULL) {
        if (configured_receipt_type != receipt_type || configured_scope_type != scope_type ||
            configured_error_type != error_type || configured_native_base != native_base ||
            configured_public_validate != expected_capability) {
            PyErr_SetString(PyExc_RuntimeError, "authority_client_already_established_with_different_contract");
            return NULL;
        }
        return new_authority_client(configured_public_validate);
    }

    if (!PyType_IsSubtype((PyTypeObject *)receipt_type, (PyTypeObject *)native_base)) {
        PyErr_SetString(PyExc_TypeError, "receipt_type_must_extend_native_base");
        return NULL;
    }

    PyObject *base_dict = ((PyTypeObject *)native_base)->tp_dict;
    if (base_dict == NULL || !PyDict_Check(base_dict)) {
        PyErr_SetString(PyExc_TypeError, "native_base_dictionary_unavailable");
        return NULL;
    }
    PyObject *vd = PyDict_GetItemString(base_dict, "_source_validate");
    PyObject *bd = PyDict_GetItemString(base_dict, "_body_json_copy");
    if (vd == NULL || bd == NULL || !PyCallable_Check(vd) || !PyCallable_Check(bd)) {
        PyErr_SetString(PyExc_TypeError, "verified_native_descriptors_required");
        return NULL;
    }

    configured_receipt_type = Py_NewRef(receipt_type);
    configured_scope_type = Py_NewRef(scope_type);
    configured_error_type = Py_NewRef(error_type);
    configured_native_base = Py_NewRef(native_base);
    configured_public_validate = Py_NewRef(expected_capability);
    validate_descriptor = Py_NewRef(vd);
    body_descriptor = Py_NewRef(bd);

    return new_authority_client(configured_public_validate);
}

static PyMethodDef module_methods[] = {
    {"establish_authority_client", (PyCFunction)module_establish_authority_client, METH_VARARGS, NULL},
    {"public_validate", (PyCFunction)(void(*)(void))module_public_validate, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL}
};

static void module_free(void *module) {
    (void)module;
    Py_CLEAR(configured_receipt_type);
    Py_CLEAR(configured_scope_type);
    Py_CLEAR(configured_error_type);
    Py_CLEAR(configured_native_base);
    Py_CLEAR(configured_public_validate);
    Py_CLEAR(validate_descriptor);
    Py_CLEAR(body_descriptor);
}

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_obl058_r12_authority_client",
    "OBL058 R12 retained authority-client capability.",
    -1,
    module_methods,
    NULL, NULL, NULL,
    module_free
};

PyMODINIT_FUNC PyInit__obl058_r12_authority_client(void) {
    if (PyType_Ready(&AuthorityClientType) < 0) return NULL;
    return PyModule_Create(&moduledef);
}
