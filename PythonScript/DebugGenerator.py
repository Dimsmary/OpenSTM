import time


class DebugGeneratorHandle:
    def __init__(self, ui):
        self.ui = ui

    def print(self, label, message):
        msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + label + ': ' + message
        self.ui.textBrowser.append(msg)

