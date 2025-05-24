import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from textLabel import textLabel
from queue import PriorityQueue

# Hàm heuristic sử dụng khoảng cách Manhattan
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)
    
def aStar(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]
        
    # Khởi tạo hàng đợi ưu tiên
    open_set = PriorityQueue()
    open_set.put((h(start, m._goal), h(start, m._goal), start))
    
    # Khởi tạo dictionary lưu trữ
    path_dict = {}

    g_score = {cell: float("inf") for cell in m.grid}
    g_score[start] = 0

    f_score = {cell: float("inf") for cell in m.grid}
    f_score[start] = h(start, m._goal)
    
    # Lưu các ô đã khám phá
    search_path = [start]
    
    while not open_set.empty():
        # Lấy ô có f_score thấp nhất
        currCell = open_set.get()[2]
        search_path.append(currCell)
        
        # Đã tìm thấy đích
        if currCell == m._goal:
            break
            
        # Khám phá các ô kề
        for d in range(4):
            if m.maze_map[currCell][d]:
                child = (currCell[0] + dx[d], currCell[1] + dy[d])

                # Tính toán g_score và f_score mới
                temp_g_score = g_score[currCell] + 1

                # Nếu tìm thấy đường đi tốt hơn
                if temp_g_score < g_score[child]:   
                    path_dict[child] = currCell
                    g_score[child] = temp_g_score
                    f_score[child] = temp_g_score + h(child, m._goal)
                    open_set.put((f_score[child], h(child, m._goal), child))

    # Tạo đường đi từ điểm bắt đầu đến đích
    forward_path = {}
    cell = m._goal

    # Kiểm tra nếu không tìm thấy đường đi
    # if m._goal not in path_dict and start != m._goal:
    #     print("No path found from start to goal!")
    #     return search_path, path_dict, forward_path
    
    while cell != start:
        forward_path[path_dict[cell]] = cell
        cell = path_dict[cell]
        
    return search_path, path_dict, forward_path


if __name__ == '__main__':
    my_maze = maze(30, 30)
    my_maze.CreateMaze(6, 4, loopPercent=100)

    search_path, path_dict, forward_path = aStar(my_maze, (1, 12))

    # Hiển thị quá trình tìm kiếm 
    agent_search = agent(my_maze, 1, 12, goal=(6, 4), filled=True, footprints=True, color=COLOR.SEARCH)

    # Hiển thị quan hệ cha-con
    agent_parent = agent(my_maze, 6, 4, goal=(1, 12), filled=True, footprints=True, color=COLOR.PARENT)

    # Hiển thị đường đi tối ưu
    agent_optimal = agent(my_maze, 1, 12, goal=(6, 4), footprints=True, color=COLOR.PATH)
    
    # Hiển thị các đường đi
    my_maze.tracePath({agent_search: search_path}, delay=100)
    my_maze.tracePath({agent_parent: path_dict}, delay=100)
    my_maze.tracePath({agent_optimal: forward_path}, delay=100)

    # Hiển thị thông tin độ dài đường đi
    textLabel(my_maze, 'A Star Forward Path', len(forward_path) + 1)
    textLabel(my_maze, 'A Star Search Path', len(search_path))

    my_maze.run()