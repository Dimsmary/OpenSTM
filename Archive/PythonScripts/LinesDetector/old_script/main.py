import cv2
import numpy as np
import os
from cvpackage import resize, to_gray, contrast_tune, gaussian_blur, canny_capture
from lineIterator import get_pixels, curve_plot, curve_fitting, curve_smooth, count_peaks

# FILE PATH HERE #
testPic = 'testsample.JPG'
picPath = 'image'
# FILE PATH HERE #

# PUBLIC PARAMETERS HERE #
brightness_param = 50
contrast_param = 50

window_len = 17
polynomial_order = 2

picture_size = 30

top_left_corner = [(0, 0)]
bottom_right_corner = [(1, 1)]
is_update = True
is_line_done = False
is_line_update = False


# PUBLIC PARAMETERS HERE #
def pictureSize(x):
    global picture_size, is_update
    picture_size = x
    is_update = True


def brightness(x):
    global brightness_param, is_update
    brightness_param = x
    is_update = True


def contrast(x):
    global contrast_param, is_update
    contrast_param = x
    is_update = True


def smooth_length(x):
    global window_len, is_line_update
    window_len = x


def smooth_order(x):
    global polynomial_order, is_line_update
    polynomial_order = x


def draw_rectangle(action, x, y, flags, *userdata):
    global top_left_corner, bottom_right_corner, is_update, is_line_done, is_line_update
    if action == cv2.EVENT_LBUTTONDOWN:
        if not is_line_done:
            top_left_corner = [(x, y)]
            is_line_done = True
        else:
            bottom_right_corner = [(x, y)]
            is_line_done = False
            is_line_update = True
            is_update = True


# main execute here
if __name__ == '__main__':


    # GUI Trackbars
    cv2.namedWindow('ControlPanel')
    cv2.createTrackbar('Pic Size', 'ControlPanel', 0, 100, pictureSize)
    cv2.setTrackbarPos('Pic Size', 'ControlPanel', picture_size)
    cv2.createTrackbar('Brightness', 'ControlPanel', -127, 127, brightness)
    cv2.setTrackbarPos('Brightness', 'ControlPanel', brightness_param)
    cv2.createTrackbar('Contrast', 'ControlPanel', -127, 127, contrast)
    cv2.setTrackbarPos('Contrast', 'ControlPanel', contrast_param)

    cv2.createTrackbar('Window Length', 'ControlPanel', 0, 51, smooth_length)
    cv2.setTrackbarPos('Window Length', 'ControlPanel', window_len)
    cv2.createTrackbar('Polynomial Order', 'ControlPanel', 0, 20, smooth_order)
    cv2.setTrackbarPos('Polynomial Order', 'ControlPanel', polynomial_order)

    # GUI Mouse Action
    cv2.namedWindow("image")
    cv2.setMouseCallback('image', draw_rectangle)

    # read path
    files = os.listdir('./' + picPath)

    # read picture
    index = 0
    image = cv2.imread('./' + picPath + '/' +files[index])

    # Gray
    image = to_gray(image)
    cropped_image = image[900:1700, 2500:4100]
    image = resize(cropped_image, picture_size)

    k = 0
    # loop
    while k != 27:

        if is_update:
            # resize the picture
            # image = resize(image, picture_size)

            # adjust contrast
            contrasted_img = contrast_tune(image, brightness_param, contrast_param)
            # canned_img = canny_capture(image, canny_low_param, canny_high_param)

            if is_line_update:
                # get value specified
                value = get_pixels(contrasted_img, top_left_corner, bottom_right_corner)
                yhat = curve_smooth(value, window_len, polynomial_order)
                peak_num = count_peaks(yhat)
                contrasted_img = cv2.putText(contrasted_img, peak_num, (50, 50), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)
                cv2.line(contrasted_img, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), thickness=2)
                is_line_update = False

            contrasted_img = cv2.putText(contrasted_img, files[index], (50, 100), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)
            cv2.imshow('image', contrasted_img)
            is_update = False

        k = cv2.waitKey(1)
        # update the curve manually
        # if pressed u
        if k == 117:
            is_line_update = True
            is_update = True

        # if pressed x
        elif k == 120:
            index += 1
            if index == len(files) - 1:
                index = 0
            image = cv2.imread('./' + picPath + '/' +files[index])
            image = to_gray(image)
            image = resize(image, picture_size)
            is_update = True

        elif k == 122:
            index -= 1
            if index == -1:
                index = len(files) - 1
            image = cv2.imread('./' + picPath + '/' +files[index])
            image = to_gray(image)
            image = resize(image, picture_size)
            is_update = True
