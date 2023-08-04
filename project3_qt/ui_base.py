from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
from algorithms_backend import *
from PIL import Image
from qt_material import apply_stylesheet
import math


class LaunchWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Visualier: Launch Window")
        self.resize(500,500)
        self.main_layout = QVBoxLayout()
        self.btn_start_pathfinding_visualizer = QPushButton("Show pathfinding\nvisualizer")
        self.btn_start_sorting_visualizer = QPushButton("Show sorting\nvisualizer")
        self.btn_exit = QPushButton("Exit")

        self.main_layout.addWidget(self.btn_start_pathfinding_visualizer)
        self.main_layout.addWidget(self.btn_start_sorting_visualizer)
        self.main_layout.addWidget(self.btn_exit)
        self.pathfinder = PathfindingVisualizer()
        self.sorter = SortingVisualizer()

        self.connect_buttons()

        self.main_widget = Color('purple')
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def connect_buttons(self):
        self.btn_start_pathfinding_visualizer.clicked.connect(self.start_pathfinder_trigger)
        self.btn_start_sorting_visualizer.clicked.connect(self.start_sorter_trigger)
        self.btn_exit.clicked.connect(self.exit_app)

    def start_pathfinder_trigger(self):
        self.pathfinder.show()

    def start_sorter_trigger(self):
        self.sorter.show()

    def exit_app(self):
        self.pathfinder.close()
        self.sorter.close()
        self.close()

class PathfindingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pathfinding Visualizer")
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
        self.btn_reset_maze = QPushButton("Reset Maze")

        self.num_elems_searched_label = QLabel("Operations Performed: 0")
        self.num_elems_searched_label.setFixedHeight(40)

        self.button_layout.setContentsMargins(10,10,10,10)
        self.button_layout.setSpacing(20)
        self.button_layout.setAlignment(Qt.AlignHCenter)
        
        self.button_layout.addWidget(self.btn_breadth_first)
        self.button_layout.addWidget(self.btn_a_star)

        self.btn_stop = QPushButton("Stop drawing")
        self.button_layout.addWidget(self.btn_stop)
        self.button_layout.addWidget(self.btn_reset_maze)


        self.button_layout.addWidget(self.num_elems_searched_label)
        
        self.visualizer_layout.addLayout(self.file_layout)

        self.create_graphic_view()

        self.btn_breadth_first.clicked.connect(self.start_bfs)
        self.btn_a_star.clicked.connect(self.start_astar)
        self.btn_import.clicked.connect(self.import_file)
        self.btn_set_maze.clicked.connect(self.set_maze)

        self.btn_stop.clicked.connect(self.stop_thread)
        self.btn_reset_maze.clicked.connect(self.set_maze)

        self.main_widget = Color('purple')
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)

    def start_bfs(self):
        maze1 = self.scene.bfs_arr
        if not self.runner:
            self.runner = BreadthFirstRunner(maze1)
            QThreadPool.globalInstance().start(self.runner)
            self.runner.signals.start_sig.connect(self.get_bfs_start_sig)
            self.runner.signals.update_sig.connect(self.get_bfs_sig)
            self.runner.signals.exit_sig.connect(self.get_bfs_exit_sig)
            self.runner.signals.count_sig.connect(self.get_count_sig)

    def stop_thread(self):
        if self.runner:
            self.runner.stop()
            if type(self.runner) == BreadthFirstRunner:
                self.runner.signals.start_sig.disconnect(self.get_bfs_start_sig)
                self.runner.signals.update_sig.disconnect(self.get_bfs_sig)
                self.runner.signals.exit_sig.disconnect(self.get_bfs_exit_sig)
                self.runner.signals.count_sig.disconnect(self.get_count_sig)
            else:
                self.runner.signals.start_sig.disconnect(self.get_astar_start_sig)
                self.runner.signals.update_sig.disconnect(self.get_astar_sig)
                self.runner.signals.update_sig2.disconnect(self.get_astar_sig2)
                self.runner.signals.exit_sig.disconnect(self.get_astar_exit_sig)
                self.runner.signals.count_sig.disconnect(self.get_count_sig)
            self.runner = None

    def start_astar(self):
        maze = self.scene.bfs_arr
        if not self.runner:
            self.runner = AStarRunner(maze)
            QThreadPool.globalInstance().start(self.runner)
            self.runner.signals.start_sig.connect(self.get_astar_start_sig)
            self.runner.signals.update_sig.connect(self.get_astar_sig)
            self.runner.signals.update_sig2.connect(self.get_astar_sig2)
            self.runner.signals.exit_sig.connect(self.get_astar_exit_sig)
            self.runner.signals.count_sig.connect(self.get_count_sig)

    def create_graphic_view(self):
        self.scene = GridScene(self.txtin_file.text(),8)

        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphic_view = QGraphicsView(self.scene, self)
        self.visualizer_layout.addWidget(graphic_view)

    def get_count_sig(self, num: int):
        self.num_elems_searched_label.setText(f"Operations Performed : {num}")

    def get_bfs_start_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end, QColor(30,235,71))

    def get_bfs_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end,QColor(25, 250, 255))

    def get_bfs_exit_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end, QColor(30,235,71))

    def get_astar_start_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end, QColor(30,235,71))

    def get_astar_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end,QColor(25, 250, 255))
    
    def get_astar_sig2(self, start: int, end: int):
        self.scene.set_cell_color(start,end,QColor(50,50,235))

    def get_astar_exit_sig(self, start: int, end: int):
        self.scene.set_cell_color(start,end, QColor(30,235,71))

    def import_file(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open PNG File', '', 'PNG Files (*.png)')
        self.txtin_file.setText(image_path)

    def set_maze(self):
        self.scene.clear()
        new_maze = self.txtin_file.text()
        self.scene.load_image(new_maze)
        self.num_elems_searched_label.setText("Operations Performed: 0")

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
        self.image_path = None
        self.bfs_arr = None

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

class SortingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sorting Visualizer")
        self.resize(1650, 1000)

        self.runner = None

        #MAIN LAYOUTS
        self.page_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.visualizer_layout = QVBoxLayout()

        self.scene = SortingScene()

        self.selector_layout = QHBoxLayout()

        self.num_elements_slider = QSlider(Qt.Horizontal)
        self.num_elements_slider.setMinimum(5)
        self.num_elements_slider.setMaximum(125)
        self.num_elements_slider.setTickInterval(1)
        self.num_elements_slider.setSingleStep(1)
        self.num_elements_slider.setValue(5)

        self.num_elements_display = QLabel(f"{self.num_elements_slider.value()}")
        self.num_elements_slider.valueChanged.connect(self.change_num_elems_label)
        self.btn_change_num_elements = QPushButton("Set new num elements")
        self.btn_change_num_elements.clicked.connect(self.update_num_elems)

        self.btn_quick_sort = QPushButton("Quick Sort")
        self.btn_select_sort = QPushButton("Selection Sort")
        self.btn_stop = QPushButton("Stop sorting")

        self.num_elems_searched_label = QLabel("Comparisons Performed: 0")
        self.num_elems_searched_label.setFixedHeight(40)

        self.button_layout.setContentsMargins(10,10,10,10)
        self.button_layout.setSpacing(20)
        self.button_layout.setAlignment(Qt.AlignHCenter)

        self.selector_layout.addWidget(self.num_elements_display)
        self.selector_layout.addWidget(self.num_elements_slider)
        self.selector_layout.addWidget(self.btn_change_num_elements)

        self.visualizer_layout.addLayout(self.selector_layout)
        
        self.create_graphic_view()

        self.button_layout.addWidget(self.btn_quick_sort)
        self.button_layout.addWidget(self.btn_select_sort)
        self.button_layout.addWidget(self.btn_stop)
        self.button_layout.addWidget(self.num_elems_searched_label)

        self.btn_quick_sort.clicked.connect(self.start_quicksort)
        self.btn_select_sort.clicked.connect(self.start_selectionsort)
        self.btn_stop.clicked.connect(self.stop_sorting)

        self.page_layout.addLayout(self.button_layout)
        self.page_layout.addLayout(self.visualizer_layout)

        self.main_widget = Color('purple')
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)
    
    def change_num_elems_label(self):
        self.num_elements_display.setText(f"{self.num_elements_slider.value()}")

    def create_graphic_view(self):
        self.scene.create_grid_based_on_input(self.num_elements_slider.value())

        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        self.graphic_view = QGraphicsView(self.scene, self)
        self.visualizer_layout.addWidget(self.graphic_view)

    def update_num_elems(self):
        num_elements = self.num_elements_slider.value()
        self.scene.create_grid_based_on_input(num_elements)
        self.graphic_view.setScene(self.scene)

    def start_quicksort(self):
        arr = self.scene.bar_lengths
        #if not self.runner:
        self.thread = SortingThread(arr)
        self.thread.start()
        self.thread.update_sig.connect(self.get_swap_sig)
        self.thread.num_comparison_sig.connect(self.get_count_sig)
            
            #QThreadPool.globalInstance().start(self.runner)
            #self.runner.signals.update_sig.connect(self.get_swap_sig)

    def start_selectionsort(self):
        arr = self.scene.bar_lengths
        self.thread = SelectionSortThread(arr)
        self.thread.start()
        self.thread.update_sig.connect(self.get_swap_sig)
        self.thread.num_comparison_sig.connect(self.get_count_sig)

    def stop_sorting(self):
        pass
        # if self.runner:
        #     self.runner.stop()
        #     self.runner.signals.update_sig.disconnect(self.get_swap_sig)

    def get_swap_sig(self, arr):
        self.scene.swap_bars(arr)

    def get_count_sig(self, count):
        self.num_elems_searched_label.setText(f"Comparisons Performed: {count}")



class SortingScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.pen = QPen(Qt.black, 2, Qt.SolidLine)
        self.bar_lengths = []
       #self.colors = []

    def create_grid_based_on_input(self, num_elements):
        self.clear()
        self.bar_lengths.clear()
        for i in range(1,num_elements+1):
            self.bar_lengths.append(i*5)

        random.shuffle(self.bar_lengths)

        spacing = 1
        bar_width = 10
        total_width = num_elements * (bar_width + spacing) - spacing
        scene_left = 50
        scene_top = 500
        scene_bottom = -800

        self.setSceneRect(scene_left, scene_top, total_width, scene_bottom)

        for i, bar_height in enumerate(self.bar_lengths):
            x_pos = scene_left + i * (bar_width + spacing)
            y_pos = scene_top - bar_height

            rect = self.addRect(x_pos, y_pos, bar_width, bar_height)

            pen = QPen(Qt.black, 2, Qt.SolidLine)
            rect.setPen(pen)
            #fill_in_color = QColor(random.randint(0, 50), random.randint(0, 200), random.randint(220, 255))
            brush = QBrush(QColor(50,200,255))
            #self.colors.append(fill_in_color)
            rect.setBrush(brush)

    def swap_bars(self, arr):
        self.bar_lengths = arr
        self.clear()
        spacing = 1
        bar_width = 10
        total_width = len(arr) * (bar_width + spacing) - spacing
        scene_left = 50
        scene_top = 500
        scene_bottom = -750

        self.setSceneRect(scene_left, scene_top, total_width, scene_bottom)

        for i, bar_height in enumerate(arr):
            x_pos = scene_left + i * (bar_width + spacing)
            y_pos = scene_top - bar_height

            rect = self.addRect(x_pos, y_pos, bar_width, bar_height)

            pen = QPen(Qt.black, 2, Qt.SolidLine)
            rect.setPen(pen)

            brush = QBrush(QColor(50,200,255))
            rect.setBrush(brush)
