# Позже здесь будет функциональность для запуска тасок на удаленных машинах
import abc
import subprocess
from typing import Tuple

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


class LocalExecutor(Executor):
    @staticmethod
    def run_stage(stage_command: str) -> Tuple[str, str]:
        command_result = subprocess.run(stage_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                        text=True)
        return command_result.stdout, command_result.stderr


class SshExecutor(Executor):
    @staticmethod
    def run_stage(stage_command: str) -> Tuple[str, str]:
        with SSHClient() as client:
            client.load_system_host_keys()
            client.connect(hostname="127.0.0.1", port=22, username="username")

            _, stdout, stderr = client.exec_command(stage_command)
            return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

