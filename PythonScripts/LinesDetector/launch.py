import cv2

from packedmodule import LineDetector


# Create object of linearDetector
lineDetector = LineDetector('image', method=1, camera=0)

# variable for key capture
k = 0

# capture first image
image = lineDetector.cv2_read_image()

while k != 27:
    # lineDetector.camera_update()
    image = lineDetector.cv2_read_image()
    # if it is need to update
    if lineDetector.cv2_check_flag():
        lineDetector.cv2_clear_flag()
        lineDetector.cv2_read_image()
        if lineDetector.check_lines():
            value = lineDetector.get_pixels(image)
            yhat = lineDetector.curve_smooth(value, is_plot=True)
            lineDetector.count_peaks(yhat)
            lineDetector.peak_clear_flag()

    k = cv2.waitKey(1)
    # if pressed ESC
    if k == 117:
        pass

    # if pressed x
    elif k == 120:
        lineDetector.next_image()


    # if pressed z
    elif k == 122:
        lineDetector.previous_image()





