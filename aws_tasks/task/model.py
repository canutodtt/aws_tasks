import logging
from typing import Optional

from botocore.exceptions import ClientError
from pydantic import BaseModel
from enum import Enum
import uuid


logger = logging.getLogger(__name__)

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(BaseModel):
    taskId: str = str(uuid.uuid4())
    title: str
    description: str
    status: Status

    class Config:
        use_enum_values = True

    @classmethod
    def get_task(cls, task_id: str, table) -> Optional['Task']:
        try:
            return Task(**table.get_item(Key={'taskId': task_id})["Item"])
        except ClientError as err:
            logger.error(
                "Couldn't get task with id %s. Here's why: %s: %s",
                task_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            return None
