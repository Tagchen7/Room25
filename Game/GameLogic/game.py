# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()
        self.room_notes = entity.Room_Notes()
        self.color_notes = entity.Color_Notes()
        self.selected_player = entity.Player(color=entity.RED)
        self.selected_grid_room = None
        self.selected_action = None
    
    def draw(self, surface):
        self.grid.draw(surface)
        self.room_notes.draw(surface)
        self.color_notes.draw(surface)

    def grid_room_clicked(self, room):
        if self.selected_grid_room:
            self.selected_grid_room.is_selected = False
        self.selected_grid_room = room
        room.is_selected = True
    
    def color_note_clicked(self, color):
        # Implement logic for when a color note is clicked
        # For example, toggle the note's state or remove it from the list
        if self.selected_grid_room:
            self.selected_grid_room.add_info(color, self.selected_player)
        
    def room_note_clicked(self, room):
        # Implement logic for when a room note is clicked
        if self.selected_grid_room:
            self.selected_grid_room.color = room.color
            self.selected_grid_room.number = room.number

    def space_pressed(self):
        # Implement logic for when the space bar is pressed
        self.grid.toggle_show_info()