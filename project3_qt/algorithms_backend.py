from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
import time
import random
from collections import deque

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


class AlgorithmHandler():
    def __init__(self, algorithm: str, grid: list[list]):
        self.algorithm = algorithm
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    def breadth_first_search(self, grid):
        my_queue = deque()
        explored = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        s = [7,1]

        my_queue.append(s)

        explored[s[0]][s[1]] = True

        while_end = True

        while(while_end == True):
            if (len(my_queue) == 0):
                while_end = False
            else:
                s = my_queue.popleft()

                next_states = []

                if (s[0] != 0 and s[1] != 0):
                    next_states = self.find_next_states(s)
                
                for i in range(len(next_states)):
                    if (grid[next_states[i][0]][next_states[i][1]] != 2 and explored[next_states[i][0]][next_states[i][1]] != True):
                        if (next_states[i][0] == 0 or next_states[i][1] == 0 or next_states[i][0] == len(grid)-1 or next_states[i][1] == len(grid[0])-1):
                            return next_states[i]
                        else:
                            print(f"explored element: {next_states[i]}")
                            my_queue.append(next_states[i])
                            explored[next_states[i][0]][next_states[i][1]] = True
        
        return [-1,-1]
        
    
    def find_next_states(self, state) -> list[list]:
        next_states = [
            [state[0]-1,state[1]],
            [state[0]+1,state[1]],
            [state[0],state[1]-1],
            [state[0],state[1]+1]
        ]
        return next_states
        
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
test = AlgorithmHandler("a",maze1)
print(test.breadth_first_search(maze1))