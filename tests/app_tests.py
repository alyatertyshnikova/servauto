import asyncio
import json

import pytest
import pytest_asyncio

from client.client import Client

JSON_LOAD_WITH_ERROR = {
    "stages": [
        {
            "name": "pytest",
            "cmd": ["pip install pytest"]
        },
        {
            "name": "error",
            "cmd": ["cd fghjfhl"]
        },
        {
            "name": "test",
            "cmd": ["curl 'https://parallel-ssh.readthedocs.io/en/latest/ssh_single.html'"]
        }
    ]
}

EXPECTED_RESPONSE_WITH_ERROR = ["pytest", "error"]

JSON_LOAD = {
    "stages": [{
        "name": "test",
        "cmd": ["curl 'https://parallel-ssh.readthedocs.io/en/latest/ssh_single.html'"]
    }
    ]
}

EXPECTED_RESPONSE = ["test"]


@pytest_asyncio.fixture(name="run_task_response")
async def run_task(request):
    client = Client()
    task_load = request.getfixturevalue("task")

    response = await client.run_task(task_load)

    yield client, response


@pytest.mark.asyncio
async def test_run_task():
    client = Client()
    response = await client.run_task(JSON_LOAD)
    assert type(response) == str


@pytest.mark.asyncio
@pytest.mark.parametrize("task, status, result",
                         [(JSON_LOAD, ["success", "pending"], EXPECTED_RESPONSE),
                          (JSON_LOAD_WITH_ERROR, ["failed", "pending"], EXPECTED_RESPONSE_WITH_ERROR)])
async def test_get_status_and_result(run_task_response, task, status, result):
    client, response = run_task_response
    await asyncio.sleep(5)

    task_result_json = await client.get_task_result(response)
    task_status = await client.get_task_status(response)

    task_result = json.loads(task_result_json)

    assert task_status in status
    assert list(task_result.keys()) == result

