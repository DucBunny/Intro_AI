import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from textLabel import textLabel
from collections import deque

def BFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)
    
    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]

    # Khởi tạo hàng đợi frontier
    frontier = deque([start])
    
    # Dictionary lưu đường đi
    parent_path = {}

    # Tập các ô đã xét hoặc đang trong hàng đợi
    explored = [start]

    # Lưu quá trình tìm kiếm
    search_path = []
    
    while frontier:
        current = frontier.popleft()
        
        # Nếu đến đích, thoát vòng lặp
        if current == m._goal:
            break
            
        # Xét các ô kề
        for d in range(4):
            if m.maze_map[current][d]:
                child = (current[0] + dx[d], current[1] + dy[d])
                
                # Bỏ qua nếu đã xét
                if child in explored:
                    continue
                    
                frontier.append(child)
                explored.append(child)
                parent_path[child] = current
                search_path.append(child)
    
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
    my_maze = maze(30, 30)
    my_maze.CreateMaze(2, 4, loopPercent=1.0)

    search_path, parent_path, forward_path = BFS(my_maze, (5, 1))
    
    # Hiển thị quá trình tìm kiếm 
    agent_search = agent(my_maze, 5, 1, goal=(2, 4), filled=True, footprints=True, color=COLOR.SEARCH)
    
    # Hiển thị quan hệ cha-con
    agent_parent = agent(my_maze, 2, 4, goal=(5, 1), filled=True, footprints=True, color=COLOR.PARENT)
    
    # Hiển thị đường đi tối ưu
    agent_optimal = agent(my_maze, 5, 1, goal=(2, 4), footprints=True, color=COLOR.PATH)
    
    # Hiển thị các đường đi
    my_maze.tracePath({agent_search: search_path}, delay=100)
    my_maze.tracePath({agent_parent: parent_path}, delay=100)
    my_maze.tracePath({agent_optimal: forward_path}, delay=100)

    # Hiển thị thông tin độ dài đường đi
    textLabel(my_maze, 'BFS Forward Path', len(forward_path) + 1)
    textLabel(my_maze, 'BFS Search Path', len(search_path))

    my_maze.run()