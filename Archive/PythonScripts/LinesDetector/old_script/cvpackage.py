import cv2
import numpy as np

def resize(img, percentage):
    width = int(img.shape[1] * percentage / 100)
    height = int(img.shape[0] * percentage / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def contrast_tune(img, bright, cont):
    con = np.int16(img)
    con = cont * (con / 127 + 1) - cont + bright
    con = np.clip(con, 0, 255)
    return np.uint8(con)


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def canny_capture(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)