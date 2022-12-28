from src.Entity.Action.Action import Action
from src.Entity.Task import Task

from uuid import uuid4
import redis
import os
import json

from consolemenu import *
from consolemenu.items import *

class CommentAction(Action):
    def __init__(self):
        self.id = str(uuid4())
        self.info = ""
        self.client_name = os.environ["NAME"]
        self.task_id = ""
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=7)

    def load(self):
        if self.id.encode() in self.redis.keys():
            data = json.loads(self.redis.get(self.id.encode()))
            self.info = data["info"]
            self.task_id = data["task_id"]
            self.client_name = data["client_name"]

    def save(self):
        data = {
            "info": self.info,
            "task_id": str(self.task_id),
            "client_name": self.client_name,
        }
        self.redis.set(self.id, json.dumps(data))

    def create(self, task_id: str):
        self.info = input("请输入评价：")
        self.task_id = task_id
        task = Task()
        task.id = task_id
        task.load()
        task.comment = self.info
        task.save()
        self.save()

    def finish(self):
        self.save()