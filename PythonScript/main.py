from PyQt5 import QtWidgets

from MainController import MainWindowController

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec_())


