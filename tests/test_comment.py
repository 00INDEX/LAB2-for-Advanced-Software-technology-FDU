import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_comment(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        sys.stdin = StringIO("1\nadmin\n2\n1\n1\ntest_comment\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["worker_name"] == "worker" and data["info"] == "test_apply_service":
                self.assertTrue(data["comment"] == "test_comment")


if __name__ == '__main__':
    unittest.main()
