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
        if not self.runner:
            self.runner = AlgorithmRunner()
            QThreadPool.globalInstance().start(self.runner)
            self.runner.signals.update_sig.connect(self.get_bfs_sig)

    def stop_thread(self):
        if self.runner:
            self.runner.stop()
            self.runner.signals.update_sig.disconnect(self.get_bfs_sig)
            self.runner = None

    def create_graphic_view(self):
        #self.scene = QGraphicsScene()
        self.scene = GridScene(10, 10, 30)

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
        self.scene.set_cell_color(start,end,QColor(255, 0, 0))


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
    
    def get_cell_color(self, row: int, col: int):
        return self.internal_grid[row][col].get_color()

    def set_cell_color(self, row: int, col: int, color):
        print(f"updating cell: [{row}, {col}]")
        self.internal_grid[row][col].set_color(color)

        # Update the visual representation in the scene
        self.update(self.internal_grid[row][col].rect())