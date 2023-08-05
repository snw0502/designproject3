# Design Project 3 - Algorithm Visualizer
Junior Design Project 3 - Shelby Wilson

Pathfinding Visualizer: Breadth First Search, A* Algorithm
Sorting Visualizer: Quick Sort, Selection Sort

Navigating this repository:

project3/mazes directory:

      * includes pre-generated mazes (from the maze generator linked below) for use in the pathfinding visualizer

project3/project3_qt:

      * main project files:
          * algorithms_backend.py: contains all back-end components (Algorithm Runners and Signal containers that run the algorithms and send signals to front-end)
          * main.py: main program file, run the application using this file and python3 interpreter
          * ui_base.py: contains all front-end components: (main windows and customized QGraphicsScene objects)

project3/solved_mazes_ref:

      * includes all pre-generated mazes solved using A* on the maze generator linked below. 
      * included to show that my application produces the correct shortest path


MODULES/LIBRARIES NEEDED:
  PySide6: pip install pyside6
  Qt-material: pip install qt-material

  General Python Libraries: time, PIL, collections/deque, heapq, random
  
GUI Framework Used:
https://pypi.org/project/PySide6/

https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html


Other Resources:

(app theme: Dark Cyan)
https://github.com/UN-GCPDS/qt-material

(maze generator for pathfinding algorithms)
https://keesiemeijer.github.io/maze-generator/

(algorithm help)
https://www.geeksforgeeks.org/implementation-of-bfs-using-adjacency-matrix/

https://www.geeksforgeeks.org/a-search-algorithm/

https://www.geeksforgeeks.org/quick-sort/

https://www.geeksforgeeks.org/python-program-for-selection-sort/
