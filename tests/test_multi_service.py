import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_multi_service(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        sys.stdin = StringIO("2\nworker\n1\n1\n2\n2\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["worker_name"] == "worker" and data["info"] == "test_apply_service":
                self.assertTrue(data["status"] == 1)
                for action in data["action_history"]:
                    if action["name"] == "worker":
                        res = True
                self.assertTrue(res)



if __name__ == '__main__':
    unittest.main()
