from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtWidgets import QMessageBox
from UI import Ui_MainWindow
import serial
import serial.tools.list_ports
import pandas as pd
from datetime import datetime


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.serial_port = serial.Serial()
        self.qt_serial_port = QSerialPort(readyRead=self.qt_serial_receive)
        self.ports = []
        self.is_connect = False

        # set dac order
        self.SAMPLE_DAC = 0
        self.Z_DAC = 1
        self.Y_DAC = 2
        self.X_DAC = 3

        # scan data restore
        self.scan_data_z = []
        self.scan_data_x = []
        self.scan_data_y = []
        self.scan_data_value = []
        self.dynamic_record_value = []
        self.dynamic_record_z = []
        self.dynamic_discard = 0
        self.dynamic_time = []

        # crash time record
        self.last_time = datetime.now()
        self.crash_est = []
        self.crash_cra = []
        self.crash_interval = []
        self.crash_dacval = []

        # bias record
        self.bias_data = []

    def setup_control(self):
        # set up Tab enabled
        self.ui.tabWidget.setEnabled(False)

        # Add baud rate list
        self.ui.comboBox_baudrate.addItem('500000')
        self.ui.comboBox_baudrate.addItem('250000')
        self.ui.comboBox_baudrate.addItem('115200')
        self.ui.comboBox_baudrate.addItem('9600')

        # Add Motor Select
        self.ui.comboBox_motorselect.addItems(['ALL', 'MotorA', 'MotorB', 'MotorC'])

        # Uart Control
        self.ui.pushButton_uartscan.clicked.connect(self.uart_scan)
        self.ui.pushButton_uartconnect.clicked.connect(self.uart_connect)

        # Coarse approach
        self.ui.pushButton_motorforward.clicked.connect(self.motor_forward)
        self.ui.pushButton_motorbackward.clicked.connect(self.motor_backward)
        self.ui.pushButton_motorforward_auto.clicked.connect(self.motor_forward_auto)
        self.ui.pushButton_motorbackward_auto.clicked.connect(self.motor_backward_auto)
        self.ui.pushButton_zadjustplus.clicked.connect(self.z_adjust_plus)
        self.ui.pushButton_zadjustminus.clicked.connect(self.z_adjust_minus)

        # Z scan
        self.ui.pushButton_tunnelingtest.clicked.connect(self.tunneling_test)

        # debug
        self.ui.pushButton_debugget.clicked.connect(self.debug_get)
        self.ui.pushButton_debugset.clicked.connect(self.debug_set)
        self.ui.horizontalSlider_debug.valueChanged.connect(self.debug_slider)
        self.ui.comboBox_debug.addItems(['0', '1', '2', '3'])
        self.ui.pushButton_debugreset.clicked.connect(self.debug_reset)

        # FINE APPROACH
        self.ui.pushButton_samplevoltage.clicked.connect(self.sample_voltage)
        self.ui.pushButton_fineapproach.clicked.connect(self.fine_approach)
        self.ui.pushButton_zrecord.clicked.connect(self.z_record)

        # Scan begin
        self.ui.pushButton_scan.clicked.connect(self.scan)

        # sample test
        self.ui.pushButton_biastest.clicked.connect(self.bias_test)

    def bias_test(self):
        if self.ui.pushButton_biastest.text() == 'BEGIN':
            self.ui.pushButton_biastest.setText('STOP')
            self.bias_data = []
            self.scan_data_value = []
            end = self.convert_dac_voltage(int(self.ui.lineEdit_biasend.text()))
            self.qt_send_command('IE', end)
            self.qt_send_command('IS', int(self.ui.lineEdit_biassteps.text()))
            self.qt_send_command('IG', 0)

        else:
            self.qt_send_command('IH', 0)
            self.ui.pushButton_biastest.setText('BEGIN')

            df = pd.DataFrame(self.scan_data_value, self.bias_data)

            end = '-E' + self.ui.lineEdit_biasend.text()
            scan_step = '-S' + self.ui.lineEdit_biassteps.text()
            param = end + scan_step
            df.to_excel('BIASData' + param + '.xlsx')

    # *** SCAN BEGIN *** #
    def scan(self):
        if self.ui.pushButton_scan.text() == 'SCAN':
            self.ui.pushButton_scan.setText('STOP')
            self.qt_send_command('SB', int(self.ui.lineEdit_scanbegin.text())-32767)
            self.qt_send_command('SE', int(self.ui.lineEdit_scanend.text())-32767)
            self.qt_send_command('SS', int(self.ui.lineEdit_scansteps.text()))
            self.qt_send_command('SD', int(self.ui.lineEdit_scandelay.text()))

            if self.ui.checkBox_constheightmode.checkState():
                if not self.ui.checkBox_scanreverse.checkState():
                    param = 2

                else:
                    param = 3

            else:
                if not self.ui.checkBox_scanreverse.checkState():
                    param = 0

                else:
                    param = 1

            self.qt_send_command('SG', param)

            self.scan_data_x = []
            self.scan_data_y = []
            self.scan_data_value = []

        else:
            df = pd.DataFrame(columns=['DAC-X', 'DAC-Y', 'ADC'])
            df['DAC-X'] = self.scan_data_x
            df['DAC-Y'] = self.scan_data_y
            df['ADC'] = self.scan_data_value

            sample_voltage = '-V' + self.ui.lineEdit_samplevoltage.text()
            test_delay = '-D' + self.ui.lineEdit_scandelay.text()
            dac_value = '-Z' +self.ui.label_daczregister.text()
            scan_step = '-S' + self.ui.lineEdit_scansteps.text()
            range = '-R' + self.ui.lineEdit_scanbegin.text() + 'to' + self.ui.lineEdit_scanend.text()
            reverse = '-RE=' + str(self.ui.checkBox_scanreverse.checkState())
            param = sample_voltage + test_delay + scan_step  + dac_value + range + reverse
            df.to_excel('SCANData' + param + '.xlsx')

            self.qt_send_command('ST', 0)
            self.ui.pushButton_scan.setText('SCAN')

    def qt_send_command(self, command, param):
        self.qt_serial_port.write((command + str(param) + '\n').encode())

    # *** Tunneling Curve TEST *** #
    def z_adjust_plus(self):
        register_val = int(self.ui.label_daczregister.text()) + int(self.ui.lineEdit_zadjust.text())
        cs = self.Z_DAC + 1
        param = cs * 100000 + register_val
        self.qt_serial_port.write(('DA' + str(param) + '\n').encode())

    def z_adjust_minus(self):
        register_val = int(self.ui.label_daczregister.text()) - int(self.ui.lineEdit_zadjust.text())
        cs = self.Z_DAC + 1
        param = cs * 100000 + register_val
        self.qt_serial_port.write(('DA' + str(param) + '\n').encode())

    def tunneling_test(self):
        if self.ui.pushButton_tunnelingtest.text() == 'TEST':
            self.ui.pushButton_tunnelingtest.setText('STOP')
            # Clear the record buffer
            self.scan_data_z = []
            self.scan_data_value = []

            # send begin command to MCU
            self.qt_serial_port.write(('T1' + str(self.ui.lineEdit_ztestdelay.text()) + '\n').encode())
            self.qt_serial_port.write(('T2' + str(self.ui.lineEdit_zteststep.text()) + '\n').encode())
            self.qt_serial_port.write('TT\n'.encode())

        else:
            self.qt_serial_port.write('TN\n'.encode())
            self.ui.pushButton_tunnelingtest.setText('TEST')
            df = pd.DataFrame(self.scan_data_z, self.scan_data_value)
            sample_voltage = self.ui.lineEdit_samplevoltage.text()
            test_delay = self.ui.lineEdit_ztestdelay.text()
            test_step = self.ui.lineEdit_zteststep.text()
            param = '-V' + sample_voltage + '-D' + test_delay + '-S' + test_step
            df.to_excel('ScanTest' + param + '.xlsx')

    def z_record(self):
        if self.ui.pushButton_zrecord.text() == 'REC':
            self.ui.pushButton_zrecord.setText('STOP')
            self.dynamic_record_value = []
            self.dynamic_record_z = []
            self.dynamic_time = []
            self.dynamic_discard = 0
        else:
            self.ui.pushButton_zrecord.setText('REC')
            df = pd.DataFrame(columns=['Time', 'DAC-Z', 'ADC'])
            df['Time'] = self.dynamic_time
            df['DAC-Z'] = self.dynamic_record_z
            df['ADC'] = self.dynamic_record_value

            sample_voltage = self.ui.lineEdit_samplevoltage.text()
            test_delay = self.ui.lineEdit_ztestdelay.text()
            dac_value = self.ui.label_daczregister.text()
            param = '-V' + sample_voltage + '-D' + test_delay + '-' + dac_value
            df.to_excel('DynamicTest' + param + '.xlsx')

    # *** FINE APPROACH *** #
    @QtCore.pyqtSlot()
    def qt_serial_receive(self):
        while self.qt_serial_port.canReadLine():
            text = self.qt_serial_port.readLine().data().decode()
            text = text.rstrip('\r\n')
            # convert receive data into command and param
            header = text[0:2]
            param = text[2:]

            # restore ad/da value
            try:
                param = int(param)
            except ValueError:
                print(param)

            # dac Z value get
            if header == 'DZ':
                self.ui.label_daczregister.setText(str(param))

            # dac X value get
            if header == 'DX':
                self.ui.label_dacxregister.setText(str(param))

            # dac Y value get
            if header == 'DY':
                self.ui.label_dacyregister.setText(str(param))

            # dac SAMPLE value get
            if header == 'DS':
                self.ui.label_dacsampleregister.setText(str(param))

            # adc value get
            elif header == 'AD':
                self.ui.label_adcregister.setText(str(param))
                if self.ui.pushButton_tunnelingtest.text() == 'STOP':
                    self.scan_data_append()

                if self.ui.pushButton_zrecord.text() == 'STOP':
                    self.dynamic_data_append()

                if self.ui.pushButton_scan.text() == 'STOP':
                    self.scan_data_append_xy()

                if self.ui.pushButton_biastest.text() == 'STOP':
                    self.bias_data_append()

            # Tunneling current established
            elif header == 'DO':
                self.ui.label_approachsta.setText('Approach:OK')
                print("Tunneling Current established")
                self.crash_time_recorder('est')

            # Tunneling Crashed
            elif header == 'CR':
                self.ui.label_approachsta.setText('Approach:NULL')
                self.crash_time_recorder('cra')
                print("Tunneling Current CRASHED")
                print("Crashed Value:" + self.ui.label_daczregister.text())

    def bias_data_append(self):
        self.bias_data.append(self.ui.label_dacsampleregister.text())
        self.scan_data_value.append(self.ui.label_adcregister.text())

    def scan_data_append_xy(self):
        self.scan_data_x.append(self.ui.label_dacxregister.text())
        self.scan_data_y.append(self.ui.label_dacyregister.text())
        self.scan_data_value.append(self.ui.label_adcregister.text())

    def scan_data_append(self):
        self.scan_data_z.append(self.ui.label_daczregister.text())
        self.scan_data_value.append(self.ui.label_adcregister.text())

    def dynamic_data_append(self):
        # if self.dynamic_discard < 10:
        #     self.dynamic_discard += 1
        # else:
        #     self.dynamic_discard = 0
        self.dynamic_time.append(str(datetime.now())[11:])
        self.dynamic_record_value.append(self.ui.label_adcregister.text())
        self.dynamic_record_z.append(self.ui.label_daczregister.text())

    def crash_time_recorder(self, param):
        if param == 'est':
            self.last_time = datetime.now()
            self.ui.label_est.setText(str(self.last_time)[11:])
        else:
            now = datetime.now()
            interval = str(now - self.last_time)
            self.ui.label_cra.setText(str(now)[11:])
            self.ui.label_interval.setText(interval)

            self.crash_est.append(str(self.last_time))
            self.crash_cra.append(str(now))
            self.crash_interval.append(interval)
            self.crash_dacval.append(self.ui.label_daczregister.text())

            df = pd.DataFrame(columns=['Established', 'Crashed', 'Interval', 'DACZ'])
            df['Established'] = self.crash_est
            df['Crashed'] = self.crash_cra
            df['Interval'] = self.crash_interval
            df['DACZ'] = self.crash_dacval
            df.to_excel('CrashInterval.xlsx')

    def sample_voltage(self):
        # compute register value
        voltage = float(self.ui.lineEdit_samplevoltage.text())
        if self.ui.pushButton_fineapproach.text() == 'STOP':
            self.qt_send_voltage(voltage, self.SAMPLE_DAC)

        else:
            self.send_voltage(voltage, self.SAMPLE_DAC)
        self.ui.label_samplevoltage.setText('NOW:' + str(voltage) + 'V')

    def fine_approach(self):
        # if it is wait for approach
        if self.ui.pushButton_fineapproach.text() == 'Approach':
            tunneling_voltage_limit = self.convert_adc_voltage(float(self.ui.lineEdit_currentlimit.text()))
            tunneling_crash_limit = self.convert_adc_voltage(float(self.ui.lineEdit_crashlimit.text()))
            motor_forward_step = self.ui.lineEdit_forwardsteps.text()
            piezo_step = self.ui.lineEdit_zsteps.text()
            piezo_delay = self.ui.lineEdit_zdelay.text()
            piezo_drwaback = self.ui.lineEdit_backpiezostep.text()

            self.ui.label_currentlimit.setText(str(tunneling_voltage_limit))
            self.ui.label_crashlimit.setText(str(tunneling_crash_limit))

            sta_0 = self.send_command('TU', tunneling_voltage_limit)
            sta_1 = self.send_command('TC', tunneling_crash_limit)
            sta_2 = self.send_command('TF', int(motor_forward_step))
            sta_3 = self.send_command('TS', int(piezo_step))
            sta_4 = self.send_command('TD', int(piezo_delay))
            sta_5 = self.send_command('TP', int(piezo_drwaback))
            sta_6 = self.send_command('TG', 0)

            if sta_0 and sta_1 and sta_2 and sta_3 and sta_4 and sta_5 and sta_6:
                self.ui.progressBar.setValue(25)
                self.ui.pushButton_fineapproach.setText('STOP')
                self.serial_port.close()
                self.qt_serial_port.open(QtCore.QIODevice.ReadWrite)
            else:
                QMessageBox.about(self, 'Approach', 'Parameters transfer failed!')

        else:
            self.qt_serial_port.close()
            self.serial_port.open()
            self.send_command('TH', 0)
            if self.send_command('TH', 0):
                self.ui.progressBar.setValue(0)
                self.ui.pushButton_fineapproach.setText('Approach')

            else:
                QMessageBox.about(self, 'Approach', 'Command transfer failed!')
                self.serial_port.close()
                self.qt_serial_port.open(QtCore.QIODevice.ReadWrite)

    def convert_dac_register(self, register_val):
        return (register_val / 65535) * 20.1 - 10.05

    def convert_dac_voltage(self, voltage):
        return int((voltage + 10.05) / 20.1 * 65535)

    def convert_adc_register(self, register_val):
        return (register_val / 65535) * 24.576 - 12.288

    def convert_adc_voltage(self, voltage):
        return int((voltage + 12.288) / 24.576 * 65535)

    def send_voltage(self, voltage, dac_num):
        register = self.convert_dac_voltage(voltage)
        param = (dac_num + 1) * 100000 + register
        self.serial_port.reset_input_buffer()
        self.serial_port.write(('DA' + str(param) + '\n').encode())
        # return status
        if self.serial_port.readline().decode()[0:2] == 'OK':
            return True
        else:
            return False

    def qt_send_voltage(self, voltage, dac_num):
        register = self.convert_dac_voltage(voltage)
        param = (dac_num + 1) * 100000 + register
        self.qt_serial_port.write(('DA' + str(param) + '\n').encode())

    def send_command(self, command, param):
        self.serial_port.reset_input_buffer()
        self.serial_port.write((command + str(param) + '\n').encode())
        # return status
        if self.serial_port.readline().decode()[0:2] == 'OK':
            return True
        else:
            return False

    # *** DEBUG *** #
    def debug_reset(self):
        self.serial_port.write('RE\n'.encode())

    def debug_slider(self):
        register_val = self.ui.horizontalSlider_debug.value()
        voltage = self.convert_dac_register(register_val)
        self.ui.label_debugdac.setText(str(register_val) + '(' + str(voltage)[0:5] + 'V)')
        if self.ui.checkBox_follow.checkState():
            self.debug_set()

    def debug_get(self):
        self.serial_port.write(('AD\n').encode())

        # Flush before connect
        self.serial_port.reset_input_buffer()
        income = self.serial_port.readline().decode()

        # Convert to Volt and display
        register_val = income[2:-2]
        voltage = self.convert_adc_register(int(register_val))
        self.ui.label_debugadc.setText(register_val + '(' + str(voltage) + 'V)')

    def debug_set(self):
        register_val = self.ui.horizontalSlider_debug.value()
        cs = self.ui.comboBox_debug.currentIndex() + 1
        param = cs * 100000 + register_val
        self.serial_port.write(('DA' + str(param) + '\n').encode())

    # *** COARSE APPROACH *** #
    def motor_forward_auto(self):
        self.motor_set_speed()
        step = self.ui.lineEdit_motorautolast.text()
        self.serial_port.write(('ME' + step + '\n').encode())

    def motor_backward_auto(self):
        self.motor_set_speed()
        step = self.ui.lineEdit_motorautolast.text()
        self.serial_port.write(('MR' + step + '\n').encode())

    def motor_set_speed(self):
        speed = self.ui.lineEdit_motordelay.text()
        self.serial_port.write(('MS' + speed + '\n').encode())

    def motor_stop(self):
        self.serial_port.write('MH\n'.encode())

    def motor_backward(self):
        if self.ui.pushButton_motorbackward.text() == 'BACKWARD':
            self.ui.pushButton_motorbackward.setText('STOP')
            self.motor_set_speed()
            index = self.ui.comboBox_motorselect.currentIndex()
            if index == 0:
                self.serial_port.write('MB\n'.encode())
            elif index == 1:
                self.serial_port.write('M11\n'.encode())
            elif index == 2:
                self.serial_port.write('M21\n'.encode())
            elif index == 3:
                self.serial_port.write('M31\n'.encode())
        else:
            self.motor_stop()
            self.ui.pushButton_motorbackward.setText('BACKWARD')

    def motor_forward(self):
        if self.ui.pushButton_motorforward.text() == 'FORWARD':
            self.ui.pushButton_motorforward.setText('STOP')
            self.motor_set_speed()
            index = self.ui.comboBox_motorselect.currentIndex()
            if index == 0:
                self.serial_port.write('MF\n'.encode())
            elif index == 1:
                self.serial_port.write('M1\n'.encode())
            elif index == 2:
                self.serial_port.write('M2\n'.encode())
            elif index == 3:
                self.serial_port.write('M3\n'.encode())

        else:
            self.ui.pushButton_motorforward.setText('FORWARD')
            self.motor_stop()

    # *** UART CONTROL *** #
    def uart_scan(self):
        # clear comboBox for previous result
        self.ui.comboBox_port.clear()
        self.ports = []
        ports = serial.tools.list_ports.comports()
        for ports, desc, _ in ports:
            self.ports.append(ports)
            self.ui.comboBox_port.addItem(desc)

    def uart_connect(self):
        # Get current selected comport and baud rate
        if not self.ports:
            pass
        else:
            if not self.is_connect:
                com_port = self.ports[self.ui.comboBox_port.currentIndex()]
                baud_rate = self.ui.comboBox_baudrate.currentText()
                # try to connect
                try:
                    self.serial_port.baudrate = baud_rate
                    self.serial_port.port = com_port
                    self.serial_port.open()
                    self.ui.pushButton_uartconnect.setText('STOP')
                    self.is_connect = True
                    self.ui.tabWidget.setEnabled(self.is_connect)

                    # set qt serial port
                    self.qt_serial_port.setBaudRate(int(baud_rate))
                    self.qt_serial_port.setPortName(com_port)

                except (OSError, serial.SerialException):
                    # Pop a message box to indicate that connect failed
                    QMessageBox.about(self, 'UART Connect', 'Uart Connect Failed!')

            else:
                self.serial_port.close()
                self.ui.pushButton_uartconnect.setText('CONNECT')
                self.is_connect = False
                self.ui.tabWidget.setEnabled(self.is_connect)


