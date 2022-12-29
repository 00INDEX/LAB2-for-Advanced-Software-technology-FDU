import unittest


import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_dispatcher_answer_complain(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        sys.stdin = StringIO("3\ndispatcher\n2\n1\ntest_dispatcher_answer_complain\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == "admin" and data["info"] == "test_complain":
                for reason in data["reason"]:
                    if reason["name"] == "dispatcher":
                        self.assertTrue(reason["reason"] == "test_dispatcher_answer_complain")


if __name__ == '__main__':
    unittest.main()
