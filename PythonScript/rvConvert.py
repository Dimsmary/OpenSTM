

class rvConverterHandle:
    def __init__(self, ui):
        self.ui = ui

    # def voltage_to_register_16bit(self, voltage):
    #     bias = self.ui.spinBox_settings_bias_16bit.value()
    #     register = int(((voltage + 10) / 20) * 65535) + bias
    #     return register
    #
    # def voltage_to_register_12bit(self, voltage):
    #     bias = self.ui.spinBox_settings_bias_12bit.value()
    #     register = int(((voltage + 10) / 20) * 4095)
    #     register = register << 4
    #     return register
    #
    # def voltage_to_register_z(self, voltage):
    #     bias = self.ui.spinBox_settings_bias_z.value()
    #     register = int(((voltage + 10) / 20) * 65535)
    #     register = register
    #     return register
    #
    # def voltage_to_register_x(self, voltage):
    #     bias = self.ui.spinBox_settings_bias_x.value()
    #     register = int(((voltage + 10) / 20) * 65535)
    #     register = register
    #     return register
    #
    # def voltage_to_register_y(self, voltage):
    #     bias = self.ui.spinBox_settings_bias_y.value()
    #     register = int(((voltage + 10) / 20) * 65535)
    #     register = register
    #     return register
    def voltage_to_register_12bit(self, voltage):
        register = int(((voltage / 1000 + 10) / 20) * 4095)
        register = register
        return register

    def voltage_to_register_16bit(self, voltage):
        register = int(((voltage / 1000 + 10) / 20) * 65535)
        register = register
        return register

    def register_to_voltage_16bit(self, register):
        ret = (register / 65535) * 20 - 10
        return ret * 1000

    def register_to_voltage_12bit(self, register):
        ret = (register / 4095) * 20 - 10
        return ret * 1000

    # output with mV
    def register_to_voltage_adc(self, register):
        bias = self.ui.spinBox_settings_bias_adc.value() / 1000
        full_range = 5.12 + bias
        half_range = full_range / 2
        ret = (register / 65535) * full_range - half_range
        return ret * 1000

    # pass in mV
    def voltage_to_register_adc(self, voltage):
        full_range = 5.12
        half_range = full_range / 2
        register = int(((voltage / 1000 + half_range) / full_range) * 65535)
        return register

    # calculate single step of DAC
    # return mV
    def single_step_DAC_16bit(self, register):
        return register * (20 / 65535) * 1000

