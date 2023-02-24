# Позже здесь будет функциональность для запуска тасок на удаленных машинах
import abc
import subprocess
from typing import Tuple, Optional
import threading

from models.status import Status

from paramiko.client import SSHClient


class Executor(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def run_stage(stage_command: str) -> Tuple[str, str]:
        """
        Execute a command
        return stdout, stderr
        """
        pass


class LocalExecutor(threading.Thread, Executor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._process: Optional[subprocess.Popen] = None
        self._status: Status = Status.PENDING
        self._current_command = None
        self._stdout = None
        self._stderr = None

    def run(self) -> None:
        process = subprocess.Popen(self._current_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        self._status = Status.RUNNING
        self._process = process
        stdout, stderr = process.communicate()
        if stderr:
            self._status = Status.FAILED
        else:
            self._status = Status.SUCCESS
        self._stderr = stderr
        self._stdout = stdout

    def set_command(self, command: str):
        self._current_command = command

    def get_result(self) -> Tuple[str, str]:
        return self._stderr, self._stdout

    @property
    def status(self) -> Status:
        return self._status

    def stop_stage(self):
        self._process.kill()
        self._status = Status.FAILED


class SshExecutor(Executor):
    @staticmethod
    def run_stage(stage_command: str) -> Tuple[str, str]:
        with SSHClient() as client:
            client.load_system_host_keys()
            client.connect(hostname="127.0.0.1", port=22, username="username")

            _, stdout, stderr = client.exec_command(stage_command)
            return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

