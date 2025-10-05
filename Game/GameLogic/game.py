# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()
        self.room_notes = entity.Room_Notes()
        self.color_notes = entity.Color_Notes()
        self.selected_player = entity.Player(color=entity.PLAYERCOLOR["brown"])
        self.selected_grid_room = None
        self.old_grid_room = None
        self.old_arrow = None
    
    def draw(self, surface):
        self.grid.draw(surface)
        self.room_notes.draw(surface)
        self.color_notes.draw(surface)

    def handle_click(self, pos):
            #print(pygame.mouse.get_pos())
            # check if an arrow was clicked
            for arrow in self.grid.arrows:
                if arrow.rect.collidepoint(pos):
                    print(f"Clicked on arrow {arrow.direction}, {arrow.number}")
                    self.arrow_clicked(arrow)
                    return
            for room in self.grid.rooms.values():
                if room.rect.collidepoint(pos):
                    print(f"Clicked on room {room.color}{room.number}")
                    self.grid_room_clicked(room)
                    return
            for room in self.room_notes.all_rooms():
                if room.rect.collidepoint(pos):
                    print(f"Clicked on note room {room.color}{room.number}")
                    self.room_note_clicked(room)
                    return
            for note in self.color_notes.all_notes():
                if note.rect.collidepoint(pos):
                    print(f"Clicked on color note {note.color}")
                    self.color_note_clicked(note)
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
            if note == self.color_notes.swap_note:
                self.color_notes.swap = not self.color_notes.swap
            else:
                self.selected_grid_room.add_info(note.color, self.selected_player)

        
    def room_note_clicked(self, room):
        # Implement logic for when a room note is clicked
        self.deselect_old_grid()
        self.deselect_old_arrow()
        if self.selected_grid_room:
            self.selected_grid_room.color = room.color
            self.selected_grid_room.number = room.number

    def space_pressed(self):
        # Implement logic for when the space bar is pressed
        self.grid.toggle_show_info()