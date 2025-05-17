import sys
import os
library_path = os.path.join(os.path.dirname(__file__), '..', 'Library')
sys.path.append(library_path)

from agent import *
from maze import maze
from textLabel import textLabel

def dijkstra(m,start=None):
    if start is None:
        start=(m.rows,m.cols)

    unvisited={n:float('inf') for n in m.grid}
    unvisited[start]=0
    visited={}
    revPath={}
    searched = 0
    while unvisited:
        currCell=min(unvisited,key=unvisited.get)
        visited[currCell]=unvisited[currCell]
        if currCell==m._goal:
            break
        searched += 1
        for d in range(4):
            if m.maze_map[currCell][d]==True:
                dx = m.delta()[0]
                dy = m.delta()[1]
                child = (currCell[0] + dx[d], currCell[1] + dy[d])
                if child in visited:
                    continue
                tempDist= unvisited[currCell]+1
                # for hurdle in hurdles:
                #     if hurdle[0]==currCell:
                #         tempDist+=hurdle[1]

                if tempDist < unvisited[child]:
                    unvisited[child]=tempDist
                    revPath[child]=currCell
        unvisited.pop(currCell)
    
    fwdPath={}
    cell=m._goal
    # print("Dijkstra Path: ", m._goal)
    while cell!=start:
        fwdPath[revPath[cell]]=cell
        cell=revPath[cell]
        # print(cell)
    return fwdPath,visited[m._goal], searched


if __name__=='__main__':
    myMaze=maze(10,10)
    myMaze.CreateMaze(1,4)

    path,c, step=dijkstra(myMaze,start=(6,1))
    textLabel(myMaze,'Total Cost',c)
    print(c, len(path), step)

    # a=agent(myMaze,color=COLOR.cyan,filled=True,footprints=True)
    a=agent(myMaze,6,1,color=COLOR.cyan,filled=True,footprints=True)
    myMaze.tracePath({a:path})

    myMaze.run()