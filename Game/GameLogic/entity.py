# Contains definitions for game entities like Player, Enemy, Projectile, etc.
from sre_parse import WHITESPACE
from turtle import circle
import pygame

# Define some colors for rooms
ROOMCOLOR = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "yellow" : (255, 255, 0),
    "blue" : (0, 255, 255),
    "grey" : (180, 180, 180),
    "white" : (235, 235, 235)
}

# Define some colors for players
PLAYERCOLOR = {
    "brown" : (150, 75, 0),
    "pink" : (250, 0, 250),
    "yellow" : (250, 250, 0),
    "orange" : (250, 125, 0),
    "grey" : (150, 150, 150),
    "blue" : (0, 0, 250),
    "green" : (0, 250, 0),
    "red" : (250, 0, 0)
}

def get_color_name(color=ROOMCOLOR["grey"]):
    if color == ROOMCOLOR["red"]:
        return "Red"
    elif color == ROOMCOLOR["green"]:
        return "Green"
    elif color == ROOMCOLOR["yellow"]:
        return "Yellow"
    elif color == ROOMCOLOR["blue"]:
        return "Blue"
    elif color == ROOMCOLOR["white"]:
        return "White"
    elif color == ROOMCOLOR["grey"]:
        return "Grey"
    else:
        return "Unknown"

class Base_Room(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, corner=False, color=ROOMCOLOR["grey"], number=0):
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
        names = {(ROOMCOLOR["blue"], 1): "Central",
                 (ROOMCOLOR["blue"], 2): "Exit",
                 (ROOMCOLOR["blue"], 3): "Key",
                 (ROOMCOLOR["green"], 1): "Empty",
                 (ROOMCOLOR["green"], 2): "Vision",
                 (ROOMCOLOR["green"], 3): "Swapping",
                 (ROOMCOLOR["green"], 4): "Shifting",
                 (ROOMCOLOR["green"], 5): "Portal",
                 (ROOMCOLOR["green"], 6): "Regeneration",
                 (ROOMCOLOR["green"], 7): "Robot",
                 (ROOMCOLOR["red"], 1): "Acid",
                 (ROOMCOLOR["red"], 2): "Death",
                 (ROOMCOLOR["red"], 3): "Trap",
                 (ROOMCOLOR["red"], 4): "Flooded",
                 (ROOMCOLOR["red"], 5): "Shredder",
                 (ROOMCOLOR["red"], 6): "Timer",
                 (ROOMCOLOR["red"], 7): "Paranoia",
                 (ROOMCOLOR["red"], 8): "Illusion",
                 (ROOMCOLOR["yellow"], 1): "Vortex",
                 (ROOMCOLOR["yellow"], 2): "Prison",
                 (ROOMCOLOR["yellow"], 3): "Cold",
                 (ROOMCOLOR["yellow"], 4): "Dark",
                 (ROOMCOLOR["yellow"], 5): "Pivot",
                 (ROOMCOLOR["yellow"], 6): "Jamming",
                 (ROOMCOLOR["yellow"], 7): "M.A.C.",
                 (ROOMCOLOR["yellow"], 8): "Mirror"
                 }
        return names.get((self.color, self.number), "Unknown")
    	
    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)

class Text_Sprite(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, color, text=None):
        super().__init__()
        self.text = text
        self.color = color
        self.image = pygame.image.load(f"Game/Assets/Color.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)
        self.rect = self.image.get_rect()
        self.update_image()
    
    def update_image(self):
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.image.fill(self.color)

    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)
        if self.text:
            text = pygame.font.SysFont('arial', 15).render(f"{self.text}", True, (0,0,0))
            surface.blit(text, (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.rect.height/2 - text.get_height()/2))

class Player(Text_Sprite):
    def __init__(self, color, number=0):
        super().__init__(color=color)
        self.color = color
        self.number = number
        self.is_selected = False

    def draw(self, surface):
        super().draw(surface)
        if self.is_selected:
            image = pygame.image.load(f"Game/Assets/O.png")
            image = pygame.transform.scale(image, (40, 40))
            surface.blit(image, (self.rect.centerx - image.get_width()/2, self.rect.centery - image.get_height()/2))

class Info(Text_Sprite):
    sprite_size = (50, 20)
    def __init__(self, color, player=None):
        super().__init__(color=color)
        self.player = player
        self.color = color
    
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
        self._player = player
        if player:
            self.text = player.number
        else:
            self.text = None

class Room(Base_Room):
    sprite_size = (50, 50)
    show_info = False
    def __init__(self, corner=False, color=ROOMCOLOR["grey"], number=0):
        super().__init__(corner=corner, color=color, number=number)
        # whenever someone looks at the room, add the info based on what they see
        self.info = []
        self.is_selected = False
        self.was_selected = 0

    def add_info(self, color, player):
        self.info.append(Info(color=color, player=player))

    def remove_info(self):
        if self.info:
            self.info.pop()
    
    def draw(self, surface):
        self.update_image()
        surface.blit(self.image, self.rect)
        if self.number == 0 or self.show_info:
            for i, info in enumerate(self.info):
                info.rect.width = self.sprite_size[1] / len(self.info)
                info.rect.bottomleft = (self.rect.bottomleft[0] + i * info.rect.width, self.rect.bottomleft[1])
                info.draw(surface)
        if self.corner and self.name() == "Unknown":
            pygame.draw.circle(surface, "blue", self.rect.center, 7.5)
        if self.was_selected:
            pygame.draw.circle(surface, (180, 180, 180), self.rect.center, 5.5) # color = grey
        if self.is_selected:
            pygame.draw.circle(surface, "green", self.rect.center, 5.5)
            

class Shift_Arrow(pygame.sprite.Sprite):
    sprite_size = (50, 50)
    def __init__(self, direction, number):
        super().__init__()
        self.direction = direction
        self.number = number
        self.consecutive_clicks = 0
        self.image = pygame.image.load(f"Game/Assets/Shift_Arrow.png")
        self.image = pygame.transform.scale(self.image, self.sprite_size)
        self.image = pygame.transform.rotate(self.image, 90 * direction)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.consecutive_clicks > 0:
            text = pygame.font.SysFont('arial', 15).render(f"{self.consecutive_clicks}", True, (0,0,0))
            surface.blit(text, (self.rect.x + self.rect.width/2 - text.get_width()/2, self.rect.y + self.rect.height/2 - text.get_height()/2))
    
    def __eq__(self, other):
        if isinstance(other, Shift_Arrow):
            return self.direction == other.direction and self.number == other.number
        return False
    
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
                    self.rooms[(x, y)].color = ROOMCOLOR["blue"]
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
    
    def get_room_pos(self, room:Room):
        for pos, r in self.rooms.items():
            if r == room:
                return pos
        return None
    
    def swap_rooms(self, room1, room2):
        pos_1 = self.get_room_pos(room1)
        pos_2 = self.get_room_pos(room2)
        self.rooms[pos_1] = room2
        self.rooms[pos_2] = room1

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
    
    def toggle_show_info(self):
        Room.show_info = not Room.show_info

class Room_Notes():
    sprite_size = (50, 50)
    starting_center = (50, 400)

    def __init__(self):
        self.blue_rooms = [Base_Room(color=ROOMCOLOR["blue"], number=i) for i in range(1, 4)]
        self.green_rooms = [Base_Room(color=ROOMCOLOR["green"], number=i) for i in range(1, 8)]
        self.yellow_rooms = [Base_Room(color=ROOMCOLOR["yellow"], number=i) for i in range(1, 9)]
        self.red_rooms = [Base_Room(color=ROOMCOLOR["red"], number=i) for i in range(1, 9)]
        self.undo_room = Base_Room(color=ROOMCOLOR["grey"], number=0)
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

    def __init__(self):
        self.notes = [Info(color=color) for color in ROOMCOLOR.values()]
        self.undo_note = Info(color=ROOMCOLOR["white"], player=None)
        self.swap_note = Info(color=ROOMCOLOR["white"], player=None)
        self.swap = False
        for note in self.all_notes():
            note.image = pygame.transform.scale(note.image, self.sprite_size)
            note.rect = note.image.get_rect()
    
    @property
    def swap(self):
        return self._swap

    @swap.setter
    def swap(self, swap_selected:bool):
        self._swap = swap_selected
        if self.swap:
            self.swap_note.color = ROOMCOLOR["green"]
        else:
            self.swap_note.color = ROOMCOLOR["white"]

    def all_notes(self):
        return self.notes + [self.undo_note] + [self.swap_note]

    def draw(self, surface):
        for i, note in enumerate(self.all_notes()):
            note.rect.center = (self.starting_center[0], self.starting_center[1] + self.sprite_size[1] * i)
            if note == self.swap_note:
                note.rect.center = (self.starting_center[0] - self.sprite_size[0], self.starting_center[1] + self.sprite_size[1] * (i-1))
            note.draw(surface)
            if note == self.undo_note:
                image = pygame.image.load(f"Game/Assets/X.png")
                image = pygame.transform.scale(image, (30, 30))
                surface.blit(image, (note.rect.centerx - image.get_width()/2, note.rect.centery - image.get_height()/2))
            if note == self.swap_note:
                image = pygame.image.load(f"Game/Assets/Swap.png")
                image = pygame.transform.scale(image, (30, 30))
                surface.blit(image, (note.rect.centerx - image.get_width()/2, note.rect.centery - image.get_height()/2))

class Player_Notes():
    sprite_size = (50, 50)
    starting_center = (500, 0)
    selection_center = (100, 200)

    def __init__(self) -> None:
        self.players = []
        self.possible_players = [Player(color=color, number=0) for color in PLAYERCOLOR.values()]

    def draw_selection(self, surface):
        for i, player in enumerate(self.possible_players):
            player.rect.center = (self.selection_center[0]+ self.sprite_size[0] * i, self.selection_center[1])
            player.draw(surface)

    def finalise_players(self):
        for player in self.players.copy():
            if player.number == 0:
                self.players.remove(player)
        self.players = sorted(self.players, key=lambda player: player.number)

    def draw(self, surface):
        for player in self.players:
            player.rect.center = (self.starting_center[0], self.starting_center[1] + self.sprite_size[1] * player.number)
            player.draw(surface)