#include <stddef.h>
#include <stdlib.h>
/* Runtime-only compatibility shim. Rawlsing uses trust auth and no LDAP paths. */
void ldap_memfree(void *p) { free(p); }
int ldap_count_entries(void *ld, void *res) { (void)ld; (void)res; return 0; }
int ldap_get_option(void *ld, int opt, void *out) { (void)ld; (void)opt; (void)out; return -1; }
int ldap_initialize(void **ldp, const char *uri) { (void)uri; if (ldp) *ldp = NULL; return -1; }
int ldap_simple_bind_s(void *ld, const char *who, const char *cred) { (void)ld; (void)who; (void)cred; return -1; }
void *ldap_first_entry(void *ld, void *res) { (void)ld; (void)res; return NULL; }
void ldap_free_urldesc(void *ludp) { (void)ludp; }
int ldap_dn2domain(const char *dn, char **domainp) { (void)dn; if (domainp) *domainp=NULL; return -1; }
int ldap_search_s(void *ld, const char *base, int scope, const char *filter, char **attrs, int attrsonly, void **res) { (void)ld;(void)base;(void)scope;(void)filter;(void)attrs;(void)attrsonly;if(res)*res=NULL;return -1; }
const char *ldap_err2string(int err) { (void)err; return "LDAP unavailable in offline Rawlsing runtime"; }
int ldap_unbind(void *ld) { (void)ld; return 0; }
int ldap_url_parse(const char *url, void **ludpp) { (void)url; if(ludpp)*ludpp=NULL; return -1; }
int ldap_unbind_s(void *ld) { (void)ld; return 0; }
int ldap_set_option(void *ld, int opt, const void *in) { (void)ld;(void)opt;(void)in;return -1; }
int ldap_start_tls_s(void *ld, void *serverctrls, void *clientctrls) { (void)ld;(void)serverctrls;(void)clientctrls;return -1; }
int ldap_msgfree(void *msg) { (void)msg; return 0; }
char *ldap_get_dn(void *ld, void *entry) { (void)ld;(void)entry;return NULL; }
int ldap_domain2hostlist(const char *domain, char **hostlist) { (void)domain;if(hostlist)*hostlist=NULL;return -1; }
void **ldap_get_values_len(void *ld, void *entry, const char *target) { (void)ld;(void)entry;(void)target;return NULL; }
void *ldap_init(const char *host, int port) { (void)host;(void)port;return NULL; }
int ldap_result(void *ld, int msgid, int all, const void *timeout, void **result) { (void)ld;(void)msgid;(void)all;(void)timeout;if(result)*result=NULL;return -1; }
int ldap_search_st(void *ld, const char *base, int scope, const char *filter, char **attrs, int attrsonly, const void *timeout, void **res) { (void)ld;(void)base;(void)scope;(void)filter;(void)attrs;(void)attrsonly;(void)timeout;if(res)*res=NULL;return -1; }
int ldap_simple_bind(void *ld, const char *who, const char *cred) { (void)ld;(void)who;(void)cred;return -1; }
void ldap_value_free_len(void **vals) { (void)vals; }
