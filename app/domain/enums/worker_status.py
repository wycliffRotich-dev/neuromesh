from enum import StrEnum


class WorkerStatus(StrEnum):
    """
    Represents the lifecycle state of a worker.
    """

    STARTING = "STARTING"
    IDLE = "IDLE"
    BUSY = "BUSY"
    DRAINING = "DRAINING"
    OFFLINE = "OFFLINE"
