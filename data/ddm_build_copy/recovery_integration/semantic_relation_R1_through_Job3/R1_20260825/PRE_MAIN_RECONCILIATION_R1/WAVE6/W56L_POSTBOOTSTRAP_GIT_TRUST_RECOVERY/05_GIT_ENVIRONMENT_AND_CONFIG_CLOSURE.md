# Git environment and configuration closure

Git subprocesses receive a newly constructed environment, not `os.environ.copy()`. Parent `PATH` is absent.

| Variable / source | Disposition | Security reason |
|---|---|---|
| `PATH` | absent | cannot select Git or any helper |
| `GIT_DIR` | absent | cannot redirect repository |
| `GIT_WORK_TREE` | absent | cannot redirect worktree |
| `GIT_COMMON_DIR` | absent | cannot redirect shared repository metadata |
| `GIT_INDEX_FILE` | absent | index is irrelevant and cannot redirect state |
| `GIT_OBJECT_DIRECTORY` | absent | cannot redirect object store |
| `GIT_ALTERNATE_OBJECT_DIRECTORIES` | absent | cannot inject alternate objects |
| `GIT_NAMESPACE` | absent | cannot redirect refs into a namespace |
| `GIT_CONFIG` | absent | no injected config file authority |
| `GIT_CONFIG_GLOBAL` | forced to `os.devnull` | global config suppressed |
| `GIT_CONFIG_SYSTEM` | forced to `os.devnull` | system config suppressed |
| `GIT_CONFIG_NOSYSTEM` | `1` | system config suppressed defense-in-depth |
| `GIT_CONFIG_COUNT` | `0` | injected command-scope config entries suppressed |
| `GIT_EXEC_PATH` | absent | cannot redirect external Git helpers |
| `GIT_EXTERNAL_DIFF` | absent | external diff cannot be injected |
| `GIT_PAGER` / `PAGER` | empty + `--no-pager` | pager executable cannot run |
| `GIT_NO_REPLACE_OBJECTS` | `1` + `--no-replace-objects` | replacement semantics disabled |
| `GIT_NO_LAZY_FETCH` | `1` | missing object cannot trigger remote/helper fetch |
| `GIT_TERMINAL_PROMPT` | `0` | no prompt path |
| `HOME` / `XDG_CONFIG_HOME` | absent | no user/XDG config discovery |

On Windows only OS loader directory variables required for absolute process creation may be copied as host prerequisites; PATH remains absent.

Repository-local Git config is not governance authority. The used commands are exact builtins/plumbing; aliases cannot override builtins; no hooks are invoked; `cat-file` reads object bytes without filters; `diff-tree` uses `--no-ext-diff --no-textconv --no-renames`; no network command is used; lazy fetch is disabled.

Repository metadata attacks are separately closed by rejecting replacement refs, nonempty `info/grafts`, nonempty `objects/info/alternates`, shallow repositories, and a Git-reported worktree root that differs from the explicit repository root.