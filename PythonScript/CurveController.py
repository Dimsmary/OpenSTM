import pyqtgraph as pg


class CurveControllerHandle:
    def __init__(self, ui, port, debug, command_send, rv_converter):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.command_send = command_send
        self.rv_converter = rv_converter

        # -- setting up curve module for Tunneling Current -- #
        self.graph_length = self.ui.spinBox_curve_current_points.value()
        self.graph_x = list(range(self.graph_length))
        self.graph_y = [0] * self.graph_length
        pen = pg.mkPen(color=(255, 162, 41))
        self.line = self.ui.graphWidget.plot(self.graph_x, self.graph_y, pen=pen)

        # setting up curve module for PID Curve -- #
        self.graph_length_pid = self.ui.spinBox_curve_pid_points.value()
        self.graph_x_pid = list(range(self.graph_length_pid))
        self.graph_y_pid = [0] * self.graph_length_pid
        pen2 = pg.mkPen(color=(0, 161, 195))
        self.line2 = self.ui.graphWidget_2.plot(self.graph_x_pid, self.graph_y_pid, pen=pen2)

        # -- setting up curve module for Punch Curve -- #
        self.graph_length_punch = self.ui.spinBox_curve_punch_points.value()
        self.graph_x_punch = list(range(self.graph_length_punch))
        self.graph_y_punch = [0] * self.graph_length_punch
        pen3 = pg.mkPen(color=(146, 1, 194))
        self.line3 = self.ui.graphWidget_3.plot(self.graph_x_punch, self.graph_y_punch, pen=pen3)

        # Set Style of all graph
        self.ui.graphWidget.showGrid(x=True, y=True)
        self.ui.graphWidget.setBackground('w')
        self.ui.graphWidget_2.showGrid(x=True, y=True)
        self.ui.graphWidget_2.setBackground('w')
        self.ui.graphWidget_3.showGrid(x=True, y=True)
        self.ui.graphWidget_3.setBackground('w')

    def auto_update(self):
        # get frequency from GUI
        freq = self.ui.spinBox_settings_curvehz.value()

        # transmit the command
        if self.ui.checkBox_curve.isChecked():
            param = 32768 + 1000/freq
            self.command_send.send_to_curve(int(param))
        else:
            param = 1000
            self.command_send.send_to_curve(param)

    def tunneling_update(self, value):
        # get feedback resistance from GUI
        resistance = self.ui.spinBox_settings_curveres.value()
        # convert register to voltage
        voltage = self.rv_converter.register_to_voltage_adc(value)

        # update lcd display
        self.ui.lcdNumber_curve_voltage.display(voltage)
        self.ui.lcdNumber_curve_resister.display(value)

        # calculate the tunneling current
        current = voltage * resistance / 10000 + self.ui.spinBox_settings_curvecurrent.value()/10
        self.ui.lcdNumber_curve_current.display(current)

        # update graph
        self.graph_x = self.graph_x[1:]
        self.graph_x.append(self.graph_x[-1] + 1)
        self.graph_y = self.graph_y[1:]
        self.graph_y.append(current)
        self.line.setData(self.graph_x, self.graph_y)

    def pid_update(self, value):
        # update graph
        self.graph_x_pid = self.graph_x_pid[1:]
        self.graph_x_pid.append(self.graph_x_pid[-1] + 1)
        self.graph_y_pid = self.graph_y_pid[1:]
        self.graph_y_pid.append(value)
        self.line2.setData(self.graph_x_pid, self.graph_y_pid)

    def punch_update(self, value):
        # update graph
        self.graph_x_punch = self.graph_x_punch[1:]
        self.graph_x_punch.append(self.graph_x_punch[-1] + 1)
        self.graph_y_punch = self.graph_y_punch[1:]
        self.graph_y_punch.append(value)
        self.line3.setData(self.graph_x_punch, self.graph_y_punch)

