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
    def merge_rects(rects) -> dict:
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

