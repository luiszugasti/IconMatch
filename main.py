from PIL import ImageGrab
from pynput import mouse
import numpy as np
import cv2

print("Choose the top left and bottom right coordinates of your box.")

button_presses = []

# Stream of events
with mouse.Events() as events:
    for event in events:
        if hasattr(event, "button") and event.pressed:
            print(
                "The {0} button was {1} at the following coordinates: x:{2}, y:{3}".format(
                    event.button,
                    "pressed" if event.pressed else "released",
                    event.x,
                    event.y,
                )
            )
            button_presses.append(event)
        if len(button_presses) == 2:
            break

im = ImageGrab.grab(
    bbox=(
        button_presses[0].x,
        button_presses[0].y,
        button_presses[1].x,
        button_presses[1].y,
    )
)
im.save("copy.png")

img = cv2.imread("copy.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
kp = sift.detect(gray, None)

imgb = cv2.drawKeypoints(image=gray, keypoints=kp, outImage=img, color=(255, 0, 0))

cv2.imwrite("sift_keypoints.png", img)
