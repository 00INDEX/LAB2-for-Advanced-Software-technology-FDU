import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_reject_service(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        sys.stdin = StringIO("2\nworker\n1\n1\n3\n")
        import main
        res = False
        for key in connection.keys():
            data = json.loads(connection.get(key))
            if data["client_name"] == "admin" and data["info"] == "test_apply_service":
                self.assertTrue(data["status"] == 0)


if __name__ == '__main__':
    unittest.main()
