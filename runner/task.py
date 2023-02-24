import abc
import doctest
from queue import SimpleQueue
from typing import List, Optional, Union, Iterator

from models.models import GitStageModel, CmdStageModel
from models.status import Status


class Stage(abc.ABC):
    """
    Abstract class for any kind of steps. Should store step command which will be executed.
    """
    def __init__(self, name):
        self._name: str = name
        self._status: Optional[Status] = None
        self._result: Optional[str] = None

    @abc.abstractmethod
    def command(self) -> str:
        """
        Returns a shell command that should be executed by Executor instance.
        """
        pass

    @property
    def status(self) -> Optional[Status]:
        return self._status

    @property
    def name(self) -> Optional[str]:
        return self._name

    def set_status(self, status: Status) -> None:
        self._status = status

    def set_result(self, result: str) -> None:
        self._result = result


class CmdStage(Stage):
    """
    Class for shell commands
    """
    def __init__(self, name, commands):
        super().__init__(name)
        self._commands: List[str] = commands

    @property
    def command(self) -> str:
        return ' && '.join(self._commands)


class GitStage(Stage):
    """
    Class for git commands that checkout a specific branch for the specified repository.
    """
    def __init__(self, name, repository, branch):
        super().__init__(name)
        self._repository: str = repository
        self._branch: str = branch

    @property
    def command(self) -> str:
        return f"git clone {self._repository} && git checkout {self._branch}"


class Task:
    def __init__(self, id_: str, stages: List[Stage]):
        self._id: str = id_
        self._stages: List[Stage] = stages
        self._done: bool = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def stages(self):
        return self._stages

    def set_done(self):
        self._done = True

    @property
    def done(self):
        return self._done


class TaskManager:
    def __init__(self):
        self._tasks = SimpleQueue()
        self._completed_tasks: List[Task] = []

    def __iter__(self) -> Iterator[Task]:
        if not self._tasks.empty():
            yield self._tasks.get()

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, id_: str, stages: List[Union[GitStageModel, CmdStageModel]]):
        """
        DOCTEST:
        >>> manager = TaskManager()
        >>> manager.add_task([{"name": "checkout", "git": {"repository": "url", "branch": "master"}}])
        """
        task_stages = []
        for stage in stages:
            if isinstance(stage, GitStageModel):
                new_stage = GitStage(stage.name, stage.git.repository, stage.git.branch)
            else:
                new_stage = CmdStage(stage.name, stage.cmd)
            new_stage.set_status(Status.PENDING)
            task_stages.append(new_stage)
        task = Task(id_, task_stages)
        self._tasks.put(task)

    def complete_task(self, task: Task):
        """
        Adds task to the list of completed ones
        """
        self._completed_tasks.append(task)

    def get_completed_task_by_id(self, task_id: str) -> Task:
        """
        Finds task by its id and returns it
        """
        completed_task = next(task for task in self._completed_tasks if task.id == task_id)
        return completed_task


if __name__ == '__main__':
    doctest.testmod()
