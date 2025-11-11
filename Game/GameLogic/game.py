# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity
import pickle
import sys
import os

import tkinter as tk
from tkinter import filedialog

from Game.GameLogic.utils import edit_filename

def _resolve_savefiles_base():
    candidates = []

    # 1) If frozen (PyInstaller/py2exe), check common runtime locations
    if getattr(sys, 'frozen', False):
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            candidates.append(meipass)

    # Last resort: assume repository layout relative to this file
    try:
        fallback = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'SaveFiles')
        return os.path.normpath(fallback)
    except Exception:
        # extremely fallback to current directory Assets
        return os.path.normpath(os.path.join(os.getcwd(), 'SaveFiles'))
    

SAVEFILES_BASE = _resolve_savefiles_base()

class GameState:
    def __init__(self):
        self.draw_callback = {}
        self.click_callback = {}
        self.grid = entity.Grid()
        self.room_notes = entity.Room_Notes()
        self.color_notes = entity.Color_Notes()
        self.player_notes = entity.Player_Notes()
        self.setting_notes = entity.Setting_Notes()
        self.selected_player = None
        self.selected_grid_room = None
        self.old_grid_room = None
        self.old_arrow = None
        # possible states: start, play, name
        self.state = "start"
        self.mode = "play"
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state
        # reset board
        self.draw_callback = {}
        self.click_callback = {}
        # add board drawables and clickables
        if self.state == "play":
            self.play_state()
            return
        if self.state == "start":
            self.start_state()
            return
        

    def start_state(self):
        self.draw_callback["player_notes"] = self.player_notes.draw
        self.click_callback["player_notes"] = self.player_selection_note_clicked
        self.click_callback["confirm_note"] = self.player_confirm_note_clicked
        self.draw_callback["setting_notes"] = self.setting_notes.draw
        self.click_callback["setting_notes"] = self.setting_note_clicked
    
    def play_state(self):
        self.draw_callback["grid"] = self.grid.draw
        self.click_callback["grid_room"] = self.grid_room_clicked
        self.click_callback["grid_arrow"] = self.arrow_clicked
        self.draw_callback["room_notes"] = self.room_notes.draw
        self.click_callback["room_notes"] = self.room_note_clicked
        self.draw_callback["color_notes"] = self.color_notes.draw
        self.click_callback["color_notes"] = self.color_note_clicked
        self.draw_callback["player_notes"] = self.player_notes.draw
        self.click_callback["player_notes"] = self.player_note_clicked
        self.draw_callback["setting_notes"] = self.setting_notes.draw
        self.click_callback["setting_notes"] = self.setting_note_clicked
    
    def draw(self, surface):
        for drawfunc in self.draw_callback.values():
            drawfunc(surface)
        if self.state == "start":
            pos = (self.player_notes.selection_center[0], self.player_notes.selection_center[1] - 2*self.player_notes.sprite_size[1])
            entity.draw_caption(pos=pos, text="Player Selection", surface=surface)

    def handle_click(self, pos):
        # do not get any mouse input while naming a player
        if self.mode == "name":
            return
        if self.click_callback.get("setting_notes", None):
            for note in self.setting_notes.all_notes():
                if note.rect.collidepoint(pos):
                    print(f"Clicked on setting note")
                    self.click_callback["setting_notes"](note)
                    return
        self.setting_notes.deselect_all()
            
        if self.click_callback.get("grid_arrow", None):
            for arrow in self.grid.arrows:
                if arrow.rect.collidepoint(pos):
                    print(f"Clicked on arrow {arrow.direction}, {arrow.number}")
                    self.click_callback["grid_arrow"](arrow)
                    return
        if self.click_callback.get("grid_room", None):
            for room in self.grid.rooms.values():
                if room.rect.collidepoint(pos):
                    print(f"Clicked on room {room.color}{room.number}")
                    self.click_callback["grid_room"](room)
                    return
        if self.click_callback.get("room_notes", None):
            for room in self.room_notes.all_rooms():
                if room.rect.collidepoint(pos):
                    print(f"Clicked on note room {room.color}{room.number}")
                    self.click_callback["room_notes"](room)
                    return
        if self.click_callback.get("color_notes", None):
            for note in self.color_notes.all_notes():
                if note.rect.collidepoint(pos):
                    print(f"Clicked on color note {note.color}")
                    self.click_callback["color_notes"](note)
                    return
        if self.click_callback.get("player_notes", None):
            for player in self.player_notes.players:
                if player.rect.collidepoint(pos):
                    print(f"Clicked on player note {player.color}{player.number}")
                    self.click_callback["player_notes"](player)
                    return
        if self.click_callback.get("confirm_note", None):
                if self.player_notes.confirm_note.rect.collidepoint(pos):
                    print(f"Clicked on confirm note")
                    self.click_callback["confirm_note"]()
                    return
                
    def deselect_old_grid(self):
        if self.old_grid_room:
            self.old_grid_room.was_selected = False
        self.old_grid_room = None
        print("deselect")

    def deselect_old_arrow(self):
        if self.old_arrow:
            self.old_arrow.consecutive_clicks = 0
        self.old_arrow = None
    
    def arrow_clicked(self, arrow):
        self.deselect_old_grid()
        self.grid.shift_rooms(arrow.direction, arrow.number)
        if self.old_arrow != arrow:
            self.deselect_old_arrow()
        self.old_arrow = arrow
        self.old_arrow.consecutive_clicks += 1

    def grid_room_clicked(self, room):
        self.deselect_old_arrow()
        self.deselect_old_grid()
        if self.selected_grid_room:
            if self.color_notes.swap:
                # Swap the the two rooms
                self.grid.swap_rooms(self.selected_grid_room, room)
                self.color_notes.swap = False
                self.old_grid_room = self.selected_grid_room
                print("select")
                self.old_grid_room.was_selected = True
            self.selected_grid_room.is_selected = False
        self.selected_grid_room = room
        self.selected_grid_room.is_selected = True
    
    def color_note_clicked(self, note):
        # Implement logic for when a color note is clicked
        # For example, toggle the note's state or remove it from the list
        self.deselect_old_grid()
        self.deselect_old_arrow()
        if self.selected_grid_room:
            if note == self.color_notes.undo_note:
                self.selected_grid_room.remove_info()
            elif note == self.color_notes.swap_note:
                self.color_notes.swap = not self.color_notes.swap
            else:
                self.selected_grid_room.add_info(note.color, self.selected_player)

    def player_note_clicked(self, player):
        if self.selected_player:
            self.selected_player.is_selected = False
        self.selected_player = player
        player.is_selected = True
    
    def player_selection_note_clicked(self, player):
        self.player_note_clicked(player=player)
        self.player_notes.assign_number(player)

    def player_confirm_note_clicked(self):
        self.player_notes.finalise_players()
        self.player_note_clicked(self.player_notes.players[0])
        self.state = "play"
        self.grid_room_clicked(self.grid.rooms[(2,2)])
        
    def room_note_clicked(self, room):
        # Implement logic for when a room note is clicked
        self.deselect_old_grid()
        self.deselect_old_arrow()
        if self.selected_grid_room:
            self.selected_grid_room.color = room.color
            self.selected_grid_room.number = room.number
            
    def setting_note_clicked(self, note):
        # undo selection of other setting notes
        if note != self.setting_notes.save_note:
            self.setting_notes.save = False
        if note != self.setting_notes.load_note:
            self.setting_notes.load = False
        if note != self.setting_notes.restart_note:
            self.setting_notes.restart = False
            
        if note == self.setting_notes.save_note:
            self.save_game()
        elif note == self.setting_notes.load_note:
            self.load_game()
        elif note == self.setting_notes.restart_note:
            self.restart_game()
    
    def key_pressed(self, keychar):
        if keychar == "return":
            self.return_pressed()
            self.setting_notes.deselect_all()
            return
        if self.mode == "name":
            self.name(keychar)
            return
        
        if keychar == "r":
            self.setting_note_clicked(self.setting_notes.restart_note)
            return
        if keychar == "s":
            self.setting_note_clicked(self.setting_notes.save_note)
            return
        if keychar == "l":
            self.setting_note_clicked(self.setting_notes.load_note)
            return
        self.setting_notes.deselect_all()
        
        if keychar == " ":
            self.space_pressed()
            return
    
    def return_pressed(self):
        if self.mode == "play" and self.selected_player != None:
            self.mode = "name"
            self.selected_player.name = "_"
            print(self.selected_player.name)
        elif self.mode == "name":
            self.name(None)
            self.room_notes.all_rooms()
            self.mode = "play"
    
    def space_pressed(self):
        # Space bar toggles show info
        self.grid.toggle_show_info()
        
    def name(self, char):
        if self.selected_player: 
            self.selected_player.name = self.selected_player.name[:-1]
            if char == "backspace":
                if self.selected_player.name:
                    self.selected_player.name = self.selected_player.name[:-1]
            elif char:
                self.selected_player.name += char
            if char != None:
                self.selected_player.name += "_"
        else:
            print("tried to name without a player")
            
    def save_game(self, filename="savefile"):
        if not self.setting_notes.save:
            self.setting_notes.save = True
            return
        self.setting_notes.save = False
        
        print("Saving game...")
        file_path = filedialog.asksaveasfilename(initialdir=SAVEFILES_BASE, title="Save Game As", initialfile=edit_filename(filename), defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        with open(file_path, 'wb') as f:
            pickle.dump(self.to_save_dict(), f)
    
    def load_game(self):
        if not self.setting_notes.load:
            self.setting_notes.load = True
            return
        self.setting_notes.load = False
        
        print("Loading game...")
        file_path = filedialog.askopenfilename(initialdir=SAVEFILES_BASE, title="Select Save File", defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        with open(file_path, 'rb') as f:
            self.from_save_dict(pickle.load(f))
    
    def restart_game(self):
        if not self.setting_notes.restart:
            self.setting_notes.restart = True
            return
        self.setting_notes.restart = False
        
        print("Restarting game...")
        self.__init__()
        
    def to_save_dict(self):
        # Convert the current game state to a dictionary for saving
        save_dict = {
            "grid": self.grid.to_save_dict(),
            "player_notes": self.player_notes.to_save_dict(),
            "state": self.state,
            "mode": self.mode,
        }
        
        return save_dict
    
    def from_save_dict(self, save_dict):
        # Load the game state from a saved dictionary
        self.grid.from_save_dict(save_dict["grid"])
        self.player_notes.from_save_dict(save_dict["player_notes"])
        self.state = save_dict["state"]
        self.mode = save_dict["mode"]
        
        self.selected_player = None
        for player in self.player_notes.players:
            if player.is_selected:
                self.selected_player = player
                break
        self.selected_grid_room = None
        self.old_grid_room = None
        for room in self.grid.rooms.values():
            if room.is_selected:
                self.selected_grid_room = room
            if room.was_selected:
                self.old_grid_room = room
        self.old_arrow = None
        for arrow in self.grid.arrows:
            if arrow.consecutive_clicks > 0:
                self.old_arrow = arrow
                break