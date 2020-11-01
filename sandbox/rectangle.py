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

    def __eq__(self, other) -> bool:
        if isinstance(other, Rectangle):
            return (
                self.top == other.top
                and self.left == other.left
                and self.right == other.right
                and self.bottom == other.bottom
            )
        return False
