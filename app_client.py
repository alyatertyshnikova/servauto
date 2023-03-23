import requests
import time

import aiohttp
import asyncio


def get_result(task_id: str):
    print(requests.get(f"http://localhost:8000/status/{task_id}").text)


ids = []


async def run_task(session: aiohttp.ClientSession):
    json_load = {
        "stages": [
                {
                    "name": "test",
                    "cmd": ["curl 'https://parallel-ssh.readthedocs.io/en/latest/ssh_single.html'"]
                }
            ]
        }
    async with session.post("http://localhost:8000/run_task", json=json_load) as response:
        response_json = await response.json()
        print("Task was created: ", response_json)
        ids.append(int(response_json))
        return int(response_json)


async def main():

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(1, 4):
            tasks.append(asyncio.create_task(run_task(session)))

        await asyncio.gather(*tasks)
        for task in tasks:
            print(task)


asyncio.run(main())

time.sleep(5)

for i in ids:
    get_result(i)
