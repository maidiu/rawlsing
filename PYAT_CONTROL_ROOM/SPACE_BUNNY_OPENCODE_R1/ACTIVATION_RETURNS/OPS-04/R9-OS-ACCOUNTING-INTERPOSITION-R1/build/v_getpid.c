#define _GNU_SOURCE
#include <dlfcn.h>
#include <unistd.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static pid_t r9_f(void){ static pid_t(*real)(void); if(!real) real=dlsym(RTLD_NEXT,"getpid"); return real(); }
DYLD_INTERPOSE(r9_f, getpid)
