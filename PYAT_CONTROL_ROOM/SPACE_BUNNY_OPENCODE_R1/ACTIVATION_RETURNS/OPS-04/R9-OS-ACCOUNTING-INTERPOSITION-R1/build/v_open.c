#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#define DYLD_INTERPOSE(r,x) __attribute__((used)) static struct{const void*r;const void*x;} _i_##x \
  __attribute__((section("__DATA,__interpose"))) = {(const void*)(unsigned long)&r,(const void*)(unsigned long)&x};
static int r9_f(const char*p,int f,...){ static int(*real)(const char*,int,...); if(!real) real=dlsym(RTLD_NEXT,"open");
 mode_t m=0; if(f&O_CREAT){va_list a;va_start(a,f);m=(mode_t)va_arg(a,int);va_end(a);} return real(p,f,m); }
DYLD_INTERPOSE(r9_f, open)
