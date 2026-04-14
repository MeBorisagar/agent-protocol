import redis
import json
from protocol.schemas.task import TaskStatus

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class TaskStore:

    def create_task(self, task_id: str):
        r.set(task_id, json.dumps({
            "task_id": task_id,
            "status": TaskStatus.PENDING
        }))

    def update_status(self, task_id: str, status: TaskStatus):
        task = json.loads(r.get(task_id))
        task["status"] = status
        r.set(task_id, json.dumps(task))

    def complete_task(self, task_id: str, result: dict):
        task = json.loads(r.get(task_id))
        task["status"] = TaskStatus.COMPLETED
        task["result"] = result
        r.set(task_id, json.dumps(task))

    def fail_task(self, task_id: str, error: str):
        task = json.loads(r.get(task_id))
        task["status"] = TaskStatus.FAILED
        task["error"] = error
        r.set(task_id, json.dumps(task))

    def get_task(self, task_id: str):
        data = r.get(task_id)
        return json.loads(data) if data else None