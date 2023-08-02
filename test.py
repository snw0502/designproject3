import sys
import random
import time
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QPushButton, QVBoxLayout, QWidget, QGraphicsRectItem


class SortSigs(QObject):
    sort_step_completed = Signal(list)

class SortingThread(QThread):

    def __init__(self, array):
        super().__init__()
        self.array = array
        self.signals = SortSigs()

    def run(self):
        self.quick_sort(self.array, 0, len(self.array) - 1)

    def quick_sort(self, array, low, high):
        if low < high:
            pivot_idx = self.partition(array, low, high)
            self.quick_sort(array, low, pivot_idx - 1)
            self.quick_sort(array, pivot_idx + 1, high)
            self.sort_step_completed.emit(array[:])
            time.sleep(0.05)

    def partition(self, array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                self.signals.sort_step_completed.emit(array[:])
                time.sleep(0.05)
        array[i + 1], array[high] = array[high], array[i + 1]
        self.signals.sort_step_completed.emit(array[:])
        return i + 1

class BarItem(QGraphicsRectItem):
    def __init__(self, x, height):
        super().__init__(x, 0, 20, height * 5)
        self.setBrush(QColor(Qt.blue))

class QuickSortApp(QWidget):
    def __init__(self):
        super().__init__()

        self.array = [random.randint(1, 300) for _ in range(100)]
        self.sort_thread = SortingThread(self.array)
        self.sort_thread.sort_step_completed.connect(self.update_array)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)

        self.sort_button = QPushButton("Start QuickSort")
        self.sort_button.clicked.connect(self.start_sorting)
        layout.addWidget(self.sort_button)

        self.setLayout(layout)
        self.setWindowTitle("QuickSort Simulation")
        self.init_scene()
        self.show()

    def init_scene(self):
        for idx, value in enumerate(self.array):
            bar_item = BarItem(idx * 25, value)
            self.scene.addItem(bar_item)

    def start_sorting(self):
        self.sort_button.setEnabled(False)
        self.sort_thread.start()

    def update_array(self, array):
        self.array = array
        for idx, value in enumerate(self.array):
            item = self.scene.itemAt(idx * 25, 0, self.view.transform())
            if item:
                item.setRect(idx * 25, 0, 20, value * 5)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuickSortApp()
    sys.exit(app.exec_())
