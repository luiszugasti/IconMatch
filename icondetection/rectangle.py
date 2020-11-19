import sys


class Rectangle:
    def __init__(self, top, left, bottom, right):
        """
        Create a rectangle in "std" notation
        """
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    @staticmethod
    def intersect(rectA, rectB) -> bool:
        """
        Determines if rectA, rectB, intersect.
        Modified slightly from:
        https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other#306332
        """

        ret = (
                rectA.left < rectB.right
                and rectA.right > rectB.left
                and rectA.top < rectB.bottom
                and rectA.bottom > rectB.top
        )
        return ret

    @staticmethod
    def merge_rects(rects):
        """
        Merges a list of rects into one conglomerate rect in "std".
        """

        ans = Rectangle(sys.maxsize, sys.maxsize, 0, 0)

        for rect in rects:
            if rect.left < ans.left:
                ans.left = rect.left
            if rect.top < ans.top:
                ans.top = rect.top
            if rect.bottom > ans.bottom:
                ans.bottom = rect.bottom
            if rect.right > ans.right:
                ans.right = rect.right

        return ans

    @staticmethod
    def rect_cv_to_cartesian(rect):
        """
        Converts a rectangle from CV representation to cartesian coordinates.
        Note: Keep in mind that y increases from top to bottom!
                            0 - x +
                            |
                            y
                            +
        Where top, bottom, left and right are named relative to cartesian coordinates. Basically, the below
        diagram shows what they mean.
                               Top
                            --------
                            |      |
                       Left |      | Right
                            |      |
                            --------
                             Bottom
        """
        new_rect = Rectangle(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
        return new_rect

    @staticmethod
    def rect_cartesian_to_cv(rect):
        """
        Convert rectangle from Std representation back to CV representation
        """
        new_rect = (rect.top, rect.left, rect.bottom - rect.top, rect.right - rect.left)
        return new_rect

    def __eq__(self, other) -> bool:
        if isinstance(other, Rectangle):
            return (
                    self.top == other.top
                    and self.left == other.left
                    and self.right == other.right
                    and self.bottom == other.bottom
            )
        return False

    # Not an absolute comparison.
    def __lt__(self, other) -> bool:
        if self.get_area() > other.get_area():
            return True
        return False

    def get_area(self):
        if not hasattr(self, "area"):
            self.area = (self.right - self.left) * (self.bottom - self.top)
        return self.area

    def contains_point(self, point) -> bool:
        # for now: x is point[0], y is point[1]
        if self.right > point[0] > self.left and self.bottom > point[1] > self.top:
            return True
        return False

    def distance_to_point(self, point: tuple) -> int:
        # brute force: determine squared Euclidean distance from each corner to the point and return the lowest value.

        def euclidean_distance(point1: tuple, point2: tuple) -> int:
            # for now: x is point[0], y is point[1]
            return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2

        dist_top_left = euclidean_distance(point, (self.top, self.left))
        dist_top_right = euclidean_distance(point, (self.top, self.right))
        dist_bottom_left = euclidean_distance(point, (self.bottom, self.left))
        dist_bottom_right = euclidean_distance(point, (self.bottom, self.right))

        return max(dist_top_left, dist_top_right, dist_bottom_left, dist_bottom_right)
