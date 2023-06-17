from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore
from ManualController import ManualControllerHandle
from CommandSend import CommandSendHandle
from rvConvert import rvConverterHandle
from CurveController import CurveControllerHandle
from ApproachController import ApproachControllerHandle
from CurveScanController import CurveScanControllerHandle
from ScanController import ScanControllerHandle
from PyQt5.QtWidgets import QMessageBox


class UartControllerCommandHandle:
    def __init__(self, ui, port, debug):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.debug_label = 'UART Command'
        self.approach_label = 'Approach'
        self.system_label = 'System'
        self.curve_test = 'Curve Test'
        self.scan = 'Scan'

        # Register-Voltage Converter
        self.rv_converter = rvConverterHandle(self.ui)

        # Command Send manager
        self.command_send = CommandSendHandle(self.port)

        # Manual control manager
        self.manual_handle = ManualControllerHandle(self.ui, self.port, self.debug,
                                                    self.command_send, self.rv_converter)
        # Curve control manager
        self.curve_handle = CurveControllerHandle(self.ui, self.port, self.debug,
                                                  self.command_send, self.rv_converter)
        # Approach control manager
        self.approach_handle = ApproachControllerHandle(self.ui, self.port, self.debug,
                                                  self.command_send, self.rv_converter)

        # Curve Scan manager
        self.curve_scan_handle = CurveScanControllerHandle(self.ui, self.port, self.debug,
                                                  self.command_send, self.rv_converter)

        # Image Scan manager
        self.scan_handle = ScanControllerHandle(self.ui, self.port, self.debug,
                                                           self.command_send, self.rv_converter)

    def read_port(self):
        while self.port.canReadLine():
            data = self.port.readLine()
            data = QtCore.QTextStream(data).readAll()[:-2]
            splited = data.split('=')

            # get header and datas
            header = splited[0]
            datas = ''

            # Normal format: XXXXX=XXXXX
            if len(splited) == 2:
                datas = splited[1]

            # -- System -- #
            if header == 'VERSI':
                self.debug.print(self.system_label, 'Hardware Version=' + datas)
                self.ui.label_hwversion.setText(datas)

            # -- Curve Handle -- #
            elif header == 'GETAD':
                self.curve_handle.tunneling_update(int(datas))
            elif header == 'APPPI':
                self.curve_handle.pid_update(int(datas))
            elif header == 'APPPU':
                self.curve_handle.punch_update(int(datas))
                self.debug.print(self.approach_label, 'Punch Value=' + str(datas))

            # -- Approach Handle -- #
            # slider amplitude feedback
            elif header == 'APPAM':
                self.debug.print(self.approach_label, 'Slider amplitude(SLOW)=' + str(datas))

            # slider slope feedback
            elif header == 'APPSO':
                self.debug.print(self.approach_label, 'Slider slope(Global)=' + str(datas))

            # slider fast mode limitation
            elif header == 'APPFA':
                self.debug.print(self.approach_label, 'Fast mode limitation=' + str(datas))

            # slider slow mode limitation
            elif header == 'APPSL':
                self.debug.print(self.approach_label, 'Slow mode limitation=' + str(datas))

            # bias voltage
            elif header == 'APPBI':
                self.debug.print(self.approach_label, 'Bias voltage=' + str(datas))

            # target current
            elif header == 'APPTA':
                self.debug.print(self.approach_label, 'Targe current=' + str(datas))

            # crash current
            elif header == 'APPCA':
                self.debug.print(self.approach_label, 'Crash current=' + str(datas))

            # KP
            elif header == 'APPS0':
                self.debug.print(self.approach_label, 'Kp=' + str(datas))

            # KI
            elif header == 'APPS1':
                self.debug.print(self.approach_label, 'Ki=' + str(datas))

            # KD
            elif header == 'APPS2':
                self.debug.print(self.approach_label, 'Kd=' + str(datas))

            # Approach status
            elif header == 'APPRE':
                self.debug.print(self.approach_label, 'Status=' + str(datas))

            # Approach status
            elif header == 'APPST':
                # 1-> 4-> 5-> 6
                # 1 Fast Mode
                # 4 Slow Mode
                # 5 Z extending mode
                # 6 Pid mode
                datas = int(datas)
                if datas == 1:
                    self.debug.print(self.approach_label, 'Fast Mode')
                    self.ui.progressBar.setValue(25)
                    self.ui.label_approach_status.setText('FAST')
                elif datas == 4:
                    self.debug.print(self.approach_label, 'Slow Mode')
                    self.ui.progressBar.setValue(50)
                    self.ui.label_approach_status.setText('SLOW')
                elif datas == 5:
                    self.debug.print(self.approach_label, 'Z Extending Mode')
                    self.ui.progressBar.setValue(75)
                    self.ui.label_approach_status.setText('Z EXT')
                elif datas == 6:
                    self.debug.print(self.approach_label, 'PID Mode')
                    self.ui.progressBar.setValue(100)
                    self.ui.label_approach_status.setText('OK')

            # -- Curve scan Handle -- #

            elif header == 'CTDZP':
                self.curve_scan_handle.di_x_update(int(datas))

            elif header == 'CTDCU':
                self.curve_scan_handle.di_y_update(int(datas))

            elif header == 'CTDOK':
                self.debug.print(self.curve_test, 'D-I test finished.')
                QMessageBox.information(None, 'Curve Scan', 'D-I Test Finished.')
                self.ui.pushButton_curve_dibegin.click()

            elif header == 'CTBBI':
                self.curve_scan_handle.di_x_update(int(datas))

            elif header == 'CTBCU':
                self.curve_scan_handle.di_y_update(int(datas))

            elif header == 'CTBOK':
                self.debug.print(self.curve_test, 'Bias test finished.')
                QMessageBox.information(None, 'Bias Test', 'Bias Test Finished.')
                self.ui.pushButton_curve_bbegin.click()

            # -- Scan -- #
            elif header == 'SCLP0':
                self.scan_handle.line_update_x(int(datas))

            elif header == 'SCLC0':
                self.scan_handle.line_update_y(int(datas))

            elif header == 'SCLP1':
                self.scan_handle.line_update_x1(int(datas))

            elif header == 'SCLC1':
                self.scan_handle.line_update_y1(int(datas))

            elif header == 'SCLOK':
                self.debug.print(self.scan, 'Line Test finished.')
                # QMessageBox.information(None, 'Bias Test', 'Bias Test Finished.')
                self.ui.pushButton_scan_Tbegin.click()

            elif header == 'SCOKO':
                self.debug.print(self.scan, 'Scan finished.')
                # QMessageBox.information(None, 'Bias Test', 'Scan Finished.')
                self.ui.pushButton_scan_begin.click()

            elif header == 'SCPOX':
                self.scan_handle.scan_x_update(int(datas))

            elif header == 'SCPOY':
                self.scan_handle.scan_y_update(int(datas))

            elif header == 'SCCUR':
                self.scan_handle.san_current_update(int(datas))

            # -- Other -- #
            else:
                self.debug.print(self.debug_label, data)





