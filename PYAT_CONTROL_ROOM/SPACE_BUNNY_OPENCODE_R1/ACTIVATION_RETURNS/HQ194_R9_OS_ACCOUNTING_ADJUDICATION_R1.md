# HQ194 — R9 OS-accounting return adjudication and architecture-warrant fork

Status:
`R9_LOWER_LAYER_UNGOVERNABLE_ON_CURRENT_HOST_RUNTIME__BLOCKER_PRESERVED__ARCHITECTURE_WARRANT_FORK_BOUND`

Reviewed return:
`agent/rabochii-pyat-hq192-r9-os-accounting-interposition-r1 @ 81a006638b8a21a19150fa35c9caba544d272550`

Accepted disposition:
`R9_PARTIAL__LOWER_LAYER_STILL_UNGOVERNABLE`

## Accepted findings

The return is accepted as a truthful source-free blocker-preservation result.

### Part A — literal path-level OS opens

The current Darwin/Python/pyreadstat execution surface cannot lawfully observe or enforce the compiled reader's literal path-level `open(2)` accounting using the unprivileged mechanisms tested.

Accepted evidence:
- plain `DYLD_INSERT_LIBRARIES` symbol definitions loaded but failed even on a direct libc.open control, so zero observations are mechanism failure, not evidence of zero opens;
- `__DATA,__interpose` tuples make the tested CPython processes fail at startup, including cold getpid interception;
- the same behavior occurs on both available interpreters;
- SIP is enabled;
- available tracing tools requiring root are outside the commissioned no-sudo authority.

No OS-open count is inferred from zero observations.

### Part B — selected-column count

No executable `usecols`/selected-column reader owner exists across the current 23-module closure.

Selected-variable exactness is real and governed by contract/acceptance checks. A selected-read COUNT would currently name an operation the decoder does not perform.

No count is invented.

### Part C — SRC26 header-prefix owner

The prior "not performed" finding is narrowed.

An executable source-free owner exists:
`rawlsing_next/pre553_physical_decoder.py::_raw_layout_declarations`

It performs:
- one Python-level path open;
- one bounded prefix read;
- 176 bytes for SAV, 512 bytes for DTA at this owner.

Pre-operation refusal of excess header-prefix work was demonstrated on synthetic carriers.

This closes the owner/measurability question for that account at the Python layer, not the literal OS-open account.

### Additional accepted observations

The lane identified:
- two Python-level opens per ordinary decode path exercised: full-file hash + header prefix;
- Python-visible byte accounting for those operations;
- a third reader invocation site through `iter_batches -> pyreadstat.read_file_in_chunks`;
- compiled-reader internal opens/bytes remain unobservable on the current host surface.

## Why R9 remains

The frozen O1-C07 law requires separate accounting for:
- file hash passes;
- path-level opens and measurement basis;
- metadata;
- header-prefix;
- decoder;
- selected/full reads;
- bytes where measurable;
- retries.

Its acceptance says:
`Freeze expected budgets and instrumentation before launch; retain measured counts.`

C4B's unsigned warrant template requires exact accounting fields per source but intentionally leaves them as requirement tokens.

AT20 requires declared read/decoder counts and stop laws to remain exact.

The current runtime can neither:
1. lawfully measure the literal compiled-reader OS-open count on this host; nor
2. enforce a frozen maximum at that literal layer.

Therefore R9 is not closed by replacing path opens with reader invocations or Python-level opens.

## Stage-ownership ambiguity requiring adjudication

There is now a consequential ambiguity in the combined authority:

- O1-C07 is staged `DURING_EXECUTION_AND_RETURN`;
- its acceptance requires expected budgets/instrumentation frozen `before launch`;
- C4B leaves exact values as issuance-time requirement tokens;
- the current host/runtime cannot observe one mandatory named account.

The next question is not another tracing experiment.

It is whether the governing contract requires:
A. literal exact OS-open budget + measurement under the current runtime;
B. exact application-level source-access events with a separately disclosed unobservable compiled-reader interior;
C. a runtime change that makes literal opens observable;
D. privileged tracing authority;
E. another exact architecture disposition.

Because C4's own terminal set includes:
`ARCHITECTURE_WARRANT — demonstrate a required grain that existing jurisdictions cannot represent or lawfully succeed`,
HQ treats this as a potential architecture-warrant case.

## Next two lanes

1. Documentary/forensic stage-ownership and architecture-warrant packet.
2. Source-free minimal runtime-instrumentation feasibility lane, to determine whether a narrowly instrumented pyreadstat/ReadStat execution surface could expose/enforce the missing account without changing survey semantics, and what requalification burden that would entail.

Neither lane may access real sources.

## Current state

- R7: CLOSED
- warrant-instrument technical blockers: 1 — R9
- live-execution blockers: 1 — host disk policy/capacity
- freeze blockers: 0
- HQ182 C4 non-adoption hold: still pending reserved Astra decision
- raw-source access: NOT AUTHORIZED
- locator discovery: NOT AUTHORIZED
- warrant issuance: NOT AUTHORIZED
- live C4: NOT AUTHORIZED
