#!/usr/bin/env sh
# Local-machine on-demand queue invocation; not a daemon or native receiving.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
exec python3 "$root/REMONT/SOROK/QUEUE/check_queue.py" run --repo "$root" --publish "$@"
