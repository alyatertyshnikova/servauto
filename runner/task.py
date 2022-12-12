from typing import List, Optional
from queue import SimpleQueue
import doctest

from status import Status


class Task:
    def __init__(self, *stages: "Stage"):
        self._stages: List[Stage] = list(stages)
        self._done: bool = False

    # TODO: Add steps property

    def set_done(self):
        self._done = True

    @property
    def done(self):
        return self._done


class Stage:
    """
    Abstract class for any kind of steps. Should store step command which will be executed.
    TODO: Make this class abstract with abstract property `command` and non-abs. property `status`
    """
    def __init__(self):
        self._status: Optional[Status] = None

    def command(self) -> str:
        """
        Returns a shell command that should be executed by Executor instance.
        """

    def set_status(self, status: Status) -> None:
        """
        TODO: add implementation
        """

    def set_result(self, result: str) -> None:
        """
        TODO: add implementation
        """


class CmdStage(Stage):
    """
    TODO: add implementation for the plane stage with cmd argument. A command will be presented as a shell command or bat.
    """


class GitStage(Stage):
    """
    TODO: add implementation. Main purpose of such stage is to checkout a specific branch for the specified repository.
    """


class TaskManager:
    def __init__(self):
        self._tasks = SimpleQueue()

    @property
    def has_task(self) -> bool:
        return not self._tasks.empty()

    def add_task(self, stages: List[dict]):
        """
        DOCTEST:
        >>> manager = TaskManager()
        >>> manager.add_task([{"name": "checkout", "git": {"repository": "url", "branch": "master"}}])

        TODO: add implementation
        """

    def next_task(self) -> Task:
        """
        TODO: add implementation. Do not forget to pop the item from the queue!
        """


if __name__ == '__main__':
    doctest.testmod()
