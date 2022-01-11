import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# WORK FLOW
# 1: Judge the mode
# 2: Load the original image & stack font on the image
# 3: wait for update
# 4: if calculate point has been specified, then update peak message, and set peak flag to 1
# 5: if any opencv callback function triggered, set update flag to 1


# Line detector class
class LineDetector:

    def __init__(self, path, method, camera=0):

        # read camera or from the path
        self.method = method
        if method == 0:
            self.camera = cv2.VideoCapture(camera)
            _, self.original_image = self.camera.read()
        else:
            # read the path
            self.files = os.listdir('./' + path)
            self.path = path
            self.path_check()
            self.index = 0
            self.original_image = cv2.imread('./' + self.path + '/' + self.files[self.index])

        # opencv param
        self.brightness = 50
        self.contrast = 50
        self.picture_resize = 30
        self.top_left_corner = []
        self.bottom_right_corner = []
        self.is_point_out = False

        # smooth param
        self.window_len = 17
        self.polynomial_order = 2
        self.peak_num = 0

        # status indicate
        self.frame_update = False
        self.peak_count_update = False

        # initialize opencv
        self.cv2_init()

    def cv2_init(self):

        # create windows
        cv2.namedWindow('ControlPanel')
        cv2.namedWindow("Image")

        # Create the control panel attach to control window
        cv2.createTrackbar('Pic Size', 'ControlPanel', 0, 100, self.cv2_callback_picture_crop)
        cv2.setTrackbarPos('Pic Size', 'ControlPanel', self.picture_resize)
        cv2.createTrackbar('Brightness', 'ControlPanel', -127, 127, self.cv2_callback_brightness)
        cv2.setTrackbarPos('Brightness', 'ControlPanel', self.brightness)
        cv2.createTrackbar('Contrast', 'ControlPanel', -127, 127, self.cv2_callback_contrast)
        cv2.setTrackbarPos('Contrast', 'ControlPanel', self.contrast)

        cv2.createTrackbar('Window Length', 'ControlPanel', 0, 51, self.cv2_callback_window_length)
        cv2.setTrackbarPos('Window Length', 'ControlPanel', self.window_len)
        cv2.createTrackbar('Polynomial Order', 'ControlPanel', 0, 20, self.cv2_callback_polynomial_order)
        cv2.setTrackbarPos('Polynomial Order', 'ControlPanel', self.polynomial_order)

        # set Mouse action callback
        cv2.setMouseCallback('Image', self.cv2_callback_mouse)

        # display image
        self.cv2_read_image()

    def cv2_read_image(self, is_show=True):
        # read the image, crop and to gray
        # if it is in camera mode
        if self.method == 0:
            cropped_image = self.original_image
        else:
            cropped_image = self.original_image[900:1800, 2500:4100]

        # resize the image
        resized_image = self.cv2_resize(cropped_image, self.picture_resize)

        # to gray
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # contrast tune
        contrasted = self.cv2_contrast(gray_image, self.brightness, self.contrast)
        contrasted_copy = contrasted.copy()

        # stack the font
        self.cv2_stack_path(contrasted)

        # if required to show the image
        if is_show:
            cv2.imshow('Image', contrasted)

        # return the final image
        return contrasted_copy

    def cv2_stack_path(self, image):
        # if the coordinate of line is not empty
        if self.bottom_right_corner != [] and self.top_left_corner != []:
            cv2.line(image,
                     self.top_left_corner[0],
                     self.bottom_right_corner[0],
                     (0, 255, 0),
                     thickness=2)
            cv2.putText(image,
                        str(self.peak_num),
                        (0, 100),
                        cv2.FONT_ITALIC, 1,
                        (255, 255, 0), 1)
        # stack filename on the image
        # if it is in camera mode
        if self.method == 0:
            cv2.putText(image, 'CAMERA', (0, 40), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)
        else:
            cv2.putText(image, self.files[self.index], (0, 40), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)

    def cv2_resize(self, image, percentage):
        # calculate the resize rate
        width = int(image.shape[1] * percentage / 100)
        height = int(image.shape[0] * percentage / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    def cv2_contrast(self, image, bright, contrast):
        # adjust the contrast and brightness of the image
        contrasted = np.int16(image)
        contrasted = contrast * (contrasted / 127 + 1) - contrast + bright
        contrasted = np.clip(contrasted, 0, 255)
        return np.uint8(contrasted)

    def cv2_callback_mouse(self, action, x, y, flags, *userdata):
        # left click to select the start point
        # right click to select the end point
        if action == cv2.EVENT_LBUTTONDOWN:
            self.top_left_corner = [(x, y)]

        elif action == cv2.EVENT_RBUTTONDOWN:
            self.bottom_right_corner = [(x, y)]
            self.peak_set_flag()
        self.cv2_set_flag()

    def cv2_callback_picture_crop(self, x):
        self.picture_resize = x
        self.cv2_set_flag()

    def cv2_callback_brightness(self, x):
        self.brightness = x
        self.cv2_set_flag()

    def cv2_callback_contrast(self, x):
        self.contrast = x
        self.cv2_set_flag()

    def cv2_callback_window_length(self, x):
        self.window_len = x
        self.cv2_set_flag()

    def cv2_callback_polynomial_order(self, x):
        self.polynomial_order = x
        self.cv2_set_flag()

    def cv2_set_flag(self):
        self.frame_update = True

    def cv2_clear_flag(self):
        self.frame_update = False

    def cv2_check_flag(self):
        return self.frame_update

    def path_check(self):
        if len(self.files) == 0:
            print("Empty Path!")

        else:
            print("Image loaded.")

    def peak_clear_flag(self):
        self.peak_count_update = False

    def peak_set_flag(self):
        self.peak_count_update = True

    def check_lines(self):
        is_coordinate = self.bottom_right_corner != [] and self.top_left_corner != []
        return is_coordinate and self.peak_count_update

    # get the pixel value from the image
    def get_pixels(self, image):
        # split the point into x and y list
        x = [self.top_left_corner[0][0], self.bottom_right_corner[0][0]]
        y = [self.top_left_corner[0][1], self.bottom_right_corner[0][1]]

        # calculate two point's linear equation
        coefficients = np.polyfit(x, y, 1)

        # get coefficients
        a = coefficients[0]
        b = coefficients[1]

        # create list of pixel coordinate
        ys = []
        xs = []

        # get the pixel coordinate
        for i in range(x[0], x[1]):
            ys.append(int(i * a + b))
            xs.append(i)

        value = []
        y_index = 0
        # get the pixel value
        for i in xs:
            value.append(image[ys[y_index]][i])
            y_index += 1

        return value

    # smooth the curve with savgol filter
    def curve_smooth(self, value, is_plot=False):
        x = np.arange(0, len(value))
        y = np.array(value)
        yhat = savgol_filter(y, self.window_len, self.polynomial_order)

        if is_plot:
            plt.plot(x, y, label='Original')
            plt.plot(x, yhat, label='Fitting')
            plt.show()
        return yhat

    # count how many peaks
    def count_peaks(self, value):
        peaks, _ = find_peaks(-value, prominence=1)
        self.peak_num = str(peaks.size)
        print('find ' + self.peak_num + ' peaks:')
        print(peaks)

    # load the original image
    def load_image(self):
        self.original_image = cv2.imread('./' + self.path + '/' + self.files[self.index])

    # switch image
    def next_image(self):
        self.index += 1
        if self.index == len(self.files) - 1:
            self.index = 0
        self.load_image()
        self.cv2_set_flag()

    def previous_image(self):
        self.index -= 1
        if self.index == -1:
            len(self.files) - 1
        self.load_image()
        self.cv2_set_flag()

    def camera_update(self):
        _, self.original_image = self.camera.read()

