import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
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

def find_all_paths_DFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)
    
    dx = [0, -1, 1, 0]
    dy = [-1, 0, 0, 1]
    
    all_paths = []
    visited = set()
    
    def dfs(current, path):
        if current == m._goal:
            all_paths.append(path[:])
            return
            
        for d in range(4):
            if m.maze_map[current][d]:
                neighbor = (current[0] + dx[d], current[1] + dy[d])
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path)
                    path.pop()
                    visited.remove(neighbor)
    
    visited.add(start)
    dfs(start, [start])
    
    return all_paths

if __name__ == '__main__':
    my_maze = maze(10, 10)
    my_maze.CreateMaze(2, 4, loopPercent=1.0)
    
    all_paths = find_all_paths_DFS(my_maze, (5, 1))
    
    # Chọn hai đường đi nếu có
    if len(all_paths) >= 2:
        path1 = all_paths[0]
        path2 = all_paths[1]
        
        # Hiển thị hai đường đi
        agent_path1 = agent(my_maze, 5, 1, goal=(2, 4), filled=True, footprints=True, color=COLOR.SEARCH)
        agent_path2 = agent(my_maze, 5, 1, goal=(2, 4), filled=True, footprints=True, color=COLOR.PATH)
        
        my_maze.tracePath({agent_path1: path1}, delay=100)
        my_maze.tracePath({agent_path2: path2}, delay=100)
        
        textLabel(my_maze, 'More than one path found', 'Yes')
        textLabel(my_maze, 'Path 1 Length', len(path1))
        textLabel(my_maze, 'Path 2 Length', len(path2))
    else:
        search_path, parent_path, forward_path = DFS(my_maze, (5, 1))

        # Hiển thị quá trình tìm kiếm 
        agent_search = agent(my_maze, 5, 1, goal=(2, 4), filled=True, footprints=True, color=COLOR.SEARCH)
        
        # Hiển thị quan hệ cha-con
        agent_parent = agent(my_maze, 2, 4, goal=(5, 1), filled=True, footprints=True, color=COLOR.PARENT)
        
        # Hiển thị đường đi 
        agent_path = agent(my_maze, 5, 1, goal=(2, 4), footprints=True, color=COLOR.PATH)
        
        # Hiển thị các đường đi
        my_maze.tracePath({agent_search: search_path}, showMarked=True, delay=100)
        my_maze.tracePath({agent_parent: parent_path}, delay=100)
        my_maze.tracePath({agent_path: forward_path}, delay=100)

        # Hiển thị thông tin độ dài đường đi
        textLabel(my_maze, 'More than one path found', 'No')
        textLabel(my_maze, 'DFS Forward Path', len(forward_path) + 1)
        textLabel(my_maze, 'DFS Search Path', len(search_path))
    
    my_maze.run()