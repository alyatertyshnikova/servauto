"""
Data models
"""
from typing import List, Union

from pydantic import BaseModel


class CmdStageModel(BaseModel):
    name: str
    cmd: list[str]


class GitCheckoutCmdModel(BaseModel):
    repository: str
    branch: str


class GitStageModel(BaseModel):
    name: str
    git: GitCheckoutCmdModel


class TaskModel(BaseModel):
    stages: List[Union[CmdStageModel, GitStageModel]]
