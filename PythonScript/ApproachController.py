import time


class ApproachControllerHandle:
    def __init__(self, ui, port, debug, command_send, rv_converter):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.command_send = command_send
        self.rv_converter = rv_converter

        self.is_approach = False

    def approach(self):
        if self.is_approach:
            # send command to mcu
            self.command_send.send_to_approach_register(0)
            # set progress bar value
            self.ui.progressBar.setValue(0)
            self.ui.label_approach_status.setText('IDLE')
            self.ui.pushButton_approach.setText('Approach')
            self.is_approach = False
        else:
            # Preprocess the data
            set_point = float(self.ui.lineEdit_approach_setpoint.text())
            crash = int(self.ui.lineEdit_crash.text())
            kp = float(self.ui.lineEdit_settings_kp.text()) * 10000
            ki = float(self.ui.lineEdit_settings_ki.text()) * 10000
            kd = float(self.ui.lineEdit_settings_kd.text()) * 10000
            bias = self.ui.spinBox_settings_biasVoltage.value()
            cap_fast = self.ui.spinBox_approach_capFast.value()
            cap_slow = self.ui.spinBox_approach_capSlow.value()

            # set slider amplitude and slope
            self.command_send.send_to_approach_amplitude(self.ui.spinBox_approach_sliderA.value())
            self.command_send.send_to_approach_slope(self.ui.spinBox_approach_siderSL.value())

            # set slider mode switch limitation
            # fast_register = self.rv_converter.voltage_to_register_adc(cap_fast)
            self.command_send.send_to_approach_cap_fast(cap_fast)
            # slow_register = self.rv_converter.voltage_to_register_adc(cap_slow)
            self.command_send.send_to_approach_cap_slow(cap_slow)

            # set bias voltage
            bias_register = self.rv_converter.voltage_to_register_16bit(bias)
            self.command_send.send_to_approach_bias(bias_register)

            # send target voltage
            voltage = set_point
            target_register = self.rv_converter.voltage_to_register_adc(voltage)
            self.command_send.send_to_approach_target(target_register)

            # send PID parameters
            self.command_send.send_to_approach_kp(kp)
            self.command_send.send_to_approach_ki(ki)
            self.command_send.send_to_approach_kd(kd)

            # send crash voltage
            voltage = crash
            target_register = self.rv_converter.voltage_to_register_adc(voltage)
            self.command_send.send_to_approach_crash(target_register)

            # set status begin
            self.command_send.send_to_approach_register(1)

            self.is_approach = True
            self.ui.pushButton_approach.setText('Stop')

            # set progress bar value
            self.ui.progressBar.setValue(25)
            self.ui.label_approach_status.setText('FAST')

    def forward(self):
        self.command_send.send_to_approach_amplitude(self.ui.spinBox_approach_sliderA.value())
        self.command_send.send_to_approach_slope(self.ui.spinBox_approach_siderSL.value())
        step = self.ui.spinBox_approach_fw.value()
        self.command_send.send_to_approach_step(step)
        self.command_send.send_to_approach_register(2)

    def retract(self):
        self.command_send.send_to_approach_amplitude(self.ui.spinBox_approach_sliderA.value())
        self.command_send.send_to_approach_slope(self.ui.spinBox_approach_siderSL.value())
        step = self.ui.spinBox_approach_fw.value()
        self.command_send.send_to_approach_step(step)
        self.command_send.send_to_approach_register(3)


