from tkinter import *

class textLabel:
    def __init__(self,parentMaze,title,value):
        self.title=title
        self._value=value
        self._parentMaze=parentMaze
        # self._parentMaze._labels.append(self)
        self._var=None
        self.drawLabel()
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,v):
        self._value=v
        self._var.set(f'{self.title} : {v}')
    def drawLabel(self):
        self._var = StringVar()
        self.lab = Label(self._parentMaze._canvas, textvariable=self._var, bg="white", fg="black",font=('Helvetica bold',12),relief=RIDGE)
        self._var.set(f'{self.title} : {self.value}')
        self.lab.pack(expand = True,side=LEFT,anchor=NW)