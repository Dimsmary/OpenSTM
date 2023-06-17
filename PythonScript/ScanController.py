import pyqtgraph as pg
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
import numpy as np
import time
from PyQt5.QtWidgets import QMessageBox
import pandas as pd


class ScanControllerHandle:
    def __init__(self, ui, port, debug, command_send, rv_converter):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.command_send = command_send
        self.rv_converter = rv_converter
        self.scan = 'Scan'

        # setting up graphWidget
        self.ui.graphWidget_6.showGrid(x=True, y=True)
        self.pen = pg.mkPen(color=(255, 10, 10))
        self.pen1 = pg.mkPen(color=(10, 10, 255))

        self.graph_x = []
        self.graph_y = []
        self.graph_x_1 = []
        self.graph_y_1 = []

        self.line = self.ui.graphWidget_6.plot(self.graph_x, self.graph_y, pen=self.pen)
        self.line1 = self.ui.graphWidget_6.plot(self.graph_x_1, self.graph_y_1, pen=self.pen1)

        # Setting up MODE comboBox
        self.ui.comboBox_scan_mode.addItems(['UpLeft', 'UpRight',
                                            'DownLeft', 'DownRight'])

        # scan image data restore
        self.image_x = []
        self.image_y = []
        self.image_current = []
        self.pixels = []

        pixels = [[0, 0, 0],
                  [0, 1, 0],
                  [0, 0, 0]]
        array = np.array(pixels, dtype=np.uint16)
        self.img = Image.fromarray(array)

    # --> Line Test
    def line_update_x(self, value):
        self.graph_x.append(value)

    def line_update_y(self, value):
        self.graph_y.append(value)
        self.line.setData(self.graph_x, self.graph_y)

    def line_update_x1(self, value):
        self.graph_x_1.append(value)

    def line_update_y1(self, value):
        self.graph_y_1.append(value)
        self.line1.setData(self.graph_x_1, self.graph_y_1)

    def line_test_begin(self):
        if self.ui.pushButton_scan_Tbegin.text() == 'Begin':
            # generate file name
            xy_label = 'Y'
            if self.ui.radioButton_X.isChecked():
                xy_label = 'X'

            ch_label = 'CC'
            if self.ui.radioButton_lineCH.isChecked():
                ch_label = 'CH'

            ez_switch = 0
            if self.ui.radioButton_lineZ.isChecked():
                ez_switch = 1

            time_stamp = time.strftime('%Y-%m-%d %H-%M', time.localtime()) + '-'
            curve_attribute = 'TARGET' + str(self.ui.spinBox_scan_Ttarget.value()) + '-'
            curve_attribute = curve_attribute + 'PID' + str(self.ui.spinBox_scan_line_piderr.value()) + '-'
            curve_attribute = curve_attribute + 'SETPOINT' + str(self.ui.lineEdit_approach_setpoint.text()) + '-'
            curve_attribute = curve_attribute + 'INC' + str(self.ui.spinBox_scan_Tinc.value()) + '-'
            curve_attribute = curve_attribute + 'DELAY' + str(self.ui.spinBox_scan_freq_2.value()) + '-'
            curve_attribute = curve_attribute + 'BIAS' + str(self.ui.spinBox_settings_biasVoltage.value())
            self.ui.lineEdit_scan_line_filename.setText('LineTest-' + xy_label + '-' +
                                                        ch_label + '-' + time_stamp + curve_attribute)

            # empty the graph buffer
            self.graph_x = []
            self.graph_y = []
            self.graph_x_1 = []
            self.graph_y_1 = []

            # -- Send UART command -- #
            origin_x = self.ui.spinBox_scan_origin_Tx.value()
            origin_y = self.ui.spinBox_scan_origin_Ty.value()
            target = self.ui.spinBox_scan_Ttarget.value()
            cc_inc = self.ui.spinBox_scan_line_piderr.value()
            retract_num = self.ui.spinBox_scan_line_retract.value()

            # mode = 0 for constant height, 1 for constant current
            if self.ui.radioButton_lineCH.isChecked():
                mode = 0
            else:
                mode = 1

            if self.ui.radioButton_X.isChecked():
                if target > 0:
                    target = origin_x + target
                    direction = 1
                else:
                    target = origin_x + (-target)
                    direction = 2
            else:
                if target > 0:
                    target = origin_y + target
                    direction = 3
                else:
                    target = origin_y + (-target)
                    direction = 4

            delay = self.ui.spinBox_scan_freq_2.value()
            inc = self.ui.spinBox_scan_Tinc.value()

            # Must send delay first
            self.command_send.send_to_scan_delay(delay)
            self.command_send.send_to_scan_line_target(target)
            self.command_send.send_to_scan_line_inc(inc)
            self.command_send.send_to_scan_line_direction(direction)
            self.command_send.send_to_scan_cc_inc(cc_inc)
            self.command_send.send_to_scan_ez_switch(ez_switch)
            self.command_send.send_to_scan_retract(retract_num)
            self.command_send.send_to_scan_ccch_mode(mode)

            # send origin last, origin_y must behind origin_x
            self.command_send.send_to_scan_line_origin_x(origin_x)
            self.command_send.send_to_scan_line_origin_y(origin_y)

            # begin test
            self.command_send.send_to_scan_reg(1)

            # Change text on button
            self.ui.pushButton_scan_Tbegin.setText('Stop')

        else:
            self.command_send.send_to_scan_reg(0)
            self.ui.pushButton_scan_Tbegin.setText('Begin')

    def scan_begin(self):
        if self.ui.pushButton_scan_begin.text() == 'Begin':
            # -- generate file name -- #
            ch_label = 'CC'
            ch_mode = 1
            if self.ui.radioButton_scan_ch.isChecked():
                ch_label = 'CH'
                ch_mode = 0
            time_stamp = time.strftime('%Y-%m-%d %H-%M', time.localtime()) + '-'
            curve_attribute = 'SIZE' + str(self.ui.spinBox_scan_size.value()) + '-'
            curve_attribute = curve_attribute + 'ORIGIN' + str(self.ui.spinBox_scan_origin_x.value()) \
                              + 'x' + str(self.ui.spinBox_scan_origin_y.value()) + '-'
            curve_attribute = curve_attribute + 'MODE' + str(self.ui.comboBox_scan_mode.currentIndex()) + '-'
            curve_attribute = curve_attribute + 'PID' + str(self.ui.spinBox_scan_piderr.value()) + '-'
            curve_attribute = curve_attribute + 'SETPOINT' + str(self.ui.lineEdit_approach_setpoint.text()) + '-'
            curve_attribute = curve_attribute + 'INC' + str(self.ui.spinBox_scan_inc.value()) + '-'
            curve_attribute = curve_attribute + 'DELAY' + str(self.ui.spinBox_scan_freq.value()) + '-'
            curve_attribute = curve_attribute + 'BIAS' + str(self.ui.spinBox_settings_biasVoltage.value())
            self.ui.lineEdit_scan_image_filename.setText('Image-' + ch_label + '-' + time_stamp + curve_attribute)
            # Empty the buffer
            self.image_x = []
            self.image_y = []
            self.image_current = []

            # -- send parameters -- #
            mode = self.ui.comboBox_scan_mode.currentIndex()
            origin_x = self.ui.spinBox_scan_origin_x.value()
            origin_y = self.ui.spinBox_scan_origin_y.value()
            size = self.ui.spinBox_scan_size.value()
            inc = self.ui.spinBox_scan_inc.value()
            delay = self.ui.spinBox_scan_freq.value()
            cc_inc = self.ui.spinBox_scan_piderr.value()
            retract_num = self.ui.spinBox_scan_line_retract.value()
            ez_switch = 0
            if self.ui.radioButton_scan_z.isChecked():
                ez_switch = 1

            begin_x = 0
            begin_y = 0
            end_x = 0
            end_y = 0
            # UpRight corner as begin point
            if mode == 0:
                begin_x = origin_x
                begin_y = origin_y
                end_x = origin_x + size
                end_y = origin_y + size

            # UpLeft corner as begin point
            elif mode == 1:
                begin_x = origin_x + size
                begin_y = origin_y
                end_x = origin_x
                end_y = origin_y + size

            # DownRight corner as begin point
            elif mode == 2:
                begin_x = origin_x
                begin_y = origin_y + size
                end_x = origin_x + size
                end_y = origin_y

            # DownLeft corner as begin point
            elif mode == 3:
                begin_x = origin_x + size
                begin_y = origin_y + size
                end_x = origin_x
                end_y = origin_y

            self.command_send.send_to_scan_delay(delay)
            self.command_send.send_to_scan_x_begin(begin_x)
            self.command_send.send_to_scan_x_end(end_x)
            self.command_send.send_to_scan_y_begin(begin_y)
            self.command_send.send_to_scan_y_end(end_y)
            self.command_send.send_to_scan_inc(inc)
            self.command_send.send_to_scan_cc_inc(cc_inc)
            self.command_send.send_to_scan_ez_switch(ez_switch)
            self.command_send.send_to_scan_retract(retract_num)
            self.command_send.send_to_scan_ccch_mode(ch_mode)
            self.command_send.send_to_scan_mode(mode)

            # begin test
            self.command_send.send_to_scan_reg(2)

            self.ui.pushButton_scan_begin.setText('Stop')

        else:
            # Reformat the current data into pixels
            self.pixels = []
            pixels_line = [self.image_current[0]]
            for i in range(1, len(self.image_current)):
                # if y is another line
                if self.image_y[i] != self.image_y[i - 1]:
                    # append line data to the pixels, empty the pixels_line buffer
                    self.pixels.append(pixels_line)
                    pixels_line = []
                pixels_line.append(self.image_current[i])
            self.pixels.append(pixels_line)
            # Turn pixels to np array
            try:
                array = np.array(self.pixels, dtype=np.uint16)

            except ValueError:
                # Terminate the Scan process
                self.command_send.send_to_scan_reg(0)
                self.ui.pushButton_scan_begin.setText('Begin')

            else:
                # Proceed the display image
                display_array = array.copy()
                min_num = np.amin(display_array)

                display_array = display_array - min_num
                max_num = np.amax(display_array)
                display_array = (display_array / max_num) * 255
                display_array = display_array.astype(np.uint8)

                # Generate original Image
                self.img = Image.fromarray(array)
                display_img = Image.fromarray(display_array)
                display_img = display_img.resize((361, 361))

                # Convert into QT image
                qt_img = ImageQt(display_img)
                pixmap = QPixmap.fromImage(qt_img)

                # Display Image
                self.ui.scan_image.setPixmap(pixmap)

                # Terminate the Scan process
                self.command_send.send_to_scan_reg(0)
                self.ui.pushButton_scan_begin.setText('Begin')

    def scan_x_update(self, value):
        self.image_x.append(value)

    def scan_y_update(self, value):
        self.image_y.append(value)

    def san_current_update(self, value):
        self.image_current.append(value)

    def line_save(self):
        QMessageBox.information(None, 'Save', 'File Saved!')
        save_data = pd.DataFrame({'Position1': self.graph_x,
                                  'Current': self.graph_y,
                                  'Position2': self.graph_x_1,
                                  'Current2': self.graph_y_1})
        path = 'ScanData/' + self.ui.lineEdit_scan_line_filename.text() + '.xlsx'
        save_data.to_excel(path)
        self.debug.print(self.scan, 'File Saved to ' + '\"' + path + '\"')

    def image_save(self):
        QMessageBox.information(None, 'Save', 'Image Saved!')
        save_data = pd.DataFrame({'X': self.image_x,
                                  'Y': self.image_y,
                                  'Current': self.image_current})
        path = 'ScanData/' + self.ui.lineEdit_scan_image_filename.text()
        save_data.to_excel(path + '.xlsx')

        self.debug.print(self.scan, 'File Saved to ' + '\"' + path + '\"')
        self.img.save(path + '.tif')









