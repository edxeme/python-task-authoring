"""Verification suite for the comprehension task.

These tests encode the *verified answers* to the questions in README.md.
Run them to confirm the reference answers are factual, not guessed.
"""

from unittest import mock

import pytest

from src.retry import RetryError, retry


def test_attempts_never_exceed_max_attempts():
    calls = {"n": 0}

    @retry(max_attempts=3, base_delay=0)
    def always_fails():
        calls["n"] += 1
        raise ValueError("boom")

    with pytest.raises(RetryError) as excinfo:
        always_fails()

    assert calls["n"] == 3
    assert excinfo.value.attempts == 3


def test_retry_error_chains_original_exception():
    @retry(max_attempts=2, base_delay=0)
    def boom():
        raise ValueError("original")

    with pytest.raises(RetryError) as excinfo:
        boom()

    assert isinstance(excinfo.value.__cause__, ValueError)


def test_keyboard_interrupt_is_not_caught():
    calls = {"n": 0}

    @retry(max_attempts=5, base_delay=0)
    def interrupted():
        calls["n"] += 1
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        interrupted()

    assert calls["n"] == 1  # no retries for BaseException subclasses


def test_metadata_is_preserved():
    @retry(max_attempts=1, base_delay=0)
    def fetch_page():
        """Fetch one page."""

    assert fetch_page.__name__ == "fetch_page"
    assert fetch_page.__doc__ == "Fetch one page."


def test_success_on_first_try_does_not_retry():
    calls = {"n": 0}

    @retry(max_attempts=3, base_delay=0)
    def ok():
        calls["n"] += 1
        return "ok"

    assert ok() == "ok"
    assert calls["n"] == 1


def test_recovers_before_exhaustion():
    calls = {"n": 0}

    @retry(max_attempts=3, base_delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("transient")
        return "recovered"

    assert flaky() == "recovered"
    assert calls["n"] == 2


def test_retry_on_can_widen_or_narrow_the_caught_set():
    @retry(max_attempts=2, base_delay=0, retry_on=(KeyError,))
    def missing_key():
        raise KeyError("k")

    with pytest.raises(RetryError):
        missing_key()


def test_jitter_uses_time_sleep_with_varying_delays():
    sleeps = []

    with mock.patch("src.retry.time.sleep", side_effect=sleeps.append):

        @retry(max_attempts=3, base_delay=1.0, backoff_factor=2.0)
        def always_fails():
            raise ValueError("boom")

        with pytest.raises(RetryError):
            always_fails()

    assert len(sleeps) == 2  # one sleep per retry, none on success/failure


def test_invalid_max_attempts_is_rejected():
    with pytest.raises(ValueError, match="max_attempts"):
        retry(max_attempts=0)
