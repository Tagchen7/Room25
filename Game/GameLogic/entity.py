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
    def __init__(self, sprite_size = (50, 50), corner=False, color=ROOMCOLOR["grey"], number=0):
        super().__init__()
        # Center = (0, 0)
        self.rect = pygame.Rect((0,0), sprite_size)
        self.corner = corner
        self._color = color
        self._number = number
        self.update_image()
    
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
            self.image = pygame.image.load(f"Game/Assets/{get_color_name(self.color)}_{self.number}.png")
        self.image = pygame.transform.scale(self.image, self.rect.size)

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
        surface.blit(self.image, self.rect)

class Text_Sprite(pygame.sprite.Sprite):

    def __init__(self, sprite_size, color, text=None):
        super().__init__()
        self.image = pygame.image.load(f"Game/Assets/Color.png")
        self.image = pygame.transform.scale(self.image, sprite_size)
        self.rect = self.image.get_rect()
        self.text = text
        self.color = color
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        self.image.fill(self.color)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        self.rendered_text = pygame.font.SysFont('arial', 15).render(f"{self.text}", True, (0,0,0))

    
    def change_image(self, width=None, height=None, size=None, color=None, text=None):
        # if size changes, update image size
        # size overwrites height/width params
        if height != None or width != None or size != None:
            if height != None:
                self.rect.height = height
            if width != None:
                self.rect.width = width
            if size != None:
                self.rect.size = size
            self.image = pygame.transform.scale(self.image, self.rect.size)
            self.rect = self.image.get_rect()
        if color != None:
            self.color = color
        if text != None:
            self.text = text

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.text:
            surface.blit(self.rendered_text, (self.rect.x + self.rect.width/2 - self.rendered_text.get_width()/2, self.rect.y + self.rect.height/2 - self.rendered_text.get_height()/2))

class Player(Text_Sprite):
    def __init__(self, sprite_size, color, number=0, selected_sprite_size=(40, 40)):
        super().__init__(sprite_size=sprite_size, color=color)
        self.color = color
        self.number = number
        self.is_selected = False
        self.is_selected_image = pygame.image.load(f"Game/Assets/O.png")
        self.is_selected_image = pygame.transform.scale(self.is_selected_image, selected_sprite_size)

    def draw(self, surface):
        self.text = self.number
        super().draw(surface)
        if self.is_selected:
            surface.blit(self.is_selected_image, (self.rect.centerx - self.is_selected_image.get_width()/2, self.rect.centery - self.is_selected_image.get_height()/2))

class Info(Text_Sprite):
    show_player = True
    def __init__(self, sprite_size, color, player=None):
        super().__init__(sprite_size=sprite_size, color=color)
        self.player_info_sprite = Text_Sprite(sprite_size=(sprite_size[0], sprite_size[1] / 2), color=PLAYERCOLOR["grey"], text=None)
        self.player = player
        self.color = color
        self.change_image(size=sprite_size)

    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
        self._player = player
        if player:
            self.player_info_sprite.color = player.color
            if player.number > 0:
                self.text = player.number
            else:
                self.text = None
        else:
            self.text = None

    def change_image(self, width=None, height=None, size=None, color=None, text=None):
        super().change_image(width=width, height=height, size=size, color=color, text=text)
        heightmod = 3
        newheight = height / heightmod if height else height
        newwidth = width
        if size:
            newwidth = size[0]
            newheight = size[1] / heightmod
        self.player_info_sprite.change_image(width=newwidth, height=newheight)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.show_player and self.player:
            self.player_info_sprite.rect.bottomleft = self.rect.topleft
            self.player_info_sprite.draw(surface=surface)
        if self.text:
            surface.blit(self.rendered_text, (self.rect.x + self.rect.width/2 - self.rendered_text.get_width()/2, self.rect.y + self.rect.height/2 - self.rendered_text.get_height()/2))


class Room(Base_Room):
    show_info = True

    def __init__(self, sprite_size=(50, 50), info_height=20, corner=False, color=ROOMCOLOR["grey"], number=0):
        super().__init__(sprite_size=sprite_size, corner=corner, color=color, number=number)
        # whenever someone looks at the room, add the info based on what they see
        self.info_height = info_height
        self.info = []
        self.is_selected = False
        self.was_selected = 0

    def add_info(self, color, player):
        self.info.append(Info(sprite_size=(self.info_height, self.info_height), color=color, player=player))
        self.update_info()

    def remove_info(self):
        if self.info:
            self.info.pop()
            self.update_info()

    def update_info(self):
        new_sprite_width = 0
        if self.info:
            new_sprite_width = self.rect.width / len(self.info)
        for i, info in enumerate(self.info):
            info.change_image(height=self.info_height, width=new_sprite_width)
            info.rect.bottomleft = (self.rect.bottomleft[0] + i * info.rect.width, self.rect.bottomleft[1])
    
    def draw(self, surface):
        super().draw(surface)
        if self.number == 0 or self.show_info:
            for info in self.info:
                self.update_info()
                info.draw(surface)
        if self.corner and self.name() == "Unknown":
            pygame.draw.circle(surface, "blue", self.rect.center, 7.5)
        if self.was_selected:
            pygame.draw.circle(surface, (180, 180, 180), self.rect.center, 5.5) # color = grey
        if self.is_selected:
            pygame.draw.circle(surface, "green", self.rect.center, 5.5)          

class Shift_Arrow(pygame.sprite.Sprite):
    def __init__(self, direction, number, sprite_size=(50, 50)):
        super().__init__()
        self.direction = direction
        self.number = number
        self.consecutive_clicks = 0
        self.image = pygame.image.load(f"Game/Assets/Shift_Arrow.png")
        self.image = pygame.transform.scale(self.image, sprite_size)
        self.image = pygame.transform.rotate(self.image, 90 * direction)
        self.rect = self.image.get_rect()

    @property
    def consecutive_clicks(self):
        return self._consecutive_clicks
    
    @consecutive_clicks.setter
    def consecutive_clicks(self, consecutive_clicks):
        self._consecutive_clicks = consecutive_clicks
        self.rendered_text = pygame.font.SysFont('arial', 15).render(f"{self.consecutive_clicks}", True, (0,0,0))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.consecutive_clicks > 0:
            surface.blit(self.rendered_text, (self.rect.x + self.rect.width/2 - self.rendered_text.get_width()/2, self.rect.y + self.rect.height/2 - self.rendered_text.get_height()/2))
    
    def __eq__(self, other):
        if isinstance(other, Shift_Arrow):
            return self.direction == other.direction and self.number == other.number
        return False
    
class Grid:
    size = 5
    def __init__(self, room_size=(50, 50)):
        # self.rooms have a tuple denoting position as key (x, y) = (0, 1) and a room at the position
        # room positions are in range(size)
        # center room is always B1
        self.room_size = room_size
        self.rooms = {}
        for x in range(5):
            cx = x - self.size//2
            for y in range(5):
                cy = y - self.size//2
                corner = (cx!=0 and cy!=0) and (abs(cx) != 1 or abs(cy) != 1)
                self.rooms[(x, y)] = Room(corner=corner, sprite_size=self.room_size)
                if cx == 0 and cy == 0:
                    self.rooms[(x, y)].color = ROOMCOLOR["blue"]
                    self.rooms[(x, y)].number = 1
        self.arrows = []
        for i in range(self.size):
            ci = i - self.size//2
            if ci != 0:
                self.arrows.append(Shift_Arrow(direction=0, number=i, sprite_size=self.room_size))  # right
                self.arrows.append(Shift_Arrow(direction=1, number=i, sprite_size=self.room_size))  # down
                self.arrows.append(Shift_Arrow(direction=2, number=i, sprite_size=self.room_size))  # left
                self.arrows.append(Shift_Arrow(direction=3, number=i, sprite_size=self.room_size))  # up

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
        # 0I -> RI -> R0 -> 00
        if Room.show_info and Info.show_player:
            Info.show_player = False
            return
        if Room.show_info and not Info.show_player:
            Room.show_info = False
            return
        if not Room.show_info and not Info.show_player:
            Info.show_player = True
            return
        else:
            Room.show_info = True
            return

class Room_Notes():
    starting_center = (50, 400)

    def __init__(self, sprite_size=(50, 50)):
        self.sprite_size = sprite_size
        self.blue_rooms = [Base_Room(color=ROOMCOLOR["blue"], number=i, sprite_size=sprite_size) for i in range(1, 4)]
        self.green_rooms = [Base_Room(color=ROOMCOLOR["green"], number=i, sprite_size=sprite_size) for i in range(1, 8)]
        self.yellow_rooms = [Base_Room(color=ROOMCOLOR["yellow"], number=i, sprite_size=sprite_size) for i in range(1, 9)]
        self.red_rooms = [Base_Room(color=ROOMCOLOR["red"], number=i, sprite_size=sprite_size) for i in range(1, 9)]
        self.undo_room = Base_Room(color=ROOMCOLOR["grey"], number=0, sprite_size=sprite_size)
        for room in self.all_rooms():
            room.rect = room.image.get_rect()
        self.init_rect_pos()

    def all_rooms(self):
        return self.blue_rooms + self.green_rooms + self.yellow_rooms + self.red_rooms + [self.undo_room]

    def init_rect_pos(self):
        for room in self.blue_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1])
        self.undo_room.rect.center = (self.starting_center[0] + self.sprite_size[0] * 6, self.starting_center[1])
        for room in self.green_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + self.sprite_size[1])
        for room in self.yellow_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + 2 * self.sprite_size[1])
        for room in self.red_rooms:
            room.rect.center = (self.starting_center[0] + self.sprite_size[0] * (room.number - 1), self.starting_center[1] + 3 * self.sprite_size[1])

    def draw(self, surface):
        for room in self.all_rooms():
            room.draw(surface)

class Color_Notes():
    starting_center = (400, 50)

    def __init__(self, sprite_size = (50, 50), symbol_sprite_size = (30, 30)):
        self.sprite_size = sprite_size
        self.notes = [Info(color=color, sprite_size=sprite_size, player=None) for color in ROOMCOLOR.values()]
        self.undo_note = Info(color=ROOMCOLOR["white"], sprite_size=sprite_size, player=None)
        self.swap_note = Info(color=ROOMCOLOR["white"], sprite_size=sprite_size, player=None)
        self.swap = False
        self.undo_image = pygame.image.load(f"Game/Assets/X.png")
        self.undo_image = pygame.transform.scale(self.undo_image, symbol_sprite_size)
        self.swap_image = pygame.image.load(f"Game/Assets/Swap.png")
        self.swap_image = pygame.transform.scale(self.swap_image, symbol_sprite_size)
        self.init_rect_pos()
    
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

    def init_rect_pos(self):
        for i, note in enumerate(self.all_notes()):
            note.rect.center = (self.starting_center[0], self.starting_center[1] + self.sprite_size[1] * i)
            if note == self.swap_note:
                note.rect.center = (self.starting_center[0] - self.sprite_size[0], self.starting_center[1] + self.sprite_size[1] * (i-1))

    def draw(self, surface):
        for note in self.all_notes():
            note.draw(surface)
            if note == self.undo_note:
                surface.blit(self.undo_image, (note.rect.centerx - self.undo_image.get_width()/2, note.rect.centery - self.undo_image.get_height()/2))
            if note == self.swap_note:
                surface.blit(self.swap_image, (note.rect.centerx - self.swap_image.get_width()/2, note.rect.centery - self.swap_image.get_height()/2))

class Player_Notes():
    starting_center = (500, 0)
    selection_center = (100, 200)
    min_players = 4

    def __init__(self, sprite_size=(50, 50), selected_sprite_size=(40, 40)) -> None:
        self.sprite_size = sprite_size
        self.selected_sprite_size = selected_sprite_size
        self.players = self.all_players(ordered=False)
        self.confirm_note = Info(color=ROOMCOLOR["white"], sprite_size=sprite_size, player=None)
        self.confirmed_players = False
        self.confirm_image = pygame.image.load(f"Game/Assets/O.png")
        self.confirm_image = pygame.transform.scale(self.confirm_image, selected_sprite_size)
        self.update_rect_pos()

    def all_players(self, ordered = False):
        step = 1 if ordered else 0
        return [Player(color=color, number=(i+1)*step, sprite_size=self.sprite_size, selected_sprite_size=self.selected_sprite_size) for i, color in enumerate(PLAYERCOLOR.values())]
    
    def assign_number(self, player):
        if player.number > 0:
            player.number = 0
        else:
            player.number = self.get_lowest_missing_number()
    
    def get_lowest_missing_number(self):
        possible_numbers = [i+1 for i in range(len(self.all_players()))]
        for player in self.players:
            if player.number in possible_numbers:
                possible_numbers.remove(player.number)
        if possible_numbers:
            return min(possible_numbers)
        return 0

    def finalise_players(self):
        self.confirmed_players = True
        for player in self.players.copy():
            if player.number == 0:
                self.players.remove(player)
        if len(self.players) < self.min_players:
            self.players = self.all_players(ordered=True)
        self.players = sorted(self.players, key=lambda player: player.number)
        self.update_rect_pos()

    def update_rect_pos(self):
        if not self.confirmed_players:
            for i, player in enumerate(self.players + [self.confirm_note]):
                player.rect.center = (self.selection_center[0]+ self.sprite_size[0] * i, self.selection_center[1])
        else:
            for player in self.players:
                player.rect.center = (self.starting_center[0], self.starting_center[1] + self.sprite_size[1] * player.number)

    def draw(self, surface):
        for player in self.players:
            player.draw(surface)
        if not self.confirmed_players:
            self.confirm_note.draw(surface=surface)
            surface.blit(self.confirm_image, (self.confirm_note.rect.centerx - self.confirm_image.get_width()/2, self.confirm_note.rect.centery - self.confirm_image.get_height()/2))