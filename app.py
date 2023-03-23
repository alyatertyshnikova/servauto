import uvicorn
from fastapi import FastAPI

from models.models import TaskModel
from runner.engine import Engine

app = FastAPI()
engine = Engine()

task_id_counter = 0


@app.post("/run_task")
async def run_task(task: TaskModel) -> str:
    global task_id_counter
    task_id_counter = task_id_counter + 1
    engine.start_task(task_id_counter, task)
    return task_id_counter


@app.get("/status/{task_id}")
async def get_task_status(task_id: str) -> str:
    """
    Finds task by id and returns its status
    """
    try:
        task_status = engine.get_task_status(int(task_id))
    except Exception:
        return "Task not found"
    return task_status


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

