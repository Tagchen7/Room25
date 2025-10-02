# Contains definitions for game entities like Player, Enemy, Projectile, etc.

from xmlrpc.client import Boolean


class Room:
    def __init__(self, corner=False, color="grey", number=0):
        # Center = (0, 0)
        self.corner = corner
        self.color = color
        self.number = number

    def __repr__(self) -> str:
        if self.number > 0:
            return f"{self.color}:{self.number}"
        return self.color
    
class Grid:
    size = 5
    def __init__(self):
        # self.rooms have a tuple denoting position as key (x, y) = (0, 1) and a room at the position
        # room positions are in range(size)
        # center room is always B1
        self.rooms = {}
        for x in range(5):
            cx = x - self.size//2
            for y in range(5):
                cy = y - self.size//2
                corner = (abs(cx) == abs(cy) and abs(cx) != 1) or (cx!=0 and cy!=0)
                self.rooms[(x, y)] = Room(corner=corner)
                if cx == 0 and cy == 0:
                    self.rooms[(x, y)].color = "blue"
                    self.rooms[(x, y)].number = 1

    def shift_rooms(self, row:bool, num:int, forward:bool):
        old_rooms = self.rooms.copy()
        for i in range(self.size):
            if forward:
                i_new = (i + 1) % self.size
            else:
                i_new = (i - 1 + self.size) % self.size
            if row:
                x_new, y_new = i_new, num
                x_old, y_old = i, num
            else:
                x_new, y_new = num, i_new
                x_old, y_old = num, i
            self.rooms[(x_new, y_new)] = old_rooms[(x_old, y_old)]
    
    def swap_rooms(self, pos_1:tuple, pos_2:tuple):
        temp = self.rooms[pos_1]
        self.rooms[pos_1] = self.rooms[pos_2]
        self.rooms[pos_2] = temp