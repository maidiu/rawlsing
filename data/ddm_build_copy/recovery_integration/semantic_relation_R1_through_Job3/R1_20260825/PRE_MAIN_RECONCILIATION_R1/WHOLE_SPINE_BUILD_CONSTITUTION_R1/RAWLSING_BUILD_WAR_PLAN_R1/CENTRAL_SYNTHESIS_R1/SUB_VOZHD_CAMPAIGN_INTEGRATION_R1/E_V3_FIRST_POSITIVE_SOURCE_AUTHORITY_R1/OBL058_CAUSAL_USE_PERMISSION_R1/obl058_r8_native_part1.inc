#define _GNU_SOURCE
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <signal.h>
#include <time.h>

/*
 * OBL058 R8 native receipt + broker transport core.
 *
 * Correctness-relevant broker transport uses POSIX socket/connect/getsockopt/
 * send/recv directly from this extension.  It does not resolve or call the
 * mutable Python socket constructor/module during issuance, validation, or
 * close.  The R7 native generation key and C-owned lifetime reservation remain.
 */

typedef struct {
    PyObject_HEAD
    unsigned long long authority_key;
    PyObject *body_json;
    int issued;
    int closed;
} NativeReceipt;

typedef struct PinNode {
    PyObject *receipt;
    struct PinNode *next;
} PinNode;

typedef struct {
    char *data;
    Py_ssize_t len;
    Py_ssize_t cap;
} Buffer;

static PinNode *pin_head = NULL;
static Py_ssize_t pin_count_value = 0;
static unsigned long long next_authority_key = 1;
static unsigned long long request_counter = 1;
static unsigned long long successful_native_closes = 0;
static unsigned long long successful_transport_roundtrips = 0;

static char *broker_path = NULL;
static char *broker_starttime = NULL;
static char *broker_dir = NULL;
static char *broker_script = NULL;
static pid_t broker_pid = 0;
static uid_t broker_uid = 0;
static int broker_configured = 0;
static int broker_start_locked = 0;

static int buffer_reserve(Buffer *buf, Py_ssize_t extra) {
    if (extra < 0 || buf->len > PY_SSIZE_T_MAX - extra - 1) {
        PyErr_NoMemory();
        return -1;
    }
    Py_ssize_t need = buf->len + extra + 1;
    if (need <= buf->cap) return 0;
    Py_ssize_t cap = buf->cap ? buf->cap : 256;
    while (cap < need) {
        if (cap > PY_SSIZE_T_MAX / 2) { cap = need; break; }
        cap *= 2;
    }
    char *next = (char *)PyMem_Realloc(buf->data, (size_t)cap);
    if (next == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    buf->data = next;
    buf->cap = cap;
    return 0;
}

static int buffer_append(Buffer *buf, const char *data, Py_ssize_t size) {
    if (buffer_reserve(buf, size) < 0) return -1;
    if (size) memcpy(buf->data + buf->len, data, (size_t)size);
    buf->len += size;
    buf->data[buf->len] = '\0';
    return 0;
}

static int buffer_char(Buffer *buf, char ch) {
    return buffer_append(buf, &ch, 1);
}

static void buffer_free(Buffer *buf) {
    PyMem_Free(buf->data);
    buf->data = NULL;
    buf->len = 0;
    buf->cap = 0;
}

static int json_string(Buffer *buf, PyObject *value) {
    Py_ssize_t size = 0;
    const char *text = PyUnicode_AsUTF8AndSize(value, &size);
    if (text == NULL) return -1;
    if (buffer_char(buf, '"') < 0) return -1;
    for (Py_ssize_t i = 0; i < size; i++) {
        unsigned char ch = (unsigned char)text[i];
        switch (ch) {
            case '"': if (buffer_append(buf, "\\\"", 2) < 0) return -1; break;
            case '\\': if (buffer_append(buf, "\\\\", 2) < 0) return -1; break;
            case '\b': if (buffer_append(buf, "\\b", 2) < 0) return -1; break;
            case '\f': if (buffer_append(buf, "\\f", 2) < 0) return -1; break;
            case '\n': if (buffer_append(buf, "\\n", 2) < 0) return -1; break;
            case '\r': if (buffer_append(buf, "\\r", 2) < 0) return -1; break;
            case '\t': if (buffer_append(buf, "\\t", 2) < 0) return -1; break;
            default:
                if (ch < 0x20) {
                    char esc[7];
                    snprintf(esc, sizeof(esc), "\\u%04x", (unsigned int)ch);
                    if (buffer_append(buf, esc, 6) < 0) return -1;
                } else {
                    if (buffer_char(buf, (char)ch) < 0) return -1;
                }
        }
    }
    return buffer_char(buf, '"');
}

static int json_value(Buffer *buf, PyObject *value, int depth) {
    if (depth > 16) {
        PyErr_SetString(PyExc_ValueError, "native_json_depth_exceeded");
        return -1;
    }
    if (PyUnicode_Check(value)) return json_string(buf, value);
    if (value == Py_True) return buffer_append(buf, "true", 4);
    if (value == Py_False) return buffer_append(buf, "false", 5);
    if (value == Py_None) return buffer_append(buf, "null", 4);
    if (PyLong_Check(value)) {
        PyObject *text_obj = PyObject_Str(value);
        if (text_obj == NULL) return -1;
        Py_ssize_t n = 0;
        const char *text = PyUnicode_AsUTF8AndSize(text_obj, &n);
        int rc = text ? buffer_append(buf, text, n) : -1;
        Py_DECREF(text_obj);
        return rc;
    }
    if (PyDict_CheckExact(value)) {
        if (buffer_char(buf, '{') < 0) return -1;
        Py_ssize_t pos = 0;
        PyObject *key = NULL, *item = NULL;
        int first = 1;
        while (PyDict_Next(value, &pos, &key, &item)) {
            if (!PyUnicode_Check(key)) {
                PyErr_SetString(PyExc_TypeError, "native_json_dict_key_must_be_string");
                return -1;
            }
            if (!first && buffer_char(buf, ',') < 0) return -1;
            first = 0;
            if (json_string(buf, key) < 0 || buffer_char(buf, ':') < 0 || json_value(buf, item, depth + 1) < 0) return -1;
        }
        return buffer_char(buf, '}');
    }
    PyErr_SetString(PyExc_TypeError, "native_json_unsupported_value");
    return -1;
}

static int hex_digit(char ch) {
    if (ch >= '0' && ch <= '9') return ch - '0';
    if (ch >= 'a' && ch <= 'f') return ch - 'a' + 10;
    if (ch >= 'A' && ch <= 'F') return ch - 'A' + 10;
    return -1;
}

static int append_utf8_codepoint(Buffer *buf, unsigned int cp) {
    char out[4];
    Py_ssize_t n = 0;
    if (cp <= 0x7f) { out[n++] = (char)cp; }
    else if (cp <= 0x7ff) {
        out[n++] = (char)(0xc0 | (cp >> 6));
        out[n++] = (char)(0x80 | (cp & 0x3f));
    } else if (cp <= 0xffff) {
        out[n++] = (char)(0xe0 | (cp >> 12));
        out[n++] = (char)(0x80 | ((cp >> 6) & 0x3f));
        out[n++] = (char)(0x80 | (cp & 0x3f));
    } else if (cp <= 0x10ffff) {
        out[n++] = (char)(0xf0 | (cp >> 18));
        out[n++] = (char)(0x80 | ((cp >> 12) & 0x3f));
        out[n++] = (char)(0x80 | ((cp >> 6) & 0x3f));
        out[n++] = (char)(0x80 | (cp & 0x3f));
    } else return -1;
    return buffer_append(buf, out, n);
}

static void skip_ws(const char **p, const char *end) {
    while (*p < end && (**p == ' ' || **p == '\n' || **p == '\r' || **p == '\t')) (*p)++;
}

static PyObject *parse_json_string(const char **p, const char *end) {
    if (*p >= end || **p != '"') {
        PyErr_SetString(PyExc_ValueError, "native_response_json_string_expected");
        return NULL;
    }
    (*p)++;
    Buffer buf = {0};
    while (*p < end) {
        unsigned char ch = (unsigned char)*(*p)++;
        if (ch == '"') {
            PyObject *result = PyUnicode_DecodeUTF8(buf.data ? buf.data : "", buf.len, "strict");
            buffer_free(&buf);
            return result;
        }
        if (ch != '\\') {
            if (buffer_char(&buf, (char)ch) < 0) { buffer_free(&buf); return NULL; }
            continue;
        }
        if (*p >= end) break;
        char esc = *(*p)++;
        switch (esc) {
            case '"': case '\\': case '/': if (buffer_char(&buf, esc) < 0) goto fail; break;
            case 'b': if (buffer_char(&buf, '\b') < 0) goto fail; break;
            case 'f': if (buffer_char(&buf, '\f') < 0) goto fail; break;
            case 'n': if (buffer_char(&buf, '\n') < 0) goto fail; break;
            case 'r': if (buffer_char(&buf, '\r') < 0) goto fail; break;
            case 't': if (buffer_char(&buf, '\t') < 0) goto fail; break;
            case 'u': {
                if (end - *p < 4) goto parse_fail;
                int h0 = hex_digit((*p)[0]), h1 = hex_digit((*p)[1]), h2 = hex_digit((*p)[2]), h3 = hex_digit((*p)[3]);
                if (h0 < 0 || h1 < 0 || h2 < 0 || h3 < 0) goto parse_fail;
                unsigned int cp = (unsigned int)((h0 << 12) | (h1 << 8) | (h2 << 4) | h3);
                *p += 4;
                if (cp >= 0xd800 && cp <= 0xdbff && end - *p >= 6 && (*p)[0] == '\\' && (*p)[1] == 'u') {
                    int l0 = hex_digit((*p)[2]), l1 = hex_digit((*p)[3]), l2 = hex_digit((*p)[4]), l3 = hex_digit((*p)[5]);
                    if (l0 >= 0 && l1 >= 0 && l2 >= 0 && l3 >= 0) {
                        unsigned int low = (unsigned int)((l0 << 12) | (l1 << 8) | (l2 << 4) | l3);
                        if (low >= 0xdc00 && low <= 0xdfff) {
                            cp = 0x10000 + (((cp - 0xd800) << 10) | (low - 0xdc00));
                            *p += 6;
                        }
                    }
                }
                if (append_utf8_codepoint(&buf, cp) < 0) goto fail;
                break;
            }
            default: goto parse_fail;
        }
    }
parse_fail:
    PyErr_SetString(PyExc_ValueError, "native_response_json_parse_error");
fail:
    buffer_free(&buf);
    return NULL;
}

static PyObject *parse_flat_response(const char *data, Py_ssize_t size) {
    const char *p = data, *end = data + size;
    skip_ws(&p, end);
    if (p >= end || *p++ != '{') {
        PyErr_SetString(PyExc_ValueError, "native_response_json_object_expected");
        return NULL;
    }
    PyObject *dict = PyDict_New();
    if (dict == NULL) return NULL;
    skip_ws(&p, end);
    if (p < end && *p == '}') { p++; return dict; }
    while (p < end) {
        skip_ws(&p, end);
        PyObject *key = parse_json_string(&p, end);
        if (key == NULL) goto fail;
        skip_ws(&p, end);
        if (p >= end || *p++ != ':') { Py_DECREF(key); PyErr_SetString(PyExc_ValueError, "native_response_json_colon_expected"); goto fail; }
        skip_ws(&p, end);
        PyObject *value = NULL;
        if (p < end && *p == '"') {
            value = parse_json_string(&p, end);
        } else if (end - p >= 4 && memcmp(p, "true", 4) == 0) {
            p += 4; value = Py_NewRef(Py_True);
        } else if (end - p >= 5 && memcmp(p, "false", 5) == 0) {
            p += 5; value = Py_NewRef(Py_False);
        } else if (end - p >= 4 && memcmp(p, "null", 4) == 0) {
            p += 4; value = Py_NewRef(Py_None);
        } else if (p < end && (*p == '-' || isdigit((unsigned char)*p))) {
            const char *start = p++;
            while (p < end && isdigit((unsigned char)*p)) p++;
            value = PyLong_FromString((char *)start, NULL, 10);
        } else {
            Py_DECREF(key);
            PyErr_SetString(PyExc_ValueError, "native_response_json_value_unsupported");
            goto fail;
        }
        if (value == NULL) { Py_DECREF(key); goto fail; }
        if (PyDict_SetItem(dict, key, value) < 0) { Py_DECREF(key); Py_DECREF(value); goto fail; }
        Py_DECREF(key); Py_DECREF(value);
        skip_ws(&p, end);
        if (p < end && *p == ',') { p++; continue; }
        if (p < end && *p == '}') { p++; skip_ws(&p, end); if (p != end) { PyErr_SetString(PyExc_ValueError, "native_response_json_trailing_data"); goto fail; } return dict; }
        PyErr_SetString(PyExc_ValueError, "native_response_json_separator_expected");
        goto fail;
    }
    PyErr_SetString(PyExc_ValueError, "native_response_json_unterminated_object");
fail:
    Py_DECREF(dict);
    return NULL;
}

static int read_process_starttime(pid_t pid, char *out, size_t out_size) {
    char path[64];
    snprintf(path, sizeof(path), "/proc/%ld/stat", (long)pid);
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd < 0) return -1;
    char data[8192];
    ssize_t n = read(fd, data, sizeof(data) - 1);
    int saved = errno;
    close(fd);
    errno = saved;
    if (n <= 0) return -1;
    data[n] = '\0';
    char *tail = strrchr(data, ')');
    if (tail == NULL || tail[1] != ' ') return -1;
    char *p = tail + 2;
    for (int index = 0; index <= 19; index++) {
        while (*p == ' ') p++;
        if (!*p) return -1;
        char *start = p;
        while (*p && *p != ' ') p++;
        if (index == 19) {
            size_t len = (size_t)(p - start);
            if (len + 1 > out_size) return -1;
            memcpy(out, start, len);
            out[len] = '\0';
            return 0;
        }
    }
    return -1;
}

static int verify_broker_generation(void) {
    if (!broker_configured) {
        PyErr_SetString(PyExc_RuntimeError, "authority_broker_not_configured");
        return -1;
    }
    char observed[128];
    if (read_process_starttime(broker_pid, observed, sizeof(observed)) < 0) {
        PyErr_SetString(PyExc_ValueError, "authority_broker_identity_unavailable");
        return -1;
    }
    if (strcmp(observed, broker_starttime) != 0) {
        PyErr_SetString(PyExc_ValueError, "authority_broker_identity_mismatch");
        return -1;
    }
    return 0;
}

static int send_all(int fd, const char *data, Py_ssize_t size) {
    Py_ssize_t sent = 0;
    while (sent < size) {
        ssize_t n = send(fd, data + sent, (size_t)(size - sent), MSG_NOSIGNAL);
        if (n < 0) { if (errno == EINTR) continue; return -1; }
        if (n == 0) return -1;
        sent += (Py_ssize_t)n;
    }
    return 0;
}

static PyObject *transport_roundtrip(PyObject *request) {
    if (!PyDict_CheckExact(request)) {
        PyErr_SetString(PyExc_TypeError, "authority_broker_request_must_be_exact_dict");
        return NULL;
    }
    if (verify_broker_generation() < 0) return NULL;

    Buffer wire = {0};
    if (json_value(&wire, request, 0) < 0 || buffer_char(&wire, '\n') < 0) {
        buffer_free(&wire);
        return NULL;
    }

    int fd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0) {
        buffer_free(&wire);
        PyErr_SetString(PyExc_ValueError, "authority_broker_unavailable");
        return NULL;
    }
    struct timeval timeout = {30, 0};
    (void)setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    (void)setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));

    struct sockaddr_un address;
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    size_t path_len = strlen(broker_path);
    if (path_len >= sizeof(address.sun_path)) {
        close(fd); buffer_free(&wire);
        PyErr_SetString(PyExc_ValueError, "authority_broker_path_too_long");
        return NULL;
    }
    memcpy(address.sun_path, broker_path, path_len + 1);
    if (connect(fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        close(fd); buffer_free(&wire);
        PyErr_SetString(PyExc_ValueError, "authority_broker_unavailable");
        return NULL;
    }

    struct ucred cred;
    socklen_t cred_size = sizeof(cred);
    if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, &cred, &cred_size) < 0 || cred.pid != broker_pid || cred.uid != broker_uid) {
        close(fd); buffer_free(&wire);
        PyErr_SetString(PyExc_ValueError, "authority_broker_identity_mismatch");
        return NULL;
    }

    if (send_all(fd, wire.data, wire.len) < 0) {
        close(fd); buffer_free(&wire);
        PyErr_SetString(PyExc_ValueError, "authority_broker_unavailable");
        return NULL;
    }
    buffer_free(&wire);

    Buffer response_wire = {0};
    char chunk[4096];
    int found_newline = 0;
    while (!found_newline) {
        ssize_t n = recv(fd, chunk, sizeof(chunk), 0);
        if (n < 0) { if (errno == EINTR) continue; close(fd); buffer_free(&response_wire); PyErr_SetString(PyExc_ValueError, "authority_broker_unavailable"); return NULL; }
        if (n == 0) { close(fd); buffer_free(&response_wire); PyErr_SetString(PyExc_ValueError, "authority_broker_unavailable"); return NULL; }
        for (ssize_t i = 0; i < n; i++) {
            if (chunk[i] == '\n') {
                if (buffer_append(&response_wire, chunk, (Py_ssize_t)i) < 0) { close(fd); buffer_free(&response_wire); return NULL; }
                found_newline = 1;
                break;
            }
        }
        if (!found_newline && buffer_append(&response_wire, chunk, (Py_ssize_t)n) < 0) { close(fd); buffer_free(&response_wire); return NULL; }
        if (response_wire.len > 1000000) { close(fd); buffer_free(&response_wire); PyErr_SetString(PyExc_ValueError, "authority_broker_protocol_error"); return NULL; }
    }
    close(fd);

    PyObject *response = parse_flat_response(response_wire.data ? response_wire.data : "", response_wire.len);
    buffer_free(&response_wire);
    if (response == NULL) return NULL;

    PyObject *request_id = PyDict_GetItemString(request, "request_id");
    PyObject *response_id = PyDict_GetItemString(response, "request_id");
    if (request_id == NULL || response_id == NULL || PyObject_RichCompareBool(request_id, response_id, Py_EQ) != 1) {
        Py_DECREF(response);
        PyErr_SetString(PyExc_ValueError, "authority_broker_response_mismatch");
        return NULL;
    }
    PyObject *ok = PyDict_GetItemString(response, "ok");
    if (ok != Py_True) {
        PyObject *error = PyDict_GetItemString(response, "error");
        const char *message = (error && PyUnicode_Check(error)) ? PyUnicode_AsUTF8(error) : "authority_broker_protocol_error";
        Py_DECREF(response);
        if (message == NULL) return NULL;
        PyErr_SetString(PyExc_ValueError, message);
        return NULL;
    }
    successful_transport_roundtrips++;
    return response;
}
