from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException

from models.models import TaskModel
from runner.engine import Engine
from runner.task import TaskNotFound

app = FastAPI()
engine = Engine()

task_id_counter = 0


@app.post("/run_task")
async def run_task(task: TaskModel) -> str:
    try:
        global task_id_counter
        task_id_counter = task_id_counter + 1
        engine.start_task(task_id_counter, task)
        return str(task_id_counter)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Task {task} failed: {ex}")


@app.get("/status/{task_id}")
async def get_task_status(task_id: str) -> str:
    """
    Finds task by id and returns its status
    """
    try:
        task_status = engine.get_task_status(int(task_id))
        return task_status
    except TaskNotFound as ex:
        raise HTTPException(status_code=500, detail=f"Task {task_id} not found: {ex}")


@app.get("/result/{task_id}")
async def get_task_result(task_id: str) -> Union[dict[str, str], str]:
    """
    Find task by id and return its result
    """
    try:
        task_result = engine.get_task_result(int(task_id))
        return task_result
    except TaskNotFound as ex:
        raise HTTPException(status_code=500, detail=f"Task {task_id} not found: {ex}")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
