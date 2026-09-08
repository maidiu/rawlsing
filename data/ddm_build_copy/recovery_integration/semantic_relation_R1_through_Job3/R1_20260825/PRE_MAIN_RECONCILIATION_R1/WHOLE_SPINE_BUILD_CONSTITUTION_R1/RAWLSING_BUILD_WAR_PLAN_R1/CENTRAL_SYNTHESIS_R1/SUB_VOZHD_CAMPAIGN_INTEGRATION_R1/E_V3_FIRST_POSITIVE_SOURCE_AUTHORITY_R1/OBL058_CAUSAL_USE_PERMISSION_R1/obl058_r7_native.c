#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct {
    PyObject_HEAD
    unsigned long long authority_key;
    PyObject *body_json;
    int issued;
    int closed;
} NativeReceipt;

static PyObject *broker_callable = NULL;
typedef struct PinNode {
    PyObject *receipt;
    struct PinNode *next;
} PinNode;
static PinNode *pin_head = NULL;
static Py_ssize_t pin_count_value = 0;
static unsigned long long next_authority_key = 1;
static unsigned long long request_counter = 1;
static unsigned long long successful_native_closes = 0;

static PyObject *new_request_id(NativeReceipt *self) {
    unsigned long long serial = request_counter++;
    if (serial == 0) serial = request_counter++;
    return PyUnicode_FromFormat("r7-%llu-%llu", self->authority_key, serial);
}

static int call_close(NativeReceipt *self) {
    if (!self->issued || self->closed) {
        self->closed = 1;
        return 0;
    }
    if (broker_callable == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_not_bound");
        return -1;
    }
    PyObject *request_id = new_request_id(self);
    if (request_id == NULL) return -1;
    PyObject *request = Py_BuildValue("{s:s,s:K,s:O}",
        "op", "close", "object_id", self->authority_key, "request_id", request_id);
    Py_DECREF(request_id);
    if (request == NULL) return -1;
    PyObject *response = PyObject_CallOneArg(broker_callable, request);
    Py_DECREF(request);
    if (response == NULL) return -1;
    Py_DECREF(response);
    self->closed = 1;
    successful_native_closes++;
    return 0;
}

static PyObject *NativeReceipt_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {
    NativeReceipt *self = (NativeReceipt *)type->tp_alloc(type, 0);
    if (self == NULL) return NULL;
    unsigned long long key = next_authority_key++;
    if (key == 0) key = next_authority_key++;
    self->authority_key = key;
    self->body_json = PyUnicode_FromString("");
    if (self->body_json == NULL) { Py_DECREF(self); return NULL; }
    self->issued = 0;
    self->closed = 0;
    return (PyObject *)self;
}

static void NativeReceipt_dealloc(NativeReceipt *self) {
    if (self->issued && !self->closed && broker_callable != NULL) {
        if (call_close(self) < 0) PyErr_Clear();
    }
    Py_XDECREF(self->body_json);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *NativeReceipt_source_issue(NativeReceipt *self, PyObject *args) {
    PyObject *scope = NULL, *basis_id = NULL, *fixture_class = NULL;
    if (!PyArg_ParseTuple(args, "OOO:_source_issue", &scope, &basis_id, &fixture_class)) return NULL;
    if (self->issued) { PyErr_SetString(PyExc_ValueError, "object_identity_already_issued"); return NULL; }
    if (broker_callable == NULL) { PyErr_SetString(PyExc_RuntimeError, "authority_broker_not_bound"); return NULL; }

    PyObject *request_id = new_request_id(self);
    if (request_id == NULL) return NULL;
    PyObject *request = Py_BuildValue("{s:s,s:K,s:O,s:O,s:O,s:O}",
        "op", "issue", "object_id", self->authority_key, "scope", scope,
        "basis_id", basis_id, "fixture_class", fixture_class, "request_id", request_id);
    Py_DECREF(request_id);
    if (request == NULL) return NULL;
    PyObject *response = PyObject_CallOneArg(broker_callable, request);
    Py_DECREF(request);
    if (response == NULL) return NULL;
    if (!PyDict_Check(response)) { Py_DECREF(response); PyErr_SetString(PyExc_RuntimeError, "authority_broker_protocol_error"); return NULL; }
    PyObject *body = PyDict_GetItemString(response, "body_json");
    if (body == NULL || !PyUnicode_Check(body) || PyUnicode_GetLength(body) <= 0) {
        Py_DECREF(response); PyErr_SetString(PyExc_RuntimeError, "authority_broker_protocol_error"); return NULL;
    }

    Py_INCREF(body);
    Py_SETREF(self->body_json, body);
    self->issued = 1;
    self->closed = 0;
    PinNode *node = (PinNode *)PyMem_Malloc(sizeof(PinNode));
    if (node == NULL) {
        if (call_close(self) < 0) PyErr_Clear();
        Py_DECREF(response);
        PyErr_NoMemory();
        return NULL;
    }
    node->receipt = Py_NewRef((PyObject *)self);
    node->next = pin_head;
    pin_head = node;
    pin_count_value++;
    Py_DECREF(response);
    return Py_NewRef(self->body_json);
}

static PyObject *NativeReceipt_validate(NativeReceipt *self, PyObject *expected_scope) {
    if (!self->issued || self->closed || self->body_json == NULL || PyUnicode_GetLength(self->body_json) <= 0) {
        PyErr_SetString(PyExc_ValueError, "receipt_not_issued_by_source_authority"); return NULL;
    }
    if (broker_callable == NULL) { PyErr_SetString(PyExc_RuntimeError, "authority_broker_not_bound"); return NULL; }
    PyObject *request_id = new_request_id(self);
    if (request_id == NULL) return NULL;
    PyObject *request = Py_BuildValue("{s:s,s:K,s:O,s:O,s:O}",
        "op", "validate", "object_id", self->authority_key, "body_json", self->body_json,
        "expected_scope", expected_scope, "request_id", request_id);
    Py_DECREF(request_id);
    if (request == NULL) return NULL;
    PyObject *response = PyObject_CallOneArg(broker_callable, request);
    Py_DECREF(request);
    if (response == NULL) return NULL;
    if (!PyDict_Check(response)) { Py_DECREF(response); PyErr_SetString(PyExc_RuntimeError, "authority_broker_protocol_error"); return NULL; }
    PyObject *decision = PyDict_GetItemString(response, "decision");
    if (decision == NULL || !PyUnicode_Check(decision)) { Py_DECREF(response); PyErr_SetString(PyExc_RuntimeError, "authority_broker_protocol_error"); return NULL; }
    PyObject *out = Py_NewRef(decision);
    Py_DECREF(response);
    return out;
}

static void unpin_receipt(NativeReceipt *self) {
    PinNode **cursor = &pin_head;
    while (*cursor != NULL) {
        PinNode *node = *cursor;
        if (node->receipt == (PyObject *)self) {
            *cursor = node->next;
            pin_count_value--;
            PyObject *held = node->receipt;
            PyMem_Free(node);
            Py_DECREF(held);
            return;
        }
        cursor = &node->next;
    }
}

static PyObject *NativeReceipt_close(NativeReceipt *self, PyObject *Py_UNUSED(ignored)) {
    if (!self->issued || self->closed) { self->closed = 1; Py_RETURN_FALSE; }
    if (call_close(self) < 0) return NULL;
    unpin_receipt(self);
    Py_RETURN_TRUE;
}
static PyObject *NativeReceipt_body_json_copy(NativeReceipt *self, PyObject *Py_UNUSED(ignored)) {
    if (self->body_json == NULL) return PyUnicode_FromString("");
    return Py_NewRef(self->body_json);
}
static PyObject *NativeReceipt_is_issued(NativeReceipt *self, PyObject *Py_UNUSED(ignored)) {
    if (self->issued && !self->closed) Py_RETURN_TRUE;
    Py_RETURN_FALSE;
}

static PyMethodDef NativeReceipt_methods[] = {
    {"_source_issue", (PyCFunction)NativeReceipt_source_issue, METH_VARARGS, NULL},
    {"_source_validate", (PyCFunction)NativeReceipt_validate, METH_O, NULL},
    {"_source_close", (PyCFunction)NativeReceipt_close, METH_NOARGS, NULL},
    {"_body_json_copy", (PyCFunction)NativeReceipt_body_json_copy, METH_NOARGS, NULL},
    {"_is_source_issued", (PyCFunction)NativeReceipt_is_issued, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};
static PyTypeObject NativeReceiptType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_obl058_r7_native.NativeReceiptBase",
    .tp_basicsize = sizeof(NativeReceipt),
    .tp_dealloc = (destructor)NativeReceipt_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_methods = NativeReceipt_methods,
    .tp_new = NativeReceipt_new,
};

static PyObject *module_bind_broker(PyObject *module, PyObject *callable) {
    if (!PyCallable_Check(callable)) { PyErr_SetString(PyExc_TypeError, "broker callable required"); return NULL; }
    if (broker_callable == NULL) { broker_callable = Py_NewRef(callable); Py_RETURN_NONE; }
    if (broker_callable == callable) Py_RETURN_NONE;
    PyErr_SetString(PyExc_RuntimeError, "broker_already_bound"); return NULL;
}
static PyObject *module_close_success_count(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromUnsignedLongLong(successful_native_closes);
}
static PyObject *module_pin_count(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromSsize_t(pin_count_value);
}
static PyMethodDef module_methods[] = {
    {"bind_broker", (PyCFunction)module_bind_broker, METH_O, NULL},
    {"close_success_count", (PyCFunction)module_close_success_count, METH_NOARGS, NULL},
    {"pin_count", (PyCFunction)module_pin_count, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};
static void module_free(void *module) {
    while (pin_head != NULL) {
        PinNode *node = pin_head;
        pin_head = node->next;
        pin_count_value--;
        PyObject *held = node->receipt;
        PyMem_Free(node);
        Py_DECREF(held);
    }
    Py_CLEAR(broker_callable);
}
static struct PyModuleDef moduledef = { PyModuleDef_HEAD_INIT, "_obl058_r7_native", NULL, -1, module_methods, NULL, NULL, NULL, module_free };
PyMODINIT_FUNC PyInit__obl058_r7_native(void) {
    if (PyType_Ready(&NativeReceiptType) < 0) return NULL;
    PyObject *module = PyModule_Create(&moduledef);
    if (module == NULL) return NULL;
    Py_INCREF(&NativeReceiptType);
    if (PyModule_AddObject(module, "NativeReceiptBase", (PyObject *)&NativeReceiptType) < 0) {
        Py_DECREF(&NativeReceiptType); Py_DECREF(module); return NULL;
    }
    return module;
}
