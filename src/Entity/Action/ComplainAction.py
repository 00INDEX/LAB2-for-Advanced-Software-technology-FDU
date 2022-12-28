from src.Entity.Action.Action import Action
from src.Entity.Task import Task

from uuid import uuid4
import redis
import os
import json

from consolemenu import *
from consolemenu.items import *

class ComplainAction(Action):
    def __init__(self):
        self.id = str(uuid4())
        self.info = ""
        self.explain = ""
        self.reason = []
        self.client_name = os.environ["NAME"]
        self.task_id = ""
        self.status = 0
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=3)

    def load(self):
        if self.id.encode() in self.redis.keys():
            data = json.loads(self.redis.get(self.id.encode()))
            self.info = data["info"]
            self.status = data["status"]
            self.reason = data["reason"]
            self.task_id = data["task_id"]
            self.client_name = data["client_name"]
            self.explain = data["explain"]

    def save(self):
        data = {
            "info": self.info,
            "status": self.status,
            "reason": self.reason,
            "task_id": str(self.task_id),
            "client_name": self.client_name,
            "explain": self.explain
        }
        self.redis.set(self.id, json.dumps(data))

    def create(self, task_id: str):
        self.info = input("请输入投诉信息：")
        self.task_id = task_id
        self.save()

    def finish(self):
        self.explain = input("请输入投诉情况说明：")
        self.save()

    @classmethod
    def get_menu_by_client_name(cls, client_name):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        menu = ConsoleMenu()
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == client_name:
                status = "等待处理"
                if data["status"] == 1:
                    status = "正在处理"
                elif data["status"] == 2:
                    status = "已处理"
                reason = ','.join([f'{item["name"]}：{item["reason"]}' for item in data['reason']])
                menu.append_item(MenuItem(f"投诉内容：{data['info']}||工作人员回复：{reason}||物业经理回复：{data['explain']}||状态：{status}"))
        menu.show()

    @classmethod
    def get_menu_by_name(cls, name, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        menu = ConsoleMenu()
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if Task.is_need_reason(data["task_id"], name) and data["status"] == 0 and name not in [item['name'] for item in data["reason"]]:
                status = "等待处理"
                if data["status"] == 1:
                    status = "正在处理"
                elif data["status"] == 2:
                    status = "已处理"
                reason = ','.join([f'{item["name"]}：{item["reason"]}' for item in data['reason']])
                menu.append_item(
                    FunctionItem(f"投诉内容：{data['info']}||工作人员回复：{reason}||物业经理回复：{data['explain']}||状态：{status}", func, [key.decode()]))
        menu.show()

    @classmethod
    def get_menu_by_status(cls, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        menu = ConsoleMenu()
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["status"] == 0:
                status = "等待处理"
                if data["status"] == 1:
                    status = "正在处理"
                elif data["status"] == 2:
                    status = "已处理"
                reason = ','.join([f'{item["name"]}：{item["reason"]}' for item in data['reason']])
                menu.append_item(
                    FunctionItem(
                        f"投诉内容：{data['info']}||工作人员回复：{reason}||物业经理回复：{data['explain']}||状态：{status}", func,
                        [key.decode()]))
        menu.show()