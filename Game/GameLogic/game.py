# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()
        self.grid.rooms[(0, 0)].color = "red"
        self.grid.rooms[(0, 0)].number = 2
        self.grid.rooms[(4, 0)].color = "yellow"
        self.grid.rooms[(4, 0)].number = 2
        self.grid.rooms[(0, 4)].color = "green"
        self.grid.rooms[(0, 4)].number = 5
        self.grid.rooms[(4, 4)].color = "blue"
        self.grid.rooms[(4, 4)].number = 2