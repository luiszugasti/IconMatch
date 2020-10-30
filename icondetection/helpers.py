from PIL import Image
import numpy as np
import cv2


def runSIFT(img):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp = sift.detect(gray, None)

    cv2.drawKeypoints(image=gray, keypoints=kp, outImage=img)
    return img


def saveImg(img, name):
    if isinstance(img, Image.Image):
        img.save("{0}.png".format(name))
    else:
        cv2.imwrite("{0}.png".format(name), img)


def openImg(img_path):
    return cv2.imread(img_path)
