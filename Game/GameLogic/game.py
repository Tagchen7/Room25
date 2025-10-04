# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()
        self.grid.rooms[0, 0].corner = True  # center room is always a corner
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
        self.grid.rooms[(1, 1)].info.append(entity.Info(pr, entity.RED))
        self.grid.rooms[(1, 1)].info.append(entity.Info(entity.Player("green"), entity.GREEN))
        self.grid.rooms[(1, 1)].info.append(entity.Info(entity.Player("brown"), entity.YELLOW))
        self.grid.rooms[(1, 1)].info.append(entity.Info(pr, entity.BLUE))
        self.grid.rooms[(1, 1)].info.append(entity.Info(pr, entity.GREY))
        self.grid.rooms[(1, 1)].info.append(entity.Info(pr, entity.WHITE))