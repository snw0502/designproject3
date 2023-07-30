from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
from algorithms_backend import *
from PIL import Image


class AlgorithmVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Visualizer")
        self.resize(1400, 1000)

        #draw task
        self.runner = None

        #MAIN LAYOUTS
        self.page_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.visualizer_layout = QVBoxLayout()

        self.file_layout = QHBoxLayout()

        self.txtin_file = QLineEdit("./maze2.png")
        self.btn_import = QPushButton("Import")
        self.btn_set_maze = QPushButton("Set new maze")

        self.file_layout.addWidget(self.txtin_file)
        self.file_layout.addWidget(self.btn_import)
        self.file_layout.addWidget(self.btn_set_maze)


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
        
        self.visualizer_layout.addLayout(self.file_layout)

        self.create_graphic_view()

        self.btn_breadth_first.clicked.connect(self.start_thread)
        self.btn_import.clicked.connect(self.import_file)
        self.btn_set_maze.clicked.connect(self.set_maze)

        self.btn_stop.clicked.connect(self.stop_thread)

        self.main_widget = Color('light blue')
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)

    def start_thread(self):
        maze1 = self.scene.bfs_arr
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
        self.scene = GridScene(self.txtin_file.text(),8)

        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphic_view = QGraphicsView(self.scene, self)
        self.visualizer_layout.addWidget(graphic_view)


    def get_bfs_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end,QColor(158, 29, 68))

    def import_file(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open PNG File', '', 'PNG Files (*.png)')
        self.txtin_file.setText(image_path)

    def set_maze(self):
        new_maze = self.txtin_file.text()
        self.scene.load_image(new_maze)


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
    def __init__(self, image_path: str, cell_size: int):
        super().__init__()
        self.cell_size = cell_size
        self.internal_grid = []
        #self.load_image(image_path)

    def load_image(self, image_path: str):
        image = Image.open(image_path)
        
        gray_image = image.convert('L')
        threshold = 128
        cols, rows = gray_image.size

        self.bfs_arr = [[None for _ in range(cols)] for _ in range(rows)]
        self.internal_grid = [[None for _ in range(cols)] for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                x = col * self.cell_size
                y = row * self.cell_size
                pixel_value = gray_image.getpixel((col, row))
                if pixel_value > threshold:
                    color = QColor(255,255,255)
                    self.bfs_arr[row][col] = 8
                else:
                    color = QColor(0,0,0)
                    self.bfs_arr[row][col] = 2
                cell = GridCell(x, y, self.cell_size)
                cell.set_color(color)
                self.addItem(cell)
                self.internal_grid[row][col] = cell
    
    def get_cell_color(self, row: int, col: int):
        return self.internal_grid[row][col].get_color()

    def set_cell_color(self, row: int, col: int, color):
        if self.internal_grid[row][col]:
            self.internal_grid[row][col].set_color(color)#updating internal grid
            self.update(self.internal_grid[row][col].rect())#updating visual scene