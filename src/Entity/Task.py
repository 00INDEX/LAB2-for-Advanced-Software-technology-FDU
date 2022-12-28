import os

from src.Entity import Entity

from uuid import uuid4
import json
import redis
import datetime


from prettytable import PrettyTable

from consolemenu import *
from consolemenu.items import *


class Task:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=2)
        self.id = str(uuid4())
        self.info = ""
        self.apply_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.contact = ""
        self.type = 0
        self.status = 0
        self.client_name = ""
        self.worker_name = ""
        self.action_history = []
        self.comment = ""

    def load(self):
        if self.id.encode() in self.redis.keys():
            data = json.loads(self.redis.get(self.id.encode()))
            self.info = data["info"]
            self.status = data["status"]
            self.type = data["type"]
            self.action_history = data["action_history"]
            self.client_name = data["client_name"]
            self.worker_name = data["worker_name"]
            self.comment = data["comment"]
            self.apply_time = data["apply_time"]
            self.contact = data["contact"]

    def save(self):
        data = {
            "info": self.info,
            "status": self.status,
            "type": self.type,
            "action_history": self.action_history,
            "client_name": self.client_name,
            "worker_name": self.worker_name,
            "comment": self.comment,
            "apply_time": self.apply_time,
            "contact": self.contact
        }
        self.redis.set(self.id, json.dumps(data))

    def create(self):
        self.info = input("请输入报修详情：")
        self.contact = input("请输入您的联系方式：")
        self.client_name = os.environ["NAME"]
        self.save()
        print("创建报修信息成功")



    @classmethod
    def get_menu_by_client_name(cls, client_name, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        menu = ConsoleMenu("请选择报修事务")
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == client_name:
                status = "等待分配"
                if data["status"] == 1:
                    status = "正在检修"
                elif data["status"] == 2:
                    status = "已完成"
                menu.append_item(FunctionItem(f"申请客户：{data['client_name']}||情况描述：{data['info']}||"
                                              f"联系方式：{data['contact']}||创建时间：{data['apply_time']}||"
                                              f"状态：{status}", func, [key.decode()]))
        menu.show()

    @classmethod
    def get_menu_by_worker_name(cls, worker_name, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        menu = ConsoleMenu("请选择报修事务")
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["worker_name"] == worker_name and data["status"] == 1:
                status = "等待分配"
                if data["status"] == 1:
                    status = "等待检修"
                elif data["status"] == 2:
                    status = "已完成"
                menu.append_item(FunctionItem(f"申请客户：{data['client_name']}||情况描述：{data['info']}||"
                                              f"联系方式：{data['contact']}||创建时间：{data['apply_time']}||"
                                              f"状态：{status}", func, [key.decode()]))
        menu.show()

    @classmethod
    def get_menu_by_status(cls, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        menu = ConsoleMenu("请选择报修事务")
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["status"] != 2:
                status = "等待分配"
                if data["status"] == 1:
                    status = "正在检修"
                elif data["status"] == 2:
                    status = "已完成"
                menu.append_item(FunctionItem(f"申请客户：{data['client_name']}||情况描述：{data['info']}||"
                                              f"联系方式：{data['contact']}||创建时间：{data['apply_time']}||"
                                              f"状态：{status}", func, [key.decode()]))
        menu.show()

    @classmethod
    def add_action_history(cls, task_id, action):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        data = json.loads(connection.get(task_id))
        data["action_history"].append(action)
        connection.set(task_id, json.dumps(data))

    @classmethod
    def is_need_reason(cls, task_id, name):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        data = json.loads(connection.get(task_id))
        for action in data["action_history"]:
            if (action["type"] == "service" or action["type"] == "dispatch") and action["name"] == name:
                return True
        return False

    @classmethod
    def is_done(cls, task_id):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        data = json.loads(connection.get(task_id))
        return data["status"] == 2

    @classmethod
    def get_menu_by_worker_name_and_status(cls, worker_name):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        menu = ConsoleMenu("历史维修记录")
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["worker_name"] == worker_name and data["status"] == 2:
                status = "等待分配"
                if data["status"] == 1:
                    status = "等待检修"
                elif data["status"] == 2:
                    status = "已完成"
                menu.append_item(MenuItem(f"申请客户：{data['client_name']}||情况描述：{data['info']}||"
                                              f"联系方式：{data['contact']}||创建时间：{data['apply_time']}||"
                                              f"状态：{status}"))
        menu.show()

