class ManualControllerHandle:
    def __init__(self, ui, port, debug, command_send, rv_converter):
        self.ui = ui
        self.port = port
        self.debug = debug
        self.command_send = command_send
        self.rv_converter = rv_converter

    # set all DACs to 0v
    def reset(self):
        self.command_send.send_to_dac_16bit(self.rv_converter.voltage_to_register_16bit(0))
        self.command_send.send_to_dac_12bit(self.rv_converter.voltage_to_register_12bit(0))
        self.command_send.send_to_dac_z(self.rv_converter.voltage_to_register_16bit(0))
        self.command_send.send_to_dac_x(self.rv_converter.voltage_to_register_16bit(0))
        self.command_send.send_to_dac_y(self.rv_converter.voltage_to_register_16bit(0))

    # -> DACZ
    # slider control
    def slider_dac_z(self):
        new_value = self.ui.horizontalSlider_manual_dacz.value()
        self.ui.spinBox_manual_dacz_register.setValue(new_value)
        self.ui.lcdNumber_manual_dacz_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))
        # if check box is check then update the dac immediately
        if self.ui.checkBox_manual_dacz.isChecked():
            self.command_send.send_to_dac_z(new_value)

    def spin_box_register_z(self):
        new_value = self.ui.spinBox_manual_dacz_register.value()
        self.ui.horizontalSlider_manual_dacz.setValue(new_value)
        self.ui.lcdNumber_manual_dacz_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))

    # button control
    def button_dac_z(self):
        new_value = self.ui.spinBox_manual_dacz_register.value()
        self.command_send.send_to_dac_z(new_value)

    # -> DACX
    # slider control
    def slider_dac_x(self):
        new_value = self.ui.horizontalSlider_manual_dacx.value()
        self.ui.spinBox_manual_dacx_register.setValue(new_value)
        self.ui.lcdNumber_manual_dacx_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))
        # if check box is check then update the dac immediately
        if self.ui.checkBox_manual_dacx.isChecked():
            self.command_send.send_to_dac_x(new_value)

    def spin_box_register_x(self):
        new_value = self.ui.spinBox_manual_dacx_register.value()
        self.ui.horizontalSlider_manual_dacx.setValue(new_value)
        self.ui.lcdNumber_manual_dacx_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))

    # button control
    def button_dac_x(self):
        new_value = self.ui.spinBox_manual_dacx_register.value()
        self.command_send.send_to_dac_x(new_value)

    # -> DACY
    # slider control
    def slider_dac_y(self):
        new_value = self.ui.horizontalSlider_manual_dacy.value()
        self.ui.spinBox_manual_dacy_register.setValue(new_value)
        self.ui.lcdNumber_manual_dacy_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))
        # if check box is check then update the dac immediately
        if self.ui.checkBox_manual_dacy.isChecked():
            self.command_send.send_to_dac_y(new_value)

    def spin_box_register_y(self):
        new_value = self.ui.spinBox_manual_dacy_register.value()
        self.ui.horizontalSlider_manual_dacy.setValue(new_value)
        self.ui.lcdNumber_manual_dacy_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))

    # button control
    def button_dac_y(self):
        new_value = self.ui.spinBox_manual_dacy_register.value()
        self.command_send.send_to_dac_y(new_value)

    # -> DAC12b
    # slider control
    def slider_dac_12b(self):
        new_value = self.ui.horizontalSlider_manual_dac12b.value()
        self.ui.spinBox_manual_dac12b_register.setValue(new_value)
        self.ui.lcdNumber_manual_dac12b_voltage_2.display(self.rv_converter.register_to_voltage_12bit(new_value))
        # if check box is check then update the dac immediately
        if self.ui.checkBox_manual_dac12b.isChecked():
            self.command_send.send_to_dac_12bit(new_value)

    def spin_box_register_12b(self):
        new_value = self.ui.spinBox_manual_dac12b_register.value()
        self.ui.horizontalSlider_manual_dac12b.setValue(new_value)
        self.ui.lcdNumber_manual_dac12b_voltage_2.display(self.rv_converter.register_to_voltage_12bit(new_value))

        # button control

    def button_dac_12b(self):
        new_value = self.ui.spinBox_manual_dac12b_register.value()
        self.command_send.send_to_dac_12bit(new_value)

    # -> DAC16b
    # slider control
    def slider_dac_16b(self):
        new_value = self.ui.horizontalSlider_manual_dac16b.value()
        self.ui.spinBox_manual_dac16b_register.setValue(new_value)
        self.ui.lcdNumber_manual_dac16b_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))
        # if check box is check then update the dac immediately
        if self.ui.checkBox_manual_dac16b.isChecked():
            self.command_send.send_to_dac_16bit(new_value)

    def spin_box_register_16b(self):
        new_value = self.ui.spinBox_manual_dac16b_register.value()
        self.ui.horizontalSlider_manual_dac16b.setValue(new_value)
        self.ui.lcdNumber_manual_dac16b_voltage_2.display(self.rv_converter.register_to_voltage_16bit(new_value))

        # button control

    def button_dac_16b(self):
        new_value = self.ui.spinBox_manual_dac16b_register.value()
        self.command_send.send_to_dac_16bit(new_value)


