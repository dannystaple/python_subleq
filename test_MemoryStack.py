from MemoryStack import MemoryStack

__author__ = 'stapled'

import unittest

class TestMemoryStack(unittest.TestCase):
    def test_PushOnePullOne(self):
        st = MemoryStack()
        st[0] = 5
        pulled = st[0]
        self.assertEqual(pulled, 5)

    def test_PushTwoPullTwo(self):
        st = MemoryStack()
        st[0] = 5
        st[0] = 7
        pulled = (st[0], st[0])
        self.assertEqual(pulled, (7, 5))

if __name__ == '__main__':
    unittest.main()
