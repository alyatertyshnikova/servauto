from typing import Dict

from models.models import TaskModel
from runner.runner import Runner
from runner.task import TaskManager


class Engine:
    def __init__(self):
        self._task_manager = TaskManager()
        self._runner = Runner(self._task_manager)
        self._runner.start()

    def start_task(self, task_id: str, task: TaskModel):
        self._task_manager.add_task(task_id, task.stages)

    def get_task_status(self, task_id: int) -> str:
        """
        Finds task by its id and collects its stages statuses into one
        """
        return self._task_manager.get_task_status(task_id)

    def get_task_result(self, task_id: int) -> Dict[str, str]:
        """
        Finds task by its id and ?
        """
        return self._task_manager.get_task_result(task_id)
