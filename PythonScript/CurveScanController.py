import time
import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
import math


class CurveScanControllerHandle:
    def __init__(self, ui, port, debug, command_send, rv_converter):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.command_send = command_send
        self.rv_converter = rv_converter

        # setting up graphWidget
        self.ui.graphWidget_4.showGrid(x=True, y=True)
        self.pen = pg.mkPen(color=(255, 10, 10))

        self.ui.graphWidget_5.showGrid(x=True, y=True)
        self.pen1 = pg.mkPen(color=(10, 10, 255))

        # graph store
        self.graph_x = []
        self.graph_y = []
        self.line_DI = self.ui.graphWidget_4.plot(self.graph_x, self.graph_y, pen=self.pen)

        self.graph_x_ln = []
        self.graph_y_ln = []
        self.line_LN = self.ui.graphWidget_5.plot(self.graph_x_ln, self.graph_y_ln, pen=self.pen1)

        self.curve_test = 'Curve Test'
        self.mode = 0

    def freq_cal(self, delay):
        return int(1000 / delay)

    def update_eta(self, step, delay, label):
        eta_s = int(65535 / step * delay / 1000)
        eta_m = int(eta_s / 60)
        eta_s = eta_s - eta_m * 60
        label.setText(str(eta_m) + 'm' + str(eta_s) + 's')

    # --> Di Test --- #
    def di_begin(self):
        if self.ui.pushButton_curve_dibegin.text() == 'Begin':
            # switch mode
            self.mode = 1
            # Clear
            self.graph_x = []
            self.graph_y = []
            self.graph_x_ln = []
            self.graph_y_ln = []

            # Generate the file name
            time_stamp = time.strftime('%Y-%m-%d %H-%M', time.localtime()) + '-'
            curve_attribute = 'SP' + str(self.ui.spinBox_curve_distop.value()) + '-'
            curve_attribute = curve_attribute + 'INC' + str(self.ui.spinBox_curve_diinc.value()) + '-'
            curve_attribute = curve_attribute + 'DEL' + str(self.ui.spinBox_curve_difreq.value()) + '-'
            curve_attribute = curve_attribute + 'BIAS' + str(self.ui.spinBox_settings_biasVoltage.value())
            self.ui.lineEdit_curve_filename.setText('DITest-' + time_stamp + curve_attribute)

            # Switch the button
            self.ui.pushButton_curve_dibegin.setText('Stop')

            # -- Send UART command -- #
            stop = self.ui.spinBox_curve_distop.value()
            stop = self.rv_converter.voltage_to_register_adc(stop)
            inc = self.ui.spinBox_curve_diinc.value()
            delay = self.ui.spinBox_curve_difreq.value()

            # Parameters of DI scan
            self.command_send.send_to_curve_test_di_stop(stop)
            self.command_send.send_to_curve_test_di_inc(inc)
            self.command_send.send_to_curve_test_delay(delay)
            self.command_send.send_to_curve_test_reset(0)

            time.sleep(0.1)
            # Scan begin
            self.command_send.send_to_curve_test_register(1)

        else:
            #switch mode
            self.mode = 0
            # Switch the button
            self.command_send.send_to_curve_test_register(0)
            print(self.graph_x)
            print(self.graph_y)
            self.ui.pushButton_curve_dibegin.setText('Begin')

    def di_inc_switch(self):
        # switch register to voltage in mV
        value = self.ui.spinBox_curve_diinc.value()
        voltage = self.rv_converter.single_step_DAC_16bit(value)
        voltage = int(voltage)
        self.ui.label_curve_diinc_mv.setText(str(voltage) + 'mV')

        # update ETA
        step = value
        delay = self.ui.spinBox_curve_difreq.value()
        self.update_eta(step, delay, self.ui.label_curve_dieta)

    def di_freq_switch(self):
        delay = self.ui.spinBox_curve_difreq.value()
        freq = self.freq_cal(delay)
        self.ui.label_curve_diinc_hz.setText(str(freq) + 'Hz')

        # update ETA
        step = self.ui.spinBox_curve_diinc.value()
        delay = delay
        self.update_eta(step, delay, self.ui.label_curve_dieta)

    def di_x_update(self, value):
        # update graphic
        self.graph_x.append(value)
        if self.mode == 1:
            self.graph_x_ln.append(value)

    def di_y_update(self, value):
        self.graph_y.append(value)
        if self.mode == 1:
            voltage = -self.rv_converter.register_to_voltage_adc(value)
            self.graph_y_ln.append(math.log(voltage))
            self.line_LN.setData(self.graph_x_ln, self.graph_y_ln)
        self.line_DI.setData(self.graph_x, self.graph_y)

    # --> BIAS Test --- #
    def bias_begin(self):
        if self.ui.pushButton_curve_bbegin.text() == 'Begin':
            self.mode = 2
            # Clear
            self.graph_x = []
            self.graph_y = []
            self.graph_x_ln = []
            self.graph_y_ln = []

            # Generate the file name
            time_stamp = time.strftime('%Y-%m-%d %H-%M', time.localtime()) + '-'
            curve_attribute = 'RANGE' + str(self.ui.spinBox_curve_bstop.value()) + '-'
            curve_attribute = curve_attribute + 'INC' + str(self.ui.spinBox_curve_binc.value()) + '-'
            curve_attribute = curve_attribute + 'DEL' + str(self.ui.spinBox_curve_bfreq.value()) + '-'
            curve_attribute = curve_attribute + 'BIAS' + str(self.ui.spinBox_settings_biasVoltage.value())
            self.ui.lineEdit_curve_filename.setText('BiasTest-' + time_stamp + curve_attribute)

            # Switch the button
            self.ui.pushButton_curve_bbegin.setText('Stop')

            # -- Send UART command -- #
            stop = self.ui.spinBox_curve_bstop.value()
            stop = self.rv_converter.voltage_to_register_16bit(stop)
            start = 32768
            if self.ui.checkBox_curve_bipolar.isChecked():
                start = 32768 - (stop - 32768)

            inc = self.ui.spinBox_curve_binc.value()
            delay = self.ui.spinBox_curve_bfreq.value()

            # Parameters of DI scan
            self.command_send.send_to_curve_test_bi_stop(stop)
            self.command_send.send_to_curve_test_bi_inc(inc)
            self.command_send.send_to_curve_test_delay(delay)
            self.command_send.send_to_curve_test_bi_start(start)
            self.command_send.send_to_curve_test_reset(1)

            time.sleep(0.1)
            # Scan begin
            self.command_send.send_to_curve_test_register(2)

        else:
            self.mode = 0
            # Switch the button
            self.command_send.send_to_curve_test_register(0)
            print(self.graph_x)
            print(self.graph_y)
            self.ui.pushButton_curve_bbegin.setText('Begin')

    def bi_inc_switch(self):
        # switch register to voltage in mV
        value = self.ui.spinBox_curve_binc.value()
        voltage = self.rv_converter.single_step_DAC_16bit(value)
        voltage = int(voltage)
        self.ui.label_curve_biinc_mv.setText(str(voltage) + 'mV')

        # update ETA
        step = value
        delay = self.ui.spinBox_curve_difreq.value()
        self.update_eta(step, delay, self.ui.label_bieta)

    def bi_freq_switch(self):
        delay = self.ui.spinBox_curve_bfreq.value()
        freq = self.freq_cal(delay)
        self.ui.label_curve_biinc_hz.setText(str(freq) + 'Hz')

        # update ETA
        step = self.ui.spinBox_curve_binc.value()
        delay = delay
        self.update_eta(step, delay, self.ui.label_bieta)

    def save_data(self):
        QMessageBox.information(None, 'Save', 'File Saved!')
        save_data = pd.DataFrame({'Z Voltage/Bias': self.graph_x,
                                  'Current': self.graph_y,
                                  'log_e': self.graph_y_ln})
        path = 'CurveTestData/' + self.ui.lineEdit_curve_filename.text() + '.xlsx'
        save_data.to_excel(path)
        self.debug.print(self.curve_test, 'File Saved to ' + '\"' + path + '\"')





