import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from color import COLOR
from maze import maze
from textLabel import textLabel

def DFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)
    
    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]
    
    # Danh sách các ô đã xét
    visited = [start]
    
    # Stack cho DFS (LIFO)
    stack = [start]
    
    # Dictionary lưu đường đi
    parent_path = {}
    
    # Lưu quá trình tìm kiếm
    search_path = []
    
    while stack:
        current = stack.pop()  # Lấy phần tử cuối cùng (LIFO)
        search_path.append(current)
        
        # Nếu đến đích, thoát vòng lặp
        if current == m._goal:
            break
            
        possible_moves = 0
        
        # Xét các ô kề
        for d in range(4):
            if m.maze_map[current][d] == True:
                neighbor = (current[0] + dx[d], current[1] + dy[d])
                
                # Bỏ qua nếu đã xét
                if neighbor in visited:
                    continue
                    
                possible_moves += 1
                visited.append(neighbor)
                stack.append(neighbor)
                parent_path[neighbor] = current
                
        # Đánh dấu các ô có nhiều hơn 1 đường đi
        if possible_moves > 1:
            m.markCells.append(current)
    
    # Tạo đường đi từ goal về start
    forward_path = {}
    cell = m._goal
    
    # Kiểm tra nếu không tìm thấy đường đi
    # if m._goal not in parent_path and start != m._goal:
    #     print("No path found from start to goal!")
    #     return search_path, parent_path, forward_path
    
    # Tái tạo đường đi từ goal về start
    while cell != start:
        forward_path[parent_path[cell]] = cell
        cell = parent_path[cell]
        
    return search_path, parent_path, forward_path


if __name__ == '__main__':
    # Tạo mê cung 10x10 với điểm đích ở (2,4)
    my_maze = maze(10, 10)
    my_maze.CreateMaze(2, 4, loopPercent=1.0)

    # Tìm đường với DFS
    search_path, parent_path, forward_path = DFS(my_maze, (5, 1))

    # Hiển thị quá trình tìm kiếm (màu vàng)
    agent_search = agent(my_maze, 5, 1, goal=(2, 4), footprints=True, color=COLOR.yellow, shape='square', filled=True)
    
    # Hiển thị quan hệ cha-con
    agent_parent = agent(my_maze, 2, 4, goal=(5, 1), footprints=True, filled=True)
    
    # Hiển thị đường đi (màu vàng)
    agent_path = agent(my_maze, 5, 1, footprints=True, color=COLOR.yellow)
    
    # Hiển thị các đường đi
    my_maze.tracePath({agent_search: search_path}, showMarked=True, delay=100)
    my_maze.tracePath({agent_parent: parent_path})
    my_maze.tracePath({agent_path: forward_path})

    # Hiển thị thông tin độ dài đường đi
    textLabel(my_maze, 'DFS Path Length', len(forward_path) + 1)
    textLabel(my_maze, 'DFS Search Length', len(search_path))

    # Chạy mô phỏng
    my_maze.run()