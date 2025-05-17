import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import *
from maze import maze
# from Library import *
from collections import deque

def BFS(m, start=None):
    if start is None:
        start=(m.rows,m.cols)
    frontier = deque()
    frontier.append(start)
    bfsPath = {}
    explored = [start]
    bSearch=[]
    while len(frontier)>0:
        currCell=frontier.popleft()
        if currCell==m._goal:
            break
        for d in range(4):
            if m.maze_map[currCell][d]==True:
                dx = [0, -1, 1, 0]
                dy = [-1, 0 ,0, 1]
                child=(currCell[0] + dx[d], currCell[1] + dy[d])
                if child in explored:
                    continue
                frontier.append(child)
                explored.append(child)
                bfsPath[child] = currCell
                bSearch.append(child)
    fwdPath={}
    cell=m._goal
    # print("BFS Path: ", m._goal)
    while cell!= start:
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
        # print(cell)
    return bSearch,bfsPath,fwdPath

if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(2, 4, loopPercent=1.0)

    bSearch,bfsPath,fwdPath = BFS(m, (5,1))
    a=agent(m,5,1,goal=(2,4),footprints=True,color=COLOR.yellow,shape='square',filled=True)
    b=agent(m,2,4,goal=(5,1),footprints=True,filled=True)
    c=agent(m,5,1,footprints=True,color=COLOR.yellow)

    m.tracePath({a:bSearch},delay=100)
    m.tracePath({b:bfsPath},delay=100)
    m.tracePath({c:fwdPath},delay=100)

    m.run()