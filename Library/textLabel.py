from tkinter import Label, StringVar, RIDGE

class textLabel:
    def __init__(self, parent_maze, title, value, bg="white", fg="black", font=('Helvetica bold', 12), relief=RIDGE):
        self.title = title
        self._value = value
        self._parent_maze = parent_maze
        self._var = None
        self._bg = bg
        self._fg = fg
        self._font = font
        self._relief = relief
        self._create_label()
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._var.set(f'{self.title} : {new_value}')
    
    def _create_label(self):
        self._var = StringVar()
        self.label = Label(
            self._parent_maze._canvas, 
            textvariable=self._var,
            bg=self._bg,
            fg=self._fg,
            font=self._font,
            relief=self._relief
        )
        self._var.set(f'{self.title} : {self.value}')
        self.label.pack(expand=True, side="left", anchor="nw")