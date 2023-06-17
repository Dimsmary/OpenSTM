
class CommandSendHandle:
    def __init__(self, port):
        self.port = port

    def data_format(self, val):
        return ('%05d' % (val, )) + '\r\n'

    def send_to_dac_16bit(self, val):
        self.port.write(("SETD0" + self.data_format(val)).encode())

    def send_to_dac_z(self, val):
        self.port.write(("SETD1" + self.data_format(val)).encode())

    def send_to_dac_y(self, val):
        self.port.write(("SETD2" + self.data_format(val)).encode())

    def send_to_dac_x(self, val):
        self.port.write(("SETD3" + self.data_format(val)).encode())

    def send_to_dac_12bit(self, val):
        val = val << 4
        self.port.write(("SETD4" + self.data_format(val)).encode())

    def send_get_adc(self):
        self.port.write("GETAD00000\r\n".encode())

    def send_to_curve(self, val):
        self.port.write(("CURVE" + self.data_format(val)).encode())

    def send_to_approach_begin(self):
        self.port.write(("APPGO" + self.data_format(0)).encode())

    def send_to_approach_stop(self):
        self.port.write(("APPST" + self.data_format(0)).encode())

    def send_to_approach_target(self, value):
        self.port.write(("APPTA" + self.data_format(value)).encode())

    def send_to_approach_register(self, value):
        self.port.write(("APPRE" + self.data_format(value)).encode())

    def send_to_approach_kp(self, value):
        self.port.write(("APPS0" + self.data_format(value)).encode())

    def send_to_approach_ki(self, value):
        self.port.write(("APPS1" + self.data_format(value)).encode())

    def send_to_approach_kd(self, value):
        self.port.write(("APPS2" + self.data_format(value)).encode())

    def send_to_approach_step(self, value):
        self.port.write(("APPSS" + self.data_format(value)).encode())

    def send_to_approach_crash(self, value):
        self.port.write(("APPCA" + self.data_format(value)).encode())

    def send_to_approach_amplitude(self, value):
        self.port.write(("APPAM" + self.data_format(value)).encode())

    def send_to_approach_slope(self, value):
        self.port.write(("APPSO" + self.data_format(value)).encode())

    def send_to_approach_cap_fast(self, value):
        self.port.write(("APPFA" + self.data_format(value)).encode())

    def send_to_approach_cap_slow(self, value):
        self.port.write(("APPSL" + self.data_format(value)).encode())

    def send_to_approach_bias(self, value):
        self.port.write(("APPBI" + self.data_format(value)).encode())

    def send_to_curve_test_register(self, value):
        self.port.write(("CTREG" + self.data_format(value)).encode())

    def send_to_curve_test_di_stop(self, value):
        self.port.write(("CTDST" + self.data_format(value)).encode())

    def send_to_curve_test_di_inc(self, value):
        self.port.write(("CTDIN" + self.data_format(value)).encode())

    def send_to_curve_test_delay(self, value):
        self.port.write(("CTDLY" + self.data_format(value)).encode())

    def send_to_curve_test_reset(self, value):
        self.port.write(("CTRST" + self.data_format(value)).encode())

    def send_to_curve_test_bi_stop(self, value):
        self.port.write(("CTBST" + self.data_format(value)).encode())

    def send_to_curve_test_bi_start(self, value):
        self.port.write(("CTBSS" + self.data_format(value)).encode())

    def send_to_curve_test_bi_inc(self, value):
        self.port.write(("CTBIN" + self.data_format(value)).encode())

    def send_to_scan_reg(self, value):
        self.port.write(("SCREG" + self.data_format(value)).encode())

    def send_to_scan_delay(self, value):
        self.port.write(("SCDLY" + self.data_format(value)).encode())

    def send_to_scan_line_target(self, value):
        self.port.write(("SCLTA" + self.data_format(value)).encode())

    def send_to_scan_line_origin_x(self, value):
        self.port.write(("SCLTX" + self.data_format(value)).encode())

    def send_to_scan_line_origin_y(self, value):
        self.port.write(("SCLTY" + self.data_format(value)).encode())

    def send_to_scan_line_inc(self, value):
        self.port.write(("SCLIN" + self.data_format(value)).encode())

    def send_to_scan_line_direction(self, value):
        self.port.write(("SCLDI" + self.data_format(value)).encode())

    def send_to_scan_ccch_mode(self, value):
        self.port.write(("SCCMO" + self.data_format(value)).encode())

    # scan parameters
    def send_to_scan_x_begin(self, value):
        self.port.write(("SCXBE" + self.data_format(value)).encode())

    def send_to_scan_x_end(self, value):
        self.port.write(("SCXEN" + self.data_format(value)).encode())

    def send_to_scan_y_begin(self, value):
        self.port.write(("SCYBE" + self.data_format(value)).encode())

    def send_to_scan_y_end(self, value):
        self.port.write(("SCYEN" + self.data_format(value)).encode())

    def send_to_scan_inc(self, value):
        self.port.write(("SCINC" + self.data_format(value)).encode())

    def send_to_scan_cc_inc(self, value):
        self.port.write(("SCCIN" + self.data_format(value)).encode())

    def send_to_scan_mode(self, value):
        self.port.write(("SCMOD" + self.data_format(value)).encode())

    def send_to_scan_ch(self, value):
        self.port.write(("SCICH" + self.data_format(value)).encode())

    def send_to_scan_retract(self, value):
        self.port.write(("SCRET" + self.data_format(value)).encode())

    def send_to_scan_ez_switch(self, value):
        self.port.write(("SCEZS" + self.data_format(value)).encode())