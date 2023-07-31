from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_widgets import *
from ui_help import *
import time
import random
from collections import deque
import heapq

# just do bfs for now
class BreadthFirstSignals(QObject):
    start_sig = Signal(int,int)
    update_sig = Signal(int, int)  #index to update
    exit_sig = Signal(int, int)

class BreadthFirstRunner(QRunnable):
    def __init__(self, grid):
        super().__init__()
        self.signals = BreadthFirstSignals()
        self.stop_flag = False
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def stop(self):
        self.stop_flag = True

    def find_next_states(self, state) -> list[list]:
        next_states = [
            [state[0]-1,state[1]],
            [state[0]+1,state[1]],
            [state[0],state[1]-1],
            [state[0],state[1]+1]
        ]
        return next_states
    

    def run(self):
        my_queue = deque()
        explored = [[False for _ in range(self.cols)] for _ in range(self.rows)]


        #find start state
        for i in range(self.rows):
            if self.grid[i][0] == 8:
                s = [i,0]
                self.signals.start_sig.emit(i,0)


        my_queue.append(s)

        explored[s[0]][s[1]] = True

        while_end = True

        while(while_end == True and self.stop_flag == False):
            if (len(my_queue) == 0):
                while_end = False
            else:
                s = my_queue.popleft()

                next_states = []

                next_states = self.find_next_states(s)
                
                for i in range(len(next_states)):
                    if (self.grid[next_states[i][0]][next_states[i][1]] != 2 and explored[next_states[i][0]][next_states[i][1]] != True):
                        if (next_states[i][0] == 0 or next_states[i][1] == 0 or next_states[i][0] == len(self.grid)-1 or next_states[i][1] == len(self.grid[0])-1):
                            self.signals.exit_sig.emit(next_states[i][0],next_states[i][1])
                            return next_states[i]
                        else:
                            print(f"explored element: {next_states[i]}")
                            self.signals.update_sig.emit(next_states[i][0],next_states[i][1])
                            my_queue.append(next_states[i])
                            explored[next_states[i][0]][next_states[i][1]] = True
            time.sleep(0.005)

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class AStarSignals(QObject):
    start_sig = Signal(int,int)
    update_sig = Signal(int,int)
    update_sig2 = Signal(int,int)
    exit_sig = Signal(int,int)
    

class AStarRunner(QRunnable):
    def __init__(self, grid):
        super().__init__()
        self.signals = AStarSignals()
        self.stop_flag = False
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
    
    def stop(self):
        self.stop_flag = True

    def heuristic(self, node, goal):
        return abs(node.x - goal.x) + abs(node.y - goal.y)#dist

    def get_neighbors(self, maze, node):
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 2:
                neighbors.append(Node(nx, ny, node))
        return neighbors

    def run(self):

        #find start state
        for i in range(self.rows):
            if self.grid[i][0] == 8:
                s = [i,0]
                self.signals.start_sig.emit(i,0)
                print("HELLOOOOOOOOOOOOO")
                print("HELLOOOOOOOOOOOOO")
                print("HELLOOOOOOOOOOOOO")
                print("HELLOOOOOOOOOOOOO")
        
        #find end state
        for i in range(self.rows):
            if self.grid[i][self.cols-1] == 8:
                e = [i,self.cols-1]
                self.signals.exit_sig.emit(i,self.cols-1)
        
        open_list = []
        closed_set = set()

        start_node = Node(s[0], s[1])
        goal_node = Node(e[0], e[1])

        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            self.signals.update_sig.emit(current_node.x,current_node.y)

            if current_node.x == goal_node.x and current_node.y == goal_node.y:
                path = []
                while current_node:
                    self.signals.update_sig2.emit(current_node.x,current_node.y)
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]

            closed_set.add((current_node.x, current_node.y))

            for neighbor in self.get_neighbors(self.grid, current_node):
                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                tentative_g = current_node.g + 1
                if neighbor not in open_list or tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor, goal_node)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node

                    if neighbor not in open_list:
                        heapq.heappush(open_list, neighbor)
            time.sleep(0.005)
        return None