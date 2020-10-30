import cv2 as cv
import numpy as np
import argparse
import random as rng

rng.seed(12345)


# rect_overlap assumes that rect1 is to the left of rect2,
# and is in cv2 format:
#   | x, y
#   | where rect is defined by top left = (rect[0], rect[1])
#   |                          bottom right = (rect[0] + rect[2], rect[1] + rect[3]
def rect_overlap(rectA, rectB):
    """
    Determines if rectA, rectB are overlapping in cartesian space.
    Modified slightly from:
    https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other#306332
    """

    ret = (
        rectA.left < rectB.right
        and rectA.right > rectB.left
        and rectA.top > rectB.bottom
        and rectA.bottom < rectB.top
    )
    return ret


def merge_rects(rects):
    """
    Merges a list of rects into one conglomerate rect.
    """
    pass


def cv_rect_to_std(rect):
    """
    Convert rectangle from CV representation to something easier to work with
    Keep in mind that y increases from top to bottom!
    0 ----------------- x +
    |
    |
    |
    |
    |
    y +
    """
    new_rect = None
    new_rect.top = rect[0]
    new_rect.left = rect[1]
    new_rect.bottom = rect[0] + rect[2]
    new_rect.right = rect[1] + rect[3]
    return new_rect


def std_rect_to_cv(rect):
    """
    Convert rectangle from Std representation back to CV representation
    """
    new_rect = (rect.top, rect.left, rect.bottom - rect.top, rect.right - rect.left)
    return new_rect


def rect_list_to_dict(rects):
    """
    Takes a list of rects and returns their dictionary representation for
    simple filtering.
    """
    rec_dict = {}
    for rect in rects:
        rect_mod = cv_rect_to_std(rect)
        rec_dict[rect_mod.left] = rect_mod

    return rec_dict


def group_rects(rects, min_x, max_x):
    """
    Accepts a dictionary of rects in this format:
    left-coordinate: {left, right, top, bottom}
    And scans the complete (min_x, max_x) space to group rectangles.

    More technically, I am tackling the overlapping rectangle problem using a
    scanning line from min_x to min_max. This is why it's important for the rect
    dictionary to have keys as the left most coordinate of a rectangle; this
    makes lookups pretty easy depending on what level I'm scanning in.

    I am also maintaining a UnionFind structure of all the unique components.
    What UF allows me to do is to efficiently add rectangles to one component
    or to another, all the while maintaining the top left and bottom right
    coordinates of the conglomerate rectangle <<<TODO

    While scanning, I am maintaining a min heap of all rectangle's right most
    endpoints as key (since when the scanning index is greater than the right most
    endpoint, we are no longer in that rectangle) and the actual rectangle as an
    entry.

    The main objective here is, any time there is a new rectangle added to the
    mean heap, to iterate through the mean heap, checking if the rectangles
    overlap.
        | If they do: we perform a union() call on this rectangle pair.

    We then continue checking each rectangle pair and once we are done, we add
    the current rectangle to the min heap.

    The function itself will return the entries from UF, as they are (which
    later in the pipeline, will be converted back to how OpenCV expects them)
    """


def thresh_callback(val):
    """
    Function modified from this tutorial:
    https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
    Takes a value of threshold for the canny edge detector and finds the
    bounding rectangles of appropriate edges within an image.
    """
    threshold = val

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    _, contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None] * len(contours)
    radius = [None] * len(contours)

    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])

    drawing = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8
    )

    for i in range(len(contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(
            drawing,
            (int(boundRect[i][0]), int(boundRect[i][1])),
            (
                int(boundRect[i][0] + boundRect[i][2]),
                int(boundRect[i][1] + boundRect[i][3]),
            ),
            color,
            2,
        )

    cv.imshow("Contours", drawing)


parser = argparse.ArgumentParser(
    description="Code for Creating Bounding boxes and circles for contours tutorial."
)
parser.add_argument("--input", help="Path to input image.")
args = parser.parse_args()
src = cv.imread(args.input)
if src is None:
    print("Could not open or find the image:", args.input)
    exit(0)
# Convert image to gray and blur it
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3, 3))
source_window = "Source"
cv.namedWindow(source_window)
cv.imshow(source_window, src)
max_thresh = 255
thresh = 100  # initial threshold
cv.createTrackbar("Canny thresh:", source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)
cv.waitKey()
