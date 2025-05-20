from tkinter import *
from color import COLOR

class agent:
    def __init__(self, parent_maze, x=None, y=None, shape='square', goal=None, filled=False, footprints=False, color=COLOR.DEFAULT):
        self._parent_maze = parent_maze
        
        # Xử lý color
        self.color = self._validate_color(color)
        
        self.filled = filled
        self.shape = shape
        self._orient = 0
        
        # Xử lý tọa độ và mục tiêu
        self.x = x if x is not None else parent_maze.rows
        self.y = y if y is not None else parent_maze.cols
        self.footprints = footprints
        self._parent_maze._agents.append(self)
        self.goal = goal if goal is not None else self._parent_maze._goal
        
        self._body = []
        self.position = (self.x, self.y)
    
    # Hàm xác thực và chuyển đổi màu sắc
    def _validate_color(self, color):
        if isinstance(color, str):
            if color in COLOR.__members__:
                return COLOR[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        return color
    
    # Tính toán tọa độ cho agent dựa trên vị trí hiện tại
    def _calculate_coordinates(self):
        w = self._parent_maze._cell_width
        x = self.x * w - w + self._parent_maze._LabWidth
        y = self.y * w - w + self._parent_maze._LabWidth
        
        if self.shape == 'square':
            if self.filled:
                return (y, x, y + w, x + w)
            else:
                return (y + w/2.5, x + w/2.5, y + w/2.5 + w/4, x + w/2.5 + w/4)
        else:
            return (y + w/2, x + 3*w/9, y + w/2, x + 3*w/9 + w/4)
    
    # Hàm cập nhật biểu diễn trực quan của agent
    def _update_visual_representation(self):
        if hasattr(self, '_head'):
            if self.footprints is False:
                self._parent_maze._canvas.delete(self._head)
            else:
                self._handle_footprints()
            
            self._create_new_head()
        else:
            self._create_new_head()
    
    # Hàm xử lý dấu chân
    def _handle_footprints(self):
        if self.shape == 'square':
            self._parent_maze._canvas.itemconfig(self._head, fill=self.color.value[1], outline="")
            self._parent_maze._canvas.tag_raise(self._head)
            self._try_lower_tag()
            
            if self.filled:
                coords = self._parent_maze._canvas.coords(self._head)
                old_cell = (
                    round(((coords[1]-26)/self._parent_maze._cell_width)+1),
                    round(((coords[0]-26)/self._parent_maze._cell_width)+1)
                )
                self._parent_maze._redrawCell(*old_cell, self._parent_maze.theme)
        else:
            self._parent_maze._canvas.itemconfig(self._head, fill=self.color.value[1])
            self._parent_maze._canvas.tag_raise(self._head)
            self._try_lower_tag()
            
        self._body.append(self._head)
    
    # Hàm hạ thấp thẻ 'ov' xuống dưới
    def _try_lower_tag(self):
        try:
            self._parent_maze._canvas.tag_lower(self._head, 'ov')
        except:
            pass
    
    # Tạo biểu diễn mới cho đầu của agent
    def _create_new_head(self):
        self._head = self._parent_maze._canvas.create_rectangle(
            *self._coord, fill=self.color.value[0], outline=''
        )
        self._try_lower_tag()
        self._parent_maze._redrawCell(self.x, self.y, theme=self._parent_maze.theme)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, new_x):
        self._x = new_x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, new_y):
        self._y = new_y
        # Tính toán tọa độ mới và cập nhật trạng thái
        self._coord = self._calculate_coordinates()
        self._update_visual_representation()
    
    @property
    def position(self):
        return (self.x, self.y)
    
    @position.setter
    def position(self, new_pos):
        self.x = new_pos[0]
        self.y = new_pos[1]
        self._position = new_pos