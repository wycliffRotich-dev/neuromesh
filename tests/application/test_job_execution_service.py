from __future__ import annotations

from datetime import timedelta

from app.application.services.job_execution_service import (
    JobExecutionService,
)

_IGNORE_SIGTERM_AND_SLEEP = (
    "import signal, time; "
    "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
    "time.sleep(30)"
)


def test_execute_with_no_command_succeeds_immediately() -> None:
    service = JobExecutionService()

    result = service.execute(
        command=None,
        timeout=timedelta(seconds=1),
    )

    assert result.succeeded is True
    assert result.timed_out is False
    assert result.exit_code == 0


def test_execute_successful_command() -> None:
    service = JobExecutionService()

    result = service.execute(
        command=["python3", "-c", "print('hello')"],
        timeout=timedelta(seconds=5),
    )

    assert result.succeeded is True
    assert result.timed_out is False
    assert result.exit_code == 0
    assert "hello" in result.stdout


def test_execute_failing_command() -> None:
    service = JobExecutionService()

    result = service.execute(
        command=["python3", "-c", "import sys; sys.exit(1)"],
        timeout=timedelta(seconds=5),
    )

    assert result.succeeded is False
    assert result.timed_out is False
    assert result.exit_code == 1


def test_execute_terminates_gracefully_on_timeout() -> None:
    """
    A well-behaved process that respects SIGTERM should be
    stopped by the graceful signal alone, well within the
    grace period, never reaching SIGKILL.
    """
    service = JobExecutionService(
        termination_grace_period=timedelta(seconds=3),
    )

    result = service.execute(
        command=["python3", "-c", "import time; time.sleep(30)"],
        timeout=timedelta(seconds=0.5),
    )

    assert result.succeeded is False
    assert result.timed_out is True
    assert result.duration < timedelta(seconds=3)


def test_execute_force_kills_command_that_ignores_sigterm() -> None:
    """
    A process that explicitly ignores SIGTERM must still be
    stopped, via SIGKILL, once the grace period elapses.
    This is the test that actually proves the escalation
    path works, rather than only proving SIGTERM alone is
    often sufficient.
    """
    service = JobExecutionService(
        termination_grace_period=timedelta(seconds=1),
    )

    result = service.execute(
        command=["python3", "-c", _IGNORE_SIGTERM_AND_SLEEP],
        timeout=timedelta(seconds=0.5),
    )

    assert result.succeeded is False
    assert result.timed_out is True
    # Grace period (1s) + timeout budget (0.5s) + slack,
    # but nowhere near the process's own 30s sleep.
    assert result.duration < timedelta(seconds=5)


def test_execute_captures_stderr() -> None:
    service = JobExecutionService()

    result = service.execute(
        command=[
            "python3",
            "-c",
            "import sys; print('oops', file=sys.stderr)",
        ],
        timeout=timedelta(seconds=5),
    )

    assert "oops" in result.stderr
