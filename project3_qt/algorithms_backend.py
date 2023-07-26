from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
import time
import random

# just do bfs for now
class AlgorithmSignals(QObject):
    update_sig = Signal(int, int)  # index to update

class AlgorithmRunner(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = AlgorithmSignals()
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    @Slot()
    def run(self):
        while not self.stop_flag:
            x1, y1 = random.randint(0, 9), random.randint(0, 9)

            self.signals.update_sig.emit(x1, y1)
            time.sleep(1)