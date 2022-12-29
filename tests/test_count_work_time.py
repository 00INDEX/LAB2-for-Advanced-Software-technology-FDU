import unittest

import sys
from io import StringIO
import redis
import json

class MyTestCase(unittest.TestCase):
    def test_count_work_time(self):
        connection = redis.StrictRedis(host='localhost', port=6379, db=2)
        sys.stdin = StringIO("2\nworker\n4\n")
        sys.stdout = custom_stdout = StringIO()
        import main
        self.assertTrue('15' in custom_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
