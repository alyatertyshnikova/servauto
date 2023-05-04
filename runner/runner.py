from runner.task import TaskManager, Task
from executor.executor import LocalStageExecutor
from models.status import Status
import threading


class TaskExecutor(threading.Thread):
    def __init__(self, task: Task, semaphore: threading.Semaphore):
        super(TaskExecutor, self).__init__()
        self._task = task
        self._stop_event = threading.Event()
        self._semaphore = semaphore

    def run(self):
        for stage in self._task.stages:
            if self._stop_event.is_set():
                break
            executor = LocalStageExecutor(stage.command)
            stage.set_status(Status.RUNNING)
            executor.start()
            stage.set_result(executor.get_result())
            stage.set_status(executor.status)
            if stage.status is Status.FAILED:
                break

        self._task.set_done()
        self._semaphore.release()

    def stop(self):
        self._stop_event.set()
        self.join()


class Runner(threading.Thread):
    def __init__(self, task_manager: TaskManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._task_manager = task_manager
        self._semaphore = threading.Semaphore(value=2)
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            task = self._task_manager.get_task()
            if task is None:
                self._stop_event.wait(0.1)
            else:
                # self._semaphore.acquire()  # TODO blocking the execution
                task_executor = TaskExecutor(task, self._semaphore)
                task_executor.start()

    def stop(self):
        self._stop_event.set()
        self.join()
