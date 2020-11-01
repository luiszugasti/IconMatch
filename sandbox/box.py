import cv2 as cv
import numpy as np
import argparse
import random as rng
import heapq
from icondetection.weighted_quick_unionUF import WeightedQuickUnionUF as uf
import sys
import sandbox.rectangle as r

rng.seed(12345)


def merge_rects(rects) -> dict:
    """
    Merges a list of rects into one conglomerate rect in "std".
    """

    # for now, just parse through the list, obtaining the smallest
    # value for top, left, and biggest value for bottom, right
    ans = r.Rectangle(sys.maxsize, sys.maxsize, 0, 0)

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
    new_rect = r.Rectangle(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    return new_rect


def std_rect_to_cv(rect):
    """
    Convert rectangle from Std representation back to CV representation
    """
    new_rect = (rect.top, rect.left, rect.bottom - rect.top, rect.right - rect.left)
    return new_rect


def rect_list_to_dict(rects):
    """
    Takes a list of cv rects and returns their dictionary representation for
    simple filtering.
    """
    rec_dict = {}
    rec_list = [None] * len(rects)
    for i in range(len(rects)):
        rect_mod = cv_rect_to_std(rect)
        rec_dict[rect_mod.left] = rect_mod
        rec_list[i] = rect_mod

    return (rec_dict, rect_mod)


def group_rects(cv_rects, min_x, max_x):
    """
    Accepts a list of rects. This list is converted to a dictionary in
    this format:
    left-coordinate: [
        {left, right, top, bottom},
        {left, right, top, bottom},
        .
        .
        .
        {left, right, top, bottom}
    ]
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
    rect_list, rect_dict = rect_list_to_dict(cv_rects)
    rect_heap = []
    unified_rects = uf(len(rect_list), rect_list)

    for x in range(min_x, max_x):
        # prune any outdated rects from the current_rects
        while True:
            if len(rect_heap) == 0:
                break
            if rect_heap[0][0] == x - 1:  # means we are at the edge
                heapq.heappop(rect_heap)
            else:
                break

        # get the potential list of rectangles along this axis
        temp_rects = cv_rects[x]
        # for each rect in the current_rects priority queue,
        # check each of these entries against each in temp_rects and perform
        # union if required
        # this is likely going to be a bottle neck
        for rectA in rect_heap:
            for rectB in temp_rects:
                if rect_overlap(rectA[1], rectB):
                    unified_rects.union(rectA[1], rectB)

            # add the rectB to the heap now.
            for rectB in temp_rects:
                heapq.heappush(rect_heap, (rectB.right, rectB))

    return unified_rects


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


if __name__ == "__main__":
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
    cv.createTrackbar(
        "Canny thresh:", source_window, thresh, max_thresh, thresh_callback
    )
    thresh_callback(thresh)
    cv.waitKey()
