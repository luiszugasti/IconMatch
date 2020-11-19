import argparse
import random as rng
import cv2 as cv

from icondetection.box import grayscale_blur, canny_detection, group_rects


def _handle_mouse(event, x: int, y: int, flags, params):
    """
    code partly inspired by that found here:
    https://divyanshushekhar.com/mouse-events-opencv/
    Left click to print the x, y coordinates.
    """
    text = ''
    font = cv.FONT_HERSHEY_COMPLEX
    color = (255, 0, 0)

    if event == cv.EVENT_LBUTTONDOWN:
        print("x coordinate:{}, y coordinate: {}".format(x, y))
        text = "x coordinate:{}, y coordinate: {}".format(x, y)

    cv.putText(src2, text, (x, y), font, 0.5, color, 1, cv.LINE_AA)


def _null_handler(event, x, y, flags, params):
    pass


def _render_rectangles(rectangles, input_image, display_text, callback):
    """
    Make sure to send a copy of your image with .copy()
    """

    # TODO: may not need to have specialized conversion from different rect
    #       types
    for index in range(len(rectangles)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(
            input_image,
            (int(rectangles[index][0]), int(rectangles[index][1])),
            (
                int(rectangles[index][0] + rectangles[index][2]),
                int(rectangles[index][1] + rectangles[index][3]),
            ),
            color,
            2,
        )

    cv.imshow(display_text, input_image)
    cv.setMouseCallback("Grouped Rectangles", callback)


# def _render_interactive_window():
#     def draw_rectangle_with_drag(event, x, y, flags, param):
#
#         global ix, iy, drawing, img
#
#         if event == cv.EVENT_LBUTTONDOWN:
#             drawing = True
#             ix = x
#             iy = y
#
#         elif event == cv.EVENT_MOUSEMOVE:
#             if drawing == True:
#                 cv.rectangle(img, pt1=(ix, iy),
#                              pt2=(x, y),
#                              color=(0, 255, 255),
#                              thickness=-1)
#
#         elif event == cv.EVENT_LBUTTONUP:
#             drawing = False
#             cv.rectangle(img, pt1=(ix, iy),
#                          pt2=(x, y),
#                          color=(0, 255, 255),
#                          thickness=-1)
#
#     cv.namedWindow(winname="Title of Popup Window")
#     cv.setMouseCallback("Title of Popup Window",
#                         draw_rectangle_with_drag)
#     while True:
#         cv.imshow("Title of popup window", src2)

def threshold_callback(val):
    """
    Takes a value of threshold for the canny edge detector and finds the
    bounding rectangles of appropriate edges within an image.
    """

    # accept an input image and convert it to grayscale, and blur it
    gray_scale_image = grayscale_blur(src)

    # determine the bounding rectangles from canny detection
    _, bound_rect = canny_detection(gray_scale_image, min_threshold=val)

    # group the rectangles from this step
    grouped_rects = group_rects(bound_rect, 0, src.shape[1])

    # (for display purposes) use the provided rectangles to display in your program
    _render_rectangles(grouped_rects, src.copy(), "Grouped Rectangles", _null_handler)
    _render_rectangles(bound_rect, src.copy(), "Original Rectangles", _null_handler)
    # _render_interactive_window()


if __name__ == "__main__":
    rng.seed(12345)
    parser = argparse.ArgumentParser(
        description="Sample showcase of IconDetection."
    )

    parser.add_argument("--input", help="Path to input image.")

    args = parser.parse_args()
    src = cv.imread(args.input)
    src2 = cv.imread(args.input)  # image for closest rectangle detection

    if src is None:
        print("Could not open or find the image:", args.input)
        exit(0)

    src_gray = grayscale_blur(src)

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
