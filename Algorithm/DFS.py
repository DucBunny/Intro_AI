import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import *
from maze import maze
from textLabel import textLabel
# from collections import deque


# E:3 W:0 N:1 S:2

def DFS(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    visited=[start]
    queue=[start]
    dfsPath={}
    dSearch=[]
    while len(queue)>0:
        currCell=queue.pop()
        dSearch.append(currCell)
        if currCell==m._goal:
            break
        poss=0
        for d in range(4):
            if m.maze_map[currCell][d]==True:
                dx = m.delta()[0]
                dy = m.delta()[1]
                child=(currCell[0] + dx[d], currCell[1] + dy[d])
                if child in visited:
                    continue
                poss+=1
                visited.append(child)
                queue.append(child)
                dfsPath[child]=currCell
        if poss>1:
            m.markCells.append(currCell)
    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
    return dSearch,dfsPath,fwdPath


if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(2,4, loopPercent=1.0)

    dSearch,dfsPath,fwdPath=DFS(m,(5,1)) # (5,1) is Start Cell, Change that to any other valid cell

    # a=agent(m,5,1,goal=(2,4),footprints=True,shape='square',color=COLOR.green)
    a=agent(m,5,1,goal=(2,4),footprints=True,color=COLOR.yellow,shape='square',filled=True)
    b=agent(m,2,4,goal=(5,1),footprints=True,filled=True)
    c=agent(m,5,1,footprints=True,color=COLOR.yellow)
    print(dSearch)
    m.tracePath({a:dSearch},showMarked=True, delay = 100)
    m.tracePath({b:dfsPath})
    m.tracePath({c:fwdPath})
    l3 = textLabel(m, 'DFS Search Length', len(fwdPath) + 1)
    m.run()

    # m=maze()
    # m.CreateMaze(loadMaze='dfs.csv')

    # dSearch,dfsPath,fwdPath=DFS(m)

    # a=agent(m,footprints=True,shape='square',color=COLOR.green)
    # b=agent(m,1,1,goal=(5,5),footprints=True,filled=True,color=COLOR.cyan)
    # c=agent(m,footprints=True,color=COLOR.yellow)
    # m.tracePath({a:dSearch},showMarked=True)
    # m.tracePath({b:dfsPath})
    # m.tracePath({c:fwdPath})
    # m.run()