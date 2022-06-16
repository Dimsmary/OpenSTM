import numpy as np
from numpy import sin
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter, find_peaks


def get_pixels(img, begin, end):
    # split the point into x and y list
    x = [begin[0][0], end[0][0]]
    y = [begin[0][1], end[0][1]]

    # linear fit
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
        value.append(img[ys[y_index]][i])
        y_index += 1

    print(value)
    return value


def curve_plot(value):
    x = np.arange(0, len(value))
    y = np.array(value)

    plt.title('Curve demostrate')
    plt.plot(x, y)
    plt.show()


def objective(x, a, b, c, d):
    return a * sin(b - x) + c * x**2 + d


def curve_fitting(value):
    x = np.arange(0, len(value))
    y = np.array(value)

    popt, _ = curve_fit(objective, x, y)

    a, b, c, d = popt

    x_line = np.arange(min(x), max(x), 1)
    y_line = objective(x_line, a, b, c, d)

    plt.plot(x, y, label='Original')
    plt.plot(x_line, y_line, '--', label='Fitting')
    plt.show()


# smooth the curve and plot with Savgol filter
def curve_smooth(value, window_len, polynomial_order):
    x = np.arange(0, len(value))
    y = np.array(value)
    yhat = savgol_filter(y, window_len, polynomial_order)
    plt.plot(x, y, label='Original')
    plt.plot(x, yhat, label='Fitting')
    plt.show()
    return yhat


def count_peaks(inputs):
    peaks, _ = find_peaks(-inputs, prominence=1)
    print('find ' + str(peaks.size) + ' peaks:')
    print(peaks)
    return str(peaks.size)

