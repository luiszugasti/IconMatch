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
        rectA.Left < rectB.Right
        and rectA.Right > rectB.Left
        and rectA.Top > rectB.Bottom
        and rectA.Bottom < rectB.Top
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
    new_rect.Top = rect[0]
    new_rect.Left = rect[1]
    new_rect.Bottom = rect[0] + rect[2]
    new_rect.Right = rect[1] + rect[3]
    return new_rect


def rec_list_to_dict(rects):
    """
    Takes a list of rects and returns their dictionary representation for
    simple filtering.
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
