import cv2 as cv
import numpy as np
import argparse
import random as rng
import heapq
from icondetection.weighted_quick_unionUF import WeightedQuickUnionUF as uf
from icondetection.rectangle import Rectangle

rng.seed(12345)


def rect_list_to_dict(rects):
    """
    Takes a list of cv rects and returns their dictionary representation for
    simple filtering.
    """
    # POTENTIALLY PROBLEMATIC: necessarily has to be a list of (index, rects)
    rect_dict = {}
    rect_list = [None] * len(rects)

    for rect_index in range(len(rects)):
        temp_rect = Rectangle.rect_cv_to_cartesian(rects[rect_index])

        # step to modify dictionary
        if temp_rect.left in rect_dict:
            tmp_list = rect_dict[temp_rect.left]
            tmp_list.append((rect_index, temp_rect))
            rect_dict[temp_rect.left] = tmp_list
        else:
            rect_dict[temp_rect.left] = [(rect_index, temp_rect)]

        # step to modify list
        rect_list[rect_index] = temp_rect

    return (rect_dict, rect_list)


def group_rects(cv_rects, min_x, max_x):
    """
    Accepts a list of rects in openCV format, and groups them according to their
    overlapping locations.
    """

    rect_dict, rect_list = rect_list_to_dict(cv_rects)
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

        # get rectangles in this index
        if x in rect_dict:
            temp_rects = rect_dict[x]
        else:
            continue

        # perform intersection
        for rectA in rect_heap:
            for rectB in temp_rects:
                if Rectangle.intersect(rectA[1], rectB[1]):
                    unified_rects.union(rectA[2], rectB[0])

        # push new elements onto heap
        for rectB in temp_rects:
            heapq.heappush(rect_heap, (rectB[1].right, rectB[1], rectB[0]))

    # perform groupings
    grouped_rects = []
    unions = unified_rects.get_unions()
    for group in unions.values():
        grouped_rects.append(
            Rectangle.rect_cartesian_to_cv(Rectangle.merge_rects(group))
        )

    return grouped_rects


def threshold_callback(val):
    """
    Function modified from this tutorial:
    https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
    Takes a value of threshold for the canny edge detector and finds the
    bounding rectangles of appropriate edges within an image.
    """
    multiplier = 2
    contour_accuracy = 3
    min_threshold = val
    max_threshold = int(min_threshold * multiplier)
    src = cv.imread(args.input)
    src2 = src.copy()

    canny_output = cv.Canny(src_gray, min_threshold, max_threshold)

    _, contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None] * len(contours)
    radius = [None] * len(contours)

    for index, contour in enumerate(contours):
        contours_poly[index] = cv.approxPolyDP(contour, contour_accuracy, True)
        boundRect[index] = cv.boundingRect(contours_poly[index])
        centers[index], radius[index] = cv.minEnclosingCircle(contours_poly[index])

    drawing_all_rects = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8
    )

    drawing_grouped_rects = np.zeros(
        (canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8
    )

    grouped_rects = group_rects(boundRect, 0, src.shape[1])

    for index in range(len(boundRect)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(
            src,
            (int(boundRect[index][0]), int(boundRect[index][1])),
            (
                int(boundRect[index][0] + boundRect[index][2]),
                int(boundRect[index][1] + boundRect[index][3]),
            ),
            color,
            2,
        )

    # TODO: may not need to have specialized conversion from different rect
    #       types
    for index in range(len(grouped_rects)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(
            src2,
            (int(grouped_rects[index][0]), int(grouped_rects[index][1])),
            (
                int(grouped_rects[index][0] + grouped_rects[index][2]),
                int(grouped_rects[index][1] + grouped_rects[index][3]),
            ),
            color,
            2,
        )

    cv.imshow("Contours", src)
    cv.imshow("Groupings", src2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Code for Creating Bounding boxes using Canny Edge Detector."
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
        "Canny threshold:", source_window, thresh, max_thresh, threshold_callback
    )
    threshold_callback(thresh)
    cv.waitKey()