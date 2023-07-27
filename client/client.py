import logging
from typing import Dict, List

import aiohttp


class Client:
    def __init__(self):
        self._ids: List[str] = []

    @property
    def ids(self) -> List[str]:
        return self._ids

    async def get_task_result(self, task_id: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/result/{task_id}") as response:
                task_result = await response.json()
                logging.info(f"Task {task_id} result: {task_result}")
                return task_result

    async def get_task_status(self, task_id: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/status/{task_id}") as response:
                task_status = await response.json()
                logging.info(f"Task {task_id} result: {task_status}")
                return task_status

    async def run_task(self, task: Dict[str, list]):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8000/run_task", json=task) as response:
                task_id = await response.json()
                logging.info("Task was created: ", task_id)
                self._ids.append(task_id)
                return task_id
