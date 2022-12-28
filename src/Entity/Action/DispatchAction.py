from src.Entity.Action.Action import Action
from src.Entity.Task import Task

from uuid import uuid4
import redis
import os
import json

from consolemenu import *
from consolemenu.items import *

class DispatchAction(Action):
    def __init__(self):
        self.id = str(uuid4())
        self.task_id = ""
        self.worker_name = ""
        self.dispatcher_name = ""
        self.status = 0
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=5)

    def load(self):
        if self.id.encode() in self.redis.keys():
            data = json.loads(self.redis.get(self.id.encode()))
            self.task_id = data["task_id"]
            self.status = data["status"]
            self.worker_name = data["worker_name"]
            self.dispatcher_name = data["dispatcher_name"]

    def save(self):
        data = {
            "worker_name": self.worker_name,
            "status": self.status,
            "dispatcher_name": self.dispatcher_name,
            "task_id": self.task_id
        }
        self.redis.set(self.id, json.dumps(data))

    def create(self, task_id: str, worker_name):
        self.dispatcher_name = os.environ["NAME"]
        self.task_id = task_id
        self.worker_name = worker_name
        task = Task()
        task.id = task_id
        task.load()
        task.worker_name = worker_name
        task.status = 1
        task.action_history.append({
            "type": "dispatch",
            "id": self.id,
            "name": self.dispatcher_name
        })
        task.save()
        self.save()

    def finish(self):
        self.status = 1
        self.save()