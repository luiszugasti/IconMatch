import unittest
from icondetection.weighted_quick_unionUF import WeightedQuickUnionUF as uf

# from icondetection import helpers


class TestSIFT(unittest.TestCase):
    def test_invalid_datatype(self):
        """
        No tests... just set up the testing framework
        """
        self.assertEqual(1, 1)


class TestUF(unittest.TestCase):
    """
    Simulating many of the tests from the Princeton Course.
    """

    def test_uf_functionalities(self):
        t = uf(4)
        self.assertEqual(t.count, 4)
        t.union(0, 3)
        self.assertEqual(t.count, 3)
        t.union(3, 0)
        self.assertEqual(t.count, 3)
        t.union(2, 0)
        self.assertEqual(t.count, 2)
        t.union(1, 0)
        self.assertEqual(t.count, 1)
        self.assertTrue(t.connected(1, 0))

        u = uf(10)
        self.assertEqual(u.count, 10)
        u.union(0, 8)
        u.union(3, 5)
        u.union(4, 7)
        u.union(1, 9)
        self.assertEqual(u.count, 6)


if __name__ == "__main__":
    unittest.main()
