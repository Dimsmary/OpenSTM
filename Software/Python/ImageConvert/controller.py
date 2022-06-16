from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from UI import Ui_MainWindow
import pandas as pd
import cv2
import numpy as np


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.df = pd.DataFrame()
        self.filename = ''

    # GUI setup here
    def setup_control(self):
        self.ui.pushButton_open.clicked.connect(self.open_file)
        self.ui.pushButton_draw.clicked.connect(self.draw_image)

    def draw_image(self):
        df = self.df
        # get minimum of data
        x_min = df['DAC-X'].min()
        y_min = df['DAC-Y'].min()
        value_min = df['ADC'].min()

        # init axis value
        df['DAC-X'] = df['DAC-X'] - x_min
        df['DAC-Y'] = df['DAC-Y'] - y_min
        times = int(self.ui.lineEdit_times.text())
        df['DAC-X'] = df['DAC-X'] / times
        df['DAC-Y'] = df['DAC-Y'] / times

        # init gray value
        df['ADC'] = df['ADC'] - value_min
        pixel_value_max = df['ADC'].max()
        df['ADC'] = (df['ADC'] / pixel_value_max) * 256

        # get maximum of data
        x_pixel_max = int(df['DAC-X'].max()) + 1
        y_pixel_max = int(df['DAC-Y'].max()) + 1

        blank_img = np.zeros((x_pixel_max, y_pixel_max, 1), dtype="uint8")

        for index, row in df.iterrows():
            x = int(row['DAC-X'])
            y = int(row['DAC-Y'])
            value = int(row['ADC'])
            blank_img[x][y] = value
            self.ui.progressBar.setValue(int(y / (y_pixel_max - 1) * 100))

        winname = 'IMG DISPLAY'
        cv2.namedWindow(winname)  # Create a named window
        cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
        cv2.imshow(winname, blank_img)
        cv2.imwrite(self.filename + '.bmp', blank_img)

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileNames(self, 'Open file', './')
        filename = filename[0]
        self.filename = filename
        self.ui.lineEdit_address.setText(filename)

        # open excel file
        df = pd.read_excel(filename)

        # print original data msg
        self.ui.label_originallength.setText(str(df.shape[0]))

        # drop duplicate and null value
        df.dropna(inplace=True)
        df.drop_duplicates(subset=['DAC-X', 'DAC-Y'], keep='last', inplace=True)
        self.ui.label_droplength.setText(str(df.shape[0]))
        self.df = df


        