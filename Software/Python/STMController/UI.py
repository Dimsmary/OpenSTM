# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 728)
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("open_stm.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 771, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_motorforward = QtWidgets.QPushButton(self.tab)
        self.pushButton_motorforward.setGeometry(QtCore.QRect(140, 130, 121, 31))
        self.pushButton_motorforward.setObjectName("pushButton_motorforward")
        self.pushButton_motorbackward = QtWidgets.QPushButton(self.tab)
        self.pushButton_motorbackward.setGeometry(QtCore.QRect(300, 130, 121, 31))
        self.pushButton_motorbackward.setObjectName("pushButton_motorbackward")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(140, 80, 91, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit_motordelay = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_motordelay.setGeometry(QtCore.QRect(240, 80, 181, 31))
        self.lineEdit_motordelay.setObjectName("lineEdit_motordelay")
        self.comboBox_motorselect = QtWidgets.QComboBox(self.tab)
        self.comboBox_motorselect.setGeometry(QtCore.QRect(460, 80, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_motorselect.setFont(font)
        self.comboBox_motorselect.setObjectName("comboBox_motorselect")
        self.lineEdit_motorautolast = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_motorautolast.setGeometry(QtCore.QRect(240, 200, 181, 31))
        self.lineEdit_motorautolast.setObjectName("lineEdit_motorautolast")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(140, 200, 91, 31))
        self.label_15.setObjectName("label_15")
        self.pushButton_motorbackward_auto = QtWidgets.QPushButton(self.tab)
        self.pushButton_motorbackward_auto.setGeometry(QtCore.QRect(300, 250, 121, 31))
        self.pushButton_motorbackward_auto.setObjectName("pushButton_motorbackward_auto")
        self.pushButton_motorforward_auto = QtWidgets.QPushButton(self.tab)
        self.pushButton_motorforward_auto.setGeometry(QtCore.QRect(140, 250, 121, 31))
        self.pushButton_motorforward_auto.setObjectName("pushButton_motorforward_auto")
        self.pushButton_releasemotor = QtWidgets.QPushButton(self.tab)
        self.pushButton_releasemotor.setGeometry(QtCore.QRect(460, 250, 121, 31))
        self.pushButton_releasemotor.setObjectName("pushButton_releasemotor")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(40, 150, 101, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_currentlimit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_currentlimit.setGeometry(QtCore.QRect(150, 100, 113, 31))
        self.lineEdit_currentlimit.setObjectName("lineEdit_currentlimit")
        self.lineEdit_crashlimit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_crashlimit.setGeometry(QtCore.QRect(150, 140, 113, 31))
        self.lineEdit_crashlimit.setObjectName("lineEdit_crashlimit")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(30, 110, 111, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_backpiezostep = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_backpiezostep.setGeometry(QtCore.QRect(150, 220, 113, 31))
        self.lineEdit_backpiezostep.setObjectName("lineEdit_backpiezostep")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(10, 230, 141, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_fineapproach = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_fineapproach.setGeometry(QtCore.QRect(160, 390, 101, 31))
        self.pushButton_fineapproach.setObjectName("pushButton_fineapproach")
        self.lineEdit_zdelay = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_zdelay.setGeometry(QtCore.QRect(150, 260, 111, 31))
        self.lineEdit_zdelay.setObjectName("lineEdit_zdelay")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(80, 270, 61, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_zsteps = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_zsteps.setGeometry(QtCore.QRect(150, 300, 113, 31))
        self.lineEdit_zsteps.setObjectName("lineEdit_zsteps")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(40, 310, 91, 16))
        self.label_9.setObjectName("label_9")
        self.pushButton_tunnelingtest = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_tunnelingtest.setGeometry(QtCore.QRect(630, 90, 101, 31))
        self.pushButton_tunnelingtest.setObjectName("pushButton_tunnelingtest")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(510, 340, 91, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_scandelay = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_scandelay.setGeometry(QtCore.QRect(620, 290, 113, 31))
        self.lineEdit_scandelay.setObjectName("lineEdit_scandelay")
        self.lineEdit_scansteps = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_scansteps.setGeometry(QtCore.QRect(620, 330, 113, 31))
        self.lineEdit_scansteps.setObjectName("lineEdit_scansteps")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(550, 300, 61, 16))
        self.label_11.setObjectName("label_11")
        self.pushButton_scan = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_scan.setGeometry(QtCore.QRect(630, 390, 101, 31))
        self.pushButton_scan.setObjectName("pushButton_scan")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(20, 30, 131, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_samplevoltage = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_samplevoltage.setGeometry(QtCore.QRect(150, 20, 113, 31))
        self.lineEdit_samplevoltage.setObjectName("lineEdit_samplevoltage")
        self.pushButton_samplevoltage = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_samplevoltage.setGeometry(QtCore.QRect(160, 60, 101, 31))
        self.pushButton_samplevoltage.setObjectName("pushButton_samplevoltage")
        self.label_samplevoltage = QtWidgets.QLabel(self.tab_2)
        self.label_samplevoltage.setGeometry(QtCore.QRect(30, 70, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_samplevoltage.setFont(font)
        self.label_samplevoltage.setStyleSheet("color: rgb(9, 182, 0);")
        self.label_samplevoltage.setObjectName("label_samplevoltage")
        self.progressBar = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar.setGeometry(QtCore.QRect(30, 530, 461, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_daczregister = QtWidgets.QLabel(self.tab_2)
        self.label_daczregister.setGeometry(QtCore.QRect(390, 440, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_daczregister.setFont(font)
        self.label_daczregister.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_daczregister.setObjectName("label_daczregister")
        self.label_adcregister = QtWidgets.QLabel(self.tab_2)
        self.label_adcregister.setGeometry(QtCore.QRect(150, 440, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_adcregister.setFont(font)
        self.label_adcregister.setStyleSheet("color: rgb(255, 85, 0);")
        self.label_adcregister.setObjectName("label_adcregister")
        self.label_approachsta = QtWidgets.QLabel(self.tab_2)
        self.label_approachsta.setGeometry(QtCore.QRect(10, 400, 131, 16))
        self.label_approachsta.setObjectName("label_approachsta")
        self.label_adcregister_2 = QtWidgets.QLabel(self.tab_2)
        self.label_adcregister_2.setGeometry(QtCore.QRect(30, 440, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_adcregister_2.setFont(font)
        self.label_adcregister_2.setStyleSheet("color: rgb(255, 85, 0);")
        self.label_adcregister_2.setObjectName("label_adcregister_2")
        self.label_daczregister_2 = QtWidgets.QLabel(self.tab_2)
        self.label_daczregister_2.setGeometry(QtCore.QRect(270, 440, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_daczregister_2.setFont(font)
        self.label_daczregister_2.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_daczregister_2.setObjectName("label_daczregister_2")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(30, 470, 41, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(270, 470, 41, 16))
        self.label_14.setObjectName("label_14")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(30, 500, 111, 16))
        self.label_16.setObjectName("label_16")
        self.label_est = QtWidgets.QLabel(self.tab_2)
        self.label_est.setGeometry(QtCore.QRect(80, 470, 181, 16))
        self.label_est.setObjectName("label_est")
        self.label_cra = QtWidgets.QLabel(self.tab_2)
        self.label_cra.setGeometry(QtCore.QRect(320, 470, 181, 16))
        self.label_cra.setObjectName("label_cra")
        self.label_interval = QtWidgets.QLabel(self.tab_2)
        self.label_interval.setGeometry(QtCore.QRect(140, 500, 181, 16))
        self.label_interval.setObjectName("label_interval")
        self.label_crashlimit = QtWidgets.QLabel(self.tab_2)
        self.label_crashlimit.setGeometry(QtCore.QRect(280, 150, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_crashlimit.setFont(font)
        self.label_crashlimit.setStyleSheet("color: rgb(255, 85, 0);")
        self.label_crashlimit.setObjectName("label_crashlimit")
        self.label_currentlimit = QtWidgets.QLabel(self.tab_2)
        self.label_currentlimit.setGeometry(QtCore.QRect(280, 110, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_currentlimit.setFont(font)
        self.label_currentlimit.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_currentlimit.setObjectName("label_currentlimit")
        self.lineEdit_forwardsteps = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_forwardsteps.setGeometry(QtCore.QRect(150, 180, 113, 31))
        self.lineEdit_forwardsteps.setObjectName("lineEdit_forwardsteps")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 121, 16))
        self.label_7.setObjectName("label_7")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(50, 350, 91, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_zadjust = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_zadjust.setGeometry(QtCore.QRect(150, 340, 113, 31))
        self.lineEdit_zadjust.setObjectName("lineEdit_zadjust")
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(550, 20, 61, 16))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(510, 60, 91, 16))
        self.label_19.setObjectName("label_19")
        self.lineEdit_ztestdelay = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_ztestdelay.setGeometry(QtCore.QRect(620, 10, 113, 31))
        self.lineEdit_ztestdelay.setObjectName("lineEdit_ztestdelay")
        self.lineEdit_zteststep = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_zteststep.setGeometry(QtCore.QRect(620, 50, 113, 31))
        self.lineEdit_zteststep.setObjectName("lineEdit_zteststep")
        self.pushButton_zadjustplus = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_zadjustplus.setGeometry(QtCore.QRect(270, 340, 41, 31))
        self.pushButton_zadjustplus.setObjectName("pushButton_zadjustplus")
        self.pushButton_zadjustminus = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_zadjustminus.setGeometry(QtCore.QRect(320, 340, 41, 31))
        self.pushButton_zadjustminus.setObjectName("pushButton_zadjustminus")
        self.pushButton_zrecord = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_zrecord.setGeometry(QtCore.QRect(270, 390, 101, 31))
        self.pushButton_zrecord.setObjectName("pushButton_zrecord")
        self.lineEdit_scanbegin = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_scanbegin.setGeometry(QtCore.QRect(620, 210, 113, 31))
        self.lineEdit_scanbegin.setObjectName("lineEdit_scanbegin")
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setGeometry(QtCore.QRect(550, 220, 61, 16))
        self.label_20.setObjectName("label_20")
        self.lineEdit_scanend = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_scanend.setGeometry(QtCore.QRect(620, 250, 113, 31))
        self.lineEdit_scanend.setObjectName("lineEdit_scanend")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(550, 260, 61, 16))
        self.label_21.setObjectName("label_21")
        self.label_dacxregister = QtWidgets.QLabel(self.tab_2)
        self.label_dacxregister.setGeometry(QtCore.QRect(650, 440, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_dacxregister.setFont(font)
        self.label_dacxregister.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_dacxregister.setObjectName("label_dacxregister")
        self.label_daczregister_4 = QtWidgets.QLabel(self.tab_2)
        self.label_daczregister_4.setGeometry(QtCore.QRect(510, 440, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_daczregister_4.setFont(font)
        self.label_daczregister_4.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_daczregister_4.setObjectName("label_daczregister_4")
        self.label_dacyregister = QtWidgets.QLabel(self.tab_2)
        self.label_dacyregister.setGeometry(QtCore.QRect(650, 470, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_dacyregister.setFont(font)
        self.label_dacyregister.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_dacyregister.setObjectName("label_dacyregister")
        self.label_1 = QtWidgets.QLabel(self.tab_2)
        self.label_1.setGeometry(QtCore.QRect(510, 470, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_1.setObjectName("label_1")
        self.label_samplevoltage_2 = QtWidgets.QLabel(self.tab_2)
        self.label_samplevoltage_2.setGeometry(QtCore.QRect(510, 500, 131, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_samplevoltage_2.setFont(font)
        self.label_samplevoltage_2.setStyleSheet("color: rgb(9, 182, 0);")
        self.label_samplevoltage_2.setObjectName("label_samplevoltage_2")
        self.label_dacsampleregister = QtWidgets.QLabel(self.tab_2)
        self.label_dacsampleregister.setGeometry(QtCore.QRect(650, 500, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Adobe Myungjo Std M")
        font.setPointSize(12)
        self.label_dacsampleregister.setFont(font)
        self.label_dacsampleregister.setStyleSheet("color: rgb(85, 170, 127);")
        self.label_dacsampleregister.setObjectName("label_dacsampleregister")
        self.lineEdit_biasend = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_biasend.setGeometry(QtCore.QRect(582, 130, 81, 31))
        self.lineEdit_biasend.setObjectName("lineEdit_biasend")
        self.label_22 = QtWidgets.QLabel(self.tab_2)
        self.label_22.setGeometry(QtCore.QRect(470, 140, 101, 16))
        self.label_22.setObjectName("label_22")
        self.pushButton_biastest = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_biastest.setGeometry(QtCore.QRect(630, 170, 101, 31))
        self.pushButton_biastest.setObjectName("pushButton_biastest")
        self.lineEdit_biassteps = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_biassteps.setGeometry(QtCore.QRect(672, 130, 61, 31))
        self.lineEdit_biassteps.setObjectName("lineEdit_biassteps")
        self.checkBox_constheightmode = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_constheightmode.setGeometry(QtCore.QRect(520, 370, 91, 16))
        self.checkBox_constheightmode.setObjectName("checkBox_constheightmode")
        self.checkBox_scanreverse = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_scanreverse.setGeometry(QtCore.QRect(520, 400, 91, 16))
        self.checkBox_scanreverse.setObjectName("checkBox_scanreverse")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalSlider_debug = QtWidgets.QSlider(self.tab_3)
        self.horizontalSlider_debug.setGeometry(QtCore.QRect(40, 80, 581, 22))
        self.horizontalSlider_debug.setMaximum(65535)
        self.horizontalSlider_debug.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_debug.setObjectName("horizontalSlider_debug")
        self.pushButton_debugset = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_debugset.setGeometry(QtCore.QRect(640, 70, 91, 41))
        self.pushButton_debugset.setObjectName("pushButton_debugset")
        self.label_debugdac = QtWidgets.QLabel(self.tab_3)
        self.label_debugdac.setGeometry(QtCore.QRect(40, 115, 181, 31))
        self.label_debugdac.setObjectName("label_debugdac")
        self.label_debugadc = QtWidgets.QLabel(self.tab_3)
        self.label_debugadc.setGeometry(QtCore.QRect(40, 220, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_debugadc.setFont(font)
        self.label_debugadc.setObjectName("label_debugadc")
        self.pushButton_debugget = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_debugget.setGeometry(QtCore.QRect(640, 220, 91, 41))
        self.pushButton_debugget.setObjectName("pushButton_debugget")
        self.comboBox_debug = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_debug.setGeometry(QtCore.QRect(600, 130, 131, 22))
        self.comboBox_debug.setObjectName("comboBox_debug")
        self.pushButton_debugreset = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_debugreset.setGeometry(QtCore.QRect(640, 310, 91, 41))
        self.pushButton_debugreset.setObjectName("pushButton_debugreset")
        self.checkBox_follow = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_follow.setGeometry(QtCore.QRect(660, 160, 71, 16))
        self.checkBox_follow.setObjectName("checkBox_follow")
        self.tabWidget.addTab(self.tab_3, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 610, 771, 91))
        self.groupBox.setObjectName("groupBox")
        self.comboBox_port = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_port.setGeometry(QtCore.QRect(70, 40, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_port.setFont(font)
        self.comboBox_port.setObjectName("comboBox_port")
        self.comboBox_baudrate = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_baudrate.setGeometry(QtCore.QRect(430, 40, 91, 31))
        self.comboBox_baudrate.setEditable(False)
        self.comboBox_baudrate.setCurrentText("")
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.pushButton_uartconnect = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_uartconnect.setGeometry(QtCore.QRect(650, 40, 101, 31))
        self.pushButton_uartconnect.setObjectName("pushButton_uartconnect")
        self.pushButton_uartscan = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_uartscan.setGeometry(QtCore.QRect(540, 40, 101, 31))
        self.pushButton_uartscan.setObjectName("pushButton_uartscan")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 50, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(340, 50, 91, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.comboBox_baudrate.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "STMController"))
        self.pushButton_motorforward.setText(_translate("MainWindow", "FORWARD"))
        self.pushButton_motorbackward.setText(_translate("MainWindow", "BACKWARD"))
        self.label_3.setText(_translate("MainWindow", "Delay(ms):"))
        self.lineEdit_motordelay.setText(_translate("MainWindow", "5"))
        self.lineEdit_motorautolast.setText(_translate("MainWindow", "400"))
        self.label_15.setText(_translate("MainWindow", "Last(ms):"))
        self.pushButton_motorbackward_auto.setText(_translate("MainWindow", "BACKWARD"))
        self.pushButton_motorforward_auto.setText(_translate("MainWindow", "FORWARD"))
        self.pushButton_releasemotor.setText(_translate("MainWindow", "RELEASE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "CoarseApproach"))
        self.label_4.setText(_translate("MainWindow", "CrashLimit:"))
        self.lineEdit_currentlimit.setText(_translate("MainWindow", "0.2"))
        self.lineEdit_crashlimit.setText(_translate("MainWindow", "8"))
        self.label_5.setText(_translate("MainWindow", "CurrentLimit:"))
        self.lineEdit_backpiezostep.setText(_translate("MainWindow", "5000"))
        self.label_6.setText(_translate("MainWindow", "BackPiezoSteps:"))
        self.pushButton_fineapproach.setText(_translate("MainWindow", "Approach"))
        self.lineEdit_zdelay.setText(_translate("MainWindow", "1"))
        self.label_8.setText(_translate("MainWindow", "Delay:"))
        self.lineEdit_zsteps.setText(_translate("MainWindow", "25"))
        self.label_9.setText(_translate("MainWindow", "DACStpes:"))
        self.pushButton_tunnelingtest.setText(_translate("MainWindow", "TEST"))
        self.label_10.setText(_translate("MainWindow", "DACStpes:"))
        self.lineEdit_scandelay.setText(_translate("MainWindow", "1"))
        self.lineEdit_scansteps.setText(_translate("MainWindow", "10"))
        self.label_11.setText(_translate("MainWindow", "Delay:"))
        self.pushButton_scan.setText(_translate("MainWindow", "SCAN"))
        self.label_12.setText(_translate("MainWindow", "SampleVoltage:"))
        self.lineEdit_samplevoltage.setText(_translate("MainWindow", "-0.05"))
        self.pushButton_samplevoltage.setText(_translate("MainWindow", "SET"))
        self.label_samplevoltage.setText(_translate("MainWindow", "NOW:NULL"))
        self.label_daczregister.setText(_translate("MainWindow", "NULL"))
        self.label_adcregister.setText(_translate("MainWindow", "NULL"))
        self.label_approachsta.setText(_translate("MainWindow", "Approach:NULL"))
        self.label_adcregister_2.setText(_translate("MainWindow", "ADC Register:"))
        self.label_daczregister_2.setText(_translate("MainWindow", "DAC Reigster:"))
        self.label_13.setText(_translate("MainWindow", "EST:"))
        self.label_14.setText(_translate("MainWindow", "CRA:"))
        self.label_16.setText(_translate("MainWindow", "INTERVAL:"))
        self.label_est.setText(_translate("MainWindow", "NULL"))
        self.label_cra.setText(_translate("MainWindow", "NULL"))
        self.label_interval.setText(_translate("MainWindow", "NULL"))
        self.label_crashlimit.setText(_translate("MainWindow", "NULL"))
        self.label_currentlimit.setText(_translate("MainWindow", "NULL"))
        self.lineEdit_forwardsteps.setText(_translate("MainWindow", "15"))
        self.label_7.setText(_translate("MainWindow", "ForwardSteps:"))
        self.label_17.setText(_translate("MainWindow", "Z Adjust:"))
        self.lineEdit_zadjust.setText(_translate("MainWindow", "25"))
        self.label_18.setText(_translate("MainWindow", "Delay:"))
        self.label_19.setText(_translate("MainWindow", "DACStpes:"))
        self.lineEdit_ztestdelay.setText(_translate("MainWindow", "1"))
        self.lineEdit_zteststep.setText(_translate("MainWindow", "10"))
        self.pushButton_zadjustplus.setText(_translate("MainWindow", "+"))
        self.pushButton_zadjustminus.setText(_translate("MainWindow", "-"))
        self.pushButton_zrecord.setText(_translate("MainWindow", "REC"))
        self.lineEdit_scanbegin.setText(_translate("MainWindow", "0"))
        self.label_20.setText(_translate("MainWindow", "From:"))
        self.lineEdit_scanend.setText(_translate("MainWindow", "65535"))
        self.label_21.setText(_translate("MainWindow", "To:"))
        self.label_dacxregister.setText(_translate("MainWindow", "NULL"))
        self.label_daczregister_4.setText(_translate("MainWindow", "DAC XReigster:"))
        self.label_dacyregister.setText(_translate("MainWindow", "NULL"))
        self.label_1.setText(_translate("MainWindow", "DAC XReigster:"))
        self.label_samplevoltage_2.setText(_translate("MainWindow", "SAMPLE DAC:"))
        self.label_dacsampleregister.setText(_translate("MainWindow", "NULL"))
        self.lineEdit_biasend.setText(_translate("MainWindow", "-1"))
        self.label_22.setText(_translate("MainWindow", "END/STEPS"))
        self.pushButton_biastest.setText(_translate("MainWindow", "BEGIN"))
        self.lineEdit_biassteps.setText(_translate("MainWindow", "10"))
        self.checkBox_constheightmode.setText(_translate("MainWindow", "CH Mode"))
        self.checkBox_scanreverse.setText(_translate("MainWindow", "Reverse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "FineApproach/SCAN"))
        self.pushButton_debugset.setText(_translate("MainWindow", "SET"))
        self.label_debugdac.setText(_translate("MainWindow", "0(-10V)"))
        self.label_debugadc.setText(_translate("MainWindow", "0(12.228V)"))
        self.pushButton_debugget.setText(_translate("MainWindow", "GET"))
        self.pushButton_debugreset.setText(_translate("MainWindow", "RESET"))
        self.checkBox_follow.setText(_translate("MainWindow", "FO"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "ManualControl"))
        self.groupBox.setTitle(_translate("MainWindow", "UART Port Select"))
        self.pushButton_uartconnect.setText(_translate("MainWindow", "CONNECT"))
        self.pushButton_uartscan.setText(_translate("MainWindow", "SCAN"))
        self.label.setText(_translate("MainWindow", "Port:"))
        self.label_2.setText(_translate("MainWindow", "BaudRate???"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
