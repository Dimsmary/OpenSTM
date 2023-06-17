from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from UartController import UartControllerHandle
from DebugGenerator import DebugGeneratorHandle
import os
import time


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        # Gui init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Debug Generator init
        self.debug = DebugGeneratorHandle(self.ui)

        # UART init
        self.uart = UartControllerHandle(self.ui, self.debug)

        # config file name
        self.config_file_name = 'config'

        # -- Config Prefix -- #
        self.baud_rate = 'BAUD_RATE'
        self.bias_16bit = 'BIAS_16Bit'
        self.bias_12bit = 'BIAS_12Bit'
        self.bias_DACZ = 'BIAS_DACZ'
        self.bias_DACX = 'BIAS_DACX'
        self.bias_DACY = 'BIAS_DACY'
        self.bias_ADC = 'BIAS_ADC'
        self.curve_FREQ = 'CURVE_FREQ'
        self.curve_RES = 'CURVE_RESISTANCE'
        self.curve_cBIAS = 'CURVE_CURRENT_BIAS'
        self.approach_KP = 'APPROACH_KP'
        self.approach_KI = 'APPROACH_KI'
        self.approach_KD = 'APPROACH_KD'
        self.bias_voltage = 'BIAS_VOLTAGE'
        self.set_point = 'SET_POINT'
        self.fw_step = 'APPROACH_FW_STEP'
        self.crash_point = 'CRASH_POINT'
        self.slider_amplitude = 'SLIER_AMPLITUDE'
        self.slider_slope = 'SLIDER_SLOPE'
        self.slider_fast_lim = 'SLIDER_CAP_FAST'
        self.slider_slow_lim = 'SLIDER_CAP_SLOW'
        self.curve_current_points = 'CURVE_CURRENT_POINTS'
        self.curve_pid_points = 'CURVE_PID_POINTS'
        self.curve_punch_points = 'CURVE_PUNCH_POINTS'
        self.curve_test_di_set_points = 'CURVE_TEST_DI_SET_POINTS'
        self.curve_test_di_increment = 'CURVE_TEST_DI_INCREMENT'
        self.curve_test_di_delay = 'CURVE_TEST_DI_DELAY'
        self.curve_test_bi_set_points = 'CURVE_TEST_BI_SET_POINTS'
        self.curve_test_bi_increment = 'CURVE_TEST_BI_INCREMENT'
        self.curve_test_bi_delay = 'CURVE_TEST_BI_DELAY'
        self.scan_line_target = 'SCAN_LINE_TARGET'
        self.scan_line_origin_x = 'SCAN_LINE_ORIGIN_X'
        self.scan_line_origin_y = 'SCAN_LINE_ORIGIN_Y'
        self.scan_line_delay = 'SCAN_LINE_DELAY'
        self.scan_line_inc = 'SCAN_LINE_INCREMENT'
        self.scan_line_pid_err = 'SCAN_LINE_PID_ERR_TH'
        self.scan_line_retract = 'SCAN_LINE_RETRACT'
        self.scan_size = 'SCAN_SIZE'
        self.scan_origin_x = 'SCAN_ORIGIN_X'
        self.scan_origin_y = 'SCAN_ORIGIN_Y'
        self.scan_delay = 'SCAN_DELAY'
        self.scan_increment = 'SCAN_INCREMENT'
        self.scan_pid_err = 'SCAN_PID_ERROR'
        self.scan_retract = 'SCAN_RETRACT'

        # Slot Binding
        self.setup_control()

    def config_formatting(self, key, value):
        return key + '=' + str(value) + '\n'

    # -- get the parameters on the GUI -- #
    def update_config(self):
        # -> UART Config
        config_s = self.config_formatting(self.baud_rate,
                                          self.ui.comboBox_UART_BaudRate.currentIndex())

        # -> BIAS config
        # 16bit dac
        config_s = config_s + self.config_formatting(self.bias_16bit,
                                                     self.ui.spinBox_settings_bias_16bit.value())
        # 12bit dac
        config_s = config_s + self.config_formatting(self.bias_12bit,
                                                     self.ui.spinBox_settings_bias_12bit.value())
        # DAC Z
        config_s = config_s + self.config_formatting(self.bias_DACZ,
                                                     self.ui.spinBox_settings_bias_z.value())
        # DAC X
        config_s = config_s + self.config_formatting(self.bias_DACX,
                                                     self.ui.spinBox_settings_bias_x.value())
        # DAC Y
        config_s = config_s + self.config_formatting(self.bias_DACX,
                                                     self.ui.spinBox_settings_bias_y.value())
        # ADC
        config_s = config_s + self.config_formatting(self.bias_ADC,
                                                     self.ui.spinBox_settings_bias_adc.value())

        # -> Curve config
        config_s = config_s + self.config_formatting(self.curve_FREQ,
                                                     self.ui.spinBox_settings_curvehz.value())
        config_s = config_s + self.config_formatting(self.curve_RES,
                                                     self.ui.spinBox_settings_curveres.value())
        config_s = config_s + self.config_formatting(self.curve_cBIAS,
                                                     self.ui.spinBox_settings_curvecurrent.value())
        config_s = config_s + self.config_formatting(self.curve_current_points,
                                                     self.ui.spinBox_curve_current_points.value())
        config_s = config_s + self.config_formatting(self.curve_pid_points,
                                                     self.ui.spinBox_curve_pid_points.value())
        config_s = config_s + self.config_formatting(self.curve_punch_points,
                                                     self.ui.spinBox_curve_punch_points.value())



        # -> Approach Config
        config_s = config_s + self.config_formatting(self.approach_KP,
                                                     self.ui.lineEdit_settings_kp.text())
        config_s = config_s + self.config_formatting(self.approach_KI,
                                                     self.ui.lineEdit_settings_ki.text())
        config_s = config_s + self.config_formatting(self.approach_KD,
                                                     self.ui.lineEdit_settings_kd.text())
        config_s = config_s + self.config_formatting(self.bias_voltage,
                                                     self.ui.spinBox_settings_biasVoltage.value())
        config_s = config_s + self.config_formatting(self.set_point,
                                                     self.ui.lineEdit_approach_setpoint.text())
        config_s = config_s + self.config_formatting(self.fw_step,
                                                     self.ui.spinBox_approach_fw.value())
        config_s = config_s + self.config_formatting(self.crash_point,
                                                     self.ui.lineEdit_crash.text())
        config_s = config_s + self.config_formatting(self.slider_amplitude,
                                                     self.ui.spinBox_approach_sliderA.value())
        config_s = config_s + self.config_formatting(self.slider_slope,
                                                     self.ui.spinBox_approach_siderSL.value())
        config_s = config_s + self.config_formatting(self.slider_fast_lim,
                                                     self.ui.spinBox_approach_capFast.value())
        config_s = config_s + self.config_formatting(self.slider_slow_lim,
                                                     self.ui.spinBox_approach_capSlow.value())

        # -> Curve Test
        config_s = config_s + self.config_formatting(self.curve_test_di_delay,
                                                     self.ui.spinBox_curve_difreq.value())
        config_s = config_s + self.config_formatting(self.curve_test_di_increment,
                                                     self.ui.spinBox_curve_diinc.value())
        config_s = config_s + self.config_formatting(self.curve_test_di_set_points,
                                                     self.ui.spinBox_curve_distop.value())

        config_s = config_s + self.config_formatting(self.curve_test_bi_delay,
                                                     self.ui.spinBox_curve_bfreq.value())
        config_s = config_s + self.config_formatting(self.curve_test_bi_increment,
                                                     self.ui.spinBox_curve_binc.value())
        config_s = config_s + self.config_formatting(self.curve_test_bi_set_points,
                                                     self.ui.spinBox_curve_bstop.value())

        # -> Scan
        # line test
        config_s = config_s + self.config_formatting(self.scan_line_target,
                                                     self.ui.spinBox_scan_Ttarget.value())
        config_s = config_s + self.config_formatting(self.scan_line_origin_x,
                                                     self.ui.spinBox_scan_origin_Tx.value())
        config_s = config_s + self.config_formatting(self.scan_line_origin_y,
                                                     self.ui.spinBox_scan_origin_Ty.value())
        config_s = config_s + self.config_formatting(self.scan_line_delay,
                                                     self.ui.spinBox_scan_freq_2.value())
        config_s = config_s + self.config_formatting(self.scan_line_inc,
                                                     self.ui.spinBox_scan_Tinc.value())
        config_s = config_s + self.config_formatting(self.scan_line_pid_err,
                                                     self.ui.spinBox_scan_line_piderr.value())
        config_s = config_s + self.config_formatting(self.scan_line_retract,
                                                     self.ui.spinBox_scan_line_retract.value())

        # image scan
        config_s = config_s + self.config_formatting(self.scan_size,
                                                     self.ui.spinBox_scan_size.value())
        config_s = config_s + self.config_formatting(self.scan_origin_x,
                                                     self.ui.spinBox_scan_origin_x.value())
        config_s = config_s + self.config_formatting(self.scan_origin_y,
                                                     self.ui.spinBox_scan_origin_y.value())
        config_s = config_s + self.config_formatting(self.scan_delay,
                                                     self.ui.spinBox_scan_freq.value())
        config_s = config_s + self.config_formatting(self.scan_increment,
                                                     self.ui.spinBox_scan_inc.value())
        config_s = config_s + self.config_formatting(self.scan_pid_err,
                                                     self.ui.spinBox_scan_piderr.value())
        config_s = config_s + self.config_formatting(self.scan_retract,
                                                     self.ui.spinBox_scan_retract.value())


        with open(self.config_file_name, "w") as f:
            f.write(config_s)

    # read configure file
    def read_config(self):
        try:
            with open(self.config_file_name, 'r') as f:
                for i in f:
                    splited = i[:-1].split('=')
                    key = splited[0]
                    value = splited[1]

                    # -> uart
                    if key == self.baud_rate:
                        self.ui.comboBox_UART_BaudRate.setCurrentIndex(int(value))

                    # -> BIAS
                    elif key == self.bias_16bit:
                        self.ui.spinBox_settings_bias_16bit.setValue(int(value))
                    elif key == self.bias_12bit:
                        self.ui.spinBox_settings_bias_12bit.setValue(int(value))
                    elif key == self.bias_DACZ:
                        self.ui.spinBox_settings_bias_z.setValue(int(value))
                    elif key == self.bias_DACX:
                        self.ui.spinBox_settings_bias_x.setValue(int(value))
                    elif key == self.bias_DACY:
                        self.ui.spinBox_settings_bias_y.setValue(int(value))
                    elif key == self.bias_ADC:
                        self.ui.spinBox_settings_bias_adc.setValue(int(value))
                    elif key == self.curve_FREQ:
                        self.ui.spinBox_settings_curvehz.setValue(int(value))
                    elif key == self.curve_RES:
                        self.ui.spinBox_settings_curveres.setValue(int(value))
                    elif key == self.curve_cBIAS:
                        self.ui.spinBox_settings_curvecurrent.setValue(int(value))
                    elif key == self.approach_KP:
                        self.ui.lineEdit_settings_kp.setText(value)
                    elif key == self.approach_KI:
                        self.ui.lineEdit_settings_ki.setText(value)
                    elif key == self.approach_KD:
                        self.ui.lineEdit_settings_kd.setText(value)
                    elif key == self.bias_voltage:
                        self.ui.spinBox_settings_biasVoltage.setValue(int(value))
                    elif key == self.set_point:
                        self.ui.lineEdit_approach_setpoint.setText(value)
                    elif key == self.fw_step:
                        self.ui.spinBox_approach_fw.setValue(int(value))
                    elif key == self.crash_point:
                        self.ui.lineEdit_crash.setText(value)
                    elif key == self.slider_amplitude:
                        self.ui.spinBox_approach_sliderA.setValue(int(value))
                    elif key == self.slider_slope:
                        self.ui.spinBox_approach_siderSL.setValue(int(value))
                    elif key == self.slider_fast_lim:
                        self.ui.spinBox_approach_capFast.setValue(int(value))
                    elif key == self.slider_slow_lim:
                        self.ui.spinBox_approach_capSlow.setValue(int(value))
                    elif key == self.curve_current_points:
                        self.ui.spinBox_curve_current_points.setValue(int(value))
                    elif key == self.curve_pid_points:
                        self.ui.spinBox_curve_pid_points.setValue(int(value))
                    elif key == self.curve_punch_points:
                        self.ui.spinBox_curve_punch_points.setValue(int(value))
                    elif key == self.curve_test_di_delay:
                        self.ui.spinBox_curve_difreq.setValue(int(value))
                    elif key == self.curve_test_di_set_points:
                        self.ui.spinBox_curve_distop.setValue(int(value))
                    elif key == self.curve_test_di_increment:
                        self.ui.spinBox_curve_diinc.setValue(int(value))
                    elif key == self.curve_test_bi_delay:
                        self.ui.spinBox_curve_bfreq.setValue(int(value))
                    elif key == self.curve_test_bi_set_points:
                        self.ui.spinBox_curve_bstop.setValue(int(value))
                    elif key == self.curve_test_bi_increment:
                        self.ui.spinBox_curve_binc.setValue(int(value))
                    elif key == self.scan_line_target:
                        self.ui.spinBox_scan_Ttarget.setValue(int(value))
                    elif key == self.scan_line_origin_x:
                        self.ui.spinBox_scan_origin_Tx.setValue(int(value))
                    elif key == self.scan_line_origin_y:
                        self.ui.spinBox_scan_origin_Ty.setValue(int(value))
                    elif key == self.scan_line_delay:
                        self.ui.spinBox_scan_freq_2.setValue(int(value))
                    elif key == self.scan_line_inc:
                        self.ui.spinBox_scan_Tinc.setValue(int(value))
                    elif key == self.scan_line_pid_err:
                        self.ui.spinBox_scan_line_piderr.setValue(int(value))
                    elif key == self.scan_size:
                        self.ui.spinBox_scan_size.setValue(int(value))
                    elif key == self.scan_origin_x:
                        self.ui.spinBox_scan_origin_x.setValue(int(value))
                    elif key == self.scan_origin_y:
                        self.ui.spinBox_scan_origin_y.setValue(int(value))
                    elif key == self.scan_delay:
                        self.ui.spinBox_scan_freq.setValue(int(value))
                    elif key == self.scan_increment:
                        self.ui.spinBox_scan_inc.setValue(int(value))
                    elif key == self.scan_pid_err:
                        self.ui.spinBox_scan_piderr.setValue(int(value))
                    elif key == self.scan_retract:
                        self.ui.spinBox_scan_retract.setValue(int(value))
                    elif key == self.scan_line_retract:
                        self.ui.spinBox_scan_line_retract.setValue(int(value))

        except IOError:
            self.update_config()

    # save config when quitting
    def closeEvent(self, event):
        self.update_config()

    # load the config and binding the item
    def setup_control(self):
        self.read_config()

        # -> Uart Controller Binding
        self.ui.pushButton_UART_Refresh.clicked.connect(self.uart.refresh_port)
        self.ui.pushButton_UART_Connect.clicked.connect(self.uart.connect)
        self.ui.pushButton_debug_clear.clicked.connect(self.text_browser_clear)
        self.ui.pushButton_debug_save.clicked.connect(self.text_browser_save)

        # -> Manual Binding
        self.ui.pushButton_manual_reset.clicked.connect(self.uart.uart_controller_command.manual_handle.reset)
        self.ui.horizontalSlider_manual_dacz.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.slider_dac_z)
        self.ui.pushButton_manual_dacz.clicked.connect(self.uart.uart_controller_command.manual_handle.button_dac_z)
        self.ui.spinBox_manual_dacz_register.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.spin_box_register_z)

        self.ui.horizontalSlider_manual_dacx.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.slider_dac_x)
        self.ui.pushButton_manual_dacx.clicked.connect(self.uart.uart_controller_command.manual_handle.button_dac_x)
        self.ui.spinBox_manual_dacx_register.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.spin_box_register_x)

        self.ui.horizontalSlider_manual_dacy.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.slider_dac_y)
        self.ui.pushButton_manual_dacy.clicked.connect(self.uart.uart_controller_command.manual_handle.button_dac_y)
        self.ui.spinBox_manual_dacy_register.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.spin_box_register_y)

        self.ui.horizontalSlider_manual_dac12b.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.slider_dac_12b)
        self.ui.pushButton_manual_dac12b.clicked.connect(self.uart.uart_controller_command.manual_handle.button_dac_12b)
        self.ui.spinBox_manual_dac12b_register.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.spin_box_register_12b)

        self.ui.horizontalSlider_manual_dac16b.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.slider_dac_16b)
        self.ui.pushButton_manual_dac16b.clicked.connect(self.uart.uart_controller_command.manual_handle.button_dac_16b)
        self.ui.spinBox_manual_dac16b_register.valueChanged.connect(
            self.uart.uart_controller_command.manual_handle.spin_box_register_16b)

        # -> Curve
        self.ui.checkBox_curve.clicked.connect(self.uart.uart_controller_command.curve_handle.auto_update)

        # -> APPROACH
        self.ui.pushButton_approach.clicked.connect(self.uart.uart_controller_command.approach_handle.approach)
        self.ui.pushButton_approach_fw.clicked.connect(self.uart.uart_controller_command.approach_handle.forward)
        self.ui.pushButton_retract.clicked.connect(self.uart.uart_controller_command.approach_handle.retract)

        # -> Curve Scan
        self.ui.pushButton_curve_dibegin.clicked.connect(self.uart.uart_controller_command.curve_scan_handle.di_begin)
        self.ui.pushButton_curve_bbegin.clicked.connect(self.uart.uart_controller_command.curve_scan_handle.bias_begin)
        self.ui.spinBox_curve_diinc.valueChanged.connect(self.uart.uart_controller_command.curve_scan_handle.di_inc_switch)
        self.ui.spinBox_curve_difreq.valueChanged.connect(self.uart.uart_controller_command.curve_scan_handle.di_freq_switch)
        self.ui.spinBox_curve_binc.valueChanged.connect(self.uart.uart_controller_command.curve_scan_handle.bi_inc_switch)
        self.ui.spinBox_curve_bfreq.valueChanged.connect(self.uart.uart_controller_command.curve_scan_handle.bi_freq_switch)
        self.ui.pushButton_curve_save.clicked.connect(self.uart.uart_controller_command.curve_scan_handle.save_data)

        # call function to update the message
        self.uart.uart_controller_command.curve_scan_handle.di_inc_switch()
        self.uart.uart_controller_command.curve_scan_handle.di_freq_switch()
        self.uart.uart_controller_command.curve_scan_handle.bi_inc_switch()
        self.uart.uart_controller_command.curve_scan_handle.bi_freq_switch()

        # -> IMAGE SCAN!
        self.ui.pushButton_scan_Tbegin.clicked.connect(self.uart.uart_controller_command.scan_handle.line_test_begin)
        self.ui.pushButton_scan_line_save.clicked.connect(self.uart.uart_controller_command.scan_handle.line_save)
        self.ui.pushButton_scan_begin.clicked.connect(self.uart.uart_controller_command.scan_handle.scan_begin)
        self.ui.pushButton_scan_image_save.clicked.connect(self.uart.uart_controller_command.scan_handle.image_save)


        # -> Init some GUI
        path = os.getcwd() + '\\CurveTestData'
        self.ui.lineEdit_curve_path.setText(path)

    def text_browser_clear(self):
        self.ui.textBrowser.clear()

    def text_browser_save(self):
        filename = time.strftime('log/' + '%Y-%m-%d %H-%M-%S', time.localtime()) + '-log.txt'
        self.uart.debug.print('Debug', 'Debug file saved: ' + filename)
        with open(filename, 'w') as yourFile:
            yourFile.write(str(self.ui.textBrowser.toPlainText()))














