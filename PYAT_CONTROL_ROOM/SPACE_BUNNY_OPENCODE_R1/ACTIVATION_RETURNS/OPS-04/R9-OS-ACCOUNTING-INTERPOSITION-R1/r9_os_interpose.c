/*
 * r9_os_interpose.c — process-local, user-space libc interposition for the
 * R9 OS-level accounting gap.
 *
 * SCOPE AND LIMITS (read before trusting any number this produces)
 * --------------------------------------------------------------
 *  - Process-local. Loaded only into the python process that sets
 *    DYLD_INSERT_LIBRARIES. Never installed globally. No sudo. No system
 *    change. Reversible by unsetting the environment variable.
 *  - Unprivileged. Requires an interpreter that is NOT hardened-runtime
 *    signed and NOT SIP-protected. On this host the uv-managed
 *    LOCAL_COURTS CPython qualifies; the /Library/Frameworks python does not.
 *  - This observes SYSCALL-BOUNDARY libc entry points, not kernel audit
 *    records. It is an interposer, not an audit trail.
 *  - It cannot see operations performed by a library that issues raw
 *    syscalls without going through the interposed libc symbols.
 *
 * MEASUREMENT BASIS (declared explicitly, as O1-C07 requires)
 * ----------------------------------------------------------
 *  Every counted event is one ENTRY into an interposed libc function, in the
 *  calling process, on a path that is inside the configured prefix. The basis
 *  is "libc symbol entry count", NOT "kernel open(2) count" and NOT
 *  "distinct file access". Duplicates are possible where libsystem routes one
 *  logical access through more than one interposed symbol; the log records
 *  every entry so the distinction stays auditable.
 *
 * ENFORCEMENT
 * -----------
 *  When the configured maximum for an account is already consumed, the
 *  interposer returns failure (-1 / NULL) with errno set BEFORE calling the
 *  real function. The excess file operation therefore never executes.
 *
 * Environment:
 *   R9_PREFIX        path prefix to account for (required to scope events)
 *   R9_EVENTLOG      JSONL event log path (optional)
 *   R9_MAX_OPENS     max open/openat entries on prefixed paths (optional)
 *   R9_MAX_READS     max read/pread entries on prefixed fds (optional)
 *   R9_MAX_BYTES     max cumulative bytes read on prefixed fds (optional)
 */

#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

/* ---------------------------------------------------------------------
 * WHY DYLD_INTERPOSE AND NOT A PLAIN SYMBOL DEFINITION
 * ----------------------------------------------------
 * A first attempt in this lane defined plain functions named open/openat/
 * fopen/read/pread/close and loaded them with DYLD_INSERT_LIBRARIES. The
 * library loaded (its constructor and destructor both ran) but captured
 * ZERO events - including for a direct ctypes libc.open() call. The cause
 * is that libsystem symbols live in the dyld shared cache and a plain
 * definition does not interpose them. macOS requires an explicit
 * interposing tuple in the __DATA,__interpose section. That is what the
 * macro below emits. Recorded as finding MECH-01 in the return.
 * ------------------------------------------------------------------- */
#define DYLD_INTERPOSE(_replacement, _replacee) \
    __attribute__((used)) static struct {        \
        const void *replacement;                 \
        const void *replacee;                    \
    } _interpose_##_replacee                     \
    __attribute__((section("__DATA,__interpose"))) = { \
        (const void *)(unsigned long)&_replacement,     \
        (const void *)(unsigned long)&_replacee};

/* ---------------------------------------------------------------- state */

static char g_prefix[4096];
static size_t g_prefix_len = 0;
static int g_prefix_ready = 0;
static FILE *g_log = NULL;
static int g_log_ready = 0;

static long g_max_opens = -1;
static long g_max_reads = -1;
static long g_max_bytes = -1;

static long g_open_entries = 0;   /* open + openat + fopen entries on prefix */
static long g_read_entries = 0;   /* read + pread entries on prefixed fds   */
static long g_read_bytes = 0;     /* cumulative bytes on prefixed fds       */
static long g_close_entries = 0;
static long g_refused_opens = 0;
static long g_refused_reads = 0;

#define FD_TRACK 4096
static char g_fd_is_prefixed[FD_TRACK];

static void ensure_init(void) __attribute__((constructor));

static void ensure_init(void) {
    if (g_prefix_ready) return;
    const char *p = getenv("R9_PREFIX");
    if (p && *p) {
        strncpy(g_prefix, p, sizeof(g_prefix) - 1);
        g_prefix_len = strlen(g_prefix);
    }
    g_prefix_ready = 1;

    const char *l = getenv("R9_EVENTLOG");
    if (l && *l) {
        g_log = fopen(l, "a");
        if (g_log) setvbuf(g_log, NULL, _IOLBF, 0);
        g_log_ready = 1;
    }
    const char *mo = getenv("R9_MAX_OPENS");
    if (mo && *mo) g_max_opens = strtol(mo, NULL, 10);
    const char *mr = getenv("R9_MAX_READS");
    if (mr && *mr) g_max_reads = strtol(mr, NULL, 10);
    const char *mb = getenv("R9_MAX_BYTES");
    if (mb && *mb) g_max_bytes = strtol(mb, NULL, 10);

    memset(g_fd_is_prefixed, 0, sizeof(g_fd_is_prefixed));

    if (g_log_ready) {
        fprintf(g_log,
                "{\"event\":\"init\",\"pid\":%d,\"prefix\":\"%s\","
                "\"max_opens\":%ld,\"max_reads\":%ld,\"max_bytes\":%ld}\n",
                (int)getpid(), g_prefix, g_max_opens, g_max_reads, g_max_bytes);
    }
}

static int on_prefix(const char *path) {
    if (!g_prefix_ready || !path) return 0;
    if (g_prefix_len == 0) return 0;
    size_t n = strlen(path);
    if (n < g_prefix_len) return 0;
    return strncmp(path, g_prefix, g_prefix_len) == 0;
}

static void mark_fd(int fd, int prefixed) {
    if (fd >= 0 && fd < FD_TRACK) g_fd_is_prefixed[fd] = (char)(prefixed ? 1 : 0);
}
static int fd_prefixed(int fd) {
    if (fd >= 0 && fd < FD_TRACK) return g_fd_is_prefixed[fd];
    return 0;
}

static void emit(const char *sym, const char *path, int fd, long n, int refused) {
    if (!g_log_ready || !g_log) return;
    fprintf(g_log,
            "{\"event\":\"op\",\"sym\":\"%s\",\"path\":\"%s\",\"fd\":%d,"
            "\"n\":%ld,\"refused\":%d,\"open_entries\":%ld,\"read_entries\":%ld,"
            "\"read_bytes\":%ld}\n",
            sym, path ? path : "", fd, n, refused,
            g_open_entries, g_read_entries, g_read_bytes);
}

/* Refuse BEFORE calling the real function when the maximum is consumed. */
static int open_budget_exhausted(void) {
    return (g_max_opens >= 0 && g_open_entries >= g_max_opens);
}
static int read_budget_exhausted(void) {
    if (g_max_reads >= 0 && g_read_entries >= g_max_reads) return 1;
    if (g_max_bytes >= 0 && g_read_bytes >= g_max_bytes) return 1;
    return 0;
}

/* ------------------------------------------------------------ interposed */

typedef int (*open_fn)(const char *, int, ...);
typedef int (*openat_fn)(int, const char *, int, ...);
typedef FILE *(*fopen_fn)(const char *, const char *);
typedef ssize_t (*read_fn)(int, void *, size_t);
typedef ssize_t (*pread_fn)(int, void *, size_t, off_t);
typedef int (*close_fn)(int);

static int r9_open(const char *path, int flags, ...) {
    static open_fn real = NULL;
    if (!real) real = (open_fn)dlsym(RTLD_NEXT, "open");
    mode_t mode = 0;
    if (flags & O_CREAT) {
        va_list ap; va_start(ap, flags); mode = (mode_t)va_arg(ap, int); va_end(ap);
    }
    ensure_init();
    int scoped = on_prefix(path);
    if (scoped && open_budget_exhausted()) {
        g_open_entries++;            /* the attempt itself is an entry */
        g_refused_opens++;
        emit("open", path, -1, 0, 1);
        errno = EACCES;
        return -1;                   /* excess open NEVER executes */
    }
    int fd = real(path, flags, mode);
    if (scoped) { g_open_entries++; mark_fd(fd, 1); emit("open", path, fd, 0, 0); }
    return fd;
}

static int r9_openat(int dirfd, const char *path, int flags, ...) {
    static openat_fn real = NULL;
    if (!real) real = (openat_fn)dlsym(RTLD_NEXT, "openat");
    mode_t mode = 0;
    if (flags & O_CREAT) {
        va_list ap; va_start(ap, flags); mode = (mode_t)va_arg(ap, int); va_end(ap);
    }
    ensure_init();
    int scoped = on_prefix(path);
    if (scoped && open_budget_exhausted()) {
        g_open_entries++;
        g_refused_opens++;
        emit("openat", path, -1, 0, 1);
        errno = EACCES;
        return -1;
    }
    int fd = real(dirfd, path, flags, mode);
    if (scoped) { g_open_entries++; mark_fd(fd, 1); emit("openat", path, fd, 0, 0); }
    return fd;
}

static FILE *r9_fopen(const char *path, const char *mode) {
    static fopen_fn real = NULL;
    if (!real) real = (fopen_fn)dlsym(RTLD_NEXT, "fopen");
    ensure_init();
    int scoped = on_prefix(path);
    if (scoped && open_budget_exhausted()) {
        g_open_entries++;
        g_refused_opens++;
        emit("fopen", path, -1, 0, 1);
        errno = EACCES;
        return NULL;                 /* excess fopen NEVER executes */
    }
    FILE *f = real(path, mode);
    if (scoped) {
        g_open_entries++;
        emit("fopen", path, f ? fileno(f) : -1, 0, 0);
        if (f) mark_fd(fileno(f), 1);
    }
    return f;
}

static ssize_t r9_read(int fd, void *buf, size_t n) {
    static read_fn real = NULL;
    if (!real) real = (read_fn)dlsym(RTLD_NEXT, "read");
    ensure_init();
    if (fd_prefixed(fd) && read_budget_exhausted()) {
        g_read_entries++;
        g_refused_reads++;
        emit("read", NULL, fd, (long)n, 1);
        errno = EACCES;
        return -1;                   /* excess read NEVER executes */
    }
    ssize_t got = real(fd, buf, n);
    if (fd_prefixed(fd)) {
        g_read_entries++;
        if (got > 0) g_read_bytes += (long)got;
        emit("read", NULL, fd, (long)got, 0);
    }
    return got;
}

static ssize_t r9_pread(int fd, void *buf, size_t n, off_t off) {
    static pread_fn real = NULL;
    if (!real) real = (pread_fn)dlsym(RTLD_NEXT, "pread");
    ensure_init();
    if (fd_prefixed(fd) && read_budget_exhausted()) {
        g_read_entries++;
        g_refused_reads++;
        emit("pread", NULL, fd, (long)n, 1);
        errno = EACCES;
        return -1;
    }
    ssize_t got = real(fd, buf, n, off);
    if (fd_prefixed(fd)) {
        g_read_entries++;
        if (got > 0) g_read_bytes += (long)got;
        emit("pread", NULL, fd, (long)got, 0);
    }
    return got;
}

static int r9_close(int fd) {
    static close_fn real = NULL;
    if (!real) real = (close_fn)dlsym(RTLD_NEXT, "close");
    ensure_init();
    int scoped = fd_prefixed(fd);
    int r = real(fd);
    if (scoped) { g_close_entries++; mark_fd(fd, 0); emit("close", NULL, fd, 0, 0); }
    return r;
}

/* Interposing tuples. These are what actually redirect the calls. */
DYLD_INTERPOSE(r9_open,     open)
DYLD_INTERPOSE(r9_openat,   openat)
DYLD_INTERPOSE(r9_fopen,    fopen)
DYLD_INTERPOSE(r9_read,     read)
DYLD_INTERPOSE(r9_pread,    pread)
DYLD_INTERPOSE(r9_close,    close)

/* --------------------------------------------- end-of-run summary hook */

__attribute__((destructor)) static void emit_summary(void) {
    if (!g_log_ready || !g_log) return;
    fprintf(g_log,
            "{\"event\":\"summary\",\"pid\":%d,\"open_entries\":%ld,"
            "\"read_entries\":%ld,\"read_bytes\":%ld,\"close_entries\":%ld,"
            "\"refused_opens\":%ld,\"refused_reads\":%ld}\n",
            (int)getpid(), g_open_entries, g_read_entries, g_read_bytes,
            g_close_entries, g_refused_opens, g_refused_reads);
    fclose(g_log);
    g_log = NULL;
}