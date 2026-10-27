"""Retry decorator with exponential backoff.

Small, production-flavored utility — the kind of code found inside HTTP
clients and job runners. Used by the comprehension task in this folder.
"""

from __future__ import annotations

import functools
import random
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class RetryError(RuntimeError):
    """Raised when all attempts are exhausted."""

    def __init__(self, attempts: int, last: BaseException) -> None:
        super().__init__(f"giving up after {attempts} attempt(s): {last!r}")
        self.attempts = attempts
        self.last = last


def retry(
    max_attempts: int = 3,
    base_delay: float = 0.1,
    backoff_factor: float = 2.0,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[F], F]:
    """Decorate *func* so it is retried with exponential backoff.

    - ``max_attempts`` counts the total number of calls, retries included.
    - Sleeps ``base_delay`` before the first retry, then multiplies the
      delay by ``backoff_factor`` after every failed attempt. A uniform
      jitter of up to 50% of the current delay avoids thundering herds.
    - Only exceptions in ``retry_on`` are retried; anything else (including
      ``KeyboardInterrupt`` and ``SystemExit``) propagates immediately.
    - When every attempt fails, raises ``RetryError`` chained to the last
      underlying exception.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_on as exc:
                    if attempt == max_attempts:
                        raise RetryError(attempt, exc) from exc
                    time.sleep(delay + random.uniform(0, delay / 2))
                    delay *= backoff_factor
            raise AssertionError("unreachable: attempt loop must return or raise")

        return wrapper  # type: ignore[return-value]

    return decorator
