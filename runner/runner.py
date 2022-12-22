from runner.task import TaskManager
from executor.executor import LocalExecutor
from runner.status import Status


class Runner:
    def __init__(self, task_manager: TaskManager):
        self._task_manager = task_manager
        self._available_executors = [LocalExecutor()]

    def run(self):
        while self._task_manager.has_task:
            task = self._task_manager.next_task()
            executor = self._available_executors.pop()
            for stage in task.stages:  # add implementation in the task class
                stage.set_status(Status.RUNNING)
                stdout, stderr, exit_code = executor.run_stage(stage.command)
                # set status here. Exit code may help identify the issues.
                # set result here
                # break if there was an error
                if exit_code == 0:
                    stage.set_status(Status.SUCCESS)
                    stage.set_result(stdout)
                else:
                    stage.set_status(Status.FAILED)
                    stage.set_result(stderr)
                    break

            task.set_done()
            self._available_executors.append(executor)