import abc
import doctest
from queue import SimpleQueue
from typing import List, Optional

from runner.status import Status


class Task:
    def __init__(self, stages: list):
        self._stages: List[Stage] = stages
        self._done: bool = False

    @property
    def stages(self):
        return self._stages

    def set_done(self):
        self._done = True

    @property
    def done(self):
        return self._done


class Stage(abc.ABC):
    """
    Abstract class for any kind of steps. Should store step command which will be executed.
    """
    def __init__(self):
        self._status: Optional[Status] = None
        self._result: Optional[str] = None

    @abc.abstractmethod
    def command(self) -> str:
        """
        Returns a shell command that should be executed by Executor instance.
        """
        pass

    def set_status(self, status: Status) -> None:
        self._status = status

    def set_result(self, result: str) -> None:
        self._result = result


class CmdStage(Stage):
    """
    Class for shell commands
    """
    def __init__(self, name, commands):
        super().__init__()
        self._name: str = name
        self._commands: list[str] = commands

    @property
    def command(self) -> str:
        return ' && '.join(self._commands)


class GitStage(Stage):
    """
    Class for git commands that checkout a specific branch for the specified repository.
    """
    def __init__(self, name, repository, branch):
        super().__init__()
        self._name: str = name
        self._repository: str = repository
        self._branch: str = branch

    @property
    def command(self) -> str:
        return f"git clone {self._repository} && git checkout {self._branch}"


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
        """
        task_stages = []
        for stage in stages:
            if stage.get("git") is not None:
                new_stage = GitStage(stage["name"], stage["git"]["repository"], stage["git"]["branch"])
            else:
                new_stage = CmdStage(stage["name"], stage["cmd"])
            new_stage.set_status(Status.PENDING)
            task_stages.append(new_stage)
        task = Task(task_stages)
        self._tasks.put(task)

    def next_task(self) -> Task:
        return self._tasks.get()


if __name__ == '__main__':
    doctest.testmod()
