import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import agent
from maze import maze
from color import COLOR
from textLabel import textLabel
from queue import PriorityQueue

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2
    return abs(x1-x2) + abs(y1-y2)

def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    searchedPath = []
    while not open.empty():
        currCell=open.get()[2]
        if currCell not in searchedPath:
            searchedPath.append(currCell)
        for d in range(4):
            if m.maze_map[currCell][d]==True:
                dx = [0, -1, 1, 0]
                dy = [-1, 0 ,0, 1]
                child=(currCell[0] + dx[d], currCell[1] + dy[d])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(child,(1,1))

                if temp_f_score < f_score[child]:
                    g_score[child]= temp_g_score
                    f_score[child]= temp_f_score
                    open.put((temp_f_score,h(child,(1,1)),child))
                    aPath[child]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath

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
    
    myMaze=maze(10,15)
    myMaze.CreateMaze(6,4,loopPercent=100)

    searchPath,aPath,fwdPath=aStar(myMaze,(1,12))


    a=agent(myMaze,1,12,footprints=True,color=COLOR.SEARCH,filled=True)
    b=agent(myMaze,6,4,footprints=True,color=COLOR.PARENT,filled=True,goal=(1,12))
    c=agent(myMaze,1,12,footprints=True,color=COLOR.PATH,goal=(6,4))
    myMaze.tracePath({a:searchPath},delay=100)
    myMaze.tracePath({b:aPath},delay=100)

    myMaze.tracePath({c:fwdPath},delay=100)

    l=textLabel(myMaze,'A Star Path Length',len(fwdPath)+1)
    l=textLabel(myMaze,'A Star Search Length',len(searchPath))

    myMaze.run()