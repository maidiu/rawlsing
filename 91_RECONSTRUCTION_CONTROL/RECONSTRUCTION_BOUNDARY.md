# Reconstruction boundary

This worktree begins from the verified v41 multipart handoff. Sections 00–62 are executable authority evidence. Inherited Sections 63–80 are recovery records only and are not imported as P3C decisions.

The PostgreSQL LDAP compatibility library in `runtime_compat/` exists solely because the bundled Debian PostgreSQL 15 binary requires the OpenLDAP 2.5 symbol version while the host ships OpenLDAP 2.6. Rawlsing runs with local trust authentication and does not invoke LDAP. The shim implements only fail-closed stubs and changes no Rawlsing code, evidence, schema, or authority logic.
