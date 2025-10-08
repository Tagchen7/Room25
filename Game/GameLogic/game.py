# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.draw_callback = {}
        self.click_callback = {}
        self.grid = entity.Grid()
        self.room_notes = entity.Room_Notes()
        self.color_notes = entity.Color_Notes()
        self.player_notes = entity.Player_Notes()
        #TODO: add player selection
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
    
    def draw(self, surface):
        for drawfunc in self.draw_callback.values():
            drawfunc(surface)

    def handle_click(self, pos):
        # do not get any mouse input while naming a player
        if self.mode == "name":
            return
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
    
    def key_pressed(self, keychar):
        if keychar == "return":
            self.return_pressed()
        elif self.mode == "name":
            self.name(keychar)
        elif keychar == " ":
            self.space_pressed()
    
    def return_pressed(self):
        if self.mode == "play" and self.selected_player != None:
            self.mode = "name"
            self.selected_player.name = "_"
            print(self.selected_player.name)
        elif self.mode == "name":
            self.name(None)
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
                self.selected_player.name += "_"
            elif char:
                self.selected_player.name += char + "_"
        else:
            print("tried to name without a player")