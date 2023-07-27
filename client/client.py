import asyncio
import logging
from datetime import datetime
from datetime import timedelta
from typing import Dict

import aiohttp

from models.status import Status


class Client:
    def __init__(self):
        self._base_url: str = "http://server.servauto.com:8000"
        self._session = aiohttp.ClientSession()

    async def get_task_result(self, task_id: str) -> str:
        async with self._session.get(f"{self._base_url}/result/{task_id}") as response:
            task_result = await response.json()
            logging.info(f"Task {task_id} result: {task_result}")
            return task_result

    async def get_task_status(self, task_id: str) -> str:
        async with self._session.get(f"{self._base_url}/status/{task_id}") as response:
            task_status = await response.json()
            logging.info(f"Task {task_id} result: {task_status}")
            return task_status

    async def run_task(self, task: Dict[str, list]):
        async with self._session.post(f"{self._base_url}/run_task", json=task) as response:
            task_id = await response.json()
            logging.info("Task was created: ", task_id)
            return task_id

    async def close_session(self):
        await self._session.close()

    async def wait_for_task_is_done(self, task_id: str, timeout: timedelta):
        init_time = datetime.now()
        while (init_time + timeout) > datetime.now():
            status = await self.get_task_status(task_id)
            if status in [Status.FAILED.value, Status.SUCCESS.value]:
                break
            await asyncio.sleep(1)
