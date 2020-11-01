import unittest
from icondetection.weighted_quick_unionUF import WeightedQuickUnionUF as uf
import sandbox.box as b
import sandbox.rectangle as r


class TestSIFT(unittest.TestCase):
    def test_invalid_datatype(self):
        """
        No tests for sift yet
        """
        self.assertEqual(1, 1)


class TestUF(unittest.TestCase):
    """
    Simulating many of the tests from the Princeton Course.
    """

    def test_uf_ints(self):
        a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        t = uf(4, a[:4])
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

        u = uf(10, a)
        self.assertEqual(u.count, 10)
        u.union(0, 8)
        u.union(3, 5)
        u.union(4, 7)
        u.union(1, 9)
        self.assertEqual(u.count, 6)


class TestBox(unittest.TestCase):
    """
    Test the functionality in Box Sandbox
    """

    def test_same_intersect(self):
        """
        Tests that a rectangle overlaps with itself
        """
        a = r.Rectangle(2, 2, 8, 8)

        # the same rect should overlap
        self.assertTrue(r.Rectangle.intersect(a, a))

    def test_types_of_overlap(self):
        """
        Test different types of overlap
        """
        # top, left, bottom, right
        a = r.Rectangle(2, 2, 8, 8)
        c = r.Rectangle(4, 4, 8, 8)
        d = r.Rectangle(2, 2, 6, 6)
        e = r.Rectangle(2, 4, 8, 8)
        f = r.Rectangle(2, 2, 8, 6)

        # One rectangle overlapping with bottom right
        self.assertTrue(r.Rectangle.intersect(a, c))

        # Top left
        self.assertTrue(r.Rectangle.intersect(a, d))

        # Top right
        self.assertTrue(r.Rectangle.intersect(a, e))

        # Bottom left
        self.assertTrue(r.Rectangle.intersect(a, f))

    def test_types_of_none_overlap(self):
        """
        Test different types of non-overlap
        """
        # top, left, bottom, right
        a = r.Rectangle(2, 2, 8, 8)
        c = r.Rectangle(10, 10, 16, 16)
        d = r.Rectangle(2, 8, 8, 12)
        e = r.Rectangle(8, 2, 10, 8)
        f = r.Rectangle(8, 8, 16, 16)
        g = r.Rectangle(0, 0, 2, 2)

        self.assertFalse(r.Rectangle.intersect(a, c))
        self.assertFalse(r.Rectangle.intersect(a, d))
        self.assertFalse(r.Rectangle.intersect(a, e))
        self.assertFalse(r.Rectangle.intersect(a, f))
        self.assertFalse(r.Rectangle.intersect(a, g))


if __name__ == "__main__":
    unittest.main()
