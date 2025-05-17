import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from textLabel import textLabel
from queue import PriorityQueue

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))
    
def aStar(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    open = PriorityQueue()
    open.put((h(start, m._goal), h(start, m._goal), start))
    aPath = {}
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal)
    searchPath=[start]
    while not open.empty():
        currCell = open.get()[2]
        searchPath.append(currCell)
        if currCell == m._goal:
            break        
        for d in range(4):
            if m.maze_map[currCell][d]==True:
                dx = [0, -1, 1, 0]
                dy = [-1, 0 ,0, 1]
                child=(currCell[0] + dx[d], currCell[1] + dy[d])

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(child, m._goal)

                if temp_f_score < f_score[child]:   
                    aPath[child] = currCell
                    g_score[child] = temp_g_score
                    f_score[child] = temp_g_score + h(child, m._goal)
                    open.put((f_score[child], h(child, m._goal), child))

    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath

if __name__=='__main__':
    
    myMaze=maze(20,20)
    myMaze.CreateMaze(6,4,loopPercent=100)

    searchPath,aPath,fwdPath=aStar(myMaze,(1,12))

    a=agent(myMaze,1,12,footprints=True,color=COLOR.blue,filled=True)
    b=agent(myMaze,6,4,footprints=True,color=COLOR.yellow,filled=True,goal=(1,12))
    c=agent(myMaze,1,12,footprints=True,color=COLOR.red,goal=(6,4))
    myMaze.tracePath({a:searchPath},delay=200)
    myMaze.tracePath({b:aPath},delay=200)

    myMaze.tracePath({c:fwdPath},delay=200)

    l=textLabel(myMaze,'A Star Path Length',len(fwdPath)+1)
    l=textLabel(myMaze,'A Star Search Length',len(searchPath))

    myMaze.run()