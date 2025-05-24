import random
from tkinter import *
from color import COLOR
from collections import deque
from agent import agent

class maze:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.maze_map = {}
        self.grid = []
        self.path = {} 
        self._cell_width = 50  
        self._win = None 
        self._canvas = None
        self._agents = []
        self.markCells = []

    @property
    def grid(self):
        return self._grid
        
    @grid.setter        
    def grid(self, n):
        self._grid = []
        for col in range(self.cols):
            x = 1
            y = col + 1
            for row in range(self.rows):
                self._grid.append((x, y))
                self.maze_map[x, y] = {0: 0, 1: 0, 2: 0, 3: 0}
                x += 1 
                
    def delta(self):
        # 0:North, 1:East, 2:West, 3:South
        return [0, -1, 1, 0], [-1, 0, 0, 1]
    
    def _Open(self, x, y, d):
        dx, dy = self.delta()
        self.maze_map[x, y][d] = 1
        newX = x + dx[d]
        newY = y + dy[d] 
        if (newX > 0 and newX <= self.rows) and (newY > 0 and newY <= self.cols):
            self.maze_map[newX, newY][3-d] = 1

    def CreateMaze(self, x=1, y=1, pattern=None, loopPercent=0, theme=COLOR.MAZE):
        _stack = []
        _closed = []
        self.theme = theme
        self._goal = (x, y)
        
        if isinstance(theme, str):
            if theme in COLOR.__members__:
                self.theme = COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')
                
        def blockedNeighbours(cell):
            n = []
            dx, dy = self.delta()
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d] == 0:
                    newX = cell[0] + dx[d]
                    newY = cell[1] + dy[d]
                    if (newX, newY) in self.grid:
                        n.append((newX, newY))
            return n
            
        def removeWallinBetween(cell1, cell2):
            if cell1[0] == cell2[0]:
                if cell1[1] == cell2[1] + 1:
                    self.maze_map[cell1][0] = 1
                    self.maze_map[cell2][3] = 1
                else:
                    self.maze_map[cell1][3] = 1
                    self.maze_map[cell2][0] = 1
            else:
                if cell1[0] == cell2[0] + 1:
                    self.maze_map[cell1][1] = 1
                    self.maze_map[cell2][2] = 1
                else:
                    self.maze_map[cell1][2] = 1
                    self.maze_map[cell2][1] = 1
                    
        def isCyclic(cell1, cell2):
            if cell1[0] == cell2[0]:
                if cell1[1] > cell2[1]: 
                    cell1, cell2 = cell2, cell1
                if self.maze_map[cell1][2] == 1 and self.maze_map[cell2][2] == 1:
                    if (cell1[0]+1, cell1[1]) in self.grid and self.maze_map[(cell1[0]+1, cell1[1])][3] == 1:
                        return True
                if self.maze_map[cell1][1] == 1 and self.maze_map[cell2][1] == 1:
                    if (cell1[0]-1, cell1[1]) in self.grid and self.maze_map[(cell1[0]-1, cell1[1])][3] == 1:
                        return True
            else:
                if cell1[0] > cell2[0]: 
                    cell1, cell2 = cell2, cell1
                if self.maze_map[cell1][3] == 1 and self.maze_map[cell2][3] == 1:
                    if (cell1[0], cell1[1]+1) in self.grid and self.maze_map[(cell1[0], cell1[1]+1)][2] == 1:
                        return True
                if self.maze_map[cell1][0] == 1 and self.maze_map[cell2][0] == 1:
                    if (cell1[0], cell1[1]-1) in self.grid and self.maze_map[(cell1[0], cell1[1]-1)][2] == 1:
                        return True
            return False
            
        def BFS(cell):
            dx, dy = self.delta()
            frontier = deque([cell])
            path = {}
            visited = {(self.rows, self.cols)}
            
            while frontier:
                cell = frontier.popleft()
                for d in range(4):
                    nextCell = (cell[0] + dx[d], cell[1] + dy[d])
                    if self.maze_map[cell][d] == 1 and nextCell not in visited:
                        path[nextCell] = cell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                        
            fwdPath = {}
            cell = self._goal
            while cell != (self.rows, self.cols):
                try:
                    fwdPath[path[cell]] = cell
                    cell = path[cell]
                except:
                    print('Path to goal not found!')
                    return
            return fwdPath

        # Generate maze
        _stack.append((x, y))
        _closed.append((x, y))
        biasLength = 2  # if pattern is 'v' or 'h'
        
        if pattern is not None:
            if pattern.lower() == 'h':
                biasLength = max(self.cols // 10, 2)
            elif pattern.lower() == 'v':
                biasLength = max(self.rows // 10, 2)
                
        bias = 0
        dx, dy = self.delta()
        
        while _stack:
            cell = []
            bias += 1
            
            for d in range(4):
                newX = x + dx[d]
                newY = y + dy[d]
                if (newX, newY) not in _closed and (newX, newY) in self.grid:
                    cell.append(d)
                    
            if cell:    
                if pattern is not None:
                    if pattern.lower() == 'h' and bias <= biasLength:
                        if 3 in cell or 0 in cell:
                            if 2 in cell: cell.remove(2)
                            if 1 in cell: cell.remove(1)
                    elif pattern.lower() == 'v' and bias <= biasLength:
                        if 1 in cell or 2 in cell:
                            if 3 in cell: cell.remove(3)
                            if 0 in cell: cell.remove(0)
                    else:
                        bias = 0
                        
                current_cell = random.choice(cell)
                self._Open(x, y, current_cell)
                newX = x + dx[current_cell]
                newY = y + dy[current_cell]
                self.path[newX, newY] = x, y
                x, y = newX, newY
                _closed.append((x, y))
                _stack.append((x, y))
            else:
                x, y = _stack.pop()

        # Multiple Path Loops
        if loopPercent != 0:
            x, y = self.rows, self.cols
            pathCells = [(x, y)]
            
            while x != self.rows or y != self.cols:
                x, y = self.path[(x, y)]
                pathCells.append((x, y))
                
            notPathCells = [i for i in self.grid if i not in pathCells]
            random.shuffle(pathCells)
            random.shuffle(notPathCells)
            
            pathLength = len(pathCells)
            notPathLength = len(notPathCells)
            count1 = pathLength / 3 * loopPercent / 100
            count2 = notPathLength / 3 * loopPercent / 100
            
            # Remove blocks from shortest path cells
            count, i = 0, 0
            while count < count1:
                if i >= len(pathCells):
                    break
                    
                neighbors = blockedNeighbours(pathCells[i])
                if neighbors:
                    cell = random.choice(neighbors)
                    if not isCyclic(cell, pathCells[i]):
                        removeWallinBetween(cell, pathCells[i])
                        count += 1
                i += 1
                    
            # Remove blocks from outside shortest path cells
            if notPathCells:
                count, i = 0, 0
                while count < count2:
                    if i >= len(notPathCells):
                        break
                        
                    neighbors = blockedNeighbours(notPathCells[i])
                    if neighbors:
                        cell = random.choice(neighbors)
                        if not isCyclic(cell, notPathCells[i]):
                            removeWallinBetween(cell, notPathCells[i])
                            count += 1
                    i += 1
                        
            self.path = BFS((self.rows, self.cols))
            
        self._drawMaze(self.theme)
        agent(self, *self._goal, shape='square', filled=True, color=COLOR.GOAL)

    def _drawMaze(self, theme):
        self._LabWidth = 26  # Space from the top for Labels
        self._win = Tk()
        self._win.state('zoomed')
        self._win.title('Maze')
        
        scr_width = self._win.winfo_screenwidth()
        scr_height = self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0])
        self._canvas.pack(expand=YES, fill=BOTH)
        
        # Calculate cell width based on maze dimensions
        k = 3.25
        if self.rows >= 95 and self.cols >= 95:
            k = 0
        elif self.rows >= 80 and self.cols >= 80:
            k = 1
        elif self.rows >= 70 and self.cols >= 70:
            k = 1.5
        elif self.rows >= 50 and self.cols >= 50:
            k = 2
        elif self.rows >= 35 and self.cols >= 35:
            k = 2.5
        elif self.rows >= 22 and self.cols >= 22:
            k = 3
            
        self._cell_width = round(min(
            ((scr_height - self.rows - k * self._LabWidth) / (self.rows)),
            ((scr_width - self.cols - k * self._LabWidth) / (self.cols)),
            90
        ), 3)
        
        # Draw maze walls
        if self.grid:
            for cell in self.grid:
                x, y = cell
                w = self._cell_width
                x = x * w - w + self._LabWidth
                y = y * w - w + self._LabWidth
                
                if not self.maze_map[cell][3]:
                    self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][0]:
                    self._canvas.create_line(y, x, y, x + w, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][1]:
                    self._canvas.create_line(y, x, y + w, x, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][2]:
                    self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill=theme.value[1], tag='line')

    def _redrawCell(self, x, y, theme):
        w = self._cell_width
        cell = (x, y)
        x = x * w - w + self._LabWidth
        y = y * w - w + self._LabWidth
        
        if not self.maze_map[cell][3]:
            self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill=theme.value[1])
        if not self.maze_map[cell][0]:
            self._canvas.create_line(y, x, y, x + w, width=2, fill=theme.value[1])
        if not self.maze_map[cell][1]:
            self._canvas.create_line(y, x, y + w, x, width=2, fill=theme.value[1])
        if not self.maze_map[cell][2]:
            self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill=theme.value[1])

    _tracePathList = []
    
    def _tracePathSingle(self, a, p, kill, showMarked, delay):
        def killAgent(a):
            for i in range(len(a._body)):
                self._canvas.delete(a._body[i])
            self._canvas.delete(a._head) 
            
        w = self._cell_width
        if (a.x, a.y) in self.markCells and showMarked:
            x = a.x * w - w + self._LabWidth
            y = a.y * w - w + self._LabWidth
            self._canvas.create_oval(
                y + w/2.5 + w/20, 
                x + w/2.5 + w/20,
                y + w/2.5 + w/4 - w/20, 
                x + w/2.5 + w/4 - w/20,
                fill='red', outline='red', tag='ov'
            )
            self._canvas.tag_raise('ov')

        if (a.x, a.y) == a.goal:
            del maze._tracePathList[0][0][a]
            if not maze._tracePathList[0][0]:
                del maze._tracePathList[0]
                if len(maze._tracePathList) > 0:
                    self.tracePath(
                        maze._tracePathList[0][0],
                        kill=maze._tracePathList[0][1],
                        delay=maze._tracePathList[0][2]
                    )
            if kill:
                self._win.after(300, killAgent, a)         
            return
            
        # Handle different path formats
        if isinstance(p, dict):
            if not p:
                del maze._tracePathList[0][0][a]
                return 
            a.x, a.y = p[(a.x, a.y)]
            
        elif isinstance(p, str):
            if not p:
                del maze._tracePathList[0][0][a]
                if not maze._tracePathList[0][0]:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList) > 0:
                        self.tracePath(
                            maze._tracePathList[0][0],
                            kill=maze._tracePathList[0][1],
                            delay=maze._tracePathList[0][2]
                        )
                if kill:
                    self._win.after(300, killAgent, a)         
                return

        elif isinstance(p, list):
            if not p:
                del maze._tracePathList[0][0][a]
                if not maze._tracePathList[0][0]:
                    del maze._tracePathList[0]
                    if len(maze._tracePathList) > 0:
                        self.tracePath(
                            maze._tracePathList[0][0],
                            kill=maze._tracePathList[0][1],
                            delay=maze._tracePathList[0][2]
                        )
                if kill:                    
                    self._win.after(300, killAgent, a)  
                return  
            a.x, a.y = p[0]
            del p[0]

        self._win.after(delay, self._tracePathSingle, a, p, kill, showMarked, delay)    

    def tracePath(self, d, kill=False, delay=100, showMarked=False):
        self._tracePathList.append((d, kill, delay))
        if maze._tracePathList[0][0] == d: 
            for a, p in d.items():
                if a.goal != (a.x, a.y) and p:
                    self._tracePathSingle(a, p, kill, showMarked, delay)
                    
    def run(self):
        self._win.mainloop()