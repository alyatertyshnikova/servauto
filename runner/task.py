import abc
import doctest
import json
import logging
from queue import Queue
from typing import List, Optional, Union

from models.models import GitStageModel, CmdStageModel
from models.status import Status

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


class Stage(abc.ABC):
    """
    Abstract class for any kind of steps. Should store step command which will be executed.
    """

    def __init__(self, name):
        self._name: str = name
        self._status: Status = Status.PENDING
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
    def result(self) -> Optional[Status]:
        return self._result

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

    def __str__(self):
        return f"Task({self._id})"


class TaskNotFound(Exception):
    pass


class TaskManager:
    def __init__(self):
        self._tasks = Queue()
        self._future_tasks = Queue()

    def get_task(self) -> Optional[Task]:
        if not self._tasks.empty():
            task = self._tasks.get()
            self._future_tasks.put(task)
            return task
        return

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, id_: str, stages: List[Union[GitStageModel, CmdStageModel]]) -> None:
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
            task_stages.append(new_stage)
        task = Task(id_, task_stages)
        logger.debug("task was created: %s", task)
        self._tasks.put(task)

    def get_task_status(self, task_id: int) -> str:
        """
        Finds task by its id and returns its status
        """
        if any(task_id == task.id for task in self._tasks.queue):
            return Status.NOT_STARTED.value
        # for i in range(self._tasks.qsize()):
        #     task = self._tasks.queue[i]
        #     if task.id == task_id:
        #         return Status.NOT_STARTED.value

        for i in range(self._future_tasks.qsize()):
            task = self._future_tasks.queue[i]
            if task.id == task_id:
                any_stage_failure = any(stage.status == Status.FAILED for stage in task.stages)
                return Status.FAILED.value if any_stage_failure else task.stages[-1].status.value
        else:
            raise TaskNotFound(task_id)

    def get_task_result(self, task_id: int) -> str:
        task_results = {}
        for i in range(self._future_tasks.qsize()):
            task = self._future_tasks.queue[i]
            if task.id == task_id:
                for stage in task.stages:
                    task_results[stage.name] = stage.result
                    if stage.status is Status.FAILED:
                        break
                return json.dumps(task_results)
        else:
            raise TaskNotFound(task_id)


if __name__ == '__main__':
    doctest.testmod()
