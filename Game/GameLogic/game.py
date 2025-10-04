# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()
        self.room_notes = entity.Room_Notes()
        self.color_notes = entity.Color_Notes()
        self.selected_player = None
        self.selected_grid_room = None
        self.selected_action = None

        # Test setup
        self.grid.rooms[(0, 0)].color = entity.RED
        self.grid.rooms[(0, 0)].number = 2
        self.grid.rooms[(4, 0)].color = entity.YELLOW
        self.grid.rooms[(4, 0)].number = 2
        self.grid.rooms[(0, 4)].color = entity.GREEN
        self.grid.rooms[(0, 4)].number = 5
        self.grid.rooms[(4, 4)].color = entity.BLUE
        self.grid.rooms[(4, 4)].number = 2
        pr = entity.Player("red")
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=pr, color=entity.RED))
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=entity.Player("green"), color=entity.GREEN))
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=entity.Player("brown"), color=entity.YELLOW))
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=pr, color=entity.BLUE))
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=pr, color=entity.GREY))
        self.grid.rooms[(1, 1)].info.append(entity.Info(player=pr, color=entity.WHITE))
    
    def draw(self, surface):
        self.grid.draw(surface)
        self.room_notes.draw(surface)
        self.color_notes.draw(surface)