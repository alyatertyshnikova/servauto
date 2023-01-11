from runner.task import TaskManager
from executor.executor import LocalExecutor
from runner.status import Status


class Runner:
    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager
        self._available_executors = [LocalExecutor()]

    def run(self):
        for task in self._task_manager:
            executor = self._available_executors.pop()
            for stage in task.stages:
                stage.set_status(Status.RUNNING)
                stdout, stderr, exit_code = executor.run_stage(stage.command)
                if exit_code == 0:
                    stage.set_status(Status.SUCCESS)
                    stage.set_result(stdout)
                else:
                    stage.set_status(Status.FAILED)
                    stage.set_result(stderr)
                    break

            task.set_done()
            self._task_manager.complete_task(task)
            self._available_executors.append(executor)
