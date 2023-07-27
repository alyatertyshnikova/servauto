import asyncio
import time

from client.client import Client

json_load = {
    "stages": [
        {
            "name": "error",
            "cmd": ["cd fghjfhl"]
        },
        {
            "name": "test",
            "cmd": ["curl 'https://parallel-ssh.readthedocs.io/en/latest/ssh_single.html'"]
        },
        {
            "name": "pytest",
            "cmd": ["pip install pytest"]
        }
    ]
}

client = Client()


async def main():
    tasks = []
    for _ in range(1, 4):
        tasks.append(asyncio.create_task(client.run_task(json_load)))

    await asyncio.gather(*tasks)
    for task in tasks:
        print(task)

    time.sleep(5)

    result_tasks = []
    for i in client.ids:
        result_tasks.append(asyncio.create_task(client.get_task_result(i)))

    await asyncio.gather(*result_tasks)
    for task in result_tasks:
        print(task.result())


asyncio.run(main())



