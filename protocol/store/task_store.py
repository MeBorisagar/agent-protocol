from typing import Dict
from protocol.schemas.task import Task, TaskStatus


class TaskStore:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def create_task(self, task_id: str):
        self.tasks[task_id] = Task(
            task_id=task_id,
            status=TaskStatus.PENDING
        )

    def update_status(self, task_id: str, status: TaskStatus):
       
        self.tasks[task_id].status = status

    def complete_task(self, task_id: str, result: dict):
        
        self.tasks[task_id].status = TaskStatus.COMPLETED
        self.tasks[task_id].result = result

    def fail_task(self, task_id: str, error: str):
       
        self.tasks[task_id].status = TaskStatus.FAILED
        self.tasks[task_id].error = error

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)