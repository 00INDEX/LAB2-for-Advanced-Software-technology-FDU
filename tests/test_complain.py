import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_complain(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=3)
        sys.stdin = StringIO("1\nadmin\n2\n1\n2\ntest_complain\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == "admin":
                self.assertTrue(data["info"] == "test_complain")


if __name__ == '__main__':
    unittest.main()
