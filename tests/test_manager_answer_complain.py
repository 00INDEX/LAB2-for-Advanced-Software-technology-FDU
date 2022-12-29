import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_manager_answer_complain(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        sys.stdin = StringIO("4\nmanager\n1\n1\ntest_manager_answer_complain\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == "admin" and data["info"] == "test_complain":
                self.assertTrue(data["explain"] == "test_manager_answer_complain")



if __name__ == '__main__':
    unittest.main()
