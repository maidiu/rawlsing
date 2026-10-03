#!/bin/sh
# HQ192 Part A — reproducible interposition probe.
#
# Runs the same matrix that produced the negative result recorded in
# interposition_matrix.json. Source-free. Synthetic carriers only.
# No sudo. No system installation. Process-local only.
#
# Usage: sh run_interposition_probe.sh
# Writes: interposition_probe_live.json  (in this directory)

set -u
HERE=$(cd "$(dirname "$0")" && pwd)
BUILD="$HERE/build"
UV=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/c4c3-env/bin/python3.11
FW=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11

mkdir -p "$BUILD"

# Build the three single-symbol interposers used by the matrix.
gen() { # $1=symbol
  case "$1" in
    getpid)
      cat > "$BUILD/v_$1.c" <<'EOF'
#define _GNU_SOURCE
#include <dlfcn.h>
#include <unistd.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static pid_t r9_f(void){ static pid_t(*real)(void); if(!real) real=dlsym(RTLD_NEXT,"getpid"); return real(); }
DYLD_INTERPOSE(r9_f, getpid)
EOF
      ;;
    stat)
      cat > "$BUILD/v_$1.c" <<'EOF'
#define _GNU_SOURCE
#include <dlfcn.h>
#include <sys/stat.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static int r9_f(const char*p, struct stat*b){ static int(*real)(const char*,struct stat*); if(!real) real=dlsym(RTLD_NEXT,"stat"); return real(p,b); }
DYLD_INTERPOSE(r9_f, stat)
EOF
      ;;
    open)
      cat > "$BUILD/v_$1.c" <<'EOF'
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static int r9_f(const char*p,int f,...){ static int(*real)(const char*,int,...); if(!real) real=dlsym(RTLD_NEXT,"open");
 mode_t m=0; if(f&O_CREAT){va_list a;va_start(a,f);m=(mode_t)va_arg(a,int);va_end(a);} return real(p,f,m); }
DYLD_INTERPOSE(r9_f, open)
EOF
      ;;
  esac
  clang -dynamiclib -O1 -o "$BUILD/lib$1.dylib" "$BUILD/v_$1.c" 2>/dev/null
}

for s in getpid stat open; do gen "$s"; done

OUT="$HERE/interposition_probe_live.json"
printf '{\n  "probe": "HQ192 Part A interposition matrix",\n  "results": [\n' > "$OUT"
first=1
for py in "$UV|uv_c4c3" "$FW|framework"; do
  P=${py%%|*}; N=${py##*|}
  if [ ! -x "$P" ]; then continue; fi
  for lib in none libgetpid libstat libopen; do
    if [ "$lib" = "none" ]; then
      OUTP=$("$P" -c "print('OK')" 2>/dev/null); RC=$?
    else
      OUTP=$(DYLD_INSERT_LIBRARIES="$BUILD/$lib.dylib" "$P" -c "print('OK')" 2>/dev/null); RC=$?
    fi
    [ $first -eq 1 ] || printf ',\n' >> "$OUT"
    first=0
    printf '    {"interposed": "%s", "interpreter": "%s", "rc": %s, "stdout": "%s"}' \
      "$lib" "$N" "$RC" "$OUTP" >> "$OUT"
  done
done
printf '\n  ]\n}\n' >> "$OUT"
echo "wrote $OUT"
cat "$OUT"