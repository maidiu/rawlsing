#define _GNU_SOURCE
#include <dlfcn.h>
#include <sys/stat.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static int r9_f(const char*p, struct stat*b){ static int(*real)(const char*,struct stat*); if(!real) real=dlsym(RTLD_NEXT,"stat"); return real(p,b); }
DYLD_INTERPOSE(r9_f, stat)
