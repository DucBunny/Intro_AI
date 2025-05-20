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
    return (abs(x1 - x2) + abs(y1 - y2))
    
def aStar(m, start=None):
    if start is None:
        start = (m.rows, m.cols) # Điểm bắt đầu mặc định là góc dưới bên trái của mê cung
    
    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]

    open_set = PriorityQueue()
    open_set.put((h(start, m._goal), h(start, m._goal), start))
    
    # Dictionary lưu đường đi
    path_dict = {}
    
    # Chi phí từ điểm bắt đầu đến mỗi ô
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    
    # Chi phí ước lượng tổng cộng
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal)
    
    # Tập các ô đã xét
    closed_set = set()
    
    # Lưu quá trình tìm kiếm
    search_path = [start]
    
    while not open_set.empty():
        # Lấy ô có f_score thấp nhất
        current = open_set.get()[2]
        search_path.append(current)
        
        # Nếu đến đích, thoát vòng lặp
        if current == m._goal:
            break
        
        # Thêm vào danh sách đã xét
        closed_set.add(current)
        
        # Xét các ô kề
        for d in range(4):
            if m.maze_map[current][d] == True:
                child = (current[0] + dx[d], current[1] + dy[d])
                
                # Bỏ qua nếu đã xét
                if child in closed_set:
                    continue

                # Tính chi phí mới
                temp_g_score = g_score[current] + 1
                
                # Nếu tìm được đường đi tốt hơn
                if temp_g_score < g_score[child]:   
                    path_dict[child] = current
                    g_score[child] = temp_g_score
                    f_score[child] = temp_g_score + h(child, m._goal)
                    open_set.put((f_score[child], h(child, m._goal), child))

    # Tạo đường đi tối ưu từ goal về start
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
    # Tạo mê cung 20x20 với điểm đích ở (6,4)
    my_maze = maze(20, 20)
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