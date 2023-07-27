import time
import subprocess
from typing import Tuple, Optional
import threading

from models.status import Status
from concurrent.futures import Future, CancelledError

from paramiko.client import SSHClient

from runner.task import Stage


class LocalStageExecutor(threading.Thread):
    def __init__(self, stage: Stage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._process: Optional[subprocess.Popen] = None
        self._stage: Stage = stage
        self._future = Future()

    @property
    def status(self):
        return self._status

    def run(self) -> None:
        self._status = Status.RUNNING
        try:
            process = subprocess.Popen(self._stage.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                       text=True, encoding="cp866")
            self._process = process
            stdout, stderr = process.communicate()
            if self._future.cancelled():
                return

            self._future.set_result((stdout, stderr))
            if not stdout:
                self._stage.set_status(Status.FAILED)
            else:
                self._stage.set_status(Status.SUCCESS)
        except Exception as err:
            self._future.set_exception(err)
            self._stage.set_status(Status.FAILED)

    def get_result(self, timeout: Optional[float] = None) -> Optional[Tuple[str, str]]:
        try:
            return self._future.result(timeout)
        except (CancelledError, TimeoutError):
            return None

    def cancel(self):
        if self._process is not None:
            self._process.kill()
            self._future.cancel()
            self._stage.set_status(Status.ABORTED)
        else:
            raise ChildProcessError("Process is not created yet.")


class SshExecutor(threading.Thread):
    @staticmethod
    def run_stage(stage_command: str) -> Tuple[str, str]:
        with SSHClient() as client:
            client.load_system_host_keys()
            client.connect(hostname="127.0.0.1", port=22, username="username")

            _, stdout, stderr = client.exec_command(stage_command)
            return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")


if __name__ == '__main__':
    local_executor = LocalStageExecutor("ping localhost", threading.Semaphore(value=1))
    local_executor.start()
    # print(local_executor.get_result())
    print(local_executor.status)
    time.sleep(0.01)
    # local_executor.cancel()
    print(local_executor.get_result())
    # print(local_executor.status)
