from models.models import TaskModel
from runner.runner import Runner
from runner.task import TaskManager


class Engine:
    def __init__(self):
        self._task_manager = TaskManager()
        self._runner = Runner(self._task_manager)

    def start(self, task_id: str, task: TaskModel):
        # temporary solution with loading local json file that contain the list of stages
        # with open(f"examples/{filename}") as fd:
        #     task = json.load(fd)
        self._task_manager.add_task(task_id, task.stages)
        self._runner.run()

    def get_task_status(self, task_id: str) -> str:
        """
        Finds task by its id and collects its stages statuses into one
        """
        task_status = ""
        task = self._task_manager.get_completed_task_by_id(task_id)
        for stage in task.stages:
            task_status += f"{stage.name}: {stage.status} \n"
        return task_status
