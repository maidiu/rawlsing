# Successor-closes-parent attack

The central dependency/return graph correctly preserves successor relationships and explicit `RETURN_TO` edges; protocol text says spawning a successor never closes its parent by inference.

Machine ruling: `BYPASS_FOUND`.

The validator rejects `spawned_successors` only when `return_to_ids` is empty. It does not prove one valid return edge per successor, does not validate the target against the dependency/return graph, and does not check that the parent remains open. Any nonempty `return_to_ids` value satisfies the check, while `local_status` is ignored.

Thus literal successor-with-no-return is rejected, but a fake return token plus parent-close claim can pass. That is constitutionally equivalent to the forbidden path.
