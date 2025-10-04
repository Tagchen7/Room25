# Contains the main game logic, including game initialization, game loop, collision detection, etc.
from Game.GameLogic import entity

class GameState:
    def __init__(self):
        self.players = []
        self.grid = entity.Grid()