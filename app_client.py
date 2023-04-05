import asyncio
import time

from client.client import Client

json_load = {
    "stages": [
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


asyncio.run(main())

time.sleep(5)

for i in client.ids:
    asyncio.run(client.get_task_result(i))
