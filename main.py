import json

from runner.runner import Runner
from runner.task import TaskManager


class Engine:
    def __init__(self):
        self._task_manager = TaskManager()
        self._runner = Runner(self._task_manager)

    def start(self):
        # temporary solution with loading local json file that contain the list of stages
        with open("examples/run_task.json") as fd:
            task = json.load(fd)
            self._task_manager.add_task(task["stages"])
        self._runner.run()