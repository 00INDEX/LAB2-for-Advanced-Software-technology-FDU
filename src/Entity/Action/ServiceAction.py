from src.Entity.Action.Action import Action
from src.Entity.Task import Task

from uuid import uuid4
import redis
import os
import json

from consolemenu import *
from consolemenu.items import *

class ServiceAction(Action):
    def __init__(self):
        self.id = str(uuid4())
        self.task_id = ""
        self.worker_name = ""
        self.work_time = 0
        self.status = 0
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=4)

    def load(self):
        if self.id.encode() in self.redis.keys():
            data = json.loads(self.redis.get(self.id.encode()))
            self.task_id = data["task_id"]
            self.status = data["status"]
            self.worker_name = data["worker_name"]
            self.work_time = data["work_time"]

    def save(self):
        data = {
            "worker_name": self.worker_name,
            "status": self.status,
            "work_time": self.work_time,
            "task_id": self.task_id
        }
        self.redis.set(self.id, json.dumps(data))

    def create(self, task_id: str, finish: bool):
        self.worker_name = os.environ["NAME"]
        self.task_id = task_id
        self.work_time = input("请输入本次工时：")
        task = Task()
        task.id = task_id
        task.load()
        if finish:
            task.status = 2
        task.action_history.append({
            "type": "service",
            "name": self.worker_name,
            "id": self.id
        })
        task.save()
        self.save()

    def finish(self):
        self.status = 1
        self.save()

    @classmethod
    def count_work_time(cls, worker_name):
        connection = redis.StrictRedis(host='localhost', port=6379, db=4)
        total = 0
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["worker_name"] == worker_name:
                total = total + int(data["work_time"])
        return total