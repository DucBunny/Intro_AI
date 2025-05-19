import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from collections import deque

def BFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)
    
    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]
    
    # Hàng đợi các ô cần xét
    frontier = deque()
    frontier.append(start)
    
    # Dictionary lưu đường đi
    parent_path = {}
    
    # Tập các ô đã xét hoặc đang trong hàng đợi
    explored = set([start])
    
    # Lưu quá trình tìm kiếm
    search_path = []
    
    while frontier:
        current = frontier.popleft()
        
        # Nếu đến đích, thoát vòng lặp
        if current == m._goal:
            break
            
        # Xét các ô kề
        for d in range(4):
            if m.maze_map[current][d] == True:
                # Sử dụng dx, dy đã khai báo ở đầu hàm
                neighbor = (current[0] + dx[d], current[1] + dy[d])
                
                # Bỏ qua nếu đã xét
                if neighbor in explored:
                    continue
                    
                frontier.append(neighbor)
                explored.add(neighbor)
                parent_path[neighbor] = current
                search_path.append(neighbor)
    
    # Tạo đường đi tối ưu từ goal về start
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
    m = maze(10, 10)
    m.CreateMaze(2, 4, loopPercent=1.0)

    # Tìm đường với BFS
    search_path, parent_path, forward_path = BFS(m, (5, 1))

    # Hiển thị quá trình tìm kiếm (màu vàng)
    agent_search = agent(m, 5, 1, goal=(2, 4), footprints=True, color=COLOR.yellow, shape='square', filled=True)
    
    # Hiển thị quan hệ cha-con
    agent_parent = agent(m, 2, 4, goal=(5, 1), footprints=True, filled=True)
    
    # Hiển thị đường đi tối ưu (màu vàng)
    agent_optimal = agent(m, 5, 1, footprints=True, color=COLOR.yellow)
    
    # Hiển thị các đường đi
    m.tracePath({agent_search: search_path}, delay=100)
    m.tracePath({agent_parent: parent_path}, delay=100)
    m.tracePath({agent_optimal: forward_path}, delay=100)

    # Chạy mô phỏng
    m.run()