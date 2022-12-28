from src.Entity.User import User
from src.Entity.Task import Task
from src.Entity.Action.ComplainAction import ComplainAction
from src.Entity.Action.CommentAction import CommentAction

import redis
import json
import uuid
import os

from consolemenu import *
from consolemenu.items import *

class Client:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=1)
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
        menu.append_item(FunctionItem("提交报修事务", self.main, [0]))
        menu.append_item(FunctionItem("查看报修事务", self.main, [1]))
        menu.append_item(FunctionItem("查看投诉事务", self.main, [2]))
        menu.show()

    def main(self, choice: int):
        if choice == 0:
            task = Task()
            task.create()
        elif choice == 1:
            def check_service(task_id: str):
                def complain(task_id: str):
                    complainAction = ComplainAction()
                    complainAction.create(task_id)
                def comment(task_id: str):
                    commentAction = CommentAction()
                    commentAction.create(task_id)
                menu = ConsoleMenu("请选择要进行的操作")
                if Task.is_done(task_id):
                    menu.append_item(FunctionItem("评价", comment, [task_id]))
                menu.append_item(FunctionItem("投诉", complain, [task_id]))
                menu.show()

            Task.get_menu_by_client_name(self.name, check_service)
        elif choice == 2:
            ComplainAction.get_menu_by_client_name(self.name)