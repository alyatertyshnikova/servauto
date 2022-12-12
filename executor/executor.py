# Позже здесь будет функциональность для запуска тасок на удаленных машинах
import subprocess
from typing import Tuple

from runner.task import Stage


class LocalExecutor:
    def run_stage(self, stage: Stage) -> Tuple[str, str, int]:
        """
        TODO: method should execute a command using subprocess module and return stdout, stderr and exit code
        """