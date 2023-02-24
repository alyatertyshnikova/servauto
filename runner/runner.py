from runner.task import TaskManager
from executor.executor import SshExecutor, LocalExecutor
from models.status import Status
import queue


class Runner:
    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager
        self._available_executors = queue.SimpleQueue()
        self._available_executors.put(LocalExecutor())
        # self._available_executors = [SshExecutor()]

    def run(self):
        for task in self._task_manager:
            executor = self._available_executors.get(timeout=1)
            for stage in task.stages:
                stage.set_status(Status.RUNNING)
                executor.set_command(stage.command)
                executor.start()
                # stdout, stderr = executor.run_stage(stage.command)
                stage.set_status(executor.status)
                stage.set_result((stdout, stderr))

            task.set_done()
            self._task_manager.complete_task(task)
            self._available_executors.append(executor)
