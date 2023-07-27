from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
from algorithms_backend import *


class AlgorithmVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Visualizer")
        self.resize(800, 600)

        #draw task
        self.runner = None

        #MAIN LAYOUTS
        self.page_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.visualizer_layout = QVBoxLayout()

        self.page_layout.addLayout(self.button_layout)
        self.page_layout.addLayout(self.visualizer_layout)
        
        #BUTTONS
        self.btn_breadth_first = QPushButton("Breadth First Search")
        self.btn_a_star = QPushButton("A Star Search")
        self.btn_quick_sort = QPushButton("Quick Sort")
        self.btn_select_sort = QPushButton("Selection Sort")

        self.button_layout.addWidget(self.btn_breadth_first)
        self.button_layout.addWidget(self.btn_a_star)
        self.button_layout.addWidget(self.btn_quick_sort)
        self.button_layout.addWidget(self.btn_select_sort)

        self.btn_stop = QPushButton("Stop drawing")
        self.button_layout.addWidget(self.btn_stop)


        #Grid and stuff
        self.visualizer_layout.addWidget(UI_Help.create_label("Algorithm Visualizer", Fonts.large_bold_font))
        
        self.create_graphic_view()

        self.btn_breadth_first.clicked.connect(self.start_thread)

        self.btn_stop.clicked.connect(self.stop_thread)

        self.main_widget = Color('light blue')
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)

    def start_thread(self):
        maze1 = [
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,8,8,8,8,8,8,8,8,8,2,8,8,8,8,8,8,8,8,8,8,8,8,8,2,8,8,8,8,8,2,2],
            [2,8,2,8,2,2,2,8,2,8,2,2,2,8,2,8,2,2,2,8,2,2,2,8,2,2,2,8,2,2,2,2],
            [2,8,2,8,8,8,8,8,2,8,8,8,2,8,2,8,8,8,8,8,8,8,2,8,8,8,2,8,8,8,2,2],
            [2,8,2,2,2,8,2,8,2,2,2,8,2,8,2,8,2,2,2,2,2,8,2,2,2,8,2,2,2,8,2,2],
            [2,8,8,8,8,8,2,8,8,8,2,8,8,8,8,8,8,8,2,8,8,8,8,8,2,8,8,8,8,8,2,2],
            [2,2,2,8,2,2,2,2,2,8,2,8,2,2,2,8,2,8,2,2,2,2,2,8,2,2,2,8,2,8,2,2],
            [2,8,8,8,8,8,8,8,2,8,8,8,8,8,8,8,2,8,8,8,8,8,8,8,8,8,2,8,2,8,8,8],
            [2,8,2,2,2,2,2,8,2,8,2,8,2,2,2,8,2,8,2,2,2,8,2,8,2,2,2,8,2,8,2,2],
            [2,8,8,8,2,8,8,8,8,8,2,8,8,8,8,8,8,8,2,8,2,8,2,8,2,8,8,8,8,8,2,2],
            [2,8,2,2,2,8,2,2,2,8,2,2,2,8,2,2,2,8,2,8,2,8,2,2,2,8,2,2,2,8,2,2],
            [2,8,8,8,8,8,2,8,8,8,8,8,2,8,8,8,2,8,8,8,8,8,8,8,8,8,2,8,8,8,2,2],
            [2,8,2,8,2,2,2,8,2,2,2,8,2,8,2,8,2,2,2,8,2,2,2,8,2,2,2,8,2,8,2,2],
            [2,8,2,8,8,8,8,8,8,8,8,8,8,8,2,8,8,8,8,8,8,8,8,8,8,8,8,8,2,8,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ];
        if not self.runner:
            self.runner = AlgorithmRunner(maze1)
            QThreadPool.globalInstance().start(self.runner)
            self.runner.signals.update_sig.connect(self.get_bfs_sig)

    def stop_thread(self):
        if self.runner:
            self.runner.stop()
            self.runner.signals.update_sig.disconnect(self.get_bfs_sig)
            self.runner = None

    def create_graphic_view(self):
        #self.scene = QGraphicsScene()
        self.scene = GridScene(16, 32, 30)

        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphic_view = QGraphicsView(self.scene, self)
        graphic_view.setGeometry(0,0,600,500)
        self.visualizer_layout.addWidget(graphic_view)

    #BUTTON SIGNALS
    #def show_bfs(self):
    #    self.scene.addLine(50,50,200,200)

    def get_bfs_sig(self, start: int, end: int):
        #self.scene.addLine(start,start,end,end)
        self.scene.set_cell_color(start,end,QColor(158, 29, 68))


class GridCell(QGraphicsRectItem):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.setPen(QPen(Qt.black))
        self.setBrush(QColor(255, 255, 255))
    
    def get_color(self):
        return self.brush().color()

    def set_color(self, color):
        self.setBrush(color)

class GridScene(QGraphicsScene):
    def __init__(self, rows: int, cols: int, cell_size: int):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.internal_grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.draw_grid()


    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                cell = GridCell(x, y, self.cell_size)
                self.addItem(cell)
                self.internal_grid[row][col] = cell

        self.set_cell_color(0,0,QColor(18,30,91))
        self.set_cell_color(0,1,QColor(18,30,91))
        self.set_cell_color(0,2,QColor(18,30,91))
        self.set_cell_color(0,3,QColor(18,30,91))
        self.set_cell_color(0,4,QColor(18,30,91))
        self.set_cell_color(0,5,QColor(18,30,91))
        self.set_cell_color(0,6,QColor(18,30,91))
        self.set_cell_color(0,7,QColor(18,30,91))
        self.set_cell_color(0,8,QColor(18,30,91))
        self.set_cell_color(0,9,QColor(18,30,91))
        self.set_cell_color(0,10,QColor(18,30,91))
        self.set_cell_color(0,11,QColor(18,30,91))
        self.set_cell_color(0,12,QColor(18,30,91))
        self.set_cell_color(0,13,QColor(18,30,91))
        self.set_cell_color(0,14,QColor(18,30,91))
        self.set_cell_color(0,15,QColor(18,30,91))
        self.set_cell_color(0,16,QColor(18,30,91))
        self.set_cell_color(0,17,QColor(18,30,91))
        self.set_cell_color(0,18,QColor(18,30,91))
        self.set_cell_color(0,19,QColor(18,30,91))
        self.set_cell_color(0,20,QColor(18,30,91))
        self.set_cell_color(0,21,QColor(18,30,91))
        self.set_cell_color(0,22,QColor(18,30,91))
        self.set_cell_color(0,23,QColor(18,30,91))
        self.set_cell_color(0,24,QColor(18,30,91))
        self.set_cell_color(0,25,QColor(18,30,91))
        self.set_cell_color(0,26,QColor(18,30,91))
        self.set_cell_color(0,27,QColor(18,30,91))
        self.set_cell_color(0,28,QColor(18,30,91))
        self.set_cell_color(0,29,QColor(18,30,91))
        self.set_cell_color(0,30,QColor(18,30,91))
        self.set_cell_color(0,31,QColor(18,30,91))
        self.set_cell_color(1,0,QColor(18,30,91))
        self.set_cell_color(1,10,QColor(18,30,91))
        self.set_cell_color(1,24,QColor(18,30,91))
        self.set_cell_color(1,30,QColor(18,30,91))
        self.set_cell_color(1,31,QColor(18,30,91))
        self.set_cell_color(2,0,QColor(18,30,91))
        self.set_cell_color(2,2,QColor(18,30,91))
        self.set_cell_color(2,4,QColor(18,30,91))
        self.set_cell_color(2,5,QColor(18,30,91))
        self.set_cell_color(2,6,QColor(18,30,91))
        self.set_cell_color(2,8,QColor(18,30,91))
        self.set_cell_color(2,10,QColor(18,30,91))
        self.set_cell_color(2,11,QColor(18,30,91))
        self.set_cell_color(2,12,QColor(18,30,91))
        self.set_cell_color(2,14,QColor(18,30,91))
        self.set_cell_color(2,16,QColor(18,30,91))
        self.set_cell_color(2,17,QColor(18,30,91))
        self.set_cell_color(2,18,QColor(18,30,91))
        self.set_cell_color(2,20,QColor(18,30,91))
        self.set_cell_color(2,21,QColor(18,30,91))
        self.set_cell_color(2,22,QColor(18,30,91))
        self.set_cell_color(2,24,QColor(18,30,91))
        self.set_cell_color(2,25,QColor(18,30,91))
        self.set_cell_color(2,26,QColor(18,30,91))
        self.set_cell_color(2,28,QColor(18,30,91))
        self.set_cell_color(2,29,QColor(18,30,91))
        self.set_cell_color(2,30,QColor(18,30,91))
        self.set_cell_color(2,31,QColor(18,30,91))
        self.set_cell_color(3,0,QColor(18,30,91))
        self.set_cell_color(3,2,QColor(18,30,91))
        self.set_cell_color(3,8,QColor(18,30,91))
        self.set_cell_color(3,12,QColor(18,30,91))
        self.set_cell_color(3,14,QColor(18,30,91))
        self.set_cell_color(3,22,QColor(18,30,91))
        self.set_cell_color(3,26,QColor(18,30,91))
        self.set_cell_color(3,30,QColor(18,30,91))
        self.set_cell_color(3,31,QColor(18,30,91))
        self.set_cell_color(4,0,QColor(18,30,91))
        self.set_cell_color(4,2,QColor(18,30,91))
        self.set_cell_color(4,3,QColor(18,30,91))
        self.set_cell_color(4,4,QColor(18,30,91))
        self.set_cell_color(4,6,QColor(18,30,91))
        self.set_cell_color(4,8,QColor(18,30,91))
        self.set_cell_color(4,9,QColor(18,30,91))
        self.set_cell_color(4,10,QColor(18,30,91))
        self.set_cell_color(4,12,QColor(18,30,91))
        self.set_cell_color(4,14,QColor(18,30,91))
        self.set_cell_color(4,16,QColor(18,30,91))
        self.set_cell_color(4,17,QColor(18,30,91))
        self.set_cell_color(4,18,QColor(18,30,91))
        self.set_cell_color(4,19,QColor(18,30,91))
        self.set_cell_color(4,20,QColor(18,30,91))
        self.set_cell_color(4,22,QColor(18,30,91))
        self.set_cell_color(4,23,QColor(18,30,91))
        self.set_cell_color(4,24,QColor(18,30,91))
        self.set_cell_color(4,26,QColor(18,30,91))
        self.set_cell_color(4,27,QColor(18,30,91))
        self.set_cell_color(4,28,QColor(18,30,91))
        self.set_cell_color(4,30,QColor(18,30,91))
        self.set_cell_color(4,31,QColor(18,30,91))
        self.set_cell_color(5,0,QColor(18,30,91))
        self.set_cell_color(5,6,QColor(18,30,91))
        self.set_cell_color(5,10,QColor(18,30,91))
        self.set_cell_color(5,18,QColor(18,30,91))
        self.set_cell_color(5,24,QColor(18,30,91))
        self.set_cell_color(5,30,QColor(18,30,91))
        self.set_cell_color(5,31,QColor(18,30,91))
        self.set_cell_color(6,0,QColor(18,30,91))
        self.set_cell_color(6,1,QColor(18,30,91))
        self.set_cell_color(6,2,QColor(18,30,91))
        self.set_cell_color(6,4,QColor(18,30,91))
        self.set_cell_color(6,5,QColor(18,30,91))
        self.set_cell_color(6,6,QColor(18,30,91))
        self.set_cell_color(6,7,QColor(18,30,91))
        self.set_cell_color(6,8,QColor(18,30,91))
        self.set_cell_color(6,10,QColor(18,30,91))
        self.set_cell_color(6,12,QColor(18,30,91))
        self.set_cell_color(6,13,QColor(18,30,91))
        self.set_cell_color(6,14,QColor(18,30,91))
        self.set_cell_color(6,16,QColor(18,30,91))
        self.set_cell_color(6,18,QColor(18,30,91))
        self.set_cell_color(6,19,QColor(18,30,91))
        self.set_cell_color(6,20,QColor(18,30,91))
        self.set_cell_color(6,21,QColor(18,30,91))
        self.set_cell_color(6,22,QColor(18,30,91))
        self.set_cell_color(6,24,QColor(18,30,91))
        self.set_cell_color(6,25,QColor(18,30,91))
        self.set_cell_color(6,26,QColor(18,30,91))
        self.set_cell_color(6,28,QColor(18,30,91))
        self.set_cell_color(6,30,QColor(18,30,91))
        self.set_cell_color(6,31,QColor(18,30,91))
        self.set_cell_color(7,0,QColor(18,30,91))
        self.set_cell_color(7,8,QColor(18,30,91))
        self.set_cell_color(7,16,QColor(18,30,91))
        self.set_cell_color(7,26,QColor(18,30,91))
        self.set_cell_color(7,28,QColor(18,30,91))
        self.set_cell_color(8,0,QColor(18,30,91))
        self.set_cell_color(8,2,QColor(18,30,91))
        self.set_cell_color(8,3,QColor(18,30,91))
        self.set_cell_color(8,4,QColor(18,30,91))
        self.set_cell_color(8,5,QColor(18,30,91))
        self.set_cell_color(8,6,QColor(18,30,91))
        self.set_cell_color(8,8,QColor(18,30,91))
        self.set_cell_color(8,10,QColor(18,30,91))
        self.set_cell_color(8,12,QColor(18,30,91))
        self.set_cell_color(8,13,QColor(18,30,91))
        self.set_cell_color(8,14,QColor(18,30,91))
        self.set_cell_color(8,16,QColor(18,30,91))
        self.set_cell_color(8,18,QColor(18,30,91))
        self.set_cell_color(8,19,QColor(18,30,91))
        self.set_cell_color(8,20,QColor(18,30,91))
        self.set_cell_color(8,22,QColor(18,30,91))
        self.set_cell_color(8,24,QColor(18,30,91))
        self.set_cell_color(8,25,QColor(18,30,91))
        self.set_cell_color(8,26,QColor(18,30,91))
        self.set_cell_color(8,28,QColor(18,30,91))
        self.set_cell_color(8,30,QColor(18,30,91))
        self.set_cell_color(8,31,QColor(18,30,91))
        self.set_cell_color(9,0,QColor(18,30,91))
        self.set_cell_color(9,4,QColor(18,30,91))
        self.set_cell_color(9,10,QColor(18,30,91))
        self.set_cell_color(9,18,QColor(18,30,91))
        self.set_cell_color(9,20,QColor(18,30,91))
        self.set_cell_color(9,22,QColor(18,30,91))
        self.set_cell_color(9,24,QColor(18,30,91))
        self.set_cell_color(9,30,QColor(18,30,91))
        self.set_cell_color(9,31,QColor(18,30,91))
        self.set_cell_color(10,0,QColor(18,30,91))
        self.set_cell_color(10,2,QColor(18,30,91))
        self.set_cell_color(10,3,QColor(18,30,91))
        self.set_cell_color(10,4,QColor(18,30,91))
        self.set_cell_color(10,6,QColor(18,30,91))
        self.set_cell_color(10,7,QColor(18,30,91))
        self.set_cell_color(10,8,QColor(18,30,91))
        self.set_cell_color(10,10,QColor(18,30,91))
        self.set_cell_color(10,11,QColor(18,30,91))
        self.set_cell_color(10,12,QColor(18,30,91))
        self.set_cell_color(10,14,QColor(18,30,91))
        self.set_cell_color(10,15,QColor(18,30,91))
        self.set_cell_color(10,16,QColor(18,30,91))
        self.set_cell_color(10,18,QColor(18,30,91))
        self.set_cell_color(10,20,QColor(18,30,91))
        self.set_cell_color(10,22,QColor(18,30,91))
        self.set_cell_color(10,23,QColor(18,30,91))
        self.set_cell_color(10,24,QColor(18,30,91))
        self.set_cell_color(10,26,QColor(18,30,91))
        self.set_cell_color(10,27,QColor(18,30,91))
        self.set_cell_color(10,28,QColor(18,30,91))
        self.set_cell_color(10,30,QColor(18,30,91))
        self.set_cell_color(10,31,QColor(18,30,91))
        self.set_cell_color(11,0,QColor(18,30,91))
        self.set_cell_color(11,6,QColor(18,30,91))
        self.set_cell_color(11,12,QColor(18,30,91))
        self.set_cell_color(11,16,QColor(18,30,91))
        self.set_cell_color(11,26,QColor(18,30,91))
        self.set_cell_color(11,30,QColor(18,30,91))
        self.set_cell_color(11,31,QColor(18,30,91))
        self.set_cell_color(12,0,QColor(18,30,91))
        self.set_cell_color(12,2,QColor(18,30,91))
        self.set_cell_color(12,4,QColor(18,30,91))
        self.set_cell_color(12,5,QColor(18,30,91))
        self.set_cell_color(12,6,QColor(18,30,91))
        self.set_cell_color(12,8,QColor(18,30,91))
        self.set_cell_color(12,9,QColor(18,30,91))
        self.set_cell_color(12,10,QColor(18,30,91))
        self.set_cell_color(12,12,QColor(18,30,91))
        self.set_cell_color(12,14,QColor(18,30,91))
        self.set_cell_color(12,16,QColor(18,30,91))
        self.set_cell_color(12,17,QColor(18,30,91))
        self.set_cell_color(12,18,QColor(18,30,91))
        self.set_cell_color(12,20,QColor(18,30,91))
        self.set_cell_color(12,21,QColor(18,30,91))
        self.set_cell_color(12,22,QColor(18,30,91))
        self.set_cell_color(12,24,QColor(18,30,91))
        self.set_cell_color(12,25,QColor(18,30,91))
        self.set_cell_color(12,26,QColor(18,30,91))
        self.set_cell_color(12,28,QColor(18,30,91))
        self.set_cell_color(12,30,QColor(18,30,91))
        self.set_cell_color(12,31,QColor(18,30,91))
        self.set_cell_color(13,0,QColor(18,30,91))
        self.set_cell_color(13,2,QColor(18,30,91))
        self.set_cell_color(13,14,QColor(18,30,91))
        self.set_cell_color(13,28,QColor(18,30,91))
        self.set_cell_color(13,30,QColor(18,30,91))
        self.set_cell_color(13,31,QColor(18,30,91))
        self.set_cell_color(14,0,QColor(18,30,91))
        self.set_cell_color(14,1,QColor(18,30,91))
        self.set_cell_color(14,2,QColor(18,30,91))
        self.set_cell_color(14,3,QColor(18,30,91))
        self.set_cell_color(14,4,QColor(18,30,91))
        self.set_cell_color(14,5,QColor(18,30,91))
        self.set_cell_color(14,6,QColor(18,30,91))
        self.set_cell_color(14,7,QColor(18,30,91))
        self.set_cell_color(14,8,QColor(18,30,91))
        self.set_cell_color(14,9,QColor(18,30,91))
        self.set_cell_color(14,10,QColor(18,30,91))
        self.set_cell_color(14,11,QColor(18,30,91))
        self.set_cell_color(14,12,QColor(18,30,91))
        self.set_cell_color(14,13,QColor(18,30,91))
        self.set_cell_color(14,14,QColor(18,30,91))
        self.set_cell_color(14,15,QColor(18,30,91))
        self.set_cell_color(14,16,QColor(18,30,91))
        self.set_cell_color(14,17,QColor(18,30,91))
        self.set_cell_color(14,18,QColor(18,30,91))
        self.set_cell_color(14,19,QColor(18,30,91))
        self.set_cell_color(14,20,QColor(18,30,91))
        self.set_cell_color(14,21,QColor(18,30,91))
        self.set_cell_color(14,22,QColor(18,30,91))
        self.set_cell_color(14,23,QColor(18,30,91))
        self.set_cell_color(14,24,QColor(18,30,91))
        self.set_cell_color(14,25,QColor(18,30,91))
        self.set_cell_color(14,26,QColor(18,30,91))
        self.set_cell_color(14,27,QColor(18,30,91))
        self.set_cell_color(14,28,QColor(18,30,91))
        self.set_cell_color(14,29,QColor(18,30,91))
        self.set_cell_color(14,30,QColor(18,30,91))
        self.set_cell_color(14,31,QColor(18,30,91))
        self.set_cell_color(15,0,QColor(18,30,91))
        self.set_cell_color(15,1,QColor(18,30,91))
        self.set_cell_color(15,2,QColor(18,30,91))
        self.set_cell_color(15,3,QColor(18,30,91))
        self.set_cell_color(15,4,QColor(18,30,91))
        self.set_cell_color(15,5,QColor(18,30,91))
        self.set_cell_color(15,6,QColor(18,30,91))
        self.set_cell_color(15,7,QColor(18,30,91))
        self.set_cell_color(15,8,QColor(18,30,91))
        self.set_cell_color(15,9,QColor(18,30,91))
        self.set_cell_color(15,10,QColor(18,30,91))
        self.set_cell_color(15,11,QColor(18,30,91))
        self.set_cell_color(15,12,QColor(18,30,91))
        self.set_cell_color(15,13,QColor(18,30,91))
        self.set_cell_color(15,14,QColor(18,30,91))
        self.set_cell_color(15,15,QColor(18,30,91))
        self.set_cell_color(15,16,QColor(18,30,91))
        self.set_cell_color(15,17,QColor(18,30,91))
        self.set_cell_color(15,18,QColor(18,30,91))
        self.set_cell_color(15,19,QColor(18,30,91))
        self.set_cell_color(15,20,QColor(18,30,91))
        self.set_cell_color(15,21,QColor(18,30,91))
        self.set_cell_color(15,22,QColor(18,30,91))
        self.set_cell_color(15,23,QColor(18,30,91))
        self.set_cell_color(15,24,QColor(18,30,91))
        self.set_cell_color(15,25,QColor(18,30,91))
        self.set_cell_color(15,26,QColor(18,30,91))
        self.set_cell_color(15,27,QColor(18,30,91))
        self.set_cell_color(15,28,QColor(18,30,91))
        self.set_cell_color(15,29,QColor(18,30,91))
        self.set_cell_color(15,30,QColor(18,30,91))
        self.set_cell_color(15,31,QColor(18,30,91))
        
    
    def get_cell_color(self, row: int, col: int):
        return self.internal_grid[row][col].get_color()

    def set_cell_color(self, row: int, col: int, color):
        print(f"updating cell: [{row}, {col}]")
        self.internal_grid[row][col].set_color(color)

        # Update the visual representation in the scene
        self.update(self.internal_grid[row][col].rect())