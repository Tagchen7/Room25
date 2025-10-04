# Contains definitions for game entities like Player, Enemy, Projectile, etc.
from sre_parse import WHITESPACE
from turtle import circle
import pygame

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0) 
YELLOW = (255, 255, 0)
BLUE = (0, 255, 255)
GREY = (180, 180, 180)
WHITE = (235, 235, 235)

def get_color_name(color=GREY):
    if color == RED:
        return "Red"
    elif color == GREEN:
        return "Green"
    elif color == YELLOW:
        return "Yellow"
    elif color == BLUE:
        return "Blue"
    elif color == WHITE:
        return "White"
    elif color == GREY:
        return "Grey"
    else:
        return "Unknown"

class Player:
    total_amount = 0

    def __init__(self, color):
        self.color = color
        Player.total_amount += 1
        self.index = self.total_amount
        self.name = self.reset_name()

    def reset_name(self):
        return f"{self.color.capitalize()}_{self.index}"
    
    def set_name(self, new_name):
        self.name = new_name

class Base_Room(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, corner=False, color=GREY, number=0):
        super().__init__()
        # Center = (0, 0)
        self.corner = corner
        self.color = color
        self.number = number
        self.update_image()
        self.rect = self.image.get_rect()

    def update_image(self):
        if self.name() == "Unknown":
            self.image = pygame.image.load("Game/Assets/Unknown.png")
        else:
            self.image = pygame.image.load(f"Game/Assets/{get_color_name(self.color)}_{self.number}.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)

    def __repr__(self) -> str:
        if self.number > 0:
            return f"{self.color}:{self.number}"
        return self.color
    
    def name(self):
        # name is organised by a (color, number) tuple
        names = {(BLUE, 1): "Central",
                 (BLUE, 2): "Exit",
                 (BLUE, 3): "Key",
                 (GREEN, 1): "Empty",
                 (GREEN, 2): "Vision",
                 (GREEN, 3): "Swapping",
                 (GREEN, 4): "Shifting",
                 (GREEN, 5): "Portal",
                 (GREEN, 6): "Regeneration",
                 (GREEN, 7): "Robot",
                 (RED, 1): "Acid",
                 (RED, 2): "Death",
                 (RED, 3): "Trap",
                 (RED, 4): "Flooded",
                 (RED, 5): "Shredder",
                 (RED, 6): "Timer",
                 (RED, 7): "Paranoia",
                 (RED, 8): "Illusion",
                 (YELLOW, 1): "Vortex",
                 (YELLOW, 2): "Prison",
                 (YELLOW, 3): "Cold",
                 (YELLOW, 4): "Dark",
                 (YELLOW, 5): "Pivot",
                 (YELLOW, 6): "Jamming",
                 (YELLOW, 7): "M.A.C.",
                 (YELLOW, 8): "Mirror"
                 }
        return names.get((self.color, self.number), "Unknown")
    	
    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)

class Info(pygame.sprite.Sprite):
    sprite_size = (50, 20)
    def __init__(self, color, player=None):
        super().__init__()
        self.player = player
        self.color = color
        self.image = pygame.image.load(f"Game/Assets/Color.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)
        self.update_image()
        self.rect = self.image.get_rect()

    def __repr__(self):
        return f"{self.player}:{self.color}"
    
    def update_image(self):
        self.image.fill(self.color)

    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)
        if self.player is not None:
            text = pygame.font.SysFont('arial', 15).render(f"{self.player.index}", True, (0,0,0))
            surface.blit(text, (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.rect.height/2 - text.get_height()/2))

class Room(Base_Room):
    sprite_size = (50, 50)
    def __init__(self, corner=False, color=GREY, number=0):
        super().__init__(corner=corner, color=color, number=number)
        # whenever someone looks at the room, add the info based on what they see
        self.info = []
        self.is_selected = False

    def add_info(self, color, player):
        self.info.append(Info(color=color, player=player))
    	
    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)
        if self.number == 0:
            for i, info in enumerate(self.info):
                info.rect.width = self.sprite_size[1] / len(self.info)
                info.rect.bottomleft = (self.rect.bottomleft[0] + i * info.rect.width, self.rect.bottomleft[1])
                info.draw(surface)
        if self.corner and self.name() == "Unknown":
            pygame.draw.circle(surface, "blue", self.rect.center, 7.5)
        if self.is_selected:
            pygame.draw.circle(surface, "green", self.rect.center, 5.5)
            

class Shift_Arrow(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, direction, number):
        super().__init__()
        self.direction = direction
        self.number = number
        self.image = pygame.image.load(f"Game/Assets/Shift_Arrow.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)
        self.image = pygame.transform.rotate(self.image, 90 * direction)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)  
    
    def __eq__(self, other):
        return self.direction == other.direction and self.number == other.number
    
class Grid:
    size = 5
    room_size = (50, 50)
    def __init__(self):
        # self.rooms have a tuple denoting position as key (x, y) = (0, 1) and a room at the position
        # room positions are in range(size)
        # center room is always B1
        Room.sprite_size = self.room_size
        self.rooms = {}
        for x in range(5):
            cx = x - self.size//2
            for y in range(5):
                cy = y - self.size//2
                corner = (cx!=0 and cy!=0) and (abs(cx) != 1 or abs(cy) != 1)
                self.rooms[(x, y)] = Room(corner=corner)
                if cx == 0 and cy == 0:
                    self.rooms[(x, y)].color = BLUE
                    self.rooms[(x, y)].number = 1
        self.arrows = []
        for i in range(self.size):
            ci = i - self.size//2
            if ci != 0:
                self.arrows.append(Shift_Arrow(0, i))  # right
                self.arrows.append(Shift_Arrow(1, i))  # down
                self.arrows.append(Shift_Arrow(2, i))  # left
                self.arrows.append(Shift_Arrow(3, i))  # up

    def shift_rooms(self, direction:int, num:int):
        # direction, number == Shift_Arrow.direction, Shift_Arrow.number
        # direction: 0 = left, 1 = down, 2 = right, 3 = up
        # all valid shifts have a shift arrow
        if Shift_Arrow(direction, num) not in self.arrows:
            return
        old_rooms = self.rooms.copy()
        for i in range(self.size):
            if direction in [0, 3]:
                i_new = (i + 1) % self.size
            else:
                i_new = (i - 1 + self.size) % self.size
            if direction % 2 == 0:
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

    def draw(self, surface):
        for pos, room in self.rooms.items():
            room.rect.center = ((pos[0]+1.5)*self.room_size[0], (pos[1]+1.5)*self.room_size[1])
            room.draw(surface)
        for arrow in self.arrows:
            if arrow.direction == 0:  # left
                arrow.rect.center = (0.5*self.room_size[0], (arrow.number+1.5)*self.room_size[1])
            elif arrow.direction == 1:  # down
                arrow.rect.center = ((arrow.number+1.5)*self.room_size[0], (self.size+1.5)*self.room_size[1])
            elif arrow.direction == 2:  # right
                arrow.rect.center = ((self.size+1.5)*self.room_size[0], (arrow.number+1.5)*self.room_size[1])
            elif arrow.direction == 3:  # up
                arrow.rect.center = ((arrow.number+1.5)*self.room_size[0], 0.5*self.room_size[1])
            arrow.draw(surface)

class Room_Notes():
    sprite_size = (50, 50)
    starting_center = (50, 400)

    def __init__(self):
        self.blue_rooms = [Base_Room(color=BLUE, number=i) for i in range(1, 4)]
        self.green_rooms = [Base_Room(color=GREEN, number=i) for i in range(1, 8)]
        self.yellow_rooms = [Base_Room(color=YELLOW, number=i) for i in range(1, 9)]
        self.red_rooms = [Base_Room(color=RED, number=i) for i in range(1, 9)]
        self.undo_room = Base_Room(color=GREY, number=0)
        for room in self.all_rooms():
            room.rect = room.image.get_rect()

    def all_rooms(self):
        return self.blue_rooms + self.green_rooms + self.yellow_rooms + self.red_rooms + [self.undo_room]

    def draw(self, surface):
        for room in self.blue_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1])
        self.undo_room.rect.center = (self.starting_center[0] + self.sprite_size[0] * 6, self.starting_center[1])
        for room in self.green_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + self.sprite_size[1])
        for room in self.yellow_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + 2 * self.sprite_size[1])
        for room in self.red_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + 3 * self.sprite_size[1])
        for room in self.all_rooms():
            room.draw(surface)

class Color_Notes():
    sprite_size = (50, 50)
    starting_center = (400, 50)
    note_colors = [BLUE, GREEN, YELLOW, RED, GREY, WHITE]

    def __init__(self):
        self.notes = [Info(color=color) for color in self.note_colors]
        self.special_note = Info(color=GREY, player=None)
        for note in self.all_notes():
            note.image = pygame.transform.scale(note.image, self.sprite_size)
            note.rect = note.image.get_rect()

    def all_notes(self):
        return self.notes + [self.special_note]

    def draw(self, surface):
        for i, room in enumerate(self.notes):
            room.rect.center = (self.starting_center[0], self.starting_center[1] + self.sprite_size[1] * i)
            room.draw(surface)

