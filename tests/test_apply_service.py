import unittest

import sys
from io import StringIO
import redis
import json


class MyTestCase(unittest.TestCase):
    def test_apply_service(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        sys.stdin = StringIO("1\nadmin\n1\ntest_apply_service\n158xxxxxxxx\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            res = data["info"] == "test_apply_service"
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
