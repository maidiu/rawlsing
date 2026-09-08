static void stop_broker_process(void) {
    if (broker_pid > 0) {
        (void)kill(broker_pid, SIGTERM);
        for (int i = 0; i < 100; i++) {
            int status = 0;
            pid_t got = waitpid(broker_pid, &status, WNOHANG);
            if (got == broker_pid || (got < 0 && errno == ECHILD)) break;
            struct timespec delay = {0, 10000000};
            nanosleep(&delay, NULL);
        }
        int status = 0;
        if (waitpid(broker_pid, &status, WNOHANG) == 0) {
            (void)kill(broker_pid, SIGKILL);
            (void)waitpid(broker_pid, &status, 0);
        }
    }
    if (broker_path) (void)unlink(broker_path);
    if (broker_dir) (void)rmdir(broker_dir);
    broker_pid = 0;
    broker_uid = 0;
    broker_configured = 0;
}

static int assign_broker_identity(const char *path, pid_t pid, const char *start, uid_t uid, const char *dir, const char *script) {
    broker_path = (char *)PyMem_Malloc(strlen(path) + 1);
    broker_starttime = (char *)PyMem_Malloc(strlen(start) + 1);
    broker_dir = (char *)PyMem_Malloc(strlen(dir) + 1);
    broker_script = (char *)PyMem_Malloc(strlen(script) + 1);
    if (!broker_path || !broker_starttime || !broker_dir || !broker_script) {
        PyMem_Free(broker_path); broker_path = NULL;
        PyMem_Free(broker_starttime); broker_starttime = NULL;
        PyMem_Free(broker_dir); broker_dir = NULL;
        PyMem_Free(broker_script); broker_script = NULL;
        PyErr_NoMemory();
        return -1;
    }
    strcpy(broker_path, path);
    strcpy(broker_starttime, start);
    strcpy(broker_dir, dir);
    strcpy(broker_script, script);
    broker_pid = pid;
    broker_uid = uid;
    broker_configured = 1;
    return 0;
}

static PyObject *module_start_broker(PyObject *module, PyObject *script_obj) {
    if (!PyUnicode_Check(script_obj)) {
        PyErr_SetString(PyExc_TypeError, "broker_script_path_required");
        return NULL;
    }
    const char *script = PyUnicode_AsUTF8(script_obj);
    if (script == NULL) return NULL;
    if (broker_start_locked) {
        if (broker_configured && broker_script && strcmp(broker_script, script) == 0) Py_RETURN_NONE;
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_transport_already_started_or_retired");
        return NULL;
    }
    broker_start_locked = 1;

    char template_path[] = "/tmp/obl058-r8-broker-XXXXXX";
    char *dir = mkdtemp(template_path);
    if (dir == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_directory_unavailable");
        return NULL;
    }
    char socket_path[sizeof(((struct sockaddr_un *)0)->sun_path)];
    int written = snprintf(socket_path, sizeof(socket_path), "%s/authority.sock", dir);
    if (written <= 0 || (size_t)written >= sizeof(socket_path)) {
        (void)rmdir(dir);
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_path_too_long");
        return NULL;
    }

    char python_exe[4096];
    ssize_t exe_len = readlink("/proc/self/exe", python_exe, sizeof(python_exe) - 1);
    if (exe_len <= 0) {
        (void)rmdir(dir);
        PyErr_SetString(PyExc_RuntimeError, "python_executable_unavailable");
        return NULL;
    }
    python_exe[exe_len] = '\0';

    pid_t child = fork();
    if (child < 0) {
        (void)rmdir(dir);
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_launch_failed");
        return NULL;
    }
    if (child == 0) {
        (void)prctl(PR_SET_PDEATHSIG, SIGTERM);
        if (getppid() == 1) _exit(127);
        int devnull = open("/dev/null", O_RDWR);
        if (devnull >= 0) {
            (void)dup2(devnull, STDIN_FILENO);
            (void)dup2(devnull, STDOUT_FILENO);
            (void)dup2(devnull, STDERR_FILENO);
            if (devnull > STDERR_FILENO) close(devnull);
        }
        execl(python_exe, python_exe, "-S", script, "--broker-service-r6", socket_path, (char *)NULL);
        _exit(127);
    }

    char starttime[128];
    int start_ok = 0;
    for (int i = 0; i < 200; i++) {
        if (read_process_starttime(child, starttime, sizeof(starttime)) == 0) { start_ok = 1; break; }
        struct timespec delay = {0, 10000000}; nanosleep(&delay, NULL);
    }
    if (!start_ok) {
        (void)kill(child, SIGKILL); (void)waitpid(child, NULL, 0); (void)rmdir(dir);
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_identity_unavailable");
        return NULL;
    }
    if (assign_broker_identity(socket_path, child, starttime, getuid(), dir, script) < 0) {
        (void)kill(child, SIGKILL); (void)waitpid(child, NULL, 0); (void)rmdir(dir);
        return NULL;
    }

    int ready = 0;
    for (int i = 0; i < 2000; i++) {
        int status = 0;
        pid_t got = waitpid(child, &status, WNOHANG);
        if (got == child) break;
        struct stat st;
        if (stat(socket_path, &st) == 0) {
            PyObject *request_id = PyUnicode_FromFormat("r8-ping-%ld-%d", (long)getpid(), i);
            if (request_id == NULL) { stop_broker_process(); return NULL; }
            PyObject *request = Py_BuildValue("{s:s,s:O}", "op", "ping", "request_id", request_id);
            Py_DECREF(request_id);
            if (request == NULL) { stop_broker_process(); return NULL; }
            PyObject *response = transport_roundtrip(request);
            Py_DECREF(request);
            if (response != NULL) {
                PyObject *pong = PyDict_GetItemString(response, "pong");
                ready = (pong == Py_True);
                Py_DECREF(response);
                if (ready) break;
            } else {
                PyErr_Clear();
            }
        }
        struct timespec delay = {0, 10000000}; nanosleep(&delay, NULL);
    }
    if (!ready) {
        stop_broker_process();
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_unavailable");
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *module_shutdown_broker(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    stop_broker_process();
    Py_RETURN_NONE;
}

static PyObject *module_transport_configured(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    if (broker_configured) Py_RETURN_TRUE;
    Py_RETURN_FALSE;
}

static PyObject *module_close_success_count(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromUnsignedLongLong(successful_native_closes);
}
static PyObject *module_pin_count(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromSsize_t(pin_count_value);
}
static PyObject *module_transport_success_count(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    return PyLong_FromUnsignedLongLong(successful_transport_roundtrips);
}
static PyObject *module_broker_pid(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    if (!broker_configured) Py_RETURN_NONE;
    return PyLong_FromLong((long)broker_pid);
}
static PyObject *module_broker_path(PyObject *module, PyObject *Py_UNUSED(ignored)) {
    if (!broker_configured || broker_path == NULL) Py_RETURN_NONE;
    return PyUnicode_FromString(broker_path);
}

static PyMethodDef module_methods[] = {
    {"start_broker", (PyCFunction)module_start_broker, METH_O, NULL},
    {"shutdown_broker", (PyCFunction)module_shutdown_broker, METH_NOARGS, NULL},
    {"transport_configured", (PyCFunction)module_transport_configured, METH_NOARGS, NULL},
    {"close_success_count", (PyCFunction)module_close_success_count, METH_NOARGS, NULL},
    {"pin_count", (PyCFunction)module_pin_count, METH_NOARGS, NULL},
    {"transport_success_count", (PyCFunction)module_transport_success_count, METH_NOARGS, NULL},
    {"broker_pid", (PyCFunction)module_broker_pid, METH_NOARGS, NULL},
    {"broker_path", (PyCFunction)module_broker_path, METH_NOARGS, NULL},
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
    stop_broker_process();
    PyMem_Free(broker_path); broker_path = NULL;
    PyMem_Free(broker_starttime); broker_starttime = NULL;
    PyMem_Free(broker_dir); broker_dir = NULL;
    PyMem_Free(broker_script); broker_script = NULL;
}

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_obl058_r8_native",
    "OBL058 R8 native object-generation and broker-transport core.",
    -1,
    module_methods,
    NULL, NULL, NULL,
    module_free
};

PyMODINIT_FUNC PyInit__obl058_r8_native(void) {
    if (PyType_Ready(&NativeReceiptType) < 0) return NULL;
    PyObject *module = PyModule_Create(&moduledef);
    if (module == NULL) return NULL;
    Py_INCREF(&NativeReceiptType);
    if (PyModule_AddObject(module, "NativeReceiptBase", (PyObject *)&NativeReceiptType) < 0) {
        Py_DECREF(&NativeReceiptType); Py_DECREF(module); return NULL;
    }
    return module;
}
