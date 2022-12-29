from src.Entity.User import User
from src.Entity.Task import Task
from src.Entity.User.Worker import Worker
from src.Entity.Action.ComplainAction import ComplainAction
from src.Entity.Action.DispatchAction import DispatchAction

import redis
import json
import uuid
import os

from consolemenu import *
from consolemenu.items import *

class Manager:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=6)
        self.id = str(uuid.uuid4())
        self.name = "None"
        self.action_history = []

    def load(self):
        if self.name in self.redis.keys():
            data = json.loads(self.redis.get(self.name))
            self.id = data["id"]
            self.action_history = data["action_history"]

    def save(self):
        data = {
            "id": self.id,
            "action_history": self.action_history,
        }
        self.redis.set(self.name, json.dumps(data))


    def login(self):
        self.name = input("请输入用户名：")
        os.environ["NAME"] = self.name
        self.load()
        menu = ConsoleMenu("请选择要进行的操作")
        menu.append_item(FunctionItem("查看投诉信息", self.main, [1]))
        menu.show()

    def main(self, choice: int):
        if choice == 1:
            def reason(complain_id: str):
                complainAction = ComplainAction()
                complainAction.id = complain_id
                complainAction.load()
                explain = input("请输入投诉情况说明：")
                complainAction.explain = explain
                complainAction.status = 2
                complainAction.save()

            ComplainAction.get_menu_by_status(reason)