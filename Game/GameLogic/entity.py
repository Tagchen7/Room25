# Contains definitions for game entities like Player, Enemy, Projectile, etc.
from typing import Any
import pygame
from pygame.locals import *

class Player:
    total_amount = 0

    def __init__(self, color):
        self.color = color
        self.total_amount += 1
        self.index = self.total_amount
        self.name = self.reset_name()

    def reset_name(self):
        return f"{self.color.capitalize()}_{self.index}"
    
    def set_name(self, new_name):
        self.name = new_name

class Info:
    def __init__(self, player, color):
        self.player = player
        self.color = color

class Room(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, corner=False, color="grey", number=0):
        super().__init__()
        # Center = (0, 0)
        self.corner = corner
        self.color = color
        self.number = number
        self.update_image()
        self.rect = self.image.get_rect()
        # whenever someone looks at the room, add the info based on what they see
        self.info = []

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        self.update_image()

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, number):
        self._number = number
        self.update_image()

    def update_image(self):
        if self.name() == "Unknown":
            self.image = pygame.image.load("Game/Assets/Unknown.png")
        else:
            self.image = pygame.image.load(f"Game/Assets/{self.color.capitalise()}_{self.number}.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)

    def add_info(self, person, color):
        self.info.append(Info(person, color))

    def __repr__(self) -> str:
        if self.number > 0:
            return f"{self.color}:{self.number}"
        return self.color
    
    def name(self):
        # name is organised by a (color, number) tuple
        names = {("blue", 1): "Central",
                 ("blue", 2): "Exit",
                 ("blue", 3): "Key",
                 ("green", 1): "Empty",
                 ("green", 2): "Vision",
                 ("green", 3): "Swapping",
                 ("green", 4): "Shifting",
                 ("green", 5): "Portal",
                 ("green", 6): "Regeneration",
                 ("green", 7): "Robot",
                 ("red", 1): "Acid",
                 ("red", 2): "Death",
                 ("red", 3): "Trap",
                 ("red", 4): "Flooded",
                 ("red", 5): "Shredder",
                 ("red", 6): "Timer",
                 ("red", 7): "Paranoia",
                 ("red", 8): "Illusion",
                 ("yellow", 1): "Vortex",
                 ("yellow", 2): "Prison",
                 ("yellow", 3): "Cold",
                 ("yellow", 4): "Dark",
                 ("yellow", 5): "Pivot",
                 ("yellow", 6): "Jamming",
                 ("yellow", 7): "M.A.C.",
                 ("yellow", 8): "Mirror"
                 }
        return names.get((self.color, self.number), "Unknown")
    
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