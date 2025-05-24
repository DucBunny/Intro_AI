import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from textLabel import textLabel

def dijkstra(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    # Các hướng di chuyển
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]

    # Khởi tạo các tập hợp
    unvisited = {cell: float('inf') for cell in m.grid}
    unvisited[start] = 0
    visited = {}
    parent_path = {}
    cells_searched = 0
    
    while unvisited:
        # Lấy ô có khoảng cách ngắn nhất
        current = min(unvisited, key = unvisited.get)
        
        # Thêm vào tập đã xét
        visited[current] = unvisited[current]
        
        # Nếu đến đích, thoát vòng lặp
        if current == m._goal:
            break
            
        cells_searched += 1
        
        # Xét các ô kề
        for d in range(4):
            if m.maze_map[current][d] == True:
                neighbor = (current[0] + dx[d], current[1] + dy[d])
                
                # Bỏ qua nếu đã xét
                if neighbor in visited:
                    continue
                    
                # Tính khoảng cách mới
                new_distance = unvisited[current] + 1
                
                # Nếu tìm được đường đi ngắn hơn
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    parent_path[neighbor] = current
                    
        # Xóa ô hiện tại khỏi tập chưa xét
        unvisited.pop(current)
    
    # Tạo đường đi tối ưu từ goal về start
    forward_path = {}
    cell = m._goal
    
    # Kiểm tra nếu không tìm thấy đường đi
    # if m._goal not in parent_path and start != m._goal:
    #     print("No path found from start to goal!")
    #     return {}, 0, cells_searched
    
    # Tái tạo đường đi từ goal về start
    while cell != start:
        forward_path[parent_path[cell]] = cell
        cell = parent_path[cell]
        
    # Trả về đường đi, chi phí và số ô đã duyệt
    return forward_path, visited[m._goal], cells_searched


if __name__ == '__main__':
    # Tạo mê cung 10x10 với điểm đích ở (1,4)
    my_maze = maze(10, 10)
    my_maze.CreateMaze(1, 4)

    forward_path, cost, cells_searched = dijkstra(my_maze, (6, 1))

    # Hiển thị quá trình tìm kiếm 
    agent_path = agent(my_maze, 6, 1, goal=(1, 4), filled=True, footprints=True, color=COLOR.SEARCH)

    # Hiển thị quan hệ cha-con
    # agent_parent = agent(my_maze, 1, 4, goal=(6, 1), filled=True, footprints=True, color=COLOR.PARENT)

    # Hiển thị các đường đi
    my_maze.tracePath({agent_path: forward_path}, delay=100)
    # my_maze.tracePath({agent_parent: parent_path}, delay=100)

    # Hiển thị thông tin về đường đi
    textLabel(my_maze, 'Cost', cost)
    textLabel(my_maze, 'Dijkstra Forward Path', len(forward_path) + 1)
    textLabel(my_maze, 'Dijkstra Cell Search', cells_searched)

    my_maze.run()