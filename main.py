import uuid

import uvicorn
from fastapi import FastAPI

from models.models import TaskModel
from runner.engine import Engine

app = FastAPI()
engine = Engine()


@app.post("/run_task")
def run_task(task: TaskModel) -> str:
    """
    Runs the task
    :param task:
    :return: task id
    """
    task_id = str(uuid.uuid1())
    engine.start(task_id, task)
    return task_id


@app.get("/status/{task_id}")
def get_task_status(task_id: str) -> str:
    """
    Finds task by id and returns its status
    :param task_id:
    :return:
    """
    task_status = engine.get_task_status(task_id)
    return task_status


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

