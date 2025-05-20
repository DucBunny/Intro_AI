import random, datetime, csv, os
from tkinter import *
from color import COLOR
from collections import deque
from agent import agent
from typing import Dict, List, Tuple, Set, Optional, Union, Any

class maze:
    """
    Lớp maze biểu diễn một mê cung có thể tạo, hiển thị và thực hiện các thuật toán tìm đường.
    """
    
    def __init__(self, rows=10, cols=10):
        """
        Khởi tạo một mê cung với số hàng và cột xác định.
        
        Parameters:
            rows (int): Số hàng của mê cung
            cols (int): Số cột của mê cung
        """
        self.rows = rows
        self.cols = cols
        self.maze_map = {}
        self._grid = []
        self.path = {}
        self._cell_width = 50
        self._win = None
        self._canvas = None
        self._agents = []
        self.markCells = []
        self._goal = None
        self.theme = COLOR.MAZE
        self._LabWidth = 26  # Space from the top for Labels

    @property
    def grid(self):
        """Trả về lưới mê cung."""
        return self._grid
        
    @grid.setter
    def grid(self, n):
        """Khởi tạo lưới các ô và bản đồ mê cung."""
        self._grid = []
        for y in range(1, self.cols + 1):
            for x in range(1, self.rows + 1):
                self._grid.append((x, y))
                self.maze_map[(x, y)] = {0: 0, 1: 0, 2: 0, 3: 0}  # E, N, S, W
    
    def delta(self):
        """Trả về các vector hướng di chuyển: East(0), North(1), South(2), West(3)."""
        dx = [0, -1, 1, 0]  # E, N, S, W
        dy = [-1, 0, 0, 1]  # E, N, S, W
        return dx, dy
    
    def _open(self, x, y, d):
        """Mở tường giữa hai ô kề nhau."""
        dx, dy = self.delta()
        self.maze_map[x, y][d] = 1
        new_x = x + dx[d]
        new_y = y + dy[d] 
        if (new_x > 0 and new_x <= self.rows) and (new_y > 0 and new_y <= self.cols):
            self.maze_map[new_x, new_y][3-d] = 1  # Mở tường đối diện

    def CreateMaze(self, x=1, y=1, pattern=None, loopPercent=0, saveMaze=False, 
                   loadMaze=None, theme=COLOR.MAZE):
        """
        Tạo mê cung mới hoặc tải từ file.
        
        Parameters:
            x, y: Tọa độ điểm đích
            pattern: Mẫu tạo mê cung ('h' cho ngang, 'v' cho dọc)
            loopPercent: Phần trăm tạo thêm các vòng lặp
            saveMaze: Lưu mê cung vào file
            loadMaze: Đường dẫn file để tải mê cung
            theme: Màu sắc mê cung
        """
        self._goal = (x, y)
        self.theme = theme if not isinstance(theme, str) else COLOR[theme] if theme in COLOR.__members__ else COLOR.MAZE
            
        # Nếu tải mê cung từ file
        if loadMaze:
            self._load_maze_from_file(loadMaze)
        else:
            self._generate_random_maze(x, y, pattern, loopPercent)
            
        # Vẽ mê cung và thêm điểm đích
        self._drawMaze(self.theme)
        agent(self, *self._goal, shape='square', filled=True, color=COLOR.GOAL)
        
        # Lưu mê cung nếu yêu cầu
        if saveMaze:
            self._save_maze_to_file()
    
    def _generate_random_maze(self, x, y, pattern, loopPercent):
        """Tạo mê cung ngẫu nhiên bằng thuật toán DFS."""
        _stack = [(x, y)]
        _closed = [(x, y)]
        
        # Tham số cho mẫu
        bias_length = 2
        if pattern is not None:
            if pattern.lower() == 'h':
                bias_length = max(self.cols // 10, 2)
            elif pattern.lower() == 'v':
                bias_length = max(self.rows // 10, 2)
        bias = 0
        dx, dy = self.delta()
        
        # Thuật toán DFS tạo mê cung
        while _stack:
            x, y = _stack[-1]
            cell_options = []
            bias += 1
            
            # Kiểm tra các ô kề
            for d in range(4):
                new_x = x + dx[d]
                new_y = y + dy[d]
                if (new_x, new_y) not in _closed and (new_x, new_y) in self.grid:
                    cell_options.append(d)
            
            if cell_options:
                # Áp dụng mẫu nếu được chỉ định
                if pattern is not None and pattern.lower() == 'h' and bias <= bias_length:
                    if 3 in cell_options or 0 in cell_options:
                        if 2 in cell_options: cell_options.remove(2)
                        if 1 in cell_options: cell_options.remove(1)
                elif pattern is not None and pattern.lower() == 'v' and bias <= bias_length:
                    if 1 in cell_options or 2 in cell_options:
                        if 3 in cell_options: cell_options.remove(3)
                        if 0 in cell_options: cell_options.remove(0)
                else:
                    bias = 0
                
                # Chọn ngẫu nhiên một hướng
                d = random.choice(cell_options)
                self._open(x, y, d)
                new_x = x + dx[d]
                new_y = y + dy[d]
                self.path[(new_x, new_y)] = (x, y)
                x, y = new_x, new_y
                _closed.append((x, y))
                _stack.append((x, y))
            else:
                _stack.pop()
        
        # Thêm các vòng lặp
        if loopPercent > 0:
            self._add_loops(loopPercent)
            self._update_path()
    
    def _add_loops(self, loopPercent):
        """Thêm các vòng lặp vào mê cung để tạo nhiều đường đi."""
        def blocked_neighbours(cell):
            """Tìm các ô kề mà chưa thông với cell."""
            n = []
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d] == 0:
                    dx, dy = self.delta()
                    new_x = cell[0] + dx[d]
                    new_y = cell[1] + dy[d]
                    if (new_x, new_y) in self.grid:
                        n.append((new_x, new_y))
            return n
            
        def remove_wall_between(cell1, cell2):
            """Xóa tường giữa hai ô."""
            if cell1[0] == cell2[0]:  # Cùng hàng
                if cell1[1] == cell2[1] + 1:  # cell1 ở bên phải cell2
                    self.maze_map[cell1][0] = 1  # Mở East của cell1
                    self.maze_map[cell2][3] = 1  # Mở West của cell2
                else:  # cell1 ở bên trái cell2
                    self.maze_map[cell1][3] = 1  # Mở West của cell1
                    self.maze_map[cell2][0] = 1  # Mở East của cell2
            else:  # Cùng cột
                if cell1[0] == cell2[0] + 1:  # cell1 ở bên dưới cell2
                    self.maze_map[cell1][1] = 1  # Mở North của cell1
                    self.maze_map[cell2][2] = 1  # Mở South của cell2
                else:  # cell1 ở bên trên cell2
                    self.maze_map[cell1][2] = 1  # Mở South của cell1
                    self.maze_map[cell2][1] = 1  # Mở North của cell2
        
        def is_cyclic(cell1, cell2):
            """Kiểm tra xem việc xóa tường giữa cell1 và cell2 có tạo chu trình không."""
            if cell1[0] == cell2[0]:  # Cùng hàng
                if cell1[1] > cell2[1]: 
                    cell1, cell2 = cell2, cell1
                # Kiểm tra tạo chu trình qua phía trên
                if self.maze_map[cell1][2] == 1 and self.maze_map[cell2][2] == 1:
                    if (cell1[0]+1, cell1[1]) in self.grid and self.maze_map[(cell1[0]+1, cell1[1])][3] == 1:
                        return True
                # Kiểm tra tạo chu trình qua phía dưới
                if self.maze_map[cell1][1] == 1 and self.maze_map[cell2][1] == 1:
                    if (cell1[0]-1, cell1[1]) in self.grid and self.maze_map[(cell1[0]-1, cell1[1])][3] == 1:
                        return True
            else:  # Cùng cột
                if cell1[0] > cell2[0]: 
                    cell1, cell2 = cell2, cell1
                # Kiểm tra tạo chu trình qua phía phải
                if self.maze_map[cell1][3] == 1 and self.maze_map[cell2][3] == 1:
                    if (cell1[0], cell1[1]+1) in self.grid and self.maze_map[(cell1[0], cell1[1]+1)][2] == 1:
                        return True
                # Kiểm tra tạo chu trình qua phía trái
                if self.maze_map[cell1][0] == 1 and self.maze_map[cell2][0] == 1:
                    if (cell1[0], cell1[1]-1) in self.grid and self.maze_map[(cell1[0], cell1[1]-1)][2] == 1:
                        return True
            return False
        
        # Lấy các ô trên đường đi và ngoài đường đi
        x, y = self.rows, self.cols
        path_cells = [(x, y)]
        while (x, y) != self._goal:
            try:
                x, y = self.path[(x, y)]
                path_cells.append((x, y))
            except KeyError:
                break
                
        not_path_cells = [i for i in self.grid if i not in path_cells]
        random.shuffle(path_cells)
        random.shuffle(not_path_cells)
        
        # Tính số lượng tường cần xóa
        path_length = len(path_cells)
        not_path_length = len(not_path_cells)
        count1 = path_length / 3 * loopPercent / 100
        count2 = not_path_length / 3 * loopPercent / 100
        
        # Xóa tường từ các ô trên đường đi
        count = 0
        i = 0
        while count < count1 and i < len(path_cells):
            neighbors = blocked_neighbours(path_cells[i])
            if neighbors:
                cell = random.choice(neighbors)
                if not is_cyclic(cell, path_cells[i]):
                    remove_wall_between(cell, path_cells[i])
                    count += 1
            i += 1
            
        # Xóa tường từ các ô ngoài đường đi
        if not_path_cells:
            count = 0
            i = 0
            while count < count2 and i < len(not_path_cells):
                neighbors = blocked_neighbours(not_path_cells[i])
                if neighbors:
                    cell = random.choice(neighbors)
                    if not is_cyclic(cell, not_path_cells[i]):
                        remove_wall_between(cell, not_path_cells[i])
                        count += 1
                i += 1
    
    def _update_path(self):
        """Cập nhật đường đi ngắn nhất sau khi thêm các vòng lặp."""
        dx, dy = self.delta()
        frontier = deque([(self.rows, self.cols)])
        path = {}
        visited = {(self.rows, self.cols)}
        
        while frontier:
            cell = frontier.popleft()
            if cell == self._goal:
                break
                
            for d in range(4):
                if self.maze_map[cell][d] == 1:
                    next_cell = (cell[0] + dx[d], cell[1] + dy[d])
                    if next_cell not in visited:
                        path[next_cell] = cell
                        frontier.append(next_cell)
                        visited.add(next_cell)
        
        # Tạo đường đi từ goal đến start
        fwd_path = {}
        cell = self._goal
        while cell != (self.rows, self.cols):
            try:
                fwd_path[path[cell]] = cell
                cell = path[cell]
            except:
                print('Không tìm thấy đường đi đến đích!')
                return
                
        self.path = path
    
    def _load_maze_from_file(self, file_path):
        """Tải mê cung từ file CSV."""
        # Đọc kích thước mê cung
        with open(file_path, 'r') as f:
            last = list(f.readlines())[-1]
            c = last.split(',')
            c[0] = int(c[0].lstrip('"('))
            c[1] = int(c[1].rstrip(')"'))
            self.rows = c[0]
            self.cols = c[1]
            self.grid = []  # Trigger setter

        # Đọc bản đồ mê cung
        with open(file_path, 'r') as f:
            r = csv.reader(f)
            next(r)  # Bỏ qua header
            for i in r:
                c = i[0].split(',')
                c[0] = int(c[0].lstrip('('))
                c[1] = int(c[1].rstrip(')'))
                self.maze_map[tuple(c)] = {
                    3: int(i[1]),
                    0: int(i[2]),
                    1: int(i[3]),
                    2: int(i[4])
                }
        
        # Tính đường đi
        self._update_path()
    
    def _save_maze_to_file(self):
        """Lưu mê cung vào file CSV."""
        dt_string = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        with open(f'maze--{dt_string}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['  cell  ', 3, 0, 1, 2])
            for k, v in self.maze_map.items():
                entry = [k]
                for i in v.values():
                    entry.append(i)
                writer.writerow(entry)
    
    def _drawMaze(self, theme):
        """Vẽ mê cung trên canvas."""
        # Khởi tạo cửa sổ và canvas
        self._win = Tk()
        self._win.state('zoomed')
        self._win.title('Maze')
        
        scr_width = self._win.winfo_screenwidth()
        scr_height = self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0])
        self._canvas.pack(expand=YES, fill=BOTH)
        
        # Tính toán kích thước ô mê cung
        k = self._calculate_cell_width_factor()
        self._cell_width = round(min(
            ((scr_height - self.rows - k * self._LabWidth) / self.rows),
            ((scr_width - self.cols - k * self._LabWidth) / self.cols),
            90
        ), 3)
        
        # Vẽ các đường tường của mê cung
        if self._win and self.grid:
            for cell in self.grid:
                x, y = cell
                w = self._cell_width
                x = x * w - w + self._LabWidth
                y = y * w - w + self._LabWidth
                # Vẽ các bức tường
                if not self.maze_map[cell][3]:  # East wall
                    self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][0]:  # West wall
                    self._canvas.create_line(y, x, y, x + w, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][1]:  # North wall
                    self._canvas.create_line(y, x, y + w, x, width=2, fill=theme.value[1], tag='line')
                if not self.maze_map[cell][2]:  # South wall
                    self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill=theme.value[1], tag='line')
    
    def _calculate_cell_width_factor(self):
        """Tính toán hệ số điều chỉnh kích thước ô theo kích thước mê cung."""
        if self.rows >= 95 and self.cols >= 95:
            return 0
        elif self.rows >= 80 and self.cols >= 80:
            return 1
        elif self.rows >= 70 and self.cols >= 70:
            return 1.5
        elif self.rows >= 50 and self.cols >= 50:
            return 2
        elif self.rows >= 35 and self.cols >= 35:
            return 2.5
        elif self.rows >= 22 and self.cols >= 22:
            return 3
        return 3.25

    def _redrawCell(self, x, y, theme):
        """Vẽ lại một ô trong mê cung với màu mới."""
        w = self._cell_width
        cell = (x, y)
        x = x * w - w + self._LabWidth
        y = y * w - w + self._LabWidth
        # Vẽ các bức tường
        if not self.maze_map[cell][3]:  # East
            self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill=theme.value[1])
        if not self.maze_map[cell][0]:  # West
            self._canvas.create_line(y, x, y, x + w, width=2, fill=theme.value[1])
        if not self.maze_map[cell][1]:  # North
            self._canvas.create_line(y, x, y + w, x, width=2, fill=theme.value[1])
        if not self.maze_map[cell][2]:  # South
            self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill=theme.value[1])

    # Biến lưu danh sách các đường đi cần vẽ
    _tracePathList = []
    
    def _tracePathSingle(self, a, p, kill, show_marked, delay):
        """Vẽ từng bước di chuyển của một agent theo đường đi p."""
        def kill_agent(a):
            """Xóa agent khỏi canvas."""
            for i in range(len(a._body)):
                self._canvas.delete(a._body[i])
            self._canvas.delete(a._head)
            
        # Đánh dấu ô đặc biệt nếu cần
        if (a.x, a.y) in self.markCells and show_marked:
            w = self._cell_width
            x = a.x * w - w + self._LabWidth
            y = a.y * w - w + self._LabWidth
            self._canvas.create_oval(
                y + w/2.5 + w/20, x + w/2.5 + w/20,
                y + w/2.5 + w/4 - w/20, x + w/2.5 + w/4 - w/20,
                fill='red', outline='red', tag='ov'
            )
            self._canvas.tag_raise('ov')

        # Kiểm tra nếu đã đến đích
        if (a.x, a.y) == a.goal:
            del maze._tracePathList[0][0][a]
            if not maze._tracePathList[0][0]:
                del maze._tracePathList[0]
                if maze._tracePathList:
                    self.tracePath(
                        maze._tracePathList[0][0],
                        kill=maze._tracePathList[0][1],
                        delay=maze._tracePathList[0][2]
                    )
            if kill:
                self._win.after(300, kill_agent, a)
            return
        
        # Xử lý dựa trên loại đường đi
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
                    if maze._tracePathList:
                        self.tracePath(
                            maze._tracePathList[0][0],
                            kill=maze._tracePathList[0][1],
                            delay=maze._tracePathList[0][2]
                        )
                if kill:
                    self._win.after(300, kill_agent, a)
                return
        
        elif isinstance(p, list):
            if not p:
                del maze._tracePathList[0][0][a]
                if not maze._tracePathList[0][0]:
                    del maze._tracePathList[0]
                    if maze._tracePathList:
                        self.tracePath(
                            maze._tracePathList[0][0],
                            kill=maze._tracePathList[0][1],
                            delay=maze._tracePathList[0][2]
                        )
                if kill:                    
                    self._win.after(300, kill_agent, a)
                return
            a.x, a.y = p[0]
            del p[0]

        # Lên lịch bước di chuyển tiếp theo
        self._win.after(delay, self._tracePathSingle, a, p, kill, show_marked, delay)

    def tracePath(self, d, kill=False, delay=100, showMarked=False):
        """
        Vẽ đường đi của các agent trên mê cung.
        
        Parameters:
            d: Dictionary chứa các agent và đường đi tương ứng
            kill: Có xóa agent sau khi hoàn thành không
            delay: Độ trễ giữa các bước (ms)
            showMarked: Có hiển thị các ô đặc biệt không
        """
        self._tracePathList.append((d, kill, delay))
        if maze._tracePathList[0][0] == d:
            for a, p in d.items():
                if a.goal != (a.x, a.y) and p:
                    self._tracePathSingle(a, p, kill, showMarked, delay)

    def run(self):
        """Chạy và hiển thị cửa sổ mê cung."""
        self._win.mainloop()