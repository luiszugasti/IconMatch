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
    Test the base methods of Union Find.
    """

    def setUp(self):
        self.a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.t = uf(4, self.a[:4])
        self.u = uf(10, self.a)

    def test_count(self):
        self.assertEqual(self.t.count, 4)
        self.t.union(0, 3)

        self.assertEqual(self.t.count, 3)
        self.t.union(3, 0)

        self.assertEqual(self.t.count, 3)
        self.t.union(2, 0)

        self.assertEqual(self.t.count, 2)
        self.t.union(1, 0)

        self.assertEqual(self.t.count, 1)
        self.assertTrue(self.t.connected(1, 0))

        self.assertEqual(self.u.count, 10)

        self.u.union(0, 8)
        self.u.union(3, 5)
        self.u.union(4, 7)
        self.u.union(1, 9)
        self.assertEqual(self.u.count, 6)

    def test_find(self):
        # p, q << all things equal, p will be picked
        self.t.union(0, 3)
        self.assertEqual(self.t.find(3), 0, "Parent should be 0")

        self.t.union(3, 0)
        self.assertEqual(self.t.find(3), 0, "No change is expected")
        self.assertEqual(self.t.size[0], 2, "Parent 0 should have 2 components")

        self.t.union(2, 0)
        self.assertEqual(self.t.size[0], 3, "Parent 0 should have 3 components")

        self.t.union(1, 0)
        self.assertEqual(self.t.size[0], 4, "Parent 0 should have 4 components")

    def test_get_unions(self):
        self.u.union(0, 9)
        self.u.union(1, 8)
        self.u.union(2, 7)
        self.u.union(3, 6)
        self.u.union(4, 5)

        unions_u = self.u.get_unions()
        self.assertCountEqual([0, 1, 2, 3, 4], unions_u.keys())

        self.t.union(0, 3)
        self.t.union(2, 0)
        self.t.union(1, 0)
        unions_t = self.t.get_unions()
        self.assertCountEqual([0], unions_t.keys())


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

    def test_types_of_non_overlap(self):
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

    def test_conglomeration(self):
        """
        Test that the complete bounding rectangle is returned.
        """
        # top, left, bottom, right
        a = r.Rectangle(2, 2, 8, 8)
        c = r.Rectangle(4, 4, 8, 8)
        d = r.Rectangle(2, 2, 6, 6)
        e = r.Rectangle(2, 4, 8, 8)
        f = r.Rectangle(2, 2, 8, 6)

        g = r.Rectangle(2, 2, 16, 16)
        h = r.Rectangle(15, 15, 16, 16)

        self.assertEqual(a, b.merge_rects([a, c, d, e, f]))

        self.assertEqual(g, b.merge_rects([a, h]))

        # delete it
        me = uf(1, [a])
        print(me)


if __name__ == "__main__":
    unittest.main()
