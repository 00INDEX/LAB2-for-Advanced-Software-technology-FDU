from src.Entity.User import User
from src.Entity.Task import Task
from src.Entity.Action.ComplainAction import ComplainAction
from src.Entity.Action.ServiceAction import ServiceAction

import redis
import json
import os

from consolemenu import *
from consolemenu.items import *


class Worker:
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.id = 0
        self.name = "None"
        self.status = 0
        self.type = 0
        self.action_history = []

    def load(self):
        if self.name in self.redis.keys():
            data = json.loads(self.redis.get(self.name))
            self.id = data["id"]
            self.status = data["status"]
            self.type = data["type"]
            self.action_history = data["action_history"]
        else:
            self.save()

    def save(self):
        data = {
            "id": self.id,
            "status": self.status,
            "action_history": self.action_history,
            "type": self.type,
            "name": self.name
        }
        self.redis.set(self.name, json.dumps(data))

    def login(self):
        self.name = input("请输入用户名：")
        os.environ["NAME"] = self.name
        self.load()
        menu = ConsoleMenu("请选择要进行的操作")
        menu.append_item(FunctionItem("查看报修事务", self.main, [0]))
        menu.append_item(FunctionItem("查看投诉信息", self.main, [1]))
        menu.append_item(FunctionItem("查看完成的历史报修", self.main, [2]))
        menu.append_item(FunctionItem("查看工时统计", self.main, [3]))
        menu.show()

    def main(self, choice: int):
        if choice == 0:
            def task_menu(task_id):
                def service(task_id, finish):
                    serviceAction = ServiceAction()
                    serviceAction.create(task_id, finish)

                def cancel(task_id):
                    task = Task()
                    task.id = task_id
                    task.load()
                    task.status = 0
                    task.save()

                menu = ConsoleMenu("请选择要进行的操作")
                menu.append_item(FunctionItem("完成报修事务", service, [task_id, True]))
                menu.append_item(FunctionItem("延后报修事务", service, [task_id, False]))
                menu.append_item(FunctionItem("取消报修事务", cancel, [task_id]))
                menu.show()

            Task.get_menu_by_worker_name(self.name, task_menu)
        elif choice == 1:
            def reason(complain_id: str):
                complainAction = ComplainAction()
                complainAction.id = complain_id
                complainAction.load()
                reason = input("请输入投诉情况说明：")
                complainAction.reason.append({
                    "name": self.name,
                    "reason": reason
                })
                complainAction.save()

            ComplainAction.get_menu_by_name(self.name, reason)
        elif choice == 2:
            Task.get_menu_by_worker_name_and_status(self.name)
        elif choice == 3:
            print(f"您的总工时为：{ServiceAction.count_work_time(self.name)}")

    @classmethod
    def get_menu_by_status(cls, func):
        connection = redis.StrictRedis(host='localhost', port=6379, db=0)
        menu = ConsoleMenu("请选择维修人员")
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["status"] != 1:
                type = "水工"
                if data["type"] == 1:
                    type = "电工"
                elif data["type"] == 2:
                    type = "网络修理"
                menu.append_item(FunctionItem(f"姓名：{data['name']}||类型：{type}", func, [data["name"]]))
        menu.show()
