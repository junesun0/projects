# -*- coding: utf-8 -*-
# tetrominoes.py

# Name : June Sun
# Collaborators : Elisabeth, Cara, Taylor, Kaija, Hannah D

# Tetris yo

from graphics import *
from time import *
import random

class Game():
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.win = GraphWin ("T E T R I S", self.cols * 30, self.rows * 30)
        self.win.setBackground("alice blue")
        self.already_dropped = []
    def welcome_screen(self):
        self.welcome = Text(Point((self.cols * 30)/2, (self.rows * 30)/3), "WELCOME")
        self.welcome.setTextColor("gray17")
        self.welcome.setStyle("bold italic")
        self.welcome.setFace("helvetica")
        self.welcome.draw(game.win)
    def click_play_screen(self):
        self.click_to_play = Text(Point((self.cols * 30)/2, (self.rows * 30)/3 + 40), "*click to play*\npress i for instructions")
        self.click_to_play.setTextColor("gray17")
        self.click_to_play.setStyle("bold italic")
        self.click_to_play.setFace("helvetica")
        self.click_to_play.setSize(8)
        self.click_to_play.draw(game.win)
    def instructions_screen(self):
        self.move_arr = Text(Point((self.cols * 30)/2-30, (self.rows * 30)*2/3), "← ↓ →\nMOVE")
        self.move_arr.setTextColor("gray17")
        self.move_arr.setStyle("bold italic")
        self.move_arr.setFace("helvetica")
        self.move_arr.setSize(8)
        self.rotate_arr = Text(Point((self.cols * 30)/2+30, (self.rows * 30)*2/3), "↑\nROTATE")
        self.rotate_arr.setTextColor("gray17")
        self.rotate_arr.setStyle("bold italic")
        self.rotate_arr.setFace("helvetica")
        self.rotate_arr.setSize(8)
        self.move_arr.draw(game.win)
        self.rotate_arr.draw(game.win)
    def add_drop_shape(self, shape_letter):
        shape_dict = {"I": I_shape, "J": J_shape, "L": L_shape, "O": O_shape, "S": S_shape, "T": T_shape, "Z": Z_shape}
        self.current_shape = shape_dict[shape_letter](Point(self.cols/2, 0))
        self.current_shape.draw(self.win)
        if not self.current_shape.can_move(0, 1, self.cols, self.rows, self.get_block_location()):
            return False
        self.time = time()
        while self.current_shape.can_move(0, 1, self.cols, self.rows, self.get_block_location()):
            if time() - self.time >= 0.3:
                self.current_shape.move(0, 1)
                self.handle_keypress()
                self.time = time()
            self.win.update()
        self.already_dropped.append(self.current_shape)
        self.del_full_row(self.cols, self.rows, self.get_block_location())
        return True
    def get_block_location(self): 
        locations = []
        for s in self.already_dropped:
            for b in s.blocks:
                locations.append((b.x, b.y))
        return locations
    def is_row_full(self, cols, rows, locations):
        full = range(rows)
        for r in range(rows):
            for c in range(cols):
                if (c, r) not in locations:
                    full.remove(r)
                    break
        return full
    def del_full_row(self, cols, rows, locations):
        full = self.is_row_full(cols, rows, locations)
        to_be_deleted = []
        for f in full:
            for l in locations[:]:
                if l[1] == f:
                    to_be_deleted.append(l)
                    locations.remove(l)
        for l in to_be_deleted:
            for s in self.already_dropped[:]:
                for b in s.blocks:
                    if (b.x, b.y) == l:
                        b.undraw()
                        s.blocks.remove(b)
        self.shift_rows_down(full)
    def shift_rows_down(self, full):
        for r in sorted(full):
            for s in self.already_dropped[:]:
                for b in s.blocks:
                    if b.y < r:
                        b.move(0, 1)
    def handle_keypress(self):
        self.key = self.win.checkKey()
        if self.key == "Left":
            if self.current_shape.can_move(-1, 0, self.cols, self.rows, self.get_block_location()):
                self.current_shape.move(-1, 0)
        if self.key == "Right":
            if self.current_shape.can_move(1, 0, self.cols, self.rows, self.get_block_location()):
                self.current_shape.move(1, 0)
        if self.key == "Down":
            if self.current_shape.can_move(0, 2, self.cols, self.rows, self.get_block_location()):
                self.current_shape.move(0, 2)
        if self.key == "Up" and not isinstance(self.current_shape, O_shape):
            self.current_shape.rotate(self.cols, self.rows, self.get_block_location())
            

class Block(Rectangle):
    def __init__(self, location, color):
        self.location = location
        self.x = location.getX()
        self.y = location.getY()
        self.first_point = Point(self.location.getX()*30, self.location.getY()*30)
        self.second_point = Point((self.location.getX()+1)*30, (self.location.getY()+1)*30)
        Rectangle.__init__(self, self.first_point, self.second_point)
        self.setFill(color)
    def move(self, dx, dy):
        self.location = Point(self.location.getX() + dx, self.location.getY() + dy)
        Rectangle.move(self, 30 * dx, 30 * dy)
        self.x = self.x + dx
        self.y = self.y + dy
    def can_move(self, dx, dy, cols, rows, locations):
        if -1 < self.x + dx < cols and 0 < self.y + dy < rows and (self.x + dx, self.y + dy) not in locations:
            return True
        else:
            return False

class Shape(object): 
    def __init__(self, blocks, color): 
        self.color = color
        self.blocks = []
        for n in blocks:
            n_block = Block(n, self.color)
            self.blocks.append(n_block)
    def move(self, dx, dy):
        for n in self.blocks:
            n.move(dx, dy)
    def draw(self, win):
        for n in self.blocks:
            n.draw(win)
    def can_move(self, dx, dy, cols, rows, locations):
        for n in self.blocks:
            if not n.can_move(dx, dy, cols, rows, locations):
                return False
        return True
    def rotate(self, cols, rows, locations):
        x_c = self.center_block.location.getX()
        y_c = self.center_block.location.getY()
        list_positions = []
        for n in self.blocks:
            x_i = n.location.getX()
            y_i = n.location.getY()
            diff_x = x_i - x_c
            diff_y = y_i - y_c
            new_x = x_c
            new_y = y_c
            if diff_x < 0:
                new_y = y_c + abs(diff_x)
            elif diff_x > 0:
                new_y = y_c - abs(diff_x)
            if diff_y < 0:
                new_x = x_c - abs(diff_y)
            elif diff_y > 0:
                new_x = x_c + abs(diff_y)
            move_x = new_x - x_i
            move_y = new_y - y_i
            if not n.can_move(move_x, move_y, cols, rows, locations):
                return None
            list_positions.append((move_x, move_y))
        for i in range(len(list_positions)):
            dx = list_positions[i][0]
            dy = list_positions[i][1]
            self.blocks[i].move(dx, dy) 

class I_shape(Shape):
   def  __init__(self,  center):
       coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x  +  2,  center.y)]
       Shape.__init__(self,  coords,  "white")
       self.center_block = self.blocks[1]

class J_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x  +  1,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]
        
class L_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x  -  1,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]
        
class O_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  -  1,  center.y + 1),
                 Point(center.x,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]
        
class S_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  +  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  -  1,  center.y + 1),
                 Point(center.x,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]
        
class T_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]
        
class Z_shape(Shape):
    def  __init__(self,  center):
        coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x,  center.y + 1),
                 Point(center.x  +  1,  center.y + 1)]
        Shape.__init__(self,  coords,  "white")
        self.center_block = self.blocks[1]

def get_random_letter():
    shape_letter_list = ["I", "J", "L", "O", "S", "T", "Z"]
    rand_shape = random.choice(shape_letter_list)
    return rand_shape

def loopy_loop():
    game_not_over = True
    while game_not_over: # repeat indefinitely
        rand_shape = get_random_letter()
        game_not_over = game.add_drop_shape(rand_shape)
    loser = Text(Point(70, 25), "GAME OVER")
    loser.setTextColor("IndianRed1")
    loser.setStyle("bold italic")
    loser.setFace("helvetica")
    loser.draw(game.win)

game = Game(12, 20)
game.welcome_screen()
game.click_play_screen()
start_game = False
i_clicked = False
while not start_game:
    if game.win.checkKey() == "i":
        game.instructions_screen()
        i_clicked = True
    if game.win.checkMouse():
        game.welcome.undraw()
        game.click_to_play.undraw()
        if i_clicked == True:
            game.move_arr.undraw()
            game.rotate_arr.undraw()
        start_game = True
loopy_loop()

game.win.mainloop()
