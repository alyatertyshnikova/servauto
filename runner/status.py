import enum


class Status(enum.Enum):
    """ Represents possible task statuses """
    FAILED = "failed"
    SUCCESS = "success"
    RUNNING = "running"
    PENDING = "pending"
