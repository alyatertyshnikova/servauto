# Позже здесь будет функциональность для запуска тасок на удаленных машинах
import subprocess
from typing import Tuple

from runner.task import Stage


class LocalExecutor:
    @staticmethod
    def run_stage(stage_command: str) -> Tuple[str, str, int]:
        """
        Execute a command
        return stdout, stderr and exit code
        """
        command_result = subprocess.run(stage_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return command_result.stdout, command_result.stderr, command_result.returncode