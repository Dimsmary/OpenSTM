from PyQt5 import QtCore, QtSerialPort, QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import time
from UartControllerCommand import UartControllerCommandHandle


class UartControllerHandle:
    def __init__(self, ui, debug):
        # Comment bottom line when running
        # self.ui = Ui_MainWindow()

        # Receive the Object from Main Controller
        self.ui = ui
        self.debug = debug

        # Create the QSerialPort Object
        self.port = QSerialPort()

        # Debug Label
        self.debug_label = "UART"

        # Creat UartCommand handle
        self.uart_controller_command = UartControllerCommandHandle(ui, self.port, self.debug)

        self.setup()

    def refresh_port(self):
        # clear the current port list
        self.ui.comboBox_UART_Port.clear()

        # update the available com port
        self.ui.comboBox_UART_Port.addItems([port.portName() for port in QSerialPortInfo().availablePorts()])

        # self.ui = Ui_MainWindow()
        self.debug.print(self.debug_label, 'Port Refreshed')

        # Connect receive function
        self.port.readyRead.connect(self.uart_controller_command.read_port)

    def setup(self):
        # add preset baud rate
        self.ui.comboBox_UART_BaudRate.addItems([
            '9600', '51200', '115200', '256000', '921600', '1200000'
        ])
        # select default baud rate
        self.ui.comboBox_UART_BaudRate.setCurrentIndex(3)

        # refresh the com port list
        self.refresh_port()

    def connect(self):
        # if port is connected
        if self.port.isOpen():
            self.port.close()
            self.ui.pushButton_UART_Connect.setText('Connect')
            self.debug.print(self.debug_label, 'Disconnected')

        # if port is not connect
        else:
            # get port name and baud rate from the comboBox
            port = self.ui.comboBox_UART_Port.currentText()
            baud_rate = self.ui.comboBox_UART_BaudRate.currentText()
            self.debug.print(self.debug_label, 'Connecting to port ' + port + ' with baud rate ' + baud_rate)

            # setting the port
            self.port.setPortName(port)
            self.port.setBaudRate(int(baud_rate))

            # begin connecting
            r = self.port.open(QtCore.QIODevice.ReadWrite)

            # if connect failed
            if not r:
                self.debug.print(self.debug_label, 'Connect Failed')

            # if connect success
            else:
                # Reset MCU
                self.port.setDataTerminalReady(False)
                self.port.setRequestToSend(True)
                time.sleep(0.1)
                self.port.setDataTerminalReady(False)
                self.port.setRequestToSend(False)
                self.debug.print(self.debug_label, 'Connected')
                self.ui.pushButton_UART_Connect.setText('Disconnect')
                # send welcome message
                time.sleep(0.5)
                self.port.write(('VERSI' + '00000').encode())
