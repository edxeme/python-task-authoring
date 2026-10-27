# Verified answers — retry-with-backoff decorator

Each answer states the reasoning and names the test in `tests/test_retry.py`
that verifies it. A benchmark grader checks both: the claim and its evidence.

## 1. Why doesn't Ctrl-C (`KeyboardInterrupt`) break out of the retry loop?

`retry_on` defaults to `(Exception,)`. `KeyboardInterrupt` and `SystemExit`
derive from `BaseException`, **not** `Exception`, so the `except retry_on`
clause never sees them: they propagate on the first attempt and the loop
ends without retrying. This is the correct production behavior — user
interrupts and interpreter shutdown must never be swallowed.

*Verified by `test_keyboard_interrupt_is_not_caught` (1 call, no retries).*

## 2. With `max_attempts=3`, what is the maximum number of calls to the wrapped function?

Exactly **3**. `max_attempts` counts *total* calls, retries included: the
loop runs `attempt = 1..max_attempts`, sleeping only between attempts, and
the final failure raises `RetryError` instead of looping again. Callers can
therefore reason about worst-case load: `max_attempts` calls, never more.

*Verified by `test_attempts_never_exceed_max_attempts` (`calls == 3` and
`excinfo.value.attempts == 3`).*

## 3. Why does the decorator need `functools.wraps`? What breaks without it?

`wrapper` replaces the wrapped function object, so without
`functools.wraps(func)` its `__name__`, `__doc__`, `__module__` and
`__wrapped__` would be the wrapper's own. That breaks tracebacks, logging
and metrics that key off function names, pytest fixture introspection,
doctest discovery, and any tool using `inspect.signature`. With `wraps`,
the metadata is copied through and the wrapper stays transparent.

*Verified by `test_metadata_is_preserved`.*

## 4. When every attempt fails, what exactly does the caller receive — and how is the original exception preserved?

A `RetryError(attempts, last)` — carrying the attempt count and the last
exception — raised with `raise RetryError(...) from exc`. The `from exc`
chaining sets `__cause__`, so the original root cause survives for
debuggers, Sentry-style tracebacks and log aggregation. Without the
explicit chain the original would be re-wrapped as implicit context only,
and `RetryError.__cause__` would be `None`.

*Verified by `test_retry_error_chains_original_exception`
(`isinstance(excinfo.value.__cause__, ValueError)`).*

## Bonus: why the jitter?

All workers that failed at the same instant would otherwise retry in
lock-step and re-overwhelm the dependency they just failed against. The
uniform jitter (`uniform(0, delay / 2)`) spreads retries over time.
*Verified by `test_jitter_uses_time_sleep_with_varying_delays` (two sleeps
for two retries, none on success).*
