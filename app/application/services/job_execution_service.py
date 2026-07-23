from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from datetime import timedelta

DEFAULT_TERMINATION_GRACE_PERIOD = timedelta(seconds=5)


@dataclass(frozen=True, slots=True)
class JobExecutionResult:
    """
    The outcome of one real subprocess execution attempt.

    timed_out distinguishes "the process ran and exited
    with a nonzero code" from "we killed it ourselves
    because it exceeded its timeout" -- both are failures,
    but they're different failures worth being able to
    tell apart in logs, events, or future alerting.
    """

    exit_code: int | None
    timed_out: bool
    duration: timedelta
    stdout: str
    stderr: str

    @property
    def succeeded(self) -> bool:
        return (
            not self.timed_out
            and self.exit_code == 0
        )


class JobExecutionService:
    """
    Executes a job's command as a real subprocess, with
    real timeout enforcement.

    A job with no command set (the current default for
    every job created through the public API -- see
    Job.command's docstring and ADR 0012) is treated as a
    no-op success: this lets the rest of the execution
    pipeline (timeout enforcement, result branching,
    worker state transitions) be exercised end-to-end
    without requiring every job to carry a real command
    yet.
    """

    def __init__(
        self,
        termination_grace_period: timedelta = DEFAULT_TERMINATION_GRACE_PERIOD,
    ) -> None:
        self._termination_grace_period = termination_grace_period

    def execute(
        self,
        command: list[str] | None,
        timeout: timedelta,
    ) -> JobExecutionResult:
        if command is None:
            return JobExecutionResult(
                exit_code=0,
                timed_out=False,
                duration=timedelta(seconds=0),
                stdout="",
                stderr="",
            )

        start = time.monotonic()

        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            try:
                stdout, stderr = process.communicate(
                    timeout=timeout.total_seconds(),
                )

                duration = timedelta(
                    seconds=time.monotonic() - start,
                )

                return JobExecutionResult(
                    exit_code=process.returncode,
                    timed_out=False,
                    duration=duration,
                    stdout=stdout,
                    stderr=stderr,
                )

            except subprocess.TimeoutExpired:
                return self._terminate_after_timeout(
                    process,
                    start,
                )

    def _terminate_after_timeout(
        self,
        process: subprocess.Popen,
        start: float,
    ) -> JobExecutionResult:
        """
        Escalate from a graceful SIGTERM to a forceful
        SIGKILL if the process doesn't exit within the
        grace period. This mirrors how real orchestrators
        (systemd, Kubernetes, Docker) handle shutdown: give
        the process a chance to clean up, then guarantee it
        actually stops.

        The final communicate() after kill() still carries a
        timeout. SIGKILL cannot be blocked or ignored by a
        well-behaved process on Linux, but a hung or
        zombie/defunct process is a real (if rare) failure
        mode worth bounding rather than trusting
        unconditionally.
        """
        process.terminate()

        try:
            stdout, stderr = process.communicate(
                timeout=self._termination_grace_period.total_seconds(),
            )
        except subprocess.TimeoutExpired:
            process.kill()

            try:
                stdout, stderr = process.communicate(
                    timeout=self._termination_grace_period.total_seconds(),
                )
            except subprocess.TimeoutExpired:
                stdout, stderr = "", ""

        duration = timedelta(
            seconds=time.monotonic() - start,
        )

        return JobExecutionResult(
            exit_code=process.returncode,
            timed_out=True,
            duration=duration,
            stdout=stdout,
            stderr=stderr,
        )
